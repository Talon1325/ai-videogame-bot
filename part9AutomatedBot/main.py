# Author: Talon Vorpahl
# Update my hardcoded bot to shot at targets available instead of shooting at every location in 3x3 grid in aimlabs
import cv2 as cv
import os
import time
from frame import Frame
from detection import Detection
from opencv_bot import Bot, BotState



os.chdir(os.path.dirname(os.path.abspath(__file__)))
time.sleep(3)


# Capture window of the game for object detection
framecap = Frame('aimlab_tb')

# Basic detection
detect = Detection("Aimlabs_3x3_grid_ball.JPG")

# Use this object to test accuracy of detection using hsv filter/thresholding
detect_hsv = Detection("Aimlabs_3x3_grid_ball_processed.JPG")
#hsv_filter = Filter(0, 219, 0, 132, 255, 255, 0, 0, 0, 128)

# Assign Bot obeject for bot actions
bot = Bot()

# GUI control window to change hsv
# detect.init_control_gui()

# Example of static method, not need for self and can call using class name instead of a object of class
# Frame.list_windows()

framecap.start()
detect_hsv.start()
bot.start()

def main():
    DEBUG = True

    loop_time = time.time()
    while(True):

        # If no frame at the moment continue through loop
        if framecap.frame is None:
            continue
        
        # Update the frame for object detection, rectangles are located when thread starts
        detect_hsv.update(framecap.frame)
        
        targets = detect_hsv.clickPoints(detect_hsv.rectangles)
        bot.update_targets(targets)
        bot.update_frame(detect_hsv.frame)

        # # Bot states and actions
        # if bot.state == BotState.INITIALIZE:
        #     # Collect the click points and update the targets locations for bot while initializing
        #     bot.update_targets(targets)
        #     bot.update_frame(framecap.frame)

        # elif bot.state == BotState.SEARCH:
        #     # When searching the bot needs the next set of click points, 
        #     bot.update_targets(targets)
        #     # and the next frame
        #     bot.update_frame(framecap.frame)

        # elif bot.state == BotState.CLICK:
        #     # For 100% accuracy don't click until mouse is at location
        #     bot.update_targets(targets)
        #     bot.update_frame(framecap.frame)
            


        if DEBUG:
            # Draw the rectangles around needle in frame
            output_frame = detect_hsv.drawRectangles(detect_hsv.frame, detect_hsv.rectangles)

            # Show processed ebject detection 
            cv.imshow("Detection", detect_hsv.frame)
            # Try mose call back to get color of mouse postion



        # FPS
        print('FPS {}'.format(1 / (time.time() - loop_time)))
        loop_time = time.time()

        # press 'q' to stop loop
        # waits 1 ms every loop to process key presses
        if cv.waitKey(1) == ord('q'):
            framecap.stop()
            detect_hsv.stop()
            bot.stop()
            cv.destroyAllWindows()
            break
    print("Done")


if __name__ == "__main__":
    main()