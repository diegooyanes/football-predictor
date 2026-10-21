import csv
from pathlib import Path

csv_path = Path("data/raw/results.csv")
seen_keys = set()
duplicate_count = 0

with csv_path.open("r", encoding="utf-8", newline="") as csv_file:
    reader = csv.DictReader(csv_file)

    # Check whether a match lookup key has appeared before.
    for row in reader:
        match_key = (row["date"], row["home_team"], row["away_team"])

        if match_key in seen_keys:
            duplicate_count += 1
            print("Repeated key:", match_key)
        else:
            seen_keys.add(match_key)

print("Unique match keys:", len(seen_keys))
print("Repeated match rows:", duplicate_count)
