"""Structured logging setup for vibe_sdk entry points.

Environment variables, also read from ``.env`` in the nearest parent directory:

- ``VIBE_LOG_LEVEL``: ``DEBUG``, ``INFO``, ``WARNING`` (default), or ``ERROR``.
- ``VIBE_LOG_OUTPUT``: ``stdout`` (default) or a file path.

Call ``configure_logging()`` from process entry points such as CLIs, workers, or
demo scripts. Library modules should keep using ``structlog.get_logger()``.
"""

import logging
import os
import sys
from pathlib import Path

import structlog


def _load_dotenv() -> None:
    """Load the nearest parent ``.env`` without overriding existing env vars."""
    path = Path.cwd()
    for parent in [path, *path.parents]:
        env_file = parent / ".env"
        if env_file.is_file():
            for line in env_file.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip()
                if key and key not in os.environ:
                    os.environ[key] = value
            break


def configure_logging(
    level: str | None = None,
    output: str | None = None,
) -> None:
    """Configure stdlib logging and structlog for vibe_sdk."""
    _load_dotenv()

    level = level or os.environ.get("VIBE_LOG_LEVEL", "WARNING")
    output = output or os.environ.get("VIBE_LOG_OUTPUT", "stdout")

    log_level = getattr(logging, level.upper(), logging.WARNING)

    handler: logging.Handler
    if output == "stdout":
        handler = logging.StreamHandler(sys.stdout)
    else:
        handler = logging.FileHandler(output, mode="a")

    handler.setLevel(log_level)

    logging.basicConfig(
        format="%(message)s",
        handlers=[handler],
        level=log_level,
        force=True,
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.dev.ConsoleRenderer()
            if output == "stdout"
            else structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


__all__ = ["configure_logging"]
