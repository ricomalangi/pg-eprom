#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose2D


# width = 600 and height = 450

rospy.loginfo('init')
print('init')
kecepatan_badan = Twist()
data_x = 0
data_y = 0
def callback(data):
    global data_x
    global data_y
    #print(data.x, data.y)
    data_x = int(data.x)
    data_y = int(data.y)

def run_program():
    #global data_x
    #global data_y
    print('Initilize publisher')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.init_node('robot_controller')
    rate = rospy.Rate(20)
    rospy.Subscriber('/ball_position', Pose2D, callback)
    while not rospy.is_shutdown():
        #print(data_x, data_y)
        global data_x
        global data_y
        if(data_x > 0 and data_x < 200 and data_y > 0 and data_y < 450):
            if(data_y < 225):
                print("robot jalan kiri dan mutar")
                kecepatan_badan.linear.x = 0.2
                kecepatan_badan.linear.y = 0.2
                kecepatan_badan.angular.z = 0.2
            else:
                print('robot putar kiri')
                kecepatan_badan.linear.x = 0.4
                kecepatan_badan.linear.y = 0.5
                kecepatan_badan.angular.z = 0.5
        elif(data_x > 200 and data_x < 400 and data_y > 0 and data_y < 450):
            if(data_y < 225):
                print("robot maju kencang")
                kecepatan_badan.linear.x = 0.2
                kecepatan_badan.linear.y = 0
                kecepatan_badan.angular.z = 0
            elif(data_x > 290 and data_x < 350 and data_y > 420 and data_y < 450):
                print('robot stop')
                kecepatan_badan.linear.x = 0
                kecepatan_badan.linear.y = 0
                kecepatan_badan.angular.z = 0
            elif(data_y > 255):
                print('robot maju')
                kecepatan_badan.linear.x = 0.2
                kecepatan_badan.linear.y = 0
                kecepatan_badan.angular.z = 0
        elif(data_x > 400 and data_x < 600 and data_y > 0 and data_y < 450):
            if(data_y < 225):
                print("robot jalan kanan dan mutar")
                kecepatan_badan.linear.x = -0.5
                kecepatan_badan.linear.y = -0.5
                kecepatan_badan.angular.z = -0.5

            else:
                print('robot putar kanan')
                kecepatan_badan.linear.x = -0.4
                kecepatan_badan.linear.y = -0.5
                kecepatan_badan.angular.z = -0.5
        pub.publish(kecepatan_badan)
        rate.sleep()
if __name__ == '__main__':
    try:
        run_program()
    except rospy.ROSInterruptException:
        pass
