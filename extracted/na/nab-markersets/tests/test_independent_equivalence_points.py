"""Compare all Boolean functions without using cover extraction as the oracle."""

from __future__ import annotations

import pytest

from nab_markersets.markersets import MarkerSet


def _point(index: int) -> MarkerSet:
    """One assignment of two independent memberships and one scalar predicate."""
    result = MarkerSet.full()
    for bit, text in enumerate(
        ('"a" in extras', '"b" in extras', 'sys_platform == "linux"')
    ):
        predicate = MarkerSet.from_marker(text)
        result &= predicate if index & (1 << bit) else ~predicate
    return result


@pytest.mark.parametrize("selection", range(256))
def test_all_three_predicate_functions_compare_against_known_point_changes(
    selection: int,
) -> None:
    source = MarkerSet.empty()
    for index in range(8):
        if selection & (1 << index):
            source |= _point(index)
    universe = MarkerSet.full()
    for index in range(8):
        enlarged = source | _point(index)
        expected = bool(selection & (1 << index))
        assert source.equivalent_within(enlarged, universe) == expected
        assert enlarged.equivalent_within(source, universe) == expected
