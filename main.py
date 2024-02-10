import discord
import os
from dis_bot import DisBot

client = discord.Client(intents=discord.Intents.default())
Botyaga = DisBot(317276723555336192)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await Botyaga.handle(message)
    # if message.content.startswith('$hello'):
    #     await message.channel.send(f'{message = }')
    #     await message.channel.send(f'{message.author = }')
    #     await message.channel.send(f'{type(message) = }')
    #     await message.channel.send(f'{type(message.author) = }')

client.run(os.getenv('TOKEN'))