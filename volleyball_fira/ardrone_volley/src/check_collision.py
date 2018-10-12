#!/usr/bin/env python
import rospy
from gazebo_msgs.msg import ContactsState

def callback(data):
	if not len(data.states)==0:
		print data.states[0].collision2_name

def listener():
    rospy.init_node('check_collision', anonymous=True)
    rospy.Subscriber('myworld/ball_contact_sensor_state', ContactsState, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()