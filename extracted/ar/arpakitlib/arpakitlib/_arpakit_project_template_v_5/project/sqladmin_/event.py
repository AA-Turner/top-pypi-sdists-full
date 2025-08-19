import logging
from typing import Callable

from project.core.settings import get_cached_settings
from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db

_logger = logging.getLogger(__name__)


# STARTUP API EVENTS


async def async_sqladmin_startup_event():
    _logger.info("start")

    if (
            get_cached_sqlalchemy_db() is not None
            and get_cached_settings().api_init_sqlalchemy_db
    ):
        get_cached_sqlalchemy_db().init()

    _logger.info("finish")


def get_sqladmin_startup_events() -> list[Callable]:
    res = [async_sqladmin_startup_event]
    return res


# SHUTDOWN API EVENTS


async def async_sqladmin_shutdown_event():
    _logger.info("start")
    _logger.info("finish")


def get_sqladmin_shutdown_events() -> list[Callable]:
    res = [async_sqladmin_shutdown_event]
    return res
