import discord
class Author:
    def __init__(self, author):
        if isinstance(author, discord.user.User):
            self.id = author.id 
            self.name = author.name 
            self.send = author.send

class Message:
    def __init__(self, message):
        if isinstance(message, discord.message.Message): 
            self.author = Author(message.author)
            self.content = message.content
            self.send = message.channel.send
            