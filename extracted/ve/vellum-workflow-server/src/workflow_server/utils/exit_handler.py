import logging
import multiprocessing
import signal
from typing import Any

logger = logging.getLogger(__name__)
process_killed_switch = multiprocessing.Event()


def gunicorn_exit_handler(_worker: Any) -> None:
    process_killed_switch.set()
    logger.warning("Received gunicorn kill signal")


def exit_handler(_signal: int, _frame: Any) -> None:
    """
    Gunicorn overrides this signal handler but theres periods where the gunicorn server
    hasn't initialized or for local dev where this will get called.
    """
    process_killed_switch.set()
    logger.warning("Received kill signal")
    exit(1)


def init_signal_handlers() -> None:
    signal.signal(signal.SIGTERM, exit_handler)
    signal.signal(signal.SIGINT, exit_handler)
