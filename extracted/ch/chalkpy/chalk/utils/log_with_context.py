"""
Adds thread-local context to a Python logger. Taken from neocrym/log-with-context
"""

from __future__ import annotations

import collections.abc
import contextlib
import contextvars
import functools
import logging
import logging.config
import sys
import threading
import types
from enum import Enum
from typing import Any, Dict, Mapping, Optional
from weakref import WeakKeyDictionary

from chalk.utils.missing_dependency import missing_dependency_exception

_LOGGING_CONTEXT: contextvars.ContextVar[Mapping[str, Any]] = contextvars.ContextVar("_LOGGING_CONTEXT", default={})


def _recursive_merge(a: Mapping[str, Any], b: Mapping[str, Any]):
    ans: Dict[str, Any] = {**a}
    for k, v in b.items():
        if k not in ans or not (isinstance(ans[k], collections.abc.Mapping) and isinstance(v, collections.abc.Mapping)):
            ans[k] = v
            continue
        ans[k] = _recursive_merge(ans[k], v)
    return ans


def get_logging_context() -> Mapping[str, Any]:
    """
    Retrieve the log context for the current python context.
    This initializes the thread-local variable if necessary.
    """
    return _LOGGING_CONTEXT.get({})


class LogWithContextFilter(logging.Filter):
    """Filter to append the ``extras`` onto the LogRecord."""

    def filter(self, record: logging.LogRecord) -> bool:
        items = get_logging_context().items()
        for k, v in items:
            if not hasattr(record, k):
                setattr(record, k, v)
        return True


filtered_loggers = WeakKeyDictionary()


def get_logger(name: Optional[str]):
    logger = logging.getLogger(name)
    if logger not in filtered_loggers:
        logger.addFilter(LogWithContextFilter())
        filtered_loggers[logger] = True
    return logger


# Backwards compatibility
Logger = get_logger

_logger = get_logger(__name__)


@contextlib.contextmanager
def add_logging_context(*, _merge: bool = True, **log_context: Any):
    """A context manager to push and pop `extra` dictionary keys.

    Parameters
    ----------
    _merge
        Whether to merge the new context with the existing log context.
    extra
        Contextual information to add to the log record
    """
    if _merge:
        log_context = _recursive_merge(
            _LOGGING_CONTEXT.get({}),
            log_context,
        )
    token = _LOGGING_CONTEXT.set(log_context)
    try:
        yield
    finally:
        _LOGGING_CONTEXT.reset(token)


_PUBLIC_LOGGERS_WITH_FILTER: set[str] = set()


class _PublicLoggingFilter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        record.is_public = True
        return True


def get_public_logger(name: str):
    name += ".public"
    logger = get_logger(name)
    if name not in _PUBLIC_LOGGERS_WITH_FILTER:
        _PUBLIC_LOGGERS_WITH_FILTER.add(name)
        logger.addFilter(_PublicLoggingFilter())
    return logger


OPERATION_KEY = "operation"
LABELS_KEY = "labels"
_OPERATION_ID_KEY = "operation_id"
_OPERATION_PRODUCER = "operation_producer"
_OPERATION_IS_FIRST = "operation_is_first"
_OPERATION_IS_LAST = "operation_is_last"


def get_operation_log_context(
    operation_id: str,
    operation_kind: str | Enum,
    resolver_fqn: str | None = None,
    query_name: str | None = None,
    correlation_id: str | None = None,
):
    """
    Parameters
    ----------
    operation_id
        Internal correlation id.
    operation_kind
        Operation kind or producer name.
    resolver_fqn
        Resolver FQN associated with this operation, if available.
    query_name
        Customer-provided query name.
    correlation_id
        Customer-provided correlation id.

    Returns
    -------
    dict[str, Any]
        Structured logging context for operation-scoped logs.
    """
    if isinstance(operation_kind, Enum):
        operation_kind = operation_kind.value
    ctx: dict[str, Any] = {
        _OPERATION_ID_KEY: operation_id,
        _OPERATION_PRODUCER: operation_kind,
        LABELS_KEY: {},
    }
    if resolver_fqn is not None:
        ctx[LABELS_KEY]["resolver_fqn"] = resolver_fqn
    if query_name is not None:
        ctx[LABELS_KEY]["query_name"] = query_name
    if correlation_id is not None:
        ctx["correlation_id"] = correlation_id
    return ctx


IS_FIRST_OPERATION_CTX = {_OPERATION_IS_FIRST: True}
IS_LAST_OPERATION_CTX = {_OPERATION_IS_LAST: True}


