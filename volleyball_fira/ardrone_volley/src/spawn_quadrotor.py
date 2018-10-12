#!/usr/bin/env python
import rospy
from gazebo_msgs.srv import SpawnModel
from geometry_msgs.msg import Pose


rospy.init_node('insert_object',log_level=rospy.INFO)

initial_pose1 = Pose()
initial_pose1.position.x = 2
initial_pose1.position.y = 6
initial_pose1.position.z = 0.05

initial_pose2 = Pose()
initial_pose2.position.x = 1
initial_pose2.position.y = -3
initial_pose2.position.z = 0.05

initial_pose3 = Pose()
initial_pose3.position.x = -2
initial_pose3.position.y = 6
initial_pose3.position.z = 0.05

initial_pose4 = Pose()
initial_pose4.position.x = 1
initial_pose4.position.y = 3
initial_pose4.position.z = 0.05

#f1 = open('../models/quadrotor1/model.sdf','r')
#sdff1 = f1.read()

f2 = open('/home/eve/catkin_ws/src/ardrone_volley/models/quadrotor2/model.sdf','r')
sdff2 = f2.read()

#f3 = open('../models/quadrotor3/model.sdf','r')
#sdff3 = f3.read()

f4 = open('../models/quadrotor4/model.sdf','r')
sdff4 = f4.read()

rospy.wait_for_service('gazebo/spawn_sdf_model')
spawn_model_prox = rospy.ServiceProxy('gazebo/spawn_sdf_model', SpawnModel)
#spawn_model_prox("quadrotor1", sdff1, "myworld", initial_pose1, "world")
spawn_model_prox("quadrotor2", sdff2, "quad2", initial_pose2, "world")
#spawn_model_prox("quadrotor3", sdff3, "myworld", initial_pose3, "world")
spawn_model_prox("quadrotor4", sdff4, "quad4", initial_pose4, "world")

print 'success'
