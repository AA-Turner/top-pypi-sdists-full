"""The blank-screenshot detector: flat black / white frames are flagged, real pages are not.

A JS-heavy homepage photographed before it painted comes out one flat color; the
capture retries, and a frame that is still blank is stored with
``metadata.blank = true`` so no hero reader ever shows it.
"""

from __future__ import annotations

import io
import random

import pytest

PIL = pytest.importorskip("PIL")
from PIL import Image, ImageDraw  # noqa: E402

from matrx_scraper.render_readiness import (  # noqa: E402
    blank_flag_metadata,
    blank_measure,
    png_looks_blank,
)
from matrx_scraper.web_crawl.persistence import canonical_screenshot_kind  # noqa: E402

W, H = 1440, 900


def _png(image: Image.Image) -> bytes:
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue()


def _solid(color: tuple[int, int, int]) -> bytes:
    return _png(Image.new("RGB", (W, H), color))


def _real_page(background: tuple[int, int, int]) -> bytes:
    """A dark or light page with a nav bar, a headline block, cards and an image."""
    rng = random.Random(7)
    image = Image.new("RGB", (W, H), background)
    draw = ImageDraw.Draw(image)
    fg = (240, 240, 240) if sum(background) < 384 else (20, 20, 20)
    draw.rectangle((0, 0, W, 80), fill=(30, 60, 140))
    for x in range(60, 700, 120):
        draw.rectangle((x, 30, x + 80, 50), fill=fg)
    draw.rectangle((80, 200, 900, 260), fill=fg)
    draw.rectangle((80, 290, 700, 320), fill=fg)
    for i in range(3):
        draw.rectangle((80 + i * 440, 420, 460 + i * 440, 800), outline=fg, width=3)
    for _ in range(4000):
        x, y = rng.randrange(950, 1400), rng.randrange(120, 380)
        draw.point((x, y), fill=(rng.randrange(256), rng.randrange(256), rng.randrange(256)))
    draw.rectangle((950, 120, 1400, 380), outline=(200, 40, 40), width=6)
    return _png(image)


def test_solid_black_frame_is_blank():
    png = _solid((0, 0, 0))
    assert png_looks_blank(png, W, H) is True


def test_solid_white_frame_is_blank():
    png = _solid((255, 255, 255))
    assert png_looks_blank(png, W, H) is True


def test_near_black_with_a_faint_speck_is_still_blank():
    image = Image.new("RGB", (W, H), (8, 8, 10))
    ImageDraw.Draw(image).rectangle((700, 440, 712, 452), fill=(255, 255, 255))
    assert png_looks_blank(_png(image), W, H) is True


@pytest.mark.parametrize("background", [(255, 255, 255), (10, 10, 10)])
def test_a_real_page_is_not_blank_even_on_a_dark_theme(background):
    png = _real_page(background)
    measure = blank_measure(png)
    assert measure is not None
    assert png_looks_blank(png, W, H) is False, measure


def test_blank_flag_metadata_marks_only_blank_frames():
    flagged = blank_flag_metadata(_solid((0, 0, 0)), W, H)
    assert flagged["blank"] is True
    assert flagged["blank_measure"]["dominant_share"] >= 0.985
    assert blank_flag_metadata(_real_page((255, 255, 255)), W, H) == {}


def test_full_page_capture_kinds_are_never_stored_as_viewport():
    for kind in ("full_page", "desktop_full", "mobile_full"):
        assert canonical_screenshot_kind(kind, homepage_bootstrap=False) == "full"
    for kind in ("viewport_desktop", "desktop_fold", "mobile_fold"):
        assert canonical_screenshot_kind(kind, homepage_bootstrap=False) == "viewport"
    assert canonical_screenshot_kind("desktop_full", homepage_bootstrap=True) == "homepage"
