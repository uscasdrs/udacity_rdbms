#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute( 'delete from matches;' )
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute( 'delete from players;' )
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cur = conn.cursor()
    cur.execute('select count(*) from players;')
    rows = cur.fetchall()
    conn.close()
    return rows[0][0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute ('insert into players values(%s);', (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute('''
    create view win_count as
             select winner, count(winner) as cw 
               from matches 
              group by winner
    ''')

    cur.execute('''
    create view loss_count as
             select loser, count(loser) as cl 
               from matches 
              group by loser
    ''')

    cur.execute('''
    create view win_loss_count as
             select win_count.winner, win_count.cw, loss_count.loser, loss_count.cl
               from win_count full outer join loss_count 
                 on win_count.winner = loss_count.loser;
    ''')

    cur.execute('''
    create view full_win_count as
             select players.id, players.name, win_count.cw
               from players left join win_count 
                 on win_count.winner = players.id;
    ''')

    cur.execute('''
    create view full_win_loss_count as
             select full_win_count.id, full_win_count.name, full_win_count.cw, loss_count.cl
               from full_win_count left join loss_count 
                 on full_win_count.id = loss_count.loser;
    ''')

    cur.execute("select id, name, COALESCE(cw,0), COALESCE(cw,0)+COALESCE(cl,0) from full_win_loss_count order by cw desc")
    rows = cur.fetchall()
    conn.close()
    return rows


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute ('insert into matches values(%s, %s);', (winner,loser))
    conn.commit()
    conn.close()
 
def swissPairings():
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
    st = playerStandings()
    res = []
    for i in range(0, len(st), 2):
       res.append((st[i][0], st[i][1], st[i+1][0], st[i+1][1]))
    print res
    return res
