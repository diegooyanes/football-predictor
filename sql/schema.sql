CREATE TABLE IF NOT EXISTS teams (
    team_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS matches (
    match_id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    home_team_id INTEGER NOT NULL,
    away_team_id INTEGER NOT NULL,
    home_score INTEGER NOT NULL CHECK (home_score >= 0),
    away_score INTEGER NOT NULL CHECK (away_score >= 0),
    tournament TEXT NOT NULL,
    city TEXT NOT NULL,
    country TEXT NOT NULL,
    neutral INTEGER NOT NULL CHECK (neutral IN (0, 1)),
    FOREIGN KEY (home_team_id) REFERENCES teams(team_id),
    FOREIGN KEY (away_team_id) REFERENCES teams(team_id)
);

CREATE TABLE IF NOT EXISTS goals (
    goal_id INTEGER PRIMARY KEY,
    match_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    scorer_player_id INTEGER,
    assist_player_id INTEGER,
    minute INTEGER CHECK (minute >= 0),
    own_goal INTEGER NOT NULL CHECK (own_goal IN (0, 1)),
    penalty INTEGER NOT NULL CHECK (penalty IN (0, 1)),
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (scorer_player_id) REFERENCES players(player_id),
    FOREIGN KEY (assist_player_id) REFERENCES players(player_id)
);