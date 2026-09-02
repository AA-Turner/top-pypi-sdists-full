"""Tests for _normalize_jira_labels helper (FR-004)."""

from __future__ import annotations

import pytest

from agentic_devtools.adapters.issue_type_mapping import _normalize_jira_labels


class TestNormalizeJiraLabels:
    def test_trim_whitespace(self) -> None:
        result = _normalize_jira_labels(["  docs  ", " backend "])
        assert result == ["docs", "backend"]

    def test_discard_empty(self) -> None:
        result = _normalize_jira_labels(["", "  ", "docs"])
        assert result == ["docs"]

    def test_case_sensitive_preservation(self) -> None:
        result = _normalize_jira_labels(["Backend", "backend"])
        assert result == ["Backend", "backend"]

    def test_first_occurrence_order(self) -> None:
        result = _normalize_jira_labels(["beta", "alpha", "gamma"])
        assert result == ["beta", "alpha", "gamma"]

    def test_duplicate_removal(self) -> None:
        result = _normalize_jira_labels(["docs", "docs", "docs"])
        assert result == ["docs"]

    def test_none_labels(self) -> None:
        result = _normalize_jira_labels(None)
        assert result == []

    def test_empty_list(self) -> None:
        result = _normalize_jira_labels([])
        assert result == []

    def test_non_string_label_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="must be a string"):
            _normalize_jira_labels([99])  # type: ignore[list-item]

    def test_string_declared_labels_raises_type_error(self) -> None:
        with pytest.raises(TypeError, match="must be a list of strings, not a bare str"):
            _normalize_jira_labels("backend")  # type: ignore[arg-type]
