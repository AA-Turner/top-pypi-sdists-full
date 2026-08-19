# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Tests for deterministic duplicate injection + ground truth."""

from __future__ import annotations

from loadtest.azure_scale_bench import dedupe_inject


def test_is_member_rate_matches_pct() -> None:
    n = 20_000
    members = sum(dedupe_inject.is_member(i, 0.1) for i in range(n))
    assert abs(members / n - 0.1) < 0.02
    assert all(not dedupe_inject.is_member(i, 0.0) for i in range(1000))
    assert all(dedupe_inject.is_member(i, 1.0) for i in range(1000))


def test_injected_hash_shape_and_determinism() -> None:
    h = dedupe_inject.injected_hash(5, duplicate_pct=1.0, num_groups=10, bit_flips=2)
    assert h is not None
    assert len(h) == 8
    assert all(0 <= b <= 255 for b in h)
    assert h == dedupe_inject.injected_hash(
        5, duplicate_pct=1.0, num_groups=10, bit_flips=2
    )


def test_non_members_get_no_injection() -> None:
    assert (
        dedupe_inject.injected_hash(7, duplicate_pct=0.0, num_groups=10, bit_flips=2)
        is None
    )


def test_group_members_within_threshold() -> None:
    # All rows are members (pct=1.0); same group ⇒ within 2*bit_flips hamming.
    num_groups, bit_flips = 8, 2
    by_group: dict[int, list[int]] = {}
    for i in range(400):
        g = dedupe_inject.expected_group(i, duplicate_pct=1.0, num_groups=num_groups)
        assert g is not None
        by_group.setdefault(g, []).append(i)

    checked = 0
    for rows in by_group.values():
        if len(rows) < 2:
            continue
        hashes: list[list[int]] = []
        for r in rows:
            h = dedupe_inject.injected_hash(
                r, duplicate_pct=1.0, num_groups=num_groups, bit_flips=bit_flips
            )
            assert h is not None
            hashes.append(h)
        for a in range(len(hashes)):
            for b in range(a + 1, len(hashes)):
                assert dedupe_inject.hamming(hashes[a], hashes[b]) <= 2 * bit_flips
                checked += 1
    assert checked > 0


def test_flip_positions_distinct_and_bounded() -> None:
    pos = dedupe_inject._flip_positions(123, 3)
    assert len(pos) == len(set(pos))
    assert all(0 <= p < 64 for p in pos)


def test_resolve_num_groups() -> None:
    # 10000 rows * 0.1 = 1000 members / avg 5 ⇒ 200 groups.
    assert (
        dedupe_inject.resolve_num_groups(10_000, duplicate_pct=0.1, avg_group_size=5)
        == 200
    )
    assert (
        dedupe_inject.resolve_num_groups(
            10_000, duplicate_pct=0.1, avg_group_size=5, configured=42
        )
        == 42
    )
    # Never zero.
    assert dedupe_inject.resolve_num_groups(0, duplicate_pct=0.0, avg_group_size=5) == 1
