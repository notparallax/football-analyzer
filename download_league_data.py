import os
import requests
from bs4 import BeautifulSoup

# Base URL for downloads
BASE_URL = "https://www.football-data.co.uk/"

# Dictionary mapping league codes to names
league_code = {
    'E0': 'Premier League',
    'E1': 'Championship',
    'E2': 'League 1',
    'E3': 'League 2',
    'EC': 'Conference',
    # Add more leagues as needed
}

def delete_file_if_exists(file_path):
    """Delete the file at file_path if it exists."""
    if os.path.isfile(file_path):
        try:
            os.remove(file_path)
            print(f"Deleted existing file: {file_path}")
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")
    else:
        print(f"No file to delete at: {file_path}")

def download_file(url, year, league_code_key):
    league_name = league_code.get(league_code_key, 'Unknown League')
    
    # Construct the directory structure
    base_dir = f"data/{year}/{league_name}"
    os.makedirs(base_dir, exist_ok=True)

    # Create the file name
    file_name = f"{league_name.replace(' ', '_')}_{year}.csv"
    file_path = os.path.join(base_dir, file_name)

    # Check if the file exists and delete it if it does
    delete_file_if_exists(file_path)

    # Download the file
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {file_path}")
    else:
        print(f"Failed to download {url}: {response.status_code}")

def scrape_links(page_url):
    try:
        # Send a GET request to the webpage
        response = requests.get(page_url)
        response.raise_for_status()

        # Parse the webpage content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all links to CSV files
        links = soup.find_all('a', href=True)

        # Filter and download relevant links
        for link in links:
            href = link['href']
            if href.endswith(".csv"):
                # Extract year and league code from the href
                parts = href.split("/")
                year = parts[1]  # Assuming year is in the second part
                league_code_key = parts[2].split(".")[0]  # Assuming league code is in the third part
                print(league_code_key)
                # Construct the full download URL dynamically
                download_url = f"{BASE_URL}{href}"
                download_file(download_url, year, league_code_key)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Example usage
page_url = f'{BASE_URL}englandm.php'
scrape_links(page_url)