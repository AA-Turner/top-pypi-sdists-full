# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Tests for the deterministic image-distribution core (no Pillow/Ray/Azure)."""

from __future__ import annotations

from loadtest.azure_scale_bench import constants
from loadtest.azure_scale_bench import image_distribution as dist


def test_row_hash_matches_splitmix64_reference() -> None:
    # Canonical splitmix64 outputs — pins the MMLB port against regressions.
    assert dist.row_hash(0) == 0xE220A8397B1DCDAF
    assert dist.row_hash(1) == 0x910A2DEC89025CC1
    assert dist.row_hash(12345) == 0x22118258A9D111A0


def test_row_hash_is_64_bit_and_deterministic() -> None:
    for i in (0, 1, 7, 10**9, (1 << 64) - 1):
        h = dist.row_hash(i)
        assert 0 <= h < (1 << 64)
        assert h == dist.row_hash(i)


def test_rotate_right_u64_edges() -> None:
    assert dist.rotate_right_u64(1, 1) == (1 << 63)
    assert dist.rotate_right_u64(0xDEADBEEF, 0) == 0xDEADBEEF
    assert dist.rotate_right_u64(0xDEADBEEF, 64) == 0xDEADBEEF


def test_bucket_distribution_close_to_target() -> None:
    n = 200_000
    counts = {name: 0 for name, *_ in constants.SIZE_BUCKETS}
    for i in range(n):
        counts[dist._pick_bucket(i)[0]] += 1
    weight_total = sum(w for *_, w in constants.SIZE_BUCKETS)
    for name, _, _, weight in constants.SIZE_BUCKETS:
        observed = counts[name] / n
        expected = weight / weight_total
        # Common buckets within 1.5pp; rare tails just must not blow up.
        if expected > 0.01:
            assert abs(observed - expected) < 0.015, (name, observed, expected)


def test_target_within_bucket_bounds() -> None:
    for name, lo, hi, _ in constants.SIZE_BUCKETS:
        for i in range(0, 5000, 7):
            target = dist.target_bytes(i, lo, hi)
            assert max(lo, 1) <= target < hi, (name, i, target)


def test_target_spans_bucket_range() -> None:
    # Over many rows a wide bucket's targets should span much of [lo, hi).
    lo, hi = 16 << 10, 64 << 10
    targets = [dist.target_bytes(i, lo, hi) for i in range(20_000)]
    assert min(targets) < lo * 2
    assert max(targets) > hi // 2


def test_assign_disables_large_tail_by_default() -> None:
    for i in range(50_000):
        a = dist.assign(i, include_large_tail=False)
        assert a.hi <= constants.LARGE_TAIL_THRESHOLD
        assert a.target < constants.LARGE_TAIL_THRESHOLD


def test_assign_respects_max_bytes_cap() -> None:
    cap = 4096
    for i in range(20_000):
        a = dist.assign(i, include_large_tail=True, max_bytes=cap)
        assert a.target <= cap
        assert a.hi <= cap + 1
        assert a.lo < cap
        assert a.target < a.hi


def test_assign_max_bytes_excludes_buckets_at_or_above_cap() -> None:
    cap = 256 << 10
    disallowed = {name for name, lo, _, _ in constants.SIZE_BUCKETS if lo >= cap}
    seen = set()
    for i in range(20_000):
        a = dist.assign(i, include_large_tail=True, max_bytes=cap)
        seen.add(a.bucket)
        assert a.bucket not in disallowed
        assert a.target <= cap
    assert "64_256kib" in seen
    assert "256kib_1mib" not in seen


def test_assign_is_deterministic() -> None:
    for i in (0, 99, 10**6):
        assert dist.assign(i) == dist.assign(i)


def test_pad_byte_range_and_determinism() -> None:
    for i in (0, 1, 12345, 10**9):
        b = dist.pad_byte(i)
        assert 0 <= b <= 255
        assert b == dist.pad_byte(i)


def test_derive_attrs_valid_choices() -> None:
    bg_names = {name for name, _ in constants.BACKGROUND_COLORS}
    for i in range(2000):
        attrs = dist.derive_attrs(i, "the quick brown fox jumps over the lazy dog")
        assert attrs.font in constants.FONTS
        assert attrs.background_color in bg_names
        assert len(attrs.background_rgb) == 3


def test_derive_attrs_trim_is_prefix() -> None:
    summary = "alpha beta gamma delta epsilon zeta eta theta"
    words = summary.split()
    for i in range(500):
        attrs = dist.derive_attrs(i, summary)
        kept = attrs.summary_in_image.split()
        # summary_in_image is always a leading-word prefix of the original.
        assert words[: len(kept)] == kept


def test_derive_attrs_handles_empty_summary() -> None:
    attrs = dist.derive_attrs(42, None)
    assert attrs.summary_in_image == ""
    assert attrs.font in constants.FONTS
