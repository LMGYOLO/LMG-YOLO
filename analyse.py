import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# Folder containing YOLO label files
labels_folder = 'dataset/labels/train'

# Image size (640x480)
img_width = 640
img_height = 480

# Initialize lists for storing width, height, and area information
widths = []
heights = []
small_bbox_count = 0
medium_bbox_count = 0
large_bbox_count = 0

# Lists for plotting the scatter points of different categories
small_widths = []
small_heights = []
medium_widths = []
medium_heights = []
large_widths = []
large_heights = []


# Function to read a single YOLO format label file
def read_yolo_label_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    bboxes = []
    for line in lines:
        # Parse the YOLO format: class x_center y_center width height
        parts = line.strip().split()
        x_center, y_center, width, height = map(float, parts[1:])
        # Convert to absolute width and height based on image size
        abs_width = width * img_width
        abs_height = height * img_height
        bboxes.append((abs_width, abs_height))
    return bboxes


# Iterate over all the label files in the folder
for filename in os.listdir(labels_folder):
    if filename.endswith('.txt'):
        label_file_path = os.path.join(labels_folder, filename)
        bboxes = read_yolo_label_file(label_file_path)

        # Process each bounding box
        for w, h in bboxes:
            # Append width and height for the scatter plot
            if w * h <= 32 * 32:  # Small bbox
                small_widths.append(w)
                small_heights.append(h)
                small_bbox_count += 1
            elif w * h <= 96 * 96:  # Medium bbox
                medium_widths.append(w)
                medium_heights.append(h)
                medium_bbox_count += 1
            else:  # Large bbox
                large_widths.append(w)
                large_heights.append(h)
                large_bbox_count += 1

# Create a figure for the scatter plot
fig, ax = plt.subplots()

# Scatter plot (left side) with new color scheme
ax.scatter(small_widths, small_heights, alpha=0.5, c='g', label='Small (<32x32)', s=1)
ax.scatter(medium_widths, medium_heights, alpha=0.5, c='m', label='Medium (32x32-96x96)', s=0.4)
ax.scatter(large_widths, large_heights, alpha=0.5, c='c', label='Large (>96x96)', s=0.2)
ax.set_xlabel('Width', fontsize=20)
ax.set_ylabel('Height', fontsize=20)
ax.tick_params(axis='both', which='major', labelsize=20)
ax.grid(True)
ax.legend(fontsize=12, markerscale=15)

# Create an inset axes for the pie chart
ax_inset = inset_axes(ax, width="60%", height="60%", loc='lower right')

# Pie chart (right bottom corner inside scatter plot)
sizes = [small_bbox_count, medium_bbox_count, large_bbox_count]
labels = ['Small', 'Medium', 'Large']
colors = ['g', 'm', 'c']
explode = (0.1, 0, 0)  # Explode the small slice to highlight it


def func(pct, sizes):
    # Calculate the absolute count
    abs_v = pct * sum(sizes) / 100 # 当前块的总实例数

    return f"{abs_v/1000:.1f}k \n ({pct:.1f}%)"


# Create the pie chart with both counts and percentages
ax_inset.pie(sizes, labels=labels, colors=colors, autopct=lambda pct: func(pct, sizes), explode=explode, startangle=90,
             textprops={'fontsize': 12})
ax_inset.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.

# Adjust layout and show the plots
plt.tight_layout()
plt.savefig('calc.jpg', dpi=300)
plt.show()

# Print the counts of bounding boxes in each category
print(f"Number of small bounding boxes (0-32x32): {small_bbox_count}")
print(f"Number of medium bounding boxes (32x32-96x96): {medium_bbox_count}")
print(f"Number of large bounding boxes (>96x96): {large_bbox_count}")
