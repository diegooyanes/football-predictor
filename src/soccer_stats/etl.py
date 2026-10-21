import csv
import sqlite3
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[2]
SCHEMA_PATH = PROJECT_DIR / "sql" / "schema.sql"
RESULTS_PATH = PROJECT_DIR / "data" / "raw" / "results.csv"
GOALS_PATH = PROJECT_DIR / "data" / "raw" / "goalscorers.csv"
DATABASE_PATH = PROJECT_DIR / "data" / "soccer_stats.db"


def get_team_id(connection, team_ids, name):
    if name not in team_ids:
        cursor = connection.execute(
            "INSERT INTO teams (name) VALUES (?)",
            (name,),
        )
        team_ids[name] = cursor.lastrowid

    return team_ids[name]


def get_player_id(connection, player_ids, name):
    if name in ("", "NA"):
        return None

    if name not in player_ids:
        cursor = connection.execute(
            "INSERT INTO players (name) VALUES (?)",
            (name,),
        )
        player_ids[name] = cursor.lastrowid

    return player_ids[name]


def load_matches(connection):
    team_ids = {}
    match_ids = {}
    match_count = 0

    with RESULTS_PATH.open(encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source)

        for row in reader:
            home_team_id = get_team_id(connection, team_ids, row["home_team"])
            away_team_id = get_team_id(connection, team_ids, row["away_team"])
            neutral = {"TRUE": 1, "FALSE": 0}[row["neutral"]]

            cursor = connection.execute(
                """
                INSERT INTO matches (
                    date, home_team_id, away_team_id,
                    home_score, away_score, tournament,
                    city, country, neutral
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    row["date"],
                    home_team_id,
                    away_team_id,
                    int(row["home_score"]),
                    int(row["away_score"]),
                    row["tournament"],
                    row["city"],
                    row["country"],
                    neutral,
                ),
            )

            key = (row["date"], row["home_team"], row["away_team"])

            # Mark repeated match keys as ambiguous.
            if key in match_ids:
                match_ids[key] = None
            else:
                match_ids[key] = cursor.lastrowid

            match_count += 1

    return match_count, team_ids, match_ids


def load_goals(connection, team_ids, match_ids):
    player_ids = {}
    goal_count = 0

    with GOALS_PATH.open(encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source)

        for row in reader:
            key = (row["date"], row["home_team"], row["away_team"])
            match_id = match_ids.get(key)

            if match_id is None:
                raise ValueError(f"Missing or ambiguous match: {key}")

            minute = None if row["minute"] in ("", "NA") else int(row["minute"])

            connection.execute(
                """
                INSERT INTO goals (
                    match_id, team_id, scorer_player_id,
                    assist_player_id, minute, own_goal, penalty
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    match_id,
                    team_ids[row["team"]],
                    get_player_id(connection, player_ids, row["scorer"]),
                    get_player_id(connection, player_ids, row["assist"]),
                    minute,
                    {"TRUE": 1, "FALSE": 0}[row["own_goal"]],
                    {"TRUE": 1, "FALSE": 0}[row["penalty"]],
                ),
            )
            goal_count += 1

    return goal_count, len(player_ids)


def main():
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(schema)

        # Clear generated data before loading it again.
        connection.execute("DELETE FROM goals")
        connection.execute("DELETE FROM matches")
        connection.execute("DELETE FROM players")
        connection.execute("DELETE FROM teams")

        match_count, team_ids, match_ids = load_matches(connection)
        goal_count, player_count = load_goals(connection, team_ids, match_ids)

        connection.commit()
    finally:
        connection.close()

    print(f"Loaded {match_count} matches and {len(team_ids)} teams")
    print(f"Loaded {goal_count} goals and {player_count} named players")


if __name__ == "__main__":
    main()
