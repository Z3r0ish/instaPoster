from instapy import InstaPy
from datetime import datetime, timedelta
from random import *
import os, random, time
from config import *
import discord
from discord.ext import commands
import json

posting = True
i = 0

#
# functions to parse the json file, I'm not going to comment all of them
#

def getPrefix(client, message):
    with open(jsonPath, 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

def getPath():
    with open(jsonPath, 'r') as f:
        path = json.load(f)
    return path['ath-' + user]

def getEngagementRate():
    with open(jsonPath, 'r') as f:
        path = json.load(f)
    return path['minEngagementRate-' + user]

def getAge():
    with open(jsonPath, 'r') as f:
        path = json.load(f)
    return path['minAge-' + user]

def getTimeout():
    with open(jsonPath, 'r') as f:
        path = json.load(f)
    return path['timeout-' + user]

# log into the client
client = discord.Client()

# sets the prefix
client = commands.Bot(command_prefix=getPrefix)

# when the bot is logged in print it in the terminal


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

session = InstaPy(username=user, password=passwd)

@client.command(aliases=[user])
async def posting(ctx, *args):
    # if there are no args tell the user to specify what he wants
    if len(args) == 0:
        await ctx.send('Please specify what you want to do')

    # change the path
    elif args[0].lower() == "path":
        with open(jsonPath, 'r') as f:
            path = json.load(f)
     
        path[str("path-" + user)] = args[1]

        with open(jsonPath, 'w') as f:
            json.dump(path, f, indent=4)
        await ctx.send('Set filepath to ' + args[1])

    elif args[0].lower() == "engagementrate":
        with open(jsonPath, 'r') as f:
            minEngagementRate = json.load(f)
     
        minEngagementRate[str("minEngagementRate-" + user)] = int(args[1])

        with open(jsonPath, 'w') as f:
            json.dump(minEngagementRate, f, indent=4)
        await ctx.send('Set engagement rate to be at least ' + args[1])

    elif args[0].lower() == "age":
        with open(jsonPath, 'r') as f:
            minAge = json.load(f)
     
        minAge[str("minAge-" + user)] = args[1]

        with open(jsonPath, 'w') as f:
            json.dump(minAge, f, indent=4)
        await ctx.send('Set age to be at least ' + args[1])
    
    elif args[0].lower() == "timeout":
        with open(jsonPath, 'r') as f:
            timeout = json.load(f)
     
        timeout[str("timeout-" + user)] = args[1]

        with open(jsonPath, 'w') as f:
            json.dump(timeout, f, indent=4)
        await ctx.send('Set timeout to be ' + args[1] + ' seconds')

    elif args[0].lower() == "unfollow":
        # logs into instagram
        bot = Bot() 
        bot.login(username = user, password = passwd)
        bot.unfollow_per_run(int(args[1]))
        await ctx.send('Set filepath to ' + args[1])

    elif args[0].lower() == "follow":
        session.follow_by_tags([args[2]], amount=int(args[1]), skip_top_posts=False)
        await ctx.send('Set filepath to ' + args[1])

# immport the token
client.run(token)