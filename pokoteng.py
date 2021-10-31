import os
import requests
import json
import csv
import discord
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix="hahi ", intents=intents)


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    data = json.loads(response.text)
    quote = data[0]['q'] + " -" + data[0]['a']
    return quote

@client.command(aliases=['add'])
async def _add(ctx, *args):
    msg = " ".join(args[:-1])
    alias = args[-1]
    
    with open('aliases.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='|')
        writer.writerow([alias,msg])
    
    await ctx.send("\"" + msg + "\"" + " can be called using \"hahi (call/recall/say/remember) " + alias + "\".")

@client.command(aliases=['call','recall','say','remember'])
async def _recall(ctx, *args):
    alias = args[0]
    msg = ''
    with open('aliases.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        for row in reader:
            if row[0] == alias:
                msg = row[1]
    if msg == '':
        await ctx.send("No message matching alias \"" + alias + "\" found.")
    else:
        await ctx.send(msg)

@client.command(aliases=['kinshi'])
async def _kinshi(ctx):
    await ctx.send("ehhhhhhh????")


@client.command(aliases=['quote'])
async def _remember(ctx):
    await ctx.send(get_quote())


@client.event
async def on_ready():
    print(f"logged in as {client.user}")


@client.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name='Powder Monkey')
    await member.add_roles(role)
    print("assigned role.")

client.run(os.getenv('BOT_TOKEN'))
