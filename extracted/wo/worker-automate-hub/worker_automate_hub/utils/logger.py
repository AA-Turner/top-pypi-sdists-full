import logging
import os
from pathlib import Path

from worker_automate_hub.config.settings import LOG_LEVEL


def setup_logger(name, log_file, level=logging.INFO):
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


current_dir = Path.cwd()
log_file_path = current_dir / "logs"
if not os.path.exists(log_file_path):
    os.makedirs(log_file_path)

logger = setup_logger("main_logger", f"{log_file_path}/app.log", int(LOG_LEVEL))
