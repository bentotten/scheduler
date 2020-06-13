#!/usr/bin/python3

# Author: Ben Hurricane
# Origin: 12 Nov 19
# db.py
# sqlite specific functions

import sqlite3
from bot.py import Game

db = 'roster.db'    # Roster name
table_name = 'games'
conn = sqlite3.connect(db)  # Creates file
c = conn.cursor()   # Sets cursor


# Connect
def create_table():

    c.execute(f"""CREATE TABLE [IF NOT EXISTS] {table_name} (
                id INTEGER NOT NULL PRIMARY KEY,
                confirmed ,
                not_attending text
                )""")   # Create game table

    conn.commit()   # Commits current action

    conn.close()    # Closes connection


# Insert
def insert_table(key):
    c.execute(f"INSERT INTO {table_name} VALUES ({key}, 'Justin Wood', 'John Smith')")
    conn.commit()


# Query
def query_games(key):
    c.execute(f"SELECT * FROM games WHERE id='{key}'")
    print(c.fetchall())


# create_table()  # Creates table
# insert_table('111')
query_games('111')
