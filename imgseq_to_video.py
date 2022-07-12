"""iCLOTS is a free software created for the analysis of common hematology workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-07-12
This script corresponds to tools available in version 1.0b1, more recent implementations of tools
may be available within the iCLOTS software and in source code at github.com/iCLOTS

Script function that converts a sequence of images to a video
--No other changes are made to the images

Input variables
--fps: frames per second, rate you would like new video to play at

Output files
--One single video made from all images within the selected directory
----Videos default to .avi save, but option for .mp4 is contained in commented code
----iCLOTS analyzes only .avi files
----.mp4 is better suited for viewing on Mac OS
----Video uses directory name as filename
------Avoid spaces, punctuation within directory name

Some tips from the iCLOTS team:
--This script is useful for time series that must be presented to iCLOTS as .avi files
--All images within the selected directory will be merged into one video
----All images must have the same dimensions
----Images must named in the proper alphabetical/numerical order
------If image names contain numbers, use preceding zeros to order properly
--------i.e. 01, 02, .. 10 vs. 1, 2, .. 10
----Best practice is to use all the same image format, e.g. all .png, etc.

"""

# Import
import cv2
from tkinter import filedialog
import os
import glob
import datetime

# IMPORTANT: PARAMETERS TO EDIT
# Frame rate of created video
fps = 1

# Select directory of files
dirpath = filedialog.askdirectory()

# Create a directory for saved results including time at which operation was performed
now = datetime.datetime.now()
# Create strings to indicate operations performed
str_fps = str(fps).replace('.', 'p')
output_folder = os.path.join(dirpath, 'Video, fps ' + str_fps + ', ' + now.strftime("%m_%d_%Y, %H_%M_%S"))
os.mkdir(output_folder)
os.chdir(output_folder)

# Create a list of all image files
imglist_png = glob.glob(dirpath + "/*.png")
imglist_jpg = glob.glob(dirpath + "/*.jpg")
imglist_tif = glob.glob(dirpath + "/*.tif")
imglist = sorted(imglist_png + imglist_jpg + imglist_tif)

# Save all frames within an array
img_array = []
for imgname in imglist:
    img = cv2.imread(imgname)
    img_array.append(img)

# Set up video writer
h, w, l = img.shape  # Dimensions of frame, use last called

name = os.path.basename(dirpath) + '_fps_' + str_fps + '.avi'  # String to save new video as, .avi
# name = os.path.basename(dirpath) + '_fps_' + str_fps + '.mp4'  # String to save new video as, .mp4

# Set up video writer object
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # .avi
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # .mp4
out = cv2.VideoWriter(name, fourcc, fps, (w, h))

# Add frames to videowriter
for i in range(len(img_array)):
    out.write(img_array[i])

# Finish
out.release()
