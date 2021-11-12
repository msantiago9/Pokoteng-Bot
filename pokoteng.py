import os
import requests
import json
import discord
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData

load_dotenv(find_dotenv())
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix="hahi ", intents=intents)

db_url = os.getenv("DATABASE_URL")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
engine = create_engine(db_url, echo=True)

meta = MetaData()

aliases = Table(
    'aliases', meta,
    Column('id', Integer, primary_key=True),
    Column('input', String),
    Column('output', String),
)

meta.create_all(engine)


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    data = json.loads(response.text)
    quote = data[0]['q'] + " -" + data[0]['a']
    return quote


@client.command(aliases=['add'])
async def _add(ctx, *args):
    msg = " ".join(args[:-1])
    alias = args[-1]
    ins = aliases.insert().values(input=alias, output=msg)
    s = aliases.select()

    connect = engine.connect()
    results = connect.execute(s)
    exists = False
    for result in results:
        if result[1] == alias:
            await ctx.send("alias already exists.")
            exists = True

    if not exists:
        result = connect.execute(ins)
        await ctx.send("\"" + msg + "\"" + " can be called using \"hahi (call/recall/say/remember) " + alias + "\".")


@client.command(aliases=['drop'])
async def _drop(ctx, key):
    if key == os.getenv('DELETE_TABLE_KEY'):
        meta.drop_all(bind=engine, tables=[aliases.__table__])


@client.command(aliases=['call', 'recall', 'say', 'remember'])
async def _recall(ctx, *args):
    alias = args[0]
    msg = ''
    s = aliases.select()
    connect = engine.connect()
    results = connect.execute(s)
    for result in results:
        if result[1] == alias:
            msg = result[2]
    if msg == '':
        await ctx.send("No message matching alias \"" + alias + "\" found.")
    else:
        await ctx.send(msg)


@client.command(aliases=['aliases'])
async def _aliases(ctx):
    msg = '```'
    s = aliases.select()
    connect = engine.connect()
    results = connect.execute(s)
    for result in results:
        msg = msg + str(result) + '\n'
    msg = msg + '```'
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
