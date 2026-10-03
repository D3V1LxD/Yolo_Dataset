import os
import random
from PIL import Image

# 1. Setup your folders
backgrounds_folder = 'Murky_Backgrounds'  # Put your empty water .jpgs here
foregrounds_folder = 'Transparent_Ilish'   # Put your cut-out fish .pngs here
output_images = 'Synthetic_Dataset/images'
output_labels = 'Synthetic_Dataset/labels'

os.makedirs(output_images, exist_ok=True)
os.makedirs(output_labels, exist_ok=True)

# 2. Load the file names
bg_files = [f for f in os.listdir(backgrounds_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
fg_files = [f for f in os.listdir(foregrounds_folder) if f.endswith('.png')] # MUST be PNG for transparency

if not bg_files or not fg_files:
    print("Error: Make sure you have images in both the backgrounds and foregrounds folders!")
    exit()

num_images_to_generate = 3000 # Change this to make as many as you need!

print(f"Generating {num_images_to_generate} synthetic underwater images with auto-labels...")

for i in range(num_images_to_generate):
    # 3. Pick a random background and random fish
    bg_path = os.path.join(backgrounds_folder, random.choice(bg_files))
    fg_path = os.path.join(foregrounds_folder, random.choice(fg_files))

    bg = Image.open(bg_path).convert("RGBA")
    fish = Image.open(fg_path).convert("RGBA")

    bg_width, bg_height = bg.size

    # 4. Randomly resize the fish so the AI learns different distances
    scale_factor = random.uniform(0.2, 0.6) # Fish will be 20% to 60% the size of the background
    new_fish_width = int(bg_width * scale_factor)
    # Maintain aspect ratio
    new_fish_height = int(fish.size[1] * (new_fish_width / fish.size[0])) 
    fish = fish.resize((new_fish_width, new_fish_height), Image.Resampling.LANCZOS)

    # 5. Randomly pick a spot to paste the fish
    max_x = bg_width - new_fish_width
    max_y = bg_height - new_fish_height
    
    # Ensure we don't get negative bounds if the background is too small
    paste_x = random.randint(0, max(1, max_x))
    paste_y = random.randint(0, max(1, max_y))

    # Paste the fish using its alpha channel (transparency) as the mask
    bg.paste(fish, (paste_x, paste_y), fish)

    # 6. Convert back to RGB to save as JPG
    final_image = bg.convert("RGB")
    
    image_filename = f"synthetic_hilsa_{i}.jpg"
    final_image.save(os.path.join(output_images, image_filename))

    # --- THE MAGIC: AUTOMATIC YOLO ANNOTATION MATH ---
    # YOLO format: Class X_center Y_center Width Height (all normalized from 0 to 1)
    
    x_center = (paste_x + (new_fish_width / 2.0)) / bg_width
    y_center = (paste_y + (new_fish_height / 2.0)) / bg_height
    norm_width = new_fish_width / bg_width
    norm_height = new_fish_height / bg_height

    label_filename = f"synthetic_hilsa_{i}.txt"
    with open(os.path.join(output_labels, label_filename), 'w') as f:
        # '0' is your Class ID for Hilsa
        f.write(f"0 {x_center:.6f} {y_center:.6f} {norm_width:.6f} {norm_height:.6f}\n")

print("\nSuccess! Your fully annotated synthetic dataset is ready.")