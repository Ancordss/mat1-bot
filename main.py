'''notas antes de empezar estar en modod developer en discord
    los chanel ID se sacan del canal donde quieres usarlo'''


import os
from discord.ext import commands, tasks
import discord
import urllib.request
import json
import aiohttp
import asyncio

# --------------------secure tokens-----------------------------------------

if os.path.exists(os.getcwd() + "/config.json"):
    with open("./config.json") as f:
        configData = json.load(f)
else:
    configTemplate = {"Token": "", "Prefix": "!", "Key": ""}

    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f)

TOKEN = configData["Token"]
prefix = configData["Prefix"]
KEY = configData["Key"]
# --------------------------------------------------------------------------------
intents = discord.Intents.default()
intents.members = True
intents = intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)  # prefijo del Bot
# esto pertenece a el evento de entrar al servidor
bot.remove_command("help")  # remueve el comando de ayuda normal

# comands BOT:


@bot.event
async def on_ready():
    print("Estoy Listo.")
    # como dice ahi cambia la presencia del bot.
    await bot.change_presence(activity=discord.Game(name=f"{prefix}aprender"))


# anuncios


@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def anuncios(ctx, *, message):
    embed = discord.Embed(title=f"Informacion",
                          description=message, color=0x00e1ff)
    embed.set_thumbnail(
        url="https://i.imgur.com/douh7U1.gif")
    embed.set_footer(text="Made by Ancordss")
    await ctx.send(embed=embed)


# Ban


@bot.command()
# hace que solo las personas con ese permiso puedan ejecutar el comando
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member} ha sido baneados por pvto!!!")

# kick


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member} ha sido kickeado por feo!!!")

# unban


@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    bannedUsers = await ctx.guild.bans()
    name, discrimator = member.split("#")

    for ban in bannedUsers:
        user = ban.user
        if(user.name, user.discriminator) == (name, discrimator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} ah sido desbaneado.")


# dog

@bot.command()
async def dog(ctx):
    async with aiohttp.ClientSession() as session:
        # buscar API nuevas
        request = await session.get('https://some-random-api.ml/img/dog')
        dogjson = await request.json()

        request2 = await session.get('https://some-random-api.ml/facts/dog')
        factjson = await request2.json()

    embed = discord.Embed(
        title="Doggo!", color=discord.Color.purple())
    embed.set_image(url=dogjson['link'])
    embed.set_footer(text=factjson['fact'])
    await ctx.send(embed=embed)

# ping


@bot.command(name="ping")
async def ping(ctx: commands.Context):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

# prueba ping asia otro ususario


@bot.command()
async def pinga(ctx, member):
    await ctx.send(f"Pong! {member} {round(bot.latency * 1000)}ms ")


# hola

@bot.command(name="hi")
async def hi(ctx: commands.Context):
    await ctx.send("hola baby!!!!")

# hola a otro ususario


@bot.command()
async def hia(ctx, member):
    await ctx.send(f"hola bebe {member}")

# ggs a otro usuario


@bot.command()
async def gga(ctx, member):
    await ctx.send(f"good game! {member}")

# f a otro ususario


@bot.command()
async def fa(ctx, member):
    await ctx.send(f"*F* mi pana :c {member}")

# f


@bot.command()
async def f(ctx):
    await ctx.send("#F# :C:C:C")

# show subscriptores


@bot.command(name='subs')
async def subscriptores(ctx, username):
    data = urllib.request.urlopen(
        "https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername=" + username + "&key=" + KEY).read()
    subs = json.loads(data)["items"][0]["statistics"]["subscriberCount"]
    response = username + " tiene " + \
        "{:,d}".format(int(subs)) + " suscriptores!"
    await ctx.send(response)

# suma


@bot.command(name='s')  # suma
async def sumar(ctx, num1, num2):
    response = int(num1) + int(num2)
    await ctx.send(response)

# multiplicar


@bot.command(name='m')  # multiplicar
async def multiplicar(ctx, num1, num2):
    response = int(num1) * int(num2)
    await ctx.send(response)

# cambia la actividad del BOT


