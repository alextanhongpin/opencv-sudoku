import numpy as np
import cv2 as cv

def order_points(pts):
    # Initialize a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top right, the third is the 
    # bottom-right, and the fourth is the bottom-left.
    rect = np.zeros((4, 2), dtype=np.float32)
    
    # The top-left will have the smallest sum, whereas
    # the bottom-right will have the largest sum.
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    
    # Now, compute the difference between the points,
    # the top right will have the smallest difference,
    # whereas the bottom-left will have the largest difference.
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    
    return rect

def four_point_transform(img, pts):
    rect = order_points(pts)
    print(rect)

    tl, tr, br, bl = rect
    
    # Compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordinates or the top-right and top-left x-coordinates.
    width_a = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    width_b = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    max_width = max(int(width_a), int(width_b))
    
    # Compute the height of the new image, which will be the maximum 
    # distance betwen the top-right and bottom-right y-coordinates or 
    # the top-left and bottom-left y-coordinates.
    height_a = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    height_b = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    max_height = max(int(height_a), int(height_b))
    
    dst = np.array([[0, 0],
                    [max_width - 1, 0],
                    [max_width - 1, max_height - 1],
                    [0, max_height - 1]], dtype=np.float32)
    
    # Compute the perspective transform matrix and apply it.
    M = cv.getPerspectiveTransform(rect, dst)
    return cv.warpPerspective(img, M, (max_width, max_height))
    
    