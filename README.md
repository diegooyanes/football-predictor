# Soccer Stats Pipeline + API

A Python project that loads international football results and goal events from CSV files into SQLite, checks data quality, exposes a REST API with FastAPI, and answers football questions with SQL.

## What the project does

```text
CSV files → Python ETL → SQLite database → FastAPI and SQL analysis
```

The ETL keeps the original CSV files unchanged. The SQLite database is generated locally and can be rebuilt by running the ETL again.

## Data source

The CSV files come from [International football results](https://github.com/martj42/international_results), published under [CC0-1.0](https://github.com/martj42/international_results/blob/master/LICENSE).

| File | Rows in this project | Meaning |
| --- | ---: | --- |
| `data/raw/results.csv` | 49,945 | One match result per row |
| `data/raw/goalscorers.csv` | 47,914 | One recorded goal event per row |

The goal-event file is not a complete record of every goal in every match, and it does not contain full player rosters.

## Stack

- Python 3.13.4
- SQLite, through Python's standard library
- FastAPI and Uvicorn

## Run locally (Windows PowerShell)

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe src\soccer_stats\etl.py
.\.venv\Scripts\python.exe src\soccer_stats\check_data.py
.\.venv\Scripts\python.exe -m uvicorn src.soccer_stats.api:app
```

Open `http://127.0.0.1:8000/docs` for the interactive API documentation. Stop the server with `Ctrl+C`.

The ETL creates `data/soccer_stats.db`. This generated file and the virtual environment are ignored by Git.

## Database design

- `teams`: one ID and name per team.
- `matches`: match result and context, with references to the home and away teams.
- `players`: names observed as scorers or assistants in the source data.
- `goals`: goal events linked to a match and team; scorer, assistant, and minute may be unknown.

Each match has its own `match_id`. Date and team names are not a safe unique ID: two rows for Tahiti vs New Caledonia share those values in the source CSV. The ETL keeps both records. If a goal event matches multiple games, the ETL raises an error instead of choosing one arbitrarily.

Missing scorer, assistant, and minute values become SQL `NULL`. The ETL preserves the goal event itself.

## API

| Endpoint | Result |
| --- | --- |
| `GET /teams?limit=20` | Teams ordered by name; limit from 1 to 100 |
| `GET /matches/{match_id}` | Match result and team names |
| `GET /matches/{match_id}/goals` | Recorded goal events for that match |

Example: `/matches/480/goals` returns four recorded goal events. An unknown match ID returns HTTP 404.

## SQL analysis

- `sql/analysis.sql`: top teams by total goals from match scores, including matches played and goals per match.
- `sql/top_scorers.sql`: top named scorers from recorded goal events, excluding own goals.

Run a query with Python's SQLite command-line module:

```powershell
.\.venv\Scripts\python.exe -X utf8 -m sqlite3 data\soccer_stats.db (Get-Content -Raw sql\analysis.sql)
```

The `-X utf8` option lets Python print player names with accented characters in Windows terminals.

The team ranking uses match scores because goal events do not cover all matches. The scorer ranking only covers named players in recorded events. Players with the same name are treated as one record because the source has no player IDs; this is a known limitation.

## Data quality

Run `src/soccer_stats/check_data.py` after the ETL. It compares CSV and database row counts, checks foreign-key relationships, and verifies that each recorded goal belongs to a team in its match.

For the current CSV files, the loaded database contains 49,945 matches, 337 teams, 47,914 goal events, and 15,613 distinct player names. Unknown values include 44 scorers, 254 minutes, and 45,838 assistants.

## Development roadmap

1. Repository and isolated Python environment — complete.
2. Explore and profile the source CSV files — complete.
3. Design the SQLite schema — complete.
4. Build a repeatable ETL pipeline — complete.
5. Add repeatable data-quality checks — complete.
6. Build and verify the REST API — complete.
7. Write and verify SQL analysis queries — complete.
8. Document setup, decisions, and limitations — complete.
