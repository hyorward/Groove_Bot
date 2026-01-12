import aiohttp
from discord import Intents, opus
from discord.ext import commands

from bot import config

intents = Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True  # Нужен для проверки участников канала
intents.guilds = True

# Настройка SOCKS5 прокси для обхода блокировок Discord voice
PROXY_URL = "socks5://127.0.0.1:10808"

connector = aiohttp.TCPConnector(limit=100)
bot_instance = commands.Bot(
    command_prefix='/',
    intents=intents,
    proxy=PROXY_URL
)

if config.USING_OPUS:
    opus.load_opus(config.OPUS_PATH)
