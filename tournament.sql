-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE tournament;

CREATE DATABASE tournament;

\c tournament;

-- Definition table for all players known to the system
CREATE TABLE players (
    player_id SERIAL primary key,
    name text not null
);

-- Definition table for all tournaments known to the system
CREATE TABLE tournaments (
    tournament_id SERIAL primary key,
    begin_date date DEFAULT CURRENT_DATE,
    number_of_players smallint not null
);

-- Contains all the matches played, each match saved against the tournament that it is part of. Each match is between player1 and player2. Winner is either one of them, or can be null in case of a draw
CREATE TABLE matches (
    match_id SERIAL primary key,
    tournament_id integer references tournaments(tournament_id),
    player1 integer references players(player_id) not null,
    player2 integer references players(player_id) not null,
    winner integer references players(player_id)
);

-- Relationship between tournaments and players. A row will be inserted here when a player registers. After a player plays a match, corresponding rows will be updated
CREATE TABLE tournament_players (
    tournament_id integer references tournaments(tournament_id),
    player_id integer references players(player_id) not null,
    bye boolean default false,
    total_matches smallint default 0,
    total_wins smallint default 0
);

-- View mapping most used columns from players and tournament_players
CREATE VIEW tournament_players_view AS SELECT p.player_id, p.name, t.total_wins, t.total_matches, t.tournament_id FROM players p, tournament_players t WHERE t.player_id = p.player_id