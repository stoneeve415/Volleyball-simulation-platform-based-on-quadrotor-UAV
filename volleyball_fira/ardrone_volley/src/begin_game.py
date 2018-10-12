#!/usr/bin/env python
from gazebo_msgs.srv import GetModelState
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
#pub = rospy.Publisher('quad2/cmd_vel2', Twist, queue_size=1)
#land = rospy.Publisher('/ardrone2/land', Empty, queue_size=1)
#takeoff = rospy.Publisher('/ardrone2/takeoff', Empty, queue_size=1)
#takeofff = rospy.Publisher('/ardrone4/takeoff', Empty, queue_size=1)
#reset = rospy.Publisher('/ardrone2/reset', Empty, queue_size=1)

pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
land = rospy.Publisher('/ardrone/land', Empty, queue_size=1)
takeoff = rospy.Publisher('/ardrone/takeoff', Empty, queue_size=1)
takeofff = rospy.Publisher('/ardrone4/takeoff', Empty, queue_size=1)
reset = rospy.Publisher('/ardrone/reset', Empty, queue_size=1)
rospy.init_node('begin_game')
model_coordinates = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)

#get ball message
ballName='volleyball'
ball_link_name='link_0'

#get quadrotor message
quadName='quadrotor2'
quad_link_name='base_link'


rospy.sleep(1)
speed=5
start_time =rospy.get_rostime()
ishit=False
while not rospy.is_shutdown():
    ball = model_coordinates(ballName,'')
    curent = rospy.get_rostime()
    if (curent - start_time) <  rospy.Duration(1,0):
        takeoff.publish(Empty())
        takeofff.publish(Empty())

    else:
	if ball.success == True and not ishit:# and False:
		quad = model_coordinates(quadName,'')
		dx=ball.pose.position.x-quad.pose.position.x
		dy=ball.pose.position.y-quad.pose.position.y
		print ball.pose.position.x
		print ball.pose.position.y
		print quad.pose.position.x
		print quad.pose.position.y
		print dx
		print dy
		twist = Twist()
		twist.linear.x = 0#0.008
		twist.linear.y = 0#0.04
		twist.linear.z = 2#0.04
		twist.angular.x = 0; 
		twist.angular.y = 0;
		twist.angular.z = 0
		pub.publish(twist)
		rospy.sleep(0.55)
		twist = Twist()
		twist.linear.x = -2
		twist.linear.y = 2
		twist.linear.z = 0
		twist.angular.x = 0; 
		twist.angular.y = 0;
		twist.angular.z = 0
		pub.publish(twist)
		rospy.sleep(0.5)
		twist = Twist()
		twist.linear.x = 0
		twist.linear.y = 2
		twist.linear.z = 0
		twist.angular.x = 0; 
		twist.angular.y = 0;
		twist.angular.z = 0
		pub.publish(twist)
		rospy.sleep(0.5)
		twist = Twist()
		twist.linear.x = 0#0.008
		twist.linear.y = 0#0.04
		twist.linear.z = 0#0.04
		twist.angular.x = 0; 
		twist.angular.y = 0;
		twist.angular.z = 0
		pub.publish(twist)
		ishit=True
	elif False:
		twist = Twist()
		twist.linear.x = 2
		twist.linear.y = 0
		twist.linear.z = 0
		twist.angular.x = 0; 
		twist.angular.y = 0;
		twist.angular.z = 0
		pub.publish(twist)
		start =rospy.get_rostime()
		now = rospy.get_rostime()
		while (now - start) <  rospy.Duration(10,0):
			now = rospy.get_rostime()
			quad = model_coordinates(quadName,'')
			print quad.pose.position.x
			rospy.sleep(1)

		
