import os

# 1. Define where the broken labels are
directories = [
    'YOLO_Dataset/labels/train',
    'YOLO_Dataset/labels/val'
]

fixed_count = 0

print("Scanning for labels that need fixing...")

# 2. Loop through both folders
for directory in directories:
    # Check if the directory actually exists first
    if not os.path.exists(directory):
        continue
        
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)
            
            # Read the current broken lines
            with open(filepath, 'r') as file:
                lines = file.readlines()
            
            # Open the file again to overwrite it with the fix
            with open(filepath, 'w') as file:
                for line in lines:
                    parts = line.strip().split()
                    
                    # Ensure it's a valid YOLO line (Class + 4 coordinates)
                    if len(parts) == 5:
                        parts[0] = '0'  # Force the Class ID to be 0
                        
                        # Write the corrected line back to the file
                        file.write(' '.join(parts) + '\n')
            
            fixed_count += 1

print(f"\nSuccessfully forced {fixed_count} label files to Class 0!")