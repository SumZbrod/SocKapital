import discord
import os
from bot import DisBot
from icecream import ic 
from message_api import Message

client = discord.Client(intents=discord.Intents.default())
Botyaga = DisBot(int(os.getenv('ADMIN_ID')))

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    # message = Message(message)
    await Botyaga.handle(message)

client.run(os.getenv('TOKEN'))