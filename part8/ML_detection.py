# Author: Talon Vorpahl
# Update my hardcoded bot to shot at targets available instead of shooting at every location in 3x3 grid in aimlabs
import cv2 as cv
import numpy as np
import os
import time
from frame import Frame
from detection import Detection



os.chdir(os.path.dirname(os.path.abspath(__file__)))

framecap = Frame('aimlab_tb')
# load tained model
cascade = cv.CascadeClassifier('cascade/cascade.xml')
# load empty detection
detect = Detection()

# Example of static method, not need for self and can call using class name instead of a object of class
# Frame.list_windows()

def main():

    loop_time = time.time()
    while(True):

        # get updated frame of the game
        frame = framecap.get_frame()

        # Object detection
        rectangles = cascade.detectMultiScale(frame)

        # draw rectangles
        detect_image = detect.drawRectangles(frame, rectangles)

        # Show processed ebject detection 
        cv.imshow("Unprocessed", detect_image)

        # FPS
        print('FPS {}'.format(1 / (time.time() - loop_time)))
        loop_time = time.time()

        # press 'f' to save an image of possible locations 
        # press 'd' to save an image of impossible locations
        # press 'q' to stop loop
        # waits 1 ms every loop to process key presses
        key = cv.waitKey(1)
        if key == ord('q'):
            cv.destroyAllWindows()
            break
        elif key == ord('f'):
            cv.imwrite('positive/{}.jpg'.format(loop_time), frame)
        elif key == ord('d'):
            cv.imwrite('negative/{}.jpg'.format(loop_time), frame)
    print("Done")


if __name__ == "__main__":
    main()