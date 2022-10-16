from cProfile import run
import os
import random
import shutil
import subprocess
import time
import asyncio
from asyncio import TimeoutError, sleep
from multiprocessing import Process

import discord
import requests
import tweepy as tw
from discord.ext import commands, tasks
from discord.ui import Button, View

"""VARIABLES##############################################################################################################################################################"""
global actif
server = False
nocta = 317596360775958538
actif= True
token=None
# Fonctions
if os.getlogin()=="noctabou":
    server = True
def get_type_from_url(url):
    idtweet = url.split("/").pop()[0:19]
    client = tw.Client("AAAAAAAAAAAAAAAAAAAAAGyRZwEAAAAAiAjOI77d5GB6uy074Kf8D3GnfaY%3D5ndbu0KjfWRXCJpu6kr4nhJLYljjfKE9QqUl8P3JbgsIxB72dV")
    tweet = client.get_tweet(id=idtweet, expansions="attachments.media_keys", media_fields="type")
    if "media" in tweet.includes:
        type = tweet.includes["media"][0].type
    else:
        type = "text"
    #print("Le tweet contient "+type)
    return type


# Bot Discord
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(intents=intents, case_insensitive=False,
                      allowed_mentions=discord.AllowedMentions(everyone=False))
#debug_guilds=[948862079572533269]

"""COMMANDES##############################################################################################################################################################"""
@client.event
async def on_ready():
    """This Event Gets Triggered When The Bot Successfully Connects To The Internet!"""
    print("The Bot Is Now Ready To Run!")
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    global server
    if server:
        statusMCupdate.start()
    else:
        await client.change_presence(activity=discord.Game(name="Le bot n'est pas lancé sur serveur. Fonctions limitées."))

@client.event
async def on_message(message):
    """This Event Gets Triggered When A Message Is Received!"""
    global serveurMC
    # we do not want the bot to reply to itself
    if message.author.id == client.user.id:
        return
    # si le message est une commande
    lowermessage = message.content.split(" ")[0].lower()
    if "https://media.discordapp.net/" in message.content:
        nmessage = message.content
        nmessage = nmessage.replace(
            "media.discordapp.net", "cdn.discordapp.com")
        user = str(message.author.display_name)
        await message.delete()
        await message.channel.send("**"+user+"** *a dit:* \n"+nmessage)
    elif "https://twitter.com/" in message.content:
        nmessage = message.content
        chunks = str(nmessage).split(" ")
        for c in chunks:
            if "https://twitter.com/" in c:
                link = c
        tweetType = get_type_from_url(link)
        if tweetType == "video":
            if str(message.author.nick)=="None": 
                user=str(message.author.name)
            else: 
                user=str(message.author.nick)
            nmessage=nmessage.replace("https://","https://vx")
            await message.delete()
            await message.channel.send("**"+user+"** *a partagé:* \n"+nmessage)
            await message.channel.last_message.add_reaction("▶")
        elif tweetType == "photo":
            await message.add_reaction("🖼")
        elif tweetType == "text":
            await message.add_reaction("📝")

@client.slash_command(description="Renvoie l'image de l'utilisateur mentionné.")
async def pp(ctx, member: discord.Member = None):
    if member == None:
        mec = ctx.author
    else:
        mec = member
    await ctx.respond(mec.avatar)

@client.slash_command(description="Renvoit les informations de l'utilisateur mentionné.")
async def userinfo(ctx, member: discord.Member = None):
    if member == None:
        mec = ctx.author
    else:
        mec = member
    embed = discord.Embed(title="Informations sur " +str(mec.name), description="", color=0x00ff00)
    embed.add_field(name="Nom", value=mec.name, inline=True)
    embed.add_field(name="ID", value=mec.id, inline=True)
    embed.add_field(name="Plus haut Role", value=mec.top_role)
    embed.add_field(name="A rejoint le", value=mec.joined_at)
    embed.add_field(name="Création compte", value=mec.created_at)
    embed.set_thumbnail(url=mec.avatar)
    await ctx.respond(embed=embed)

