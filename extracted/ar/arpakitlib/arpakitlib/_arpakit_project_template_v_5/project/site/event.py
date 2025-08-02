import logging

_logger = logging.getLogger(__name__)


# STARTUP SITE EVENTS


async def async_site_startup_event():
    _logger.info("start")
    _logger.info("finish")


# SHUTDOWN SITE EVENTS


async def async_site_shutdown_event():
    _logger.info("start")
    _logger.info("finish")
