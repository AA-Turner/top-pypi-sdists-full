# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

import os
import shutil
from enum import Enum, auto
from typing import TextIO

DEFAULT_LOG_PATH = "contrast-agent.log"
DEFAULT_SECURITY_LOG_PATH = "security.log"
DEFAULT_SECURITY_LOG_LEVEL = "INFO"
DEFAULT_LOG_LEVEL = "INFO"
LOGGER_NAME = "contrast"


class LogDestination(Enum):
    """
    A standard stream to log to, as distinct from a filesystem path.
    """

    STDOUT = auto()
    STDERR = auto()


YELLOW = "\033[33m"
RED = "\033[31m"
_LEVEL_COLORS = {
    "warning": YELLOW,
    "error": RED,
    "critical": RED,
}
RESET_COLOR = "\033[0m"


def color_for_level(level: str) -> str | None:
    """Return the ANSI color code for a WARNING/ERROR/CRITICAL level, else None."""
    return _LEVEL_COLORS.get(level)


def stream_is_console(stream: TextIO) -> bool:
    """Return True if `stream` is an interactive console (tty)."""
    return hasattr(stream, "isatty") and bool(stream.isatty())


def color_enabled(stream: TextIO) -> bool:
    # https://no-color.org/ - NO_COLOR takes precedence over everything else,
    # including FORCE_COLOR, whenever it's set to any non-empty value.
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("FORCE_COLOR"):
        return True
    return stream_is_console(stream)


def wrap_with_border(text: str, color: str | None) -> str:
    """Wrap `text` in a rule above and below, matching its widest line
    (clamped to the terminal width). If `color` is given, the whole block is
    wrapped in that ANSI color; otherwise the border is rendered plain."""
    width = min(
        max(len(line) for line in text.splitlines() or [""]),
        shutil.get_terminal_size(fallback=(80, 24)).columns,
    )
    border = "-" * width
    if color is None:
        return f"{border}\n{text}\n{border}"
    return f"{color}{border}\n{text}\n{border}{RESET_COLOR}"
