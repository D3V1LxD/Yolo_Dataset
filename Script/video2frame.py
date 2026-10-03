import cv2
import os

# 1. Put your downloaded YouTube video here
video_path = 'Shots.mp4'
output_folder = 'Dataset/Positive_Samples'

os.makedirs(output_folder, exist_ok=True)
cap = cv2.VideoCapture(video_path)

frame_count = 0
saved_count = 0

print(f"Extracting frames from {video_path}...")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break
        
    # 2. Save 1 frame out of every 5 (to avoid having 100 identical images)
    if frame_count % 5 == 0: 
        save_path = os.path.join(output_folder, f"hilsa_frame_{saved_count}.jpg")
        cv2.imwrite(save_path, frame)
        saved_count += 1
        
    frame_count += 1

cap.release()
print(f"Done! Extracted {saved_count} images for your Positive Samples.")