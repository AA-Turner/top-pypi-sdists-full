"""Logging configuration for Runlayer CLI."""

import logging
import os
import sys
from pathlib import Path
from datetime import datetime

import structlog

from runlayer_cli import __version__
from runlayer_cli.paths import get_runlayer_dir


def _get_log_file_path(command: str) -> Path:
    """Generate log file path based on command and version."""
    log_dir = get_runlayer_dir() / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    version_str = __version__.replace(".", "-")
    return log_dir / f"runlayer-v{version_str}-{command}-{date_str}.log"


def get_log_file_path(command: str) -> Path:
    """Get the log file path for a command."""
    return _get_log_file_path(command)


def _get_log_level() -> int:
    """Get log level from environment variable, defaulting to INFO."""
    level_name = os.environ.get("LOG_LEVEL", "INFO").upper()
    return getattr(logging, level_name, logging.INFO)


def setup_logging(command: str, quiet_console: bool = False) -> Path:
    """
    Setup logging for the CLI.

    Args:
        command: Command name (e.g., "run", "deploy")
        quiet_console: If True, suppress all console output (for stdio protocols)

    Returns:
        Path to the log file

    Environment Variables:
        LOG_LEVEL: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
                   Defaults to INFO.
    """

    log_file_path = _get_log_file_path(command)
    log_level = _get_log_level()

    # Configure stdlib logging handlers
    file_handler = logging.FileHandler(log_file_path, mode="a", encoding="utf-8")
    file_handler.setLevel(log_level)

    handlers: list[logging.Handler] = [file_handler]

    if not quiet_console:
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setLevel(log_level)
        handlers.append(console_handler)

    logging.basicConfig(
        format="%(message)s",
        level=log_level,
        handlers=handlers,
        force=True,
    )

    # Suppress noisy HTTP request logs from httpx
    logging.getLogger("httpx").setLevel(logging.WARNING)

    # Shared processors
    shared_processors: list[structlog.types.Processor] = [
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
    ]

    structlog.configure(
        processors=shared_processors
        + [structlog.stdlib.ProcessorFormatter.wrap_for_formatter],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Set formatter on all handlers
    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.dev.ConsoleRenderer(
                colors=False, exception_formatter=structlog.dev.plain_traceback
            ),
        ],
    )

    for handler in logging.root.handlers:
        handler.setFormatter(formatter)

    return log_file_path
