"""Logger name normalization into canonical logger ids."""

from __future__ import annotations


def normalize_logger_name(name: str) -> str:
    """Normalize a logger name.

    - Replace ``/`` with ``.``
    - Replace ``:`` with ``.``
    - Lowercase everything
    """
    return name.replace("/", ".").replace(":", ".").lower()
