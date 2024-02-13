import discord
import os
from bot import DisBot
from icecream import ic 
from message_api import Message
from config import *

if DEBUG_MODE:
    intents = discord.Intents(messages=True, guilds=True, message_content=True)
else:
    intents=discord.Intents.default()
client = discord.Client(intents=intents)

Botyaga = DisBot([int(os.getenv('ADMIN_ID_1')), int(os.getenv('ADMIN_ID_0'))])

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if not DEBUG_MODE:
        if isinstance(message.channel, discord.channel.TextChannel):
            return
    message = Message(message)
    await Botyaga.handle(message)

client.run(os.getenv('TOKEN'))