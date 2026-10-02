import logging
import os


# https://docs.datadoghq.com/agent/troubleshooting/debug_mode/?tab=agentv6v7#agent-log-level
logging.addLevelName(5, "TRACE")
logging.addLevelName(logging.WARNING, "WARN")
logging.addLevelName(100, "OFF")

try:
    # Added in version 3.11
    level_mapping = logging.getLevelNamesMapping()
except AttributeError:
    level_mapping = {name: num for num, name in logging._levelToName.items()}


def initialize_logging(name):
    logger = logging.getLogger(name)

    str_level = (os.environ.get("DD_LOG_LEVEL", "INFO")).upper()
    level = level_mapping.get(str_level)

    if level is None:
        logger.setLevel(logging.INFO)
        logger.warning("Invalid log level: %s Defaulting to INFO", str_level)
    else:
        logger.setLevel(level)

    log_format = "%(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s"
    log_formatter = logging.Formatter(log_format)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)

    logger.addHandler(console_handler)