@functools.lru_cache(None)
def get_json_logging_formatter(structured_exceptions: bool = False) -> logging.Formatter:
    """Returns a JSON log formatter.

    With ``structured_exceptions=False``, a record's formatted exception is appended
    to the ``message`` field, as ``logging.Formatter`` would. With
    ``structured_exceptions=True``, ``message`` stays the one-line summary and the
    exception instead ships as dedicated ``stacktrace``, ``exception_type``, and
    ``exception_message`` fields.
    """
    try:
        from pythonjsonlogger import json
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")

    class ChalkJsonFormatter(json.JsonFormatter):
        def __init__(self, structured_exceptions: bool):
            super().__init__(
                reserved_attrs=[
                    "args",
                    "msg",
                    "levelno",
                    "filename",
                    "msecs",
                    "relativeCreated",
                    "module",
                    "exc_info",
                    "stack_info",
                ],
            )
            self._structured_exceptions = structured_exceptions
            try:
                import google.cloud.client

                client = google.cloud.client.ClientWithProject()
            except:
                # Likely no credentials available
                self._gcp_project_name = None
            else:
                self._gcp_project_name = client.project

        def add_fields(self, log_record: Dict[str, Any], record: logging.LogRecord, message_dict: Dict[str, Any]):
            if self._structured_exceptions and "exc_info" in message_dict:
                # Renaming the key here keeps process_log_record's append-to-message
                # branch from ever seeing "exc_info", without mutating the record
                # (which other handlers may still format with inline tracebacks).
                message_dict = dict(message_dict)
                message_dict["stacktrace"] = message_dict.pop("exc_info")
                exc = record.exc_info[1] if isinstance(record.exc_info, tuple) else None
                if exc is not None:
                    cls = type(exc)
                    message_dict["exception_type"] = (
                        cls.__qualname__ if cls.__module__ == "builtins" else f"{cls.__module__}.{cls.__qualname__}"
                    )
                    message_dict["exception_message"] = str(exc)
            super().add_fields(log_record, record, message_dict)

        def process_log_record(self, log_record: Dict[str, Any]):
            # We want to duplicate some fields, so it will show up nicely for google structured logging
            log_record.update(get_logging_context())
            log_record["severity"] = log_record["levelname"]
            if "exc_info" in log_record:
                log_record["message"] = log_record.get("message", "") + "\n" + log_record["exc_info"]
                del log_record["exc_info"]
            source_location = {
                "file": log_record["pathname"],
                "line": str(log_record["lineno"]),
            }
            if len(log_record.get("message", "")) > 1024 * 250:
                # Datadog truncates log messages at 256KB
                # see https://docs.datadoghq.com/agent/logs/log_transport/?tab=https#https-transport
                log_record["message"] = log_record["message"] + "... (log message truncated due to size)"
            if log_record.get("funcName") is not None:
                source_location["function"] = log_record["funcName"]
            log_record["logging.googleapis.com/sourceLocation"] = source_location
            operation = {}
            if (operation_id := log_record.get(_OPERATION_ID_KEY)) is not None:
                operation["id"] = operation_id
            if (operation_producer := log_record.get(_OPERATION_PRODUCER)) is not None:
                operation["producer"] = operation_producer
            if (operation_is_first := log_record.get(_OPERATION_IS_FIRST, None)) is not None:
                operation["first"] = operation_is_first
            if (operation_is_last := log_record.get(_OPERATION_IS_LAST, None)) is not None:
                operation["last"] = operation_is_last
            if operation:
                log_record["logging.googleapis.com/operation"] = operation
            log_record["logging.googleapis.com/labels"] = log_record.get(LABELS_KEY, {})
            log_record["timestampSeconds"] = int(log_record["created"])
            log_record["timestampNanos"] = int((log_record["created"] - int(log_record["created"])) * 1e9)
            log_record = {k: v for (k, v) in log_record.items() if v is not None}
            return log_record

    return ChalkJsonFormatter(structured_exceptions)


def _threading_excepthook(args: threading.ExceptHookArgs):
    typ = args.exc_type
    value = args.exc_value
    traceback = args.exc_traceback
    thread = args.thread
    if typ is not None and value is not None:  # pyright: ignore[reportUnnecessaryComparison]
        try:
            _logger.error(
                f"Unhandled root exception in thread{'' if thread is None else f' {thread.ident} ({thread.getName()})'}",
                exc_info=(typ, value, traceback),
            )
        except:
            # Call the original excepthook in case of error
            # This function exists even though pyright doesn't know about it
            # See https://docs.python.org/3/library/threading.html#threading.__excepthook__
            threading.__excepthook__(args)  # pyright: ignore
    return True


def _sys_excepthook(
    typ: type[BaseException] | None = None,
    value: BaseException | None = None,
    traceback: types.TracebackType | None = None,
):
    if typ is not None and value is not None:
        try:
            _logger.error(
                "Unhandled root exception",
                exc_info=(typ, value, traceback),
            )
        except:
            # Call the original excepthook in case of error
            sys.__excepthook__(typ, value, traceback)
    return True


def configure_logging(logging_config: dict[str, Any]):
    logging.config.dictConfig(logging_config)
    logging.captureWarnings(True)
    _logger.info(f"Configured logging with config: `{logging_config}`")
    # If we are using structured logging, then route unhandled exceptions through the logger so they will be json-formatted
    sys.excepthook = _sys_excepthook
    threading.excepthook = _threading_excepthook
