import requests
import os
import zipfile
from pathlib import Path

def create_download_dir(directory="downloads"):
    base_dir = Path(__file__).parent
    download_path = base_dir / directory
 
    download_path.mkdir(parents=True, exist_ok=True)
    return download_path


def download_file(url, save_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded: {save_path}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")


def unzip_file(zip_path, extract_to="downloads"):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        os.remove(zip_path)
        print(f"Extracted and removed: {zip_path}")
    except Exception as e:
        print(f"Failed to unzip {zip_path}: {e}")






def process_files(download_uris, download_dir="downloads"):
    """Processes the list of URLs: download and unzip."""

    for url in download_uris:
        filename = url.split("/")[-1]  # Extract filename from URL
        save_path = download_dir / filename
     
        download_file(url, save_path)
        
        # Attempt to unzip only if the download succeeded
        if save_path.exists():
            unzip_file(save_path, download_dir)
        else:
            print(f"Skipping unzip for missing file: {save_path}")

def main():
   download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]
   
   download_dir = create_download_dir()
   process_files(download_uris, download_dir)


if __name__ == "__main__":
    main()