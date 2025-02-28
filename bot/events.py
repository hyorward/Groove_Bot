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
async def on_voice_state_update(_, before_voice_state: VoiceState, after_voice_state: VoiceState):
    if not (after_voice_state.channel and not before_voice_state.channel):  # Если пользователь зашел в голосовой канал
        return
    voice_channel = after_voice_state.channel
    if not voice_channel:  # Проверка на существование канала
        return

    random_audio = random.choice(ON_JOIN_AUDIOS)  # Выбираем случайный файл
    vc = await voice_channel.connect()
    audio_path = os.path.join(AUDIO_FOLDER, random_audio)
    vc.play(discord.FFmpegPCMAudio(audio_path))  # Воспроизведение случайного аудиофайла

    while vc.is_playing():
        await asyncio.sleep(1)

    await vc.disconnect()
