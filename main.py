import cv2
import numpy as np
import matplotlib.pyplot as plt
import operator
import math
# Read the image as grayscale.
img = cv2.imread('sudoku.jpeg')

imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply binary threshold.
# ret, threshold1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# Perform gaussian blur to reduce noise
proc = cv2.GaussianBlur(imgray.copy(), (9, 9), 0)

# Binary adaptive threshold using 11 nearest neighbour pixels.
proc = cv2.adaptiveThreshold(proc,
                             255,
                             cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                             cv2.THRESH_BINARY,
                             11, 2)

# Invert colors
proc = cv2.bitwise_not(proc, proc)
# Find the contours of a binary image
proc, contours, hierarchy = cv2.findContours(proc,
                                             cv2.RETR_EXTERNAL,
                                             cv2.CHAIN_APPROX_SIMPLE)
# Find the contour with the largest area
c = max(contours, key = cv2.contourArea)
# hull = cv2.convexHull(c)
# print(hull)
# Finds the Contour Perimeter
peri = cv2.arcLength(c, True)
print(peri)
# Find the four points for approx contour
approx = cv2.approxPolyDP(c, 0.1 * peri, True)

# Draw all contours on the image
# Remove the array [] to just print the points
cv2.drawContours(img, [approx], -1, (255, 0, 0), 3)
plt.imshow(img, 'gray')
plt.show()

