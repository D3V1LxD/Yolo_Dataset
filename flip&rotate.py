from pathlib import Path
from PIL import Image, ImageOps
import uuid
import sys

def augment_all_images(folder_path):
    directory = Path(folder_path)
    
    if not directory.exists() or not directory.is_dir():
        print(f"Error: The directory '{folder_path}' does not exist.")
        sys.exit(1)
        
    # Get all images (taking a snapshot so we don't process newly created ones)
    extensions = ('*.png', '*.jpg', '*.jpeg', '*.webp')
    image_files = []
    for ext in extensions:
        image_files.extend(directory.glob(ext))
        image_files.extend(directory.glob(ext.upper()))
        
    image_files = list(set(image_files)) 
    
    if not image_files:
        print("No images found in the specified directory.")
        return

    print(f"Found {len(image_files)} images. Generating all flips and rotations...\n")
    
    total_created = 0

    for img_path in image_files:
        try:
            with Image.open(img_path) as img:
                # Define all transformations to apply to THIS image
                transformations = {
                    "h_flip": ImageOps.mirror(img),
                    "v_flip": ImageOps.flip(img),
                    "rot_90": img.rotate(90, expand=True),
                    "rot_180": img.rotate(180, expand=True),
                    "rot_270": img.rotate(270, expand=True)
                }

                # Save each transformation with a random unique name
                for trans_name, trans_img in transformations.items():
                    random_string = uuid.uuid4().hex[:8]
                    
                    # Naming format: [random8chars]_[transformation].extension
                    new_filename = f"{random_string}_{trans_name}{img_path.suffix}"
                    new_file_path = directory / new_filename
                    
                    trans_img.save(new_file_path)
                    total_created += 1
                    
            print(f"✅ Created 5 augmented versions of {img_path.name}")
                
        except Exception as e:
            print(f"❌ Failed to process {img_path.name}: {e}")

    print(f"\nDone! Successfully created {total_created} new augmented images from {len(image_files)} originals.")

# --- Run the script ---
if __name__ == "__main__":
    # Replace this with your dataset path
    TARGET_FOLDER = r"G:\4th Year 1st Semester\Thesis NAOE 4000\Image Downloader\Dataset\Positive_Samples"
    
    augment_all_images(TARGET_FOLDER)