import os
import requests
import time  # <-- This is the new tool we need to pause the script
from duckduckgo_search import DDGS

# 1. Define your negative samples
search_queries = [
    "Chapila fish underwater",
    "Pangasius fish underwater",
    "Rui fish underwater",
    "murky river water underwater",
    "underwater floating plastic bag",
    "underwater rocks and silt"
]

images_per_query = 50 

print("Starting the download process for Negative Samples...")

# 2. Loop through queries and download
for query in search_queries:
    print(f"\n---> Searching for: {query}")
    
    # Create a clean folder name for each query
    folder_name = query.replace(" ", "_")
    folder_path = os.path.join("Dataset", "Negative_Samples", folder_name)
    os.makedirs(folder_path, exist_ok=True)
    
    try:
        # Search for images
        with DDGS() as ddgs:
            results = list(ddgs.images(query, max_results=images_per_query))
            
        # Download each image found
        for i, result in enumerate(results):
            image_url = result.get("image")
            if not image_url:
                continue
                
            try:
                # Get the image data from the URL
                response = requests.get(image_url, timeout=10)
                if response.status_code == 200:
                    file_path = os.path.join(folder_path, f"image_{i+1}.jpg")
                    with open(file_path, "wb") as file:
                        file.write(response.content)
                    print(f"Downloaded: {file_path}")
            except Exception as e:
                print(f"Skipped image {i+1} (Download failed)")
        
        # --- THE FIX ---
        # Pause for 10 seconds before searching for the next fish to avoid getting blocked
        print(f"Finished {query}. Pausing for 10 seconds to bypass bot detection...")
        time.sleep(10) 
                
    except Exception as e:
        print(f"Error searching for {query}. DuckDuckGo may have blocked the connection: {e}")
        print("Pausing for 30 seconds to let the connection reset...")
        time.sleep(30)

print("\nAll downloads completed! Check your 'Dataset/Negative_Samples' folder.")