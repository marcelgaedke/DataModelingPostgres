#Udacity - Data Engineering Nanodegree
##Project 1 - Data Modeling with Postgres

###Objective: Collecting Data on Song Data, Artist Data and User Activity from JSON Files for the Sparkify Music Streaming App. <br>
Creating a Database and Tables for this purpose and loading the collected Data into the appropriate Tables.

For this Project we created 4 Dimension Tables (Users, Songs, Artists and Time) as well as one central Fact Table (Songplays) which references the other tables in this Star Shema. 

The following files are included in this project:

create_tables.py 
----------------
- This file connects to StudentDB on the local Postgres server, creates the new Database sparkifydb and connects to it.
- Then the tables songplay, user, songs, artists and time are created (if they already exist they will be dropped first)

etl.py
-------
- This file implements the ETL (Extract, Transform, Load) Process. It reads the song and log files in JSON Format, converts them to Dataframes and loads the relevant information in the appropriate tables in the database. 

sql_queries.py
---------------
- This file contains all the used SQL Queries for creating tables, inserting data, dropping tables and subqueries for songId and artistId.
- The code in this file is imported in the files above

etl.ipynb
----------
- This is a Jupyter Notebook used for developing the etl.py file. This is used to test the syntax and the correctness of the sql queries

test.ipynb
-----------
- This is another Jupyther Notebook to run after the etl files to check if the tables have been correctly populated



###Steps to run Project in Terminal:
1. python create_tables.py
2. python etl.py