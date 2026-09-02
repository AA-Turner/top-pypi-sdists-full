from __future__ import annotations

import pytest

from matrx_scraper.screenshot_dimensions import (
    png_dimensions,
    resolve_screenshot_dimensions,
)


def _png_header(width: int, height: int) -> bytes:
    return (
        b"\x89PNG\r\n\x1a\n"
        + (13).to_bytes(4, "big")
        + b"IHDR"
        + width.to_bytes(4, "big")
        + height.to_bytes(4, "big")
    )


def test_png_dimensions_reads_ihdr() -> None:
    assert png_dimensions(_png_header(1440, 3200)) == (1440, 3200)


@pytest.mark.parametrize("width,height", [(0, 0), (None, None), (1440, 0)])
def test_missing_or_zero_metadata_falls_back_to_png(
    width: int | None,
    height: int | None,
) -> None:
    assert resolve_screenshot_dimensions(
        width,
        height,
        _png_header(1440, 3200),
    ) == (1440, 3200)


def test_valid_metadata_does_not_require_decoding() -> None:
    assert resolve_screenshot_dimensions(1366, 768, b"not-a-png") == (1366, 768)


def test_invalid_png_cannot_produce_zero_dimensions() -> None:
    with pytest.raises(ValueError, match="valid PNG"):
        resolve_screenshot_dimensions(0, 0, b"not-a-png")