@bot.command()
@commands.has_permissions(administrator=True)
async def cba(ctx, *, activity):
    await bot.change_presence(activity=discord.Game(name=activity))
    await ctx.send(f"la actividad del BOT ah sido cambia a {activity}")

# mutear a alguien


@bot.command(description="mutea a un especifico usuario")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedrole = discord.utils.get(guild.roles, name="Muted")

    if not mutedrole:
        mutedrole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedrole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

    await member.add_roles(mutedrole, reason=reason)
    await ctx.send(f"muted {member.mention} for reason {reason}")
    await member.send(f"has sido muteado en el servidor {guild.name} porque {reason}")

# desmutear a alguien XD


@bot.command(description="desmutea a un especifico usuario")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    guild = ctx.guild
    mutedrole = discord.utils.get(guild.roles, name="Muted")

    await member.remove_roles(mutedrole)
    await ctx.send(f"unmute {member.mention}")
    await member.send(f"has sido desmuteado del servidor {guild.name}")
# --------------------------embeds-----------------------------

# se puede colocar la description aqui para despues en el comando help ser llamada


@bot.command(description="recupera la informacion del usuario")
async def myinfo(ctx):
    user = ctx.author

    embed = discord.Embed(title="INFORMACION DEL USUARIO",
                          description=f"aqui va la informacion que recuperamos del usuario {user}", colour=user.colour)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="NAME", value=user.name, inline=True)
    embed.add_field(name="NICKNAME", value=user.nick, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="STATUS", value=user.status, inline=True)
    embed.add_field(name="TOP ROLE", value=user.top_role.name, inline=True)
    await ctx.send(embed=embed)

# da informacion sobre el usuario
# # TODO: arreglar (no funciona)


@bot.command()
async def userinfo(ctx, member):
    user = member

    embed = discord.Embed(title="INFORMACION DEL USUARIO",
                          description=f"aqui va la informacion que recuperamos del usuario {user}", colour=user.colour)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="NAME", value=user.name, inline=True)
    embed.add_field(name="NICKNAME", value=user.nick, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="STATUS", value=user.status, inline=True)
    embed.add_field(name="TOP ROLE", value=user.top_role.name, inline=True)
    await ctx.send(embed=embed)


@bot.command()
async def help(ctx, commandSent=None):

    if commandSent != None:

        for command in bot.commands:
            if commandSent.lower() == command.name.lower:

                paramsString = ""

                for param in command.clean.params:
                    paramsString += param + ", "

                paramsString = paramsString[:-2]

                if len(command.clean_params) == 0:
                    paramsString = "None"

                embed = discord.Embed(
                    title=f"help - {command.name}", description=command.description)
                embed.add_field(name="parameters", value=paramsString)
                await ctx.message.delete()
                await ctx.author.send(embed=embed)

    else:
        user = ctx.author
        # se le puede agregar url a el titulo o a la description colocandolo asi: title="titulo", url="https://realdrewdata.medium.com/"
        embed = discord.Embed(title="Lista de comandos",
                              description="Esta es la lista de comandos, estare agregando mas.", color=0x109319)
        # se puede insertar un icono de imagen colocando despues de url: icon_url="url de la imagen"
        embed.set_author(name="Ancordss", url="https://github.com/Ancordss",
                         icon_url="https://avatars.githubusercontent.com/u/87324382?s=96&v=4")
        embed.set_thumbnail(
            url="https://i.imgur.com/douh7U1.gif")

        embed.add_field(
            name="!adcomandos", value="para ver los comandos de administrator", inline=True)
        embed.add_field(
            name="!ping", value="devuelve el ping que tienes", inline=False)
        embed.add_field(
            name="!pinga", value="devuelve el ping de la persona que quieras usando @", inline=False)
        embed.add_field(name="!hi", value="te saluda el bot", inline=True)
        embed.add_field(
            name="!hia", value="el bot saluda a la persona que quieras [usa @]", inline=True)
        embed.add_field(
            name="!dog", value="imagen random de perros", inline=True)
        embed.add_field(name="!gga", value="gg a alguien [usa @]", inline=True)
        embed.add_field(name="!f", value="F", inline=True)
        embed.add_field(name="!fa", value="F a [usa @]", inline=True)
        embed.add_field(name="!s", value="suma 2 numeros", inline=True)
        embed.add_field(name="!m", value="multiplica 2 numeros", inline=True)
        embed.add_field(
            name="!subs", value="devuelve las subs de cierto canal uso[!subs auronplay]", inline=True)
        embed.add_field(
            name="!myinfo", value="devuelve la informacion de tu usuario xd", inline=True)
        embed.add_field(
            name="!userinfo", value="devuelve la informacion de otro usuario [esta bug y no jala XD]")

        embed.set_footer(text="es todo por ahora :'v")
        await ctx.message.delete()
        await ctx.send(embed=embed)


