# Author: Talon Vorpahl
# Update my hardcoded bot to shot at targets available instead of shooting at every location in 3x3 grid in aimlabs
import cv2 as cv
import numpy as np
import os
import time
from frame import Frame

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def main():
    window = 'aimlab_tb'
    framecap = Frame(window)
    
    loop_time = time.time()
    while(True):

        frame = framecap.get_frame()

        cv.imshow('Video', frame)

        # FPS
        print('FPS {}'.format(1 / (time.time() - loop_time)))
        loop_time = time.time()

        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break
    print("Done")



if __name__ == "__main__":
    main()