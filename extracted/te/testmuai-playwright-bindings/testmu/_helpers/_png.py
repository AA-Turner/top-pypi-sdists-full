"""Shared PNG IHDR dimension reader — no Pillow dependency.

Both scroll_until and the DESKTOP_LOCATE heal tier need to read PNG dims from
raw bytes captured via Playwright's page.screenshot().  Centralised here so the
thin binding ships one copy instead of two near-identical 5-line functions.

Usage::

    from testmu._helpers._png import _png_dimensions
    width, height = _png_dimensions(data)   # raises ValueError on bad PNG
"""
import struct


def _png_dimensions(data: bytes) -> tuple:
    """Return (width, height) of a PNG from its IHDR header.

    Reads the standard 8-byte signature + IHDR chunk only — no Pillow needed.
    The IHDR chunk follows the 8-byte signature; width and height are big-endian
    uint32 at byte offsets 16 and 20.

    Args:
        data: Raw PNG bytes (e.g. from ``page.screenshot()``).

    Returns:
        (width, height) as a 2-tuple of ints.

    Raises:
        ValueError: When *data* is not a valid PNG with an IHDR header.
    """
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise ValueError("screenshot is not a valid PNG")
    width, height = struct.unpack(">II", data[16:24])
    return width, height
