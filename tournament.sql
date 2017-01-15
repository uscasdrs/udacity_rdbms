-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament

-- Next, create the tables
CREATE TABLE players (
   name	text,
   id	serial primary key
);


CREATE TABLE matches (
   winner integer references players(id),
   loser  integer references players(id),
   id 	  serial primary key
);

-- Now we create some views
-- This view returns the number of wins for each player who has played at least one match
create view win_count as
	select winner, count(winner) as cw
	from matches
	group by winner;
	
-- This view returns the number of losses for each player who has played at least one match
create view loss_count as
	select loser, count(loser) as cl
	from matches
	group by loser;
	
-- This view creates a table of wins for all players that have registered
-- A player need not have played any games.
create view full_win_count as
	select players.id as id, players.name as name, win_count.cw as cw
	from players left join win_count
	on win_count.winner = players.id;

-- This view creates a table of wins and losses for all players that have registered.
-- If a player has not played any matches so far, the win and loss counts for this player will be zero.
create view full_win_loss_count as
    select full_win_count.id as id,
		   full_win_count.name as name,
	       COALESCE(full_win_count.cw,0) as cw,
		   COALESCE(loss_count.cl,0) as cl
    from full_win_count left join loss_count
    on full_win_count.id = loss_count.loser;

