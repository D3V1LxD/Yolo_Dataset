from pathlib import Path
from PIL import Image
import sys

def convert_webp_to_png(folder_path):
    # Create a Path object for the directory
    directory = Path(folder_path)
    
    # Check if the directory exists
    if not directory.exists() or not directory.is_dir():
        print(f"Error: The directory '{folder_path}' does not exist.")
        sys.exit(1)
        
    # Find all .webp files in the folder (case-insensitive)
    webp_files = list(directory.glob("*.webp")) + list(directory.glob("*.WEBP"))
    
    if not webp_files:
        print("No .webp files found in the specified directory.")
        return

    print(f"Found {len(webp_files)} .webp files. Starting conversion...\n")

    success_count = 0
    
    # Loop through each .webp file
    for webp_file in webp_files:
        # Create the new filename by replacing .webp with .png
        png_file = webp_file.with_suffix('.png')
        
        try:
            # Open the webp image and save it as png
            with Image.open(webp_file) as img:
                # webp can be RGBA (transparent) or RGB. Pillow handles this conversion smoothly to PNG.
                img.save(png_file, format="PNG")
                
            print(f"✅ Converted: {webp_file.name} -> {png_file.name}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ Failed to convert {webp_file.name}: {e}")

    print(f"\nDone! Successfully converted {success_count} out of {len(webp_files)} files.")

# --- Run the script ---
if __name__ == "__main__":
    # Replace the path below with the path to your folder
    # Example: "G:/4th Year 1st Semester/Thesis NAOE 4000/Image Downloader/Dataset"
    TARGET_FOLDER = r"G:\4th Year 1st Semester\Thesis NAOE 4000\Image Downloader\Images" 
    
    convert_webp_to_png(TARGET_FOLDER)