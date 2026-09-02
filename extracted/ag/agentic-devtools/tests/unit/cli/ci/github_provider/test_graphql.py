"""Tests for GitHubActionsProvider.graphql() method."""

import json
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


class TestGraphql:
    """Tests for GitHubActionsProvider.graphql()."""

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_graphql_with_variables(self, mock_run_safe) -> None:
        expected = {"data": {"repository": {"id": "R_123"}}}

        class _Result:
            returncode = 0
            stdout = json.dumps(expected)
            stderr = ""

        mock_run_safe.return_value = _Result()

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.graphql(
            query="query { repository(owner: $o, name: $n) { id } }",
            variables={"o": "owner", "n": "repo"},
        )

        assert result == expected

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_graphql_without_variables(self, mock_run_safe) -> None:
        expected = {"data": {"viewer": {"login": "user"}}}

        class _Result:
            returncode = 0
            stdout = json.dumps(expected)
            stderr = ""

        mock_run_safe.return_value = _Result()

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.graphql(query="query { viewer { login } }")

        assert result == expected

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_raises_when_graphql_errors_are_returned(self, mock_run_safe) -> None:
        class _Result:
            returncode = 0
            stdout = json.dumps({"data": {"viewer": {"login": "user"}}, "errors": [{"message": "schema mismatch"}]})
            stderr = ""

        mock_run_safe.return_value = _Result()

        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RuntimeError, match="schema mismatch"):
            provider.graphql(query="query { viewer { login } }")

    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_graphql_rate_limit_preserves_response_metadata(self, mock_run_safe, _mock_sleep) -> None:
        class _Result:
            returncode = 0
            stdout = (
                "HTTP/2 200 OK\n"
                "Retry-After: 120\n"
                "X-RateLimit-Reset: 500\n"
                "X-RateLimit-Remaining: 0\n\n"
                '{"errors": [{"type": "RATE_LIMITED", "message": "rate limit exceeded"}]}'
            )
            stderr = ""

        mock_run_safe.return_value = _Result()
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(ProviderRateLimitError) as exc_info:
            provider.graphql(query="query { viewer { login } }")

        assert exc_info.value.retry_after_seconds == 120
        assert exc_info.value.reset_timestamp == 500
        assert exc_info.value.remaining == 0
