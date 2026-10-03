import cv2
import os
import numpy as np

# 1. Define target dimensions
TARGET_SIZE = (640, 640)

# 2. Define directories
input_dir = os.path.join('Dataset', 'Positive_Samples')
output_dir = os.path.join('Dataset', 'Resized_Positive_Samples')

print(f"Starting aspect-ratio preserving resize to {TARGET_SIZE[0]}x{TARGET_SIZE[1]}...")

for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            img_path = os.path.join(root, file)
            
            # Keep folder structure
            relative_path = os.path.relpath(root, input_dir)
            save_dir = os.path.join(output_dir, relative_path)
            os.makedirs(save_dir, exist_ok=True)
                
            img = cv2.imread(img_path)
            
            if img is not None:
                # 3. Get original image dimensions (height, width)
                h, w = img.shape[:2]
                
                # 4. Calculate the scale to fit the image inside 640x640 without stretching
                scale = min(TARGET_SIZE[0] / w, TARGET_SIZE[1] / h)
                new_w = int(w * scale)
                new_h = int(h * scale)
                
                # 5. Resize the image uniformly using the calculated scale
                resized_img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
                
                # 6. Create a blank white canvas of 640x640
                # np.ones creates an array of 1s, multiplying by 255 turns them into white pixels
                canvas = np.ones((TARGET_SIZE[1], TARGET_SIZE[0], 3), dtype=np.uint8) * 255
                
                # 7. Calculate the exact center coordinates to paste the image
                x_offset = (TARGET_SIZE[0] - new_w) // 2
                y_offset = (TARGET_SIZE[1] - new_h) // 2
                
                # 8. Paste the resized image onto the white canvas
                canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized_img
                
                save_path = os.path.join(save_dir, file)
                cv2.imwrite(save_path, canvas)
                print(f"Padded and saved: {os.path.join(relative_path, file)}")
            else:
                print(f"Skipped (Corrupted or unreadable file): {img_path}")

print("\nAll images have been padded and resized successfully!")