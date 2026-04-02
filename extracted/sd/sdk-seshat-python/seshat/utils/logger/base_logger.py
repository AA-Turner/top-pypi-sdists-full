from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    FATAL = "CRITICAL"


class LogEncoding(StrEnum):
    CONSOLE = "console"
    JSON = "json"


@dataclass
class LogConfig:
    level: LogLevel = LogLevel.INFO
    format_type: LogEncoding = LogEncoding.CONSOLE

    @classmethod
    def default_config(cls) -> "LogConfig":
        return cls()


class BaseLogger(ABC):
    @abstractmethod
    def debug(self, msg: str, **fields: Any) -> None:
        pass

    @abstractmethod
    def info(self, msg: str, **fields: Any) -> None:
        pass

    @abstractmethod
    def warn(self, msg: str, **fields: Any) -> None:
        pass

    @abstractmethod
    def warning(self, msg: str, **fields: Any) -> None:
        pass

    @abstractmethod
    def error(self, msg: str, **fields: Any) -> None:
        pass

    @abstractmethod
    def fatal(self, msg: str, **fields: Any) -> None:
        pass

    def sync(self):
        pass
