"""Tests for GITHUB_DEFAULT_LABELS constant (SC-001)."""

from __future__ import annotations

from agentic_devtools.adapters.issue_provider import VALID_ISSUE_TYPES
from agentic_devtools.adapters.issue_type_mapping import GITHUB_DEFAULT_LABELS


class TestGitHubDefaultLabels:
    def test_covers_all_valid_issue_types(self) -> None:
        assert set(GITHUB_DEFAULT_LABELS.keys()) == VALID_ISSUE_TYPES

    def test_exact_values(self) -> None:
        assert GITHUB_DEFAULT_LABELS["epic"] == "epic"
        assert GITHUB_DEFAULT_LABELS["feature"] == "feature"
        assert GITHUB_DEFAULT_LABELS["subtask"] == "Subtask"
        assert GITHUB_DEFAULT_LABELS["task"] == "task"
        assert GITHUB_DEFAULT_LABELS["bug"] == "bug"

    def test_has_five_entries(self) -> None:
        assert len(GITHUB_DEFAULT_LABELS) == 5
