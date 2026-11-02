"""Tests for discover_related_prs in retro_spec/artifact_collector.py."""

from __future__ import annotations

import json
import subprocess
from unittest.mock import patch

from agentic_devtools.cli.speckit.retro_spec.artifact_collector import discover_related_prs

_MOD = "agentic_devtools.cli.speckit.retro_spec.artifact_collector"


class TestDiscoverRelatedPrs:
    """Tests for the discover_related_prs function."""

    def test_returns_empty_when_no_prs_found(self) -> None:
        """Test that no results returns empty list."""
        with patch(
            f"{_MOD}.subprocess.run",
            return_value=subprocess.CompletedProcess([], 0, "[]", ""),
        ):
            assert discover_related_prs("owner", "repo", 42) == []

    def test_ignores_malformed_pr_entries(self) -> None:
        """Malformed GitHub entries do not abort either discovery pass."""
        primary_result = json.dumps(
            [
                None,
                {"number": "bad", "title": "fixes #42"},
                {"number": 10, "title": "fixes #42", "body": 42, "state": 42, "mergedAt": 42},
            ]
        )
        secondary_result = json.dumps([None, {"number": 11, "title": 42}])

        call_count = 0

        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            result = primary_result if call_count == 1 else secondary_result
            return subprocess.CompletedProcess([], 0, result, "")

        with patch(f"{_MOD}.subprocess.run", side_effect=side_effect):
            result = discover_related_prs("owner", "repo", 42)

        assert [pr.number for pr in result] == [10]

    def test_returns_empty_for_malformed_pr_response_shape(self) -> None:
        """A non-list GitHub response is treated as an unavailable search."""
        with patch(
            f"{_MOD}.subprocess.run",
            return_value=subprocess.CompletedProcess([], 0, "null", ""),
        ):
            assert discover_related_prs("owner", "repo", 42) == []

    def test_deduplicates_across_primary_and_secondary_search(self) -> None:
        """Test that the same PR found by both searches appears only once."""
        primary_result = json.dumps(
            [{"number": 10, "title": "fixes #42", "body": "", "state": "MERGED", "mergedAt": "2024-01-01T00:00:00Z"}]
        )
        secondary_result = json.dumps(
            [
                {
                    "number": 10,
                    "title": "feat(#42): add feature",
                    "body": "",
                    "state": "MERGED",
                    "mergedAt": "2024-01-01T00:00:00Z",
                }
            ]
        )

        call_count = 0

        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return subprocess.CompletedProcess([], 0, primary_result, "")
            return subprocess.CompletedProcess([], 0, secondary_result, "")

        with patch(f"{_MOD}.subprocess.run", side_effect=side_effect):
            result = discover_related_prs("owner", "repo", 42)

        assert len(result) == 1
        assert result[0].number == 10

    def test_secondary_search_filters_by_conventional_commit_scope(self) -> None:
        """Test that only PRs with issue ref in conventional commit scope are included."""
        primary_result = "[]"
        secondary_result = json.dumps(
            [
                {
                    "number": 1,
                    "title": "feat(#42): add feature",
                    "body": "",
                    "state": "MERGED",
                    "mergedAt": "2024-01-01",
                },
                {
                    "number": 2,
                    "title": "fix: issue #42 mentioned in body",
                    "body": "",
                    "state": "MERGED",
                    "mergedAt": "2024-01-02",
                },
            ]
        )

        call_count = 0

        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return subprocess.CompletedProcess([], 0, primary_result, "")
            return subprocess.CompletedProcess([], 0, secondary_result, "")

        with patch(f"{_MOD}.subprocess.run", side_effect=side_effect):
            result = discover_related_prs("owner", "repo", 42)

        # Only PR #1 has the issue in a conventional commit scope
        assert len(result) == 1
        assert result[0].number == 1

    def test_secondary_search_matches_breaking_change_scope_titles(self) -> None:
        """Test that Conventional Commit titles with ! before : are included."""
        primary_result = "[]"
        secondary_result = json.dumps(
            [
                {
                    "number": 1,
                    "title": "feat(#42)!: add breaking change",
                    "body": "",
                    "state": "MERGED",
                    "mergedAt": "2024-01-01",
                }
            ]
        )

        call_count = 0

        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return subprocess.CompletedProcess([], 0, primary_result, "")
            return subprocess.CompletedProcess([], 0, secondary_result, "")

        with patch(f"{_MOD}.subprocess.run", side_effect=side_effect):
            result = discover_related_prs("owner", "repo", 42)

        assert len(result) == 1
        assert result[0].number == 1

    def test_sorts_results_by_merge_date(self) -> None:
        """Test that results are sorted by merge date ascending."""
        primary_result = json.dumps(
            [
                {"number": 2, "title": "fixes #42", "body": "", "state": "MERGED", "mergedAt": "2024-02-01"},
                {"number": 1, "title": "fixes #42", "body": "", "state": "MERGED", "mergedAt": "2024-01-01"},
            ]
        )

        with patch(
            f"{_MOD}.subprocess.run",
            return_value=subprocess.CompletedProcess([], 0, primary_result, ""),
        ):
            result = discover_related_prs("owner", "repo", 42)

        assert result[0].number == 1
        assert result[1].number == 2

    def test_deduplicates_within_primary_search(self) -> None:
        """Test that duplicate PR numbers in primary results are deduplicated."""
        primary_result = json.dumps(
            [
                {"number": 10, "title": "fixes #42", "body": "", "state": "MERGED", "mergedAt": "2024-01-01"},
                {"number": 10, "title": "fixes #42 dup", "body": "", "state": "MERGED", "mergedAt": "2024-01-01"},
            ]
        )

        with patch(
            f"{_MOD}.subprocess.run",
            return_value=subprocess.CompletedProcess([], 0, primary_result, ""),
        ):
            result = discover_related_prs("owner", "repo", 42)

        assert len(result) == 1
