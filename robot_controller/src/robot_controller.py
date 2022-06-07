#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose2D
from std_msgs.msg import Bool
from pg_msgs.srv import KickBall
from pg_msgs.srv import PrepareKicker
import time

# width = 600 and height = 450
kecepatan_badan = Twist()
data_x = 0
data_y = 0
status_bola = False
stop = False

def callback(data):
    global data_x
    global data_y
    data_x = int(data.x)
    data_y = int(data.y)

def ball_callback(msg):
    global status_bola
    status_bola = msg.data

def stop_callback(msg):
    global stop
    stop = msg.data


def move(cmd_vel, duration):
    begin_time = rospy.get_time()

    while True:
        current_time = rospy.get_time()
        if(current_time - begin_time < duration.to_sec()):
            pub.publish(cmd_vel)

            rate.sleep()
        else:
            kecepatan_badan.linear.x = 0.0
            kecepatan_badan.linear.y = 0.0
            kecepatan_badan.angular.z = 0.0

    

def move(cmd_vel, duration):
    begin_time = rospy.get_time()
    while True:
        current_time = rospy.get_time()
        
        if (current_time - begin_time < duration.to_sec()):
            pub.publish(cmd_vel)

            rate.sleep()
        else:
            kecepatan_badan.linear.x = 0.0
            kecepatan_badan.linear.y = 0.0
            kecepatan_badan.angular.z = 0.0
            break

def ball_detection():
    global data_x
    global data_y
    try:
        while not rospy.is_shutdown():
            if(stop):
                print('robot stop')
                kecepatan_badan.linear.x = 0.0
                kecepatan_badan.linear.y = 0.0
                kecepatan_badan.angular.z = 0.0
                break
            if(data_x > 0 and data_x < 200 and data_y > 0 and data_y < 225):
                print("robot jalan kiri dan mutar")
                kecepatan_badan.linear.x = 0.8
                kecepatan_badan.linear.y = 0.8
                kecepatan_badan.angular.z = 0.8
            elif(data_x > 0 and data_x < 200 and data_y > 225 and data_y < 450):
                print("robot putar kiri")
                kecepatan_badan.linear.x = 0.4
                kecepatan_badan.linear.y = 0.4
                kecepatan_badan.angular.z = 0.4 
            elif(data_x > 200 and data_x < 400 and data_y > 0 and data_y < 225):
                print("robot maju kencang")
                kecepatan_badan.linear.x = 2.5
                kecepatan_badan.linear.y = 0
                kecepatan_badan.angular.z = 0
            elif(data_x > 200 and data_x < 400 and data_y > 225 and data_y < 450):
                print("robot maju")
                kecepatan_badan.linear.x = 0.8
                kecepatan_badan.linear.y = 0.0
                kecepatan_badan.angular.z = 0.0
            elif(data_x > 400 and data_x < 600 and data_y > 0 and data_y < 225):
                print("robot jalan kanan dan mutar")
                kecepatan_badan.linear.x = 0.8
                kecepatan_badan.linear.y = -0.8
                kecepatan_badan.angular.z = -0.8
            elif(data_x > 400 and data_x < 600 and data_y > 225 and data_y < 450):
                print('robot putar kanan')
                kecepatan_badan.linear.x = 0.4
                kecepatan_badan.linear.y = -0.4
                kecepatan_badan.angular.z = -0.4
            pub.publish(kecepatan_badan)
            rate.sleep()
    except KeyboardInterrupt:
        pass

def pass_ball():
    rospy.loginfo('Waiting for kicker')
    rospy.wait_for_service('/kicker/kick')
    try:
        rospy.loginfo('Kicking ball')
        kick_ball = rospy.ServiceProxy('/kicker/kick', KickBall)
        res = kick_ball(True)
        rospy.loginfo('Ball kicked')
        print(res)
    except rospy.ServiceException as e:
        rospy.logerror(e)

def prepare_kicker():
    rospy.loginfo('Waiting for kicker...')
    rospy.wait_for_service('/kicker/prepare_kicker')
    try:
        rospy.loginfo('Preparing...')
        prepare_kicker = rospy.ServiceProxy('/kicker/prepare_kicker', PrepareKicker)
        res = prepare_kicker(8.0)
        rospy.loginfo('Kicker ready!')
        print(res)
    except rospy.ServiceException as e:
        rospy.logerror(e)

def mission_1():
    kecepatan_badan.linear.x = 0.0
    kecepatan_badan.linear.y = 1.6
    kecepatan_badan.angular.z = 0.0
    
    move(kecepatan_badan, rospy.Duration(2.6))

    ball_detection()

    kecepatan_badan.linear.x = 0.0
    kecepatan_badan.linear.y = 0.0
    kecepatan_badan.angular.z = -1.7

    move(kecepatan_badan, rospy.Duration(1))
    time.sleep(1)

    pass_ball()

    prepare_kicker()

if __name__ == '__main__':
    try:
        rospy.init_node('robot_controller')
        rate = rospy.Rate(20)
        pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        rospy.Subscriber('/ball_position', Pose2D, callback)
        rospy.Subscriber('/dribbler/ball_in_range', Bool, ball_callback)
        rospy.Subscriber('/dribbler/ball_in_possession', Bool, stop_callback)
        while True:
            print("-----KRI 2022-----")
            print("Menu: 1(Mission 1), 2(Mission 2), 3(Mission 3), 4(exit)")
            mission = int(input("Pilih menu: "))
            if mission == 1:
                mission_1()
            elif mission == 2:
                ball_detection()
            elif mission == 3:
                pass
            elif mission == 4:
                break
    except rospy.ROSInterruptException:
        pass
