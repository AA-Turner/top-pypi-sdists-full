"""
Logging utilities using loguru with rich formatting.

Three modes:
    1. Library (default): logger disabled, no sinks — call configure_logging() to enable.
    2. Server/serve: structured timestamped output — call configure_server_logging().
    3. TUI: buffer capture via enable_tui_capture() + install_stdlib_intercept().
"""

import contextlib
import logging
import os
import pathlib
import sys
import threading
import typing as t
from collections import deque
from dataclasses import dataclass
from datetime import datetime

from loguru import logger
from rich.console import Console
from rich.logging import RichHandler
from rich.prompt import Confirm
from rich.theme import Theme

__all__ = [
    "LogBuffer",
    "LogEntry",
    "LogLevel",
    "configure_logging",
    "configure_server_logging",
    "confirm",
    "console",
    "enable_tui_capture",
    "install_stdlib_intercept",
    "log_buffer",
    "logger",
]

LogLevel = t.Literal["trace", "debug", "info", "success", "warning", "error", "critical"]

console = Console(
    highlight=False,
    theme=Theme(
        {
            "logging.level.success": "green",
            "logging.level.trace": "dim blue",
        }
    ),
)

# In vscode jupyter, disable rich's jupyter detection to avoid issues with styling
if "VSCODE_PID" in os.environ:
    console.is_jupyter = False


# ======================================================================
# TUI log capture
# ======================================================================


@dataclass(slots=True)
class LogEntry:
    """A single captured log entry."""

    timestamp: datetime
    level: str
    source: str
    message: str
    level_no: int


class LogBuffer:
    """Thread-safe ring buffer for captured log entries."""

    def __init__(self, maxlen: int = 5000) -> None:
        self._entries: deque[LogEntry] = deque(maxlen=maxlen)
        self._lock = threading.Lock()
        self._listeners: list[t.Callable[[LogEntry], None]] = []

    def push(self, entry: LogEntry) -> None:
        with self._lock:
            self._entries.append(entry)
            listeners = list(self._listeners)
        for listener in listeners:
            listener(entry)

    def snapshot(self) -> list[LogEntry]:
        with self._lock:
            return list(self._entries)

    def clear(self) -> None:
        with self._lock:
            self._entries.clear()

    def add_listener(self, fn: t.Callable[[LogEntry], None]) -> None:
        with self._lock:
            self._listeners.append(fn)

    def remove_listener(self, fn: t.Callable[[LogEntry], None]) -> None:
        with self._lock:
            self._listeners = [f for f in self._listeners if f != fn]

    def __len__(self) -> int:
        with self._lock:
            return len(self._entries)


log_buffer = LogBuffer()

# Track TUI capture state so configure_logging() can re-add the sink
_tui_capture_level: str | None = None
_tui_capture_sink_id: int | None = None
_tui_file_sink_id: int | None = None

_TUI_LOG_MAX_SIZE = "2 MB"
_TUI_LOG_RETENTION = 2


def _private_log_opener(path: str, flags: int) -> int:
    """Open a persistent diagnostic log without following links."""

    flags |= getattr(os, "O_NOFOLLOW", 0)
    file_descriptor = os.open(path, flags, 0o600)
    with contextlib.suppress(OSError):
        os.fchmod(file_descriptor, 0o600)
    return file_descriptor


def _tui_filter(record: dict) -> bool:
    """Filter TUI log entries: dreadnode.* at any level, others at WARNING+."""
    source = record["name"] or ""
    if source.startswith("dreadnode"):
        return True
    return record["level"].no >= logging.WARNING


def _tui_sink(message: t.Any) -> None:
    """Loguru sink that captures entries into the TUI log buffer."""
    record = message.record
    msg = record["message"]
    # Append exception traceback if present
    exc = record.get("exception")
    if exc and exc.traceback:
        import traceback as tb

        msg += "\n" + "".join(tb.format_exception(type(exc.value), exc.value, exc.traceback))
    entry = LogEntry(
        timestamp=record["time"].replace(tzinfo=None),
        level=record["level"].name,
        source=record["name"] or "loguru",
        message=msg,
        level_no=record["level"].no,
    )
    log_buffer.push(entry)


def _add_tui_sinks(level: str) -> tuple[int, int | None]:
    """Install the in-memory capture and bounded persistent TUI self-log."""

    buffer_sink_id = logger.add(  # ty: ignore[no-matching-overload] - loguru stub mismatch
        _tui_sink,
        format="{message}",
        level=level.upper(),
        filter=_tui_filter,
        colorize=False,
        backtrace=False,
        diagnose=False,
    )

    # The persistent self-log feeds bug-report bundles as the "previous logs"
    # category, which is shared without the explicit TRACE/conversation consent —
    # TRACE records (prompts, model payloads) stay in the in-memory buffer only.
    file_level = "DEBUG" if level.upper() == "TRACE" else level.upper()
    file_sink_id: int | None = None
    with contextlib.suppress(OSError, ValueError):
        from dreadnode.app import paths

        paths.LOGS_DIR.mkdir(parents=True, exist_ok=True)
        file_sink_id = logger.add(
            paths.LOGS_DIR / "tui.log",
            format=(
                "{time:YYYY-MM-DDTHH:mm:ss.SSSZ} {level: <8} {name}:{function}:{line}  {message}"
            ),
            level=file_level,
            filter=_tui_filter,
            colorize=False,
            backtrace=False,
            diagnose=False,
            rotation=_TUI_LOG_MAX_SIZE,
            retention=_TUI_LOG_RETENTION,
            opener=_private_log_opener,
        )
    return buffer_sink_id, file_sink_id


