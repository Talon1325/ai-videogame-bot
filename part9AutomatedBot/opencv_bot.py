from threading import Thread, Lock
from enum import Enum
import time
import pyautogui
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
    # pydirectinput.PAUSE = 0

    stopped = True
    lock = None
    state = None
    MOVEMENT_STOPPED_THRESHOLD = .99

    targets = []
    my_pos = (0,0)
    frame = None
    movement_frame = None

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

        if self.movement_frame is None:
            self.movement_frame = self.frame.copy()

        # # compare the old screenshot to the new screenshot
        # result = cv.matchTemplate(self.frame, self.movement_frame, cv.TM_CCOEFF_NORMED)
        # # we only care about the value when the two screenshots are laid perfectly over one 
        # # another, so the needle position is (0, 0). since both images are the same size, this
        # # should be the only result that exists anyway
        # similarity = result[0][0]
        # print('Movement detection similarity: {}'.format(similarity))

        # if similarity >= self.MOVEMENT_STOPPED_THRESHOLD:
        #     return True
        



        # Using the center of the frame we can find the color 
        # if the color is 120 = blue, then click else continue seraching
        hsv_img = cv.cvtColor(self.movement_frame, cv.COLOR_BGR2HSV)
        hsv_pixel = hsv_img[540,960]
        hue = hsv_pixel[0]
        print(hsv_pixel)
        # if hue == 90:
        #     return True
        # return False

        self.movement_frame = self.frame.copy()
        return False

    def target_found(self):
        # We want to move to the closest target from the last position we clicked on 
        # And since our mouse position is always in the middle, it will be the closest postion
        # to the middle of the screen
        targets = self.targets_ordered_by_distance(self.targets)
        self.offset_x = int(targets[0][0] - self.my_pos[0])
        self.offset_y = int(targets[0][1] - self.my_pos[1])
        # print(self.offset_x, self.offset_y)
        # print(self.my_pos)
        # print(targets[0][0], targets[0][1])

        pydirectinput.move(xOffset = self.offset_x, yOffset = self.offset_y, relative=True)

        # Checks if mouse is on blue target
        if self.on_target():
            return True
        
        # Else keep searching for target
        return False

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
                    pyautogui.click()
                    self.start_click = True
                if time.time() > self.start_time + self.INITIAL_WAIT_TIME:
                    self.lock.acquire()
                    self.state = BotState.SEARCH
                    self.lock.release()

            elif self.state == BotState.SEARCH:
                if self.target_found():
                    self.lock.acquire()
                    self.state = BotState.CLICK
                    self.lock.release()

            elif self.state == BotState.CLICK:
                pydirectinput.click()
                self.lock.acquire()
                self.state = BotState.SEARCH
                self.lock.release()

