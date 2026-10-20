import csv
from pathlib import Path

data_dir = Path("data/raw")

# Visit each CSV file.
for file_name in ("results.csv", "goalscorers.csv"):
    file_path = data_dir / file_name

    with file_path.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        print(f"\n{file_name}")
        print("Columns:", reader.fieldnames)

        missing_by_column = {}
        for column in reader.fieldnames:
            missing_by_column[column] = 0

        row_count = 0
        missing_scorer_examples = []

        # Count rows and missing cells by column.
        for row_number, row in enumerate(reader, start=1):
            row_count += 1
            if row_number <= 3:
                print(row)

            if file_name == "goalscorers.csv":
                if row["scorer"] == "" or row["scorer"] == "NA":
                    if len(missing_scorer_examples) < 3:
                        missing_scorer_examples.append(row)

            for column in reader.fieldnames:
                if row[column] == "" or row[column] == "NA":
                    missing_by_column[column] += 1

        print("Rows:", row_count)
        print("Missing by column:", missing_by_column)
        if file_name == "goalscorers.csv":
            for example in missing_scorer_examples:
                print("Missing scorer example:", example)
