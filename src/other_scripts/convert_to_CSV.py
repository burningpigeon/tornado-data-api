import gzip
import shutil
from pathlib import Path

# Change this to your download directory
ROOT_FOLDER = Path(r"C:\Users\mrmac\OneDrive\Desktop\Personal Projects\tornado data\.imported_data\storm_fatalities")

for gz_file in ROOT_FOLDER.rglob("*.csv.gz"):
    csv_file = gz_file.with_suffix("")  # removes the .gz suffix

    print(f"Extracting {gz_file.name}")

    with gzip.open(gz_file, "rb") as f_in:
        with open(csv_file, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

    # Delete the compressed file
    gz_file.unlink()

print("Finished!")