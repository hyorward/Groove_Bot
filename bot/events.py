import asyncio
import os
import random

import discord
from discord import VoiceState

from bot.bot import bot_instance
from bot.config import AUDIO_FOLDER
from bot.prayers import check_prayer_times

ON_JOIN_AUDIOS = ['mephala.mp3', 'bratishka.mp3']


@bot_instance.event
async def on_ready():
    await bot_instance.tree.sync()
    check_prayer_times.start()
    print("Бот запущен.")


@bot_instance.event
async def on_voice_state_update(member, before_voice_state: VoiceState, after_voice_state: VoiceState):
    if before_voice_state.channel == after_voice_state.channel:
        return
    if not after_voice_state.channel and before_voice_state.channel:  # если все вышли бот тоже выходит
        members = before_voice_state.channel.members
        if (len(members) == 1) and (members[0].id == bot_instance.user.id):
            await member.guild.voice_client.disconnect()

    if not after_voice_state.channel:  # Если пользователь не зашел в голосовой канал
        return

    voice_channel = after_voice_state.channel
    if not voice_channel:  # Проверка на существование канала
        return

    random_audio = random.choice(ON_JOIN_AUDIOS)  # Выбираем случайный файл

    # Если бот еще не находится в новом канале
    if bot_instance.user.id not in [user.id for user in voice_channel.members]:
        vc = member.guild.voice_client
        if vc and vc.is_connected():
            if vc.channel and len(vc.channel.members) > 1:
                return
            await vc.disconnect()
        vc = await voice_channel.connect()
    else:
        if not member.guild.voice_client.is_connected():
            print("иногда случается надо разобраться почему")
            return
        vc = member.guild.voice_client
    audio_path = os.path.join(AUDIO_FOLDER, random_audio)
    vc.play(discord.FFmpegPCMAudio(audio_path))  # Воспроизведение случайного аудиофайла

    while vc.is_playing():
        await asyncio.sleep(1)
