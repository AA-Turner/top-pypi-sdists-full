"""Tests for _merge_github_labels helper (FR-003)."""

from __future__ import annotations

import pytest

from agentic_devtools.adapters.issue_type_mapping import _merge_github_labels


class TestMergeGitHubLabels:
    def test_basic_merge(self) -> None:
        result = _merge_github_labels("Epic", ["docs", "backend"])
        assert result == ["Epic", "docs", "backend"]

    def test_case_insensitive_dedup(self) -> None:
        result = _merge_github_labels("Epic", ["epic", "docs"])
        assert result == ["Epic", "docs"]

    def test_whitespace_trim(self) -> None:
        result = _merge_github_labels("Bug", ["  docs  ", "backend"])
        assert result == ["Bug", "docs", "backend"]

    def test_empty_discard(self) -> None:
        result = _merge_github_labels("Task", ["", "  ", "docs"])
        assert result == ["Task", "docs"]

    def test_derived_first_ordering(self) -> None:
        result = _merge_github_labels("Feature", ["alpha", "beta"])
        assert result[0] == "Feature"

    def test_exact_duplicate_collapse(self) -> None:
        result = _merge_github_labels("Bug", ["docs", "docs", "docs"])
        assert result == ["Bug", "docs"]

    def test_none_declared_labels(self) -> None:
        result = _merge_github_labels("Task", None)
        assert result == ["Task"]

    def test_empty_declared_labels(self) -> None:
        result = _merge_github_labels("Task", [])
        assert result == ["Task"]

    def test_non_string_label_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="must be a string"):
            _merge_github_labels("Task", [42])  # type: ignore[list-item]

    def test_string_declared_labels_raises_type_error(self) -> None:
        with pytest.raises(TypeError, match="must be a list of strings, not a bare str"):
            _merge_github_labels("Task", "docs")  # type: ignore[arg-type]
