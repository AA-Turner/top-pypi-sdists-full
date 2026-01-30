import logging.config
import os
import sys

log_level = (
    "DEBUG"
    if os.getenv("JFML_DEBUG", "false").casefold() == "true".casefold()
    else "INFO"
)
log_file = f'{os.path.expanduser("~")}/.frogml/frogml-log-history.log'
os.makedirs(os.path.dirname(log_file), exist_ok=True)

DEFAULT_LOGGING = {
    "version": 1,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(levelname)s - %(name)s.%(module)s.%(funcName)s:%(lineno)d - %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "stream": sys.stdout,
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "standard",
            "filename": log_file,
        },
    },
    "loggers": {
        __name__: {
            "level": log_level,
            "handlers": ["console", "file"],
            "propagate": False,
        },
    },
}

if os.getenv("IS_LOGGER_SHADED") is not None:
    logger = logging.getLogger(__name__)
else:
    logging.config.dictConfig(DEFAULT_LOGGING)
    logger = logging.getLogger(__name__)
