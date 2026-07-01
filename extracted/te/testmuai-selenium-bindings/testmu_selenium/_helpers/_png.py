"""Shared PNG IHDR dimension reader — no Pillow dependency.

Extracted from _action_scroll_until_element._png_dimensions so that _heal.py
can validate screenshots before making API calls without importing a
scroll-action-specific helper (the original version raises NoSuchElementException
with an action-specific message, which is misleading in the heal tier — Incident
2026-06 code review).

Callers translate ValueError to their domain exception:
  - _heal.desktop_locate:             ValueError → HealTierMiss("DESKTOP_LOCATE", ...)
  - _action_scroll_until_element:     ValueError → NoSuchElementException(existing msg)
"""
from __future__ import annotations

import struct


def _png_dimensions(data: bytes) -> tuple[int, int]:
    """(width, height) from a PNG's IHDR header — no Pillow dependency.

    The PNG spec places the 8-byte magic signature immediately before the IHDR
    chunk; width and height are big-endian uint32 at byte offsets 16 and 20.
    Keeps the shipped binding slim (no Pillow dependency for IHDR reads).

    Raises:
        ValueError: if ``data`` is not a valid PNG (wrong magic or missing IHDR).
            Intentionally generic so callers can re-raise as their domain exception.
    """
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise ValueError("screenshot is not a valid PNG")
    width, height = struct.unpack(">II", data[16:24])
    return width, height
