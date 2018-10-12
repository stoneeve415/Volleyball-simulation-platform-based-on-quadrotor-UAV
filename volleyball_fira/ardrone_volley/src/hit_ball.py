#!/usr/bin/env python
import roslib;
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty

import sys, select, termios, tty

msg = "Enter the key t to start game......"

moveBindings = {
    #   x th y z
    'i':(1,0,0,0),
    'o':(1,-1,0,0),
    'j':(0,1,0,0),
    'l':(0,-1,0,0),
    'u':(1,1,0,0),
    ';':(-1,0,0,0),
    ':':(-1,1,0,0),
    ',':(-1,-1,0,0),
    'h':(0,0,-1,0),
    'm':(0,0,1,0),
    'y':(0,0,0,1),
    'n':(0,0,0,-1),
         }

speedBindings={
    'a':(1.1,1.1),
    'w':(.9,.9),
    'z':(1.1,1),
    'x':(.9,1),
    'e':(1,1.1),
    'c':(1,.9),
        }

def getKey():
  tty.setraw(sys.stdin.fileno())
  select.select([sys.stdin], [], [], 0)
  key = sys.stdin.read(1)
  termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
  return key

speed = 0.1
turn = 0.5

def vels(speed,turn):
  return "currently:\tspeed %s\tturn %s " % (speed,turn)

if __name__=="__main__":
  settings = termios.tcgetattr(sys.stdin)
  
  pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
  takeoff = rospy.Publisher('/ardrone/takeoff', Empty, queue_size=1)
  land = rospy.Publisher('/ardrone/land', Empty, queue_size=1)
  reset = rospy.Publisher('/ardrone/reset', Empty, queue_size=1)
	
  pub2 = rospy.Publisher('quad4/cmd_vel4', Twist, queue_size=1)
  takeoff2 = rospy.Publisher('/ardrone4/takeoff', Empty, queue_size=1)
  land2 = rospy.Publisher('/ardrone4/land', Empty, queue_size=1)
  reset2 = rospy.Publisher('/ardrone4/reset', Empty, queue_size=1)
	
  rospy.init_node('hit_ball')
  x = 0
  th = 0
  y = 0
  z = 0
  status = 0
  twist = Twist()
  try:
    print msg
    print vels(speed,turn)
    while(1):
      key = getKey()
      if (key == 's'):
        takeoff.publish(Empty())
        takeoff2.publish(Empty())
        print "takeoff"
      elif (key == 'e'):
        twist.linear.x = x*speed
        twist.linear.y = -0.5
        twist.linear.z = z*speed
        twist.angular.x = 0; 
        twist.angular.y = 0;
        twist.angular.z = th*turn
        pub.publish(twist)
      elif (key == 'r'):
        twist.linear.x = x*speed
        twist.linear.y = 0.5
        twist.linear.z = z*speed
        twist.angular.x = 0; 
        twist.angular.y = 0;
        twist.angular.z = th*turn
        pub2.publish(twist)
      elif (key == 'd'):
        land.publish(Empty())
        print "land"
      elif (key == 'f'):
        land2.publish(Empty())
        print "land2"
      elif (key == 'c'):			
        twist.linear.x = 0
        twist.linear.y = 0
        twist.linear.z = 0
        twist.angular.x = 0; 
        twist.angular.y = 0;
        twist.angular.z = 0
        pub.publish(twist)
      elif (key == 'v'):
        twist.linear.x = 0
        twist.linear.y = 0
        twist.linear.z = 0
        twist.angular.x = 0; 
        twist.angular.y = 0;
        twist.angular.z = 0
        pub2.publish(twist)
        print "stop2"		
      else:
        if key in moveBindings.keys():
          x = moveBindings[key][0]
          th = moveBindings[key][1]
          y = moveBindings[key][2]
          z = moveBindings[key][3]
        elif key in speedBindings.keys():
          speed = speed * speedBindings[key][0]
          turn = turn * speedBindings[key][1]
          print vels(speed,turn)
          if (status == 14):
            print msg
          status = (status + 1) % 15
        else:
          x = 0
          th = 0
          y = 0
          z = 0
          if (key == '\x03'):
            break
        twist = Twist()
        twist.linear.x = x*speed
        twist.linear.y = y*speed
        twist.linear.z = z*speed
        twist.angular.x = 0; twist.angular.y = 0;
        twist.angular.z = th*turn
        pub.publish(twist)
  except:
    print e
  finally:
    twist = Twist()
    twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
    twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
    pub.publish(twist)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)


