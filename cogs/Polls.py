import discord
from discord.ext import commands
from util.FileIO import import_json

class Polls(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self._title = ""
        self._options = []
        self._author = ""

        
    def parse_message(self, message):
        msg_split = message.split()
        self._title = msg_split[1]
        self._options = msg_split[2:]
        self._emojis_list = import_json("numbers")
        
    
    def format_poll(self):
        reactions_list = []
        
        embed = discord.Embed(
            colour = discord.Colour.red()
        )
        
        embed.set_author(name=f"{self._author}'s poll for {self._title}")
        for count in range(len(self._options)):
            reactions_list.append(self._emojis_list[str(count)])
            embed.add_field(name=f"{self._options[count]}", value =f"{self._emojis_list[str(count)]}", inline=False)
        
        return embed, reactions_list

    @commands.command(name='poll', pass_context= True)
    async def createPoll(self, ctx, poll_title: str):
        self._author = ctx.message.author.display_name
        self.parse_message(ctx.message.clean_content)
        
        formatted_poll, reactions_list = self.format_poll()
        await ctx.send(f"{self._author} has created a poll called {self._title}")
        message = await ctx.send(embed=formatted_poll)
        for reaction in reactions_list:
            await message.add_reaction(reaction)
        
        
def setup(bot):
    bot.add_cog(Polls(bot))