@client.slash_command(description="Fonction débile qui coupe la première lettre de chaque mot.")
async def rançais(ctx, *, args=None):
    words = args.split(" ")
    nmessage = ""
    for word in words:
        word = word[1:len(word)]
        nmessage = nmessage+word+" "
    await ctx.respond(ctx.author.name+": "+nmessage)

@client.slash_command(description="Fonction débile qui transforme en émoji la première lettre de chaque mot.")
async def lettermoji(ctx, *, args=None):
    words = args.split(" ")
    nmessage = ""
    for word in words:
        if word[0].lower() in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]:
            word = ":regional_indicator_"+word[0].lower()+":"+word[1:len(word)]
        nmessage = nmessage+word+" "
    await ctx.respond(ctx.author.name+": "+nmessage)

@client.slash_command(description="Pong!")
async def ping(ctx):
    await ctx.respond(f"Pong! Latency is {client.latency}")

@client.slash_command(description="/delete <nombre messages> {user mention}")
@commands.has_permissions(manage_messages=True)
async def delete(ctx, number: int, user: discord.Member = None):
    chan=ctx.channel
    if user == None:
        rep= await ctx.channel.purge(limit=number+1)
    else:
        rep= await ctx.channel.purge(limit=number+1, check=lambda m: m.author == user)
    await ctx.respond(f"{len(rep)} messages ont été supprimés.")

