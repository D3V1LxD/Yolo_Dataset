import os
import shutil
import random

# 1. Setup paths
base_dir = 'Synthetic_Dataset'
img_dir = os.path.join(base_dir, 'images')
lbl_dir = os.path.join(base_dir, 'labels')

# 2. Create the required Train and Val folders
for split in ['train', 'val']:
    os.makedirs(os.path.join(img_dir, split), exist_ok=True)
    os.makedirs(os.path.join(lbl_dir, split), exist_ok=True)

# 3. Gather all the synthetic images we generated earlier
images = [f for f in os.listdir(img_dir) if f.endswith('.jpg') and os.path.isfile(os.path.join(img_dir, f))]

if not images:
    print("No images found in the root of 'Synthetic_Dataset/images'. (Maybe you already moved them?)")
    exit()

# 4. Shuffle and split 80/20
random.shuffle(images)
split_idx = int(len(images) * 0.8)
train_imgs = images[:split_idx]
val_imgs = images[split_idx:]

def move_files(file_list, split_name):
    for img_name in file_list:
        # Move the .jpg
        shutil.move(os.path.join(img_dir, img_name), os.path.join(img_dir, split_name, img_name))
        
        # Move the matching .txt label
        lbl_name = img_name.replace('.jpg', '.txt')
        lbl_path = os.path.join(lbl_dir, lbl_name)
        if os.path.exists(lbl_path):
            shutil.move(lbl_path, os.path.join(lbl_dir, split_name, lbl_name))

print(f"Moving {len(train_imgs)} files to the 'train' folder...")
move_files(train_imgs, 'train')

print(f"Moving {len(val_imgs)} files to the 'val' folder...")
move_files(val_imgs, 'val')

# 5. Generate the correct data.yaml file
yaml_content = f"""
train: images/train
val: images/val

nc: 1
names: ['Ilish']
"""

with open(os.path.join(base_dir, 'data.yaml'), 'w') as f:
    f.write(yaml_content.strip())

print("\nSuccess! Your Synthetic Dataset is properly formatted for YOLO.")