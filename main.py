# First, you need to install the library this script uses.
# Open your terminal or command prompt and run:
# pip install icrawler

from icrawler.builtin import BingImageCrawler
import os

def download_images(query, limit=1000, output_dir='dataset'):
    """
    Downloads images using icrawler (Bing Image Crawler).
    
    Args:
        query (str): The search keyword.
        limit (int): The number of images to download (set high to get all available).
        output_dir (str): The main directory to save images into.
    """
    print(f"Starting download for: '{query}'...")
    print(f"Attempting to download up to {limit} images (will get all available)...")
    
    # Create a specific output folder for this query
    specific_dir = os.path.join(output_dir, query.replace(' ', '_'))
    
    if not os.path.exists(specific_dir):
        os.makedirs(specific_dir)
    
    try:
        # Create crawler instance
        bing_crawler = BingImageCrawler(
            downloader_threads=4,  # Number of threads for downloading
            storage={'root_dir': specific_dir}
        )
        
        # Start crawling
        bing_crawler.crawl(
            keyword=query,
            max_num=limit,
            min_size=(200, 200),  # Minimum image size to filter out tiny images
            max_size=None
        )
        
        # Count downloaded images
        if os.path.exists(specific_dir):
            image_files = [f for f in os.listdir(specific_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'))]
            print(f"\n✓ Successfully downloaded {len(image_files)} images to: '{specific_dir}'")
        else:
            print(f"\nDownload completed for: '{specific_dir}'")
        
    except Exception as e:
        print(f"An error occurred while downloading for '{query}': {e}")
        print("Note: Some images may have been downloaded before the error occurred.")
        # Count any images that were downloaded before error
        if os.path.exists(specific_dir):
            image_files = [f for f in os.listdir(specific_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'))]
            if image_files:
                print(f"Partial download: {len(image_files)} images saved before error.")

# --- Main part of the script ---
if __name__ == "__main__":
    
    # --- Configuration ---
    # Set your search keywords here - targeting 10,000+ natural/underwater Hilsha fish images
    search_queries = [
        "Hilsa fish underwater",
        "Hilsa fish swimming",
        "Hilsa fish natural habitat",
        "Hilsa fish river",
        "Hilsa fish water",
        "Ilish fish underwater",
        "Ilish fish swimming",
        "Ilish fish natural",
        "Tenualosa ilisha underwater",
        "Tenualosa ilisha swimming",
        "Tenualosa ilisha natural",
        "Hilsa fish ocean",
        "Hilsa fish marine",
        "Hilsa fish aquatic",
        "Hilsa fish Bangladesh river",
        "Hilsa fish Padma river",
        "Hilsa fish Ganges",
        "Ilish fish river",
        "Ilish fish water natural",
        "Hilsa shad fish underwater",
        "Hilsa herring fish swimming",
        "Tenualosa ilisha aquatic",
        "Hilsa fish in water",
        "Ilish fish in water",
        "Hilsa fish sea",
        "Hilsa fish freshwater",
        "Hilsa fish wild",
        "Ilish fish wild natural",
        "Tenualosa ilisha wild",
        "Hilsa fish school swimming"
    ]
    
    # Set the number of images you want to download *per keyword*.
    # With 30 keywords × 1000 limit = up to 30,000 images (will get all available)
    images_per_keyword = 1000  
    
    # Set the main output directory.
    main_dataset_folder = 'hilsa_fish_dataset'
    # ---------------------
    
    if not os.path.exists(main_dataset_folder):
        os.makedirs(main_dataset_folder)

    for query in search_queries:
        download_images(query, limit=images_per_keyword, output_dir=main_dataset_folder)
        print("-" * 20)
        
    print("\nAll download tasks complete.")
    print(f"Please check the '{main_dataset_folder}' directory.")
    print("IMPORTANT: You must manually review all images before training!")