#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def createTournament(num):
    """Creates a new tournament and returns the tournament id"""
    conn = connect()
    c = conn.cursor()
    c.execute("insert into tournaments(number_of_players) values (%s) returning tournament_id", (num,))
    conn.commit()
    tournamentId = c.fetchone()[0]
    conn.close()
    return tournamentId

def deleteMatches(tournamentId):
    """Remove all the match records for a tournament from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("delete from matches where tournament_id = (%s)", (tournamentId,))
    conn.commit()
    conn.close()


def deletePlayers(tournamentId):
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    # First remove player from the tournament
    c.execute("delete from tournament_players where tournament_id = (%s) returning player_id", (tournamentId,))
    playerIds = c.fetchall()
    # Then, for each of the player removed earlier remove them from the player table
    for p in playerIds:
        c.execute("delete from players where player_id in (%s)", (p[0],))
    conn.commit()
    conn.close()

def countPlayers(tournamentId):
    """Returns the number of players currently registered in a tournament."""
    conn = connect()
    c = conn.cursor()
    c.execute("select count(*) from tournament_players where tournament_id = (%s)", (tournamentId,))
    count = c.fetchone()[0]
    conn.close()
    return count

def registerPlayer(name, tournamentId):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    # First insert the player into the player (check if user already exists ommitted because duplicate names are allowed)
    c.execute("insert into players (name) values (%s) returning player_id", (name,))
    playerId = c.fetchone()[0]
    # Then register the player for the tournament
    c.execute("insert into tournament_players (tournament_id, player_id) values (%s,%s)", (tournamentId, playerId))
    conn.commit()
    conn.close()


def playerStandings(tournamentId):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is curretournament(ntly a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    # For a tournament, fetch the players, ordered by total_wins (desc, because fetchall() revereses the order)
    c.execute("select player_id, name, total_wins, total_matches from tournament_players_view where tournament_id = (%s) order by total_wins desc", (tournamentId,))
    players = c.fetchall() 
    conn.close()
    return players


def reportMatch(winner, loser, tournamentId):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    # First start a match, by inserting a new in matches
    c.execute("insert into matches (tournament_id, player1, player2, winner) values (%s, %s, %s, %s)", (tournamentId, winner, loser, winner))
    # Then update the total_matches and total_wins of winner and loser appropriately
    c.execute("update tournament_players set total_matches = (total_matches + 1) where tournament_id = (%s) and player_id = (%s)", (tournamentId, loser));
    c.execute("update tournament_players set total_matches = (total_matches + 1), total_wins = (total_wins + 1) where tournament_id = (%s) and player_id = (%s)", (tournamentId, winner))
    conn.commit()
    conn.close()

 
def swissPairings(tournamentId):
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    c = conn.cursor()
    # First get the name and id of players ordered by wins
    c.execute("select player_id, name from tournament_players_view where tournament_id = (%s) order by total_matches, total_wins desc", (tournamentId,))
    players = c.fetchall()
    # Then place the data in a list of tuples, pairings
    pairings = []
    prevPlayer = -1 # Keeps track of the previous row fetched
    i = 0
    # Iterate over all entries in players. On every other entry, create a tuple and append it to the list
    while i < len(players): 
        if i % 2 != 0: 
            pairings.append((prevPlayer[0], prevPlayer[1], players[i][0], players[i][1]))
        prevPlayer = players[i] # Finally, update the previous player
        i = i + 1
    conn.close()
    return pairings