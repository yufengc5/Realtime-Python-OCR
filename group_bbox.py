import cv2
import numpy as np
import os
from CRAFT import run_CRAFT

def convert_coordinates(boxes):
    """Converts 8-coordinate/4-point boxes to rectangles [x_min, y_min, x_max, y_max]."""
    rect_boxes = []
    for box in boxes:
        x_coords = [point[0] for point in box]
        y_coords = [point[1] for point in box]
        
        x_min = min(x_coords)
        x_max = max(x_coords)
        y_min = min(y_coords)
        y_max = max(y_coords)
        
        rect_boxes.append([x_min, y_min, x_max, y_max])
    return rect_boxes

def extract_and_merge_text_regions(image_path, threshold=20, output_dir="temp", save_crops=True, show_result=True):
    """
    Detects text using CRAFT and groups bounding boxes that are close.
    
    Parameters:
        image_path (str): Path to the input image.
        threshold (int): Distance to merge vertically close boxes.
        output_dir (str): Folder path to save the cropped images.
        save_crops (bool): Whether to save crops to disk.
        show_result (bool): Whether to display the image with bounding boxes.
        
    Returns:
        cropped_images (list): List of cropped cv2 image arrays.
        final_boxes (list): List of final merged bounding box coordinates.
    """
    # 1. Run CRAFT to get initial boxes
    boxes = run_CRAFT(image_path)
    if not len(boxes):
        print("No text detected.")
        return [], []

    # 2. Convert to standard rectangles and sort top-to-bottom
    rect_boxes = convert_coordinates(boxes)
    sorted_boxes = sorted(rect_boxes, key=lambda box: box[1])

    # 3. Group and merge boxes that are vertically close
    merged_boxes = []
    current_group = [sorted_boxes[0]]

    for i in range(1, len(sorted_boxes)):
        prev_box = current_group[-1]
        curr_box = sorted_boxes[i]

        if curr_box[1] - prev_box[3] < threshold:
            current_group.append(curr_box)
        else:
            merged_boxes.append(current_group)
            current_group = [curr_box]
    merged_boxes.append(current_group)

    # 4. Calculate the final enclosing bounding box for each group
    final_boxes = []
    for group in merged_boxes:
        x_min = min([box[0] for box in group])
        y_min = min([box[1] for box in group])
        x_max = max([box[2] for box in group])
        y_max = max([box[3] for box in group])  
        final_boxes.append([x_min, y_min, x_max, y_max])

    # 5. Crop original image, save, and optionally display
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Could not load image at path: {image_path}")
        
    cropped_images = []
    
    # Ensure output directory exists if we are saving
    if save_crops and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for idx, box in enumerate(final_boxes):
        x_min, y_min, x_max, y_max = box
        
        # Ensure boundaries stay within image dimensions
        x_min = int(max(0, x_min))
        y_min = int(max(0, y_min))
        x_max = int(min(image.shape[1], x_max))
        y_max = int(min(image.shape[0], y_max))
        
        crop = image[y_min:y_max, x_min:x_max]
        cropped_images.append(crop)

        # Save and draw
        if save_crops:
            crop_path = os.path.join(output_dir, f"merged_crop_{idx}.jpg")
            cv2.imwrite(crop_path, crop)
            
        if show_result:
            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 0, 255), 5)

    if show_result:
        cv2.imshow("Image with Bounding Boxes", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return cropped_images, final_boxes

# testing
if __name__ == "__main__":
    img_path = "data/dev_images/real_life_01.jpg"
    extract_and_merge_text_regions(img_path)