@bot.command()
async def adcomandos(ctx):

    embed = discord.Embed(title="Lista de comandos de Administrador",
                          description="Esta es la lista de comandos para administradores, estare agregando mas.", color=0xab0030)

    embed.set_author(name="Ancordss", url="https://github.com/Ancordss",
                     icon_url="https://avatars.githubusercontent.com/u/87324382?s=96&v=4")
    embed.set_thumbnail(url="https://i.imgur.com/MWS0F0K.jpeg")

    embed.add_field(name="!ban", value="banea a un usuario", inline=True)
    embed.add_field(
        name="!unban", value="desbanea al usuario uso \n [!unban nombre#0000]", inline=True)
    embed.add_field(name="!mute", value="mutea a un usuario", inline=True)
    embed.add_field(name="!unmute", value="desmutea a un usuario", inline=True)
    embed.add_field(name="!kick", value="kickea a usuarios", inline=True)
    embed.add_field(
        name="!anuncios", value="crea un anuncio xd uso[!anuncio e ingresa el texto]", inline=True)
    embed.add_field(
        name="!repetir", value="repite el texto ingresado uso[!repetir start 3 'texto']", inline=True)
    embed.add_field(name="!cba (cambia la actividad del BOT)",
                    value="po eso we cambia la actividad xD", inline=True)

    embed.set_footer(text="es todo por ahora :'v")
    await ctx.send(embed=embed)


# -------------------------------moderar servidor--------------------------------


@bot.event
# detecta el link y lo elimina
async def on_message(message):
    if 'https://' in message.content:
        await message.delete()
        await message.channel.send(f"{message.author.mention} no pases links! pls")
    else:
        await bot.process_commands(message)

# crea la lista de palabras que no se pueden usar en le servidor
badwords = ['bad', 'words', 'here', 'puto']


@bot.event
async def on_message(message):
    for i in badwords:  # Go through the list of bad words;
        if i in message.content:
            await message.delete()
            await message.channel.send(f"{message.author.mention} no uses esa palabra!")
            bot.dispatch('profanity', message, i)
            # So that it doesn't try to delete the message again, which will cause an error.
            return
    await bot.process_commands(message)


@bot.event
async def on_profanity(message, word):
    # coloca el id de tu canal aqui
    channel = bot.get_channel(727909351716683879)
    # Let's make an embed!
    embed = discord.Embed(title="Alerta de profanacion!",
                          description=f"{message.author.name} ha dicho ||{word}||", color=discord.Color.blurple())
    await channel.send(embed=embed)


# ------------------------bienvenida---------------------------------------


@bot.event
async def on_member_join(member: discord.Member):
    channel = bot.get_channel(727909351716683879)

    if not channel:
        return
    embed = discord.Embed(
        title=f"Welcome {member.name}", description=f"Thanks for joining {member.guild.name}!")  # F-Strings!
    embed.set_thumbnail(url=member.avatar_url)
    await channel.send(embed=embed)

# comando para correr la tarea


@bot.command()
async def repetir(ctx, enable="start", interval=10, message=""):
    if enable.lower() == "stop":
        messageInterval.cancel()
    elif enable.lower() == "start":
        messageInterval.change_interval(seconds=int(interval))
        messageInterval.start(ctx, message)


# ------------------------task------------------------
# esto corre siempre el bot
@tasks.loop(seconds=10)
# se pueden correr en segundos (seconds) , minuros (minutes) , horas (hours)
async def messageInterval(ctx, message):
    await ctx.send(message)


bot.run(TOKEN)
