import os
import shutil
import random

# 1. Point this to your folder full of empty background/other fish images
negative_source = 'Dataset/Negative_Samples'

# 2. Your existing YOLO dataset
yolo_train_img_dir = 'YOLO_Dataset/images/train'
yolo_val_img_dir = 'YOLO_Dataset/images/val'

# 3. Gather all images
all_neg_images = [f for f in os.listdir(negative_source) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

if len(all_neg_images) == 0:
    print(f"ERROR: No images found in '{negative_source}'.")
    exit()

# 4. Shuffle and calculate the 80/20 split
random.shuffle(all_neg_images)
split_index = int(len(all_neg_images) * 0.8)

train_negatives = all_neg_images[:split_index]
val_negatives = all_neg_images[split_index:]

# 5. Move the files (Notice we do NOT look for or create .txt files)
def move_negatives(image_list, dest_folder):
    for img in image_list:
        src_path = os.path.join(negative_source, img)
        dest_path = os.path.join(dest_folder, img)
        shutil.copy(src_path, dest_path)

print(f"Injecting {len(all_neg_images)} Negative Samples into YOLO Dataset...")
move_negatives(train_negatives, yolo_train_img_dir)
move_negatives(val_negatives, yolo_val_img_dir)

print(f"Success! Added {len(train_negatives)} to Train, and {len(val_negatives)} to Val.")
print("YOLO will register these as 'Backgrounds' because they have no .txt files.")