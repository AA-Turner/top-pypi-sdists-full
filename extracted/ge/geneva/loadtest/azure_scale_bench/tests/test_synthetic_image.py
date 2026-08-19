# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Tests for the real-image generator: determinism, sizing, decodability, pHash."""

from __future__ import annotations

import io
import math
from typing import TYPE_CHECKING, Any

import pytest

from loadtest.azure_scale_bench import constants, synthetic_image

if TYPE_CHECKING:
    from PIL import Image

_PNG_IEND = b"IEND\xaeB`\x82"  # the final chunk of a valid PNG

# The pHash realism tests render in this fixed mid bucket to bound test cost.
_PHASH_LO, _PHASH_HI, _PHASH_TARGET = 16 << 10, 64 << 10, 32 << 10


def _representative(lo: int, hi: int) -> int:
    """A geometric-midpoint target inside ``[lo, hi)``."""
    mid = int(round(math.sqrt(max(lo, 1) * (hi - 1))))
    return min(max(mid, max(lo, 1)), hi - 1)


def test_render_is_deterministic() -> None:
    assert synthetic_image.render_for_id(7) == synthetic_image.render_for_id(7)


@pytest.mark.parametrize(
    ("name", "lo", "hi"),
    [(n, lo, hi) for n, lo, hi, _ in constants.SIZE_BUCKETS if hi <= 16 << 20],
)
def test_render_lands_in_bucket(name: str, lo: int, hi: int) -> None:
    # Real procedural images whose encoded size lands in the target bucket (no
    # padding). Buckets up to 16 MiB are rendered directly to bound test cost.
    rendered = synthetic_image.render_sized_image(
        0, lo, hi, _representative(lo, hi), image_format="png"
    )
    assert lo <= rendered.actual_bytes < hi, (name, rendered.actual_bytes, lo, hi)


def test_render_lands_in_large_bucket() -> None:
    # 16_64mib at its low end — exercises the large-tail path while bounding memory.
    lo, hi = 16 << 20, 64 << 20
    rendered = synthetic_image.render_sized_image(
        0, lo, hi, 17 << 20, image_format="png"
    )
    assert lo <= rendered.actual_bytes < hi


def test_render_decodes_and_has_no_trailing_padding() -> None:
    from PIL import Image

    rendered = synthetic_image.render_sized_image(3, 4 << 10, 16 << 10, 8 << 10)
    img = Image.open(io.BytesIO(rendered.image_bytes))
    img.load()
    assert img.format == "PNG"
    assert img.size == (rendered.width, rendered.height)
    # A real PNG ends exactly at IEND — proves there is no appended padding.
    assert rendered.image_bytes.endswith(_PNG_IEND)


def test_normalize_format() -> None:
    assert synthetic_image.normalize_format("JPG") == "jpeg"
    assert synthetic_image.normalize_format("jpeg") == "jpeg"
    assert synthetic_image.normalize_format("png") == "png"


def test_bucket_of() -> None:
    assert synthetic_image.bucket_of(0) == "lt_1kib"  # below floor -> first bucket
    assert synthetic_image.bucket_of(500) == "lt_1kib"
    assert synthetic_image.bucket_of(2000) == "1_4kib"
    assert synthetic_image.bucket_of(100 << 20) in {
        n for n, *_ in constants.SIZE_BUCKETS
    }


@pytest.mark.parametrize(
    ("name", "lo", "hi"),
    [
        (n, lo, hi)
        for n, lo, hi, _ in constants.SIZE_BUCKETS
        if lo >= (16 << 10) and hi <= (1 << 20)
    ],
)
def test_jpeg_render_lands_in_bucket(name: str, lo: int, hi: int) -> None:
    # JPEG size is sub-linear in resolution; id 1100 previously landed just below
    # the 64_256kib floor. The growth-aware correction loop must now reach in-bucket.
    rendered = synthetic_image.render_sized_image(
        1100, lo, hi, _representative(lo, hi), image_format="jpeg"
    )
    assert lo <= rendered.actual_bytes < hi, (name, rendered.actual_bytes, lo, hi)
    assert synthetic_image.bucket_of(rendered.actual_bytes) == name


# --- pHash realism (the property the dedupe benchmark rests on) --------------
#
# The structured generator must produce perceptual hashes that (a) spread across
# distinct images instead of collapsing, (b) are identical for identical bytes,
# (c) are stable when the same id is rendered at a different resolution, and
# (d) survive mild transforms. White-noise pixels satisfy none of these. The
# assertions are deliberately tolerant (counts/budgets, not single exact cases)
# so library/version drift does not make them brittle.


