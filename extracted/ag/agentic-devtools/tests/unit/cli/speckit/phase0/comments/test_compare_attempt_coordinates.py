"""Tests for compare_attempt_coordinates in speckit/phase0/comments.py (FR-004)."""

from __future__ import annotations

from agentic_devtools.cli.speckit.phase0.comments import AttemptCoordinate, compare_attempt_coordinates


class TestCompareAttemptCoordinates:
    """Tests for the compare_attempt_coordinates function."""

    def test_earlier_timestamp_precedes_later_timestamp(self) -> None:
        earlier = AttemptCoordinate("2026-01-01T00:00:00Z", 1, 1)
        later = AttemptCoordinate("2026-01-02T00:00:00Z", 1, 1)
        assert compare_attempt_coordinates(earlier, later) < 0
        assert compare_attempt_coordinates(later, earlier) > 0

    def test_equal_timestamps_break_tie_on_workflow_run_id(self) -> None:
        first = AttemptCoordinate("2026-01-01T00:00:00Z", 1, 1)
        second = AttemptCoordinate("2026-01-01T00:00:00Z", 2, 1)
        assert compare_attempt_coordinates(first, second) < 0

    def test_equal_timestamp_and_run_id_break_tie_on_attempt(self) -> None:
        first = AttemptCoordinate("2026-01-01T00:00:00Z", 1, 1)
        second = AttemptCoordinate("2026-01-01T00:00:00Z", 1, 2)
        assert compare_attempt_coordinates(first, second) < 0

    def test_identical_coordinates_compare_equal(self) -> None:
        a = AttemptCoordinate("2026-01-01T00:00:00Z", 1, 1)
        b = AttemptCoordinate("2026-01-01T00:00:00Z", 1, 1)
        assert compare_attempt_coordinates(a, b) == 0

    def test_compares_by_instant_not_lexicographic_string(self) -> None:
        # Use offset timestamps whose lexicographic order disagrees with their
        # temporal order to prove instant comparison is used, not string comparison.
        # "2026-01-02T00:00:00+03:00" = 2026-01-01T21:00:00Z (UTC) but
        # lexicographically it appears *after* "2026-01-01T23:00:00Z".
        earlier = AttemptCoordinate("2026-01-02T00:00:00+03:00", 1, 1)
        later = AttemptCoordinate("2026-01-01T23:00:00Z", 1, 1)
        assert compare_attempt_coordinates(earlier, later) < 0
