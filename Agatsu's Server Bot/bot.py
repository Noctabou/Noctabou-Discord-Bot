#DiscordBot
import cmd
import discord
from discord.ext import commands
import asyncio
import random
import os
import sys
import time
import libtmux
import subprocess

#fonctions
#Donne le nombre de joueurs connectés au serveur et vérifie si le serveur est en ligne
def MCServerPlaying():
    timestop=300
    os.system("tmux send-keys -t MCServer 'list' Enter")
    for i in range(timestop):
        time.sleep(0.1)
        #while the first character of the line is '>'
        output=subprocess.check_output(["tmux", "capture-pane", "-J", "-p", "-t", "MCServer"])
        output=output.decode("utf-8")
        output=output.split("\n")
        lastline=output[-1] #last line
        while lastline.startswith('>') or lastline.startswith(' ') or lastline=='':
            lastline=output.pop()
        if "INFO]: There are " in lastline:
            #print("Réponse trouvée")
            break
        if i == timestop/2:
            os.system("tmux send-keys -t MCServer 'list' Enter")
        if i == timestop-1:
            return "503"
    lastline = lastline.split("There are ").pop().split(" of a max of ")
    if len(lastline[1].split(" players online: ")) == 2:
        output = [lastline[0], lastline[1].split(" players online: ")[0], lastline[1].split(" players online: ")[1]]  # [nb joueurs, nb max joueurs, liste joueurs]
    else:
        output = [lastline[0], lastline[1].split(" players online:")[0], ""]
    return output   

#Variables
import configparser
config = configparser.RawConfigParser()
config.read('bot.properties')
details_dict = dict(config.items('AgatsuBot'))
token = (None, details_dict['token'])[details_dict['token'] != '']
MCpath = (None, details_dict['mcpath'])[details_dict['mcpath'] != '']
owners = (None, details_dict['owners'])[details_dict['owners'] != '']
MCmanagers = (owners, details_dict['mcmanagers'])[details_dict['mcmanagers'] != '']

#Ouvre une session tmux où le serveur est lancé
server = libtmux.Server()
os.system("tmux new-session -n MC -s MCServer")
session = server.sessions.get(session_name="MCServer")
window = session.attached_window
pane = window.attached_pane

#Liste des serveurs Minecraft dans le dossier séléctionné
listservers=os.listdir(MCpath)
if len(listservers) == 0:
    print("Aucun serveur trouvé dans le dossier "+MCpath)
    serveurMC=None
else:
    serveurMC=listservers[0]
running=False

#bot
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(intents=intents, case_insensitive=False,allowed_mentions=discord.AllowedMentions(everyone=False))
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
    """This Event Gets Triggered When A Message Is Received!"""
    if message.author.bot:
        return
    if message.content.startswith("Hello"):
        await message.channel.send("Hello!")
    await client.process_commands(message)

@client.slash_command()
async def printvar(ctx):
    await ctx.respond("MCpath: "+MCpath+"\n owners: "+owners+"\n MCmanagers: "+MCmanagers+"\n serveurMC: "+serveurMC+"\n running: "+str(running)+"\n Liste des serveurs: "+str(listservers))

mccommands=client.create_group(name="mc", description="Commandes Minecraft")
@mccommands.command(name="start", description="Démarrer le serveur")
async def start(ctx):
    global running, serveurMC
    if running:
        await ctx.respond("Un serveur est déjà lancé.")
        return
    if ctx.author.id in MCmanagers:
        # Vérifie que le serveur lancé avant a fini de sauvegarder
        if pane.capture_pane().pop()[-1:] != "$":
            await ctx.respond("Le serveur est en cours de sauvegarde.")
            return
        os.system("tmux send-keys -t MCServer 'cd /home/agatsu/MCServers/"+serveurMC+"/' Enter")  # va dans le dossier du serveur
        # lance le serveur
        os.system("tmux send-keys -t MCServer './start' Enter")
        await ctx.respond("Démarrage du serveur MC "+serveurMC+" !")
        running = True
    else:
        await ctx.respond("Commande réservée aux modérateurs du serveur.")


client.run(token, reconnect=True)