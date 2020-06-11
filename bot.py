#!/usr/bin/python3

# Author: Ben Hurricane
# Origin: 12 Nov 19
# bot.py
# This bot schedules rock climbing events
# Referenced:
# - https://realpython.com/how-to-make-a-discord-bot-python/
# - discordpy.readthedocs.io/en/latest/api.html#discord.User.mention

import json
import math
from datetime import datetime
import discord
from discord.ext import commands
from dotenv import load_dotenv
#  import csv

print(f'Loading...')


#  Data structurs
#  games = {'': {"Confirmed": [], "Not Attending": []}}  # store msg id
#  TODO clean me up
games = {}
keys = []
week = {'mon': {}, 'tue': {}, 'wed': {}, 'thu': {}, 'fri': {}, 'sat': {},
        'sun': {}}
weekday = {0: 'mon', 1: 'tue', 2: 'wed', 3: 'thu', 4: 'fri', 5: 'sat',
           6: 'sun'}  # Hash for time conversions
accepted_days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']  # Error chec

# Bot Setup
bot_id = 'Jack#1847'
bot = commands.Bot(command_prefix='!')
with open('token.txt') as f:
    token = f.readline().strip()  # Read in token from file
with open('role.txt') as f:
    role = f.readline().strip()  # Read in active player role from file
load_dotenv()


# Bot Events
@bot.event  # Connet Message
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    print(discord.__version__)

    #  TODO have read in on start
    #  Read in most recent keys
    #    with open('keys.csv', newline='') as f:
    #        reader = csv.reader(f)
    #        keys = list(reader)


@bot.event  # Join Message
async def on_member_join(user):
    channel = bot.get_channel(718602289098784792)
    msg = 'Welcome to the Team {user.display_name}!'
    await channel.send(msg)


@bot.event  # Triggers on reaction to game message
async def on_reaction_add(reaction, user):
    keys = []
    name = user.display_name
    msg = ('(Optional) Reason for decline:')
    msg_id = reaction.message.id

    # Read in keys  TODO Read on boot instead
    with open('keys.csv', 'r') as f:
        keys = f.read().split(',')
    if msg_id not in keys and str(user) != bot_id:
        with open('roster.json', 'r') as f:  # Read in roster
            games = json.load(f)
        if reaction.emoji == '\u2705':
            games[msg_id]['Confirmed'] = name
            with open('roster.json', 'a+') as f:
                json.dump(games, f)
        elif reaction.emoji == '\u274C':
            await user.send(msg)  # Prompts for reason for decline
            # TODO Store reply as save in games{}
            games[msg_id]['Not Attending'] = name
            with open('roster.json', 'a+') as f:
                json.dump(name, f)


# Bot Commands
# Ping
@bot.command(name='ping')
async def ping(ctx):
    # Attempt to ping user
    msg = ctx.author.mention + ' pong!'
    await ctx.send(msg)


# Help Command
@bot.command(name='commands', help="List of commands")
async def help(ctx):
    signature = '[Bot made by Ben Hurricane 2020]'
    message = '!Game team kickoff-time away/home: Pings active players and'
    + 'informs them we\'re playing, what time kickoff is, and home/away\n'
    + '!roster displays roster for last made game'
    await ctx.send(message)
    await ctx.send(signature)


# Game command: Ping active players & store response to attendance for game
@bot.command(name='g', help='Ex: !game ORSU 11:00am Away')
async def game(ctx, team='', start='', location=''):
    # Ping active players
    keys = []
    message = (f"<@&{role}>")
    game = (f"LUMBERJACKS vs {team.upper()} ({location.capitalize()}) {start}")
    prompt = ("Can you attend?")
    await ctx.send(message)
    await ctx.send(game)
    msg = await ctx.send(prompt)

    # TODO maybe write to different files but read into same dict
    # Read in most recent keys TODO potentiall duplicate
    await ctx.send('Attempting to open keys.csv')
    with open('keys.txt', 'r') as f:
        keys = f.read().strip().split(',')
    await ctx.send(f'Keys read in: {keys}')

    # Save to data structure
    if msg.id not in keys:
        keys.append(msg.id)
        games[msg.id] = {msg.id: {"Confirmed": [], "Not Attending": []}}
        await ctx.send(f'ID: {msg.id} --- Appended Keys: {keys}')

        with open('roster.json', 'w+') as f:
            json.dump(games, f)
        with open('keys.csv', mode='w+') as f:
            for line in keys:
                f.write("%s," % line)

    # Trigger initial reacts
    await msg.add_reaction('\u2705')  # Green check for yes
    await msg.add_reaction('\u274C')  # Red X for no


@bot.command(name='roster', help='Ex: !roster')
async def roster(ctx):
    with open('roster.json', 'r') as roster.json:
        data = json.load(roster.json)

    await ctx.send(f'Raw: {data}')


# !Now command
@bot.command(name='now', help='pings climbers available in the next hour')
async def now(ctx):
    # Get and process current time
    date = datetime.now()
    today = weekday[datetime.today().weekday()]
    hour = date.hour+1

    # Pull and process
    to_ping = week.get(today, {}).get(hour, "None")

    await ctx.send("Climbers free at " + str(hour) + ":00" + ":")
    await ctx.send(to_ping)


# Scheduler command
@bot.command(name='schedule', help='Inputs your availability. Ex: mon 0700 to \
             2100')
async def schedule(ctx, day='n/a', start='n/a', filler='n/a', stop='n/a'):
    message = ("Attempting to schedule " + day.capitalize() + " " + start +
               " to " + stop)
    await ctx.send(message)

    try:
        # Processes inputs
        user = ctx.author.mention
        day = day.lower()
        start = int(start)
        start = math.floor(float(start) / 100)
        stop = int(stop)
        stop = math.ceil(float(stop) / 100)

        # Error check inputs
        check = sched_error_check(ctx, day, start, stop)

        if check != 'pass':
            await ctx.send(check)

        # checks if time exists
        for i in range(start, stop):
            if i in week.get(day):
                print(str(i) + "exists")
            else:
                week[day].update({i: []})

            # checks if user is already scheduled
            if user in week.get(day, {}).get(user, 'n/a'):
                print(user + ' already scheduled at ' + day + ' ' + i)
            else:
                week[day][i].append(user)

        print(week)

        # Save to json
        with open('data.json', 'w') as fp:
            json.dump(week, fp)

    except ValueError:
        message = "Error. Please enter a valid input. Ex: !schedule Mon 1300 \
            to 1700"
        await ctx.send(message)

    else:
        message = "Success!"
        await ctx.send(message)


# Show all scheduled
@bot.command(name='all', help='Error checking, prints entire week on terminal')
async def all(ctx):
    print(week)


# Error checks the input times for schedule
def sched_error_check(ctx, day, start, stop):
    if day in accepted_days:
        print("Day check pass")
    else:
        return "Please enter three letter day"
    if start in range(0, 24):
        print("Start check pass")
    else:
        return "Please enter a valid 24h time"
    # 2330 will round up to 24 aka 0000, so range must be 0-25
    if stop in range(0, 25):
        print("Stop check pass")
    else:
        return "Please enter a valid 24h time"

    return "pass"


# Shutdown bot
@bot.command(name='sleep', help='Shutsdown bot')
@commands.has_permissions(administrator=True)
async def close(ctx):
    await bot.close()
    print("Shutwdown Complete")


bot.run(token)  # Launch bot
