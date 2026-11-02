"""Tests for _find_eligible_child with start_after skipping (branch 157->159)."""

from __future__ import annotations

from unittest.mock import patch

from agentic_devtools.hierarchy.cascade import CascadeProcessor
from agentic_devtools.hierarchy.models import ChildInfo


class TestFindEligibleSkipBefore:
    """Cover the continue branch when iterating before start_after is found."""

    def test_skips_children_before_start_after(self):
        """Children before start_after should be skipped without API calls."""
        proc = CascadeProcessor("o", "r")
        children = [
            ChildInfo(number=1, title="First"),
            ChildInfo(number=2, title="Second"),
            ChildInfo(number=3, title="Third"),
        ]

        # Mock _get_issue_state to return open issue (eligible)
        open_issue = {"state": "open", "labels": []}
        with patch.object(proc, "_get_issue_state", return_value=open_issue) as mock_get:
            eligible, skipped, failed = proc._find_eligible_child(children, start_after=2)
            # Should find #3 as eligible
            assert eligible is not None
            assert eligible.number == 3
            assert skipped == []
            assert failed is None
            # Should only call _get_issue_state for #3 (not #1 or #2)
            mock_get.assert_called_once_with(3)

    def test_no_eligible_after_start(self):
        """If start_after is the last child, no eligible found."""
        proc = CascadeProcessor("o", "r")
        children = [
            ChildInfo(number=1, title="First"),
            ChildInfo(number=2, title="Last"),
        ]

        eligible, skipped, failed = proc._find_eligible_child(children, start_after=2)
        assert eligible is None
        assert skipped == []
        assert failed is None
