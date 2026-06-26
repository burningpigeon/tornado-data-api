from pathlib import Path

import pandas as pd

from src.data_wrangling.tornado_data_wrangling import clean_tornado_details


# -----------------------
# Configuration
# -----------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FOLDER = PROJECT_ROOT / ".imported_data" / "storm_details"
OUTPUT_FOLDER = PROJECT_ROOT / "cleaned_data" / "storm_details"

COUNTY_DST_FILE = PROJECT_ROOT / "cleaned_data" / "cleaned_counties_data.csv"
DST_DATES_FILE = PROJECT_ROOT / "cleaned_data" / "DST - Sheet1.csv"

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# -----------------------

county_dst_info = pd.read_csv(COUNTY_DST_FILE)
dst_dates = pd.read_csv(DST_DATES_FILE)

files = sorted(INPUT_FOLDER.glob("StormEvents_details*.csv"))

print(f"Found {len(files)} files.\n")

for file in files:

    print(f"Cleaning {file.name}...")

    storm_details = pd.read_csv(file)

    cleaned = clean_tornado_details(
        storm_details,
        county_dst_info,
        dst_dates
    )

    output_file = OUTPUT_FOLDER / file.name

    cleaned.to_csv(output_file, index=False)

    print(f"Saved -> {output_file.name}")

print("\nFinished!")