from discord.ext import commands
from util.basic_util import fireball
from numpy import random
import numpy as np


class OutsideWork:
    
    def __init__(self, bot):
        self.bot = bot
        
        
    @commands.group(name="Basic Functions", help="Commands for the basic functions outside of work")
    async def _basicF(self, ctx):
        
        if ctx.invoke_subcommand is None:
            await self.bot.send_help(ctx)


    @_basicF.command(pass_context=True)
    async def roll(self, ctx, dice=None):
        author = ctx.message.author.display_name
        if dice is None:
            await ctx.send(f"{author} has an initiative of {random.randint(1,20)}")
        
        if dice == 'fireball':
            fb = fireball()
            await ctx.send(f'{author} casts fireball for {fb[0]} + {fb[1]} + {fb[2]} + {fb[3]} + {fb[4]} + {fb[5]} + {fb[6]} + {fb[7]} = {np.sum(fb)} ')


    @_basicF.command(pass_context=True)
    async def rps(self, ctx, throw=""):
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
           
            
def setup(bot):
    bot.add_cog(OutsideWork(bot))
    