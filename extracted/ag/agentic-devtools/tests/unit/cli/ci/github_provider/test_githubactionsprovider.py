"""Tests for GitHubActionsProvider class."""

import json
import logging
import os
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.agent_assignment import AgentAssignmentResult
from agentic_devtools.cli.ci.github_provider import (
    SUPPRESSED_DEFERRAL_ISSUE_MARKER,
    GitHubActionsProvider,
)
from agentic_devtools.cli.ci.retry import ProviderRateLimitError, RetryableError


def _mock_run_safe_response(data):
    class _Result:
        returncode = 0
        stdout = json.dumps(data)
        stderr = ""

    return _Result()


def _page(nodes, *, has_next=False, cursor=None):
    return _mock_run_safe_response(
        {
            "data": {
                "node": {
                    "comments": {
                        "pageInfo": {"hasNextPage": has_next, "endCursor": cursor},
                        "nodes": nodes,
                    }
                }
            }
        }
    )


class TestGitHubActionsProvider:
    """Tests for GitHubActionsProvider methods."""

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_get_approver_login_returns_login_when_token_present(self, mock_gh_api, monkeypatch) -> None:
        """Returns the GitHub login when AGDT_PR_APPROVER_PAT is set and API succeeds."""
        monkeypatch.setenv("AGDT_PR_APPROVER_PAT", "ghp_testtoken")
        mock_gh_api.return_value = json.dumps({"login": "bot-user"})
        provider = GitHubActionsProvider(repo="owner/repo")
        assert provider.get_approver_login() == "bot-user"

    def test_get_approver_login_returns_empty_when_token_absent(self, monkeypatch) -> None:
        """Returns empty string when AGDT_PR_APPROVER_PAT is not set."""
        monkeypatch.delenv("AGDT_PR_APPROVER_PAT", raising=False)
        provider = GitHubActionsProvider(repo="owner/repo")
        assert provider.get_approver_login() == ""

    def test_get_approver_login_returns_empty_when_token_is_blank(self, monkeypatch) -> None:
        """Returns empty string when AGDT_PR_APPROVER_PAT is set but blank."""
        monkeypatch.setenv("AGDT_PR_APPROVER_PAT", "   ")
        provider = GitHubActionsProvider(repo="owner/repo")
        assert provider.get_approver_login() == ""

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_get_approver_login_returns_empty_when_api_raises(self, mock_gh_api, monkeypatch) -> None:
        """Returns empty string when the API call raises an exception."""
        monkeypatch.setenv("AGDT_PR_APPROVER_PAT", "ghp_testtoken")
        mock_gh_api.side_effect = RuntimeError("network error")
        provider = GitHubActionsProvider(repo="owner/repo")
        assert provider.get_approver_login() == ""

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_get_approver_login_reraises_provider_rate_limit_error(self, mock_gh_api, monkeypatch) -> None:
        """Provider rate limits must propagate so the outer loop can persist a cooldown."""
        monkeypatch.setenv("AGDT_PR_APPROVER_PAT", "ghp_testtoken")
        mock_gh_api.side_effect = ProviderRateLimitError(provider="github", credential_identity="AGDT_PR_APPROVER_PAT")
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(ProviderRateLimitError):
            provider.get_approver_login()

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_get_approver_login_returns_empty_when_login_is_not_a_string(self, mock_gh_api, monkeypatch) -> None:
        """Returns empty string when the 'login' field is not a string."""
        monkeypatch.setenv("AGDT_PR_APPROVER_PAT", "ghp_testtoken")
        mock_gh_api.return_value = json.dumps({"login": None})
        provider = GitHubActionsProvider(repo="owner/repo")
        assert provider.get_approver_login() == ""

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_get_approver_login_passes_token_to_gh_api(self, mock_gh_api, monkeypatch) -> None:
        """Passes the PAT token to the _gh_api call."""
        monkeypatch.setenv("AGDT_PR_APPROVER_PAT", "ghp_mytoken")
        mock_gh_api.return_value = json.dumps({"login": "some-bot"})
        provider = GitHubActionsProvider(repo="owner/repo")
        provider.get_approver_login()
        mock_gh_api.assert_called_once_with("/user", token="ghp_mytoken")

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_get_approver_login_caches_resolved_login_across_calls(self, mock_gh_api, monkeypatch) -> None:
        """Resolves the login once and returns the cached value on subsequent calls."""
        monkeypatch.setenv("AGDT_PR_APPROVER_PAT", "ghp_mytoken")
        mock_gh_api.return_value = json.dumps({"login": "bot-user"})
        provider = GitHubActionsProvider(repo="owner/repo")
        assert provider.get_approver_login() == "bot-user"
        assert provider.get_approver_login() == "bot-user"
        mock_gh_api.assert_called_once_with("/user", token="ghp_mytoken")

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_get_approver_login_caches_empty_result_without_reissuing_request(self, mock_gh_api, monkeypatch) -> None:
        """Caches the empty-string result so a failed resolution is not retried."""
        monkeypatch.setenv("AGDT_PR_APPROVER_PAT", "ghp_mytoken")
        mock_gh_api.side_effect = RuntimeError("network error")
        provider = GitHubActionsProvider(repo="owner/repo")
        assert provider.get_approver_login() == ""
        assert provider.get_approver_login() == ""
        mock_gh_api.assert_called_once_with("/user", token="ghp_mytoken")


