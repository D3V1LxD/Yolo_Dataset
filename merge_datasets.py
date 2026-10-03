import os
import shutil

# We are going to copy everything from Synthetic to YOLO
folders_to_merge = [
    ('Synthetic_Dataset/images/train', 'YOLO_Dataset/images/train'),
    ('Synthetic_Dataset/images/val', 'YOLO_Dataset/images/val'),
    ('Synthetic_Dataset/labels/train', 'YOLO_Dataset/labels/train'),
    ('Synthetic_Dataset/labels/val', 'YOLO_Dataset/labels/val')
]

print("Merging Synthetic underwater data into the original YOLO dataset...")

for src, dst in folders_to_merge:
    if not os.path.exists(src):
        continue
    
    # Ensure destination exists
    os.makedirs(dst, exist_ok=True)
    
    # Copy all files over
    files = os.listdir(src)
    for file in files:
        src_file = os.path.join(src, file)
        dst_file = os.path.join(dst, file)
        shutil.copy(src_file, dst_file)
        
    print(f"Copied {len(files)} files into {dst}")

print("\nSuccess! Your datasets are merged.")