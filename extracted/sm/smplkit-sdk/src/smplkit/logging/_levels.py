"""Bidirectional mapping between Python logging levels and smplkit canonical levels."""

from __future__ import annotations

SMPL_LEVELS = ("TRACE", "DEBUG", "INFO", "WARN", "ERROR", "FATAL", "SILENT")

# Python level → smplkit level (exact matches only)
PYTHON_TO_SMPL: dict[int, str] = {
    5: "TRACE",
    10: "DEBUG",
    20: "INFO",
    30: "WARN",
    40: "ERROR",
    50: "FATAL",
    99: "SILENT",
}

# smplkit level → Python level
SMPL_TO_PYTHON: dict[str, int] = {
    "TRACE": 5,
    "DEBUG": 10,
    "INFO": 20,
    "WARN": 30,
    "ERROR": 40,
    "FATAL": 50,
    "SILENT": 99,
}

# Sorted breakpoints for nearest-level lookup
_SORTED_BREAKPOINTS = sorted(PYTHON_TO_SMPL.keys())


def python_level_to_smpl(level: int) -> str:
    """Map a Python logging level int to the nearest smplkit canonical level.

    Exact matches are preferred.  For non-standard levels the nearest lower
    breakpoint is used; if below all breakpoints, returns ``"TRACE"``.
    """
    if level in PYTHON_TO_SMPL:
        return PYTHON_TO_SMPL[level]
    # Find nearest lower breakpoint
    best = _SORTED_BREAKPOINTS[0]
    for bp in _SORTED_BREAKPOINTS:
        if bp <= level:
            best = bp
        else:
            break
    return PYTHON_TO_SMPL[best]


def smpl_level_to_python(level: str) -> int:
    """Map a smplkit canonical level string to a Python logging level int."""
    return SMPL_TO_PYTHON[level]