class TestGitHubActionsProviderGetPrTokenLogin:
    """Tests for GitHubActionsProvider.get_pr_token_login()."""

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_returns_login_from_speckit_pr_token(self, mock_gh_api, monkeypatch) -> None:
        """Returns the login resolved from SPECKIT_PR_TOKEN via GET /user."""
        monkeypatch.setenv("SPECKIT_PR_TOKEN", "tok_abc123")
        mock_gh_api.return_value = json.dumps({"login": "dispatch-bot"})

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.get_pr_token_login()

        assert result == "dispatch-bot"
        mock_gh_api.assert_called_once_with("/user", token="tok_abc123")

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_returns_empty_string_when_token_absent(self, mock_gh_api, monkeypatch) -> None:
        """Returns empty string when SPECKIT_PR_TOKEN is not set."""
        monkeypatch.delenv("SPECKIT_PR_TOKEN", raising=False)

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.get_pr_token_login()

        assert result == ""
        mock_gh_api.assert_not_called()

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_returns_empty_string_when_token_whitespace_only(self, mock_gh_api, monkeypatch) -> None:
        """Returns empty string when SPECKIT_PR_TOKEN is whitespace-only."""
        monkeypatch.setenv("SPECKIT_PR_TOKEN", "   ")

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.get_pr_token_login()

        assert result == ""
        mock_gh_api.assert_not_called()

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_returns_empty_string_when_api_call_fails(self, mock_gh_api, monkeypatch) -> None:
        """Returns empty string when the GET /user call raises an exception."""
        monkeypatch.setenv("SPECKIT_PR_TOKEN", "tok_expired")
        mock_gh_api.side_effect = RuntimeError("401 Unauthorized")

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.get_pr_token_login()

        assert result == ""

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_reraises_provider_rate_limit_error(self, mock_gh_api, monkeypatch) -> None:
        """Provider rate limits must propagate so callers can pause instead of failing soft."""
        monkeypatch.setenv("SPECKIT_PR_TOKEN", "tok_abc123")
        mock_gh_api.side_effect = ProviderRateLimitError(provider="github", credential_identity="SPECKIT_PR_TOKEN")

        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(ProviderRateLimitError):
            provider.get_pr_token_login()

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_returns_empty_string_when_login_missing_from_response(self, mock_gh_api, monkeypatch) -> None:
        """Returns empty string when the API response lacks a 'login' key."""
        monkeypatch.setenv("SPECKIT_PR_TOKEN", "tok_abc123")
        mock_gh_api.return_value = json.dumps({"id": 1, "name": "Bot"})

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.get_pr_token_login()

        assert result == ""

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_returns_empty_string_when_login_is_non_string(self, mock_gh_api, monkeypatch) -> None:
        """Returns empty string when 'login' is not a string (e.g., None or int)."""
        monkeypatch.setenv("SPECKIT_PR_TOKEN", "tok_abc123")
        mock_gh_api.return_value = json.dumps({"login": None})

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.get_pr_token_login()

        assert result == ""

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_caches_result_on_second_call(self, mock_gh_api, monkeypatch) -> None:
        """The resolved login is cached so GET /user is called at most once per instance."""
        monkeypatch.setenv("SPECKIT_PR_TOKEN", "tok_abc123")
        mock_gh_api.return_value = json.dumps({"login": "dispatch-bot"})

        provider = GitHubActionsProvider(repo="owner/repo")
        first = provider.get_pr_token_login()
        second = provider.get_pr_token_login()

        assert first == second == "dispatch-bot"
        assert mock_gh_api.call_count == 1

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_caches_empty_string_result(self, mock_gh_api, monkeypatch) -> None:
        """The empty-string result (failure) is also cached to avoid repeated API calls."""
        monkeypatch.setenv("SPECKIT_PR_TOKEN", "tok_bad")
        mock_gh_api.side_effect = RuntimeError("Unauthorized")

        provider = GitHubActionsProvider(repo="owner/repo")
        first = provider.get_pr_token_login()
        second = provider.get_pr_token_login()

        assert first == second == ""
        assert mock_gh_api.call_count == 1


