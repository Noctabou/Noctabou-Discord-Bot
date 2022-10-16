import discord
import random
from discord.ext import commands
import os

intents = discord.Intents.default()
client = commands.Bot(command_prefix='&', intents=intents, case_insensitive=False, allowed_mentions=discord.AllowedMentions(everyone=False))

@client.event
async def on_ready():
    """This Event Gets Triggered When The Bot Successfully Connects To The Internet!"""
    print("The Bot Is Now Ready To Run!")
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author.id == client.user.id:
        return
    # si le message est une commande
    if message.content.startswith('&'):
        await client.process_commands(message)
        return

@client.command()
async def startServer(ctx):
    os.system("mcServer.sh")


client.run('TOKEN')   
