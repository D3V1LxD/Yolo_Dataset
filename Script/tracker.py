import cv2
import numpy as np
import time
import csv
from datetime import datetime
from ultralytics import YOLO

# 1. Load model & video
model = YOLO("runs/detect/hilsa_tracker_v17/weights/best.pt")
video_path = 'Shots.mp4'
cap = cv2.VideoCapture(video_path)

# 2. Camera math & Exporter setup
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
camera_center_x = frame_width // 2
camera_center_y = frame_height // 2

output_path = 'thesis_final_output.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# We use 30 as a default fallback for the exporter if it can't read the video FPS
out = cv2.VideoWriter(output_path, fourcc, 30.0, (frame_width, frame_height))

clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))

# CSV Logging Setup
csv_filename = 'auv_telemetry_data.csv'
csv_file = open(csv_filename, mode='w', newline='')
csv_writer = csv.writer(csv_file)
# Write the header row for your thesis data
csv_writer.writerow(['Frame', 'Time', 'Processing_FPS', 'Hilsa_Count', 'Aspect_Ratio', 'Error_X', 'Error_Y', 'Status'])

# Tracking Variables
frame_count = 0
last_known_x = camera_center_x
last_known_y = camera_center_y
target_found = False

print(f"Starting advanced tracking. Exporting video to: {output_path}")
print(f"Logging telemetry data to: {csv_filename}")

while cap.isOpened():
    # Start FPS Timer
    start_time = time.time()
    
    success, frame = cap.read()
    if not success:
        break

    frame_count += 1
    current_hilsa_count = 0
    fish_detected_this_frame = False

    # Real-Time Murky Water Filtering
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(lab)
    cl = clahe.apply(l_channel) 
    limg = cv2.merge((cl, a, b))
    enhanced_frame = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    # --- NEW: Persistent Tracking ---
    # We use model.track instead of model.predict to assign unique IDs to the fish
    results = model.track(enhanced_frame, persist=True, conf=0.5, verbose=False)

    aspect_ratio = 0.0
    error_x = 0
    error_y = 0

    if results[0].boxes.id is not None:
        boxes = results[0].boxes.xyxy.cpu()
        track_ids = results[0].boxes.id.int().cpu().tolist()
        clss = results[0].boxes.cls.cpu().tolist()
        confs = results[0].boxes.conf.cpu().tolist()

        for box, track_id, cls, conf in zip(boxes, track_ids, clss, confs):
            class_name = model.names[int(cls)]
            
            if class_name.lower() == 'hilsa':
                current_hilsa_count += 1
                fish_detected_this_frame = True
                
                x1, y1, x2, y2 = map(int, box)
                
                # Biological Aspect Ratio
                fish_width = x2 - x1
                fish_height = y2 - y1
                if fish_height > 0:
                    aspect_ratio = round(fish_width / fish_height, 2)

                # Canny Edge Isolation
                fish_roi = enhanced_frame[y1:y2, x1:x2]
                if fish_roi.size > 0:
                    gray_roi = cv2.cvtColor(fish_roi, cv2.COLOR_BGR2GRAY)
                    edges = cv2.Canny(gray_roi, 50, 150)
                    edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
                    enhanced_frame[y1:y2, x1:x2] = cv2.addWeighted(fish_roi, 0.7, edges_bgr, 0.5, 0)

                # Navigation Math
                fish_center_x = (x1 + x2) // 2
                fish_center_y = (y1 + y2) // 2
                
                # Update Last Known Position
                last_known_x = fish_center_x
                last_known_y = fish_center_y
                
                error_x = fish_center_x - camera_center_x
                error_y = fish_center_y - camera_center_y

                # Draw Visuals for Locked Target
                cv2.rectangle(enhanced_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(enhanced_frame, f'ID:{track_id} {class_name} | Ratio: {aspect_ratio}', 
                            (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.circle(enhanced_frame, (fish_center_x, fish_center_y), 5, (255, 0, 0), -1)
                
                # We only track the FIRST detected Hilsa in this basic logic to avoid motor confusion
                break 

    # --- NEW: Target Lost Logic ---
    if not fish_detected_this_frame:
        # Calculate error based on where the fish was last seen
        error_x = last_known_x - camera_center_x
        error_y = last_known_y - camera_center_y
        
        cv2.putText(enhanced_frame, 'TARGET LOST - USING LAST KNOWN POS', (int(frame_width/2) - 200, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.circle(enhanced_frame, (last_known_x, last_known_y), 5, (0, 165, 255), -1) # Orange dot for ghost position
        cv2.line(enhanced_frame, (camera_center_x, camera_center_y), (last_known_x, last_known_y), (0, 165, 255), 2)
        status_text = "LOST"
    else:
        cv2.line(enhanced_frame, (camera_center_x, camera_center_y), (last_known_x, last_known_y), (255, 255, 0), 2)
        status_text = "TRACKING"

    # Draw Camera Center
    cv2.circle(enhanced_frame, (camera_center_x, camera_center_y), 5, (0, 0, 255), -1)

    # --- NEW: Calculate Processing FPS ---
    end_time = time.time()
    processing_fps = round(1 / (end_time - start_time), 1)

    # Display Overlays
    current_time = datetime.now().strftime("%H:%M:%S")
    cv2.putText(enhanced_frame, f'Time: {current_time}', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(enhanced_frame, f'Frame: {frame_count}', (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(enhanced_frame, f'Compute FPS: {processing_fps}', (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(enhanced_frame, f'Nav Error X: {error_x}px | Y: {error_y}px', (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    # --- NEW: Log Data to CSV ---
    csv_writer.writerow([frame_count, current_time, processing_fps, current_hilsa_count, aspect_ratio, error_x, error_y, status_text])

    # Export Frame
    out.write(enhanced_frame)
    cv2.imshow('Advanced AUV Vision', enhanced_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
out.release()
csv_file.close() # Close the CSV file safely!
cv2.destroyAllWindows()
print("\nProcessing complete! Video and CSV Telemetry saved.")