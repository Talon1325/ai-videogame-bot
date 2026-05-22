import cv2 as cv
import numpy as np
from part9.hsvfilter import Filter

class Detection:
    # Tracker
    TRACKER_BAR = "Trackbars"

    # Properties
    needle_img_path = None
    needle_h = 0
    needle_w = 0
    method = None

    # constructor
    def __init__(self, needle_img_path = None, method = cv.TM_CCOEFF_NORMED):
        if needle_img_path:
            # load image into OpenCV format
            self.needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)

            # Get the width and height of needle image
            self.needle_w = self.needle_img.shape[1]
            self.needle_h = self.needle_img.shape[0]

        # Select which method to use for Match Template
        self.method = method


    # This finds all images that match needle image and draws a rectangle around it 
    # or a point on it and shows the window with the drawings
    # Add max_rectangles to stop process from locking up if too many results are found
    def findRectangles(self, haystack_img, threshold = 0.65, max_rectangles = 10):
        res = cv.matchTemplate(haystack_img, self.needle_img, self.method)

        loc = np.where(res >= threshold) 
        loc = list(zip(*loc[::-1]))

        # Add this check to continue process if no locations are found 
        if not loc:
            return np.array([], dtype=np.int32).reshape(0,4)

        rectangles = []
        for l in loc:
            rect = ([int(l[0]), int(l[1]), self.needle_w, self.needle_h])
            # Want to have atleast 2 rectangles for each image because 
            # group Rectangles needs atleast 2 rectangles to group them
            rectangles.append(rect)
            rectangles.append(rect)
        

        rectangles , weights = cv.groupRectangles(rectangles, groupThreshold = 2, eps = 0.5)
        
        if len(rectangles) > max_rectangles:
            print("Warning too many rectangles found, raise threshold")
            rectangles = rectangles[:max_rectangles]

        return rectangles
    
    def clickPoints(self, rectangles):
        points = []
        
        for (x, y, w, h) in rectangles:
            center_x = x + int(w/2)
            center_y = y + int(h/2)
            points.append((center_x, center_y))
        return points
        

    def drawRectangles(self, haystack_img, rectangles):
        for (x, y, w, h) in rectangles:
            line_color = (0, 255, 0)
            line_type = cv.LINE_4

            top_left = (x, y)
            bottom_right = (x + w, y + h)
            # draw rectangle around image
            cv.rectangle(haystack_img, top_left, bottom_right, line_color, thickness = 2, lineType = line_type)
        return haystack_img


    def drawPoints(self, haystack_img, points):
        marker_color = (255, 0, 255)
        marker_type = cv.MARKER_CROSS

        for x, y in points:
            cv.drawMarker(haystack_img, (x, y), marker_color, markerType = marker_type)

        return haystack_img
    
    def init_control_gui(self):
        cv.namedWindow(self.TRACKER_BAR, cv.WINDOW_NORMAL)

        def nothing(postion):
            pass

        # https://docs.opencv.org/4.x/da/d97/tutorial_threshold_inRange.html
        # Ex: cv.createTrackbar(low_H_name, window_detection_name , low_H, max_value_H, on_low_H_thresh_trackbar)
        # OpenCV scale: Hue: 0 - 179, Saturatiuon: 0 - 255, Value: 0 - 255
        cv.createTrackbar('Low H', self.TRACKER_BAR, 0, 179, nothing)
        cv.createTrackbar('Low S', self.TRACKER_BAR, 0, 255, nothing)
        cv.createTrackbar('Low V', self.TRACKER_BAR, 0, 255, nothing)
        cv.createTrackbar('High H', self.TRACKER_BAR, 0, 179, nothing)
        cv.createTrackbar('High S', self.TRACKER_BAR, 0, 255, nothing)
        cv.createTrackbar('High V', self.TRACKER_BAR, 0, 255, nothing)

        # Set default value for MAX HSV trackbars
        cv.setTrackbarPos('High H', self.TRACKER_BAR, 179)
        cv.setTrackbarPos('High S', self.TRACKER_BAR, 255)
        cv.setTrackbarPos('High V', self.TRACKER_BAR, 255)

        # trackbars for increasing/decreasing saturation and value
        cv.createTrackbar('Add S', self.TRACKER_BAR, 0, 255, nothing)
        cv.createTrackbar('Sub S', self.TRACKER_BAR, 0, 255, nothing)
        cv.createTrackbar('Add V', self.TRACKER_BAR, 0, 255, nothing)
        cv.createTrackbar('Sub V', self.TRACKER_BAR, 0, 255, nothing)

    # returns GUI values of hsv filter object
    def get_hsv_filter_controls(self):
        # Get current postion of all trackbars
        hsv_filter = Filter()
        hsv_filter.low_H = cv.getTrackbarPos('Low H', self.TRACKER_BAR)
        hsv_filter.low_S = cv.getTrackbarPos('Low S', self.TRACKER_BAR)
        hsv_filter.low_V = cv.getTrackbarPos('Low V', self.TRACKER_BAR)
        hsv_filter.high_H = cv.getTrackbarPos('High H', self.TRACKER_BAR)
        hsv_filter.high_S = cv.getTrackbarPos('High S', self.TRACKER_BAR)
        hsv_filter.high_V = cv.getTrackbarPos('High V', self.TRACKER_BAR)
        hsv_filter.add_S = cv.getTrackbarPos('Add S', self.TRACKER_BAR)
        hsv_filter.sub_S = cv.getTrackbarPos('Sub S', self.TRACKER_BAR)
        hsv_filter.add_V = cv.getTrackbarPos('Add V', self.TRACKER_BAR)
        hsv_filter.sub_V = cv.getTrackbarPos('Sub V', self.TRACKER_BAR)
        return hsv_filter
    
    def apply_hsv_filter(self, original_image, hsv_filter = None):
        # convert image to HSV
        hsv = cv.cvtColor(original_image, cv.COLOR_BGR2HSV)

        # if we haven't been given a defined filter, use filter values from the GUI
        if not hsv_filter:
            hsv_filter = self.get_hsv_filter_controls()

        # Add/Sub saturation and value
        h, s, v = cv.split(hsv)
        s = self.shift_channel(s, hsv_filter.add_S)
        s = self.shift_channel(s, -hsv_filter.sub_S)
        v = self.shift_channel(v, hsv_filter.add_V)
        v = self.shift_channel(v, -hsv_filter.sub_V)
        hsv = cv.merge([h, s, v])

        
        # Set min and max HSV values to display
        lower = np.array([hsv_filter.low_H, hsv_filter.low_S, hsv_filter.low_V])
        upper = np.array([hsv_filter.high_H, hsv_filter.high_S, hsv_filter.high_V])
        # Apply the threshold
        # inRange function returns an array of 1s and 0s of positions
        mask = cv.inRange(hsv, lower, upper)
        result = cv.bitwise_and(hsv, hsv, mask=mask)

        # Convert back to BGR
        img = cv.cvtColor(result, cv.COLOR_HSV2BGR)

        return img


    # apply adjustments to an HSV channel if we add too much or too less
    # https://stackoverflow.com/questions/49697363/shifting-hsv-pixel-values-in-python-using-numpy
    def shift_channel(self, c, amount):
        if amount > 0:
            lim = 255 - amount
            c[c >= lim] = 255
            c[c < lim] += amount
        elif amount < 0:
            amount = -amount
            lim = amount
            c[c <= lim] = 0
            c[c > lim] -= amount
        return c
