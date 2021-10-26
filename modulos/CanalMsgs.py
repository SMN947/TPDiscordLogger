import os
import csv
import discord
from discord.ext import commands
from bot import SERVERS

class CanalMsgs(commands.Cog):
    def __init__(self, BOT):
        self.BOT = BOT

    @commands.Cog.listener()

    async def on_ready(self):
        print('✔ Modulo CanalMsgs')

    @commands.command(aliases=['cmsg', 'cm'])
    async def _CanalMsgs(self, ctx):
        await ctx.reply("Procesando la generacion de CSVs de los mensages de los canales")
        for server in SERVERS:
            guild = self.BOT.get_guild(int(server["id"]))
            for canal in server["canales"]:
                print("procesando "+canal["name"] + " del servidor "+server["name"])
                fName = 'Server_'+str(server["name"])+'_Canal_'+str(canal["name"])+'.csv'
                print(fName)
                f = open(os.path.join(os.getcwd() ,fName), 'w', newline='', encoding='utf-8')
                writer = csv.writer(f)
                rows = [["id", "autor", "contenido", "fecha"]]
                canal = guild.get_channel(int(canal["id"]))
                async for msg in canal.history(limit=10):
                    rows.append([msg.id, msg.author, msg.content, msg.created_at])

                writer.writerows(rows)
                f.close()
                await ctx.send(file=discord.File(os.path.join(os.getcwd() , fName)))

def setup(BOT):
    BOT.add_cog(CanalMsgs(BOT))
