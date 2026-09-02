"""Tests for GitHubActionsProvider.count_prs_without_labels() method."""

import json
from unittest.mock import patch

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


def _mock_run_safe_response(data):
    class _Result:
        returncode = 0
        stdout = json.dumps(data) if isinstance(data, (dict, list)) else data
        stderr = ""

    return _Result()


class TestCountPrsWithoutLabels:
    """Tests for GitHubActionsProvider.count_prs_without_labels()."""

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_returns_total_count(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_run_safe_response({"total_count": 15, "items": []})

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.count_prs_without_labels(exclude_labels=["audited", "in-progress"])

        assert result == 15

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_returns_zero_when_no_matches(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_run_safe_response({"total_count": 0, "items": []})

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.count_prs_without_labels(exclude_labels=["audited"])

        assert result == 0

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_omits_repo_qualifier_when_repo_is_empty(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_run_safe_response({"total_count": 3, "items": []})

        provider = GitHubActionsProvider(repo="")
        result = provider.count_prs_without_labels(exclude_labels=["audited"])

        assert result == 3
        args = mock_run_safe.call_args[0][0]
        endpoint = [a for a in args if "/search/issues" in a][0]
        assert "repo%3A" not in endpoint and "repo:" not in endpoint

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_includes_repo_in_query(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_run_safe_response({"total_count": 5, "items": []})

        provider = GitHubActionsProvider(repo="owner/repo")
        provider.count_prs_without_labels(exclude_labels=["audited"])

        args = mock_run_safe.call_args[0][0]
        # The endpoint should contain repo: qualifier in the query
        endpoint = [a for a in args if "/search/issues" in a]
        assert len(endpoint) == 1
        assert "repo%3Aowner%2Frepo" in endpoint[0] or "repo:owner/repo" in endpoint[0]
