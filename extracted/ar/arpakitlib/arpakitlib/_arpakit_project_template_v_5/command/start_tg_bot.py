from project.core.util import setup_logging
from project.tg_bot.start_tg_bot import start_tg_bot


def __command():
    setup_logging()
    start_tg_bot()


if __name__ == '__main__':
    __command()
