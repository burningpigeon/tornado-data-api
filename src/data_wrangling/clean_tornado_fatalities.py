from pathlib import Path
import re

import pandas as pd

from src.data_wrangling.tornado_fatalities_data_cleaning import clean_tornado_fatalities

# -------------------------------------------------
# Configuration
# -------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DETAILS_FOLDER = PROJECT_ROOT / "cleaned_data" / "storm_details"
FATALITIES_FOLDER = PROJECT_ROOT / ".imported_data" / "storm_fatalities"
OUTPUT_FOLDER = PROJECT_ROOT / "cleaned_data" / "storm_fatalities"

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------


def extract_year(filename):
    """
    Extract the storm event year from a filename.

    Example:
        StormEvents_details-ftp_v1.0_d2015_c20260323.csv
                                     ^^^^

    Returns:
        "2015"
    """
    match = re.search(r"_d(\d{4})_", filename)
    return match.group(1) if match else None


# -------------------------------------------------
# Build a lookup table of cleaned details files
# -------------------------------------------------

details_lookup = {}

for file in DETAILS_FOLDER.glob("StormEvents_details*.csv"):
    year = extract_year(file.name)

    if year is not None:
        details_lookup[year] = file

print(f"Found {len(details_lookup)} cleaned details datasets.")

# -------------------------------------------------
# Process each fatalities file
# -------------------------------------------------

fatality_files = sorted(FATALITIES_FOLDER.glob("StormEvents_fatalities*.csv"))

print(f"Found {len(fatality_files)} fatalities datasets.\n")

for fatality_file in fatality_files:

    year = extract_year(fatality_file.name)

    if year is None:
        print(f"Skipping {fatality_file.name}: could not determine year.")
        continue

    details_file = details_lookup.get(year)

    if details_file is None:
        print(f"Skipping {fatality_file.name}: no cleaned details file found for {year}.")
        continue

    print(f"Processing {year}...")

    cleaned_details = pd.read_csv(details_file)
    storm_fatalities = pd.read_csv(fatality_file)

    cleaned_fatalities = clean_tornado_fatalities(
        cleaned_details,
        storm_fatalities
    )

    output_file = OUTPUT_FOLDER / fatality_file.name

    cleaned_fatalities.to_csv(output_file, index=False)

    print(f"Saved {output_file.name}")

print("\nFinished!")