def enable_tui_capture(level: str = "trace") -> int:
    """Replace all loguru sinks with the TUI ring-buffer sink.

    Removes existing sinks (including stderr) so log output doesn't
    corrupt the Textual interface.  Returns the new sink ID for removal.
    """
    global _tui_capture_level  # noqa: PLW0603 - intentional process-wide TUI state
    global _tui_capture_sink_id
    global _tui_file_sink_id
    _tui_capture_level = level
    # Remove the default stderr sink so log output doesn't render
    # over the Textual TUI. Logs are captured into the ring buffer
    # and displayed inside the TUI's console panel instead.
    logger.remove()
    logger.enable("dreadnode")
    _tui_capture_sink_id, _tui_file_sink_id = _add_tui_sinks(level)
    return _tui_capture_sink_id


class _InterceptHandler(logging.Handler):
    """Route stdlib logging into loguru, preserving caller metadata."""

    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Patch loguru record with the stdlib caller info rather than
        # trying to walk the stack (which lands on logging internals).
        def _patch(loguru_record: dict) -> None:
            loguru_record["name"] = record.name
            loguru_record["function"] = record.funcName
            loguru_record["line"] = record.lineno

        logger.patch(_patch).opt(exception=record.exc_info).log(level, record.getMessage())


def install_stdlib_intercept() -> None:
    """Install handler that routes stdlib logging into loguru."""
    logging.basicConfig(handlers=[_InterceptHandler()], level=0, force=True)


# ======================================================================
# Configuration
# ======================================================================

_SERVER_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)


def _resolve_level(level: LogLevel | None) -> str:
    """Resolve log level from argument, env var, or default to 'info'."""
    resolved = (
        level if level is not None else os.environ.get("DREADNODE_LOG_LEVEL", "info")
    ).lower()
    if resolved not in t.get_args(LogLevel):
        resolved = "info"
    return resolved


_LOGURU_TO_STDLIB: dict[str, int] = {
    "trace": logging.DEBUG,
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "success": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}


def _loguru_to_stdlib_level(level: str) -> int:
    """Map a loguru level name to the nearest stdlib logging level."""
    return _LOGURU_TO_STDLIB.get(level.lower(), logging.DEBUG)


def configure_logging(
    level: LogLevel | None = None,
    log_file: pathlib.Path | None = None,
    log_file_level: LogLevel = "debug",
    *,
    verbose: bool = False,
) -> None:
    """
    Configure loguru with Rich console output (library/interactive mode).

    Args:
        level: Console log level. If omitted, defaults to the
            ``DREADNODE_LOG_LEVEL`` env var or ``info``.
        log_file: Optional file path for logging.
        log_file_level: Log level for file output.
        verbose: Enable richer tracebacks and show source paths.
    """
    resolved_level = _resolve_level(level)

    global _tui_capture_sink_id
    global _tui_file_sink_id

    logger.remove()
    logger.enable("dreadnode")

    # Rich-formatted console output via RichHandler
    logger.add(
        RichHandler(
            console=console,
            log_time_format="%X",
            rich_tracebacks=True,
            markup=True,
            show_path=verbose,
        ),
        format=lambda _: "{message}",
        level=resolved_level.upper(),
        backtrace=verbose,
        diagnose=False,
    )

    # Re-add TUI capture sink if it was previously enabled
    if _tui_capture_level is not None:
        _tui_capture_sink_id, _tui_file_sink_id = _add_tui_sinks(_tui_capture_level)

    if log_file is not None:
        logger.add(log_file, level=log_file_level.upper())
        logger.info(f"Logging to {log_file}")


def configure_server_logging(
    level: LogLevel | None = None,
    log_file: pathlib.Path | str | None = None,
    log_file_level: LogLevel = "debug",
) -> None:
    """
    Configure loguru for server/serve mode (structured, timestamped, no Rich).

    Intercepts uvicorn and fastapi stdlib loggers into loguru.
    Also checks the ``DREADNODE_LOG_FILE`` env var for a file sink path.

    Args:
        level: Console log level. If omitted, defaults to the
            ``DREADNODE_LOG_LEVEL`` env var or ``info``.
        log_file: Optional file path for logging. Falls back to
            ``DREADNODE_LOG_FILE`` env var if not provided.
        log_file_level: Log level for file output.
    """
    resolved_level = _resolve_level(level)
    resolved_log_file = log_file or os.environ.get("DREADNODE_LOG_FILE")

    logger.remove()
    logger.enable("dreadnode")

    # Structured stdout output
    logger.add(
        sys.stdout,
        format=_SERVER_FORMAT,
        level=resolved_level.upper(),
        diagnose=False,
        colorize=True,
    )

    # Intercept uvicorn/fastapi stdlib loggers — match their level to the
    # configured loguru level. Without this, log_config=None leaves these
    # at NOTSET → inherits root WARNING, silencing INFO access logs.
    stdlib_level = _loguru_to_stdlib_level(resolved_level)
    for name in ("uvicorn", "uvicorn.access", "uvicorn.error", "fastapi"):
        _logger = logging.getLogger(name)
        _logger.handlers = [_InterceptHandler()]
        _logger.setLevel(stdlib_level)
        _logger.propagate = False

    # Clean (no ANSI) file sink for sandbox/container log capture
    if resolved_log_file is not None:
        logger.add(
            resolved_log_file,
            format=_SERVER_FORMAT,
            level=log_file_level.upper(),
            colorize=False,
        )
        logger.info(f"Logging to {resolved_log_file}")


def confirm(action: str) -> bool:
    """Prompt user for confirmation."""
    return Confirm.ask(
        f"[bold magenta]↔[/] {action}",
        default=False,
        case_sensitive=False,
        console=console,
    )
