# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Deterministic near-duplicate pHash injection with ground truth.

MMLB does not generate near-duplicate images, so without injection the dedupe
stage has nothing to cluster. This module deterministically assigns a fraction
(``duplicate_pct``) of rows to synthetic duplicate groups: each member's pHash is
the group's base hash with a few bit-flips, so all members fall within the
Hamming ``threshold`` of each other and cluster. Keyed on ``row_index`` so it is
reproducible and provides ground truth for validating the dedupe output.
"""

from __future__ import annotations

from loadtest.azure_scale_bench.image_distribution import MASK64, row_hash

_SELECT_SALT = 0x1111_1111_1111_1111
_GROUP_SALT = 0x2222_2222_2222_2222
_BASE_SALT = 0x3333_3333_3333_3333
_FLIP_SALT = 0x4444_4444_4444_4444


def is_member(row_index: int, duplicate_pct: float) -> bool:
    """Whether a row is a synthetic-duplicate member (deterministic)."""
    if duplicate_pct <= 0.0:
        return False
    if duplicate_pct >= 1.0:
        return True
    return (row_hash(row_index ^ _SELECT_SALT) / 2.0**64) < duplicate_pct


def expected_group(
    row_index: int, *, duplicate_pct: float, num_groups: int
) -> int | None:
    """The injected group id for a row, or None if it is not a member.

    Ground truth: two member rows are near-duplicates iff they share a group.
    """
    if num_groups <= 0 or not is_member(row_index, duplicate_pct):
        return None
    return row_hash(row_index ^ _GROUP_SALT) % num_groups


def _base_hash_bytes(group_id: int) -> bytearray:
    """Deterministic 8-byte base hash for a group."""
    return bytearray(row_hash(group_id ^ _BASE_SALT).to_bytes(8, "little"))


def _flip_positions(row_index: int, bit_flips: int) -> list[int]:
    """Deterministic, distinct bit positions (0-63) to flip for a row."""
    flip_h = row_hash(row_index ^ _FLIP_SALT)
    positions: list[int] = []
    shift = 0
    while len(positions) < bit_flips and shift < 60:
        bit = (flip_h >> shift) & 0x3F
        if bit not in positions:
            positions.append(bit)
        shift += 6
    return positions


def injected_hash(
    row_index: int,
    *,
    duplicate_pct: float,
    num_groups: int,
    bit_flips: int,
) -> list[int] | None:
    """The 8-byte injected pHash for a member row, else None (use computed).

    Each member starts from its group's base hash and flips up to ``bit_flips``
    distinct bits, so any two members of a group differ by at most
    ``2 * bit_flips`` bits.
    """
    group = expected_group(
        row_index, duplicate_pct=duplicate_pct, num_groups=num_groups
    )
    if group is None:
        return None
    payload = _base_hash_bytes(group)
    for bit in _flip_positions(row_index, bit_flips):
        payload[bit // 8] ^= 1 << (bit % 8)
    return list(payload)


def resolve_num_groups(
    num_rows: int,
    *,
    duplicate_pct: float,
    avg_group_size: int,
    configured: int | None = None,
) -> int:
    """Number of synthetic groups: explicit, or derived to hit avg group size."""
    if configured is not None:
        return max(1, configured)
    members = int(num_rows * max(0.0, duplicate_pct))
    return max(1, members // max(1, avg_group_size))


def hamming(a: list[int], b: list[int]) -> int:
    """Hamming distance between two equal-length uint8 byte lists."""
    return sum(bin((x ^ y) & MASK64).count("1") for x, y in zip(a, b, strict=True))