@delete.error
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    if isinstance(error, commands.MissingPermissions):
        await ctx.respond("Vous n'avez pas la permission de faire cette commande.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.respond("Vous n'avez pas spécifié tous les arguments requis.")
    elif isinstance(error, commands.BadArgument):
        await ctx.respond("Vous avez spécifié un argument invalide.")
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.respond("Une erreur est survenue lors de l'exécution de la commande.")
    elif isinstance(error, commands.CheckFailure):
        await ctx.respond("Vous n'avez pas la permission de faire cette commande.")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.respond("Cette commande est sur cooldown.")


@client.slash_command(description="Ferme le bot.")
@commands.is_owner()
async def killbot(ctx):
    await ctx.respond("Bye-bye!")
    exit()
@killbot.error
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    if isinstance(error, commands.NotOwner):
        await ctx.respond("Tu n'es pas le propriétaire du bot. Donc PAS TOUCHE!")

@client.slash_command(description="The sus.")
@commands.guild_only()
@commands.is_owner()
async def imposter(ctx):
    #if timeout
    
    membList = [member for member in ctx.guild.members]
    memb = membList[random.randint(0, len(membList)-1)]
    while memb == client.user:
        memb = membList[random.randint(0, len(membList)-1)]
    img = requests.get(memb.display_avatar.url, stream=True)
    with open('avatar.png', 'wb') as f:
        shutil.copyfileobj(img.raw, f)
    f = open('avatar.png', 'rb')
    await client.user.edit(avatar=f.read(), username=memb.display_name)
    f.close()
    await ctx.respond("C'est très sus tout ça...",ephemeral=True)
@imposter.error
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    if isinstance(error, commands.NoPrivateMessage):
        await ctx.respond("Commande fonctionnelle uniquement dans un serveur.")

@client.slash_command(description="Do your tasks.")
@commands.is_owner()
async def crewmate(ctx):
    # reprend l'image et le nom d'origine du bot
    with open("Strawberry.png", "rb") as image:
        await client.user.edit(avatar=image.read(), username="Marcel-Bot")
        image.close()
    await ctx.respond("Marcel-Bot n'était pas l'imposter.",ephemeral=True)


"""SERVER ONLY##############################################################################################################################################################"""
if server:

    pc=client.create_group(name="pc",description="Eteint ou allume le pc de Nocta")

    @pc.command(description="Démarre le pc de Noctabou.")
    @commands.is_owner()
    async def start(ctx):
        await ctx.respond("Démarrage du PC de Noctabou...")
        os.system("wakemeup Nocta")
    @start.error
    async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
        if isinstance(error, commands.NotOwner):
            await ctx.respond("Tu n'es pas le propriétaire du bot. Donc PAS TOUCHE!")

    @pc.command(description="Arrête le pc de Noctabou.")
    @commands.is_owner()
    async def shutdown(ctx, *, args=None):
        await ctx.respond("Arrêt du PC de Noctabou...")
        if args == None:
            os.system(
                "net rpc shutdown -f -t 30 -I 192.168.1.96 -U aymer%wz5EMMLvqb7cQQA")
        elif args == "restart":
            os.system(
                "net rpc shutdown -r -t 30 -f -I 192.168.1.96 -U aymer%wz5EMMLvqb7cQQA")
        else:
            os.system(
                'net rpc shutdown -f -t 30 -I 192.168.1.96 -U aymer%wz5EMMLvqb7cQQA -C "'+str(args)+'"')
    @shutdown.error
    async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
        if isinstance(error, commands.NotOwner):
            await ctx.respond("Tu n'es pas le propriétaire du bot. Donc PAS TOUCHE!")

    @pc.command(description="Annule l'arrêt du pc de Noctabou.")
    @commands.is_owner()
    async def abort(ctx):
        await ctx.respond("Annulation de l'extinction du PC de Noctabou...")
        os.system("net rpc abortshutdown -I 192.168.1.96 -U aymer%wz5EMMLvqb7cQQA")
    @abort.error
    async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
        if isinstance(error, commands.NotOwner):
            await ctx.respond("Tu n'es pas le propriétaire du bot. Donc PAS TOUCHE!")

    """MC SERVER##############################################################################################################################################################"""
    import libtmux
    server = libtmux.Server()
    session = server.find_where({"session_name": "MCServer"})
    if session == None:
        print(os.system("tmux new -d -s MCServer"))  # créer un tmux
        session = server.find_where({"session_name": "MCServer"})
    window = session.attached_window
    pane = window.attached_pane

    mccommands=client.create_group(name="mc", description="Commandes Minecraft")

    @mccommands.command(description="Démarre le serveur Minecraft séléctionné.")
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
            os.system("tmux send-keys -t MCServer 'cd /home/noctabou/Samba/MCServs/"+serveurMC+"/' Enter")  # va dans le dossier du serveur
            # lance le serveur
            time.wait(1)
            os.system("tmux send-keys -t MCServer './start' Enter")
            await ctx.respond("Démarrage du serveur MC "+serveurMC+" !")
            running = True
        else:
            await ctx.respond("Commande réservée aux modérateurs du serveur.")

    @mccommands.command(description="Ferme le serveur Minecraft séléctionné.")
    async def stop(ctx):
        global running
        if not running:
            await ctx.respond("Aucun serveur n'est lancé.")
            return
        if ctx.author.id in MCmanagers:
            await ctx.respond("Arrêt du serveur MC!")
            os.system("tmux send-keys -t MCServer 'stop' Enter")
            running = False
        else:
            await ctx.respond("Commande réservée aux modérateurs du serveur.")

    @mccommands.command(description="Défini la gamerule keepInventory.")
    async def keepinventory(ctx, *, args=None):
        global running
        if not running:
            await ctx.respond("Aucun serveur n'est lancé.")
            return
        if args == None:
            # récupère l'état de la gamerule keepInventory et laisse une seconde au serveur pour répondre
            os.system("tmux send-keys -t MCServer 'gamerule keepInventory' Enter")
            timestop=10
            for i in range(timestop):
                time.sleep(0.2)
                output=subprocess.check_output(["tmux", "capture-pane", "-J", "-p", "-t", "MCServer"])
                output=output.decode("utf-8")
                output=output.split("\n")
                lastline=output[-1] #last line
                while lastline.startswith('>') or lastline.startswith(' ') or lastline=='':
                    lastline=output.pop()
                if "is currently set to: " in lastline:
                    #print("Réponse trouvée")
                    break
                if i == timestop/2:
                    os.system("tmux send-keys -t MCServer 'gamerule keepInventory' Enter")
                if i == timestop-1:
                    return "503"
            # récupère la réponse
            state=lastline.split("is currently set to: ")[-1]
            if state.startswith("true"):
                await ctx.respond("Le keepInventory est actuellement actif.")
            elif state.startswith("false"):
                await ctx.respond("Le keepInventory est actuellement inactif.")
            else:
                await ctx.respond("Erreur de réponse du serveur.")
            return
        args = args.lower()
        if args == "true":
            os.system(
                "tmux send-keys -t MCServer 'gamerule keepInventory true' Enter")
            await ctx.respond("La gamerule KeepInventory est activée")
        elif args == "false":
            os.system(
                "tmux send-keys -t MCServer 'gamerule keepInventory false' Enter")
            await ctx.respond("La gamerule KeepInventory est désactivée")

    # Server Infos
    def MCServerPlaying():
        timestop=10
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
            if "INFO]" in lastline and ": There are " in lastline:
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

    @mccommands.command(description="Renvoit qui joue sur le serveur Minecraft séléctionné.")
    async def playing(ctx):
        global running
        if not running:
            await ctx.respond("Aucun serveur n'est lancé.")
            return
        output = MCServerPlaying()
        if output == "503":
            await ctx.respond("Le serveur ne répond pas.")
        else:
            await ctx.respond("Il y a "+output[0]+" joueurs sur "+output[1]+" max.\n"+output[2])
    
    @tasks.loop(seconds=90)
    async def statusMCupdate():
        global running, serveurMC, actif
        #print("Execution de statusMCupdate")

        if running and actif:
            if serveurMC != None:
                output = MCServerPlaying()
                if output == "503":
                    print("Le serveur ne répond pas.")
                    pass
                else:
                    #print(serveurMC+" | "+output[0]+"/"+output[1]+" | "+output[2])
                    await client.change_presence(activity=discord.Game(name=serveurMC+" | "+output[0]+"/"+output[1]))
        else:
            #print("Aucun serveur n'est lancé.")
            await client.change_presence(activity=discord.Game(name=""))

    @mccommands.command(description="Debug le status du serveur Minecraft séléctionné.")
    async def debugstatus(ctx):
        global running
        running=MCServerRunning()
        await ctx.respond("Le serveur est "+str(running))

    def MCServerRunning():
        if MCServerPlaying() == "503":
            return False
        return True

        
    class Dropdown(discord.ui.Select):
        def __init__(self, bot_: discord.Bot):
            # For example, you can use self.bot to retrieve a user or perform other functions in the callback.
            # Alternatively you can use Interaction.client, so you don't need to pass the bot instance.
            self.bot = bot_
            # Set the options that will be presented inside the dropdown:
            options = []
            for i in os.listdir("/home/noctabou/Samba/MCServs/"):
                options.append(discord.SelectOption(label=i))

            # The placeholder is what will be shown when no option is selected.
            # The min and max values indicate we can only pick one of the three options.
            # The options parameter, contents shown above, define the dropdown options.
            super().__init__(
                placeholder="Choose your favourite colour...",
                min_values=1,
                max_values=1,
                options=options,
            )
        async def callback(self, interaction: discord.Interaction): # the function called when the user is done selecting options
            global serveurMC
            serveurMC = self.values[0]
            await interaction.response.send_message(f"Le serveur selectionné est {self.values[0]}." , ephemeral=True)

    class MyView(discord.ui.View):
        def __init__(self,bot_: discord.Bot):
            super().__init__()
            self.add_item(Dropdown(bot_))

    @mccommands.command(description="Choisi un serveur Minecraft.")
    async def selectserver(ctx):
        if ctx.author.id in MCmanagers:
            view=MyView(client)
            await ctx.respond("Choisissez un serveur Minecraft\nLe serveur "+str(serveurMC)+" est sélectionné.",view=view,ephemeral=True)
        else:
            await ctx.respond("Commande réservée aux modérateurs du serveur.",ephemeral=True)

    MCmanagers = (nocta, 396255858834800662)
    global serveurMC, running
    serveurMC = "Mod Cult"
    running = MCServerRunning()
    print("Server is running: " + str(running))
"""COMMANDS##############################################################################################################################################################"""

"""HELP##############################################################################################################################################################"""
client.remove_command("help")
"""help=client.create_group(name="help",description="Affiche l'aide du bot.")

@help.command(name="commands",description="Affiche l'aide du bot.")
async def commands(ctx):
    embed = discord.Embed(title="Commandes du Bot",
                          description="", color=0x00ff00)
    embed.add_field(name="°ping", value="Pong!", inline=False)
    embed.add_field(
        name="°msgcount", value="Affiche le nombre de messages depuis le lancement du bot", inline=False)
    embed.add_field(
        name="°userinfo", value="Affiche les informations sur l'utilisateur mentionné", inline=False)
    embed.add_field(
        name="°pp", value="Affiche la photo de profil de l'utilisateur mentionné", inline=False)
    embed.add_field(
        name="°rançais", value="Convertit un message en langue française", inline=False)
    embed.add_field(name="°lettermoji",
                    value="Convertit la première lettre de chaque mot en lettre emoji", inline=False)
    embed.add_field(
        name="°delete", value="Supprime un nombre de messages d'un utilisateur, ou du tchat si aucun n'est mentionné", inline=False)
    embed.add_field(name="°killbot",
                    value="Ferme le bot. (owner only)", inline=False)
    embed.add_field(
        name="°stopPC", value="Eteint le pc. (owner only)", inline=False)
    embed.add_field(
        name="°help", value="Affiche les commandes du bot", inline=False)
    embed.add_field(name="°help <commande>",
                    value="Affiche les informations sur une commande", inline=False)
    embed.add_field(name="#########Server Commandes#########",
                    value="Commandes qui contrôlent le serveur MC Server")
    embed.add_field(name="°MCStart",
                    value="Ouvre le serveur (gérants only)", inline=False)
    embed.add_field(
        name="°MCStop", value="Ferme le serveur (gérants only)", inline=False)
    embed.add_field(name="°MCSelectServer",
                    value="Sélectionne le serveur à utiliser (gérants only)", inline=False)
    embed.add_field(name="°MCKeepInventory",
                    value="Change la gamerule keepInventory sur le serveur", inline=False)
    embed.add_field(name="°MCPlaying",
                    value="Affiche le nombre de joueurs sur le serveur", inline=False)

    await ctx.respond(embed=embed)


@help.command()
async def userinfo(ctx):
    await ctx.respond("Affiche les informations sur l'utilisateur mentionné\n**Syntaxe:** `°userinfo [@utilisateur]`")


@help.command()
async def pp(ctx):
    await ctx.respond("Affiche la photo de profil de l'utilisateur mentionné\n**Syntaxe:** `°pp [@utilisateur]`")


@help.command()
async def rançais(ctx):
    await ctx.respond("Convertit un message en langue rançaise\n**Syntaxe:** `°rançais [message]`")


@help.command()
async def lettermoji(ctx):
    await ctx.respond("Convertit la première lettre de chaque mot en lettre emoji\n**Syntaxe:** `°lettermoji [message]`")


@help.command()
async def delete(ctx):
    await ctx.respond("Supprime un nombre de messages d'un utilisateur, ou du tchat si aucun n'est mentionné\n**Syntaxe:** `°delete [nombre] [@utilisateur]`")


@help.command()
async def stop_pc(ctx):
    await ctx.respond("Commandes PC (contrôle le PC de Noctabou)\n°stopPC : Eteint le PC dans 30s.\n°stopPC restart : Redémarre le PC dans 30s.\nSi plus d'arguments sont donnés, Eteint le PC dans 30s avec un message sur l'écran.\n°abortPC : Annule l'extinction du PC.\n°startPC : Allume le PC (prend \~1minute) ")


@help.command()
async def mckeepinventory(ctx):
    await ctx.respond("Change keepInventory\n°MCKeepInventory True : Active la gamerule\n°MCKeepInventory False : Désactive la gamerule\n°MCKeepInventory : Affiche l'état de la gamerule")

@help.command()
async def mcselectserver(ctx):
    await ctx.respond("Sélectionne le serveur à utiliser\n°MCSelectServer [serveur] (gérants only) (voué à changer)")
"""
"""HELP##############################################################################################################################################################"""

client.run(token, reconnect=True)
