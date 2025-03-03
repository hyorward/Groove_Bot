from discord import Intents, opus
from discord.ext import commands

from bot import config

intents = Intents.default()
intents.message_content = True
intents.voice_states = True  # Обработка голосовых состояний

bot_instance = commands.Bot(command_prefix='/', intents=intents)

if config.USING_OPUS:
    opus.load_opus(config.OPUS_PATH)
