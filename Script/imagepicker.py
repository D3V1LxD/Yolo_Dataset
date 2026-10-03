import shutil
import random
from pathlib import Path
import sys

def pick_random_images(source_folder, destination_folder, num_to_pick=5):
    source_dir = Path(source_folder)
    dest_dir = Path(destination_folder)
    
    # 1. Check if source exists
    if not source_dir.exists() or not source_dir.is_dir():
        print(f"Error: The source directory '{source_folder}' does not exist.")
        sys.exit(1)
        
    # 2. Create the destination folder if it doesn't exist yet
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    # Image extensions to look for
    valid_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
    total_copied = 0
    folders_processed = 0

    print(f"Scanning '{source_dir.name}' for subfolders...\n")

    # 3. Loop through every item in the source folder
    for subdir in source_dir.iterdir():
        # Make sure it's actually a folder
        if subdir.is_dir():
            # Find all images in this specific subfolder
            images_in_folder = [
                f for f in subdir.iterdir() 
                if f.is_file() and f.suffix.lower() in valid_extensions
            ]
            
            if not images_in_folder:
                print(f"⏭️ Skipping '{subdir.name}' (No images found)")
                continue
                
            # 4. Pick random images. 
            # If the folder has fewer than 5 images, just take all of them.
            amount_to_pick = min(num_to_pick, len(images_in_folder))
            selected_images = random.sample(images_in_folder, amount_to_pick)
            
            # 5. Copy the selected images to the new destination
            for img_path in selected_images:
                # Prepend the folder name to avoid accidentally overwriting files with the same name
                new_filename = f"{subdir.name}_{img_path.name}"
                new_file_path = dest_dir / new_filename
                
                # Copy the file (copy2 preserves original metadata like creation date)
                shutil.copy2(img_path, new_file_path)
                total_copied += 1
                
            print(f"✅ Copied {amount_to_pick} images from '{subdir.name}'")
            folders_processed += 1

    print(f"\nDone! Successfully copied a total of {total_copied} images from {folders_processed} folders.")
    print(f"You can find your random samples in: {dest_dir.resolve()}")

# --- Run the script ---
if __name__ == "__main__":
    # Replace these paths with your actual folder locations
    # SOURCE: The main folder that contains all the subfolders
    SOURCE_PATH = r"C:\path\to\your\main_dataset_folder" 
    
    # DESTINATION: The new folder where all the randomly picked images will go
    DESTINATION_PATH = r"C:\path\to\your\new_random_subset_folder"
    
    # You can change the '5' to any number you want!
    pick_random_images(SOURCE_PATH, DESTINATION_PATH, num_to_pick=5)