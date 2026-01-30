from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys
import os

PACKAGE_NAME = "abstract_utilities"

# ─────────────────────────────────────────────────────────────
# Formatting
# ─────────────────────────────────────────────────────────────

LOG_FORMAT = (
    "[%(asctime)s] "
    "%(levelname)-8s "
    "%(name)s:%(lineno)d | "
    "%(message)s "
    "[target=%(target_file)s:%(target_line)s]"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class SafeFormatter(logging.Formatter):
    """Formatter that tolerates missing `extra` fields."""
    def format(self, record: logging.LogRecord) -> str:
        record.target_file = getattr(record, "target_file", "-")
        record.target_line = getattr(record, "target_line", "-")
        return super().format(record)

class CallerAwareLogger(logging.Logger):
    """
    Logger that reports the first frame outside logging + abstract utilities.
    """

    def findCaller(self, stack_info=False, stacklevel=1):
        import inspect

        frame = inspect.currentframe().f_back  # ← critical fix

        while frame:
            code = frame.f_code
            filename = code.co_filename

            if not (
                "logging" in filename
                or "log_utils" in filename
                or "abstract_utilities" in filename
            ):
                return (
                    filename,
                    frame.f_lineno,
                    code.co_name,
                    None,
                )

            frame = frame.f_back

        return super().findCaller(stack_info, stacklevel)

# ─────────────────────────────────────────────────────────────
# Stack-aware logger
# ─────────────────────────────────────────────────────────────

class StackAwareLogger(logging.Logger):
    """
    Logger that automatically skips itself when reporting
    filename / line number.
    """

    _STACKLEVEL = 2

    def debug(self, msg, *args, **kwargs):
        kwargs.setdefault("stacklevel", self._STACKLEVEL)
        super().debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        kwargs.setdefault("stacklevel", self._STACKLEVEL)
        super().info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        kwargs.setdefault("stacklevel", self._STACKLEVEL)
        super().warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        kwargs.setdefault("stacklevel", self._STACKLEVEL)
        super().error(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        kwargs.setdefault("stacklevel", self._STACKLEVEL)
        super().exception(msg, *args, **kwargs)


# Ensure our logger class is used globally (safe once)
logging.setLoggerClass(StackAwareLogger)


# ─────────────────────────────────────────────────────────────
# Log directory resolution
# ─────────────────────────────────────────────────────────────

def _resolve_log_root() -> Path:
    venv = os.getenv("VIRTUAL_ENV") or os.getenv("CONDA_PREFIX")
    if venv:
        p = Path(venv) / ".logs" / PACKAGE_NAME
        p.mkdir(parents=True, exist_ok=True)
        return p

    home = Path.home() / ".cache" / PACKAGE_NAME / "logs"
    try:
        home.mkdir(parents=True, exist_ok=True)
        return home
    except PermissionError:
        pass

    try:
        syslog = Path("/var/log") / PACKAGE_NAME
        syslog.mkdir(parents=True, exist_ok=True)
        return syslog
    except PermissionError:
        fallback = Path("/tmp") / PACKAGE_NAME / "logs"
        fallback.mkdir(parents=True, exist_ok=True)
        return fallback


LOG_ROOT = _resolve_log_root()


# ─────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────

def get_logFile(
    name: str,
    *,
    level: int = logging.INFO,
    console: bool = True,
    max_bytes: int = 5 * 1024 * 1024,
    backup_count: int = 5,
) -> logging.Logger:

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(level)

    formatter = SafeFormatter(LOG_FORMAT, DATE_FORMAT)

    try:
        file_handler = RotatingFileHandler(
            LOG_ROOT / f"{name}.log",
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except PermissionError:
        logger.addHandler(logging.NullHandler())

    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    logger.propagate = False
    return logger

