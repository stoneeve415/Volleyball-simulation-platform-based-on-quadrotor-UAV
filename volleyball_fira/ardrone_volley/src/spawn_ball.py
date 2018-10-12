#!/usr/bin/env python
import rospy
from gazebo_msgs.srv import GetModelState
from gazebo_msgs.srv import SpawnModel
from geometry_msgs.msg import Pose


rospy.init_node('insert_object',log_level=rospy.INFO)

initial_pose1 = Pose()
initial_pose1.position.x = 2
initial_pose1.position.y = -2
initial_pose1.position.z = 4

initial_pose2 = Pose()
initial_pose2.position.x = 0
initial_pose2.position.y = -1
initial_pose2.position.z = 4

f1 = open('../models/ball1/model.sdf','r')
sdff1 = f1.read()

f2 = open('../models/volleyball/model.sdf','r')
sdff2 = f2.read()

rospy.wait_for_service('gazebo/spawn_sdf_model')
spawn_model_prox = rospy.ServiceProxy('gazebo/spawn_sdf_model', SpawnModel)
#spawn_model_prox("ball1", sdff1, "myworld", initial_pose1, "world")
spawn_model_prox("volleyball", sdff2, "myworld", initial_pose2, "world")


#get ball message
model_coordinates = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
ballName='volleyball'
ball_link_name='link_0'
start =rospy.get_rostime()
now = rospy.get_rostime()
while (now - start) <  rospy.Duration(10,0):
	ball = model_coordinates(ballName,'')
	print ball.pose.position.z
	rospy.sleep(0.25)
	now = rospy.get_rostime()
