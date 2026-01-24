from enum import Enum, auto
from rich.console import Console


class LoggerError(Exception):
    pass


class Level(Enum):
    DEBUG = auto()
    INFO = auto()
    ERROR = auto()


class Logger:
    def __init__(self, level: Level):
        if level is not None and not isinstance(level, Level):
            raise LoggerError("You must pass a Level as level.")

        if level is not None:
            self.level = level

        self.console = Console()

    def log(self, *logs, sep: str = ''):
        value = sep.join(logs)
        self.console.log(value)
