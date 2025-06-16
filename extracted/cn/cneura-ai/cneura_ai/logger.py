from loguru import logger
import sys

def setup_logger():
    logger.remove()  # Remove the default logger
    logger.add(sys.stdout, level="INFO")
    logger.add("/logs/app.log", level="INFO", rotation="1 week")  # Log rotation

setup_logger()
