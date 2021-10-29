import discord
from discord.ext import commands

class Ayuda(commands.Cog):
    def __init__(self, BOT):
        self.BOT = BOT

    @commands.Cog.listener()

    async def on_ready(self):
        print('✔ Modulo Info')

    @commands.command(aliases=['ayuda', 'help', 'h', 'a'])
    async def _help(self, ctx):   
        
        await ctx.channel.trigger_typing()     
        embedvar = discord.Embed(title="TPLogger - Help",description=":nerd: Hello, I am a bot 🤖\nBelow are the available commands:", color=0x00ff00)

        embedvar.add_field(name='*info', value='Shows the bot status', inline=False)
        embedvar.add_field(name='*help', value='Shows this help msg', inline=False)
        embedvar.add_field(name='*gb', value='Sends a CSV with the gearBot actions', inline=False)
        embedvar.add_field(name='*logs', value='Sends a CSV with the server log', inline=False)

        embedvar.set_footer(text="Reporting Team | reportingdiscord@teleperformance.com")

        await ctx.reply(embed=embedvar, mention_author=False)

def setup(BOT):
    BOT.add_cog(Ayuda(BOT))