import sys
from typing import Any, Optional

from loguru import logger

from seshat.utils.logger.base_logger import BaseLogger, LogConfig, LogEncoding


class LoguruConfig:
    CONSOLE_FORMAT = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{module}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )

    JSON_FORMAT = (
        "{time:YYYY-MM-DD HH:mm:ss} | " "{level} | " "{module}:{line} | " "{message}"
    )

    @classmethod
    def setup_logger(cls, config: Optional[LogConfig] = None) -> logger:
        logger.remove()
        config = config or LogConfig.default_config()
        is_json = config.format_type == LogEncoding.JSON

        logger.add(
            sys.stdout,
            format=cls.JSON_FORMAT if is_json else cls.CONSOLE_FORMAT,
            level=config.level,
            colorize=not is_json,
            serialize=is_json,
            enqueue=True,
            backtrace=True,
            diagnose=True,
        )
        return logger


class ConsoleLogger(BaseLogger):
    def __init__(self, config: Optional[LogConfig] = None):
        self.config = config or LogConfig.default_config()
        self.logger = LoguruConfig.setup_logger(self.config)

    def debug(self, msg: str, **fields: Any) -> None:
        self.logger.debug(msg, **fields)

    def info(self, msg: str, **fields: Any) -> None:
        self.logger.info(msg, **fields)

    def warn(self, msg: str, **fields: Any) -> None:
        self.logger.warning(msg, **fields)

    def warning(self, msg: str, **fields: Any) -> None:
        self.warn(msg, **fields)

    def error(self, msg: str, **fields: Any) -> None:
        self.logger.error(msg, **fields)

    def fatal(self, msg: str, **fields: Any) -> None:
        self.logger.critical(msg, **fields)

    def sync(self):
        return