class TestGitHubActionsProviderResolveTreeSha:
    """Tests for the tree-SHA resolution helper used by squash_post_repair."""

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_resolves_tree_without_fetch(self, mock_run_git) -> None:
        mock_run_git.return_value = "tree-sha\n"
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider._resolve_tree_sha("HEAD")

        assert result == "tree-sha"
        mock_run_git.assert_called_once_with(["rev-parse", "HEAD^{tree}"])

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_fetches_before_resolving_when_requested(self, mock_run_git) -> None:
        mock_run_git.side_effect = ["", "tree-sha\n"]
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider._resolve_tree_sha("abc123", fetch=True)

        assert result == "tree-sha"
        mock_run_git.assert_any_call(["fetch", "origin", "abc123"])
        mock_run_git.assert_any_call(["rev-parse", "abc123^{tree}"])

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_returns_empty_string_on_git_error(self, mock_run_git) -> None:
        mock_run_git.side_effect = RuntimeError("bad object")
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider._resolve_tree_sha("abc123", fetch=True)

        assert result == ""


class TestGitHubActionsProviderResolveCommitSha:
    """Tests for the commit-SHA resolution helper used by squash_post_repair."""

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_resolves_commit_sha_for_head(self, mock_run_git) -> None:
        mock_run_git.return_value = "abc1234567890\n"
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider._resolve_commit_sha("HEAD")

        assert result == "abc1234567890"
        mock_run_git.assert_called_once_with(["rev-parse", "HEAD"])

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_returns_empty_string_on_git_error(self, mock_run_git) -> None:
        mock_run_git.side_effect = RuntimeError("bad object")
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider._resolve_commit_sha("HEAD")

        assert result == ""


