import os
import csv
import sys
import discord
from discord.ext import commands
from bot import SERVERS
from functions.textProcessor import textProcessor

class CanalMsgs(commands.Cog):
    def __init__(self, BOT):
        self.BOT = BOT

    @commands.Cog.listener()

    async def on_ready(self):
        print('✔ Modulo CanalMsgs')

    @commands.command(aliases=['cmsg', 'cm', 'gb'])
    async def _CanalMsgs(self, ctx):
        await ctx.channel.trigger_typing()
        for server in SERVERS:
            guild = self.BOT.get_guild(int(server["id"]))
            for canal in server["canales"]:
                
                fName = 'Server_'+str(server["name"])+'_Canal_'+str(canal["name"])+'.csv'
                f = open(os.path.join(os.getcwd() ,fName), 'w', newline='', encoding='utf-8')
                writer = csv.writer(f, delimiter=";")

                fNameGb = 'Server_'+str(server["name"])+'_Canal_'+str(canal["name"])+'gearBot.csv'
                fGb = open(os.path.join(os.getcwd() ,fNameGb), 'w', newline='', encoding='utf-8')
                writerGb = csv.writer(fGb, delimiter=";")
                
                rows = [["id", "autor", "contenido", "fecha"]]
                rowsGb = [["actionId", "actionSource", "actionTarget", "actionAuthor", "actionAction", "actionReason", "actionTime"]]
                canal = guild.get_channel(int(canal["id"]))
                async for msg in canal.history(limit=None):
                    print(str(msg.author))
                    if str(msg.author) == str("GearBot#7326"):
                        content = textProcessor.gearBot_Clean(msg.content)
                        print("content OK")
                        if(content != None):                        
                            print(msg.content)
                            print("Content is not none")
                            rowsGb.append([msg.id, msg.author, content["actionTarget"], content["actionAuthor"], content["actionAction"], content["actionReason"], msg.created_at])
                        print("Content is none")
                    if("<:gearMute:scsc465177981221077003>" not in msg.content):
                        rows.append([msg.id, msg.author ,msg.content, msg.created_at])
                    print("aññadido a rows")
                    
                    
                writer.writerows(rows)
                print("Escribiendo normal")
                f.close()
                print("cerrando normal")

                writerGb.writerows(rowsGb)
                print("escribiendo GB")
                fGb.close()
                print("Cerrado GB")
                #Sending data trught the API
                #Tener credenciales
                #Enviar los datos
                #await ctx.send(file=discord.File(os.path.join(os.getcwd() , fName)))
                await ctx.reply(file=discord.File(os.path.join(os.getcwd() , fNameGb)), mention_author=False)

def setup(BOT):
    BOT.add_cog(CanalMsgs(BOT))
