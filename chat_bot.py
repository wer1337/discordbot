import asyncio
import datetime
from re import S
import discord
from discord.ext import commands
import logging
from logging.handlers import RotatingFileHandler
import sys
import os
import yaml
import random

APP_CONFIG = None
bot = commands.Bot('~')

### Move these func to utils

def fireball():
    fireball_arr = []
    sum_ = 0
    for i in range(8):
        rand_num =  random.randint(1, 6)
        fireball_arr.apppend(rand_num)
        sum_ += rand_num

    fireball_arr.append(sum_)

    return fireball_arr

class DiscordBot():
    def __init__(self, *args, **kwargs) -> None:
        self,uptime = datetime.datetime.utcnow
        super().__init__(*args, **kwargs)


def bot_init():
    bot = DiscordBot()

    for cog in APP_CONFIG.get("cogs", []):
        try:
            bot.load_extension(cog)
        except Exception:
            print(f"Failed to load in cog: {cog}")

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=APP_CONFIG.get("bot_presence")))
    print("The bot has started successfully")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")

@bot.command(pass_context=True)
async def roll(ctx, dice=None):
    author = ctx.message.author.display_name
    if dice is None:
        await ctx.send(f"{author} has an initiative of {random.randint(1,20)}")

@bot.command(pass_context=True)
async def rps(ctx, throw=""):
    rps = {
        "rock" : "paper",
        "paper" : "scissors",
        "scissors" : "rock"
    }

    if throw is None or throw.lower() not in rps:
        await ctx.send('Please throw a valid option')
        return
    
    switch = random.randrange(2)

    if switch is 1:
        await ctx.send(f"Your {throw} beats xfsunbo's {rps[throw.lower()]}. :partying_face:")
    else:
        await ctx.send(f"Your {throw} ties with xfsunbo's {throw}. :face_with_raised_eyebrow:")

@bot.command(pass_context=True)
async def commands(ctx):
    embed = discord.Embed(
        colour = discord.Colour.red()
    )

    embed.set_author(name="Commands")
    embed.add_field(name="~Hello", value = "Says hello back", inline = False)
    embed.add_field(name="~roll <option>", value = "Rolls for initiative if blank, options = [fireball]", inline = False)
    embed.add_field(name="~rps <rps>", value = "Play rps against xfsunbo, options = [rock, paper, scissors]", inline = False)

    await ctx.send(embed=embed)

if __name__ == '__main__':
    with open("app_config.yml", "r") as config_file:
        APPP_CONFIG = yaml.safe_load(config_file)
    
    try:
        bot.run(APP_CONFIG.get("bot_token"))
    except Exception as ex:
        print(f"Exception occured trying to run. {repr(ex)}")