def _phash(image_bytes: bytes, imagehash: Any) -> Any:
    """Perceptual hash of encoded image bytes (an ``imagehash.ImageHash``)."""
    from PIL import Image

    with Image.open(io.BytesIO(image_bytes)) as img:
        return imagehash.phash(img)


def _render_phash_image(image_id: int) -> bytes:
    """Render one image in the fixed pHash test bucket."""
    return synthetic_image.render_sized_image(
        image_id, _PHASH_LO, _PHASH_HI, _PHASH_TARGET, image_format="png"
    ).image_bytes


def test_phash_distinct_images_do_not_collapse() -> None:
    imagehash = pytest.importorskip("imagehash")
    n = 128
    hashes = [_phash(_render_phash_image(i), imagehash) for i in range(n)]

    # Distinct seeds must not produce the same perceptual hash.
    collisions = n - len({str(h) for h in hashes})
    assert collisions <= 1, f"{collisions} exact pHash collisions across {n} images"

    # And essentially no near-duplicate pairs: independent 64-bit hashes almost
    # never land within 10 bits by chance, so a tiny slack absorbs lib quirks.
    near = sum(
        1 for i in range(n) for j in range(i + 1, n) if hashes[i] - hashes[j] <= 10
    )
    assert near <= 2, f"{near} near-duplicate pHash pairs (distance <= 10)"


def test_phash_identical_bytes_hash_identically() -> None:
    imagehash = pytest.importorskip("imagehash")
    a = _render_phash_image(5)
    b = _render_phash_image(5)
    assert a == b  # deterministic bytes
    assert _phash(a, imagehash) - _phash(b, imagehash) == 0


def test_phash_stable_across_target_size() -> None:
    # Normalized-coords design: the SAME image_id rendered into different size
    # buckets (so the correction loop lands on different resolutions) is the same
    # image perceptually, so its pHash barely moves. This guards the invariant
    # that resolution changes inside render_sized_image do not change identity.
    imagehash = pytest.importorskip("imagehash")
    for i in range(8):
        small = synthetic_image.render_sized_image(
            i, 16 << 10, 64 << 10, 32 << 10, image_format="png"
        )
        large = synthetic_image.render_sized_image(
            i, 64 << 10, 256 << 10, 128 << 10, image_format="png"
        )
        dist = _phash(small.image_bytes, imagehash) - _phash(
            large.image_bytes, imagehash
        )
        assert dist <= 10, (i, small.width, large.width, dist)


def test_phash_stable_under_mild_transforms() -> None:
    # Real images keep their pHash under mild transforms; the structured generator
    # must too (white noise would not). Tolerant: count failures across a sample
    # rather than requiring every transform on every image to pass.
    imagehash = pytest.importorskip("imagehash")
    from PIL import Image, ImageFilter

    sample = 16
    bases = [
        Image.open(io.BytesIO(_render_phash_image(i))).convert("RGB")
        for i in range(sample)
    ]

    def _resize_roundtrip(img: Image.Image) -> Image.Image:
        w, h = img.size
        return img.resize((max(8, w // 2), max(8, h // 2))).resize((w, h))

    def _blur(img: Image.Image) -> Image.Image:
        return img.filter(ImageFilter.GaussianBlur(1.0))

    def _jpeg70(img: Image.Image) -> Image.Image:
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=70)
        return Image.open(io.BytesIO(buf.getvalue()))

    def _crop_resize(img: Image.Image) -> Image.Image:
        # A small (5%) center crop, then resize back — a gentle reframing.
        w, h = img.size
        cw, ch = int(w * 0.95), int(h * 0.95)
        left, top = (w - cw) // 2, (h - ch) // 2
        return img.crop((left, top, left + cw, top + ch)).resize((w, h))

    def _failures(transform: Any, threshold: int) -> int:
        return sum(
            1
            for img in bases
            if imagehash.phash(transform(img)) - imagehash.phash(img) > threshold
        )

    # Non-crop transforms barely move the hash; allow a tiny slack for lib drift.
    assert _failures(_resize_roundtrip, 10) <= 2
    assert _failures(_blur, 10) <= 2
    assert _failures(_jpeg70, 10) <= 2
    # A small crop reframes slightly, so allow a looser threshold + a few failures.
    assert _failures(_crop_resize, 12) <= 3