class TestGitHubActionsProviderCollectThreadComments:
    """Tests for inner review-thread comment pagination."""

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_returns_first_page_when_no_further_pages(self, mock_run_safe):
        """A thread that fits in one page needs no extra API call."""
        provider = GitHubActionsProvider(repo="owner/repo")
        thread = {
            "id": "THREAD_1",
            "comments": {
                "pageInfo": {"hasNextPage": False, "endCursor": "cursor-1"},
                "nodes": [{"databaseId": 1}],
            },
        }

        result = provider._collect_thread_comments(thread)

        assert result == [{"databaseId": 1}]
        assert mock_run_safe.call_count == 0

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_returns_empty_list_for_thread_without_comments(self, mock_run_safe):
        """A thread node missing its comments connection yields no comments."""
        provider = GitHubActionsProvider(repo="owner/repo")

        assert provider._collect_thread_comments({"id": "THREAD_1"}) == []
        assert mock_run_safe.call_count == 0

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_ignores_non_dict_page_info(self, mock_run_safe):
        """A malformed pageInfo is treated as 'no further pages'."""
        provider = GitHubActionsProvider(repo="owner/repo")
        thread = {"id": "THREAD_1", "comments": {"pageInfo": None, "nodes": [{"databaseId": 1}]}}

        assert provider._collect_thread_comments(thread) == [{"databaseId": 1}]
        assert mock_run_safe.call_count == 0

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_warns_and_truncates_when_first_page_cursor_missing(self, mock_run_safe, caplog):
        """When hasNextPage=true without endCursor, warn and return the available page."""
        provider = GitHubActionsProvider(repo="owner/repo")
        thread = {
            "id": "THREAD_1",
            "comments": {
                "pageInfo": {"hasNextPage": True, "endCursor": None},
                "nodes": [{"databaseId": 1}],
            },
        }

        with caplog.at_level("WARNING"):
            result = provider._collect_thread_comments(thread)

        assert result == [{"databaseId": 1}]
        assert mock_run_safe.call_count == 0
        assert "hasNextPage=true but no endCursor" in caplog.text

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_warns_and_truncates_when_continuation_cursor_missing(self, mock_run_safe, caplog):
        """When a continuation page lacks endCursor, warn and stop pagination."""
        mock_run_safe.side_effect = [
            _page([{"databaseId": 2}], has_next=True, cursor=None),
        ]
        provider = GitHubActionsProvider(repo="owner/repo")
        thread = {
            "id": "THREAD_1",
            "comments": {
                "pageInfo": {"hasNextPage": True, "endCursor": "cursor-1"},
                "nodes": [{"databaseId": 1}],
            },
        }

        with caplog.at_level("WARNING"):
            result = provider._collect_thread_comments(thread)

        assert result == [{"databaseId": 1}, {"databaseId": 2}]
        assert mock_run_safe.call_count == 1
        assert "continuation pageInfo has hasNextPage=true but no endCursor" in caplog.text

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_follows_multiple_comment_pages(self, mock_run_safe):
        """Comments beyond the first page are fetched until the connection ends."""
        mock_run_safe.side_effect = [
            _page([{"databaseId": 2}], has_next=True, cursor="cursor-2"),
            _page([{"databaseId": 3}], has_next=False, cursor=None),
        ]
        provider = GitHubActionsProvider(repo="owner/repo")
        thread = {
            "id": "THREAD_1",
            "comments": {
                "pageInfo": {"hasNextPage": True, "endCursor": "cursor-1"},
                "nodes": [{"databaseId": 1}],
            },
        }

        result = provider._collect_thread_comments(thread)

        assert result == [{"databaseId": 1}, {"databaseId": 2}, {"databaseId": 3}]
        assert mock_run_safe.call_count == 2
        first_payload = json.loads(mock_run_safe.call_args_list[0].kwargs["input"])
        assert first_payload["variables"] == {"threadId": "THREAD_1", "commentsCursor": "cursor-1"}
        second_payload = json.loads(mock_run_safe.call_args_list[1].kwargs["input"])
        assert second_payload["variables"] == {"threadId": "THREAD_1", "commentsCursor": "cursor-2"}

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_raises_on_null_node_payload(self, mock_run_safe):
        """A response with data.node=null raises RuntimeError instead of truncating silently."""
        mock_run_safe.return_value = _mock_run_safe_response({"data": None})
        provider = GitHubActionsProvider(repo="owner/repo")
        thread = {
            "id": "THREAD_1",
            "comments": {
                "pageInfo": {"hasNextPage": True, "endCursor": "cursor-1"},
                "nodes": [{"databaseId": 1}],
            },
        }

        with pytest.raises(RuntimeError, match="unexpected node shape"):
            provider._collect_thread_comments(thread)

    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_raises_retryable_on_rate_limit_error_in_page_response(self, mock_run_safe, _mock_sleep):
        """A GraphQL response with a rate-limit message raises ProviderRateLimitError after retries."""
        mock_run_safe.return_value = _mock_run_safe_response({"errors": [{"message": "rate limited"}], "data": None})
        provider = GitHubActionsProvider(repo="owner/repo")
        thread = {
            "id": "THREAD_1",
            "comments": {
                "pageInfo": {"hasNextPage": True, "endCursor": "cursor-1"},
                "nodes": [{"databaseId": 1}],
            },
        }

        with pytest.raises(ProviderRateLimitError):
            provider._collect_thread_comments(thread)

    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_raises_retryable_on_rate_limited_type_in_page_response(self, mock_run_safe, _mock_sleep):
        """A GraphQL error with type=RATE_LIMITED raises ProviderRateLimitError after retries."""
        mock_run_safe.return_value = _mock_run_safe_response(
            {"errors": [{"type": "RATE_LIMITED", "message": "API rate limit exceeded"}], "data": None}
        )
        provider = GitHubActionsProvider(repo="owner/repo")
        thread = {
            "id": "THREAD_1",
            "comments": {
                "pageInfo": {"hasNextPage": True, "endCursor": "cursor-1"},
                "nodes": [{"databaseId": 1}],
            },
        }

        with pytest.raises(ProviderRateLimitError) as exc_info:
            provider._collect_thread_comments(thread)
        assert exc_info.value.is_rate_limit is True

    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_raises_provider_error_on_server_error_in_page_response(self, mock_run_safe, _mock_sleep):
        """A server-error GraphQL error raises RetryableError after retries."""
        mock_run_safe.return_value = _mock_run_safe_response(
            {"errors": [{"message": "internal server error occurred"}], "data": None}
        )
        provider = GitHubActionsProvider(repo="owner/repo")
        thread = {
            "id": "THREAD_1",
            "comments": {
                "pageInfo": {"hasNextPage": True, "endCursor": "cursor-1"},
                "nodes": [{"databaseId": 1}],
            },
        }

        with pytest.raises(RetryableError):
            provider._collect_thread_comments(thread)

    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_raises_runtime_on_permanent_graphql_error_in_page_response(self, mock_run_safe, _mock_sleep):
        """A non-transient GraphQL error raises RuntimeError."""
        mock_run_safe.return_value = _mock_run_safe_response(
            {"errors": [{"message": "Field 'foo' doesn't exist on type 'Bar'"}], "data": None}
        )
        provider = GitHubActionsProvider(repo="owner/repo")
        thread = {
            "id": "THREAD_1",
            "comments": {
                "pageInfo": {"hasNextPage": True, "endCursor": "cursor-1"},
                "nodes": [{"databaseId": 1}],
            },
        }

        with pytest.raises(RuntimeError, match="Thread comment pagination GraphQL error"):
            provider._collect_thread_comments(thread)

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_raises_with_generic_message_when_errors_array_has_no_dicts(self, mock_run_safe):
        """An errors array with no dict entries raises RuntimeError with a generic message."""
        mock_run_safe.return_value = _mock_run_safe_response({"errors": ["not a dict"], "data": None})
        provider = GitHubActionsProvider(repo="owner/repo")
        thread = {
            "id": "THREAD_1",
            "comments": {
                "pageInfo": {"hasNextPage": True, "endCursor": "cursor-1"},
                "nodes": [{"databaseId": 1}],
            },
        }

        with pytest.raises(RuntimeError, match="Unknown GraphQL error"):
            provider._collect_thread_comments(thread)

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_raises_when_node_comments_not_a_dict(self, mock_run_safe):
        """When data.node.comments is not a dict RuntimeError is raised."""
        mock_run_safe.return_value = _mock_run_safe_response({"data": {"node": {"comments": None}}})
        provider = GitHubActionsProvider(repo="owner/repo")
        thread = {
            "id": "THREAD_1",
            "comments": {
                "pageInfo": {"hasNextPage": True, "endCursor": "cursor-1"},
                "nodes": [{"databaseId": 1}],
            },
        }

        with pytest.raises(RuntimeError, match="unexpected comments shape"):
            provider._collect_thread_comments(thread)

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_warns_and_truncates_when_thread_node_id_missing(self, mock_run_safe, caplog):
        """Without a node id the remaining pages cannot be fetched, so warn loudly."""
        provider = GitHubActionsProvider(repo="owner/repo")
        thread = {
            "comments": {
                "pageInfo": {"hasNextPage": True, "endCursor": "cursor-1"},
                "nodes": [{"databaseId": 1}],
            },
        }

        with caplog.at_level("WARNING"):
            result = provider._collect_thread_comments(thread)

        assert result == [{"databaseId": 1}]
        assert mock_run_safe.call_count == 0
        assert "no node id" in caplog.text


