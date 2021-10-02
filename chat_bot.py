import datetime
from re import S
import discord
from discord.ext import commands
from logging.handlers import RotatingFileHandler
import yaml
import random
import numpy as np

from util.basic_util import fireball

APP_CONFIG = None
bot = commands.Bot('~')


class DiscordBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.uptime = datetime.datetime.utcnow
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
    
    if dice == 'fireball':
        fb = fireball()
        await ctx.send(f'{author} casts fireball for {fb[0]} + {fb[1]} + {fb[2]} + {fb[3]} + {fb[4]} + {fb[5]} + {fb[6]} + {fb[7]} = {np.sum(fb)} ')

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

@bot.command(name="Commands", pass_context=True)
async def commands_(ctx):
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
        APP_CONFIG = yaml.safe_load(config_file)
    
    try:
        bot.run(APP_CONFIG.get("bot_token"))
    except Exception as ex:
        print(f"Exception occured trying to run. {repr(ex)}")

