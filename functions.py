#!/usr/bin/python3

# Author: Ben Hurricane
# Origin: 12 Nov 19
# db.py
# sqlite specific functions

import sqlite3
# from bot.py import Game

db = 'lumberjacks.db'    # Roster name
conn = sqlite3.connect(db)  # Creates file
c = conn.cursor()   # Sets cursor


# Connect
def create_table(name):
    print(f'Adding {name}')
    c.execute("CREATE TABLE IF NOT EXISTS " + name + """ (
                mid INTEGER PRIMARY KEY,
                name TEXT
                )""")   # Create game table
    conn.commit()   # Commits current action


# Insert
def insert_table(table, key, name):
    c.execute(f"INSERT or IGNORE INTO {table} VALUES ('{key}', '{name}')")
    conn.commit()


# Query
def query(name, key):
    c.execute(f"SELECT * FROM {name} WHERE mid='{key}'")
    print(c.fetchall())


# Create tables
create_table('games')  # Creates table for games
create_table('players')  # Creates table for players
create_table('roster')  # Creates table for players

# insert into tables
insert_table('games', '111', 'ORSU')    # table, key, name
insert_table('players', '1', 'Ben Totten')    # table, key, name
query('games', '111')
query('players', '1')


conn.commit()
conn.close()    # Closes connection
