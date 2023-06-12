import cv2
import numpy as np
from backend.security import create_random_name
import os

# check if ada path (makin close to solution) ( ga perlu tapi isi aja)
os.environ['LD_LIBRARY_PATH']="/home/ravindrawiguna/.local/lib/"

# mamamia please work
import ctypes; ctypes.cdll.LoadLibrary('/home/ravindrawiguna/.local/lib/libtbb.so.12');

# do something drastic ( closer to solution)
# print("DRASTICC v after ctypes")
# from numba.np.ufunc import tbbpool as tryingsohard

from numba import config
# from numba import threading_layer

# set the threading layer before any parallel target compilation
# config.THREADING_LAYER = 'threadsafe'
# config.THREADING_LAYER = 'tbb'
# config.THREADING_LAYER = 'workqueue'
config.THREADING_LAYER = 'safe'
# config.THREADING_LAYER = 'forksafe'

# print('YO PLEASE BE SAFE')
# print("Threading layer chosen:", threading_layer())

import largestinteriorrectangle as lir
import os

def resizeWidth(img, targetWidth, keepRatio=True):
    h,w = img.shape[0], img.shape[1]
    tw = int(targetWidth)

    # some guy said this https://stackoverflow.com/questions/23853632/which-kind-of-interpolation-best-for-resizing-image
    isShrinking = tw < w
    methods = [cv2.INTER_CUBIC, cv2.INTER_AREA] # 0 for false a.k.a grow/bigging, 1 for true a.k.a shrink/smallin

    if(keepRatio):
        th = int(h * (targetWidth/w))
        result = cv2.resize(img, (tw, th), interpolation=methods[isShrinking])
    else:
        result = cv2.resize(img, (tw, h), interpolation=methods[isShrinking])

    return result

def resizeHeight(img, targetHeight, keepRatio=True):
    h,w = img.shape[0], img.shape[1]
    th = int(targetHeight)

    # some guy said this https://stackoverflow.com/questions/23853632/which-kind-of-interpolation-best-for-resizing-image
    isShrinking = th < h
    methods = [cv2.INTER_CUBIC, cv2.INTER_AREA] # 0 for false a.k.a grow/bigging, 1 for true a.k.a shrink/smallin

    if(keepRatio):
        tw = int(w * (targetHeight/h))
        result = cv2.resize(img, (tw, th), interpolation=methods[isShrinking])
    else:
        result = cv2.resize(img, (w, th), interpolation=methods[isShrinking])

    return result


def matchHeight(imgs):
    # find the min height
    min_h = min(img.shape[0] for img in imgs)
    # crop all to the same height
    cropped = [img[0:min_h,:] for img in imgs]
    return cropped


def matchWidth(imgs):
    # find the min height
    min_w = min(img.shape[1] for img in imgs)
    # crop all to the same height
    cropped = [img[:,0:min_w] for img in imgs]
    return cropped

def crop_black_pixels(image):
    # Convert the image to grayscale if it's in color
    if len(image.shape) == 3:
        new_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Find the indices of non-zero pixels
    indices = np.nonzero(new_image)

    # Get the minimum and maximum row and column indices
    min_row, max_row = np.min(indices[0]), np.max(indices[0])
    min_col, max_col = np.min(indices[1]), np.max(indices[1])

    # Crop the image using the calculated bounds
    cropped_image = image[min_row:max_row, min_col:max_col]

    return cropped_image

def saveImage(img, path):
    fileName = create_random_name(32)
    fullName = f'{fileName}.png'
    filePath = os.path.join(path, fullName)
    # filePath = f'./instance/results/{fullName}'
    # print(f'saving on {filePath}')
    cv2.imwrite(filePath, img)
    return fullName

def robustImgCrop(img):
    # using LIR sir, concept is, black background easily differentiated with simple thresholding
    # print('ye callin me')
    # make it gray for thresholdin
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # print('ye got grayed')
    # treshold it
    ret, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
    # print('mama lese threshold')
    # now get the contour from the thresholded img, this contour will be fed to LIR to find LIR
    contours, hieararchy = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # print('ok dapet kontour')
    # get the maximum contour (incase fond > 1, so just pick the largest)
    max_cntr = max(contours, key=lambda x:cv2.contourArea(x))

    # print('NYARI mAX DONE')
    # convert contour shape into polygon point shape that valid by LIR (1, point, 2) so every point has 2 element x,y
    # and there are point total of point, and that list is enclosed in a list (1,...)
    # old shape is point,1,2
    max_cntr = max_cntr.reshape(1, max_cntr.shape[0], 2)

    # print('YO WASUP CONTOR DEON')

    # find Largest Interior Rectangle
    try:
        rect = lir.lir(max_cntr)
    except Exception as e:
        print(e)
        # print('^ tuh errornya')
        return img


    # print('le rect done')
    # get the topleft, bottom right
    p1 = lir.pt1(rect)
    p2 = lir.pt2(rect)

    # print('le croppin')
    # now cropit
    img = img[p1[1]:p2[1],p1[0]:p2[0]]
    return img


