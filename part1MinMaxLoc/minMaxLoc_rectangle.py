import cv2 as cv
import os

# Change current working directory to the directory this file is in
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Pull haystack image and needle image into usable variables
haystack_img = cv.imread("Aimlabs_3x3_grid.JPG", cv.IMREAD_UNCHANGED)
needle_img = cv.imread("Aimlabs_3x3_grid_ball.JPG", cv.IMREAD_UNCHANGED)

# Checks every position in the haystack image where the width and height of needle image fit inside the haystack
# Need haystack image, needle image, and the method of conversion
# Return black and white version haystack image where the whitest pionts are matches and darkest locations not matching
res = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCOEFF_NORMED)

# The minimum val is the darkest location of the image or the smallest confidence value of the dataset
# The max val is the whitest location of the image or the largest confidence value of the dataset
# the min and max location return a (x, y) tuple of the locations of the min value and max value on the image
min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
w , h = needle_img.shape[1], needle_img.shape[0]

# max_loc is the top left of the where the needle image is located in the haystack
top_left = max_loc
# add the width and height to the max location to get bottom right corner of the needle image
bottom_right = (max_loc[0] + w, max_loc[1] + h)

# Set a threshold for the the smallest the confidence value of the max value 
threshold = 0.8
if max_val >= threshold:
    # Create a rectangle around location of the needle image
    cv.rectangle(haystack_img, top_left, bottom_right, color = (0,255,0), thickness = 2, lineType = cv.LINE_4)

    # imshow opens window showing the image and the waitkey function waits until a key is pressed to stop process
    cv.imshow('Result', haystack_img) 
    cv.waitKey()

    # Write modified image to a file called minMaxLoc.JPG
    cv.imwrite('minMaxLoc.JPG', haystack_img)
else:
    print("Needle not found")