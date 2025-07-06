import os
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import logging
import sys
import inspect
import pathlib
from typing import Optional

SUCCESS = 25
logging.addLevelName(SUCCESS, 'SUCCESS')

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[36m',
        'INFO': '\033[35m',
        'SUCCESS': '\033[92m',
        'WARNING': '\033[33m',
        'ERROR': '\033[31m',
        'CRITICAL': '\033[35m',
        'RESET': '\033[0m',
        'NAME': '\033[94m',
    }

    def format(self, record):
        log_message = super().format(record)
        level_color = self.COLORS.get(record.levelname, '')
        name_color = self.COLORS['NAME']
        reset = self.COLORS['RESET']

        parts = log_message.split(' - ', 3)
        if len(parts) >= 4:
            timestamp, name, level, message = parts[0], record.name, parts[2], parts[3]
            level_padded = level.ljust(9)
            name_width = 30
            name_display = name[:name_width-3] + '...' if len(name) > name_width else name.ljust(name_width)
            formatted = f"{level_color}{level_padded}{reset} {name_color}{name_display}{reset} | {message}"
        else:
            formatted = f"{level_color}{log_message}{reset}"

        return formatted

class SuccessLogger(logging.Logger):
    def success(self, msg, *args, **kwargs):
        if self.isEnabledFor(SUCCESS):
            self._log(SUCCESS, msg, args, **kwargs)

logging.setLoggerClass(SuccessLogger)

def setup_logger(name: Optional[str] = None, level: Optional[int] = None) -> SuccessLogger:
    if name is None:
        frame = inspect.currentframe().f_back
        file_path = pathlib.Path(frame.f_globals.get('__file__', 'unknown')).resolve()
        try:
            relative_path = file_path.relative_to(pathlib.Path.cwd())
            name = str(relative_path).replace(os.sep, '.').removesuffix('.py')
        except ValueError:
            name = frame.f_globals.get('__name__', 'unknown')

    noisy_prefixes = (
        "sentence_transformers",
        "transformers",
        "huggingface_hub",
        "urllib3",
        "tqdm",
    )
    for logger_name in list(logging.root.manager.loggerDict.keys()):
        if any(logger_name.startswith(prefix) for prefix in noisy_prefixes):
            lib_logger = logging.getLogger(logger_name)
            lib_logger.setLevel(logging.WARNING)
            lib_logger.handlers.clear()
            lib_logger.propagate = False

    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = ColoredFormatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False

    # Always enforce level if specified
    logger.setLevel(level or logging.INFO)

    return logger