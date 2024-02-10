import discord
import os
from dis_bot import DisBot

client = discord.Client(intents=discord.Intents.default())
Botyaga = DisBot(os.getenv('ADMIN_ID'))

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await Botyaga.handle(message)

client.run(os.getenv('TOKEN'))