# ----------------------------------------------------------------------------
# Description    : Error check decorator for SCPI calls.
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2025)
# ----------------------------------------------------------------------------

from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, Any, Callable

from qblox_instruments.types import DebugLevel

if TYPE_CHECKING:
    from qblox_instruments.scpi.cfg_man import CfgMan
    from qblox_instruments.scpi.cluster import Cluster


def scpi_error_check(  # noqa: ANN201
    minimal_check: bool | Callable[..., Any | None] = False,
):
    """
    Factory function for a decorator that catches and checks for errors on an SCPI call.

    Parameters
    ----------
    minimal_check
        If True, this decorator will always check for errors unless the debug
        level is ``DebugLevel.NO_CHECK``. By default False.

    Returns
    ----------
    Callable
        The decorator.

    Raises
    ----------
    RuntimeError
        An error was found in system error.
    """

    def decorator(func: Callable[..., Any | None]) -> Callable[..., Any | None]:
        @wraps(func)
        def wrapper(self: Cluster | CfgMan, *args: Any, **kwargs: Any) -> Any | None:
            if self._debug in (DebugLevel.ERROR_CHECK, DebugLevel.VERSION_AND_ERROR_CHECK) or (
                self._debug == DebugLevel.MINIMAL_CHECK and minimal_check is True
            ):
                error = None
                try:
                    return func(self, *args, **kwargs)
                except OSError:
                    raise
                except Exception as err:
                    error = err
                finally:
                    self.check_error_queue(error)

            else:
                return func(self, *args, **kwargs)

        return wrapper

    # if used without parentheses
    if callable(minimal_check):
        return decorator(minimal_check)
    # if used with parentheses
    return decorator
