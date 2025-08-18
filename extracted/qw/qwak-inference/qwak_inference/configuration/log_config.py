import logging.config
import os
import sys

from qwak_inference.authentication.constants import FROGML_DIR_PATH

log_level = (
    "DEBUG"
    if os.getenv("JFML_DEBUG", "false").casefold() == "true".casefold()
    else "INFO"
)
os.makedirs(FROGML_DIR_PATH, exist_ok=True)
log_file: str = os.path.join(FROGML_DIR_PATH, "frogml-log-history.log")

DEFAULT_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
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
