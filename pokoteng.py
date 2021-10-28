import os
import requests
import json
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


@client.command()
async def kinshi(ctx):
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
