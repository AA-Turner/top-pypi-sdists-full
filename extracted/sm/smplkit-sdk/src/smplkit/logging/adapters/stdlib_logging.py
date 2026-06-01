"""StdlibLoggingAdapter — bridges smplkit logging runtime to Python stdlib logging."""

from __future__ import annotations

import logging as stdlib_logging
from collections.abc import Callable

from smplkit._debug import debug
from smplkit.logging.adapters.base import LoggingAdapter


class StdlibLoggingAdapter(LoggingAdapter):
    """Adapter for Python's built-in :mod:`logging` module.

    Discovers existing loggers, intercepts new logger creation for
    continuous discovery, and applies log levels at runtime.
    """

    def __init__(
        self,
        *,
        prefix: str | None = None,
        discover_existing: bool = True,
    ) -> None:
        self._prefix = prefix
        self._discover_existing = discover_existing
        self._original_getLogger: Callable | None = None
        # Guard set: logger names currently being level-applied by the SDK.
        # Prevents re-reporting a logger as "new" when apply_level() calls
        # getLogger() internally.
        self._applying_level: set[str] = set()

    @property
    def name(self) -> str:
        return "stdlib-logging"

    def discover(self) -> list[tuple[str, int | None, int]]:
        if not self._discover_existing:
            return []
        loggers: list[tuple[str, int | None, int]] = []
        root = stdlib_logging.getLogger()
        if self._prefix is None:
            # Root logger always has an explicit level (WARNING by default).
            loggers.append(("root", root.level if root.level > 0 else None, root.getEffectiveLevel()))
        for name, obj in stdlib_logging.root.manager.loggerDict.items():
            if isinstance(obj, stdlib_logging.Logger):
                if self._prefix is not None and not name.startswith(self._prefix):
                    continue
                explicit = obj.level if obj.level > 0 else None
                loggers.append((name, explicit, obj.getEffectiveLevel()))
        return loggers

    def apply_level(self, logger_name: str, level: int) -> None:
        level_name = stdlib_logging.getLevelName(level)
        debug("adapter", f'applying guard ON for "{logger_name}"')
        self._applying_level.add(logger_name)
        try:
            debug("adapter", f'applying level {level_name} to logger "{logger_name}" via setLevel()')
            stdlib_logging.getLogger(logger_name).setLevel(level)
        finally:
            self._applying_level.discard(logger_name)
            debug("adapter", f'applying guard OFF for "{logger_name}"')

    def install_hook(self, on_new_logger: Callable[[str, int | None, int], None]) -> None:
        if self._original_getLogger is not None:
            return  # Already patched

        debug("discovery", "installing Manager.getLogger monkey-patch")
        self._original_getLogger = stdlib_logging.Manager.getLogger
        original = self._original_getLogger
        prefix = self._prefix
        applying_level = self._applying_level

        def _patched_getLogger(self_mgr, name):  # type: ignore[no-untyped-def]
            is_new = name not in self_mgr.loggerDict
            logger = original(self_mgr, name)  # type: ignore[misc]
            if is_new and isinstance(logger, stdlib_logging.Logger):
                if prefix is None or name.startswith(prefix):
                    if name in applying_level:
                        debug(
                            "discovery",
                            f'suppressed re-reporting for "{name}" (applying guard active)',
                        )
                    else:
                        debug("discovery", f'new logger intercepted via getLogger patch: "{name}"')
                        explicit = logger.level if logger.level > 0 else None
                        on_new_logger(name, explicit, logger.getEffectiveLevel())
            return logger

        stdlib_logging.Manager.getLogger = _patched_getLogger  # type: ignore[assignment]

    def uninstall_hook(self) -> None:
        if self._original_getLogger is not None:
            debug("discovery", "uninstalling Manager.getLogger monkey-patch")
            stdlib_logging.Manager.getLogger = self._original_getLogger  # type: ignore[assignment]
            self._original_getLogger = None
