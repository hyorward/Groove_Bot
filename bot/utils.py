import os

from bot.config import AUDIO_FOLDER


def get_audio_path(file_name):
    return os.path.join(AUDIO_FOLDER, f'{file_name}.mp3')
