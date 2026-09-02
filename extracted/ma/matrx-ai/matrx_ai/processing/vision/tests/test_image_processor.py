"""Forcing-function tests for ``reencode_for_vision_class``.

The encoder is the bridge between a master image and the bytes that go
on the wire. A regression here means we pay tokens for the wrong size,
or we ship the wrong format to a provider that doesn't accept it. Each
test here asserts a property the *real* encoded output must carry —
re-encoded long edge, JPEG marker, byte-count cap, OCR-mode 4:4:4
chroma marker — and would fail against a ``return master_bytes``
replacement.
"""

from __future__ import annotations

from io import BytesIO

import pytest
from PIL import Image

from matrx_ai.processing.vision import (
    VISION_API_CLASSES,
    reencode_for_vision_class,
    should_skip_reencode,
)


def _make_master_jpeg(width: int, height: int, quality: int = 95) -> bytes:
    """A real JPEG with a deterministic gradient — fixtures are bytes, not files."""
    img = Image.new("RGB", (width, height))
    for y in range(height):
        for x in range(width):
            img.putpixel((x, y), ((x + y) % 256, (x * 2) % 256, (y * 3) % 256))
    buf = BytesIO()
    img.save(buf, format="JPEG", quality=quality, subsampling=0)
    return buf.getvalue()


def _decode(data: bytes) -> Image.Image:
    img = Image.open(BytesIO(data))
    img.load()
    return img


def test_reencode_downscales_when_master_exceeds_long_edge() -> None:
    """A 4000-px-wide master encoded for ``anthropic_sonnet_default``
    (long_edge=1568) must come out at exactly 1568 on the long edge."""
    master = _make_master_jpeg(4000, 2000)
    cls = VISION_API_CLASSES["anthropic_sonnet_default"]
    assert cls.long_edge == 1568

    out = reencode_for_vision_class(master, cls)
    img = _decode(out)
    assert max(img.size) == cls.long_edge
    # Aspect ratio must be preserved (within 1px rounding).
    assert abs(img.width / img.height - 4000 / 2000) < 0.01


def test_reencode_does_not_upscale_smaller_master() -> None:
    """A 800-px master must not be enlarged to 1568 — only downscaling allowed."""
    master = _make_master_jpeg(800, 600)
    cls = VISION_API_CLASSES["anthropic_sonnet_default"]
    out = reencode_for_vision_class(master, cls)
    img = _decode(out)
    assert max(img.size) == 800


def test_reencode_emits_jpeg_format() -> None:
    master = _make_master_jpeg(2000, 1000)
    cls = VISION_API_CLASSES["openai_high"]
    out = reencode_for_vision_class(master, cls)
    # JPEG SOI marker is the first two bytes.
    assert out.startswith(b"\xff\xd8"), "expected JPEG SOI marker"
    img = _decode(out)
    assert img.format == "JPEG"


def test_reencode_respects_max_bytes_cap() -> None:
    """When the encoder would emit bytes over ``cls.max_bytes``, it must
    drop quality in 5-step increments until it fits or hits
    ``min_quality``. Forcing function: at quality=95 the master encodes
    bigger than the cap; at the dropped quality it encodes smaller. The
    cap MUST be respected."""
    # Use a smooth gradient — high-frequency noise doesn't compress
    # enough for any quality below min_quality to fit a tight cap.
    img = Image.new("RGB", (2000, 2000))
    for y in range(2000):
        row_color = (y % 256, (y * 2) % 256, (y * 3) % 256)
        for x in range(2000):
            img.putpixel((x, y), row_color)
    buf = BytesIO()
    img.save(buf, format="JPEG", quality=95, subsampling=0)
    master = buf.getvalue()

    from matrx_ai.processing.vision.vision_classes import VisionApiClass

    high_q = VisionApiClass(
        name="high_q",
        long_edge=1568,
        quality=95,
    )
    out_high = reencode_for_vision_class(master, high_q)

    tight = VisionApiClass(
        name="tight_test",
        long_edge=1568,
        quality=95,
        max_bytes=len(out_high) // 2,  # half the high-quality size — forces shrink
        min_quality=30,
    )
    out_tight = reencode_for_vision_class(master, tight)

    assert len(out_tight) <= tight.max_bytes, (
        f"output {len(out_tight)} > cap {tight.max_bytes} "
        f"(high-q baseline was {len(out_high)})"
    )
    assert len(out_tight) < len(out_high), (
        "shrink loop didn't actually shrink — quality drop was a no-op"
    )
    assert _decode(out_tight).format == "JPEG"


