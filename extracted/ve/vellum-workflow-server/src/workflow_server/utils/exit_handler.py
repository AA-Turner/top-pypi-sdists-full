from datetime import datetime
import logging
import multiprocessing
import signal
from time import sleep
from typing import Any

from workflow_server.config import IS_ASYNC_MODE, is_development
from workflow_server.utils.system_utils import get_active_process_count

logger = logging.getLogger(__name__)
process_killed_switch = multiprocessing.Event()


def _wait_for_workers() -> None:
    # Would be annoying to have this on for dev since would prevent reload restarts. Also disabling this
    # for non async mode for now since it shouldn't be needed anyway cus we keep the requests open.
    if is_development() and not IS_ASYNC_MODE:
        return

    start_time = datetime.now()
    loops = 0

    while get_active_process_count() > 0:
        if loops % 30 == 0:
            logger.info("Waiting for workflow processes to finish...")

        # TODO needa pass in max workflow time here for VPC
        if (datetime.now() - start_time).total_seconds() > 1800:
            logger.warning("Max elapsed time waiting for workflow processes to complete exceeded, shutting down")
            exit(1)

        sleep(1)
        loops += 1


def gunicorn_exit_handler(_worker: Any) -> None:
    logger.info("Received gunicorn kill signal")
    process_killed_switch.set()
    _wait_for_workers()


def exit_handler(_signal: int, _frame: Any) -> None:
    """
    Gunicorn overrides this signal handler but theres periods where the gunicorn server
    hasn't initialized or for local dev where this will get called.
    """
    process_killed_switch.set()
    logger.warning("Received kill signal")
    _wait_for_workers()
    exit(1)


def init_signal_handlers() -> None:
    signal.signal(signal.SIGTERM, exit_handler)
    signal.signal(signal.SIGINT, exit_handler)
