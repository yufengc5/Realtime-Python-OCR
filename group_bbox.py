import cv2
import numpy as np
from CRAFT import run_CRAFT

# Load the image we are going to detect and initialize and run CRAFT
image_path = 'data/dev_images/real_life_01.jpg'
boxes = run_CRAFT(image_path)

# We don't need 8 coordinates/ 4 points to get the bounding box, 
# so we will convert them to rectangles
def convert_coordinates(boxes):
    rect_boxes = []
    for box in boxes:
        # x and y coordinates of the 4 points
        x_coords = [point[0] for point in box]
        y_coords = [point[1] for point in box]
        
        # get the min and max for x and y
        x_min = min(x_coords)
        x_max = max(x_coords)
        y_min = min(y_coords)
        y_max = max(y_coords)
        
        rect_boxes.append([x_min, y_min, x_max, y_max])
    return rect_boxes

# apply the conversion
rect_boxes = convert_coordinates(boxes)

# sort the bounding boxes based on their y_min value (for top to bottom and left to right processing)
sorted_boxes = sorted(rect_boxes, key=lambda box: box[1])

# grouping and merging boxes that are close vertically (and horizontally implicitly)
merged_boxes = []
current_group = [sorted_boxes[0]]

for i in range(1, len(sorted_boxes)):
    prev_box = current_group[-1]
    curr_box = sorted_boxes[i]

    # merge if the current box is close to the previous box vertically
    if curr_box[1] - prev_box[3] < 20:  # predefined threshold for vertical closeness
        current_group.append(curr_box)
    else:
        merged_boxes.append(current_group)
        current_group = [curr_box]
merged_boxes.append(current_group)

# calculate the enclosing bounding box
final_boxes = []
for group in merged_boxes:
    # Get min and max coordinates for each group of boxes
    x_min = min([box[0] for box in group])
    y_min = min([box[1] for box in group])
    x_max = max([box[2] for box in group])
    y_max = max([box[3] for box in group])  
    
    final_boxes.append([x_min, y_min, x_max, y_max])

# Crop the image based on the final bounding boxes
image = cv2.imread(image_path)
cropped_images = []

for box in final_boxes:
    x_min, y_min, x_max, y_max = box
    x_min = int(max(0, x_min))
    y_min = int(max(0, y_min))
    x_max = int(min(image.shape[1], x_max))
    y_max = int(min(image.shape[0], y_max))
    
    crop = image[y_min:y_max, x_min:x_max]
    cropped_images.append(crop)

    # save the cropped regions
    cv2.imwrite(f"temp/merged_crop_{final_boxes.index(box)}.jpg", crop)
    cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 0, 255), 5)

cv2.imshow("Image with Bounding Boxes", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
#print("Final merged bounding boxes:", final_boxes)