# bot.py
import asyncio
import os
import random
from datetime import datetime

import discord
import pytz
import requests
from discord import Intents, ChannelType
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv


requests.get('https://discord.com', verify=False)
VOL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'False', 'simulate': 'True', 'key': 'FFmpegExtractAudio'}
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 - reconnect_streamed 1 - reconnect_delay_max 5', 'options': '-vn'
}

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PRAYER_API_URL = 'http://api.aladhan.com/v1/timingsByCity'

intents = Intents.default()
intents.message_content = True
intents.voice_states = True # Обработка голосовых состояний

bot = commands.Bot(command_prefix='/', intents=intents)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Бот запущен')
    check_prayer_times.start()


@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel and not before.channel:  # Если пользователь зашел в голосовой канал
        voice_channel = after.channel
        if not voice_channel:  # Проверка на существование канала
            return
        
        audio_files = ['mephala.mp3', 'bratishka.mp3']  # Список аудиофайлов
        random_audio = random.choice(audio_files)  # Выбираем случайный файл
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio(random_audio))  # Воспроизведение случайного аудиофайла
        
        while vc.is_playing():
            await asyncio.sleep(1)
        
        await vc.disconnect()


@tasks.loop(minutes=1)
async def check_prayer_times():
    now = datetime.now(pytz.timezone('Europe/Moscow'))
    current_time = now.strftime('%H:%M')
    response = requests.get('http://api.aladhan.com/v1/timingsByCity',
                            params={"city": "Makhachkala", "country": "Russia"})
    all_timings = dict(response.json()['data']['timings'])
    desired_timings = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]
    timings = {timing: all_timings[timing] for timing in all_timings if timing in desired_timings}
    if current_time in timings.values():
        for channel in bot.get_all_channels():
            if channel.type.value == ChannelType.voice.value:
                if len(channel.members) > 0:
                    vc = await channel.connect()
                    vc.play(discord.FFmpegPCMAudio('azan.mp3'))
                    while vc.is_playing():
                        await asyncio.sleep(1)
                    await vc.disconnect()

@bot.hybrid_command(name='chort', description='Who is chort?')
@app_commands.describe(names='Names to choose from')
@app_commands.choices(names=[
    discord.app_commands.Choice(name='Abdurashid', value=2),
    discord.app_commands.Choice(name='Arthur', value=3),
    discord.app_commands.Choice(name='Burgers', value=4),
    discord.app_commands.Choice(name='Ibrahim', value=5),
    discord.app_commands.Choice(name='Ibrahim Chort', value=14),
    discord.app_commands.Choice(name='Khanchik', value=46),
    discord.app_commands.Choice(name='Murad', value=10)
])
async def play_random(ctx, names: discord.app_commands.Choice[int]):
    voice_channel = ctx.author.voice.channel
    vc = await voice_channel.connect()
    vc.play(discord.FFmpegPCMAudio(f'{names.value}.mp3'))
    await ctx.send('Playing..')
    while vc.is_playing():
        await asyncio.sleep(1)
    await vc.disconnect()
    await ctx.send('Done')


@bot.hybrid_command(name='characters', description="Memes in the voices of game characters")
@app_commands.describe(names='Memes to choose from')
@app_commands.choices(names=[
    discord.app_commands.Choice(name='(Geralt) Not proven yet...', value=47),
    discord.app_commands.Choice(name='(Geralt) Motivation', value=48),
    discord.app_commands.Choice(name='(Hermaeus) Superman', value=49)
])
async def play_random(ctx, names: discord.app_commands.Choice[int]):
    voice_channel = ctx.author.voice.channel
    vc = await voice_channel.connect()
    vc.play(discord.FFmpegPCMAudio(f'{names.value}.mp3'))
    await ctx.send('Playing...')
    while vc.is_playing():
        await asyncio.sleep(1)
    await vc.disconnect()
    await ctx.send('Done')


