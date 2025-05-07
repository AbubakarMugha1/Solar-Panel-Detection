import cv2
import os

# Settings
image_folder = "train\images"
labels_folder = r"E:\DL Dataset\train\labels"
output_folder = r"E:\DL Dataset\annotated_images"
os.makedirs(output_folder, exist_ok=True)

# Get the list of images
image_filenames = sorted([f for f in os.listdir(image_folder) if f.endswith(('.png'))])

for filename in image_filenames:
    image_path = os.path.join(image_folder, filename)
    label_path = os.path.join(labels_folder, os.path.splitext(filename)[0] + "_label.txt")

    # Read image
    img = cv2.imread(image_path)

    # Get image dimensions
    image_height, image_width = img.shape[:2]

    # Check if label file exists
    if not os.path.exists(label_path):
        print(f"No label for {filename}")
        continue

    # Read labels
    with open(label_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        parts = line.strip().split()
        class_id, x_center, y_center, width, height = map(float, parts)

        # Convert normalized coordinates back to pixel values based on the image's actual dimensions
        x_center *= image_width
        y_center *= image_height
        width *= image_width
        height *= image_height

        x_min = int(x_center - width / 2)
        y_min = int(y_center - height / 2)
        x_max = int(x_center + width / 2)
        y_max = int(y_center + height / 2)

        # Draw rectangle
        cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 3)

    # Save the annotated image
    output_path = os.path.join(output_folder, filename)
    cv2.imwrite(output_path, img)
    print(f"Saved annotated image to {output_path}")
