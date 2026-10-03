import os
import uuid

# 1. Define the folder containing the images you want to randomly rename
target_dir = os.path.join('Dataset', 'Resized_Positive_Samples')

print(f"Starting the random renaming process in: {target_dir} ...")

# 2. Walk through all folders and subfolders inside the target directory
for root, dirs, files in os.walk(target_dir):
    for file in files:
        # Check if the file is an image
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            
            # 3. Separate the file name from its extension (e.g., '.jpg')
            file_extension = os.path.splitext(file)[1]
            
            # 4. Generate a completely random, unique 32-character name using UUID
            random_name = uuid.uuid4().hex + file_extension
            
            # 5. Create the full file paths for the old and new names
            old_file_path = os.path.join(root, file)
            new_file_path = os.path.join(root, random_name)
            
            try:
                # 6. Actually rename the file on your hard drive
                os.rename(old_file_path, new_file_path)
                print(f"Renamed: {file}  --->  {random_name}")
            except Exception as e:
                print(f"Error renaming {file}: {e}")

print("\nAll images have been successfully assigned random names!")