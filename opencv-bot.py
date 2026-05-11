# Author: Talon Vorpahl
# Update my hardcoded bot to shot at targets available instead of shooting at every location in 3x3 grid in aimlabs
import cv2 as cv
import numpy as np
import os
import pyautogui

os.chdir(os.path.dirname(os.path.abspath(__file__)))
haystack_img = cv.imread("Aimlabs_3x3_grid.JPG", cv.IMREAD_UNCHANGED)
needle_img = cv.imread("Aimlabs_3x3_grid_ball.JPG", cv.IMREAD_UNCHANGED)
w , h = needle_img.shape[1], needle_img.shape[0]

res = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCOEFF_NORMED)
threshold = 0.65
loc = np.where(res >= threshold)

if loc :
    print("Found needle")
    for rec in zip(*loc[::-1]):
        top_left = rec
        bottom_right = (rec[0] + w, rec[1] + h)
        cv.rectangle(haystack_img, top_left, bottom_right, color = (0,255,0), thickness = 2, lineType = cv.LINE_4)
    
    cv.imshow('Result', haystack_img) 
    cv.waitKey()
    cv.imwrite('MultipleRectangles.JPG', haystack_img)
else:
    print("Needle not found")

# Debug
# cv.imshow('Result', haystack_img) 
# cv.waitKey()
# cv.imwrite('MultipleRectangles.JPG', haystack_img)




def main():
    pass



if __name__ == "__main__":
    main()