"""iCLOTS is a free software created for the analysis of common hematology workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-07-12
This script corresponds to tools available in version 1.0b1, more recent implementations of tools
may be available within the iCLOTS software and in source code at github.com/iCLOTS

Script function that edits the contrast of images (.jpg, .png, .tif) or videos (.avi)
within a selected directory
--Applies two point processes: multiplication and addition with a constant

Input variables
--alpha: the constant each pixel's intensity value is multiplied by
----Oftentimes called gain
----Should be >1, controls contrast
----High values of alpha cause the relatively bright pixels to become even brighter
----Any value of alpha leaves black pixels as black (value 0)
--beta: the constant added (or subtracted) from each pixel's intensity value
----Oftentimes called bias
---- <1 decreases overall brightness of image, >1 increases overall brightness of image
----Final pixel intensity values <0 will be saved as black (value 0)

Output files
--All images or videos with contrast edited
----Videos default to .avi save, but option for .mp4 is contained in commented code
----iCLOTS analyzes only .avi files
----.mp4 is better suited for viewing on Mac OS
--Provided within a "Contrast" folder within the original directory

Some tips from the iCLOTS team:
--Editing contrast can be useful in applications detecting movement
----Features of interest, like a cell, are more easily distinguished from background, like channels
--Take care interpreting pixel intensity values after editing contrast
----Editing contrast may lead to bias in fluoresence-based results
--See OpenCV tutorial on editing contrast for more information:
----https://docs.opencv.org/3.4/d3/dc1/tutorial_basic_linear_transform.html

"""

# Import
import cv2
import numpy as np
from tkinter import filedialog
import os
import glob
import datetime

# IMPORTANT: PARAMETERS TO EDIT
# Multiplication and addition
alpha = 1  # (<1 decrease contrast, >1 increase contrast)
beta = 0  # (<0 darken image, >0 brighten image)

# Select directory of files
dirpath = filedialog.askdirectory()

# Create a directory for saved results including time at which operation was performed
now = datetime.datetime.now()
# Create strings to indicate operations performed
str_alpha = str(alpha).replace('.', 'p').replace('-', 'n')
str_beta = str(beta).replace('.', 'p').replace('-', 'n')
output_folder = os.path.join(dirpath, 'Contrast a' + str_alpha + ', b' + \
                str_beta + ', ' + now.strftime("%m_%d_%Y, %H_%M_%S"))
os.mkdir(output_folder)
os.chdir(output_folder)

# Create a list of all image files
imglist_png = sorted(glob.glob(dirpath + "/*.png"))
imglist_jpg = sorted(glob.glob(dirpath + "/*.jpg"))
imglist_tif = sorted(glob.glob(dirpath + "/*.tif"))
imglist = imglist_png + imglist_jpg + imglist_tif

# Create a list of all video files
videolist = glob.glob(dirpath + '/*.avi')  # .avi
# videolist = glob.glob(dirpath + '/*.mp4')  # .mp4 (Mac OS)

def editcontrast(frame, w, h):
    """Function to edit contrast of a frame - can be an image file or a video frame"""

    # Apply changes in contrast
    out_frame = frame * alpha + beta
    out_frame[out_frame < 0] = 0
    out_frame[out_frame > 255] = 255  # Prevents high values from 'looping' to 0 as uint8
    out_frame = np.uint8(out_frame)  # Prevents video errors

    # Ensure dimensions are correct, important for videos
    out_frame = cv2.resize(out_frame, (w, h), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)

    return out_frame

# Edit contrast of all images, save
for img in imglist:
    frame = cv2.imread(img)

    h, w, l = frame.shape  # Dimensions of frame

    out_frame = editcontrast(frame, w, h)  # Apply function
    name = os.path.basename(img).split(".")[0] + '_a' + str_alpha + '_b' +\
           str_beta + '.png'  # String to save image as
    cv2.imwrite(name, out_frame)

# Edit contrast of all videos, save
for video in videolist:
    capture = cv2.VideoCapture(video)

    # Dimensions, must be exact for videos
    w = int(np.floor(capture.get(3))) # float
    h = int(np.floor(capture.get(4))) # float
    fps = capture.get(cv2.CAP_PROP_FPS)  # frames per second

    name = os.path.basename(video).split(".")[0] + '_a' + str_alpha + '_b' + \
           str_beta + '.avi'  # String to save image as, .avi
    # name = os.path.basename(video).split(".")[0] + '_a' + str_alpha + '_b' + \
    #        str_beta + '.mp4'  # String to save image as, .mp4

    # Set up video writer object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # .avi
    # fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # .mp4
    out = cv2.VideoWriter(name, fourcc, fps, (w, h))

    # Edit contrast of each frame
    while True:
        ret, frame = capture.read()
        if ret == True:
            out_frame = editcontrast(frame, w, h)
            out.write(out_frame)
        else:
            break

    # Finish
    capture.release()
    out.release()
    cv2.destroyAllWindows()
