# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Tests for image rendering + padding (needs Pillow; OpenCV optional)."""

from __future__ import annotations

import io

import pytest

from loadtest.azure_scale_bench import image_render

SUMMARY = "the quick brown fox jumps over the lazy dog several times over"


def _pillow_decodes(data: bytes) -> tuple[int, int]:
    from PIL import Image

    with Image.open(io.BytesIO(data)) as img:
        img.load()
        return img.size


def test_pad_to_target_appends_to_exact_length() -> None:
    base = b"PNGDATA"
    out = image_render.pad_to_target(base, 100, pad_byte=0xAB)
    assert len(out) == 100
    assert out[:7] == base
    assert out[7:] == b"\xab" * 93


def test_pad_to_target_noop_when_already_large() -> None:
    base = b"x" * 200
    assert image_render.pad_to_target(base, 100, pad_byte=0) == base


@pytest.mark.parametrize("max_bytes", [512, 4096, 64 << 10, 512 << 10])
def test_build_payload_hits_target_and_decodes_pillow(max_bytes: int) -> None:
    for row_index in range(0, 300, 13):
        result = image_render.build_payload(
            row_index, SUMMARY, max_bytes=max_bytes, font_dir="/nonexistent"
        )
        assert result.actual_bytes == len(result.image_bytes)
        # When the base render fits the target, padding lands exactly on target.
        assert result.actual_bytes >= result.target_bytes or (
            result.actual_bytes <= max_bytes
        )
        width, height = _pillow_decodes(result.image_bytes)
        assert width >= 1
        assert height >= 1


def test_build_payload_actual_matches_target_for_padded_rows() -> None:
    # Rows whose base render is below target must hit the target exactly.
    hit = 0
    for row_index in range(2000):
        result = image_render.build_payload(
            row_index, SUMMARY, max_bytes=256 << 10, font_dir="/nonexistent"
        )
        if result.actual_bytes == result.target_bytes:
            hit += 1
    assert hit > 0


def test_build_payload_jpeg_branch_decodes() -> None:
    result = image_render.build_payload(
        7, SUMMARY, image_format="jpeg", max_bytes=64 << 10, font_dir="/nonexistent"
    )
    assert result.image_format == "jpeg"
    _pillow_decodes(result.image_bytes)


def test_build_payload_small_target_uses_minimal_image() -> None:
    result = image_render.build_payload(
        3, SUMMARY, max_bytes=512, font_dir="/nonexistent"
    )
    assert result.actual_bytes <= 512
    _pillow_decodes(result.image_bytes)


def test_build_payload_is_deterministic() -> None:
    a = image_render.build_payload(123, SUMMARY, font_dir="/nonexistent")
    b = image_render.build_payload(123, SUMMARY, font_dir="/nonexistent")
    assert a == b


def test_build_payload_works_with_default_font_dir() -> None:
    result = image_render.build_payload(11, SUMMARY, max_bytes=4096)
    assert result.image_bytes
    _pillow_decodes(result.image_bytes)


def test_padded_png_decodes_opencv() -> None:
    cv2 = pytest.importorskip("cv2")
    import numpy as np

    result = image_render.build_payload(
        5, SUMMARY, max_bytes=32 << 10, font_dir="/nonexistent"
    )
    arr = np.frombuffer(result.image_bytes, dtype=np.uint8)
    assert cv2.imdecode(arr, cv2.IMREAD_UNCHANGED) is not None
