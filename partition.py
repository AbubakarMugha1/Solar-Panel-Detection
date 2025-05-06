import os
import shutil

# Define paths
source_dir = r"E:\DL Dataset\upscaled\kaggle\working\results\swinir_real_sr_x4_large"
train_dir = "train_upscaled"    # Where to put training images
test_dir = "test_upscaled"      # Where to put test images

# Create directories if they don't exist
os.makedirs(train_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# Supported image extensions
image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')

# Organize images
for filename in os.listdir(source_dir):
    if filename.lower().endswith(image_extensions):
        src_path = os.path.join(source_dir, filename)
        
        if 'test' in filename.lower():
            # Move to test directory
            dest_path = os.path.join(test_dir, filename)
            shutil.move(src_path, dest_path)
            print(f"Moved to test: {filename}")
        else:
            # Move to train directory
            dest_path = os.path.join(train_dir, filename)
            shutil.move(src_path, dest_path)
            print(f"Moved to train: {filename}")

print("\nOrganization complete!")
print(f"Training images moved to: {train_dir}")
print(f"Test images moved to: {test_dir}")