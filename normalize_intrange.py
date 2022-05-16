"""iCLOTS is a free software created for the analysis of common hematology workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-05-16
This script corresponds to tools available in version 1.0b1, more recent implementations of tools
may be available within the iCLOTS software and in source code at github.com/iCLOTS

Script function that normalizes the range of pixel intensity values to 0 (black) to 255 (white)
of images (.jpg, .png, .tif) files within a selected directory

No input variables

Output files
--All images with 0 as the lowest value and 255 as the highest value
----Normalization is applied to any number of layers
----Not currently offered for video files
--Provided within a "Normalized" folder within the original directory

Some tips from the iCLOTS team:
--Use caution normalizing images to the same range
----Normalizing can remove bias that comes from different laser power, gain, etc. settings
----Normalizing can also introduce bias
----It's always most ideal to compare images taken during the same experiment
--Ideally initial images are within (0, 255) range - "maxed out" pixel values cause loss of information
----A range of intensities may have existed beyond 255
--This script uses the following formula:

new = layer - min / (max - min) * 255

"""

# Import
import cv2
import numpy as np
from tkinter import filedialog
import os
import glob
import datetime

# Select directory of files
dirpath = filedialog.askdirectory()

# Create a directory for saved results including time at which operation was performed
now = datetime.datetime.now()
# Create strings to indicate operations performed
output_folder = dirpath + '/Normalized, ' + now.strftime("%m:%d:%Y, %H.%M.%S")
os.mkdir(output_folder)
os.chdir(output_folder)

# Create a list of all image files
imglist_png = sorted(glob.glob(dirpath + "/*.png"))
imglist_jpg = sorted(glob.glob(dirpath + "/*.jpg"))
imglist_tif = sorted(glob.glob(dirpath + "/*.tif"))
imglist = imglist_png + imglist_jpg + imglist_tif

def normalize(image):
    """Function to apply normalization operation to image"""

    h, w, l = image.shape  # Dimensions of frame

    for i in range(l):  # For each layer
        # Normalize
        image[l] = (image[l] - np.amin(image))/(np.amax(image) - np.amin(image)) * 255

    out_image = image

    return out_image

# Normalize all images, save
for img in imglist:
    image = cv2.imread(img)

    out_image = normalize(image)
    name = os.path.basename(img).split(".")[0] + '_normalized.png'  # String to save image as

    cv2.imwrite(name, out_image)