class TestGitHubActionsProviderPostCommentAsPrToken:
    """Tests for GitHubActionsProvider.post_comment_as_pr_token."""

    @patch.dict(os.environ, {"SPECKIT_PR_TOKEN": "pr-token"}, clear=False)
    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_post_comment_as_pr_token_uses_pr_token(self, mock_run_safe) -> None:
        """post_comment_as_pr_token authenticates with SPECKIT_PR_TOKEN via GH_TOKEN env var."""
        mock_run_safe.return_value = _mock_run_safe_response({"id": 77})

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.post_comment_as_pr_token(7, "token body")

        assert result == 77
        kwargs = mock_run_safe.call_args[1]
        env = kwargs.get("env")
        assert isinstance(env, dict)
        assert env.get("GH_TOKEN") == "pr-token"

    @patch.dict(os.environ, {}, clear=True)
    def test_post_comment_as_pr_token_raises_without_token(self) -> None:
        """post_comment_as_pr_token raises RuntimeError when SPECKIT_PR_TOKEN is not set."""
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RuntimeError, match="SPECKIT_PR_TOKEN is required"):
            provider.post_comment_as_pr_token(7, "token body")


def _assignment(*, success: bool = True, session_confirmed: bool = True, error: str = "") -> AgentAssignmentResult:
    return AgentAssignmentResult(
        success=success,
        method="coding_agent_task",
        task_id="task-77",
        task_url="https://example/task-77",
        attempts=1,
        token_identity="SPECKIT_PR_TOKEN",
        session_confirmed=session_confirmed,
        error=error,
    )


def _deferral_response(pr_node: object) -> dict:
    return {"data": {"repository": {"pullRequest": pr_node}}}


class TestCountOpenIssuesWithLabel:
    """Tests for GitHubActionsProvider.count_open_issues_with_label."""

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_returns_total_count_and_scopes_query_to_repo(self, mock_gh_api) -> None:
        mock_gh_api.return_value = json.dumps({"total_count": 3, "items": []})
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")

        assert provider.count_open_issues_with_label("suppressed-comment-follow-up") == 3

        endpoint = mock_gh_api.call_args.args[0]
        assert endpoint.startswith("/search/issues?q=")
        assert "repo%3Aswai-factory%2Fagentic-devtools" in endpoint
        assert "suppressed-comment-follow-up" in endpoint

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_raises_when_total_count_missing_or_malformed(self, mock_gh_api) -> None:
        mock_gh_api.return_value = json.dumps({"total_count": "many"})
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")

        with pytest.raises(RuntimeError, match="total_count"):
            provider.count_open_issues_with_label("suppressed-comment-follow-up")

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_raises_when_total_count_is_boolean(self, mock_gh_api) -> None:
        mock_gh_api.return_value = json.dumps({"total_count": True})
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")

        with pytest.raises(RuntimeError, match="total_count"):
            provider.count_open_issues_with_label("suppressed-comment-follow-up")

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_omits_repo_qualifier_when_repo_is_unset(self, mock_gh_api) -> None:
        mock_gh_api.return_value = json.dumps({"total_count": 0})
        provider = GitHubActionsProvider(repo="")

        assert provider.count_open_issues_with_label("suppressed-comment-follow-up") == 0
        assert "repo%3A" not in mock_gh_api.call_args.args[0]


