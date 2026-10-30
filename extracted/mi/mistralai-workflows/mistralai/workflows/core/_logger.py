"""SDK module loggers that leave a host's logging alone until the process configures structlog.

Kept apart from ``core/logging.py`` (which sets logging up) because modules imported by
``core/logging.py`` log through this one.
"""

import logging
from typing import Any

import structlog
from structlog.typing import EventDict, Processor

# Frames between the SDK caller and ``logging.Logger.<method>`` when calling a structlog stdlib
# ``BoundLogger`` method: ``BoundLogger.<method>``, ``BoundLogger._proxy_to_logger``,
# ``BoundLoggerBase._proxy_to_logger``. ``test_import_logging`` pins it.
_CALLER_STACKLEVEL = 4


def _to_stdlib_call(_logger: Any, _method_name: str, event_dict: EventDict) -> tuple[tuple[str], dict[str, Any]]:
    """Render the event as one text line and let the stdlib logger add the traceback and call site."""
    exc_info = event_dict.pop("exc_info", None) or None
    stack_info = bool(event_dict.pop("stack_info", False))
    message = " ".join([str(event_dict.pop("event", "")), *(f"{key}={value}" for key, value in event_dict.items())])
    return (message,), {"exc_info": exc_info, "stack_info": stack_info, "stacklevel": _CALLER_STACKLEVEL}


_UNCONFIGURED_PROCESSORS: list[Processor] = [
    structlog.stdlib.filter_by_level,
    structlog.contextvars.merge_contextvars,
    structlog.stdlib.PositionalArgumentsFormatter(),
    _to_stdlib_call,
]


class _SDKLogger:
    """Module logger for SDK code that does not depend on structlog's process-wide defaults.

    Once the process has configured structlog (``setup_logging``, the host or a framework), events
    follow that configuration, as with ``structlog.get_logger``. Until then they go to the stdlib
    logger of the same name as text, so the host's handlers and levels decide what is shown and a
    process without logging set up only sees warnings and errors, on stderr.
    """

    def __init__(self, name: str, context: dict[str, Any] | None = None) -> None:
        self._name = name
        self._context = context or {}
        self._configured_logger = structlog.get_logger(name)

    def _target(self) -> Any:
        if structlog.is_configured():
            return self._configured_logger.bind(**self._context) if self._context else self._configured_logger
        return structlog.wrap_logger(
            logging.getLogger(self._name),
            processors=_UNCONFIGURED_PROCESSORS,
            wrapper_class=structlog.stdlib.BoundLogger,
            context_class=dict,
        ).bind(**self._context)

    def bind(self, **new_values: Any) -> "_SDKLogger":
        return _SDKLogger(self._name, {**self._context, **new_values})

    def __getattr__(self, attribute: str) -> Any:
        if attribute.startswith("_"):
            # Private lookups (copy, pickle, half-built instances) must not reach the target.
            raise AttributeError(attribute)
        return getattr(self._target(), attribute)


def get_logger(name: str) -> Any:
    return _SDKLogger(name)
