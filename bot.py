import asyncio
import csv
import json
import discord
from datetime import datetime
from itertools import cycle
from discord.ext import tasks
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import os

from functions.textProcessor import textProcessor

with open("config.json", 'r') as f:
    CONFIG = json.load(f)

TOKEN = CONFIG["token"]
PREFIX = CONFIG["bot_prefix"]
SERVERS = CONFIG["servers"]
INTENTS = discord.Intents.default()
INTENTS.guilds = True

BOT = commands.Bot(command_prefix=PREFIX, intents=INTENTS)
STATUS = cycle(['Try * help', 'Prefix - *'])


BOT.remove_command("help")


@BOT.event
async def on_ready():
    change_status.start()
    print('Bot is ready')
    print("I am running as: " + str(BOT.user))
    print('Bot is ready to be used')


@BOT.event
async def on_member_update(before, after):
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    channel = BOT.get_channel(903399230503280680)
    print('{} | User {} changes from {} to {} in server {}'.format(
        current_time, before.name, before.status, after.status, before.guild))
    await channel.send('{} | User {} changes from {} to {} in server {}'.format(current_time, before.name, before.status, after.status, before.guild))


@BOT.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        em = discord.Embed(title=f"💔Ese comando no existe",
                           description=f"{ctx.author.mention}, intenta usar *ayuda para conocer la lista de comando disponible", color=ctx.author.color)
        await ctx.reply(embed=em, mention_author=False)


@tasks.loop(seconds=5)
async def change_status():
    await BOT.change_presence(activity=discord.Game(next(STATUS)))

@BOT.command(aliases=['cmsg', 'cm', 'gb'])
async def _CanalMsgs(self, ctx):
    await ctx.channel.trigger_typing()
    for server in SERVERS:
        guild = self.BOT.get_guild(int(server["id"]))
        for canal in server["canales"]:

            fName = 'Server_'+str(server["name"]) + \
                '_Canal_'+str(canal["name"])+'.csv'
            f = open(os.path.join(os.getcwd(), fName),
                     'w', newline='', encoding='utf-8')
            writer = csv.writer(f, delimiter=";")

            fNameGb = 'Server_' + \
                str(server["name"])+'_Canal_'+str(canal["name"])+'gearBot.csv'
            fGb = open(os.path.join(os.getcwd(), fNameGb),
                       'w', newline='', encoding='utf-8')
            writerGb = csv.writer(fGb, delimiter=";")

            rows = [["id", "autor", "contenido", "fecha"]]
            rowsGb = [["actionId", "actionSource", "actionTarget",
                       "actionAuthor", "actionAction", "actionReason", "actionTime"]]
            canal = guild.get_channel(int(canal["id"]))
            async for msg in canal.history(limit=None):
                if str(msg.author) == str("GearBot#7326"):
                    content = textProcessor.gearBot_Clean(msg.content)
                    if(content != None):
                        rowsGb.append([msg.id, msg.author, content["actionTarget"], content["actionAuthor"],
                                      content["actionAction"], content["actionReason"], msg.created_at])
                if("<:gearMute:scsc465177981221077003>" not in msg.content):
                    rows.append(
                        [msg.id, msg.author, msg.content, msg.created_at])

            writer.writerows(rows)
            f.close()

            writerGb.writerows(rowsGb)
            fGb.close()
            # Sending data trught the API
            # Tener credenciales
            # Enviar los datos
            # await ctx.send(file=discord.File(os.path.join(os.getcwd() , fName)))
            await ctx.reply(file=discord.File(os.path.join(os.getcwd(), fNameGb)), mention_author=False)

@BOT.command(aliases=['logs', 'l'])
async def _logs(ctx):
    print("logs called")
    print(ctx)
    # await ctx.channel.trigger_typing()
    await ctx.reply("Procesando la generacion de CSVs de los logs de los servidoes")
    for server in SERVERS:
        f = open(os.path.join(os.getcwd(), 'ServerLog_' +
                    str(server["name"])+'.csv'), 'w', newline='', encoding='utf-8')
        writer = csv.writer(f)
        rows = [["User", "Action", "Target", "Reason"]]
        guild = BOT.get_guild(int(server["id"]))
        async for entry in guild.audit_logs(limit=None):
            rows.append([entry.user, entry.action,
                        entry.target, entry.reason])
        print(guild)

        writer.writerows(rows)
        f.close()
        await ctx.send(file=discord.File(os.path.join(os.getcwd(), 'ServerLog_'+str(server["name"])+'.csv')))



@BOT.command()
async def hello(ctx):
    msg = f'Hi {ctx.author.mention}'
    await ctx.reply(msg, mention_author=False)

@BOT.command()
async def add(ctx, num1: int, num2: int):
    result = num1 + num2
    await ctx.send('{} + {} = {}'.format(num1, num2, result))


async def main():
    async with BOT:
        await BOT.start(TOKEN)

asyncio.run(main())
