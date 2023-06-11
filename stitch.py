# import the necessary packages
from backend.Stitcher import Stitcher
from backend.cv_util import robustCropImg, crop_black_pixels
import argparse
import imutils
import cv2
import numpy as np
# construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-f", "--first", required=True,
# 	help="path to the first image")
# ap.add_argument("-s", "--second", required=True,
# 	help="path to the second image")
# args = vars(ap.parse_args())

# load the two images and resize them to have a width of 400 pixels
# (for faster processing)
# imageA = cv2.imread(args["first"])
# imageB = cv2.imread(args["second"])
imageA = cv2.imread('example_img/first/canyon.jpg')
imageB = cv2.imread('example_img/second/canyon.jpg')
# imageA = imutils.resize(imageA, width=400)
# imageB = imutils.resize(imageB, width=400)
# print(imageA.shape)
# Check height shape different
if imageA.shape[0] != imageB.shape[0]:
    h = max(imageA.shape[0], imageB.shape[0])
    Ablack = np.zeros((h, imageA.shape[1], imageA.shape[2]), dtype=np.uint8)
    Ablack[0:imageA.shape[0],:] = imageA
    imageA = Ablack

    Bblack = np.zeros((h, imageB.shape[1], imageB.shape[2]),dtype=np.uint8)
    Bblack[0:imageB.shape[0],:] = imageB
    imageB = Bblack


    # imageA = imageA[0:h, :]
    # imageB = imageB[0:h, :]

# stitch the images together to create a panorama
stitcher = Stitcher()
(result, vis) = stitcher.stitch([imageA, imageB], showMatches=True)
# show the images
cv2.imshow("Image A", imageA)
cv2.imshow("Image B", imageB)
cv2.imshow("Keypoint Matches", vis)
cv2.imshow("Result", result)

catch1 = robustCropImg(result)
# a = crop_black_pixels(result)

cv2.imshow('aa', catch1)




cv2.waitKey(0)