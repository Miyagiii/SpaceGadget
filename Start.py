# Coded by TheSpaceCowboy
# Git: https://www.github.com/thespacecowboy42534
# Date: 19/08/17
# Inspired by:https://github.com/RIP95/kurisu-bot
# all code relating to json was taken from the kurisu bot

# Imports    
import json,os,sys,discord,sqlite3
from discord.ext import commands
from plugins.Helper import Helper
description = """Hello there I am Space Gadget #009 version 0.5.2 pre alpha.
I am a general use bot which can be moved between servers easily and without bot permissions
Here is the list of available commands:
"""
# Creating the bot object
prefixes = commands.when_mentioned_or("s.")
bot = commands.Bot(command_prefix=prefixes, description=description)

# If the json file exists read it
if(not os.path.isfile("config.json")):
    sys.exit("Set up your config.json file first!")
else:
    Helper.readconf(bot)

# When the bot logins in sucessfully it will run on_ready    
@bot.event
async def on_ready():
    bot.conn = sqlite3.connect('users.db')
    Helper.createDB(bot)
    
    print("Intialised Sucessfully :)")
    for x in range((10+len(bot.user.name))*3):print("#",end="")
    print(end="\n")
    print("\tBot Name: {}".format(bot.user.name))
    print("\tBot ID: {}".format(bot.user.id))
    await bot.change_presence(game=discord.Game(name='Type s.help for commands'))
    for x in range((10+len(bot.user.name))*3):print("#",end="")
    print(end="\n")
    print("Loading addons:")    
    Helper.load_plugins(bot)

    for x in range((10+len(bot.user.name))*3):print("#",end="")
    print(end="\n")
    
#Used for deciding whether 
try:   
    if bot.config['type'] == "user":
        bot.run(bot.config['email'], bot.config['password'])
    else:
        bot.run(bot.config['token'])
except:
    sys.exit("Json not properly configured, check login details or token are correct.")




