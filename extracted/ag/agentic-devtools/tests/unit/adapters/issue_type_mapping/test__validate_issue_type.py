"""Tests for _validate_issue_type helper (FR-008)."""

from __future__ import annotations

import pytest

from agentic_devtools.adapters.issue_type_mapping import _validate_issue_type


class TestValidateIssueType:
    @pytest.mark.parametrize("issue_type", ["epic", "feature", "subtask", "task", "bug"])
    def test_valid_types_pass(self, issue_type: str) -> None:
        _validate_issue_type(issue_type)

    def test_empty_string_raises(self) -> None:
        with pytest.raises(ValueError, match="non-empty string"):
            _validate_issue_type("")

    def test_whitespace_only_raises(self) -> None:
        with pytest.raises(ValueError, match="non-empty string"):
            _validate_issue_type("   ")

    def test_legacy_story_raises(self) -> None:
        with pytest.raises(ValueError, match="Unsupported issue_type 'story'"):
            _validate_issue_type("story")

    def test_legacy_sub_task_raises(self) -> None:
        with pytest.raises(ValueError, match="Unsupported issue_type 'sub-task'"):
            _validate_issue_type("sub-task")

    def test_error_contains_sorted_valid_types(self) -> None:
        with pytest.raises(ValueError, match=r"\['bug', 'epic', 'feature', 'subtask', 'task'\]"):
            _validate_issue_type("invalid")
