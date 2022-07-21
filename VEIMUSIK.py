import discord
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from discord.ext import commands
from discord.utils import get

TOKEN = 'ODQ2NzM3MjQ2MjU3MjgzMTQy.GYbkhZ.6urwcYSqI5tDv2lOMRoo4DVxGRSvcNhxRBQfJc'
BOT_PREFIX = 'vei ', 'Vei ', 'VEI '

client = commands.Bot(command_prefix=BOT_PREFIX)
players = {}

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('"moderating mode"    '))
    print("onlen dgn nama: " + client.user.name + "\n")

@client.command(pass_context=True, aliases=['masuk', 'm'])
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await ctx.send(f"aku dah masuk di cenel {channel}")


@client.command(pass_context=True, aliases=['keluar', 'k'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"kluar dari {channel}")
        await ctx.send("bai sayang")
    else:
        print("kluar chanel")
        await ctx.send("tengok, aku gak ada di situ ")


@client.command(pass_context=True, aliases=['hi'])
async def hello(ctx):
    await ctx.send('hello')

@client.command(pass_context=True, aliases=['putar'])
async def play(ctx, url):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        with  YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
        await ctx.send(f'Playing{url}')
    else:
        await ctx.send("Already playing song")
        return

@client.command(pass_context=True, aliases=['berhenti'])
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    voice.stop()

client.run(TOKEN)
