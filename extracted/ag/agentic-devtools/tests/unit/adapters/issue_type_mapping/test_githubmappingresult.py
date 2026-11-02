"""Tests for GitHubMappingResult frozen dataclass."""

from __future__ import annotations

import pytest

from agentic_devtools.adapters.issue_type_mapping import GitHubMappingResult


class TestGitHubMappingResult:
    def test_construction(self) -> None:
        result = GitHubMappingResult(merged_labels=["Epic", "docs"])
        assert result.merged_labels == ["Epic", "docs"]

    def test_frozen(self) -> None:
        result = GitHubMappingResult(merged_labels=["Bug"])
        with pytest.raises(AttributeError):
            result.merged_labels = ["other"]  # type: ignore[misc]
