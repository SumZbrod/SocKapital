import discord
from config import *
from icecream import ic

class Author:
    def __init__(self, author, message=None):
        if isinstance(author, (discord.user.User, discord.member.Member)):
            self.id = author.id 
            if DEBUG_MODE:
                self.name = f"{author.name}_{message.channel.name}" 
                self.send = message.channel.send 
            else:
                self.name = author.name 
                self.send = author.send 

class Channel:
    def __init__(self, channel):
        if isinstance(channel, (discord.channel.DMChannel, discord.channel.TextChannel)):
            self.send = channel.send


class Message:
    def __init__(self, message):

        if isinstance(message, discord.message.Message): 
            if DEBUG_MODE:
                self.author = Author(message.author, message)
            else:
                self.author = Author(message.author)

            self.channel = Channel(message.channel)
            self.content = message.content