import logging
import os

def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger that writes to both console and a rotating log file.
    Log file is stored in the same directory as this file.
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    log_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(log_dir, "..", "server.log")
    log_path = os.path.normpath(log_path)

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s  %(levelname)-8s  %(name)s  —  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(
        "%(levelname)-8s  %(message)s"
    ))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger