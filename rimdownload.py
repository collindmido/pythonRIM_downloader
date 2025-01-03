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
            print(f"Downloading: {img_url}")

            try:
                img_response = requests.get(img_url, stream=True)
                img_response.raise_for_status()

                # Save the image to the output directory
                img_name = os.path.basename(img_link)
                img_path = os.path.join(output_directory, img_name)

                with open(img_path, 'wb') as img_file:
                    for chunk in img_response.iter_content(chunk_size=8192):
                        img_file.write(chunk)

            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")

        print(f"Downloaded {len(jpeg_links)} JPEGs to {output_directory}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Run the download function
download_jpegs(base_url, output_dir)

# Required packages to install:
# - requests: To make HTTP requests.
# - beautifulsoup4: To parse HTML content.

# Install them using the following command:
# pip install requests beautifulsoup4

# Steps to create a development environment:
# 1. Navigate to the target directory:
#    cd C:\Users\ADMIN\Desktop\kiambu
# 2. Create a virtual environment:
#    python -m venv .venv
# 3. Activate the virtual environment in VS Code:
#    - Open the folder (C:\Users\ADMIN\Desktop\kiambu) in VS Code.
#    - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS) to open the Command Palette.
#    - Search for and select "Python: Select Interpreter."
#    - Choose the interpreter that corresponds to the .venv directory (e.g., `.venv\\Scripts\\python.exe`).
# 4. Activate the virtual environment manually (optional):
#    - On Windows: Execute the following command in Command Prompt or PowerShell:
#      .\.venv\Scripts\activate
# 5. Install required packages:
#    pip install requests beautifulsoup4
# 6. Verify the virtual environment is active:
#    Your terminal in VS Code should show a prefix like (.venv).
# 7. Run the script within the virtual environment to ensure dependencies are managed correctly.
