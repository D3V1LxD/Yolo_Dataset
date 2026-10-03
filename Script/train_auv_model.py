from ultralytics import YOLO

# This line protects the script so Windows can use multiple CPU cores safely
if __name__ == '__main__':
    
    print("Loading YOLOv8 Nano model...")
    model = YOLO('yolov8n.pt') 

    print("Starting training process on RTX 4060 Ti...")
    results = model.train(
        data='YOLO_Dataset/data.yaml', 
        epochs=50,                     
        imgsz=640,                     
        batch=16,                      
        device=0,                      
        name='hilsa_tracker_v3'        
    )

    print("\nTraining complete!")