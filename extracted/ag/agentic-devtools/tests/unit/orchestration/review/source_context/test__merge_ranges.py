"""Tests for _merge_ranges()."""

from __future__ import annotations

from agentic_devtools.orchestration.review.source_context import _merge_ranges


class TestMergeRanges:
    """Tests for line-range merging."""

    def test_returns_empty_list_for_no_ranges(self) -> None:
        """An empty input list produces an empty output list."""
        assert _merge_ranges([]) == []

    def test_merges_overlapping_and_adjacent_ranges(self) -> None:
        """Overlapping and adjacent ranges collapse into a single range."""
        assert _merge_ranges([(5, 8), (1, 2), (3, 4), (10, 10)]) == [(1, 8), (10, 10)]
