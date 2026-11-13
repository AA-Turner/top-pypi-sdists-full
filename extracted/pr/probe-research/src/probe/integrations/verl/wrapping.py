"""What every wrap Probe puts on a verl class shares (`live.py`, `tool_loop/`): the mark that stops a second install
from wrapping again, the fail-open guard, and the import watch's install hook."""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any

logger = logging.getLogger(__name__)

#: Marks a method Probe wrapped, so a second install never wraps it again.
WRAP_MARK = "__probe_verl__"


def is_wrapped(method: Any) -> bool:
    return bool(getattr(method, WRAP_MARK, False))


def set_wrapped(cls: type, name: str, wrapped: Any) -> None:
    """``wrapped`` marked and set on ``cls`` as ``name``."""
    setattr(wrapped, WRAP_MARK, True)
    setattr(cls, name, wrapped)


def guard(call: Callable[..., Any], *args: Any) -> Any:
    """``call(*args)``, or None when it raises: fail open, verl runs on unrecorded."""
    try:
        return call(*args)
    except Exception as exc:  # noqa: BLE001 -- fail open
        logger.debug("probe: verl %s was not recorded (%s: %s)", _get_name(call), type(exc).__name__, exc)
        return None


async def guard_async(call: Callable[..., Any], *args: Any) -> Any:
    """``await call(*args)``, or None when it raises."""
    try:
        return await call(*args)
    except Exception as exc:  # noqa: BLE001 -- fail open
        logger.debug("probe: verl %s was not recorded (%s: %s)", _get_name(call), type(exc).__name__, exc)
        return None


def make_install(class_name: str, wrap: Callable[[type], bool]) -> Callable[[Any], None]:
    """The import watch's hook: ``wrap`` the module's ``class_name`` once the module has run."""

    def install(module: Any) -> None:
        cls = getattr(module, class_name, None)
        if isinstance(cls, type):
            wrap(cls)

    return install


def _get_name(call: Any) -> str:
    return str(getattr(call, "__qualname__", None) or getattr(call, "__name__", None) or type(call).__name__)
