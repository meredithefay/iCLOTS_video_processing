"""iCLOTS is a free software created for the analysis of common hematology workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-07-12
This script corresponds to tools available in version 1.0b1, more recent implementations of tools
may be available within the iCLOTS software and in source code at github.com/iCLOTS

Script function that rotates images (.jpg, .png, .tif) or videos (.avi) within a selected directory
--Script maintains aspect ratio of original images
--Addl. dimension added to accommodate original aspect ratio has [0, 0, 0] (black) pixel intensity

Input variables
--angle: the angle the frame is rotated
----Angle value > 0 rotates counterclockwise
----Angle value < 1 rotates clockwise

Output files
--All images or videos rotated, provided within a "Rotate" folder within the original directory
----Videos default to .avi save, but option for .mp4 is contained in commented code
----iCLOTS analyzes only .avi files
----.mp4 is better suited for viewing on Mac OS

Some tips from the iCLOTS team:
--Aspect ratio is maintained
----Users can continue to provide the same micron-to-pixel conversion ratio in image analysis apps
--Rotating videos or images such that microfluidic channels are horizontal is crucial for:
----Applications that rely on left-right indexing, such as microchannel occlusion or velocity profiles
--Rotating videos or images such that microfluidic channels are horizontal is suggested for:
----One-directional movement quantification, such as deformability or velocity applications
--Rotating images has no affect on morphology measurements

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
angle = 1  # (<0: clockwise, >0: counterclockwise)

# Select directory of files
dirpath = filedialog.askdirectory()

# Create a directory for saved results including time at which operation was performed
now = datetime.datetime.now()
# Create a string to indicate degrees rotated in outputs
str_angle = str(angle).replace('.', 'p').replace('-', 'n')
output_folder = os.path.join(dirpath, 'Rotate ' + str_angle + ', ' + now.strftime("%m_%d_%Y, %H_%M_%S"))
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

def rotateframe(frame, w, h):
    """Function to rotate a frame - can be an image file or a video frame"""

    h_n, w_n = frame.shape[:2]  # Image shape has 3 dimensions
    image_center = (
        w / 2,
        h / 2)  # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape

    rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.)

    # Rotation calculates the cos and sin, taking absolutes of those.
    abs_cos = abs(rotation_mat[0, 0])
    abs_sin = abs(rotation_mat[0, 1])

    # Find the new width and height bounds
    bound_w = int(h_n * abs_sin + w_n * abs_cos)
    bound_h = int(h_n * abs_cos + w_n * abs_sin)

    # subtract old image center (bringing image back to origo) and adding the new image center coordinates
    rotation_mat[0, 2] += bound_w / 2 - image_center[0]
    rotation_mat[1, 2] += bound_h / 2 - image_center[1]

    # rotate image with the new bounds and translated rotation matrix
    out_frame = cv2.warpAffine(frame, rotation_mat, (bound_w, bound_h))

    # Ensure dimensions are correct, important for videos
    out_frame = cv2.resize(out_frame, (w, h), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)

    return out_frame

# Rotate all images, save
for img in imglist:
    frame = cv2.imread(img)

    h, w, l = frame.shape  # Dimensions of frame

    out_frame = rotateframe(frame, w, h)  # Apply function
    name = os.path.basename(img).split(".")[0] + '_rot_' + str_angle + '.png'  # String to save image as
    cv2.imwrite(name, out_frame)

# Rotate all videos, save
for video in videolist:
    capture = cv2.VideoCapture(video)

    # Dimensions, must be exact for videos
    w = int(np.floor(capture.get(3))) # float
    h = int(np.floor(capture.get(4))) # float
    fps = capture.get(cv2.CAP_PROP_FPS)  # frames per second

    name = os.path.basename(video).split(".")[0] + '_rot_' + str_angle + '.avi'  # String to save image as, .avi
    # name = os.path.basename(video).split(".")[0] + '_rot_' + str_angle + '.mp4'  # String to save image as, .mp4

    # Set up video writer object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # .avi
    # fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # .mp4
    out = cv2.VideoWriter(name, fourcc, fps, (w, h))

    # Rotate each frame
    while True:
        ret, frame = capture.read()
        if ret == True:
            out_frame = rotateframe(frame, w, h)
            out.write(out_frame)
        else:
            break

    # Finish
    capture.release()
    out.release()
    cv2.destroyAllWindows()
