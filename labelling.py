# -*- coding: utf-8 -*-
"""Labelling.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jOoUeC7C97AI7VuesAXTZVjSGqpvG4ve
"""

import cv2
import pandas as pd
from PIL import Image
import io

# Set the path to the ultrasound images directory
image_directory = '/content/inputimg/'

# Set the path to the Excel sheet containing ROI coordinates and labels
excel_file = '/content/Book2.xlsx'

# Load the ROI coordinates and labels from Excel sheet
df = pd.read_excel(excel_file)

# Group the DataFrame by image filename
grouped_df = df.groupby('fname')

# Helper function to assign different colors to each label
def get_label_color(label):
    # Define a color mapping based on label names
    label_colors = {
        'nasal bone': (0, 255, 0),  # Green
        'palate': (0, 0, 255),      # Red
        # Add more label-color mappings here
    }

    return label_colors.get(label, (255, 255, 255))  # Default color is white

# Iterate over each group (image filename and corresponding ROIs)
for filename, group in grouped_df:
    # Construct the image file path
    image_path = image_directory + filename

    # Load the ultrasound image
    image = cv2.imread(image_path)

    # Check if the image was loaded successfully
    if image is not None:
        # Iterate over each ROI in the group
        for index, row in group.iterrows():
            # Extract the ROI coordinates and label
            roi_x = row['w_min']
            roi_y = row['h_min']
            roi_width = row['w_max'] - roi_x
            roi_height = row['h_max'] - roi_y
            label = row['structure']

            # Get the color for the label
            label_color = get_label_color(label)

            # Draw a rectangle on the image using ROI coordinates
            cv2.rectangle(image, (roi_x, roi_y), (roi_x + roi_width, roi_y + roi_height), label_color, 2)

            # Add label text to the image
            label_text = f"{label}"
            font_scale = 0.5
            font_thickness = 1
            label_size, _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
            cv2.putText(image, label_text, (roi_x, roi_y - label_size[1]), cv2.FONT_HERSHEY_SIMPLEX, font_scale, label_color, font_thickness)

        # Convert the image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Display the marked image with all ROIs and labels
        pil_image = Image.fromarray(image_rgb)
        pil_image.show()
    else:
        print(f"Failed to load image: {image_path}")