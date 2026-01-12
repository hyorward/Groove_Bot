import asyncio
import os
import random
import time

import discord
from discord import VoiceState, VoiceClient

from bot.bot import bot_instance
from bot.config import AUDIO_FOLDER, FFMPEG_PATH
from bot.prayers import check_prayer_times

ON_JOIN_AUDIOS = ['salambrat.mp3']
last_time_played_meow = None

# Блокировка для предотвращения одновременных подключений
voice_lock = asyncio.Lock()
# Флаг для отслеживания активного подключения
is_connecting = False


@bot_instance.event
async def on_ready():
    await bot_instance.tree.sync()
    check_prayer_times.start()
    print("Бот запущен.")


async def leave(member, before_voice_state: VoiceState):
    members = before_voice_state.channel.members
    if (len(members) == 1) and (members[0].id == bot_instance.user.id):
        if member.guild.voice_client:
            await member.guild.voice_client.disconnect()


async def _get_voice_client(member, voice_channel) -> VoiceClient | None:
    global is_connecting
    
    # Если уже идёт подключение, пропускаем
    if is_connecting:
        print("Подключение уже в процессе, пропускаем...")
        return None
    
    # Используем блокировку для предотвращения одновременных подключений
    async with voice_lock:
        try:
            is_connecting = True
            
            # Проверяем, может бот уже подключён
            vc = member.guild.voice_client
            if vc and vc.is_connected():
                if vc.channel.id == voice_channel.id:
                    # Уже в этом канале
                    is_connecting = False
                    return vc
                # В другом канале - отключаемся
                await vc.disconnect()
                await asyncio.sleep(1)
            
            # Подключаемся к каналу
            vc = await voice_channel.connect(timeout=60.0, self_deaf=True)
            await asyncio.sleep(2)  # Ждём стабилизации соединения
            
            is_connecting = False
            return vc
        except asyncio.TimeoutError:
            print("Таймаут подключения к голосовому каналу.")
            is_connecting = False
            return None
        except Exception as e:
            print(f"Ошибка подключения к голосовому каналу: {e}")
            is_connecting = False
            return None


async def greetings(member, voice_channel):
    voice_client = await _get_voice_client(member, voice_channel)
    if voice_client is None:
        return
    random_audio = random.choice(ON_JOIN_AUDIOS)  # Выбираем случайный файл

    audio_path = os.path.join(AUDIO_FOLDER, random_audio)
    voice_client.play(
        discord.FFmpegPCMAudio(audio_path, executable=FFMPEG_PATH))  # Воспроизведение случайного аудиофайла

    while voice_client.is_playing():
        await asyncio.sleep(1)


async def meow(member, voice_channel):
    voice_client = await _get_voice_client(member, voice_channel)
    if voice_client is None:
        return

    audio_path = os.path.join(AUDIO_FOLDER, "meow.mp3")
    voice_client.play(discord.FFmpegPCMAudio(audio_path, executable=FFMPEG_PATH))

    while voice_client.is_playing():
        await asyncio.sleep(1)


def _get_muted_members(bot_id, voice_state: VoiceState):
    return [
        (member.voice.mute or member.voice.self_mute) for member in voice_state.channel.members if
        member.id != bot_id
    ]


def muted_right_now(before, after):
    return not (before.self_mute or before.mute) and (after.self_mute or after.mute)


def throttle_meow():
    global last_time_played_meow
    if last_time_played_meow is None:
        last_time_played_meow = time.time()
        return True
    if (time.time() - last_time_played_meow) > 15:
        last_time_played_meow = time.time()
        return True
    return False


@bot_instance.event
async def on_voice_state_update(member, before: VoiceState, after: VoiceState):
    if member.id == bot_instance.user.id:
        return
    if (
            all((after.channel, before.channel))
            and (
                all(_get_muted_members(bot_instance.user.id, after))
                and
                muted_right_now(before, after)
            )
            and throttle_meow()
    ):
        await asyncio.sleep(5)
        await meow(member, after.channel)
        return
    if before.channel == after.channel:
        #  Далее ивенты только для входа/выхода юзера из канала
        return
    if not after.channel and before.channel:  # если все вышли бот тоже выходит
        await leave(member, before)
        return

    if not (
            voice_channel := after.channel):  # Если пользователь не зашел в голосовой канал
        return
    await greetings(member, voice_channel)
