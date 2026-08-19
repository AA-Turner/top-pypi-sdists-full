# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Deterministic, row_index-keyed image attributes and byte-size targets.

Pure module (no Pillow / Ray / Azure). Ports MMLB's splitmix64 ``row_hash`` and
attribute derivation so output is reproducible and consistent with MMLB, and
adds the benchmark's blob-size-distribution logic (bucket choice + log-uniform
target size within the bucket), driven by independent hash streams.
"""

from __future__ import annotations

import math
from typing import NamedTuple

from loadtest.azure_scale_bench import constants

MASK64 = constants.MASK64

# Normalization for the bucket weights (the spec weights sum to ~1.000002).
BucketSpec = tuple[str, int, int, float]

_WEIGHT_TOTAL = sum(weight for *_, weight in constants.SIZE_BUCKETS)


def row_hash(x: int) -> int:
    """splitmix64 finalizer (ported from mmlb generator.rs ``row_hash``)."""
    x &= MASK64
    x = (x + 0x9E3779B97F4A7C15) & MASK64
    x = ((x ^ (x >> 30)) * 0xBF58476D1CE4E5B9) & MASK64
    x = ((x ^ (x >> 27)) * 0x94D049BB133111EB) & MASK64
    return (x ^ (x >> 31)) & MASK64


def rotate_right_u64(x: int, bits: int) -> int:
    """Rotate a 64-bit value right by ``bits`` (ported from generator.rs)."""
    bits %= 64
    if bits == 0:
        return x & MASK64
    return ((x >> bits) | (x << (64 - bits))) & MASK64


def _stream(row_index: int, salt: int) -> int:
    """An independent hash stream for ``row_index`` keyed by a fixed salt."""
    return row_hash((row_index & MASK64) ^ (salt & MASK64))


def _uniform01(h: int) -> float:
    """Map a 64-bit hash to a uniform float in [0, 1)."""
    return (h & MASK64) / 2.0**64


class BucketAssignment(NamedTuple):
    """The chosen size bucket and the concrete target byte size for a row."""

    bucket: str
    lo: int
    hi: int
    target: int


def _pick_bucket_from(
    row_index: int, buckets: list[BucketSpec]
) -> tuple[str, int, int]:
    """Pick a size bucket from ``buckets`` via normalized cumulative weights."""
    u = _uniform01(_stream(row_index, constants.BUCKET_SALT))
    acc = 0.0
    total = sum(weight for *_, weight in buckets)
    for name, lo, hi, weight in buckets:
        acc += weight / total
        if u < acc:
            return name, lo, hi
    name, lo, hi, _ = buckets[-1]
    return name, lo, hi


def _pick_bucket(row_index: int) -> tuple[str, int, int]:
    """Pick a size bucket via the full cumulative weight distribution."""
    return _pick_bucket_from(row_index, constants.SIZE_BUCKETS)


def _largest_non_tail_bucket() -> tuple[str, int, int]:
    """The largest bucket whose upper bound is within the large-tail threshold."""
    for name, lo, hi, _ in reversed(constants.SIZE_BUCKETS):
        if hi <= constants.LARGE_TAIL_THRESHOLD:
            return name, lo, hi
    name, lo, hi, _ = constants.SIZE_BUCKETS[0]
    return name, lo, hi


def _capped_buckets(*, include_large_tail: bool, max_bytes: int) -> list[BucketSpec]:
    """Buckets eligible for a capped run.

    ``max_bytes`` is a smoke/calibration cap. Buckets starting at or above the cap
    are excluded rather than assigned and then clamped, because that makes the
    manifest claim a multi-MiB target bucket while the rendered object is capped
    into a smaller bucket. A bucket that straddles the cap keeps its label but has
    an exclusive upper bound of ``max_bytes + 1`` so targets remain <= the cap.
    """
    if max_bytes < 1:
        raise ValueError(f"max_bytes must be >= 1, got {max_bytes}")

    buckets: list[BucketSpec] = []
    for name, lo, hi, weight in constants.SIZE_BUCKETS:
        if hi > constants.LARGE_TAIL_THRESHOLD and not include_large_tail:
            continue
        if lo >= max_bytes:
            continue
        capped_hi = min(hi, max_bytes + 1)
        if capped_hi > lo:
            buckets.append((name, lo, capped_hi, weight))

    if buckets:
        return buckets

    # Only possible for very tiny caps. Keep the first bucket and cap its range so
    # callers still get a deterministic minimal real image.
    name, lo, _hi, weight = constants.SIZE_BUCKETS[0]
    return [(name, lo, max(lo + 1, max_bytes + 1), weight)]


def target_bytes(row_index: int, lo: int, hi: int) -> int:
    """Log-uniform target byte size in ``[lo, hi)``, deterministic per row.

    Monotonically non-decreasing in the row's target hash stream, so the
    distribution within a bucket is reproducible and testable.
    """
    v = _uniform01(_stream(row_index, constants.TARGET_SALT))
    lo_eff = max(lo, 1)
    ln_lo = math.log(lo_eff)
    ln_hi = math.log(hi)
    target = int(round(math.exp(ln_lo + v * (ln_hi - ln_lo))))
    return min(max(target, lo_eff), hi - 1)


def expected_mean_bytes() -> float:
    """Weight-averaged mean target size (bytes) over the size distribution.

    Each bucket's size is log-uniform on ``[lo, hi)``, whose mean is
    ``(hi - lo) / ln(hi / lo)``; these are weighted by the normalized bucket weights.
    A pure function of ``SIZE_BUCKETS`` (no data scan) — used to estimate batched
    download memory (``checkpoint_size * expected_mean_bytes``).
    """
    total = 0.0
    for _name, lo, hi, weight in constants.SIZE_BUCKETS:
        lo_eff = max(lo, 1)
        bucket_mean = (hi - lo_eff) / (math.log(hi) - math.log(lo_eff))
        total += (weight / _WEIGHT_TOTAL) * bucket_mean
    return total


def assign(
    row_index: int,
    *,
    include_large_tail: bool = False,
    max_bytes: int | None = None,
) -> BucketAssignment:
    """Resolve the (possibly clamped) size bucket and target for a row.

    When ``include_large_tail`` is false, rows that fall in the >64 MiB tail are
    reassigned to the largest sub-threshold bucket. ``max_bytes`` switches to a
    capped bucket space for smoke/calibration runs: buckets above the cap are
    excluded, and any bucket that straddles the cap is capped before target
    selection. This keeps ``bucket`` aligned with the rendered object's expected
    byte range.
    """
    if max_bytes is not None:
        name, lo, hi = _pick_bucket_from(
            row_index,
            _capped_buckets(
                include_large_tail=include_large_tail,
                max_bytes=max_bytes,
            ),
        )
    else:
        name, lo, hi = _pick_bucket(row_index)
        if hi > constants.LARGE_TAIL_THRESHOLD and not include_large_tail:
            name, lo, hi = _largest_non_tail_bucket()
    target = target_bytes(row_index, lo, hi)
    return BucketAssignment(bucket=name, lo=lo, hi=hi, target=target)


def pad_byte(row_index: int) -> int:
    """Deterministic single byte (0-255) used to fill padding for a row."""
    return _stream(row_index, constants.PAD_SALT) & 0xFF


class ImageAttrs(NamedTuple):
    """Derived MMLB-compatible text/font/background attributes for a row."""

    summary_in_image: str
    font: str
    background_color: str
    background_rgb: tuple[int, int, int]


def derive_attrs(row_index: int, summary: str | None) -> ImageAttrs:
    """Derive text/font/background from ``row_index`` (ported from generator.rs)."""
    text = summary or ""
    h = row_hash(row_index)
    trim = h % (constants.MAX_SUMMARY_END_TRIM_WORD_COUNT + 1)
    words = text.split()
    summary_in_image = " ".join(words[:-trim]) if trim and len(words) > trim else text
    font = constants.FONTS[rotate_right_u64(h, 11) % len(constants.FONTS)]
    bg_name, bg_rgb = constants.BACKGROUND_COLORS[
        rotate_right_u64(h, 23) % len(constants.BACKGROUND_COLORS)
    ]
    return ImageAttrs(
        summary_in_image=summary_in_image,
        font=font,
        background_color=bg_name,
        background_rgb=bg_rgb,
    )
