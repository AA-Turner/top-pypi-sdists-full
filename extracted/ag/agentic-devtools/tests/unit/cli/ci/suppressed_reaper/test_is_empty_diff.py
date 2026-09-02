"""Tests for suppressed_reaper.is_empty_diff()."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.suppressed_reaper import is_empty_diff
from tests.unit.cli.ci.suppressed_reaper._fixtures import brief


class TestIsEmptyDiff:
    """All three statistics must be zero."""

    def test_true_when_all_counts_are_zero(self) -> None:
        """A genuinely empty commit reports no changes at all."""
        assert is_empty_diff(brief()) is True

    @pytest.mark.parametrize("field", ["changed_files", "additions", "deletions"])
    def test_false_when_any_count_is_non_zero(self, field: str) -> None:
        """Any non-zero statistic means the diff is not empty."""
        assert is_empty_diff(brief(**{field: 1})) is False
