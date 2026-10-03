import cv2
from pathlib import Path
import sys

def apply_clahe_to_folder(folder_path, clip_limit=2.0, tile_grid_size=(8, 8)):
    directory = Path(folder_path)
    
    if not directory.exists() or not directory.is_dir():
        print(f"Error: The directory '{folder_path}' does not exist.")
        sys.exit(1)
        
    # Gather all image files
    extensions = ('*.png', '*.jpg', '*.jpeg', '*.webp')
    image_files = []
    for ext in extensions:
        image_files.extend(directory.glob(ext))
        image_files.extend(directory.glob(ext.upper()))
        
    image_files = list(set(image_files))
    
    # Filter out images that already have '_CLAHE' in the name to avoid infinite loops
    image_files = [f for f in image_files if '_CLAHE' not in f.name]

    if not image_files:
        print("No un-processed images found in the specified directory.")
        return

    print(f"Found {len(image_files)} images. Applying CLAHE preprocessing...\n")
    
    # Create the CLAHE object
    # clip_limit: Threshold for contrast limiting. Higher means more contrast.
    # tile_grid_size: Divides the image into an 8x8 grid for localized equalization.
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    
    success_count = 0

    for img_path in image_files:
        try:
            # Read the image using OpenCV (loads as BGR format by default)
            img = cv2.imread(str(img_path))
            
            if img is None:
                print(f"⚠️ Could not read {img_path.name}. Skipping.")
                continue

            # 1. Convert BGR to LAB color space
            lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
            
            # 2. Split the LAB image into L, A, and B channels
            l_channel, a_channel, b_channel = cv2.split(lab)
            
            # 3. Apply CLAHE ONLY to the L (Lightness) channel
            cl = clahe.apply(l_channel)
            
            # 4. Merge the enhanced L channel back with the A and B channels
            merged_lab = cv2.merge((cl, a_channel, b_channel))
            
            # 5. Convert back to BGR color space for saving
            final_img = cv2.cvtColor(merged_lab, cv2.COLOR_LAB2BGR)
            
            # Create new filename (e.g., image1_CLAHE.png)
            new_filename = f"{img_path.stem}_CLAHE{img_path.suffix}"
            new_file_path = directory / new_filename
            
            # Save the enhanced image
            cv2.imwrite(str(new_file_path), final_img)
            
            print(f"✅ Enhanced: {img_path.name} -> {new_filename}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ Failed to process {img_path.name}: {e}")

    print(f"\nDone! Successfully applied CLAHE to {success_count} images.")

# --- Run the script ---
if __name__ == "__main__":
    # Replace this with your dataset path
    TARGET_FOLDER = r"G:\4th Year 1st Semester\Thesis NAOE 4000\Image Downloader\Dataset\Resized_Positive_Samples"
    
    # You can tweak clip_limit (try 3.0 or 4.0 if you want extreme contrast)
    apply_clahe_to_folder(TARGET_FOLDER, clip_limit=2.0)