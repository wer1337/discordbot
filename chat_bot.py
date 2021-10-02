import datetime
from re import S
import discord
from discord.ext import commands
from logging.handlers import RotatingFileHandler
import yaml

APP_CONFIG = None


class DiscordBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.uptime = datetime.datetime.utcnow
        super().__init__(*args, **kwargs)


def bot_init():
    bot = DiscordBot(command_prefix='~', description='Random Bot for Random Fun')

    for cog in APP_CONFIG.get("cogs", []):
        print(cog)
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
        
    bot = bot_init()
    
    # bot.run(APP_CONFIG.get("bot_token"))
    
    # try:
    #     bot.run(APP_CONFIG.get("bot_token"))
    # except Exception as ex:
    #     print(f"Exception occured trying to run. {repr(ex)}")

