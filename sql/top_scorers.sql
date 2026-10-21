-- Rank known scorers, excluding own goals.
SELECT
    p.name AS player,
    COUNT(*) AS goals
FROM goals AS g
JOIN players AS p ON g.scorer_player_id = p.player_id
WHERE g.own_goal = 0
GROUP BY p.player_id, p.name
ORDER BY goals DESC, player
LIMIT 10;