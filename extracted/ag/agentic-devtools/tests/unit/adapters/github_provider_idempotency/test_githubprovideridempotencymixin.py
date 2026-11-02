"""Tests for GitHubProvider."""

from __future__ import annotations

import json
import subprocess

import pytest

from agentic_devtools.adapters.github_provider import GitHubProvider
from tests.unit.adapters.github_provider._fixtures import _make_run_mock


class TestGitHubProviderHelpers:
    """Tests for internal helper methods."""

    def test_find_existing_issue_returns_orchestration_key_match(self):
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(
                stdout=json.dumps(
                    {
                        "items": [
                            {
                                "number": 42,
                                "html_url": "https://github.com/org/repo/issues/42",
                                "title": "Existing issue",
                                "body": "Issue body",
                            }
                        ]
                    }
                )
            ),
        )

        result = provider.find_existing_issue("abc123")

        assert result is not None
        assert result.identifier == "42"
        assert result.status == "existing"

    def test_find_by_orchestration_key_runtime_error(self):
        """_find_by_orchestration_key surfaces RuntimeError (e.g., auth failure)."""
        provider = GitHubProvider(
            owner_repo="org/repo", run_command=_make_run_mock(stderr="401 unauthorized", returncode=1)
        )
        with pytest.raises(RuntimeError, match="gh command failed"):
            provider._find_by_orchestration_key("abc123")

    def test_find_by_orchestration_key_query_includes_is_issue(self):
        """_find_by_orchestration_key includes is:issue in the search query to exclude PRs."""
        captured: list[list[str]] = []

        def capturing_run(args, **kwargs):
            captured.append(args)
            return subprocess.CompletedProcess(
                args=args,
                returncode=0,
                stdout=json.dumps({"items": []}),
                stderr="",
            )

        provider = GitHubProvider(owner_repo="org/repo", run_command=capturing_run)
        provider._find_by_orchestration_key("abc123")
        assert captured, "run_command was never called"
        query_arg = next((a for a in captured[0] if a.startswith("q=")), None)
        assert query_arg is not None, "no 'q=' argument found in gh call"
        assert "is:issue" in query_arg

    def test_find_by_orchestration_key_non_dict_response_raises(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout="[]"))
        with pytest.raises(RuntimeError, match="Expected search response object"):
            provider._find_by_orchestration_key("abc123")

    def test_find_by_orchestration_key_invalid_items_shape_raises(self):
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(stdout=json.dumps({"items": [None]})),
        )
        with pytest.raises(RuntimeError, match="Expected first search result item to be an object"):
            provider._find_by_orchestration_key("abc123")

    def test_find_by_orchestration_key_non_list_items_raises(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout=json.dumps({"items": 42})))
        with pytest.raises(RuntimeError, match="Expected search response items to be a list"):
            provider._find_by_orchestration_key("abc123")

    def test_find_by_orchestration_key_multiple_matches_raises(self):
        """_find_by_orchestration_key raises RuntimeError when search returns multiple issues."""
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(
                stdout=json.dumps(
                    {
                        "items": [
                            {"number": 1, "html_url": "https://github.com/org/repo/issues/1"},
                            {"number": 2, "html_url": "https://github.com/org/repo/issues/2"},
                        ]
                    }
                )
            ),
        )
        with pytest.raises(RuntimeError, match="Ambiguous idempotency-key search"):
            provider._find_by_orchestration_key("abc123")

    def test_find_by_orchestration_key_incomplete_results_raises(self):
        """When GitHub returns incomplete_results:true, raises rather than treating empty items as a miss."""
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(stdout=json.dumps({"incomplete_results": True, "items": []})),
        )
        with pytest.raises(RuntimeError, match="incomplete results"):
            provider._find_by_orchestration_key("abc123")

    def test_find_by_orchestration_key_missing_number_raises(self):
        """A match lacking a valid positive 'number' is rejected rather than binding an empty id."""
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(stdout=json.dumps({"items": [{}]})),
        )
        with pytest.raises(RuntimeError, match="valid positive issue number"):
            provider._find_by_orchestration_key("abc123")

    def test_find_by_orchestration_key_non_positive_number_raises(self):
        """A match whose 'number' is not a positive integer is rejected."""
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(stdout=json.dumps({"items": [{"number": 0}]})),
        )
        with pytest.raises(RuntimeError, match="valid positive issue number"):
            provider._find_by_orchestration_key("abc123")
