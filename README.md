# udacity_rdbms
Created in 2017 January 15
The files in the repository constitute the submission to the final project 
("Running a Swiss-style tournament") for the Udacity course "Introduction to 
Relational Database Management"

This has been tested with postgreSQL server.

There are three files in the repository.

tournament.sql contains SQL commands that must be executed the first time. It can
also be executed when we need to start with a new, empty database. The commands in
this file are commands to psql.

tournament.py contains python functions that interface with the database. Description
of each function can be found in this file.

tournament_test.sql contains python code to test the database. It also serves an example
of how the functions in tournament.py can be used. The following shows how the code can
be used. '$ ' is the shell prompt and '=> ' is the psql prompt.

$ psql
=> \i tournament.sql
[...]
=> \q
$


$ python tournament_test.sql
