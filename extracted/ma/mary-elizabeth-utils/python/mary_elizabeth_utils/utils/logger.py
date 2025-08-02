import logging
from logging import LogRecord
from typing import ClassVar

from colorama import Back, Fore, Style, init

# Initialize colorama
init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    COLORS: ClassVar[dict[str, str]] = {
        "DEBUG": Fore.CYAN,
        "INFO": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "CRITICAL": Fore.RED + Back.WHITE + Style.BRIGHT,
    }

    def format(self, record: LogRecord) -> str:
        log_message = super().format(record)
        return f"{self.COLORS.get(record.levelname, '')}{log_message}{Style.RESET_ALL}"


def setup_colored_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # Create formatter
    formatter = ColoredFormatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Add formatter to ch
    ch.setFormatter(formatter)

    # Add ch to logger
    logger.addHandler(ch)

    return logger
