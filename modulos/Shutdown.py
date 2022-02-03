import os
import csv
import discord
from discord.ext import commands

class Shutdown(commands.Cog):
    def __init__(self, BOT):
        self.BOT = BOT

    @commands.Cog.listener()

    async def on_ready(self):
        print('✔ Modulo Shutdown')

    @commands.command(aliases=['sh', 'shutdown'])
    async def _shutdown(self, ctx):
        
        await ctx.channel.trigger_typing()
        await ctx.reply("Bye bye :)")
        exit()

def setup(BOT):
    BOT.add_cog(Shutdown(BOT))