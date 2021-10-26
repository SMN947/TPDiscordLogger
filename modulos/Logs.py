import os
import csv
import discord
from discord.ext import commands
from bot import SERVERS

class Ayuda(commands.Cog):
    def __init__(self, BOT):
        self.BOT = BOT

    @commands.Cog.listener()

    async def on_ready(self):
        print('✔ Modulo Logs')

    @commands.command(aliases=['logs', 'l'])
    async def _logs(self, ctx):
        await ctx.reply("Procesando la generacion de CSVs de los logs de los servidoes")
        for server in SERVERS:
            print(server)
            print(server["name"])
            print(server)
            f = open(os.path.join(os.getcwd() ,'ServerLog_'+str(server["name"])+'.csv'), 'w', newline='', encoding='utf-8')
            writer = csv.writer(f)
            rows = [["User", "Action", "Target", "Reason"]]
            guild = self.BOT.get_guild(int(server["id"]))
            async for entry in guild.audit_logs(limit=None):
                rows.append([entry.user, entry.action, entry.target, entry.reason])

            writer.writerows(rows)
            f.close()
            await ctx.send(file=discord.File(os.path.join(os.getcwd() ,'ServerLog_'+str(server["name"])+'.csv')))

def setup(BOT):
    BOT.add_cog(Ayuda(BOT))
