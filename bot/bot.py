from discord import Intents
from discord.ext import commands

intents = Intents.default()
intents.message_content = True
intents.voice_states = True  # Обработка голосовых состояний

bot_instance = commands.Bot(command_prefix='/', intents=intents)
