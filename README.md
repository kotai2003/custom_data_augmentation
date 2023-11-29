
# Image Data Augmentation Script

## Overview
This script is designed for use in computer vision projects to increase the amount of training data available. It enhances image datasets by applying various transformations such as rotation, jittering, brightness adjustment, and noise addition. The goal is to create varied versions of existing images to improve the robustness and accuracy of machine learning models.

## Features
- **Rotation**: Rotates the image to different angles.
- **Jittering**: Applies small random shifts to the image.
- **Brightness Adjustment**: Alters the brightness level of the image.
- **Noise Addition**: Adds Gaussian noise to the image.

## Requirements
- Python
- OpenCV
- NumPy
- Random
- OS Module

## Usage
1. **Input**: Place `.png` or `.jpg` images in a designated folder.
2. **Execution**: Run the `02.Image_Data_Augumentation_5times.py` script.
3. **Output**: The script processes each image in the input folder and applies the augmentation techniques, generating multiple variations of each image.

## How to Run
To execute the script, navigate to the directory containing `02.Image_Data_Augumentation_5times.py` and run the following command in the terminal:
```
python 02.Image_Data_Augumentation_5times.py
```

## Additional Information
- `02.Image_Data_Augumentation_5times.py` is the main program file.
- Ensure that the required libraries are installed before running the script.

## Limitations
- The script currently supports only `.png` and `.jpg` image formats.
- The number of augmentations and specific parameters are predefined in the script.
