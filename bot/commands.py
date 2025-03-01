import asyncio

import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext.commands import Context

from bot import config
from bot.bot import bot_instance
from bot.utils import get_audio_path


async def play_sound(ctx: Context, audio_name):
    voice_channel = ctx.author.voice.channel
    if bot_instance.user.id not in [member.id for member in voice_channel.members]:
        if ctx.guild.voice_client:
            await ctx.send('Я уже в другом канале!')
            return
        vc = await voice_channel.connect()
    else:
        vc = ctx.guild.voice_client
    audio_path = get_audio_path(audio_name)
    vc.play(discord.FFmpegPCMAudio(audio_path))
    await ctx.send('Playing..')
    while vc.is_playing():
        await asyncio.sleep(1)
    await ctx.send('Done')


@bot_instance.hybrid_command(name='chort', description='Who is chort?')
@app_commands.describe(names='Names to choose from')
@app_commands.choices(names=[
    Choice(name=name, value=value)
    for name, value in config.SOUNDPAD_NAMES.items()
])
async def play_chort(ctx, names: discord.app_commands.Choice[int]):
    await play_sound(ctx, names.value)


@bot_instance.hybrid_command(name='characters', description="Memes in the voices of game characters")
@app_commands.describe(names='Memes to choose from')
@app_commands.choices(names=[
    Choice(name=name, value=value)
    for name, value in config.SOUNDPAD_2.items()
])
async def play_characters(ctx, names: discord.app_commands.Choice[int]):
    await play_sound(ctx, names.value)


@bot_instance.hybrid_command(name='soundpad', description='Different sounds from memes')
@app_commands.describe(names='Names to choose from')
@app_commands.choices(names=[
    Choice(name=name, value=value)
    for name, value in config.SOUNDPAD_1.items()
])
async def play_soundpad(ctx, names: discord.app_commands.Choice[int]):
    await play_sound(ctx, names.value)


@bot_instance.hybrid_command(name='azan', description='Listen to the azan')
async def azan_islam(ctx):
    await play_sound(ctx, "azan")


@bot_instance.hybrid_command(name='gel', description='Gel bunna yashim')
async def gel(ctx):
    vc = ctx.guild.voice_client
    if vc and vc.is_connected():
        await vc.disconnect()
    await ctx.author.voice.channel.connect()
