import os
import cv2
from ultralytics import YOLO

# 1. Load your custom-trained AUV brain
# Notice we are using forward slashes to avoid that Windows \b escape error!
model = YOLO("runs/detect/hilsa_tracker_v34/weights/best.pt")

# 2. Define where your test images are, and where to save the results
input_folder = "Test_Images"
output_folder = "Detection_Results_5"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

print(f"Scanning '{input_folder}' for images...")

# 3. Loop through every image in the input folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        img_path = os.path.join(input_folder, filename)
        
        # 4. Run the AI on the image
        # conf=0.5 means it will only draw a box if it is at least 50% confident
        results = model(img_path, conf=0.1, iou=0.85)
        
        # 5. Extract the annotated image (the image with the boxes and labels drawn on it)
        annotated_frame = results[0].plot()
        
        # 6. Save the final image to your output folder
        save_path = os.path.join(output_folder, f"detected_{filename}")
        cv2.imwrite(save_path, annotated_frame)
        
        print(f"Processed and saved: {save_path}")

print("\nAll images processed! Check your 'Detection_Results' folder.")