"""iCLOTS is a free software created for the analysis of common hematology workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-06-30
This script corresponds to tools available in version 1.0b1, more recent implementations of tools
may be available within the iCLOTS software and in source code at github.com/iCLOTS

Script function that crops images (.jpg, .png, .tif) or videos (.avi) to a chosen region of interest (ROI)
--This script designed to crop each file to a different ROI, could edit to crop each file to a consistent ROI

Input variables
--None, a window of your image or first video frame from which you can choose your ROI with a draggable rectangle from
---will open automatically

Output files
--All images or videos cropped to an ROI, provided within a "ROI" folder within the original directory
----Videos default to .avi save, but option for .mp4 is contained in commented code
----iCLOTS analyzes only .avi files
----.mp4 is better suited for viewing on Mac OS

Some tips from the iCLOTS team:
--In nearly all applications, small defects in channel walls can present as changes in intensity that may
---be mistaken for cells
----In all applications except for deformability and microchannel analysis, try to crop images to the channels only
--The same ROI will be applied to all frames within an individual video

"""

# Import
import cv2
from tkinter import filedialog
import os
import glob
import datetime
import numpy as np

# Select directory of files
dirpath = filedialog.askdirectory()

# Create a directory for saved results including time at which operation was performed
now = datetime.datetime.now()
output_folder = os.path.join(dirpath, 'ROI, ' + now.strftime("%m_%d_%Y, %H_%M_%S"))
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

def chooseROI(frame):
    """Function to resize a frame - can be an image file or a video frame"""

    # Choose ROI from image, pull out values
    fromCenter = False  # Set up to choose as a drag-able rectangle rather than a rectangle chosen from center
    r = cv2.selectROI("Image", frame, fromCenter)  # Choose ROI function from cv2 - opens a window to choose
    ROI_x = int(r[0])  # Take result of selectROI and put into a variable
    ROI_y = int(r[1])  # " "
    ROI_w = int(r[2])  # " "
    ROI_h = int(r[3])  # " "

    cv2.destroyAllWindows()

    return ROI_x, ROI_y, ROI_w, ROI_h

# Resize all images, save
for img in imglist:

    frame = cv2.imread(img)
    ROI_x, ROI_y, ROI_w, ROI_h = chooseROI(frame) # Find ROI by applying function

    out_frame = frame[ROI_y: (ROI_y + ROI_h), ROI_x: (ROI_x + ROI_w)]  # Crop
    name = os.path.basename(img).split(".")[0] + '_ROI.png'  # String to save image as
    cv2.imwrite(name, out_frame)

# Resize all videos, save
for video in videolist:
    capture = cv2.VideoCapture(video)
    # Dimensions, must be exact for videos
    fps = capture.get(cv2.CAP_PROP_FPS)  # frames per second

    name = os.path.basename(video).split(".")[0] + '_ROI.avi'  # String to save image as, .avi
    # name = os.path.basename(video).split(".")[0] + '_ROI.mp4'  # String to save image as, .mp4

    ret, frame_0 = capture.read()
    ROI_x, ROI_y, ROI_w, ROI_h = chooseROI(frame_0) # Find ROI by applying function

    # Set up video writer object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # .avi
    # fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # .mp4
    out = cv2.VideoWriter(name, fourcc, fps, (ROI_w, ROI_h))

    # Resize each frame
    while True:
        ret, frame = capture.read()
        if ret == True:
            out_frame = frame[ROI_y: (ROI_y + ROI_h), ROI_x: (ROI_x + ROI_w)]  # Crop
            out.write(out_frame)
        else:
            break

    # Finish
    capture.release()
    out.release()
    cv2.destroyAllWindows()
