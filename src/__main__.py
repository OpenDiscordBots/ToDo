from dotenv import load_dotenv
from os import environ as env

from libodb import APIClient

from src.bot import Bot

load_dotenv()


def main() -> None:
    bot = Bot(APIClient(env["API_TOKEN"], kv_ns="todo"), command_prefix="td!")
    bot.load_extensions([
        "src.exts.ping",
        "src.exts.todo",
    ])

    bot.run(env["TOKEN"])


if __name__ == "__main__":
    main()
