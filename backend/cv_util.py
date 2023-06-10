import cv2
import numpy as np

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