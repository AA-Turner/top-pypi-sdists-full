"""LoguruAdapter — bridges smplkit logging runtime to loguru (experimental)."""

from __future__ import annotations

import logging as stdlib_logging
from collections.abc import Callable

from loguru import logger as _loguru_logger

from smplkit._debug import debug
from smplkit.logging.adapters.base import LoggingAdapter

# Loguru level name → Python numeric level mapping
_LOGURU_LEVEL_MAP: dict[str, int] = {
    "TRACE": 5,
    "DEBUG": stdlib_logging.DEBUG,
    "INFO": stdlib_logging.INFO,
    "SUCCESS": 25,
    "WARNING": stdlib_logging.WARNING,
    "ERROR": stdlib_logging.ERROR,
    "CRITICAL": stdlib_logging.CRITICAL,
}


class LoguruAdapter(LoggingAdapter):
    """Adapter for the `loguru <https://github.com/Delgan/loguru>`_ library.

    **Experimental** — loguru does not have named loggers or a global registry,
    so full parity with stdlib is limited. Level control works at the
    module-prefix granularity, and named loggers are discovered via
    ``logger.bind()``.

    Args:
        name_field: The key in ``logger.bind(...)`` that represents
            the logger name. Defaults to ``"name"``.
    """

    def __init__(self, *, name_field: str = "name") -> None:
        self._name_field = name_field
        self._original_bind: Callable | None = None
        self._known_names: dict[str, int] = {}
        self._callback: Callable[[str, int | None, int], None] | None = None

    @property
    def name(self) -> str:
        return "loguru"

    def discover(self) -> list[tuple[str, int | None, int]]:
        # Loguru has no registry to scan; discovery happens via install_hook.
        return []

    def apply_level(self, logger_name: str, level: int) -> None:
        if level >= stdlib_logging.CRITICAL:
            debug("adapter", f'loguru: disabling "{logger_name}" (level={level})')
            _loguru_logger.disable(logger_name)
        else:
            debug("adapter", f'loguru: enabling "{logger_name}" (level={level})')
            _loguru_logger.enable(logger_name)

    def install_hook(self, on_new_logger: Callable[[str, int | None, int], None]) -> None:
        if self._original_bind is not None:
            return  # Already patched

        self._callback = on_new_logger
        self._original_bind = _loguru_logger.bind
        original_bind = self._original_bind
        name_field = self._name_field
        known = self._known_names
        callback = self._callback

        def _patched_bind(**kwargs):  # type: ignore[no-untyped-def]
            result = original_bind(**kwargs)
            bound_name = kwargs.get(name_field)
            if bound_name is not None and isinstance(bound_name, str) and bound_name not in known:
                known[bound_name] = stdlib_logging.DEBUG
                # Loguru has no level inheritance; explicit == effective.
                callback(bound_name, stdlib_logging.DEBUG, stdlib_logging.DEBUG)
            return result

        # Use type: ignore because loguru.logger is a special object
        _loguru_logger.bind = _patched_bind  # type: ignore[assignment]

    def uninstall_hook(self) -> None:
        if self._original_bind is not None:
            _loguru_logger.bind = self._original_bind  # type: ignore[assignment]
            self._original_bind = None
            self._callback = None
