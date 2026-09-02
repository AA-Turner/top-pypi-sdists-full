"""Tests for VALID_ISSUE_TYPES constant (FR-006)."""

from __future__ import annotations

import pytest

from agentic_devtools.adapters.issue_provider import VALID_ISSUE_TYPES


class TestValidIssueTypes:
    """Verify VALID_ISSUE_TYPES frozenset constant."""

    def test_is_frozenset(self):
        assert isinstance(VALID_ISSUE_TYPES, frozenset)

    def test_contains_expected_values(self):
        expected = {"epic", "feature", "subtask", "task", "bug"}
        assert VALID_ISSUE_TYPES == expected

    def test_membership_epic(self):
        assert "epic" in VALID_ISSUE_TYPES

    def test_membership_feature(self):
        assert "feature" in VALID_ISSUE_TYPES

    def test_membership_subtask(self):
        assert "subtask" in VALID_ISSUE_TYPES

    def test_membership_task(self):
        assert "task" in VALID_ISSUE_TYPES

    def test_membership_bug(self):
        assert "bug" in VALID_ISSUE_TYPES

    def test_non_membership_story(self):
        assert "story" not in VALID_ISSUE_TYPES

    def test_non_membership_sub_task(self):
        assert "sub-task" not in VALID_ISSUE_TYPES

    def test_immutability(self):
        with pytest.raises(AttributeError):
            VALID_ISSUE_TYPES.add("new-type")  # type: ignore[attr-defined]

    def test_sorted_produces_deterministic_output(self):
        result = sorted(VALID_ISSUE_TYPES)
        assert result == ["bug", "epic", "feature", "subtask", "task"]

    def test_length(self):
        assert len(VALID_ISSUE_TYPES) == 5
