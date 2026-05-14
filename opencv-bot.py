# Author: Talon Vorpahl
# Update my hardcoded bot to shot at targets available instead of shooting at every location in 3x3 grid in aimlabs
import cv2 as cv
import numpy as np
import os
import time
import win32gui, win32ui, win32con
from frame import Frame

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def findPositions(haystack_img, needle_img_path, threshold = 0.65, debug_mode = None):
    # haystack_img_path = cv.imread(haystack_img_path, cv.IMREAD_UNCHANGED)
    needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)
    needle_w , needle_h = needle_img.shape[1], needle_img.shape[0]

    method = cv.TM_CCOEFF_NORMED
    res = cv.matchTemplate(haystack_img, needle_img, method)

    loc = np.where(res >= threshold) 
    loc = list(zip(*loc[::-1]))
    points = []


    rectangles = []
    for rec in loc:
        rectangles.append([int(rec[0]), int(rec[1]), needle_w, needle_h])

    rectangles , weights = cv.groupRectangles(rectangles, groupThreshold = 2, eps = 0.5)

    if len(rectangles):
        # print("Found needle")

        for (x, y, w, h) in rectangles:
            marker_color = (255, 0, 255)
            marker_type = cv.MARKER_CROSS

            line_color = (0, 255, 0)
            line_type = cv.LINE_4

            top_left = (x, y)
            bottom_right = (x + w, y + h)

            center_x = x + int(w/2)
            center_y = y + int(h/2)
            center = (center_x, center_y)
            points.append(center)

            if debug_mode == "rectangles":
                cv.rectangle(haystack_img, top_left, bottom_right, line_color, thickness = 2, lineType = line_type)

            if debug_mode == "points":
                cv.drawMarker(haystack_img, center, marker_color, markerType = marker_type)

        if debug_mode:
            cv.imshow("Video", haystack_img)
             
        return points


def main():

    framecap = Frame('aimlab_tb')

    loop_time = time.time()
    while(True):

        frame = framecap.get_frame()
        needle_img_path = "Aimlabs_3x3_grid_ball.JPG"
        points = findPositions(frame, needle_img_path, threshold = 0.65, debug_mode = "rectangles")

        # cv.imshow('Video', frame)

        # FPS
        print('FPS {}'.format(1 / (time.time() - loop_time)))
        loop_time = time.time()

        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break
    print("Done")



if __name__ == "__main__":
    main()