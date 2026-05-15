import cv2 as cv
import numpy as np

class Detection:
    needle_img_path = None
    needle_h = 0
    needle_w = 0
    method = None

    # constructor
    def __init__(self, needle_img_path, method = cv.TM_CCOEFF_NORMED):
        # load image into OpenCV format
        self.needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)
        # Get the width and height of needle image
        self.needle_w = self.needle_img.shape[1]
        self.needle_h = self.needle_img.shape[0]
        # Select which method to use for Match Template
        self.method = method


    # This finds all images that match needle image and draws a rectangle around it 
    # or a point on it and shows the window with the drawings
    def findRectangles(self, haystack_img, threshold = 0.65):
        res = cv.matchTemplate(haystack_img, self.needle_img, self.method)

        loc = np.where(res >= threshold) 
        loc = list(zip(*loc[::-1]))

        rectangles = []
        for l in loc:
            rect = ([int(l[0]), int(l[1]), self.needle_w, self.needle_h])
            # Want to have atleast 2 rectangles for each image because 
            # group Rectangles needs atleast 2 rectangles to group them
            rectangles.append(rect)
            rectangles.append(rect)

        rectangles , weights = cv.groupRectangles(rectangles, groupThreshold = 2, eps = 0.5)
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