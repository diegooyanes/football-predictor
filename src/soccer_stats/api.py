import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query

PROJECT_DIR = Path(__file__).resolve().parents[2]
DATABASE_PATH = PROJECT_DIR / "data" / "soccer_stats.db"

app = FastAPI(title="Soccer Stats API")


@app.get("/teams")
def list_teams(limit: int = Query(20, ge=1, le=100)):
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    try:
        rows = connection.execute(
            "SELECT team_id, name FROM teams ORDER BY name LIMIT ?",
            (limit,),
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        connection.close()


@app.get("/matches/{match_id}")
def get_match(match_id: int):
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    try:
        match = connection.execute(
            """
            SELECT
                m.match_id,
                m.date,
                h.name AS home_team,
                a.name AS away_team,
                m.home_score,
                m.away_score,
                m.tournament,
                m.city,
                m.country,
                m.neutral
            FROM matches AS m
            JOIN teams AS h ON m.home_team_id = h.team_id
            JOIN teams AS a ON m.away_team_id = a.team_id
            WHERE m.match_id = ?
            """,
            (match_id,),
        ).fetchone()
    finally:
        connection.close()

    if match is None:
        raise HTTPException(status_code=404, detail="Match not found")

    return dict(match)


@app.get("/matches/{match_id}/goals")
def get_match_goals(match_id: int):
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    try:
        match = connection.execute(
            "SELECT 1 FROM matches WHERE match_id = ?",
            (match_id,),
        ).fetchone()

        if match is None:
            raise HTTPException(status_code=404, detail="Match not found")

        goals = connection.execute(
            """
            SELECT
                g.goal_id,
                t.name AS team,
                scorer.name AS scorer,
                assistant.name AS assist,
                g.minute,
                g.own_goal,
                g.penalty
            FROM goals AS g
            JOIN teams AS t ON g.team_id = t.team_id
            LEFT JOIN players AS scorer
                ON g.scorer_player_id = scorer.player_id
            LEFT JOIN players AS assistant
                ON g.assist_player_id = assistant.player_id
            WHERE g.match_id = ?
            ORDER BY g.goal_id
            """,
            (match_id,),
        ).fetchall()

        return [dict(goal) for goal in goals]
    finally:
        connection.close()
