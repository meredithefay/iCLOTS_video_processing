"""iCLOTS is a free software created for the analysis of common hematology workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-07-12
This script corresponds to tools available in version 1.0b1, more recent implementations of tools
may be available within the iCLOTS software and in source code at github.com/iCLOTS

Script function that converts a single video to a sequence of images
--No other changes are made to the video frames
----Videos defaults to .avi input, but option for .mp4 is contained within commented code

No input variables

Output files
--A series of images within a directory titled with the original video name

Some tips from the iCLOTS team:
--This script is useful for .avi files that must be presented to iCLOTS as time series
--Images are returned named with the video name plus frame number
----Up to 5 preceding zeros are used to number frames sequentially
------Code will not work as-is on >99,999 frames, but iCLOTS cannot handle that many images anyways
--Images are saved as .png files to avoid unnecessary compression

"""

# Import
import cv2
from tkinter import filedialog
import os
import datetime

# Select single file, .avi only
# videoname = filedialog.askopenfilename(filetypes=[(".avi files", "*.avi")])  # .avi
videoname = filedialog.askopenfilename(filetypes=[(".mp4 files", "*.mp4")])  # .mp4
dirpath = os.path.dirname(videoname)
name = os.path.basename(videoname).split(".")[0]

# Create a directory for saved results including time at which operation was performed
now = datetime.datetime.now()
# Create strings to indicate operations performed
output_folder = os.path.join(dirpath, name + ', ' + now.strftime("%m_%d_%Y, %H_%M_%S"))
os.mkdir(output_folder)
os.chdir(output_folder)

capture = cv2.VideoCapture(videoname)  # Read the video
length = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

# Save frames
success, frame = capture.read()
count = 0
while success and count < length-1:  # Length - 1 prevents "empty frame" error at end of video
    image_name = name + '_frame_' + str(count).zfill(5) + '.png'
    success, image = capture.read()
    cv2.imwrite(image_name, image)  # save frame as .png file
    count += 1
