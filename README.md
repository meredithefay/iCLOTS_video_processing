# iCLOTS_video_processing
Scripts useful for microscopy image and video pre-processing. All materials are also maintained at github.com/LamLabEmory.
These scripts have been designed specifically for use with iCLOTS software, a Lam lab project available at iCLOTS.org, but you might find them useful for other applications as well.
Most methods rely heavily on OpenCV image processing library. Each script has information about inputs, parameters, and outputs and a "tips" section within the module docstrings. Briefly, users select a folder of .png, .jpg., .tif, and/or .avi files for modification. Users edit indicated parameters, some image processing step is applied, and all edited files are returned in a new directory within the original.

## Scripts included in repository
- choose_roi.py: choose a region of interest from a file
- crop_video.py: shorten video to a specified start and end frame
- edit_contrast.py: edit contrast of a file using gain and bias parameters
- imgseq_to_video.py: convert a sequential list of images to a single video
- video_to_imgseq.py: convert a single video to a sequential list of images
- normalize_intrange.py: normalize a file to [0, 255] pixel range
- resize.py: increase or decrease the resolution of a file
- rotate.py: rotate a file, useful for applications relying on parallel flow (aspect ratio is preserved)

## Inputs, outputs, methods
Users are guided to choose a directory of .png, .jpg, .tif, and/or .avi files using a file dialog window.
Users should edit input parameters based on their own individual needs. All parameter values requiring user editing are directly under import statements. Sample (from resize.py):

```
# IMPORTANT: PARAMETERS TO EDIT
# Resize factor frame dimensions are multiplied by
r_f = 1  # (<1: reduce size >1: increase size)
```

Outputs:
- A new directory within the selected directory, labeled with a time stamp for reference.
  - Each file has some indicator of the operation applied appended to the original file name

## Help and contributing
Contributions are always welcome! Submit a pull request or contact me directly at meredith.e.fay@gmail.com.

## References
OpenCV:
- Bradski G. The OpenCV Library. Dr Dobb’s Journal of Software Tools 2000. 2000.
You may find OpenCV tutorials useful for better understanding the theory behind basic image processing:
- https://docs.opencv.org/4.x/d9/df8/tutorial_root.html
