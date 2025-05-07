import cv2
import os

# Settings
image_folder = "images_2"
output_folder = r"E:\DL Dataset\labels_2"
os.makedirs(output_folder, exist_ok=True)
class_id = 0  # default class (solar panel class)

# Global variables
drawing = False
start_point = None
boxes = []
scale_x = 1.0
scale_y = 1.0

def draw_rectangle(event, x, y, flags, param):
    global start_point, drawing, img_display, boxes

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_point = (x, y)

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            temp_img = img_display.copy()
            cv2.rectangle(temp_img, start_point, (x, y), (0, 255, 0), 2)
            cv2.imshow("Image", temp_img)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        end_point = (x, y)
        x_min, y_min = min(start_point[0], end_point[0]), min(start_point[1], end_point[1])
        x_max, y_max = max(start_point[0], end_point[0]), max(start_point[1], end_point[1])
        boxes.append((x_min, y_min, x_max, y_max))
        cv2.rectangle(img_display, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

# Collect image filenames
image_filenames = [f for f in os.listdir(image_folder) if f.endswith('.png')]
image_filenames = sorted(image_filenames)

# Loop through images
for filename in image_filenames:
    img_path = os.path.join(image_folder, filename)
    img = cv2.imread(img_path)
    original_height, original_width = img.shape[:2]

    img_display = img.copy()
    scale_x = 1.0
    scale_y = 1.0
    boxes = []

    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Image", img_display.shape[1], img_display.shape[0])
    cv2.setMouseCallback("Image", draw_rectangle)

    while True:
        cv2.imshow("Image", img_display)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):  # Save annotations
            label_filename = os.path.splitext(filename)[0] + "_label.txt"
            label_path = os.path.join(output_folder, label_filename)
            with open(label_path, 'w') as f:
                for box in boxes:
                    x_min = int(box[0] * scale_x)
                    y_min = int(box[1] * scale_y)
                    x_max = int(box[2] * scale_x)
                    y_max = int(box[3] * scale_y)

                    x_center = (x_min + x_max) / 2.0 / original_width
                    y_center = (y_min + y_max) / 2.0 / original_height
                    bbox_width = (x_max - x_min) / original_width
                    bbox_height = (y_max - y_min) / original_height
                    f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {bbox_width:.6f} {bbox_height:.6f}\n")
            print(f"Saved {label_path}")
            break

        elif key == ord('r'):  # Reset boxes
            img_display = img.copy()
            boxes = []

        elif key == ord('q'):  # Quit without saving
            print(f"Skipped {filename}")
            break

    cv2.destroyAllWindows()
