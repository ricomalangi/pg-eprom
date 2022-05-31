#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose2D
from std_msgs.msg import Bool

# width = 600 and height = 450
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
    
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
rate = rospy.Rate(20)
rospy.Subscriber('/ball_position', Pose2D, callback)
rospy.Subscriber('/dribbler/ball_in_range', Bool, ball_callback)

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
    while True:
        if(data_x > 0 and data_x < 200 and data_y > 0 and data_y < 225):
            print("robot jalan kiri dan mutar")
            kecepatan_badan.linear.x = 0.2
            kecepatan_badan.linear.y = 0.2
            kecepatan_badan.angular.z = 0.2
        elif(data_x > 0 and data_x < 200 and data_y > 225 and data_y < 450):
            print("robot putar kiri")
            kecepatan_badan.linear.x = 0.4
            kecepatan_badan.linear.y = 0.5
            kecepatan_badan.angular.z = 0.5 
        elif(data_x > 200 and data_x < 400 and data_y > 0 and data_y < 225):
            print("robot maju kencang")
            kecepatan_badan.linear.x = 0.2
            kecepatan_badan.linear.y = 0.0
            kecepatan_badan.angular.z = 0
        elif(data_x > 200 and data_x < 400 and data_y > 225 and data_y < 337):
            print("robot maju")
            kecepatan_badan.linear.x = 0.2
            kecepatan_badan.linear.y = 0.0
            kecepatan_badan.angular.z = 0.0
        elif(data_x > 200 and data_x < 400 and data_y > 337 and data_y < 450):
            print("robot stop")
            kecepatan_badan.linear.x = 0.0
            kecepatan_badan.linear.y = 0.0
            kecepatan_badan.angular.z = 0.0
            break
        elif(data_x > 400 and data_x < 600 and data_y > 0 and data_y < 225):
            print("robot jalan kanan dan mutar")
            kecepatan_badan.linear.x = -0.5
            kecepatan_badan.linear.y = -0.5
            kecepatan_badan.angular.z = -0.5
        elif(data_x > 400 and data_x < 600 and data_y > 225 and data_y < 450):
            print('robot putar kanan')
            kecepatan_badan.linear.x = -0.4
            kecepatan_badan.linear.y = -0.5
            kecepatan_badan.angular.z = -0.5
        pub.publish(kecepatan_badan)
        rate.sleep()

def mission_1():
    kecepatan_badan.linear.x = 0.0
    kecepatan_badan.linear.y = 0.8
    kecepatan_badan.angular.z = 0.0
    
    move(kecepatan_badan, rospy.Duration(1.5))

    ball_detection()

if __name__ == '__main__':
    try:
        rospy.init_node('robot_controller')
        while True:
            print("-----KRI 2022-----")
            print("Menu: 1(Mission 1), 2(Mission 2), 3(Mission 3), 4(exit)")
            mission = int(input("Pilih menu: "))
            if mission == 1:
                mission()
            elif mission == 2:
                pass
            elif mission == 3:
                pass
            elif mission == 4:
                break
    except rospy.ROSInterruptException:
        pass
