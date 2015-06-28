README for tournament project

tournament.sql contains the database definitions statements required for running the project. It creates a database, tournament; four tables- players, matches, tournament_players and tournaments; and a view, tournament_players_view. The DB design is flexible to support odd number of players and matches that result in a draw.

tournament.py contains various functionality of implementing the scoring system of a Swiss-style tournament. It supports multiple tournaments, with each player and match tied to a tournament.

tournament_test.py tests functions in tournament.py.

TO RUN:

1. Connect to psql
        $ psql
2. Execute the SQL statements in tournament.sql
        >> \i tournament.sql
3. Exit psql. Run tournament_test.py
        $ python tournament_test.py