def test_reencode_ocr_mode_uses_444_chroma() -> None:
    """OCR mode swaps to 4:4:4 chroma. We can't read PIL's internal
    'subsampling' flag back from the bytes, but we can verify behaviour
    via output difference: a monochrome high-frequency image encoded with
    4:4:4 + q>=90 must be LARGER than the same image encoded at default
    4:2:0 + q=85, even though both classes share long_edge."""
    master = _make_master_jpeg(1000, 1000)
    base_cls = VISION_API_CLASSES["anthropic_sonnet_default"]
    out_default = reencode_for_vision_class(master, base_cls, ocr_mode=False)
    out_ocr = reencode_for_vision_class(master, base_cls, ocr_mode=True)
    assert len(out_ocr) > len(out_default), (
        f"ocr_mode bytes {len(out_ocr)} not larger than default {len(out_default)} "
        "— expected 4:4:4 chroma + higher quality to retain more detail."
    )


def test_reencode_independent_of_input_mode() -> None:
    """Encoder must convert non-RGB modes (e.g. RGBA, P) to RGB before
    JPEG-encoding — JPEG can't carry alpha. This test feeds RGBA master
    and asserts the output is a valid JPEG."""
    img = Image.new("RGBA", (1000, 800), color=(255, 0, 0, 128))
    buf = BytesIO()
    img.save(buf, format="PNG")
    master = buf.getvalue()

    cls = VISION_API_CLASSES["anthropic_sonnet_default"]
    out = reencode_for_vision_class(master, cls)
    out_img = _decode(out)
    assert out_img.format == "JPEG"
    assert out_img.mode == "RGB"
    assert max(out_img.size) <= cls.long_edge


def test_should_skip_reencode_skips_small_jpeg_master() -> None:
    cls = VISION_API_CLASSES["anthropic_sonnet_default"]
    meta = {
        "media_type": "image/jpeg",
        "format": "JPEG",
        "width": 1000,
        "height": 800,
        "profile": "auto",
    }
    assert should_skip_reencode(meta, cls) is True


def test_should_skip_reencode_does_not_skip_oversized_master() -> None:
    cls = VISION_API_CLASSES["anthropic_sonnet_default"]
    meta = {
        "media_type": "image/jpeg",
        "format": "JPEG",
        "width": 4000,
        "height": 3000,
        "profile": "auto",
    }
    assert should_skip_reencode(meta, cls) is False


def test_should_skip_reencode_does_not_skip_non_jpeg() -> None:
    cls = VISION_API_CLASSES["anthropic_sonnet_default"]
    meta = {
        "media_type": "image/png",
        "format": "PNG",
        "width": 1000,
        "height": 800,
        "profile": "auto",
    }
    assert should_skip_reencode(meta, cls) is False


def test_should_skip_reencode_returns_false_on_missing_meta() -> None:
    cls = VISION_API_CLASSES["anthropic_sonnet_default"]
    assert should_skip_reencode(None, cls) is False
    assert should_skip_reencode({}, cls) is False


@pytest.mark.parametrize("class_name", list(VISION_API_CLASSES.keys()))
def test_reencode_round_trip_every_class(class_name: str) -> None:
    """Every class in the registry must successfully round-trip a typical
    master through the encoder. This is an integration smoke test that
    catches typos in the registry (bad ``format``, bad ``long_edge``)
    immediately."""
    cls = VISION_API_CLASSES[class_name]
    master = _make_master_jpeg(2000, 1500)
    out = reencode_for_vision_class(master, cls)
    img = _decode(out)
    assert img.format == cls.format.upper()
    assert max(img.size) <= cls.long_edge
    assert len(out) <= cls.max_bytes
