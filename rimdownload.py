import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Define the URL to scrape
base_url = "http://shambamap.hopto.org/Kenya/RIMs/022%20KIAMBU%20COUNTY/"

# Directory to save downloaded images
output_dir = r"C:\\Users\\ADMIN\\Desktop\\kiambu"
os.makedirs(output_dir, exist_ok=True)

def download_jpegs(url, output_directory):
    try:
        # Get the HTML content of the webpage
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all links ending with .jpg or .jpeg
        img_links = soup.find_all('a', href=True)
        jpeg_links = [link['href'] for link in img_links if link['href'].lower().endswith(('.jpg', '.jpeg'))]

        # Download each image
        for img_link in jpeg_links:
            # Construct the full image URL
            img_url = urljoin(url, img_link)
            img_name = os.path.basename(img_link)
            img_path = os.path.join(output_directory, img_name)

            # Skip if the file already exists
            if os.path.exists(img_path):
                print(f"Skipping: {img_url} (already downloaded)")
                continue

            print(f"Downloading: {img_url}")
            try:
                img_response = requests.get(img_url, stream=True)
                img_response.raise_for_status()

                # Save the image to the output directory
                with open(img_path, 'wb') as img_file:
                    for chunk in img_response.iter_content(chunk_size=8192):
                        img_file.write(chunk)

            except requests.exceptions.RequestException as e:
                print(f"Failed to download {img_url}: {e}")
        
        print(f"Downloaded {len(jpeg_links)} JPEGs to {output_directory}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Run the download function
download_jpegs(base_url, output_dir)



