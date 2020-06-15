#!/usr/bin/python3

# Author: Ben Hurricane
# Origin: 12 Nov 19
# db.py
# sqlite specific functions

import sqlite3
# from bot.py import Game

db = 'lumberjacks.db'    # Roster name
# conn = sqlite3.connect(db)  # Creates file
conn = sqlite3.connect(':memory:')  # Creates file
c = conn.cursor()   # Sets cursor


def scrub(table_name):
    return ''.join(chr for chr in table_name if chr.isalnum())


# Connect
# TODO someday update to take a list of columns and loop through
def create_table(table_name):
    name = scrub(table_name)  # scrub for injections
    if name != 'roster':
        c.execute("CREATE TABLE IF NOT EXISTS " + name + """ (
                    mid INTEGER NOT NULL,
                    name TEXT
                    )""")   # Create game table
    elif name == 'roster':
        c.execute("""CREATE TABLE IF NOT EXISTS roster (
                    mid INTEGER NOT NULL,
                    uid INTEGER NOT NULL,
                    attending INTEGER NOT NULL
                    )""")   # Create game table
    conn.commit()   # Commits current action


def drop_table(table_name):
    table = scrub(table_name)
    c.execute("DROP table if exists " + table)
    conn.commmit()


# Show all tables
def show_tables():
    c.execute("SELECT name from sqlite_master where type='table'")
    return (c.fetchall())


# Show all data
def show_data():
    tables = show_tables()
    rows = []
    i = 0
    for row in tables:
        x = scrub(row)
        c.execute("SELECT * FROM " + x)
        rows.insert(i, c.fetchall())
    return rows


# Basic Primary Table functions
def insert(table_name, key, value):
    table = scrub(table_name)  # scrub for injections
    c.execute("INSERT or IGNORE INTO " + table + " VALUES (?, ?)",
              (key, value))
    conn.commit()


# Query
def query(table_name, key):
    table = scrub(table_name)  # scrub for injections
    c.execute("SELECT * FROM " + table + " WHERE mid=?", (key,))
    return (c.fetchall())


# Update
def update_games(key, value):
    c.execute("""UPDATE games SET name = ?
              WHERE mid = ?""", (value, key))
    conn.commit()


def update_players(key, value):
    c.execute("""UPDATE players SET name = ?
              WHERE mid = ?""", (value, key))
    conn.commit()


# Remove
def remove(table_name, key):
    table = scrub(table_name)  # scrub for injections
    c.execute("DELETE FROM " + table + " WHERE mid = ?", (key,))
    conn.commit()


# Inserting into the roster
def insert_roster(mid, uid, flag):
    # Check if already recorded, if so update record
    c.execute("""SELECT mid, uid FROM roster WHERE EXISTS (
        SELECT * FROM roster WHERE mid = ? AND uid = ?)""", (mid, uid))
    exists = c.fetchone()

    if str(exists) == 'None':
        c.execute("INSERT or IGNORE INTO roster VALUES (?, ?, ?)",
                  (mid, uid, flag))
    else:
        c.execute("""UPDATE roster SET attending = ?
                  WHERE (mid = ? AND uid = ?)""", (flag, mid, uid))

    conn.commit()


# Compile Roster
def compile_roster_by_mid(mid):
    


# Create tables
create_table('games')  # Creates table for games
create_table('players')  # Creates table for players
create_table('roster')  # Creates table for players

# Test Commands
insert('games', '111', 'ORSU')    # table, key, name
insert('players', '1', 'Ben Totten')    # table, key, name
insert('games', '112', 'Pigs')    # table, key, name
insert('players', '2', 'Justin Wood')    # table, key, name
insert('games', '113', 'Seattle Quake')    # table, key, name
insert('players', '3', 'John Smith')    # table, key, name
insert_roster('111', '1', '1')    # table, key, name
insert_roster('111', '1', '0')    # table, key, name
insert_roster('111', '2', '1')    # table, key, name
insert_roster('112', '1', '1')    # table, key, name
print(show_tables())
print(show_data())


conn.commit()
conn.close()    # Closes connection
