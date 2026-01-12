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

# Глобальные переменные для контроля
voice_lock = asyncio.Lock()
last_greet_time = 0  # Время последнего приветствия (глобально)
GREET_COOLDOWN = 15  # Секунд между приветствиями


@bot_instance.event
async def on_ready():
    await bot_instance.tree.sync()
    check_prayer_times.start()
    print("Бот запущен.")


async def leave(member, before_voice_state: VoiceState):
    """Выходит из канала если там остался только бот"""
    members = before_voice_state.channel.members
    if (len(members) == 1) and (members[0].id == bot_instance.user.id):
        vc = member.guild.voice_client
        if vc:
            await vc.disconnect()


async def connect_and_play(guild, voice_channel):
    """Подключается к каналу и воспроизводит приветствие"""
    global last_greet_time
    
    # Проверяем cooldown
    now = time.time()
    if now - last_greet_time < GREET_COOLDOWN:
        print(f"Cooldown активен, осталось {GREET_COOLDOWN - (now - last_greet_time):.1f}с")
        return
    
    async with voice_lock:
        try:
            last_greet_time = time.time()
            
            # Проверяем текущее подключение
            vc = guild.voice_client
            
            if vc:
                if vc.is_connected() and vc.channel.id == voice_channel.id:
                    # Уже в нужном канале - просто играем
                    pass
                else:
                    # В другом канале или отключён - отключаемся
                    await vc.disconnect()
                    await asyncio.sleep(1)
                    vc = None
            
            # Подключаемся если нужно
            if vc is None:
                print(f"Подключаюсь к каналу {voice_channel.name}")
                vc = await voice_channel.connect(timeout=60.0, self_deaf=True)
                # Важно: ждём пока соединение стабилизируется
                await asyncio.sleep(3)
            
            # Проверяем что подключились
            if not vc or not vc.is_connected():
                print("Не удалось подключиться")
                return
            
            # Воспроизводим звук
            random_audio = random.choice(ON_JOIN_AUDIOS)
            audio_path = os.path.join(AUDIO_FOLDER, random_audio)
            
            if not os.path.exists(audio_path):
                print(f"Файл не найден: {audio_path}")
                return
            
            print(f"Воспроизвожу {random_audio}")
            vc.play(discord.FFmpegPCMAudio(audio_path, executable=FFMPEG_PATH))
            
            # Ждём окончания воспроизведения
            while vc.is_playing():
                await asyncio.sleep(0.5)
            
            print("Воспроизведение завершено")
            
        except Exception as e:
            print(f"Ошибка в connect_and_play: {e}")


async def meow(member, voice_channel):
    """Воспроизводит мяу"""
    async with voice_lock:
        try:
            vc = member.guild.voice_client
            if vc is None or not vc.is_connected():
                return
            
            audio_path = os.path.join(AUDIO_FOLDER, "meow.mp3")
            if not os.path.exists(audio_path):
                return
                
            vc.play(discord.FFmpegPCMAudio(audio_path, executable=FFMPEG_PATH))
            
            while vc.is_playing():
                await asyncio.sleep(0.5)
        except Exception as e:
            print(f"Ошибка в meow: {e}")


def _get_muted_members(bot_id, voice_state: VoiceState):
    return [
        (member.voice.mute or member.voice.self_mute) 
        for member in voice_state.channel.members 
        if member.id != bot_id
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
    # Игнорируем события от самого бота
    if member.id == bot_instance.user.id:
        return
    
    # Проверка на mute всех - воспроизводим мяу
    if (
        all((after.channel, before.channel))
        and all(_get_muted_members(bot_instance.user.id, after))
        and muted_right_now(before, after)
        and throttle_meow()
    ):
        await asyncio.sleep(5)
        await meow(member, after.channel)
        return
    
    # Если канал не изменился - выходим
    if before.channel == after.channel:
        return
    
    # Если пользователь вышел из канала
    if not after.channel and before.channel:
        await leave(member, before)
        return
    
    # Если пользователь зашёл в канал
    if after.channel:
        # Небольшая задержка чтобы избежать race condition
        await asyncio.sleep(0.5)
        await connect_and_play(member.guild, after.channel)
