import csv
import sqlite3
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[2]
DATABASE_PATH = PROJECT_DIR / "data" / "soccer_stats.db"
RESULTS_PATH = PROJECT_DIR / "data" / "raw" / "results.csv"
GOALS_PATH = PROJECT_DIR / "data" / "raw" / "goalscorers.csv"


def count_csv_rows(path):
    with path.open(encoding="utf-8", newline="") as source:
        return sum(1 for row in csv.DictReader(source))


def main():
    expected_matches = count_csv_rows(RESULTS_PATH)
    expected_goals = count_csv_rows(GOALS_PATH)
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        actual_matches = connection.execute("SELECT COUNT(*) FROM matches").fetchone()[
            0
        ]
        actual_goals = connection.execute("SELECT COUNT(*) FROM goals").fetchone()[0]
        broken_links = connection.execute("PRAGMA foreign_key_check").fetchall()
        wrong_teams = connection.execute(
            """
            SELECT COUNT(*)
            FROM goals AS g
            JOIN matches AS m ON g.match_id = m.match_id
            WHERE g.team_id NOT IN (m.home_team_id, m.away_team_id)
            """
        ).fetchone()[0]
    finally:
        connection.close()

    if actual_matches != expected_matches:
        raise ValueError("Match count differs from results.csv")
    if actual_goals != expected_goals:
        raise ValueError("Goal count differs from goalscorers.csv")
    if broken_links:
        raise ValueError(f"Broken database links: {broken_links}")
    if wrong_teams:
        raise ValueError(f"Goals linked to the wrong team: {wrong_teams}")

    print(f"Matches checked: {actual_matches}")
    print(f"Goals checked: {actual_goals}")
    print("Database relationships checked: OK")


if __name__ == "__main__":
    main()
