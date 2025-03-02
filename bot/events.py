import asyncio
import os
import random
import time

import discord
from discord import VoiceState, VoiceClient

from bot.bot import bot_instance
from bot.config import AUDIO_FOLDER
from bot.prayers import check_prayer_times

ON_JOIN_AUDIOS = ['salam.mp3', 'bratishka.mp3']
last_time_played_meow = None


@bot_instance.event
async def on_ready():
    await bot_instance.tree.sync()
    check_prayer_times.start()
    print("Бот запущен.")


async def leave(member, before_voice_state: VoiceState):
    members = before_voice_state.channel.members
    if (len(members) == 1) and (members[0].id == bot_instance.user.id):
        await member.guild.voice_client.disconnect()


async def _get_voice_client(member, voice_channel) -> VoiceClient | None:
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
    return vc


async def greetings(member, voice_channel):
    voice_client = await _get_voice_client(member, voice_channel)
    random_audio = random.choice(ON_JOIN_AUDIOS)  # Выбираем случайный файл

    audio_path = os.path.join(AUDIO_FOLDER, random_audio)
    voice_client.play(
        discord.FFmpegPCMAudio(audio_path))  # Воспроизведение случайного аудиофайла

    while voice_client.is_playing():
        await asyncio.sleep(1)


async def meow(member, voice_channel):
    voice_client = await _get_voice_client(member, voice_channel)

    audio_path = os.path.join(AUDIO_FOLDER, "meow.mp3")
    voice_client.play(discord.FFmpegPCMAudio(audio_path))

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
            all((after, before))
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
