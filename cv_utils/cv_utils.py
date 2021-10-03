import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import math

GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def draw(img):
    plt.figure(figsize=(10, 10))
    plt.imshow(img, cmap='gray')
    
def Gray(img):
    return cv.cvtColor(img, cv.COLOR_BGR2GRAY)

def TopHat(img, size=(9, 9)):
    width, height = size
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (width, height))
    return cv.morphologyEx(img, cv.MORPH_TOPHAT, kernel)

def Open(img, size=(9, 9)):
    kernel = cv.getStructuringElement(cv.MORPH_RECT, size)
    return cv.morphologyEx(img, cv.MORPH_OPEN, kernel)

def Close(img, size=(9, 9)):
    kernel = cv.getStructuringElement(cv.MORPH_RECT, size)
    return cv.morphologyEx(img, cv.MORPH_CLOSE, kernel)

def AdaptiveThreshold(img):
    thresh = cv.adaptiveThreshold(img, 255, 
                                  cv.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                  thresholdType=cv.THRESH_BINARY_INV,
                                  blockSize=9,
                                  C=5)
    return thresh

def Otsu(img, thresh=127):
    thresh = cv.threshold(img, thresh, 255, cv.THRESH_BINARY|cv.THRESH_OTSU)[1]
    return thresh

def Inverse(img):
    return cv.bitwise_not(img)

def Canny(img):
    return cv.Canny(img.copy(), 50, 200, None, 3)

def Dilate(img, size=(3, 3), kernel=None):
    if kernel is None:
        kernel = cv.getStructuringElement(cv.MORPH_RECT, size)
    return cv.dilate(img, kernel)

def Erode(img, size=(3, 3), kernel=None):
    if kernel is None:
        kernel = cv.getStructuringElement(cv.MORPH_RECT, size)
    return cv.erode(img, kernel)

# nonzeros = cv.findNonZero(thresh)
def MedianBlur(src, size=5):
    return cv.medianBlur(src, size)

def MinAreaRect(contour):
    rect = cv.minAreaRect(contour)
    box = cv.boxPoints(rect)
    cnt = np.int0(box)
    return cnt

# vis = cv.drawContours(img.copy(), [cnt], -1, (0, 255, 0), 1)
# draw(vis)

def FindOuterContour(thresh):
    cnts, _ = cv.findContours(thresh,
                              cv.RETR_LIST,
                              cv.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, 
                  key=cv.contourArea, 
                  reverse=True)
    cnt = None
    for c in cnts:
        # Approximate the contour.
        peri = cv.arcLength(c, True)
        approx = cv.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            cnt = approx
            break
    return cnt

def ExtractContourRegionOfInterest(im, cnt):
    x, y, w, h = cv.boundingRect(cnt)
    roi = im[y:y + h, x:x + w]
    return roi

def DrawContour(img, cnts, color=GREEN, width=1):
    draw(cv.drawContours(img.copy(), cnts, -1, color, width))
    
# def sobelxy(img, ksize=5):
#     sobelx = cv.Sobel(img, cv.CV_64F, 1, 0, ksize)  # x
#     sobely = cv.Sobel(sobelx, cv.CV_64F, 0, 1, ksize)  # y
#     return sobely

def HoughLines(src, color=GREEN, width=2, threshold=200):
    # rho in pixels.
    rho = 1

    # theta in degree.
    theta = np.pi/180

    # The minimum number of intersections to detect a line.
#     threshold = 200

    lines = cv.HoughLines(src, rho, theta, threshold, None, 0, 0)
    if lines is not None:
        for rho, theta in lines[:, 0]:
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))

            cv.line(src, pt1, pt2, color, width, cv.LINE_AA)
    return src


def HoughLinesP(img, color=(255, 255, 255), width=1):
    minLineLength = img.shape[1] * 0.2
    maxLineGap = 10
    lines = cv.HoughLinesP(img, 1, np.pi/180, 100, minLineLength, maxLineGap)
    if lines is None:
        return img
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv.line(img, (x1,y1), (x2,y2), color, width)
    return img

def Laplacian(img):
    laplacian = cv.Laplacian(img, cv.CV_8UC1) # Laplacian Edge Detection
    return laplacian

def Sobel(src):    
    # Sobel on the x-axis helps remove vertical line.
    grad_x = cv.Sobel(src, ddepth=cv.CV_32F, dx=1, dy=0, ksize=-1)
    abs_grad_x = cv.convertScaleAbs(grad_x)
    abs_grad_x = cv.normalize(abs_grad_x, abs_grad_x, 255, 0)

    # Sobel on the y-axis helps remove vertical line.
    grad_y = cv.Sobel(src, ddepth=cv.CV_32F, dx=0, dy=1, ksize=-1)
    abs_grad_y = cv.convertScaleAbs(grad_y)    
    abs_grad_y = cv.normalize(abs_grad_y, abs_grad_y, 255, 0)

    sobel = cv.bitwise_and(abs_grad_x, abs_grad_y)
    return cv.bitwise_and(sobel, src)

def GaussianBlur(src, size=(3, 3)):
    return cv.GaussianBlur(src, size, -1)

def FloodFill(src, point=(0, 0), color=(0, 0, 0)):
    h, w = src.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    
    im_floodfill = src.copy()
    # Floodfill from the given point - typically top left, since we know that would be part of the background.
    cv.floodFill(im_floodfill, mask, point, color)
    
    # Invert floodfilled image.
    im_floodfill_inv = cv.bitwise_not(im_floodfill)
    
    # Combine the two images to get the foreground.
    im_out = src | im_floodfill_inv
    
    return im_out

def ConnectedComponents(src, min_area=10):
    nlabel, labels, stats, centroids = cv.connectedComponentsWithStats(src, connectivity=8)
    for l in range(1, nlabel):
        area = stats[l, cv.CC_STAT_AREA]
        if area <= min_area:
            # CC_STAT_TOP
            # CC_STAT_WIDTH
            # CC_STAT_HEIGHT
            # CC_STAT_AREA
            l, t = stats[l, cv.CC_STAT_LEFT], stats[l, cv.CC_STAT_TOP]
            src = FloodFill(src, point=(t, l), color=(0, 0, 0))
    return src