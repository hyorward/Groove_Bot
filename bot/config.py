import os

from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

VOL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'False', 'simulate': 'True', 'key': 'FFmpegExtractAudio'}
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 - reconnect_streamed 1 - reconnect_delay_max 5', 'options': '-vn'
}

TOKEN = os.environ['DISCORD_TOKEN']
PRAYER_API_URL = 'http://api.aladhan.com/v1/timingsByCity'
AUDIO_FOLDER = 'Sounds'
USING_OPUS = False
OPUS_PATH = "/opt/homebrew/Cellar/opus/1.5.2/lib/libopus.dylib"

PRAYERS_NAMES = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]

SOUNDPAD_1 = {
    "Down syndrome": 15,
    "Blin, na..": 16,
    "Bruh": 17,
    "Kazakhstan bomb": 18,
    "I'm a muslim": 19,
    "To be continued..": 20,
    "No": 22,
    "Let's go..": 23,
    "Good night": 24,
    "KurbanHaji": 25,
    "I'm a Dagestan": 26,
    "The earth is round": 27,
    "Do the tining": 28,
    "I'm a georgian": 29,
    "Avaretc...!": 32,
    "Sheep came home": 33,
    "Autumn": 35,
    "Don't write here anymore": 36,
    "Once you live...": 37,
    "Working!": 39,
    "What a luxury!": 40,
    "Hello": 42,
    "How do you tell with me?": 43,
    "Assalamu Aleykum": 44,
    "Laugh": 45
}

SOUNDPAD_2 = {
    "(Geralt) Not proven yet...": 47,
    "(Geralt) Motivation": 48,
    "(Hermaeus) Superman": 49
}

SOUNDPAD_NAMES = {
    "Abdurashid": 2,
    "Arthur": 3,
    "Burgers": 4,
    "Ibrahim": 5,
    "Ibrahim Chort": 14,
    "Khanchik": 46,
    "Murad": 10
}
