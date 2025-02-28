from bot.bot import bot_instance
from bot.config import TOKEN
from bot.connection_check import check_connection


def main():
    if not check_connection():
        print("Connection to discord failed.")
        return
    bot_instance.run(TOKEN)


if __name__ == '__main__':
    main()
