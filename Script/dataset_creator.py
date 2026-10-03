import os
import shutil
import random

# 1. CRITICAL: Change this to the exact folder containing BOTH your .jpg and .txt files
source_folder = 'Dataset/Positive_Samples' # <--- UPDATE THIS PATH

# 2. Define the YOLO master folder
yolo_dataset_path = 'YOLO_Dataset'

# 3. Create the YOLO directory structure
folders_to_create = [
    f'{yolo_dataset_path}/images/train',
    f'{yolo_dataset_path}/images/val',
    f'{yolo_dataset_path}/labels/train',
    f'{yolo_dataset_path}/labels/val'
]
for folder in folders_to_create:
    os.makedirs(folder, exist_ok=True)

# 4. Gather all the image files
all_images = [f for f in os.listdir(source_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

if len(all_images) == 0:
    print(f"ERROR: No images found in '{source_folder}'. Please check the folder path.")
    exit()

# 5. Shuffle and calculate the split (80/20)
random.shuffle(all_images)
split_index = int(len(all_images) * 0.8)

train_images = all_images[:split_index]
val_images = all_images[split_index:]

# Counters for our summary
labels_found = 0
labels_missing = 0

# 6. Function to move the paired files
def move_files(image_list, split_type):
    global labels_found, labels_missing
    
    for image_file in image_list:
        # Move the image
        img_src = os.path.join(source_folder, image_file)
        img_dst = os.path.join(yolo_dataset_path, 'images', split_type, image_file)
        shutil.copy(img_src, img_dst)
        
        # Look for the exact matching .txt file
        label_file = os.path.splitext(image_file)[0] + '.txt'
        label_src = os.path.join(source_folder, label_file)
        label_dst = os.path.join(yolo_dataset_path, 'labels', split_type, label_file)
        
        if os.path.exists(label_src):
            shutil.copy(label_src, label_dst)
            labels_found += 1
        else:
            print(f"WARNING: Missing label! Moved '{image_file}' but could not find '{label_file}'")
            labels_missing += 1

print(f"Found {len(all_images)} images. Splitting into Train and Val...")
move_files(train_images, 'train')
move_files(val_images, 'val')

print("\n--- SPLIT SUMMARY ---")
print(f"Images moved: {len(all_images)}")
print(f"Labels (.txt) moved: {labels_found}")
if labels_missing > 0:
    print(f"Missing Labels: {labels_missing} (Check the warnings above!)")
else:
    print("Success! Every image had a matching .txt label.")