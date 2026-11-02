"""Tests for GitHubActionsProvider.graphql() method."""

import json
from unittest.mock import Mock, patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.read_token_pool import ReadCredential
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

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_graphql_query_uses_pool_credential(self, mock_run_safe) -> None:
        pool = Mock()
        credential = ReadCredential("NOEKVIST_EXT_SWICA_CLASSIC_REPO_WORKFLOW_PAT", "pool-token", "pool-user")
        selection_calls: list[tuple[str, set[str]]] = []

        def select(resource: str, *, excluded: set[str]) -> ReadCredential:
            selection_calls.append((resource, set(excluded)))
            return credential

        pool.select.side_effect = select
        pool.default_is_active = False
        pool.default_token = "default-token"
        pool.default_identity = "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"

        class _Result:
            returncode = 0
            stdout = "HTTP/2 200 OK\nX-RateLimit-Remaining: 35\n\n" + json.dumps(
                {"data": {"viewer": {"login": "user"}}}
            )
            stderr = ""

        mock_run_safe.return_value = _Result()
        provider = GitHubActionsProvider(repo="owner/repo")

        with (
            patch.dict(
                "os.environ",
                {
                    "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "default-token",
                    "GH_TOKEN": "default-token",
                    "AI_PR_LOOP_CREDENTIAL_IDENTITY": "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT",
                },
            ),
            patch("agentic_devtools.cli.ci.github_provider._get_read_token_pool", return_value=pool),
        ):
            result = provider.graphql(query="query { viewer { login } }")

        assert result == {"data": {"viewer": {"login": "user"}}}
        assert mock_run_safe.call_args.kwargs["env"]["GH_TOKEN"] == "pool-token"
        assert selection_calls == [("graphql", set())]

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    @pytest.mark.parametrize(
        "query",
        [
            "mutation { addLabelsToLabelable(input: {}) { clientMutationId } }",
            "query Read { viewer { login } } mutation Write { addLabelsToLabelable(input: {}) { clientMutationId } }",
            "query Read { viewer { login } } subscription Updates { issues { id } }",
        ],
    )
    def test_graphql_documents_with_nonquery_operations_do_not_use_pool_credential(
        self, mock_run_safe, query: str
    ) -> None:
        pool = Mock()
        pool.default_token = "default-token"
        pool.default_identity = "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"

        class _Result:
            returncode = 0
            stdout = json.dumps({"data": {"addLabelsToLabelable": {"clientMutationId": None}}})
            stderr = ""

        mock_run_safe.return_value = _Result()
        provider = GitHubActionsProvider(repo="owner/repo")

        with (
            patch.dict(
                "os.environ",
                {
                    "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "default-token",
                    "GH_TOKEN": "default-token",
                    "AI_PR_LOOP_CREDENTIAL_IDENTITY": "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT",
                },
            ),
            patch("agentic_devtools.cli.ci.github_provider._get_read_token_pool", return_value=pool),
        ):
            result = provider.graphql(query=query)

        assert result == {"data": {"addLabelsToLabelable": {"clientMutationId": None}}}
        assert mock_run_safe.call_args.kwargs["env"] is None
        pool.select.assert_not_called()

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_graphql_query_fails_over_when_graphql_payload_is_rate_limited(self, mock_run_safe) -> None:
        first = ReadCredential("NOEKVIST_EXT_SWICA_CLASSIC_REPO_WORKFLOW_PAT", "first-token", "first")
        second = ReadCredential("CTRUX_EXT_SWICA_CLASSIC_REPO_WORKFLOW_PAT", "second-token", "second")
        pool = Mock()
        selection_calls: list[tuple[str, set[str]]] = []
        selections = iter([first, second])

        def select(resource: str, *, excluded: set[str]) -> ReadCredential:
            selection_calls.append((resource, set(excluded)))
            return next(selections)

        pool.select.side_effect = select
        pool.default_is_active = False
        pool.default_token = "default-token"
        pool.default_identity = "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"

        class _Limited:
            returncode = 0
            stdout = (
                "HTTP/2 200 OK\nRetry-After: 45\nX-RateLimit-Remaining: 0\n\n"
                '{"errors": [{"type": "RATE_LIMITED", "message": "rate limit exceeded"}]}'
            )
            stderr = ""

        class _Success:
            returncode = 0
            stdout = "HTTP/2 200 OK\nX-RateLimit-Remaining: 34\n\n" + json.dumps(
                {"data": {"viewer": {"login": "user"}}}
            )
            stderr = ""

        mock_run_safe.side_effect = [_Limited(), _Success()]
        provider = GitHubActionsProvider(repo="owner/repo")

        with (
            patch.dict(
                "os.environ",
                {
                    "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "default-token",
                    "GH_TOKEN": "default-token",
                    "AI_PR_LOOP_CREDENTIAL_IDENTITY": "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT",
                },
            ),
            patch("agentic_devtools.cli.ci.github_provider._get_read_token_pool", return_value=pool),
        ):
            result = provider.graphql(query="query { viewer { login } }")

        assert result == {"data": {"viewer": {"login": "user"}}}
        assert [call.kwargs["env"]["GH_TOKEN"] for call in mock_run_safe.call_args_list] == [
            "first-token",
            "second-token",
        ]
        assert selection_calls == [
            ("graphql", set()),
            ("graphql", {first.secret_name}),
        ]
        pool.mark_rate_limited.assert_called_once()
