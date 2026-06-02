from threading import Thread, Lock
from enum import Enum
import time
import math
import pydirectinput
import numpy as np
import cv2 as cv


# Utilize this github to formulate this class\
# https://github.com/learncodebygaming/opencv_tutorials/blob/master/009_bot/bot.py#L207


class BotState(Enum):
    INITIALIZE = 0
    SEARCH = 1
    CLICK = 2


class Bot:
    # Disable the built-in delay for maximum throughput execution
    pydirectinput.PAUSE = 0.001

    stopped = True
    lock = None
    state = None

    targets = []
    my_pos = (0,0)
    frame = None
    movement_frame = None
    hsv_img = None
    hue = 0
    target = []

    window_offset = (0,0)
    w = 0
    h = 0
    offset_x = 0
    offset_y = 0

    start_time = 0
    # takes 5 seconds after first click for game to start
    INITIAL_WAIT_TIME = 5
    # Game lasts for 30 seconds
    GAME_TIME = 30
    start_click = False

    def __init__(self):
        # create the thread lock object
        self.lock = Lock()
        # initial the state of the bot
        self.state = BotState.INITIALIZE
        self.w = 1920
        self.h = 1080

        # our character is always in the center of the screen
        self.my_pos = (960, 540)

        self.start_time = time.time()

    # This function will check if the player is on the target
    def on_target(self):
        # Using the center of the frame we can find the color 
        # if the color is 120 = blue, then click else continue seraching
        hsv_pixel = self.hsv_img[540,960]
        sat = hsv_pixel[1]
        val = hsv_pixel[2]
        self.hue = hsv_pixel[0]
        # inrange = self.offset_x >= -2 and self.offset_x <= 2 and self.offset_y >= -2 and self.offset_y <= 2
        if self.hue == 120:
            # self.offset_x = self.offset_x/20
            # self.offset_y = self.offset_y/20
            return True
        return False

    def target_search(self):
        # We want to move to the closest target from the last position we clicked on 
        # And since our mouse position is always in the middle, it will be the closest postion
        # to the middle of the screen
        targets = self.targets_ordered_by_distance(self.targets)
        target = targets[0]
        self.offset_x = int((target[0] - self.my_pos[0])/40)
        self.offset_y = int((target[1] - self.my_pos[1])/40)


        pydirectinput.move(xOffset = self.offset_x, yOffset = self.offset_y, relative=True)

        # Checks if mouse is on blue target
        if self.on_target():
            pydirectinput.click(interval=0.3)
        # Else keep searching for target



    def targets_ordered_by_distance(self, targets):

        # searched "python order points by distance from point"
        # simply uses the pythagorean theorem
        # https://stackoverflow.com/a/30636138/4655368
        def pythagorean_distance(pos):
            return math.sqrt((pos[0] - self.my_pos[0])**2 + (pos[1] - self.my_pos[1])**2)
        targets.sort(key=pythagorean_distance)

        return targets

    # translate a pixel position on a screenshot image to a pixel position on the screen.
    # pos = (x, y)
    # WARNING: if you move the window being captured after execution is started, this will
    # return incorrect coordinates, because the window position is only calculated in
    # the WindowCapture __init__ constructor.
    def get_screen_position(self, pos):
        return (pos[0] + self.window_offset[0], pos[1] + self.window_offset[1])

    def update_targets(self, targets):
        self.lock.acquire()
        self.targets = targets
        self.lock.release()

    def update_frame(self, frame):
        self.lock.acquire()
        self.frame = frame
        self.hsv_img = cv.cvtColor(self.frame, cv.COLOR_BGR2HSV)
        self.lock.release()

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped and time.time() < self.start_time + self.INITIAL_WAIT_TIME + self.GAME_TIME:
            
            if self.state == BotState.INITIALIZE:
                if not self.start_click:
                    pydirectinput.click()
                    self.start_click = True
                if time.time() > self.start_time + self.INITIAL_WAIT_TIME:
                    self.lock.acquire()
                    self.state = BotState.SEARCH
                    self.lock.release()

            elif self.state == BotState.SEARCH:
                self.target_search()




