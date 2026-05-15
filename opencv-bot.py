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
detect = Detection("Aimlabs_3x3_grid_ball.JPG")

# Example of static method, not need for self and can call using class name instead of a object of class
# Frame.list_windows()

def main():
    loop_time = time.time()
    while(True):

        frame = framecap.get_frame()
        rectangles = detect.findRectangles(frame, threshold = 0.65)
        frame = detect.drawRectangles(frame, rectangles)
        cv.imshow("Detection", frame)

        # FPS
        print('FPS {}'.format(1 / (time.time() - loop_time)))
        loop_time = time.time()

        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break
    print("Done")



if __name__ == "__main__":
    main()