import asyncio
import errno
import logging
import sys

from . import ui
from .commands.command_group import dap
from .dap_error import OperationError


def _display_stacktrace() -> bool:
    logger = logging.getLogger("dap")
    return logger.getEffectiveLevel() == logging.DEBUG


def _get_last_exception(e: BaseException) -> BaseException:
    if isinstance(e, BaseExceptionGroup):
        return _get_last_exception(e.exceptions[-1])
    return e


def _exit_for_exception(e: BaseException) -> None:
    last_exc = _get_last_exception(e)
    if isinstance(last_exc, OperationError):
        sys.exit(errno.EIO)
    elif isinstance(last_exc, NotImplementedError):
        sys.exit(errno.ENOSYS)
    elif isinstance(last_exc, (asyncio.exceptions.CancelledError, KeyboardInterrupt)):
        sys.exit(errno.ECANCELED)
    sys.exit(errno.EIO)


def console_entry() -> None:
    logger = logging.getLogger("dap")

    # handle exceptions for production deployments
    try:
        dap()
    except (OperationError, BaseExceptionGroup) as e:
        ui.error(e.message)
        logger.error(e.message)
        if _display_stacktrace():
            logger.exception(e)
        _exit_for_exception(e)
    except NotImplementedError as e:
        ui.error(e.__str__())
        logger.exception(e, exc_info=_display_stacktrace())
        _exit_for_exception(e)
    except (asyncio.exceptions.CancelledError, KeyboardInterrupt) as e:
        _exit_for_exception(e)
    except Exception as e:
        ui.error(e.__str__())
        logger.exception(e, exc_info=_display_stacktrace())
        _exit_for_exception(e)


if __name__ == "__main__":
    console_entry()
