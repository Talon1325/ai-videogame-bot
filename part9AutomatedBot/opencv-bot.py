# Author: Talon Vorpahl
# Update my hardcoded bot to shot at targets available instead of shooting at every location in 3x3 grid in aimlabs
import cv2 as cv
import numpy as np
import os
import time
from frame import Frame
from detection import Detection
from hsvfilter import Filter


os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Capture window of the game for object detection
framecap = Frame('aimlab_tb')

# Basic detection
detect = Detection("Aimlabs_3x3_grid_ball.JPG")

# Use this object to test accuracy of detection using hsv filter/thresholding
detect_hsv = Detection("Aimlabs_3x3_grid_ball_processed.JPG")

# GUI control window to change hsv
# detect.init_control_gui()

# HSV settings for best detection
hsv_filter = Filter(0, 219, 0, 132, 255, 255, 0, 0, 0, 128)

# Example of static method, not need for self and can call using class name instead of a object of class
# Frame.list_windows()

def main():

    loop_time = time.time()
    while(True):

        # get updated frame of the game
        frame = framecap.get_frame()

        # hsv filtering for better image detection
        hsv_img = detect_hsv.apply_hsv_filter(frame , hsv_filter)

        # object detection of needle image in frame chosen
        rectangles = detect_hsv.findRectangles(hsv_img, threshold = 0.65)

        # Draw the rectangles around needle in frame
        output_frame = detect_hsv.drawRectangles(frame, rectangles)

        # Show processed ebject detection 
        cv.imshow("Detection", output_frame)

        # FPS
        print('FPS {}'.format(1 / (time.time() - loop_time)))
        loop_time = time.time()

        # press 'q' to stop loop
        # waits 1 ms every loop to process key presses
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break
    print("Done")


if __name__ == "__main__":
    main()