import logging
from typing import Callable

from arpakitlib.ar_base_worker_util import safe_run_worker_in_background, SafeRunInBackgroundModes
from project.core.settings import get_cached_settings
from project.operation_execution.operation_executor_worker import create_operation_executor_worker

_logger = logging.getLogger(__name__)


# API STARTUP EVENTS


async def async_startup_api_event():
    _logger.info("start")

    if get_cached_settings().api_start_operation_executor_worker:
        _ = safe_run_worker_in_background(
            worker=create_operation_executor_worker(),
            mode=SafeRunInBackgroundModes.thread
        )

    _logger.info("finish")


def get_startup_api_events() -> list[Callable]:
    res = [async_startup_api_event]
    return res


# API SHUTDOWN EVENTS


async def async_shutdown_api_event():
    _logger.info("start")
    _logger.info("finish")


def get_shutdown_api_events() -> list[Callable]:
    res = [async_shutdown_api_event]
    return res
