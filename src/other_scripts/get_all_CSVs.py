import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/"
DETAILS_FOLDER = r"./storm_data/details"
FATALITIES_FOLDER = r"./storm_data/fatalities"

def download_file(url, output_path):
    """Download a file with progress indication."""
    response = requests.get(url, stream=True)
    response.raise_for_status()

    total_size = int(response.headers.get("content-length", 0))

    with open(output_path, "wb") as file:
        downloaded = 0

        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
                downloaded += len(chunk)

                if total_size:
                    percent = downloaded / total_size * 100
                    print(
                        f"\rDownloading {os.path.basename(output_path)} "
                        f"({percent:.1f}%)",
                        end=""
                    )
    print()


def main():
    os.makedirs(DETAILS_FOLDER, exist_ok=True)
    os.makedirs(FATALITIES_FOLDER, exist_ok=True)

    print("Retrieving NOAA file listing...")

    response = requests.get(BASE_URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    links = [
        a["href"]
        for a in soup.find_all("a", href=True)
    ]

    details_files = []
    fatalities_files = []

    for filename in links:
        if filename.startswith("StormEvents_details"):
            details_files.append(filename)

        elif filename.startswith("StormEvents_fatalities"):
            fatalities_files.append(filename)

    print(f"Found {len(details_files)} details files")
    print(f"Found {len(fatalities_files)} fatalities files")

    # Download details files
    for filename in details_files:
        output_path = os.path.join(DETAILS_FOLDER, filename)

        if os.path.exists(output_path):
            print(f"Skipping existing file: {filename}")
            continue

        download_file(urljoin(BASE_URL, filename),output_path)

    # Download fatalities files
    for filename in fatalities_files:
        output_path = os.path.join(FATALITIES_FOLDER, filename)

        if os.path.exists(output_path):
            print(f"Skipping existing file: {filename}")
            continue

        download_file(urljoin(BASE_URL, filename),output_path)

    print("Done!")


if __name__ == "__main__":
    main()