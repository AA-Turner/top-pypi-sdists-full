"""Evaluate agent detection condition trees from agents.json."""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Any, Callable


def _env_set(name: str) -> bool:
    return bool(os.environ.get(name))


def _env_value(name: str, value: str) -> bool:
    return name in os.environ and os.environ[name] == value


def _env_matches(name: str, pattern: str) -> bool:
    value = os.environ.get(name)
    if not value:
        return False
    try:
        return re.search(pattern, value) is not None
    except re.error:
        # A malformed pattern in the spec should never throw at detection time.
        return False


def _path_exists(path: str) -> bool:
    try:
        return Path(path).exists()
    except OSError:
        return False


def _is_tty() -> bool:
    try:
        return bool(sys.stdout.isatty())
    except Exception:
        return False


# Swappable in tests (mirrors upstream Go isTTYFn / path checks).
path_exists_fn: Callable[[str], bool] = _path_exists
is_tty_fn: Callable[[], bool] = _is_tty


def evaluate_condition(condition: dict[str, Any]) -> bool:
    """Evaluate a condition tree. ``anyOf``/``allOf`` are combinators; the rest are leaves."""
    ctype = condition.get("type")

    if ctype == "env_set":
        return _env_set(condition["name"])

    if ctype == "env_value":
        return _env_value(condition["name"], condition["value"])

    if ctype == "env_matches":
        return _env_matches(condition["name"], condition["pattern"])

    if ctype == "no_tty":
        return not is_tty_fn()

    if ctype == "file_exists":
        return path_exists_fn(condition["path"])

    if ctype == "anyOf":
        for sub in condition.get("conditions", []):
            if evaluate_condition(sub):
                return True
        return False

    if ctype == "allOf":
        for sub in condition.get("conditions", []):
            if not evaluate_condition(sub):
                return False
        return True

    return False
