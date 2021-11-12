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


@client.command(aliases=['add'])
async def _add(ctx, *args):
    msg = " ".join(args[:-1])
    alias = args[-1]
    os.system("SETX {0} {1} /M".format(alias, msg))
    await ctx.send("\"" + msg + "\"" + " can be called using \"hahi (call/recall/say/remember) " + alias + "\".")


@client.command(aliases=['call', 'recall', 'say', 'remember'])
async def _recall(ctx, *args):
    alias = args[0]
    msg = ''
    if os.getenv(alias) is not None:
        msg = os.environ.get(alias)
    if msg == '':
        await ctx.send("No message matching alias \"" + alias + "\" found.")
    else:
        await ctx.send(msg)


@client.command(aliases=['aliases'])
async def _aliases(ctx):
    msg = ''
    for key, value in os.environ.items():
        if key == 'BOT_TOKEN' or key == 'DATABASE_URL' or key == 'SESSION_KEY':
            continue
        msg = msg + key + ' -> ' + value + '\n'
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
