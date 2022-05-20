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
            print('robot belok kiri')
            kecepatan_badan.linear.x = 0.4
            kecepatan_badan.linear.y = 0.4
            kecepatan_badan.angular.z = 0.4
        elif(data_x > 200 and data_x < 400 and data_y > 0 and data_y < 450):
            if(data_x > 250 and data_x < 310 and data_y > 420 and data_y < 460):
                print('robot stop')
                kecepatan_badan.linear.x = 0
                kecepatan_badan.linear.y = 0
                kecepatan_badan.angular.z = 0
            else:
                kecepatan_badan.linear.x = 0.4
                kecepatan_badan.linear.y = 0
                kecepatan_badan.angular.z = 0
                print('robot maju')
        elif(data_x > 400 and data_x < 600 and data_y > 0 and data_y < 450):
            print('robot belok kanan')
            kecepatan_badan.linear.x = -0.4
            kecepatan_badan.linear.y = -0.4
            kecepatan_badan.angular.z = -0.4
        pub.publish(kecepatan_badan)
        rate.sleep()
if __name__ == '__main__':
    try:
        run_program()
    except rospy.ROSInterruptException:
        pass
