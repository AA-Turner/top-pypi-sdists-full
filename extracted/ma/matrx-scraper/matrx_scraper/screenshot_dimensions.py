"""Dimension invariants for captured PNG screenshots."""

from __future__ import annotations

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def png_dimensions(content: bytes) -> tuple[int, int]:
    """Read width/height from the PNG IHDR without an image dependency."""

    if len(content) < 24 or content[:8] != PNG_SIGNATURE or content[12:16] != b"IHDR":
        raise ValueError("screenshot is not a valid PNG image")
    width = int.from_bytes(content[16:20], "big")
    height = int.from_bytes(content[20:24], "big")
    if width <= 0 or height <= 0:
        raise ValueError("screenshot PNG has invalid dimensions")
    return width, height


def resolve_screenshot_dimensions(
    width: int | None,
    height: int | None,
    content: bytes,
) -> tuple[int, int]:
    """Use valid capture metadata, falling back to the PNG's canonical size."""

    if width is not None and height is not None and width > 0 and height > 0:
        return width, height
    return png_dimensions(content)


__all__ = ["png_dimensions", "resolve_screenshot_dimensions"]
