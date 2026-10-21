-- Rank teams by goals scored in match results.
SELECT
    t.name AS team,
    COUNT(*) AS matches_played,
    SUM(s.goals) AS total_goals,
    ROUND(AVG(s.goals), 2) AS goals_per_match
FROM (
    SELECT home_team_id AS team_id, home_score AS goals
    FROM matches

    UNION ALL

    SELECT away_team_id AS team_id, away_score AS goals
    FROM matches
) AS s
JOIN teams AS t ON s.team_id = t.team_id
GROUP BY t.team_id, t.name
ORDER BY total_goals DESC
LIMIT 10;