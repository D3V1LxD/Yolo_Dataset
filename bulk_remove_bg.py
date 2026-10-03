import os
from rembg import remove

# 1. Setup your folders
input_folder = 'Ilish'     # Put all your standard JPGs of Hilsa in here
output_folder = 'Transparent_Ilish'   # The script will save the perfect PNGs here

os.makedirs(output_folder, exist_ok=True)

print(f"Scanning '{input_folder}' for images to process...")

# 2. Loop through every image in the folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        input_path = os.path.join(input_folder, filename)
        
        # Force the output file to be a .png, regardless of what the input was
        output_filename = os.path.splitext(filename)[0] + '.png'
        output_path = os.path.join(output_folder, output_filename)
        
        print(f"Slicing background out of: {filename}...")
        
        # 3. Read the image, remove the background, and save it
        with open(input_path, 'rb') as file_in:
            input_image = file_in.read()
            
        output_image = remove(input_image)
        
        with open(output_path, 'wb') as file_out:
            file_out.write(output_image)

print("\nSuccess! All fish have been isolated and saved as transparent PNGs.")