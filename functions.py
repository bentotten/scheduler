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


def scrub(table_name):
    return ''.join(chr for chr in table_name if chr.isalnum())


# Connect
def create_table(table_name):
    name = scrub(table_name)  # scrub for injections
    if name != 'roster':
        c.execute("CREATE TABLE IF NOT EXISTS " + name + """ (
                    mid INTEGER PRIMARY KEY,
                    name TEXT
                    )""")   # Create game table
    elif name == 'roster':
        c.execute("""CREATE TABLE IF NOT EXISTS roster (
                    mid INTEGER PRIMARY KEY,
                    uid INTEGER,
                    attending INTEGER
                    )""")   # Create game table
    conn.commit()   # Commits current action


# Insert
def insert_table(table_name, key, name):
    table = scrub(table_name)  # scrub for injections
    c.execute("INSERT or IGNORE INTO " + table + " VALUES (?, ?)",
              (key, '{name}'))
    conn.commit()


# Query
def query(table_name, key):
    table = scrub(table_name)  # scrub for injections
    c.execute("SELECT * FROM " + table + " WHERE mid=?", ('{key}',))
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
