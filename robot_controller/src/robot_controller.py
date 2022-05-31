#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose2D
from std_msgs.msg import Bool
import time 

# width = 600 and height = 450

rospy.loginfo('init')
print('init')
kecepatan_badan = Twist()
data_x = 0
data_y = 0
status_bola = False

def callback(data):
    global data_x
    global data_y
    data_x = int(data.x)
    data_y = int(data.y)

def ball_callback(msg):
    global status_bola
    status_bola = msg.data


def move(cmd_vel, duration):
    begin_time = rospy.get_time()

    while True:
        current_time = rospy.get_time()
        if(current_time - begin_time < duration.to_sec()):
            pub.publish(cmd_vel)
        else:
            kecepatan_badan.linear.x = 0.0
            kecepatan_badan.linear.y = 0.0


def mission_1():
    kecepatan_badan.linear.x = 0.0
    kecepatan_badan.linear.y = 0.8
    kecepatan_badan.angular.z = 0.0



def run_program():
    print('Initilize publisher')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.init_node('robot_controller')
    rate = rospy.Rate(20)
    rospy.Subscriber('/ball_position', Pose2D, callback)
    rospy.Subscriber('/dribbler/ball_in_range', Bool, ball_callback)
    
    
    while not rospy.is_shutdown():
        global data_x
        global data_y
              

        if(data_x > 0 and data_x < 200 and data_y > 0 and data_y < 225):
            print("robot jalan kiri dan mutar")
            kecepatan_badan.linear.x = 0.4
            kecepatan_badan.linear.y = 0.5
            kecepatan_badan.angular.z = 1
        elif(data_x > 0 and data_x < 200 and data_y > 225 and data_y < 450):
            print("robot putar kiri")
            kecepatan_badan.linear.x = 0.4
            kecepatan_badan.linear.y = 0.8
            kecepatan_badan.angular.z = 0.8 
        elif(data_x > 200 and data_x < 400 and data_y > 0 and data_y < 225):
            print("robot maju kencang")
            kecepatan_badan.linear.x = 0.6
            kecepatan_badan.linear.y = 0
            kecepatan_badan.angular.z = 0
        elif(data_x > 200 and data_x < 400 and data_y > 225 and data_y < 337):
            print("robot maju")
            kecepatan_badan.linear.x = 0.4
            kecepatan_badan.linear.y = 0
            kecepatan_badan.angular.z = 0
        elif(data_x > 200 and data_x < 400 and data_y > 337 and data_y < 450):
            print("robot stop")
            kecepatan_badan.linear.x = 0
            kecepatan_badan.linear.y = -0.8
            kecepatan_badan.angular.z = 0
        elif(data_x > 400 and data_x < 600 and data_y > 0 and data_y < 225):
            print("robot jalan kanan dan mutar")
            kecepatan_badan.linear.x = 0.4
            kecepatan_badan.linear.y = -0.5
            kecepatan_badan.angular.z = -1
        elif(data_x > 400 and data_x < 600 and data_y > 225 and data_y < 450):
            print('robot putar kanan')
            kecepatan_badan.linear.x = 0.4
            kecepatan_badan.linear.y = -0.8
            kecepatan_badan.angular.z = -0.8
        pub.publish(kecepatan_badan)
        rate.sleep()
if __name__ == '__main__':
    try:
        run_program()
    except rospy.ROSInterruptException:
        pass
