-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

IF EXISTS (SELECT 1 FROM pg_database WHERE datname = 'tournament') THEN
    DROP DATABASE tournament;
END IF;

CREATE DATABASE tournament;

\c tournament;

-- Definition table for all players known to the system
CREATE TABLE players (
    player_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

-- Definition table for all tournaments known to the system
CREATE TABLE tournaments (
    tournament_id SERIAL PRIMARY KEY,
    begin_date date DEFAULT CURRENT_DATE,
    number_of_players SMALLINT NOT NULL
);

-- Contains all the matches played, each match saved against the tournament that it is part of. Each match is between player1 and player2. Winner is either one of them, or can be null in case of a draw
CREATE TABLE matches (
    match_id SERIAL PRIMARY KEY,
    tournament_id INTEGER REFERENCES tournaments(tournament_id),
    player1 INTEGER REFERENCES players(player_id) NOT NULL,
    player2 INTEGER REFERENCES players(player_id) NOT NULL,
    winner INTEGER REFERENCES players(player_id)
);

-- Relationship between tournaments and players. A row will be inserted here when a player registers. After a player plays a match, corresponding rows will be updated
CREATE TABLE tournament_players (
    tournament_id INTEGER REFERENCES tournaments(tournament_id),
    player_id INTEGER REFERENCES players(player_id) NOT NULL,
    bye BOOLEAN DEFAULT FALSE,
    total_matches SMALLINT DEFAULT 0,
    total_wins SMALLINT DEFAULT 0
);

-- View mapping most used columns from players and tournament_players
CREATE VIEW tournament_players_view AS 
    SELECT p.player_id, p.name, t.total_wins, t.total_matches, t.tournament_id 
    FROM players p, tournament_players t 
    WHERE t.player_id = p.player_id;