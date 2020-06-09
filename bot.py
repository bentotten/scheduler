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
from discord.ext import commands
from dotenv import load_dotenv

print(f'Loading...')

# Role ID for later pinging
# TODO read in from file
role = "719841601018658906"

# Data structure
games = {}
players = []

# Week data structure
week = {'mon': {}, 'tue': {}, 'wed': {}, 'thu': {}, 'fri': {}, 'sat': {},
        'sun': {}}

# Hash for time conversions
weekday = {0: 'mon', 1: 'tue', 2: 'wed', 3: 'thu', 4: 'fri', 5: 'sat',
           6: 'sun'}

# for error checking
accepted_days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

# Token Setup
with open('token.txt') as f:
    token = f.readline().strip()
load_dotenv()
bot = commands.Bot(command_prefix='!')


# Join message
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


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
    message = '!Game team kickoff-time away/home: Pings active players and \
        informs them we\'re playing, what time kickoff is, and home/away'
    await ctx.send(message)
    await ctx.send(signature)


# Ping active players & store response to attendance for game
@bot.command(name='Game', help='Ex: ORSU 11:00am Away')
async def Game(ctx, team='', start='', location=''):
    message = ("<@&" + role + "> Roll call!")
    game = ("LUMBERJACKS vs " + team.upper() + " (" + location.capitalize() +
            ") at " + start)
    prompt = ("Can you attend?")
    await ctx.send(message)
    await ctx.send(game)

    msg = await ctx.send(prompt)
    await msg.add_reaction('👍')


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


bot.run(token)
