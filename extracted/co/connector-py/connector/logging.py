import datetime
import logging
from pathlib import Path

from connector.config import config
from connector.handlers.lumos_log_handler import LumosLogHandler

logger = logging.getLogger(__name__)

LOG_FORMAT = "%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s"


def set_logger_config(app_id: str):
    log_directory = config.log_directory
    log_level = config.log_level

    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    if config.log_to_stdout:
        logging.basicConfig(
            format=LOG_FORMAT,
            datefmt="%H:%M:%S",
            level=log_level.value,
            force=True,
        )

    elif log_directory:
        log_directory.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            filename=str(log_directory / f"{app_id}_{timestamp}.log"),
            filemode="a",
            format=LOG_FORMAT,
            datefmt="%H:%M:%S",
            level=log_level.value,
            force=True,
        )
    else:
        log_directory = Path.cwd() / "logs"
        log_directory.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            filename=str(log_directory / f"{app_id}_{timestamp}.log"),
            format=LOG_FORMAT,
            datefmt="%H:%M:%S",
            level=log_level.value,
            force=True,
        )

    # Add Lumos log handler if enabled
    if config.send_logs_to_on_prem_proxy and config.agent_identifier is not None:
        lumos_handler = LumosLogHandler()
        lumos_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt="%H:%M:%S"))
        logging.getLogger().addHandler(lumos_handler)
