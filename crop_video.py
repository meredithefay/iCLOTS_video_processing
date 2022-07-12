"""iCLOTS is a free software created for the analysis of common hematology workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-07-12
This script corresponds to tools available in version 1.0b1, more recent implementations of tools
may be available within the iCLOTS software and in source code at github.com/iCLOTS

Script function that crops videos (.avi) within a selected directory
--No other changes are made to videos

Input variables
--start_frame: first frame you would like to retain
--end_frame: last frame you would like to retain

Output files
--All videos with frames cropped to same range
--Provided within a "Cropped" folder within the original directory
----Videos default to .avi save, but option for .mp4 is contained in commented code
----iCLOTS analyzes only .avi files
----.mp4 is better suited for viewing on Mac OS

Some tips from the iCLOTS team:
--This script is most useful for:
----Removing portions of the video clearly affected by changes in microscopy acquisition settings
------e.g., changes in laser power or illumination intensity
----Shortening videos to reduce computational analysis time
--Providing a start and end frame value (n) is most precise
----Values must be integers
--To start and end at roughly a given time, multiply that time (in seconds) by the FPS imaging rate
----FPS = frames per second, a microscope acquisition setting
--If end_frame is greater than n frames in the video, it will stop writing at the end of the video
----The strings labeling the directory and frame will be the original value you provided

"""

# Import
import cv2
import numpy as np
from tkinter import filedialog
import os
import glob
import datetime

# IMPORTANT: PARAMETERS TO EDIT
# First and last frame to be retained
start_frame = 100
end_frame = 300

# Select directory of files
dirpath = filedialog.askdirectory()

# Create a directory for saved results including time at which operation was performed
now = datetime.datetime.now()
# Create strings to indicate operations performed
str_start = str(start_frame)
str_end = str(end_frame)
output_folder = os.path.join(dirpath, 'Cropped i' + str_start + ', f' + \
                str_end + ', ' + now.strftime("%m_%d_%Y, %H_%M_%S"))
os.mkdir(output_folder)
os.chdir(output_folder)


# Create a list of all video files
videolist = glob.glob(dirpath + '/*.avi')  # Script only applies to video files, .avi
# videolist = glob.glob(dirpath + '/*.mp4')  # .mp4 (Mac OS)


# Crop all videos, save
for video in videolist:
    capture = cv2.VideoCapture(video)

    # Dimensions, must be exact for videos
    w = int(np.floor(capture.get(3))) # float
    h = int(np.floor(capture.get(4))) # float
    fps = capture.get(cv2.CAP_PROP_FPS)  # frames per second

    name = os.path.basename(video).split(".")[0] + '_i' + str_start + '_f' + \
           str_end + '.avi'  # String to save image as, .avi
    # name = os.path.basename(video).split(".")[0] + '_i' + str_start + '_f' + \
    #        str_end + '.mp4'  # String to save image as, .mp4

    # Set up video writer object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # .avi
    # fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # .mp4
    out = cv2.VideoWriter(name, fourcc, fps, (w, h))

    # Only write frames within range
    count = 0  # Count gives frame number
    while True:
        ret, frame = capture.read()
        if ret == True:
            if (count > start_frame) and (count < end_frame):
                out.write(frame)
        else:
            break
        count += 1


    # Finish
    capture.release()
    out.release()
    cv2.destroyAllWindows()
