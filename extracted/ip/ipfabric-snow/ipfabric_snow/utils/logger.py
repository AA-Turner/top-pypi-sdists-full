import os
import sys

import dotenv
from loguru import logger


def setup_logging(
    log_level: str = None,
    log_to_file: bool = None,
    log_file_name: str = None,
    log_json: bool = None,
):
    dotenv_path = dotenv.find_dotenv()
    if dotenv_path:
        dotenv.load_dotenv(dotenv_path)
    else:
        logger.warning("No .env file found. Using system environment variables.")

    log_level = log_level or os.getenv("LOG_LEVEL", "INFO").upper()
    log_to_file = (
        log_to_file
        if log_to_file is not None
        else os.getenv("LOG_TO_FILE", "FALSE").upper()
    )
    log_file_name = log_file_name or os.getenv("LOG_FILE_NAME", "log.log")
    log_json = (
        log_json if log_json is not None else os.getenv("LOG_JSON", "FALSE").upper()
    )

    valid_log_levels = [
        "TRACE",
        "DEBUG",
        "INFO",
        "SUCCESS",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ]
    if log_level not in valid_log_levels:
        logger.warning(f"Invalid log level: {log_level}. Falling back to INFO.")
        log_level = "INFO"

    root_dir = os.path.dirname(os.path.abspath(__file__))
    default_log_dir = os.path.join(root_dir, "../..", "logs")
    os.makedirs(default_log_dir, exist_ok=True)
    log_file_path = os.path.join(default_log_dir, log_file_name)

    logger.remove()
    logger.add(sys.stderr, level=log_level)

    if log_to_file:
        logger.add(
            log_file_path,
            level=log_level,
            rotation="00:00",
            retention="7 days",
            serialize=log_json,
        )
    return logger


ipf_logger = setup_logging()
