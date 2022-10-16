#Discord Bot for transforming text to connected emojis
import discord
import asyncio
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(intents=intents, case_insensitive=False,allowed_mentions=discord.AllowedMentions(everyone=False))

@client.event
async def on_ready():
    print("Bot is ready")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

catphabet={'a':'<:HA:763600513295450112>',
'b':'<:HB:763600513375010826>',
'c':'<:HC:763600513433600091>',
'd':'<:HD:763600512909180929>',
'e':'<:HE:763600513420886056>',
'f':'<:HF:763600513131610164>',
'g':'<:HG:763600513135542284>',
'h':'<:HH:763600513383137301>',
'i':'<:HI:763600513455357952>',
'j':'<:HJ:763600513026883598>',
'k':'<:HK:763600513451032626>',
'l':'<:HL:763600513723793468>',
'm':'<:HM:763600513412759593>',
'n':'<:HN:763600513723138068>',
'o':'<:HO:763600513962082324>',
'p':'<:HP:763600513705967686>',
'q':'<:HQ:763600513727201280>',
'r':'<:HR:763600513350500383>',
's':'<:HS:763600513693909002>',
't':'<:HT:763600513941504030>',
'u':'<:HU:763600513399914507>',
'v':'<:HV:763600513546584067>',
'w':'<:HW:763600513911488532>',
'x':'<:HX:763600513929052211>',
'y':'<:HY:763600514105475112>',
'z':'<:HZ:763600513874395146>',
'.':'<:HPER:763600513668218922>',
'?':'<:HQU:763600513761148950>',
'!':'<:HEX:763600513567817769>',
"'":'<:HAP:763600513874001940>',
" ":'<:TUM:763615857703125012>'}

spaces=['<:HEAD:763620394463920129>','<:TUM:763615857703125012>','<:FEET:763615857904975912>']

@client.slash_command()
async def catsay(ctx, *, text):  
    #transform words to emojis
    if len(text) > 60:
        await ctx.respond("Text too long, please keep it under 60 characters")
        return
    text = text.lower()
    words=text.split(' ')
    text=''
    for word in words:
        text+='<:HEAD:763620394463920129>'
        for letter in word:
            if letter in catphabet:
                text+=catphabet[letter]
            else:
                text+=letter
        text+='<:FEET:763615857904975912>\n'
    await ctx.respond(text)

@client.slash_command()
async def verylongcatsay(ctx, *, text): 
    ftext='<:HEAD:763620394463920129>'
    if len(text) > 78:
        await ctx.respond("Text too long, please keep it under 80 characters")
        return
    text = text.lower()
    for letter in text:
        if letter in catphabet:
            ftext+=catphabet[letter]
        else:
            ftext+=letter
    ftext+='<:FEET:763615857904975912>'
    await ctx.respond(ftext)

@client.slash_command()
async def moguscat(ctx):
    await ctx.respond('<:ZSPACER:654639043891691521><:Cse:654639050572955658><:Tvst:654639044117921793><:Tvst:654639044117921793><:Tvst:654639044117921793><:Tvst:654639044117921793><:Csw:654639051793760257>\n<:Couro:655050190973042718><:CTn:654639039034425344><:Tvst:654639044117921793><:Tvst:654639044117921793><:Tvst:654639044117921793><:Csw:654639051793760257><:CTe:654639037700898828><:Csw:654639051793760257>\n<:Tast:654639044340482069><:ZSPACER:654639043891691521><:ZSPACER:654639043891691521><:ZSPACER:654639043891691521><:ZSPACER:654639043891691521><:Tast:654639044340482069><:Tast:654639044340482069><:Tast:654639044340482069>\n<:Cne:654639050917150720><:CTs:654639038363598858><:HS:763600513693909002><:HU:763600513399914507><:HS:763600513693909002><:Cnw:654639045833523200><:Tast:654639044340482069><:Tast:654639044340482069>\n<:ZSPACER:654639043891691521><:Tast:654639044340482069><:ZSPACER:654639043891691521><:ZSPACER:654639043891691521><:ZSPACER:654639043891691521><:ZSPACER:654639043891691521><:CTe:654639037700898828><:Cnw:654639045833523200>\n<:ZSPACER:654639043891691521><:Tast:654639044340482069><:ZSPACER:654639043891691521><:Cse:654639050572955658><:Csw:654639051793760257><:ZSPACER:654639043891691521><:Tast:654639044340482069>\n<:ZSPACER:654639043891691521><:Cne:654639050917150720><:Tvst:654639044117921793><:Cnw:654639045833523200><:Cne:654639050917150720><:Tvst:654639044117921793><:Cnw:654639045833523200>')

@client.slash_command()
async def portalcatsay(ctx, *, text):
    #transform words to emojis
    if len(text) > 60:
        await ctx.respond("Text too long, please keep it under 60 characters")
        return
    text = text.lower()
    words=text.split(' ')
    text=''
    for word in words:
        text+='<:PoW:654642045255811082>'
        for letter in word:
            if letter in catphabet:
                text+=catphabet[letter]
            else:
                text+=letter
        text+='<:PbE:654642046614896640>\n'
    text= '<:HEAD:763620394463920129>' + text[25:-26] + '<:FEET:763615857904975912>'
    await ctx.respond(text)

@client.slash_command()
async def shit(ctx):
    await ctx.respond("<:SEo:655050190973042718><:Efh:672519910567706664><:Nmad:673166882026815533><:Nth:672563359786467329><:Nf:654639061717352449><:Wp:654642045255811082><:St:654639038363598858><:Ehat:672520027874000931>\n<:NEc:654639050917150720><:SWc:654639051793760257><:Et:654639037700898828><:Wt:654639037117890571><:NSctw:654899231445876743><:Bl:654639043891691521><:NSchonk:654899230640439306>\n<:Wf:654639059465011201><:NWc:654639045833523200><:Sh:654639066813431843><:Sf:654639061809496074><:Shat:672520027181940738><:Bl:654639043891691521><:Sp:654642047143116810>")

client.run("MTAyMDMzNTA2ODEwMDcwMjM2MA.GmJoUH.pGWcMj7FYoDIPxWX-HDQ2s45uZzNHv1HP65Bbc", reconnect=True)