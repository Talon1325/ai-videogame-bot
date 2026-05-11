import cv2 as cv
import numpy as np
import os

# Change current working directory to the directory this file is in
os.chdir(os.path.dirname(os.path.abspath(__file__)))
haystack_img = cv.imread("Aimlabs_3x3_grid.JPG", cv.IMREAD_UNCHANGED)
needle_img = cv.imread("Aimlabs_3x3_grid_ball.JPG", cv.IMREAD_UNCHANGED)
w, h = needle_img.shape[1], needle_img.shape[0]

# Checks every position in haystack image that fit width and height of needle img
# Return black and white version of haystack image where the whitest pionts are matches and darkest locations not matching
res = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCOEFF_NORMED)

# Create numpy array from resulting image to get only the postions where the confidence is higher than threshold
threshold = 0.65
loc = np.where(res >= threshold)

# Create rectangles around positions found in "loc" numpy area
if loc:
    print("Found needle")
    # loc[::-1] - Reverses loc numpy array to get correct x and y coordinate postions
    # *loc[::-1] - Turn result into list of arrays
    # zip(*loc[::-1]) - Packages the coodinate positions into tuples where x is the number within each array 
    # and y is the array being processed. Ex: loc[0] is y = 0, loc[1] is y = 1 and loc[][0] is x = 0, loc[][1] is x = 1
    for rec in zip(*loc[::-1]):
        top_left = rec
        bottom_right = (rec[0] + w, rec[1] + h)
        cv.rectangle(haystack_img, top_left, bottom_right, color = (0,255,0), thickness = 2, lineType = cv.LINE_4)
    
    # Debug
    cv.imshow('Result', haystack_img) 
    cv.waitKey()
    cv.imwrite('MultipleRectangles.JPG', haystack_img)
else:
    print("Needle not found")