class TestFindDeferralIssue:
    """Tests for GitHubActionsProvider.find_deferral_issue."""

    @staticmethod
    def _issue_body(pr: int, review_id: int) -> str:
        payload = json.dumps({"pr": pr, "review_id": review_id, "base_sha": "a" * 40, "finding_count": 2})
        return f"{SUPPRESSED_DEFERRAL_ISSUE_MARKER}{payload} -->\n\n## Deferred suppressed findings\n"

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_returns_issue_number_when_marker_payload_matches(self, mock_gh_api) -> None:
        mock_gh_api.return_value = json.dumps(
            {
                "items": [
                    {"number": 41, "body": self._issue_body(11, 7)},
                    {"number": 4242, "body": self._issue_body(11, 42)},
                ]
            }
        )
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")

        assert provider.find_deferral_issue(pr_number=11, review_id=42) == 4242
        endpoint = mock_gh_api.call_args.args[0]
        assert "suppressed-comment-follow-up" in endpoint
        assert "is%3Aopen" in endpoint

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_returns_none_when_no_issue_matches(self, mock_gh_api) -> None:
        mock_gh_api.return_value = json.dumps(
            {
                "items": [
                    {"number": 41},
                    {"number": 99, "body": self._issue_body(11, 7)},
                ]
            }
        )
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")

        assert provider.find_deferral_issue(pr_number=11, review_id=42) is None

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_raises_when_search_payload_is_not_a_mapping(self, mock_gh_api) -> None:
        mock_gh_api.return_value = json.dumps([])
        provider = GitHubActionsProvider(repo="")

        with pytest.raises(RuntimeError, match="top-level object"):
            provider.find_deferral_issue(pr_number=11, review_id=42)
        assert "repo%3A" not in mock_gh_api.call_args.args[0]

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_raises_when_search_items_include_non_object(self, mock_gh_api) -> None:
        mock_gh_api.return_value = json.dumps({"items": ["bad-shape"]})
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")

        with pytest.raises(RuntimeError, match="non-object item"):
            provider.find_deferral_issue(pr_number=11, review_id=42)

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_raises_when_search_items_missing_or_malformed(self, mock_gh_api) -> None:
        mock_gh_api.return_value = json.dumps({"items": "not-a-list"})
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")

        with pytest.raises(RuntimeError, match="items"):
            provider.find_deferral_issue(pr_number=11, review_id=42)

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_raises_when_matched_marker_has_invalid_issue_number(self, mock_gh_api) -> None:
        mock_gh_api.return_value = json.dumps({"items": [{"number": 0, "body": self._issue_body(11, 42)}]})
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")

        with pytest.raises(RuntimeError, match="invalid issue number"):
            provider.find_deferral_issue(pr_number=11, review_id=42)

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_raises_when_matched_issue_number_is_boolean(self, mock_gh_api) -> None:
        mock_gh_api.return_value = json.dumps({"items": [{"number": True, "body": self._issue_body(11, 42)}]})
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")

        with pytest.raises(RuntimeError, match="invalid issue number"):
            provider.find_deferral_issue(pr_number=11, review_id=42)


