"""iCLOTS is a free software created for the analysis of common hematology workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-07-12
This script corresponds to tools available in version 1.0b1, more recent implementations of tools
may be available within the iCLOTS software and in source code at github.com/iCLOTS

Script function that resizes images (.jpg, .png, .tif) or videos (.avi) within a selected directory

Input variables
--r_f (resize factor): the factor a frame's dimensions are multiplied by during the resize process
---- < 1 indicates reducing resolution, > 1 increases resolution

Output files
--All images or videos resized, provided within a "Resize" folder within the original directory
----Videos default to .avi save, but option for .mp4 is contained in commented code
----iCLOTS analyzes only .avi files
----.mp4 is better suited for viewing on Mac OS

Some tips from the iCLOTS team:
--Decreasing resolution can help speed computational analysis of large files
----In applications quantifying movement of cells, oftentimes lower resolution is sufficient
----In applications quantifying changes in morphology maintain the highest resolution possible
--Artificially increasing resolution in post-processing oftentimes isn't useful
----It is not possible to add information that the microscope did not provide
----It may lead to bias in morphological results by exponentially increasing changes in dimension

"""

# Import
import cv2
import numpy as np
from tkinter import filedialog
import os
import glob
import datetime

# IMPORTANT: PARAMETERS TO EDIT
# Resize factor frame dimensions are multiplied by
r_f = 0.5  # (<1: reduce size >1: increase size)

# Select directory of files
dirpath = filedialog.askdirectory()

# Create a directory for saved results including time at which operation was performed
now = datetime.datetime.now()
str_r_f = str(r_f).replace('.', 'p') # Create a string to indicate resize factor in outputs
output_folder = os.path.join(dirpath, 'Resize ' + str_r_f + ', ' + now.strftime("%m:%d:%Y, %H.%M.%S"))
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

def resizeframe(frame, w_n, h_n):
    """Function to resize a frame - can be an image file or a video frame"""

    # Resize
    out_frame = cv2.resize(frame, (w_n, h_n), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)

    return out_frame

# Resize all images, save
for img in imglist:
    frame = cv2.imread(img)

    h, w, l = frame.shape  # Dimensions of frame
    w_n = int(np.floor(w * r_f))  # New width, float
    h_n = int(np.floor(h * r_f))  # New height, float

    out_frame = resizeframe(frame, w_n, h_n)  # Apply function
    name = os.path.basename(img).split(".")[0] + '_rs_' + str_r_f + '.png'  # String to save image as
    cv2.imwrite(name, out_frame)

# Resize all videos, save
for video in videolist:
    capture = cv2.VideoCapture(video)

    # Dimensions, must be exact for videos
    w_n = int(np.floor(capture.get(3) * r_f)) # float
    h_n = int(np.floor(capture.get(4) * r_f))  # float
    fps = capture.get(cv2.CAP_PROP_FPS)  # frames per second

    name = os.path.basename(video).split(".")[0] + '_rs_' + str_r_f + '.avi'  # String to save image as, avi
    # name = os.path.basename(video).split(".")[0] + '_rs_' + str_r_f + '.mp4'  # String to save image as, mp4

    # Set up video writer object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # .avi
    # fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # .mp4
    out = cv2.VideoWriter(name, fourcc, fps, (w_n, h_n))

    # Resize each frame
    while True:
        ret, frame = capture.read()
        out_frame = resizeframe(frame, w_n, h_n)
        out.write(out_frame)
        else:
            break

    # Finish
    capture.release()
    out.release()
    cv2.destroyAllWindows()
