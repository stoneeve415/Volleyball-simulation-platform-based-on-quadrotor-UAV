#!/usr/bin/env python
from gazebo_msgs.srv import GetModelState
from gazebo_msgs.srv import SpawnModel
from gazebo_msgs.srv import DeleteModel
from gazebo_msgs.srv import SetModelState
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
from gazebo_msgs.msg import ContactsState
from gazebo_msgs.msg import ModelState
from std_srvs.srv import Empty as EM
from geometry_msgs.msg import Pose
import sys, select, termios, tty


class Game:

	def __init__(self):
		rospy.init_node('begin_game')
		self.floor_collision_name='volleyfloor::field::collision'
		self.ballName='volleyball'
		self.ball_link_name='link_0'
		self.quadName2='quadrotor2'
		self.quad_link_name2='quadrotor2::base_link::hit_collision'
		self.quadName4='quadrotor4'
		self.quad_link_name4='quadrotor4::base_link_4::hit_collision'
		self.ball=''
		self.ball_contact=''
		self.teamALastHit=0
		self.teamBLastHit=0
		self.roundFinishTime=0
		self.scoreA=0
		self.scoreB=0
		self.round=0
		self.is_contact=False
		self.hit_times=0
		
		
		#banner init position
		banner_pose1 = Pose()
		banner_pose1.position.x = -2
		banner_pose1.position.y = -0.28
		banner_pose1.position.z = 1

		banner_pose2 = Pose()
		banner_pose2.position.x = -2
		banner_pose2.position.y = 0.28
		banner_pose2.position.z = 1

		self.left_banner_pos=banner_pose1
		self.right_banner_pos=banner_pose2

		#quadrotor init position
		initial_pose2 = Pose()
		initial_pose2.position.x = 1
		initial_pose2.position.y = -3
		initial_pose2.position.z = 0.05

		initial_pose4 = Pose()
		initial_pose4.position.x = 1
		initial_pose4.position.y = 3
		initial_pose4.position.z = 0.05
		self.Quada_pos=initial_pose2
		self.Quadb_pos=initial_pose4

		#ball init position
		#ADD A VIRTUAL BALL BUT YOU CANNOT SEE IN THE DEFAULT VIEW
		initial_pose = Pose()
		initial_pose.position.x = 0
		initial_pose.position.y = -20
		initial_pose.position.z = 20
		self.ball_pos=initial_pose

		self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
		self.takeoff = rospy.Publisher('/ardrone/takeoff', Empty, queue_size=1)
		self.land = rospy.Publisher('/ardrone/land', Empty, queue_size=1)
		self.reset = rospy.Publisher('/ardrone/reset', Empty, queue_size=1)

		self.pub4 = rospy.Publisher('quad4/cmd_vel4', Twist, queue_size=1)
		self.takeoff4 = rospy.Publisher('/ardrone4/takeoff', Empty, queue_size=1)
		self.land4 = rospy.Publisher('/ardrone4/land', Empty, queue_size=1)
		self.reset4 = rospy.Publisher('/ardrone4/reset', Empty, queue_size=1)
		
		rospy.Subscriber('myworld/ball_contact_sensor_state', ContactsState, self.getcollsion)

		self.addobjects()
		print 'init finished'
	def getcollsion(self,data):
		if not len(data.states)==0 and self.is_contact:
			self.ball_contact=data.states[0].collision2_name

	#get the keyboard input
	def getKey(self,settings):	
		tty.setraw(sys.stdin.fileno())
		select.select([sys.stdin], [], [], 0)
		key = sys.stdin.read(1)
		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
		return key
	
	#main loop
	def begin_game(self):	
		#get ball state
		rospy.wait_for_service('/gazebo/get_model_state')
		ball_coordinates = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
		self.ball=ball_coordinates(self.ballName,'')
		#if ball appear in playground
		if abs(self.ball.pose.position.y) <=15:
			#if ball contact with quadrotor2
			if self.ball_contact == self.quad_link_name2:
				print 'team A hit'
				self.teamALastHit=1
				self.teamBLastHit=0
				self.ball_contact=''
				self.hit_times=self.hit_times+1
			#if ball contact with quadrotor4
			if self.ball_contact == self.quad_link_name4:
				print 'team B hit'
				self.teamALastHit=0
				self.teamBLastHit=1
				self.ball_contact=''
				self.hit_times=self.hit_times+1
			#if ball contact with floor
			if self.ball_contact == self.floor_collision_name:
				print 'hit floor'
				self.is_contact=False
				self.ball_contact=''
				self.calculatefloorscore()
				rospy.sleep(1)
				self.hit_times=0
			#if ball out playground
			if self.checkballout() == 1:
				self.calculateballoutscore()
				self.hit_times=0
			#if quadrotor2 out playground
			if self.checkquadaout() == 1:
				self.calculatequadoutscore(1)
				self.hit_times=0
			#if quadrotor4 out playground
			if self.checkquadbout() == 1:
				self.calculatequadoutscore(2)
				self.hit_times=0
			#if quadrotor hit ball times more than 5
			if self.hit_times > 5:
				if self.teamALastHit == 1:
					self.calculatequadoutscore(1)
				else:
					self.calculatequadoutscore(2)
		else:
			print 'Please enter key s to start a round ...'
			settings = termios.tcgetattr(sys.stdin)
			key = self.getKey(settings)
			if (key == 's'):
				self.addball()
		
	def addobjects(self):
		#UPDATE THE BANNER
		#del_banner_prox = rospy.ServiceProxy('gazebo/delete_model', DeleteModel)
		#del_banner_prox('gradebanner')
		
		#ADD A VIRTUAL BALL BUT YOU CANNOT SEE IN THE DEFAULT VIEW
		f = open('../models/volleyball/model.sdf','r')
		sdff = f.read()
		rospy.wait_for_service('gazebo/spawn_sdf_model')
		spawn_model_prox = rospy.ServiceProxy('gazebo/spawn_sdf_model', SpawnModel)
		spawn_model_prox("volleyball", sdff, "myworld", self.ball_pos, "world")
		
		#ADD QUADROTOR
		spawn_model_prox = rospy.ServiceProxy('gazebo/spawn_sdf_model', SpawnModel)
		ff1 = open('../models/gradebanner0/model.sdf','r')
		sdff1 = ff1.read()
		ff2 = open('../models/_gradebanner0/model.sdf','r')
		sdff2 = ff2.read()
		spawn_model_prox("gradebanner0", sdff1, "myworld", self.left_banner_pos, "world")
		spawn_model_prox("_gradebanner0", sdff2, "myworld", self.right_banner_pos, "world")
		#SPAWN TWO ARDRONE
		f2 = open('../models/quadrotor2/model.sdf','r')
		sdf2 = f2.read()
		f4 = open('../models/quadrotor4/model.sdf','r')
		sdf4 = f4.read()
		#spawn_model_prox("quadrotor1", sdff1, "myworld", initial_pose1, "world")
		spawn_model_prox("quadrotor2", sdf2, "myworld", self.Quada_pos, "world")
		#spawn_model_prox("quadrotor3", sdff3, "myworld", initial_pose3, "world")
		spawn_model_prox("quadrotor4", sdf4, "myworld", self.Quadb_pos, "world")
		rospy.sleep(0.5)
		
		#SEND ARDRONE TAKEOFF
		self.takeoff.publish(Empty())
		self.takeoff4.publish(Empty())   
		
	def checkround(self):
		self.round = self.round + 1
		self.resetobjects()
	

	def resetobjects(self):
		self.land.publish(Empty())
		self.land4.publish(Empty())
		#del_ball_prox = rospy.ServiceProxy('gazebo/delete_model', DeleteModel)
		#del_ball_prox('volleyball')
		#reset world
		rospy.wait_for_service('/gazebo/reset_world')
		reset_world = rospy.ServiceProxy('/gazebo/reset_world', EM)
		#invoke
		reset_world()
		
		#reset ball
		rospy.wait_for_service('/gazebo/set_model_state')
		set_model_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
		model_state = ModelState()
		model_state.model_name = 'volleyball'
		model_state.pose= self.ball_pos
		model_state.reference_frame = 'world'
		set_model_state(model_state)
		
		#UPDATE BANNER
		rospy.wait_for_service('gazebo/spawn_sdf_model')
		spawn_baner_prox = rospy.ServiceProxy('gazebo/spawn_sdf_model', SpawnModel)
		banner_left="gradebanner"+str(self.scoreA)
		banner_right="_gradebanner"+str(self.scoreB)
		print banner_left
		print banner_right
		fn1='../models/'+banner_left+'/model.sdf'
		fn2='../models/'+banner_right+'/model.sdf'
		ff1 = open(fn1,'r')
		sdff1 = ff1.read()
		ff2 = open(fn2,'r')
		sdff2 = ff2.read()
		spawn_baner_prox(banner_left, sdff1, "myworld", self.left_banner_pos, "world")
		spawn_baner_prox(banner_right, sdff2, "myworld", self.right_banner_pos, "world")
		rospy.sleep(0.5)
		self.takeoff.publish(Empty())
		self.takeoff4.publish(Empty())
		rospy.sleep(0.5)
		



	def addball(self):
		print 'spawn a volley ball'
		initial_pose1 = Pose()
		initial_pose1.position.x = 0
		initial_pose1.position.y = 1
		initial_pose1.position.z = 4

		initial_pose2 = Pose()
		initial_pose2.position.x = 0
		initial_pose2.position.y = -1
		initial_pose2.position.z = 4
 		rospy.wait_for_service('/gazebo/set_model_state')
		set_model_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
		model_state = ModelState()
		model_state.model_name = 'volleyball'
		if (self.round % 2 == 0):
			model_state.pose= initial_pose2
		else:
			model_state.pose= initial_pose1
		model_state.reference_frame = 'world'
		set_model_state(model_state)
		rospy.sleep(0.1)
		self.is_contact=True
		

	def checkballout(self):
		ballout = 0
		if self.ball.pose.position.x > 2 or self.ball.pose.position.x < -2:
			ballout = 1
		elif self.ball.pose.position.y > 4 or self.ball.pose.position.y < -4:
			ballout = 1
		elif self.ball.pose.position.z > 6:
			ballout = 1
		return ballout
	
	def checkquadaout(self):
		quada_coordinates = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
		quada=quada_coordinates(self.quadName2,'')
		quadAOut = 0
		if quada.pose.position.x > 2 or  quada.pose.position.x<-2:
			quadAOut = 1
		elif quada.pose.position.y > 4 or  quada.pose.position.y < -4:
			quadAOut = 1
		elif quada.pose.position.z > 6:
			quadAOut = 1
		return quadAOut

	def checkquadbout(self):
		quadb_coordinates = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
		quadb=quadb_coordinates(self.quadName4,'')
		quadBOut = 0
		if quadb.pose.position.x > 2 or  quadb.pose.position.x<-2:
			quadBOut = 1
		elif quadb.pose.position.y > 4 or  quadb.pose.position.y < -4:
			quadBOut = 1
		elif quadb.pose.position.z > 6:
			quadBOut = 1
		return quadBOut
	
	def calculatefloorscore(self):
		banner_left="gradebanner"+str(self.scoreA)
		banner_right="_gradebanner"+str(self.scoreB)
		del_banne_prox = rospy.ServiceProxy('gazebo/delete_model', DeleteModel)
		# which quad was the last one that touched the ball ?
		if self.teamALastHit == 1:
			if self.ball.pose.position.y <= 0:
				self.scoreB = self.scoreB + 1
			else:
				self.scoreA = self.scoreA + 1
		elif self.teamBLastHit == 1:
			if self.ball.pose.position.y >= 0:
				self.scoreA = self.scoreA + 1
			else:
				self.scoreB = self.scoreB + 1
		else:
			if self.ball.pose.position.y >= 0:
				self.scoreA = self.scoreA + 1
			else:
				self.scoreB = self.scoreB + 1
			print str(self.scoreA)+':' +str(self.scoreB)
		rospy.sleep(5)
		del_banne_prox(banner_left)
		del_banne_prox(banner_right)
		self.checkround()
		
	def calculateballoutscore(self):
		banner_left="gradebanner"+str(self.scoreA)
		banner_right="_gradebanner"+str(self.scoreB)
		if self.teamALastHit == 1:
			self.scoreB = self.scoreB + 1 
		elif self.teamBLastHit == 1:
			self.scoreA = self.scoreA + 1
		else:
			if self.round%2==0:
				self.scoreB = self.scoreB + 1
			else:
				self.scoreA = self.scoreA + 1
		del_banne_prox(banner_left)
		del_banne_prox(banner_right)
		self.checkround()
	

	def calculatequadoutscore(self,i):
		banner_left="gradebanner"+str(self.scoreA)
		banner_right="_gradebanner"+str(self.scoreB)
		if i == 1:
			self.scoreB = self.scoreB + 1
		elif i == 2:
			self.scoreA = self.scoreA + 1
		del_banne_prox(banner_left)
		del_banne_prox(banner_right)
		self.checkround()
if __name__=='__main__':
	game=Game()
	while not rospy.is_shutdown():
		game.begin_game()