class TestCreateDeferralIssue:
    """Tests for GitHubActionsProvider.create_deferral_issue."""

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_creates_issue_with_marker_labels_and_findings(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_run_safe_response({"number": 4242})
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")

        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token-value"}, clear=True):
            issue_number = provider.create_deferral_issue(
                pr_number=11,
                review_id=42,
                base_sha="abc1234",
                findings=[("specs/3672/spec.md", "The criteria are ambiguous.")],
                labels=["suppressed-comment-follow-up"],
            )

        assert issue_number == 4242
        call = mock_run_safe.call_args
        assert "/repos/swai-factory/agentic-devtools/issues" in call.args[0]
        assert call.kwargs["env"]["GH_TOKEN"] == "token-value"
        payload = json.loads(call.kwargs["input"])
        body = payload["body"]
        assert body.startswith(SUPPRESSED_DEFERRAL_ISSUE_MARKER)
        assert payload["labels"] == ["suppressed-comment-follow-up"]
        assert "### Finding 1 — `specs/3672/spec.md`" in body
        assert "The criteria are ambiguous." in body

    def test_raises_when_speckit_token_missing(self) -> None:
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(RuntimeError, match="SPECKIT_PR_TOKEN"):
                provider.create_deferral_issue(
                    pr_number=11,
                    review_id=42,
                    base_sha="abc1234",
                    findings=[],
                    labels=[],
                )

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_raises_when_issue_number_missing_from_response(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_run_safe_response({})
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")

        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token-value"}, clear=True):
            with pytest.raises(RuntimeError, match="missing issue number"):
                provider.create_deferral_issue(
                    pr_number=11,
                    review_id=42,
                    base_sha="abc1234",
                    findings=[],
                    labels=[],
                )

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_raises_when_issue_number_is_zero(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_run_safe_response({"number": 0})
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")

        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token-value"}, clear=True):
            with pytest.raises(RuntimeError, match="missing issue number"):
                provider.create_deferral_issue(
                    pr_number=11,
                    review_id=42,
                    base_sha="abc1234",
                    findings=[],
                    labels=[],
                )

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_raises_when_issue_number_is_negative(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_run_safe_response({"number": -1})
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")

        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token-value"}, clear=True):
            with pytest.raises(RuntimeError, match="missing issue number"):
                provider.create_deferral_issue(
                    pr_number=11,
                    review_id=42,
                    base_sha="abc1234",
                    findings=[],
                    labels=[],
                )

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_raises_when_issue_number_is_boolean(self, mock_run_safe) -> None:
        """bool is a subclass of int; True (==1) must still be rejected as an issue number."""
        mock_run_safe.return_value = _mock_run_safe_response({"number": True})
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")

        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token-value"}, clear=True):
            with pytest.raises(RuntimeError, match="missing issue number"):
                provider.create_deferral_issue(
                    pr_number=11,
                    review_id=42,
                    base_sha="abc1234",
                    findings=[],
                    labels=[],
                )

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_does_not_retry_non_idempotent_issue_creation(self, mock_gh_api) -> None:
        mock_gh_api.side_effect = RetryableError("GitHub API error: HTTP 503")
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")

        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token-value"}, clear=True):
            with pytest.raises(RetryableError, match="HTTP 503"):
                provider.create_deferral_issue(
                    pr_number=11,
                    review_id=42,
                    base_sha="abc1234",
                    findings=[],
                    labels=["suppressed-comment-follow-up"],
                )

        assert mock_gh_api.call_count == 1


class TestDispatchSuppressedTriage:
    """Tests for GitHubActionsProvider.dispatch_suppressed_triage."""

    @patch("agentic_devtools.cli.ci.github_provider.assign_issue_to_agent")
    @patch("agentic_devtools.cli.ci.github_provider._read_repo_file")
    def test_dispatches_via_shared_assignment_helper(self, mock_read_repo_file, mock_assign) -> None:
        mock_read_repo_file.return_value = "# prompt"
        mock_assign.return_value = _assignment()
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")

        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token-value"}, clear=True):
            result = provider.dispatch_suppressed_triage(issue_number=4242, pr_number=11, review_id=42)

        assert result.success is True
        kwargs = mock_assign.call_args.kwargs
        assert kwargs["repo"] == "swai-factory/agentic-devtools"
        assert kwargs["issue_number"] == 4242
        assert kwargs["custom_agent"] == "agdt.suppressed-comment-triage.evaluate"
        assert kwargs["token_env_vars"] == ("SPECKIT_PR_TOKEN",)
        assert "#11" in kwargs["problem_statement"]
        assert "42" in kwargs["problem_statement"]
        assert kwargs["problem_statement"] == kwargs["custom_instructions"]

    @patch("agentic_devtools.cli.ci.github_provider.assign_issue_to_agent")
    def test_raises_when_speckit_token_missing(self, mock_assign) -> None:
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(RuntimeError, match="SPECKIT_PR_TOKEN"):
                provider.dispatch_suppressed_triage(issue_number=4242, pr_number=11, review_id=42)
        mock_assign.assert_not_called()

    @patch("agentic_devtools.cli.ci.github_provider.assign_issue_to_agent")
    @patch("agentic_devtools.cli.ci.github_provider._read_repo_file")
    def test_raises_when_prompt_file_cannot_be_read(self, mock_read_repo_file, mock_assign) -> None:
        mock_read_repo_file.return_value = ""
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")

        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token-value"}, clear=True):
            with pytest.raises(RuntimeError, match="Could not read required agent prompt file"):
                provider.dispatch_suppressed_triage(issue_number=4242, pr_number=11, review_id=42)

        mock_assign.assert_not_called()

    @patch("agentic_devtools.cli.ci.github_provider.assign_issue_to_agent")
    @patch("agentic_devtools.cli.ci.github_provider._read_repo_file")
    def test_raises_when_assignment_fails(self, mock_read_repo_file, mock_assign) -> None:
        mock_read_repo_file.return_value = "# prompt"
        mock_assign.return_value = _assignment(success=False, error="all methods failed")
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")

        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token-value"}, clear=True):
            with pytest.raises(RuntimeError, match="all methods failed"):
                provider.dispatch_suppressed_triage(issue_number=4242, pr_number=11, review_id=42)

    @patch("agentic_devtools.cli.ci.github_provider.assign_issue_to_agent")
    @patch("agentic_devtools.cli.ci.github_provider._read_repo_file")
    def test_succeeds_when_session_is_not_confirmed(
        self,
        mock_read_repo_file,
        mock_assign,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        mock_read_repo_file.return_value = "# prompt"
        mock_assign.return_value = _assignment(session_confirmed=False)
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")

        with (
            caplog.at_level(logging.WARNING, logger="agentic_devtools.cli.ci.github_provider"),
            patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token-value"}, clear=True),
        ):
            result = provider.dispatch_suppressed_triage(issue_number=4242, pr_number=11, review_id=42)

        assert result.success is True
        assert "session_confirmed=False" in caplog.text


class TestListLinkedIssueLabels:
    """Tests for GitHubActionsProvider.list_linked_issue_labels."""

    def test_returns_label_names_of_linked_issues(self) -> None:
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")
        pr_node = {
            "closingIssuesReferences": {
                "pageInfo": {"hasNextPage": False},
                "nodes": [
                    {
                        "labels": {
                            "pageInfo": {"hasNextPage": False},
                            "nodes": [{"name": "enhancement"}, {"name": "suppressed-comment-follow-up"}],
                        }
                    },
                ],
            }
        }

        with patch.object(provider, "graphql", return_value=_deferral_response(pr_node)) as mock_graphql:
            labels = provider.list_linked_issue_labels(11)

        assert labels == ["enhancement", "suppressed-comment-follow-up"]
        assert mock_graphql.call_args.kwargs["variables"] == {
            "owner": "swai-factory",
            "repo": "agentic-devtools",
            "number": 11,
        }

    def test_raises_when_closing_issues_references_truncated(self) -> None:
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")
        pr_node = {
            "closingIssuesReferences": {
                "pageInfo": {"hasNextPage": True},
                "nodes": [{"labels": {"nodes": [{"name": "suppressed-comment-follow-up"}]}}],
            }
        }

        with patch.object(provider, "graphql", return_value=_deferral_response(pr_node)):
            with pytest.raises(RuntimeError, match="more than 100 closing issue references"):
                provider.list_linked_issue_labels(11)

    def test_raises_when_pr_node_missing(self) -> None:
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")
        with patch.object(provider, "graphql", return_value=_deferral_response(None)):
            with pytest.raises(RuntimeError, match="pullRequest"):
                provider.list_linked_issue_labels(11)

    def test_raises_when_repository_missing(self) -> None:
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")
        with patch.object(provider, "graphql", return_value={"data": {"repository": None}}):
            with pytest.raises(RuntimeError, match="repository"):
                provider.list_linked_issue_labels(11)

    def test_raises_when_closing_issues_references_absent(self) -> None:
        """A missing closingIssuesReferences key is an unexpected response shape — raise to fail closed."""
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")
        pr_node: dict[str, object] = {}  # no closingIssuesReferences key

        with patch.object(provider, "graphql", return_value=_deferral_response(pr_node)):
            with pytest.raises(RuntimeError, match="closingIssuesReferences"):
                provider.list_linked_issue_labels(11)

    def test_raises_when_linked_issue_node_is_malformed(self) -> None:
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")
        pr_node = {
            "closingIssuesReferences": {
                "pageInfo": {"hasNextPage": False},
                "nodes": ["not-a-dict"],
            }
        }

        with patch.object(provider, "graphql", return_value=_deferral_response(pr_node)):
            with pytest.raises(RuntimeError, match="closingIssuesReferences.nodes\\[0\\]"):
                provider.list_linked_issue_labels(11)

    def test_raises_when_linked_issue_labels_are_truncated(self) -> None:
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")
        pr_node = {
            "closingIssuesReferences": {
                "pageInfo": {"hasNextPage": False},
                "nodes": [
                    {
                        "labels": {
                            "pageInfo": {"hasNextPage": True},
                            "nodes": [{"name": "suppressed-comment-follow-up"}],
                        }
                    },
                ],
            }
        }

        with patch.object(provider, "graphql", return_value=_deferral_response(pr_node)):
            with pytest.raises(RuntimeError, match="more than 100 labels"):
                provider.list_linked_issue_labels(11)

    def test_returns_empty_when_no_linked_issues(self) -> None:
        """An empty nodes list is a valid response (PR has no linked issues)."""
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")
        pr_node = {
            "closingIssuesReferences": {
                "pageInfo": {"hasNextPage": False},
                "nodes": [],
            }
        }

        with patch.object(provider, "graphql", return_value=_deferral_response(pr_node)):
            labels = provider.list_linked_issue_labels(11)

        assert labels == []
