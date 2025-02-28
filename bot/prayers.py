import asyncio
import os
from datetime import datetime

import discord
import pytz
import requests
from discord import ChannelType
from discord.ext import tasks

from bot import config
from bot.bot import bot_instance
from bot.config import AUDIO_FOLDER


@tasks.loop(minutes=1)
async def check_prayer_times():
    now = datetime.now(pytz.timezone('Europe/Moscow'))
    current_time = now.strftime('%H:%M')
    response = requests.get('http://api.aladhan.com/v1/timingsByCity', params={"city": "Makhachkala", "country": "Russia"})
    all_timings = dict(response.json()['data']['timings'])
    timings = {timing: all_timings[timing] for timing in all_timings if timing in config.PRAYERS_NAMES}
    if current_time not in timings.values():
        return
    for channel in bot_instance.get_all_channels():
        if (channel.type.value == ChannelType.voice.value) and (len(channel.members) > 0):
            vc = await channel.connect()
            audio_path = os.path.join(AUDIO_FOLDER, 'azan.mp3')

            async def _disconnect():
                await bot_instance.disconnect()

            vc.play(
                discord.FFmpegPCMAudio(audio_path),
                after=_disconnect
            )
