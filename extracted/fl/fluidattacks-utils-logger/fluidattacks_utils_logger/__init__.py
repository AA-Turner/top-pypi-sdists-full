import sys

from fa_purity import (
    Cmd,
)

from . import (
    handlers,
    logger,
)
from .env import (
    current_app_env,
)
from .levels import (
    LoggingLvl,
)

__version__ = "3.0.0"


def set_main_log(
    name: str,
    conf: handlers.LoggingConf,
    debug: bool,
) -> Cmd[None]:
    _log_handler = handlers.logger_handler(conf, sys.stderr)
    _handlers = (_log_handler,)
    env = current_app_env()
    display_env = logger.get_logger(name).bind(
        lambda log: env.bind(lambda e: log.info("%s@%s", (name, e.value))),  # noqa: PLE1206
    )
    return (
        logger.set_logger(name, LoggingLvl.DEBUG if debug else LoggingLvl.INFO, _handlers)
        + display_env
    )
