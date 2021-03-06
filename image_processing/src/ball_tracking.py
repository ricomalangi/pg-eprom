#!/usr/bin/env python3
# import the necessary packages
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Pose2D
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

# construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-v", "--video", help="path to the (optional) video file")
#ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
#args = vars(ap.parse_args())
# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
orangeLower = (0, 150, 150)
orangeUpper = (10, 255, 255)
bridge = CvBridge()

def run_ball_tracking():
    rospy.loginfo('Initialize node') 
    rospy.init_node('position_tracker')
    pub_position_tracker = rospy.Publisher('ball_position', Pose2D, queue_size=5)
    pub_image = rospy.Publisher('data_image', Image, queue_size=20)
    data_image = Image()
    rate = rospy.Rate(20)

    vs = VideoStream(src=0).start()
    time.sleep(2.0)

    # keep looping
    while not rospy.is_shutdown():
        # grab the current frame
        frame = vs.read()
        
        # handle the frame from VideoCapture or VideoStream
        # if we are viewing a video and we did not grab a frame,
        # then we have reached the end of the video
        if frame is None:
            break
        # resize the frame, blur it, and convert it to the HSV
        # color space
        frame = imutils.resize(frame, width=600)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        cv2.line(frame, (200,0), (200,450), (255,0,0), 2)
        cv2.line(frame, (400,0), (400,450), (255,0,0), 2)
        # construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
    
        mask = cv2.inRange(hsv, orangeLower, orangeUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            # find z position
            data_position_tracker = Pose2D()
            data_position_tracker.x = x
            data_position_tracker.y = y
            pub_position_tracker.publish(data_position_tracker)
            
            print(x,y)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            # only proceed if the radius meets a minimum size
            if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),
                    (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)

        data_image = bridge.cv2_to_imgmsg(frame, "bgr8")
        pub_image.publish(data_image)

        rate.sleep()

    # if we are not using a video file, stop the camera video stream
    
    vs.release()
    # close all windows
    cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        run_ball_tracking()
    except rospy.ROSInterruptException:
        pass