@bot.hybrid_command(name='soundpad', description='Different sounds from memes')
@app_commands.describe(names='Names to choose from')
@app_commands.choices(names=[
    discord.app_commands.Choice(name='Down syndrome', value=15),
    discord.app_commands.Choice(name='Blin, na..', value=16),
    discord.app_commands.Choice(name='Bruh', value=17),
    discord.app_commands.Choice(name='Kazakhstan bomb', value=18),
    discord.app_commands.Choice(name="I'm a muslim", value=19),
    discord.app_commands.Choice(name='To be continued..', value=20),
    discord.app_commands.Choice(name="No", value=22),
    discord.app_commands.Choice(name="Let's go..", value=23),
    discord.app_commands.Choice(name="Good night", value=24),
    discord.app_commands.Choice(name="KurbanHaji", value=25),
    discord.app_commands.Choice(name="I'm a Dagestan", value=26),
    discord.app_commands.Choice(name="The earth is round", value=27),
    discord.app_commands.Choice(name="Do the tining", value=28),
    discord.app_commands.Choice(name="I'm a georgian", value=29),
    discord.app_commands.Choice(name="Avaretc...!", value=32),
    discord.app_commands.Choice(name="Sheep came home", value=33),
    discord.app_commands.Choice(name="Autumn", value=35),
    discord.app_commands.Choice(name="Don't write here anymore", value=36),
    discord.app_commands.Choice(name="Once you live...", value=37),
    discord.app_commands.Choice(name="Working!", value=39),
    discord.app_commands.Choice(name="What a luxury!", value=40),
    discord.app_commands.Choice(name="Hello", value=42),
    discord.app_commands.Choice(name="How do you tell with me?", value=43),
    discord.app_commands.Choice(name="Assalamu Aleykum", value=44),
    discord.app_commands.Choice(name="Laugh", value=45)
])
async def play_random(ctx, names: discord.app_commands.Choice[int]):
    voice_channel = ctx.author.voice.channel
    vc = await voice_channel.connect()
    vc.play(discord.FFmpegPCMAudio(f'{names.value}.mp3'))
    await ctx.send('Playing..')
    while vc.is_playing():
        await asyncio.sleep(1)
    await vc.disconnect()
    await ctx.send('Done')


@bot.hybrid_command(name='blessyou', description='Bless you!')
async def bless_random(ctx):
    voice_channel = ctx.author.voice.channel
    vc = await voice_channel.connect()
    audio_files = ['blessyou', 'blessyou1']
    random_audio = random.choice(audio_files)
    vc.play(discord.FFmpegPCMAudio(random_audio + '.mp3'))
    await ctx.send('Blessing..')
    while vc.is_playing():
        await asyncio.sleep(1)
    await vc.disconnect()
    await ctx.send('Done')


@bot.hybrid_command(name='goodmorning', description='Good Morning!')
async def bless_random(ctx):
    voice_channel = ctx.author.voice.channel
    vc = await voice_channel.connect()
    vc.play(discord.FFmpegPCMAudio(f'dobr.mp3'))
    await ctx.send('Listening..')
    while vc.is_playing():
        await asyncio.sleep(1)
    await vc.disconnect()
    await ctx.send('Done')

@bot.hybrid_command(name='podkol', description='Kirkorov meme')
async def podkol_kirk(ctx):
    voice_channel = ctx.author.voice.channel
    vc = await  voice_channel.connect()
    vc.play(discord.FFmpegPCMAudio(f'podkol.mp3'))
    await ctx.send('Listening to Kirkorov..')
    while vc.is_playing():
        await asyncio.sleep(1)
    await vc.disconnect()
    await ctx.send('Done')


@bot.hybrid_command(name='azan', description='Listen to the azan')
async def azan_islam(ctx):
    voice_channel = ctx.author.voice.channel
    vc = await voice_channel.connect()
    vc.play(discord.FFmpegPCMAudio(f'azan.mp3'))
    await ctx.send('Listening..')
    while vc.is_playing():
        await asyncio.sleep(1)
    await vc.disconnect()
    await ctx.send('Done')

bot.run(TOKEN)