"""Tests for GitHubActionsProvider class."""

import itertools
import json
import logging
import os
from types import SimpleNamespace
from typing import Any
from unittest.mock import call, patch

import pytest

from agentic_devtools.cli.ci.agent_assignment import AgentAssignmentResult
from agentic_devtools.cli.ci.github_provider import (
    _MAX_COMMENT_BODY_CHARS,
    SUPPRESSED_DEFERRAL_ISSUE_MARKER,
    GitHubActionsProvider,
    _raise_for_graphql_errors,
)
from agentic_devtools.cli.ci.models import AgentTaskInventoryLoadResult, CheckRunStatus, ReviewCommentInfo, ReviewInfo
from agentic_devtools.cli.ci.provider import RepairDispatchNotAttemptedError
from agentic_devtools.cli.ci.repair_accounting import repair_work_key
from agentic_devtools.cli.ci.retry import ProviderRateLimitError, RetryableError
from agentic_devtools.cli.ci.review_thread_promotion import AnchorSelection, ReviewThreadAnchor
from agentic_devtools.cli.ci.review_thread_tree_paths import _source_path_exists_in_captured_trees
from agentic_devtools.cli.github.ccr_review_format import CCRFinding
from tests.unit.cli.ci._github_response_fixtures import _mock_run_safe_response, _page, _preflight_responses


class TestGitHubActionsProvider:
    """Tests for GitHubActionsProvider methods."""

    @pytest.mark.parametrize("status", [200, 401, 403, 404, None])
    def test_preflight_cached_by_actual_base_repository(self, monkeypatch, status) -> None:
        monkeypatch.setenv("AGDT_PR_APPROVER_PAT", "offline-credential" if status is not None else "")
        responses, capability, endpoints = _preflight_responses(status)
        with patch("agentic_devtools.cli.ci.github_provider.run_safe") as runner:
            runner.side_effect = responses
            provider = GitHubActionsProvider(repo="head/fork")
            first = provider.get_approver_preflight("base/one")
            assert provider.get_approver_preflight("base/one") is first
            second = provider.get_approver_preflight("base/two")
        assert first.blocking_capability == second.blocking_capability == capability
        assert [item.args[0][2] for item in runner.call_args_list] == endpoints
        assert all(item.args[0][4] == "GET" for item in runner.call_args_list)
        assert "offline-credential" not in repr(first)

    def test_binary_git_output_preserves_carriage_return_paths(self, monkeypatch: pytest.MonkeyPatch) -> None:
        provider = GitHubActionsProvider(repo="owner/repo")
        source_path = "src/\u200ba\rb.py"
        responses = iter((b"", source_path.encode("utf-8") + b"\0"))
        calls: list[dict[str, Any]] = []

        def run_safe(*_args: Any, **kwargs: Any) -> SimpleNamespace:
            calls.append(kwargs)
            return SimpleNamespace(returncode=0, stdout=next(responses), stderr=b"")

        monkeypatch.setattr("agentic_devtools.cli.ci.github_provider.run_safe", run_safe)

        assert _source_path_exists_in_captured_trees("base", "head", provider._run_git, source_path) is True
        assert [call["text"] for call in calls] == [False, False]

    def test_binary_git_output_reports_failed_commands(self, monkeypatch: pytest.MonkeyPatch) -> None:
        provider = GitHubActionsProvider(repo="owner/repo")

        def run_safe(*_args: Any, **_kwargs: Any) -> SimpleNamespace:
            return SimpleNamespace(returncode=1, stdout=b"", stderr=b"missing tree")

        monkeypatch.setattr("agentic_devtools.cli.ci.github_provider.run_safe", run_safe)

        with pytest.raises(RuntimeError, match="git ls-tree -z failed: b'missing tree'"):
            provider._run_git(["ls-tree", "-z"])

    def test_review_repair_evidence_excludes_failed_checks(self, monkeypatch) -> None:
        monkeypatch.delenv("AGDT_USE_AGENT_TASKS_API", raising=False)
        provider = GitHubActionsProvider(repo="owner/repo")
        comment = ReviewCommentInfo(id=11, path="src/app.py", body="Fix this", html_url="")
        failed_check = CheckRunStatus(id=3, name="Build", status="completed", conclusion="failure")
        with (
            patch("agentic_devtools.cli.ci.github_provider._require_default_workflow_token", return_value="token"),
            patch("agentic_devtools.cli.ci.github_provider._build_repair_comment", return_value="@copilot repair"),
            patch.object(provider, "_post_repair_comment", return_value='{"id": 99}') as post_repair,
        ):
            provider.dispatch_repair(
                pr_number=42,
                head_sha="head",
                repair_type="review",
                failed_checks=[failed_check],
                review_comments=[comment],
                review_id=100,
            )

        expected_key = repair_work_key(100, [comment], [])
        expected_marker = f"<!-- repair-dispatch:work:head:100:{expected_key} -->"
        posted_body = post_repair.call_args.kwargs["body"]
        assert posted_body.endswith(expected_marker)

    def test_rate_limited_agent_task_post_preserves_pending_intent_without_fallback(self, monkeypatch) -> None:
        monkeypatch.setenv("AGDT_USE_AGENT_TASKS_API", "true")
        provider = GitHubActionsProvider(repo="owner/repo")
        retryable = RetryableError(
            "GitHub API rate limited (HTTP 429)",
            retry_after=15,
            reset_timestamp=1234,
            remaining=0,
            provider="github",
            credential_identity="DEFAULT_CLASSIC_REPO_WORKFLOW_PAT",
            source="retry-after",
            is_rate_limit=True,
        )
        with (
            patch("agentic_devtools.cli.ci.github_provider._require_default_workflow_token", return_value="token"),
            patch("agentic_devtools.cli.ci.github_provider._build_repair_comment", return_value="@copilot repair"),
            patch.object(
                provider,
                "get_pr_metadata",
                return_value=SimpleNamespace(base_branch="main", head_branch="repair"),
            ),
            patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=retryable) as post_task,
            patch.object(provider, "_post_repair_comment") as fallback,
            pytest.raises(ProviderRateLimitError) as exc_info,
        ):
            provider.dispatch_repair(42, "head", "review", [], [])

        assert exc_info.value.retry_after_seconds == 15
        assert exc_info.value.reset_timestamp == 1234
        assert exc_info.value.remaining == 0
        assert exc_info.value.provider == "github"
        assert exc_info.value.credential_identity == "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"
        assert exc_info.value.source == "retry-after"
        post_task.assert_called_once()
        fallback.assert_not_called()

    def test_comment_only_quota_rejection_retries_with_metadata(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("AGDT_USE_AGENT_TASKS_API", raising=False)
        monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "token")
        provider = GitHubActionsProvider(repo="owner/repo")
        quota_error = RetryableError(
            "GitHub API rate limited (HTTP 429)",
            retry_after=19,
            reset_timestamp=2345,
            remaining=0,
            provider="github",
            credential_identity="DEFAULT_CLASSIC_REPO_WORKFLOW_PAT",
            source="retry-after",
            is_rate_limit=True,
        )
        errors = [quota_error] * 6

        with (
            patch("agentic_devtools.cli.ci.retry.time.sleep"),
            patch("agentic_devtools.cli.ci.github_provider._require_default_workflow_token", return_value="token"),
            patch("agentic_devtools.cli.ci.github_provider._build_repair_comment", return_value="@copilot repair"),
            patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=errors) as post_comment,
            pytest.raises(RepairDispatchNotAttemptedError) as rejected_error,
        ):
            provider.dispatch_repair(42, "head", "review", [], [])

        rate_limit = rejected_error.value.__cause__
        assert isinstance(rate_limit, ProviderRateLimitError)
        assert rate_limit.retry_after_seconds == 19
        assert rate_limit.reset_timestamp == 2345
        assert rate_limit.remaining == 0
        assert rate_limit.credential_identity == "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"
        assert post_comment.call_count == 6

    def test_ambiguous_comment_post_is_not_retried(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("AGDT_USE_AGENT_TASKS_API", raising=False)
        monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "token")
        provider = GitHubActionsProvider(repo="owner/repo")
        ambiguous_error = RetryableError("GitHub API server error (HTTP 503)", is_rate_limit=False)

        with (
            patch("agentic_devtools.cli.ci.retry.time.sleep"),
            patch("agentic_devtools.cli.ci.github_provider._require_default_workflow_token", return_value="token"),
            patch("agentic_devtools.cli.ci.github_provider._build_repair_comment", return_value="@copilot repair"),
            patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=ambiguous_error) as post_comment,
            pytest.raises(RetryableError) as exc_info,
        ):
            provider.dispatch_repair(42, "head", "review", [], [])

        assert exc_info.value is ambiguous_error
        assert post_comment.call_count == 1

    def test_non_rate_limited_agent_task_post_remains_uncertain_without_fallback(self, monkeypatch) -> None:
        monkeypatch.setenv("AGDT_USE_AGENT_TASKS_API", "true")
        provider = GitHubActionsProvider(repo="owner/repo")
        retryable = RetryableError("GitHub API server error (HTTP 503)", is_rate_limit=False)
        with (
            patch("agentic_devtools.cli.ci.github_provider._require_default_workflow_token", return_value="token"),
            patch("agentic_devtools.cli.ci.github_provider._build_repair_comment", return_value="@copilot repair"),
            patch.object(
                provider,
                "get_pr_metadata",
                return_value=SimpleNamespace(base_branch="main", head_branch="repair"),
            ),
            patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=retryable) as post_task,
            patch.object(provider, "_post_repair_comment") as fallback,
            pytest.raises(RetryableError) as exc_info,
        ):
            provider.dispatch_repair(42, "head", "review", [], [])

        assert exc_info.value is retryable
        post_task.assert_called_once()
        fallback.assert_not_called()

    def test_missing_dispatch_token_is_a_definitive_pre_creation_failure(self, monkeypatch) -> None:
        monkeypatch.delenv("AGDT_USE_AGENT_TASKS_API", raising=False)
        provider = GitHubActionsProvider(repo="owner/repo")
        with (
            patch(
                "agentic_devtools.cli.ci.github_provider._require_default_workflow_token",
                side_effect=RuntimeError("token missing"),
            ),
            pytest.raises(RepairDispatchNotAttemptedError) as error,
        ):
            provider.dispatch_repair(42, "head", "review", [], [])

        assert isinstance(error.value.__cause__, RuntimeError)

    @pytest.mark.parametrize("response", ["{}", "[]", '{"id": 0}'])
    def test_repair_comment_requires_a_confirmed_creation_receipt(self, response, monkeypatch):
        monkeypatch.delenv("AGDT_USE_AGENT_TASKS_API", raising=False)
        provider = GitHubActionsProvider(repo="owner/repo")
        with (
            patch("agentic_devtools.cli.ci.github_provider._require_default_workflow_token", return_value="token"),
            patch("agentic_devtools.cli.ci.github_provider._build_repair_comment", return_value="@copilot repair"),
            patch.object(provider, "_post_repair_comment", return_value=response),
            pytest.raises(RuntimeError, match="confirmed comment receipt"),
        ):
            provider.dispatch_repair(42, "head", "review", [], [])

    @pytest.mark.parametrize("failure", ["summary", "malformed", "preflight", "preflight_rate_limit"])
    def test_repair_creation_boundary_never_replaces_an_uncertain_or_created_task(self, failure, monkeypatch):
        monkeypatch.setenv("AGDT_USE_AGENT_TASKS_API", "true")
        provider = GitHubActionsProvider(repo="owner/repo")
        metadata = SimpleNamespace(base_branch="main", head_branch="repair")
        metadata_error = (
            ProviderRateLimitError(provider="github")
            if failure == "preflight_rate_limit"
            else RuntimeError("metadata unavailable")
        )
        with (
            patch("agentic_devtools.cli.ci.github_provider._require_default_workflow_token", return_value="token"),
            patch("agentic_devtools.cli.ci.github_provider._build_repair_comment", return_value="@copilot repair"),
            patch.object(
                provider,
                "get_pr_metadata",
                side_effect=metadata_error if failure.startswith("preflight") else None,
                return_value=metadata,
            ),
            patch(
                "agentic_devtools.cli.ci.github_provider._gh_api",
                return_value=json.dumps({} if failure == "malformed" else {"id": 55, "html_url": "task-url"}),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.summary._find_active_summary_comment",
                side_effect=RuntimeError("optional summary write failed"),
            ),
            patch.object(provider, "_post_repair_comment", return_value='{"id": 77}') as fallback,
        ):
            if failure in {"malformed", "preflight_rate_limit"}:
                with pytest.raises((RuntimeError, ProviderRateLimitError)) as error:
                    provider.dispatch_repair(42, "head", "review", [], [], review_id=10)
                if failure == "preflight_rate_limit":
                    assert isinstance(error.value, RepairDispatchNotAttemptedError)
                    assert isinstance(error.value.__cause__, ProviderRateLimitError)
                fallback.assert_not_called()
            else:
                receipt = provider.dispatch_repair(42, "head", "review", [], [], review_id=10)
                if failure == "summary":
                    assert receipt == "task:owner/repo:55"
                    fallback.assert_not_called()
                else:
                    assert receipt == 77
                    assert "<!-- repair-dispatch:work:head:10:" in fallback.call_args.kwargs["body"]

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_list_pr_commits_includes_parents_and_paginates(self, mock_api):
        commits = [{"sha": "P"}, {"sha": "R", "parents": [{"sha": "P"}]}]
        mock_api.return_value = json.dumps(commits)
        assert GitHubActionsProvider(repo="owner/repo").list_pr_commits(1) == commits
        mock_api.assert_called_once_with("/repos/owner/repo/pulls/1/commits", paginate=True)

    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_list_pr_commits_propagates_exhausted_rate_limit(self, mock_api, mock_sleep):
        mock_api.side_effect = RetryableError("rate limited", is_rate_limit=True)
        with pytest.raises(ProviderRateLimitError):
            GitHubActionsProvider(repo="owner/repo").list_pr_commits(1)
        assert mock_api.call_count == 6

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
    def test_get_trusted_loop_comment_logins_caches_local_fallback(
        self,
        mock_gh_api,
        monkeypatch,
    ) -> None:
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        mock_gh_api.return_value = json.dumps({"login": "local-user"})
        provider = GitHubActionsProvider(repo="owner/repo")

        with patch.object(provider, "get_pr_token_login", return_value=""):
            trusted = {"local-user", "github-actions[bot]"}
            assert provider.get_trusted_loop_comment_logins() == trusted
            assert provider.get_trusted_loop_comment_logins() == trusted

        mock_gh_api.assert_called_once_with("/user")

    def test_get_trusted_loop_comment_logins_rejects_missing_actions_identity(self, monkeypatch) -> None:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        provider = GitHubActionsProvider(repo="owner/repo")
        with (
            patch.object(provider, "get_pr_token_login", return_value="pat-owner"),
            patch.object(provider, "get_bookkeeping_token_login", return_value=""),
            pytest.raises(RuntimeError, match="could not both be verified"),
        ):
            provider.get_trusted_loop_comment_logins()

    def test_get_trusted_loop_comment_logins_rejects_ambiguous_actions_identity(self, monkeypatch) -> None:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        provider = GitHubActionsProvider(repo="owner/repo")
        with (
            patch.object(provider, "get_pr_token_login", return_value="same-login"),
            patch.object(provider, "get_bookkeeping_token_login", return_value="SAME-LOGIN"),
            pytest.raises(RuntimeError, match="identities are ambiguous"),
        ):
            provider.get_trusted_loop_comment_logins()

    def test_get_trusted_loop_comment_logins_rejects_non_bot_actions_identity(self, monkeypatch) -> None:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        provider = GitHubActionsProvider(repo="owner/repo")
        with (
            patch.object(provider, "get_pr_token_login", return_value="pat-owner"),
            patch.object(provider, "get_bookkeeping_token_login", return_value="other-bot"),
            pytest.raises(RuntimeError, match="must be github-actions\\[bot\\]"),
        ):
            provider.get_trusted_loop_comment_logins()

    @patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=RuntimeError("API unavailable"))
    def test_get_trusted_loop_comment_logins_wraps_local_identity_lookup_errors(self, mock_gh_api, monkeypatch) -> None:
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        provider = GitHubActionsProvider(repo="owner/repo")

        with (
            patch.object(provider, "get_pr_token_login", return_value=""),
            pytest.raises(RuntimeError, match="Could not verify the local GitHub comment identity"),
        ):
            provider.get_trusted_loop_comment_logins()

        mock_gh_api.assert_called_once_with("/user")

    @patch(
        "agentic_devtools.cli.ci.github_provider._gh_api",
        side_effect=ProviderRateLimitError(provider="github", credential_identity="GH_TOKEN"),
    )
    def test_get_trusted_loop_comment_logins_reraises_local_rate_limit(self, _mock_gh_api, monkeypatch) -> None:
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        provider = GitHubActionsProvider(repo="owner/repo")

        with (
            patch.object(provider, "get_pr_token_login", return_value=""),
            pytest.raises(ProviderRateLimitError),
        ):
            provider.get_trusted_loop_comment_logins()

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_get_trusted_loop_comment_logins_includes_pat_and_ambient_logins(self, mock_gh_api, monkeypatch) -> None:
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        mock_gh_api.return_value = json.dumps({"login": "ambient-user"})
        provider = GitHubActionsProvider(repo="owner/repo")

        with patch.object(provider, "get_pr_token_login", return_value="local-pat-user"):
            assert provider.get_trusted_loop_comment_logins() == {
                "local-pat-user",
                "ambient-user",
                "github-actions[bot]",
            }

        mock_gh_api.assert_called_once_with("/user")

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_get_local_comment_login_resolves_and_caches_ambient_identity(self, mock_gh_api) -> None:
        mock_gh_api.return_value = json.dumps({"login": "ambient-user"})
        provider = GitHubActionsProvider(repo="owner/repo")

        assert provider.get_local_comment_login() == "ambient-user"
        assert provider.get_local_comment_login() == "ambient-user"

        mock_gh_api.assert_called_once_with("/user")

    @pytest.mark.parametrize("response", ["[]", json.dumps({"login": None})])
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_get_local_comment_login_returns_empty_for_invalid_identity(self, mock_gh_api, response) -> None:
        mock_gh_api.return_value = response
        provider = GitHubActionsProvider(repo="owner/repo")

        assert provider.get_local_comment_login() == ""

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_create_review_thread_rejects_unverified_bookkeeping_identity(self, mock_gh_api, monkeypatch) -> None:
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")
        provider = GitHubActionsProvider(repo="owner/repo")

        with (
            patch.object(provider, "get_pr_metadata", return_value=SimpleNamespace(head_sha="head-sha")),
            patch.object(provider, "get_bookkeeping_token_login", return_value=""),
            pytest.raises(RuntimeError, match="identity could not be verified"),
        ):
            provider.create_review_thread(
                pr_number=4,
                commit_sha="head-sha",
                path="src/app.py",
                line=9,
                side="RIGHT",
                body="Finding",
            )

        mock_gh_api.assert_not_called()

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_create_review_thread_allows_verified_local_bookkeeping_identity(self, mock_gh_api, monkeypatch) -> None:
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "local-token")
        mock_gh_api.return_value = json.dumps({"id": 123, "user": {"login": "local-user"}})
        provider = GitHubActionsProvider(repo="owner/repo")

        with (
            patch.object(provider, "get_pr_metadata", return_value=SimpleNamespace(head_sha="head-sha")),
            patch.object(provider, "get_bookkeeping_token_login", return_value="local-user"),
        ):
            result = provider.create_review_thread(
                pr_number=4,
                commit_sha="head-sha",
                path="src/app.py",
                line=9,
                side="RIGHT",
                body="Finding",
            )

        assert result.id == 123
        assert mock_gh_api.call_args.kwargs["token"] == "local-token"
        assert mock_gh_api.call_args.kwargs["credential_identity"] == "AI_PR_LOOP_BOOKKEEPING_TOKEN"

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_create_review_thread_requires_actions_bot_identity_in_actions(self, mock_gh_api, monkeypatch) -> None:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")
        provider = GitHubActionsProvider(repo="owner/repo")

        with (
            patch.object(provider, "get_pr_metadata", return_value=SimpleNamespace(head_sha="head-sha")),
            patch.object(provider, "get_bookkeeping_token_login", return_value="local-user"),
            pytest.raises(RuntimeError, match="could not be verified as github-actions\\[bot\\]"),
        ):
            provider.create_review_thread(
                pr_number=4,
                commit_sha="head-sha",
                path="src/app.py",
                line=9,
                side="RIGHT",
                body="Finding",
            )

        mock_gh_api.assert_not_called()

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_get_trusted_loop_comment_logins_caches_unavailable_local_fallback(
        self,
        mock_gh_api,
        monkeypatch,
    ) -> None:
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        mock_gh_api.return_value = json.dumps({})
        provider = GitHubActionsProvider(repo="owner/repo")

        with patch.object(provider, "get_pr_token_login", return_value=""):
            for _ in range(2):
                with pytest.raises(RuntimeError, match="Could not verify the local GitHub comment identity"):
                    provider.get_trusted_loop_comment_logins()

        mock_gh_api.assert_called_once_with("/user")

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


class TestGitHubActionsProviderListAgentTasks:
    """Tests for the shared Agent Tasks inventory operation."""

    @patch.object(GitHubActionsProvider, "_fetch_agent_tasks", return_value='{"tasks":[{"id":"task-1"}]}')
    def test_uses_copilot_token_and_returns_inventory(self, mock_fetch, monkeypatch) -> None:
        monkeypatch.setenv("COPILOT_GITHUB_TOKEN", "task-token")
        provider = GitHubActionsProvider(repo="owner/repo")

        inventory = provider.list_agent_tasks("owner/repo")

        assert isinstance(inventory, AgentTaskInventoryLoadResult)
        assert inventory.tasks == ({"id": "task-1"},)
        assert inventory.complete
        mock_fetch.assert_called_once_with("owner/repo", "task-token")

    @patch("agentic_devtools.cli.ci.github_provider.require_default_repo_workflow_token", return_value="workflow-token")
    @patch.object(GitHubActionsProvider, "_fetch_agent_tasks", return_value='{"tasks":[]}')
    def test_uses_default_workflow_token_when_copilot_token_is_unset(
        self,
        mock_fetch,
        mock_token,
        monkeypatch,
    ) -> None:
        monkeypatch.delenv("COPILOT_GITHUB_TOKEN", raising=False)
        provider = GitHubActionsProvider(repo="owner/repo")

        inventory = provider.list_agent_tasks("owner/repo")
        assert isinstance(inventory, AgentTaskInventoryLoadResult)
        assert inventory.tasks == ()
        assert inventory.complete

        mock_token.assert_called_once_with("list Copilot Agent Tasks")
        mock_fetch.assert_called_once_with("owner/repo", "workflow-token")

    @patch.object(GitHubActionsProvider, "_fetch_agent_tasks", return_value='[{"id":"task-1"}]')
    def test_rejects_non_dict_inventory_page(self, _mock_fetch, monkeypatch) -> None:
        monkeypatch.setenv("COPILOT_GITHUB_TOKEN", "task-token")

        inventory = GitHubActionsProvider(repo="owner/repo").list_agent_tasks("owner/repo")
        assert isinstance(inventory, AgentTaskInventoryLoadResult)
        assert not inventory.complete
        assert inventory.failure_category == "malformed_response"

    @pytest.mark.parametrize("repo", ["", "repo-without-owner"])
    def test_rejects_invalid_repository(self, repo: str) -> None:
        with pytest.raises(ValueError, match="owner/repo"):
            GitHubActionsProvider(repo="owner/repo").list_agent_tasks(repo)

    def test_rejects_non_string_repository(self) -> None:
        with pytest.raises(ValueError, match="owner/repo"):
            GitHubActionsProvider(repo="owner/repo").list_agent_tasks(None)  # type: ignore[arg-type]

    @pytest.mark.parametrize("response", ['{"tasks":"invalid"}', "", " \r\n\t"])
    @patch.object(GitHubActionsProvider, "_fetch_agent_tasks")
    def test_rejects_malformed_inventory_payload(self, mock_fetch, response, monkeypatch) -> None:
        monkeypatch.setenv("COPILOT_GITHUB_TOKEN", "task-token")
        mock_fetch.return_value = response
        inventory = GitHubActionsProvider(repo="owner/repo").list_agent_tasks("owner/repo")
        assert isinstance(inventory, AgentTaskInventoryLoadResult)
        assert not inventory.complete
        assert inventory.failure_category == "malformed_response"


class TestGitHubActionsProviderGetPrTokenLogin:
    """Tests for GitHubActionsProvider.get_pr_token_login()."""

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_returns_login_from_default_workflow_token(self, mock_gh_api, monkeypatch) -> None:
        """Returns the login resolved from DEFAULT_CLASSIC_REPO_WORKFLOW_PAT via GET /user."""
        monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "tok_abc123")
        mock_gh_api.return_value = json.dumps({"login": "dispatch-bot"})

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.get_pr_token_login()

        assert result == "dispatch-bot"
        mock_gh_api.assert_called_once_with("/user", token="tok_abc123", read_pool=False)

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_returns_empty_string_when_token_absent(self, mock_gh_api, monkeypatch) -> None:
        """Returns empty string when DEFAULT_CLASSIC_REPO_WORKFLOW_PAT is not set."""
        monkeypatch.delenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", raising=False)

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.get_pr_token_login()

        assert result == ""
        mock_gh_api.assert_not_called()

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_returns_empty_string_when_token_whitespace_only(self, mock_gh_api, monkeypatch) -> None:
        """Returns empty string when DEFAULT_CLASSIC_REPO_WORKFLOW_PAT is whitespace-only."""
        monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "   ")

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.get_pr_token_login()

        assert result == ""
        mock_gh_api.assert_not_called()

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_returns_empty_string_when_api_call_fails(self, mock_gh_api, monkeypatch) -> None:
        """Returns empty string when the GET /user call raises an exception."""
        monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "tok_expired")
        mock_gh_api.side_effect = RuntimeError("401 Unauthorized")

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.get_pr_token_login()

        assert result == ""

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_reraises_provider_rate_limit_error(self, mock_gh_api, monkeypatch) -> None:
        """Provider rate limits must propagate so callers can pause instead of failing soft."""
        monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "tok_abc123")
        mock_gh_api.side_effect = ProviderRateLimitError(
            provider="github",
            credential_identity="DEFAULT_CLASSIC_REPO_WORKFLOW_PAT",
        )

        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(ProviderRateLimitError):
            provider.get_pr_token_login()

    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_retries_pr_token_login_rate_limit_and_preserves_cooldown_metadata(
        self, mock_gh_api, _mock_sleep, monkeypatch
    ) -> None:
        monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "tok_abc123")
        retryable = RetryableError(
            "GitHub API rate limited (HTTP 429)",
            retry_after=23,
            reset_timestamp=1234,
            remaining=0,
            provider="github",
            credential_identity="DEFAULT_CLASSIC_REPO_WORKFLOW_PAT",
            source="retry-after",
            is_rate_limit=True,
        )
        mock_gh_api.side_effect = [retryable] * 6 + [json.dumps({"login": "dispatch-bot"})]
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(ProviderRateLimitError) as exc_info:
            provider.get_pr_token_login()

        assert exc_info.value.retry_after_seconds == 23
        assert exc_info.value.reset_timestamp == 1234
        assert exc_info.value.remaining == 0
        assert exc_info.value.provider == "github"
        assert exc_info.value.credential_identity == "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"
        assert exc_info.value.source == "retry-after"
        assert provider._pr_token_login_cache is None
        assert provider.get_pr_token_login() == "dispatch-bot"
        assert mock_gh_api.call_count == 7

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_returns_empty_string_when_login_missing_from_response(self, mock_gh_api, monkeypatch) -> None:
        """Returns empty string when the API response lacks a 'login' key."""
        monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "tok_abc123")
        mock_gh_api.return_value = json.dumps({"id": 1, "name": "Bot"})

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.get_pr_token_login()

        assert result == ""

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_returns_empty_string_when_login_is_non_string(self, mock_gh_api, monkeypatch) -> None:
        """Returns empty string when 'login' is not a string (e.g., None or int)."""
        monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "tok_abc123")
        mock_gh_api.return_value = json.dumps({"login": None})

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.get_pr_token_login()

        assert result == ""

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_caches_result_on_second_call(self, mock_gh_api, monkeypatch) -> None:
        """The resolved login is cached so GET /user is called at most once per instance."""
        monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "tok_abc123")
        mock_gh_api.return_value = json.dumps({"login": "dispatch-bot"})

        provider = GitHubActionsProvider(repo="owner/repo")
        first = provider.get_pr_token_login()
        second = provider.get_pr_token_login()

        assert first == second == "dispatch-bot"
        assert mock_gh_api.call_count == 1

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_caches_empty_string_result(self, mock_gh_api, monkeypatch) -> None:
        """The empty-string result (failure) is also cached to avoid repeated API calls."""
        monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "tok_bad")
        mock_gh_api.side_effect = RuntimeError("Unauthorized")

        provider = GitHubActionsProvider(repo="owner/repo")
        first = provider.get_pr_token_login()
        second = provider.get_pr_token_login()

        assert first == second == ""
        assert mock_gh_api.call_count == 1

    @patch("agentic_devtools.cli.ci.pipeline.summary._find_active_summary_comment", return_value=None)
    @patch("agentic_devtools.cli.ci.github_provider._build_repair_comment", return_value="@copilot repair")
    @patch("agentic_devtools.cli.ci.github_provider._require_default_workflow_token", return_value="token")
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_agent_task_dispatch_survives_rate_limited_identity_lookup(
        self,
        mock_gh_api,
        _mock_require_token,
        _mock_build_comment,
        _mock_find_summary,
        monkeypatch,
    ) -> None:
        """A bookkeeping identity rate limit does not trigger fallback dispatch."""
        monkeypatch.setenv("AGDT_USE_AGENT_TASKS_API", "true")
        provider = GitHubActionsProvider(repo="owner/repo")
        with (
            patch.object(
                provider,
                "get_pr_metadata",
                return_value=SimpleNamespace(base_branch="main", head_branch="repair-branch"),
            ),
            patch.object(
                provider,
                "get_pr_token_login",
                side_effect=ProviderRateLimitError(
                    provider="github", credential_identity="DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"
                ),
            ),
            patch.object(provider, "_post_repair_comment") as mock_post_repair_comment,
            patch.object(provider, "_reply_to_review_comment") as mock_reply_to_review_comment,
        ):
            mock_gh_api.return_value = json.dumps(
                {"html_url": "https://github.com/swai-factory/agentic-devtools/tasks/1"}
            )
            result = provider.dispatch_repair(
                pr_number=4223,
                head_sha="head-sha",
                repair_type="review",
                failed_checks=[],
                review_comments=[ReviewCommentInfo(id=17, path="file.py", body="review", html_url="")],
            )

        assert result == "task:https://github.com/swai-factory/agentic-devtools/tasks/1"
        mock_post_repair_comment.assert_not_called()
        mock_reply_to_review_comment.assert_not_called()
        assert mock_gh_api.call_count == 1

    @patch("agentic_devtools.cli.ci.pipeline.summary._find_active_summary_comment")
    @patch("agentic_devtools.cli.ci.github_provider._build_repair_comment", return_value="@copilot repair")
    @patch("agentic_devtools.cli.ci.github_provider._require_default_workflow_token", return_value="token")
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_agent_task_dispatch_survives_summary_update_failure(
        self,
        mock_gh_api,
        _mock_require_token,
        _mock_build_comment,
        mock_find_summary,
        monkeypatch,
    ) -> None:
        """A failure updating the summary comment does not trigger a duplicate fallback dispatch."""
        monkeypatch.setenv("AGDT_USE_AGENT_TASKS_API", "true")
        mock_find_summary.return_value = (99, "summary body")
        provider = GitHubActionsProvider(repo="owner/repo")
        with (
            patch.object(
                provider,
                "get_pr_metadata",
                return_value=SimpleNamespace(base_branch="main", head_branch="repair-branch"),
            ),
            patch.object(provider, "get_pr_token_login", return_value=""),
            patch.object(provider, "update_comment", side_effect=RuntimeError("summary update failed")),
            patch.object(provider, "_post_repair_comment") as mock_post_repair_comment,
        ):
            mock_gh_api.return_value = json.dumps(
                {"html_url": "https://github.com/swai-factory/agentic-devtools/tasks/1"}
            )
            result = provider.dispatch_repair(
                pr_number=4223,
                head_sha="head-sha",
                repair_type="review",
                failed_checks=[],
                review_comments=[],
            )

        assert result == "task:https://github.com/swai-factory/agentic-devtools/tasks/1"
        mock_post_repair_comment.assert_not_called()
        assert mock_gh_api.call_count == 1

    @patch("agentic_devtools.cli.ci.pipeline.summary._find_active_summary_comment", return_value=None)
    @patch("agentic_devtools.cli.ci.github_provider._build_repair_comment", return_value="@copilot repair")
    @patch("agentic_devtools.cli.ci.github_provider._require_default_workflow_token", return_value="token")
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_agent_task_dispatch_survives_malformed_response_body(
        self,
        mock_gh_api,
        _mock_require_token,
        _mock_build_comment,
        _mock_find_summary,
        monkeypatch,
    ) -> None:
        """A malformed Agent Tasks API response does not trigger a duplicate fallback dispatch."""
        monkeypatch.setenv("AGDT_USE_AGENT_TASKS_API", "true")
        provider = GitHubActionsProvider(repo="owner/repo")
        with (
            patch.object(
                provider,
                "get_pr_metadata",
                return_value=SimpleNamespace(base_branch="main", head_branch="repair-branch"),
            ),
            patch.object(provider, "get_pr_token_login", return_value=""),
            patch.object(provider, "_post_repair_comment") as mock_post_repair_comment,
        ):
            # The POST succeeds, but the response body is not valid JSON.
            mock_gh_api.return_value = "not-json"
            with pytest.raises(json.JSONDecodeError):
                provider.dispatch_repair(
                    pr_number=4223,
                    head_sha="head-sha",
                    repair_type="review",
                    failed_checks=[],
                    review_comments=[],
                )

        mock_post_repair_comment.assert_not_called()
        assert mock_gh_api.call_count == 1


class TestGitHubActionsProviderBookkeepingTokenLogin:
    """Tests for bookkeeping-token identity resolution."""

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_resolves_and_caches_login_using_only_bookkeeping_token(self, mock_gh_api, monkeypatch) -> None:
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")
        monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "human-token")
        mock_gh_api.return_value = json.dumps({"data": {"viewer": {"login": "github-actions[bot]"}}})
        provider = GitHubActionsProvider(repo="owner/repo")

        assert provider.get_bookkeeping_token_login() == "github-actions[bot]"
        assert provider.get_bookkeeping_token_login() == "github-actions[bot]"
        mock_gh_api.assert_called_once_with(
            "graphql",
            method="POST",
            body={"query": "query { viewer { login } }"},
            token="bot-token",
            credential_identity="AI_PR_LOOP_BOOKKEEPING_TOKEN",
            response_metadata={},
        )

    @patch("agentic_devtools.cli.ci.github_provider._raise_for_graphql_errors", wraps=_raise_for_graphql_errors)
    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_retries_graphql_rate_limit_response_for_bookkeeping_identity(
        self, mock_gh_api, _mock_sleep, mock_raise_for_graphql_errors, monkeypatch
    ) -> None:
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")
        metadata_by_call = []

        def _graphql_response(*_args, **kwargs):
            metadata = kwargs.get("response_metadata")
            if isinstance(metadata, dict):
                metadata_by_call.append(metadata)
                if len(metadata_by_call) == 1:
                    metadata.update(retry_after=1.0, reset_timestamp=123.0, remaining=0)
            if mock_gh_api.call_count == 1:
                return json.dumps(
                    {
                        "data": None,
                        "errors": [{"type": "RATE_LIMITED", "message": "API rate limit exceeded"}],
                    }
                )
            return json.dumps({"data": {"viewer": {"login": "github-actions[bot]"}}})

        mock_gh_api.side_effect = _graphql_response

        provider = GitHubActionsProvider(repo="owner/repo")

        assert provider.get_bookkeeping_token_login() == "github-actions[bot]"
        assert mock_gh_api.call_count == 2
        assert len(metadata_by_call) == 2
        assert metadata_by_call[0] == {"retry_after": 1.0, "reset_timestamp": 123.0, "remaining": 0}
        assert mock_raise_for_graphql_errors.call_args_list[0].kwargs == {
            "context": "Bookkeeping token identity GraphQL error",
            "provider": "github",
            "credential_identity": "AI_PR_LOOP_BOOKKEEPING_TOKEN",
            "retry_after": 1.0,
            "reset_timestamp": 123.0,
            "remaining": 0,
        }

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_returns_empty_and_caches_when_bookkeeping_token_is_missing(self, mock_gh_api, monkeypatch) -> None:
        monkeypatch.delenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", raising=False)
        monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "human-token")
        provider = GitHubActionsProvider(repo="owner/repo")

        assert provider.get_bookkeeping_token_login() == ""
        assert provider.get_bookkeeping_token_login() == ""
        mock_gh_api.assert_not_called()

    @pytest.mark.parametrize(
        "response",
        [
            '{"login":"github-actions[bot]"}',
            '{"data":{"viewer":{"login":null}}}',
            '{"data":null}',
            "[]",
        ],
    )
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_returns_empty_when_bookkeeping_identity_response_is_invalid(
        self, mock_gh_api, response, monkeypatch
    ) -> None:
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")
        mock_gh_api.return_value = response

        assert GitHubActionsProvider(repo="owner/repo").get_bookkeeping_token_login() == ""

    @patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=RuntimeError("API unavailable"))
    def test_returns_empty_when_bookkeeping_identity_lookup_fails(self, mock_gh_api, monkeypatch) -> None:
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")

        assert GitHubActionsProvider(repo="owner/repo").get_bookkeeping_token_login() == ""
        mock_gh_api.assert_called_once()

    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_reraises_rate_limit_for_bookkeeping_identity(self, mock_gh_api, _mock_sleep, monkeypatch) -> None:
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")
        mock_gh_api.side_effect = RetryableError(
            "GitHub API rate limited (HTTP 429)",
            retry_after=1,
            provider="github",
            credential_identity="AI_PR_LOOP_BOOKKEEPING_TOKEN",
            is_rate_limit=True,
        )

        with pytest.raises(ProviderRateLimitError) as exc_info:
            GitHubActionsProvider(repo="owner/repo").get_bookkeeping_token_login()

        assert exc_info.value.credential_identity == "AI_PR_LOOP_BOOKKEEPING_TOKEN"
        assert mock_gh_api.call_count == 6


class TestGitHubActionsProviderTrustedReviewBookkeepingLogins:
    """Tests for authenticated bookkeeping identities."""

    def test_returns_casefolded_bot_and_legacy_workflow_identities(self, monkeypatch) -> None:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")
        provider = GitHubActionsProvider(repo="owner/repo")
        with (
            patch.object(provider, "get_bookkeeping_token_login", return_value="GitHub-Actions[Bot]"),
            patch.object(provider, "get_pr_token_login", return_value="Legacy-Workflow"),
        ):
            assert provider._trusted_review_bookkeeping_logins() == {
                "github-actions[bot]",
                "legacy-workflow",
            }

    def test_returns_empty_when_neither_credential_identity_is_verified(self, monkeypatch) -> None:
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        provider = GitHubActionsProvider(repo="owner/repo")
        with (
            patch.object(provider, "get_bookkeeping_token_login", return_value=""),
            patch.object(provider, "get_pr_token_login", return_value=""),
        ):
            assert provider._trusted_review_bookkeeping_logins() == set()

    def test_requires_bookkeeping_identity_in_actions_when_token_is_missing(self, monkeypatch) -> None:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        monkeypatch.delenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", raising=False)
        provider = GitHubActionsProvider(repo="owner/repo")
        with (
            patch.object(provider, "get_pr_token_login", return_value="legacy-workflow"),
            pytest.raises(RuntimeError, match="AI_PR_LOOP_BOOKKEEPING_TOKEN"),
        ):
            provider._trusted_review_bookkeeping_logins()

    def test_requires_verified_bookkeeping_identity_in_actions(self, monkeypatch) -> None:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bookkeeping-token")
        provider = GitHubActionsProvider(repo="owner/repo")
        with (
            patch.object(provider, "get_bookkeeping_token_login", return_value=""),
            patch.object(provider, "get_pr_token_login", return_value="legacy-workflow"),
            pytest.raises(RuntimeError, match="AI_PR_LOOP_BOOKKEEPING_TOKEN"),
        ):
            provider._trusted_review_bookkeeping_logins()

    def test_rejects_non_bot_bookkeeping_identity_in_actions(self, monkeypatch) -> None:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bookkeeping-token")
        provider = GitHubActionsProvider(repo="owner/repo")
        with (
            patch.object(provider, "get_bookkeeping_token_login", return_value="other-bot"),
            patch.object(provider, "get_pr_token_login", return_value="legacy-workflow"),
            pytest.raises(RuntimeError, match="must be github-actions\\[bot\\]"),
        ):
            provider._trusted_review_bookkeeping_logins()


class TestGitHubActionsProviderReplyToReviewComment:
    """Tests for GitHubActionsProvider._reply_to_review_comment()."""

    @pytest.fixture(autouse=True)
    def _verified_bookkeeping_identity(self, monkeypatch):
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        with patch.object(
            GitHubActionsProvider,
            "get_bookkeeping_token_login",
            return_value="github-actions[bot]",
        ):
            yield

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_uses_only_the_bookkeeping_credential(self, mock_gh_api, monkeypatch) -> None:
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")
        monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "human-token")
        monkeypatch.setenv("GH_TOKEN", "human-token")

        GitHubActionsProvider(repo="owner/repo")._reply_to_review_comment(42, 99, body="Thread resolved")

        assert mock_gh_api.call_args.kwargs["token"] == "bot-token"
        assert mock_gh_api.call_args.kwargs["credential_identity"] == "AI_PR_LOOP_BOOKKEEPING_TOKEN"

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_allows_verified_local_bookkeeping_identity(self, mock_gh_api, monkeypatch) -> None:
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "local-token")

        with patch.object(GitHubActionsProvider, "get_bookkeeping_token_login", return_value="local-user"):
            GitHubActionsProvider(repo="owner/repo")._reply_to_review_comment(42, 99, body="Thread resolved")

        assert mock_gh_api.call_args.kwargs["token"] == "local-token"
        assert mock_gh_api.call_args.kwargs["credential_identity"] == "AI_PR_LOOP_BOOKKEEPING_TOKEN"

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_rejects_unverified_bookkeeping_identity(self, mock_gh_api, monkeypatch) -> None:
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")
        provider = GitHubActionsProvider(repo="owner/repo")

        with (
            patch.object(provider, "get_bookkeeping_token_login", return_value=""),
            pytest.raises(RuntimeError, match="identity could not be verified"),
        ):
            provider._reply_to_review_comment(42, 99, body="Thread resolved")

        mock_gh_api.assert_not_called()

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_neutralizes_copilot_mentions(self, mock_gh_api, monkeypatch) -> None:
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")

        GitHubActionsProvider(repo="owner/repo")._reply_to_review_comment(42, 99, body="Rationale: @Copilot review")

        assert mock_gh_api.call_args.kwargs["body"]["body"] == "Rationale: @\u200bcopilot review\n\n🤖 AI PR Loop ·"

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_rejects_missing_local_bookkeeping_identity(self, mock_gh_api, monkeypatch) -> None:
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "local-token")

        with (
            patch.object(GitHubActionsProvider, "get_bookkeeping_token_login", return_value=""),
            pytest.raises(RuntimeError, match="identity could not be verified"),
        ):
            GitHubActionsProvider(repo="owner/repo")._reply_to_review_comment(42, 99)

        mock_gh_api.assert_not_called()

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_rejects_non_bot_actions_bookkeeping_identity(self, mock_gh_api, monkeypatch) -> None:
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")

        with (
            patch.object(GitHubActionsProvider, "get_bookkeeping_token_login", return_value="local-user"),
            pytest.raises(RuntimeError, match="could not be verified as github-actions\\[bot\\]"),
        ):
            GitHubActionsProvider(repo="owner/repo")._reply_to_review_comment(42, 99)

        mock_gh_api.assert_not_called()

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_does_not_fall_back_when_bookkeeping_credential_is_missing(self, mock_gh_api, monkeypatch) -> None:
        monkeypatch.delenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", raising=False)
        monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "human-token")
        monkeypatch.setenv("GH_TOKEN", "human-token")

        with pytest.raises(RuntimeError, match="AI_PR_LOOP_BOOKKEEPING_TOKEN"):
            GitHubActionsProvider(repo="owner/repo")._reply_to_review_comment(42, 99)

        mock_gh_api.assert_not_called()


class TestGitHubActionsProviderDispatchRepair:
    """Tests for GitHubActionsProvider.dispatch_repair()."""

    @pytest.mark.parametrize(
        ("model_override", "expected_model"),
        [
            (None, "gpt-6-luna"),
            ("", "gpt-6-luna"),
            (" \t ", "gpt-6-luna"),
            ("custom-model", "custom-model"),
            ("  custom-model \t", "custom-model"),
        ],
    )
    @pytest.mark.parametrize("repair_type", ["review", "ci", "both"])
    def test_uses_configured_model_for_agent_tasks(
        self,
        model_override: str | None,
        expected_model: str,
        repair_type: str,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setenv("AGDT_USE_AGENT_TASKS_API", "1")
        monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "test-token")
        if model_override is None:
            monkeypatch.delenv("COPILOT_AGENT_MODEL", raising=False)
        else:
            monkeypatch.setenv("COPILOT_AGENT_MODEL", model_override)

        provider = GitHubActionsProvider(repo="owner/repo")
        prompt = "@copilot repair prompt"
        with (
            patch.object(
                provider, "get_pr_metadata", return_value=SimpleNamespace(base_branch="main", head_branch="feature")
            ),
            patch("agentic_devtools.cli.ci.github_provider._build_repair_comment", return_value=prompt),
            patch(
                "agentic_devtools.cli.ci.github_provider._gh_api", return_value=json.dumps({"html_url": "task-url"})
            ) as api,
            patch("agentic_devtools.cli.ci.pipeline.summary._find_active_summary_comment", return_value=None),
            patch.object(provider, "get_pr_token_login", return_value=""),
        ):
            result = provider.dispatch_repair(
                pr_number=42,
                head_sha="head-sha",
                repair_type=repair_type,
                failed_checks=[],
                review_comments=[],
            )

        assert result == "task:task-url"
        api.assert_called_once()
        (endpoint,) = api.call_args.args
        assert endpoint == "/agents/repos/owner/repo/tasks"
        assert api.call_args.kwargs["method"] == "POST"
        assert api.call_args.kwargs["token"] == "test-token"
        payload = api.call_args.kwargs["body"]
        assert payload["prompt"].startswith(f"{prompt}\n\n<!-- repair-dispatch:work:head-sha:0:")
        assert payload["prompt"].endswith(" -->")
        assert {**payload, "prompt": prompt} == {
            "prompt": prompt,
            "custom_agent": "agdt.address-copilot-review.evaluate-and-respond",
            "model": expected_model,
            "base_ref": "main",
            "head_ref": "feature",
            "create_pull_request": False,
        }

    def test_keeps_agent_tasks_opt_in(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("AGDT_USE_AGENT_TASKS_API", raising=False)
        monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "test-token")
        provider = GitHubActionsProvider(repo="owner/repo")

        with (
            patch("agentic_devtools.cli.ci.github_provider._build_repair_comment", return_value="@copilot repair"),
            patch("agentic_devtools.cli.ci.github_provider._gh_api") as api,
            patch.object(provider, "get_pr_metadata") as get_metadata,
            patch.object(provider, "_post_repair_comment", return_value=json.dumps({"id": 123})) as post_comment,
        ):
            result = provider.dispatch_repair(
                pr_number=42,
                head_sha="head-sha",
                repair_type="review",
                failed_checks=[],
                review_comments=[],
            )

        assert result == 123
        api.assert_not_called()
        get_metadata.assert_not_called()
        post_comment.assert_called_once()

    def test_does_not_fall_back_when_agent_task_creation_is_uncertain(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AGDT_USE_AGENT_TASKS_API", "1")
        monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "test-token")
        provider = GitHubActionsProvider(repo="owner/repo")

        with (
            patch.object(
                provider, "get_pr_metadata", return_value=SimpleNamespace(base_branch="main", head_branch="feature")
            ),
            patch("agentic_devtools.cli.ci.github_provider._build_repair_comment", return_value="@copilot repair"),
            patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=RuntimeError("unavailable")),
            patch("agentic_devtools.cli.ci.pipeline.summary._find_active_summary_comment") as find_summary,
            patch.object(provider, "_post_repair_comment", return_value=json.dumps({"id": 123})) as post_comment,
        ):
            with pytest.raises(RuntimeError, match="unavailable"):
                provider.dispatch_repair(
                    pr_number=42,
                    head_sha="head-sha",
                    repair_type="review",
                    failed_checks=[],
                    review_comments=[],
                )

        find_summary.assert_not_called()
        post_comment.assert_not_called()


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

    @patch.dict(os.environ, {"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "pr-token"}, clear=False)
    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_post_comment_as_pr_token_uses_pr_token(self, mock_run_safe) -> None:
        """post_comment_as_pr_token authenticates with DEFAULT_CLASSIC_REPO_WORKFLOW_PAT."""
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
        """post_comment_as_pr_token raises RuntimeError when DEFAULT_CLASSIC_REPO_WORKFLOW_PAT is not set."""
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RuntimeError, match="DEFAULT_CLASSIC_REPO_WORKFLOW_PAT is required"):
            provider.post_comment_as_pr_token(7, "token body")

    def test_rate_limit_error_propagates_without_reconciliation(self) -> None:
        """Rate-limit errors are not reconciled as ambiguous comment writes."""
        provider = GitHubActionsProvider(repo="owner/repo")
        error = RetryableError("rate limited", is_rate_limit=True)

        with (
            patch.object(provider, "_post_comment_as_pr_token_once", side_effect=error),
            patch.object(provider, "get_dispatch_login") as mock_get_login,
            pytest.raises(ProviderRateLimitError),
        ):
            provider.post_comment_as_pr_token(7, "token body")

        mock_get_login.assert_not_called()

    def test_returns_latest_matching_comment_after_ambiguous_write(self) -> None:
        """Returns the newest matching dispatch comment without resending it."""
        provider = GitHubActionsProvider(repo="owner/repo")
        error = RetryableError("request timed out")
        comments = [
            SimpleNamespace(id=10, author="other", body="token body"),
            SimpleNamespace(id=11, author="DISPATCH-BOT", body="different body"),
            SimpleNamespace(id=12, author="Dispatch-Bot", body="token body"),
            SimpleNamespace(id=13, author="dispatch-bot", body="token body"),
        ]

        with (
            patch.object(provider, "_post_comment_as_pr_token_once", side_effect=error) as mock_post,
            patch.object(provider, "get_dispatch_login", return_value="dispatch-bot"),
            patch.object(provider, "list_issue_comments", return_value=comments),
        ):
            assert provider.post_comment_as_pr_token(7, "token body") == 13

        mock_post.assert_called_once_with(7, "token body")

    def test_refuses_to_resend_when_dispatch_login_is_unavailable(self, caplog) -> None:
        """Refuses to resend when no trusted matching comment can be checked."""
        provider = GitHubActionsProvider(repo="owner/repo")
        error = RetryableError("request timed out")

        with (
            patch.object(provider, "_post_comment_as_pr_token_once", side_effect=error),
            patch.object(provider, "get_dispatch_login", return_value=""),
            patch.object(provider, "list_issue_comments") as mock_list_comments,
            pytest.raises(RetryableError) as exc_info,
        ):
            provider.post_comment_as_pr_token(7, "token body")

        assert exc_info.value is error
        mock_list_comments.assert_not_called()
        assert "no trusted matching comment found" in caplog.text

    def test_wraps_non_rate_limit_reconciliation_failure(self, caplog) -> None:
        """Wraps lookup failures while preserving the original posting error as the cause."""
        provider = GitHubActionsProvider(repo="owner/repo")
        posting_error = RetryableError("request timed out")
        lookup_error = RuntimeError("lookup failed")

        with (
            patch.object(provider, "_post_comment_as_pr_token_once", side_effect=posting_error),
            patch.object(provider, "get_dispatch_login", side_effect=lookup_error),
            pytest.raises(RetryableError, match="Could not verify whether the PR comment was accepted") as exc_info,
        ):
            provider.post_comment_as_pr_token(7, "token body")

        assert exc_info.value.__cause__ is posting_error
        assert "Could not reconcile ambiguous comment write" in caplog.text

    def test_propagates_rate_limit_during_reconciliation(self) -> None:
        """Propagates rate limits encountered while checking an ambiguous comment write."""
        provider = GitHubActionsProvider(repo="owner/repo")
        posting_error = RetryableError("request timed out")
        lookup_error = RetryableError("lookup rate limited", is_rate_limit=True)

        with (
            patch.object(provider, "_post_comment_as_pr_token_once", side_effect=posting_error),
            patch.object(provider, "get_dispatch_login", side_effect=lookup_error),
            pytest.raises(ProviderRateLimitError),
        ):
            provider.post_comment_as_pr_token(7, "token body")


class TestGitHubActionsProviderUpdateCommentAsPrToken:
    """Tests for dispatch-identity updates that must not migrate comment ownership."""

    @patch.dict(os.environ, {"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "pr-token"}, clear=False)
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_updates_only_a_verified_dispatch_owned_comment(self, gh_api, monkeypatch) -> None:
        gh_api.side_effect = [json.dumps({"user": {"login": "dispatch-user"}}), "{}"]
        provider = GitHubActionsProvider(repo="owner/repo")
        monkeypatch.setattr(provider, "get_pr_token_login", lambda: "dispatch-user")

        assert provider.update_comment_as_pr_token(100, "updated ledger") is None

        assert gh_api.call_args_list[0].kwargs["token"] == "pr-token"
        assert gh_api.call_args_list[0].kwargs["credential_identity"] == "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"
        assert gh_api.call_args_list[1].kwargs["method"] == "PATCH"
        assert gh_api.call_args_list[1].kwargs["token"] == "pr-token"
        assert gh_api.call_args_list[1].kwargs["body"] == {"body": "updated ledger"}

    @patch.dict(os.environ, {"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "pr-token"}, clear=False)
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_rejects_comment_not_owned_by_dispatch_identity(self, gh_api, monkeypatch) -> None:
        gh_api.return_value = json.dumps({"user": {"login": "github-actions[bot]"}})
        provider = GitHubActionsProvider(repo="owner/repo")
        monkeypatch.setattr(provider, "get_pr_token_login", lambda: "dispatch-user")

        with pytest.raises(RuntimeError, match="not owned by the verified PR-token identity"):
            provider.update_comment_as_pr_token(100, "updated ledger")

        gh_api.assert_called_once()

    @patch.dict(os.environ, {"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "pr-token"}, clear=False)
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_rejects_unverified_dispatch_identity_without_api_write(self, gh_api, monkeypatch) -> None:
        provider = GitHubActionsProvider(repo="owner/repo")
        monkeypatch.setattr(provider, "get_pr_token_login", lambda: "")

        with pytest.raises(RuntimeError, match="identity could not be verified"):
            provider.update_comment_as_pr_token(100, "updated ledger")

        gh_api.assert_not_called()

    @pytest.mark.parametrize("response", ["not-json", "[]", json.dumps({"user": {}})])
    @patch.dict(os.environ, {"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "pr-token"}, clear=False)
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_rejects_malformed_dispatch_comment_author(self, gh_api, response, monkeypatch) -> None:
        gh_api.return_value = response
        provider = GitHubActionsProvider(repo="owner/repo")
        monkeypatch.setattr(provider, "get_pr_token_login", lambda: "dispatch-user")

        with pytest.raises(RuntimeError):
            provider.update_comment_as_pr_token(100, "updated ledger")

        gh_api.assert_called_once()


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

        with patch.dict("os.environ", {"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "token-value"}, clear=True):
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

    def test_raises_when_default_token_missing(self) -> None:
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(RuntimeError, match="DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"):
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

        with patch.dict("os.environ", {"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "token-value"}, clear=True):
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

        with patch.dict("os.environ", {"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "token-value"}, clear=True):
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

        with patch.dict("os.environ", {"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "token-value"}, clear=True):
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

        with patch.dict("os.environ", {"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "token-value"}, clear=True):
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

        with patch.dict("os.environ", {"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "token-value"}, clear=True):
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

        with patch.dict("os.environ", {"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "token-value"}, clear=True):
            result = provider.dispatch_suppressed_triage(issue_number=4242, pr_number=11, review_id=42)

        assert result.success is True
        kwargs = mock_assign.call_args.kwargs
        assert kwargs["repo"] == "swai-factory/agentic-devtools"
        assert kwargs["issue_number"] == 4242
        assert kwargs["custom_agent"] == "agdt.suppressed-comment-triage.evaluate"
        assert kwargs["token_env_vars"] == ("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "GH_TOKEN")
        assert "#11" in kwargs["problem_statement"]
        assert "42" in kwargs["problem_statement"]
        assert kwargs["problem_statement"] == kwargs["custom_instructions"]

    @patch("agentic_devtools.cli.ci.github_provider.assign_issue_to_agent")
    def test_raises_when_default_token_missing(self, mock_assign) -> None:
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(RuntimeError, match="DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"):
                provider.dispatch_suppressed_triage(issue_number=4242, pr_number=11, review_id=42)
        mock_assign.assert_not_called()

    @patch("agentic_devtools.cli.ci.github_provider.assign_issue_to_agent")
    @patch("agentic_devtools.cli.ci.github_provider._read_repo_file")
    def test_raises_when_prompt_file_cannot_be_read(self, mock_read_repo_file, mock_assign) -> None:
        mock_read_repo_file.return_value = ""
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")

        with patch.dict("os.environ", {"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "token-value"}, clear=True):
            with pytest.raises(RuntimeError, match="Could not read required agent prompt file"):
                provider.dispatch_suppressed_triage(issue_number=4242, pr_number=11, review_id=42)

        mock_assign.assert_not_called()

    @patch("agentic_devtools.cli.ci.github_provider.assign_issue_to_agent")
    @patch("agentic_devtools.cli.ci.github_provider._read_repo_file")
    def test_raises_when_assignment_fails(self, mock_read_repo_file, mock_assign) -> None:
        mock_read_repo_file.return_value = "# prompt"
        mock_assign.return_value = _assignment(success=False, error="all methods failed")
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")

        with patch.dict("os.environ", {"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "token-value"}, clear=True):
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
            patch.dict("os.environ", {"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "token-value"}, clear=True),
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


def _git_stub(responses: dict):
    """Build a ``_run_git`` side effect from an args→output mapping."""

    def side_effect(args, *, stdin_text=None):
        del stdin_text
        key = tuple(args)
        if key in responses:
            result = responses[key]
            if isinstance(result, Exception):
                raise result
            return result
        raise RuntimeError(f"unexpected: {args}")

    return side_effect


class TestGitHubActionsProviderComputeDiffFiles:
    """Tests for GitHubActionsProvider.compute_diff_files."""

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_uses_pinned_base_sha_for_fetch_and_diff(self, mock_run_git) -> None:
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "base-sha"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "--name-only", "-z", "base-sha...abc123"): "a.py\0",
            }
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_files(base_branch="main", sha="abc123", base_sha="base-sha")

        assert result == ["a.py"]

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_raises_runtime_error_when_fetch_base_fails(self, mock_run_git) -> None:
        mock_run_git.side_effect = RuntimeError("network failure")
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RuntimeError, match="failed to fetch base branch main"):
            provider.compute_diff_files(base_branch="main", sha="abc123")

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_returns_changed_files(self, mock_run_git) -> None:
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "--name-only", "-z", "origin/main...abc123"): "a.py\0b.py\0",
            }
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_files(base_branch="main", sha="abc123")

        assert result == ["a.py", "b.py"]

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_returns_none_when_sha_unavailable_and_targeted_fetch_fails(self, mock_run_git) -> None:
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "deadbeef^{commit}"): RuntimeError("unknown object"),
                ("fetch", "--no-tags", "origin", "deadbeef"): RuntimeError("sha not found"),
            }
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_files(base_branch="main", sha="deadbeef")

        assert result is None

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_fetches_sha_when_not_locally_available(self, mock_run_git) -> None:
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): RuntimeError("not available"),
                ("fetch", "--no-tags", "origin", "abc123"): "",
                ("diff", "--name-only", "-z", "origin/main...abc123"): "folder/file.py\0",
            }
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_files(base_branch="main", sha="abc123")

        assert result == ["folder/file.py"]

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_raises_runtime_error_when_git_diff_fails(self, mock_run_git) -> None:
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "--name-only", "-z", "origin/main...abc123"): RuntimeError("diff command failed"),
            }
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RuntimeError, match="git diff --name-only origin/main...abc123 failed"):
            provider.compute_diff_files(base_branch="main", sha="abc123")

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_preserves_unusual_filenames_without_stripping(self, mock_run_git) -> None:
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "--name-only", "-z", "origin/main...abc123"): " leading.txt\0trailing.txt \0quoted\\name.py\0",
            }
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_files(base_branch="main", sha="abc123")

        assert result == [" leading.txt", "trailing.txt ", "quoted\\name.py"]

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_create_review_thread_posts_validated_diff_location(self, mock_gh_api, monkeypatch) -> None:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        monkeypatch.setenv("GH_TOKEN", "ambient-token")
        monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "human-token")
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")
        mock_gh_api.return_value = json.dumps(
            {
                "id": 123,
                "path": "src/app.py",
                "line": 9,
                "side": "RIGHT",
                "body": "Finding",
                "html_url": "https://github.com/owner/repo/pull/4#discussion_r123",
                "pull_request_review_id": 456,
                "user": {"login": "agent[bot]"},
            }
        )
        provider = GitHubActionsProvider(repo="owner/repo")
        provider._thread_signals_cache[4] = {123: (False, False, None, "", None)}
        provider._thread_identity_cache[4] = {"thread": (False, (123,))}

        with (
            patch.object(provider, "get_pr_metadata", return_value=SimpleNamespace(head_sha="head-sha")),
            patch.object(provider, "get_bookkeeping_token_login", return_value="github-actions[bot]"),
        ):
            result = provider.create_review_thread(
                pr_number=4,
                commit_sha="head-sha",
                path="src/app.py",
                line=9,
                side="RIGHT",
                body="Finding @copilot",
            )

        assert result.id == 123
        assert result.html_url.endswith("discussion_r123")
        assert result.source_review_id == 456
        assert 4 not in provider._thread_signals_cache
        assert 4 not in provider._thread_identity_cache
        assert mock_gh_api.call_args.kwargs["token"] == "bot-token"
        assert mock_gh_api.call_args.kwargs["credential_identity"] == "AI_PR_LOOP_BOOKKEEPING_TOKEN"
        assert mock_gh_api.call_args.kwargs["body"] == {
            "body": "Finding @\u200bcopilot\n\n🤖 AI PR Loop ·",
            "commit_id": "head-sha",
            "path": "src/app.py",
            "line": 9,
            "side": "RIGHT",
        }

    @pytest.mark.parametrize(
        ("arguments", "message"),
        [
            ({"pr_number": 0}, "pr_number"),
            ({"commit_sha": ""}, "commit_sha"),
            ({"path": ""}, "path"),
            ({"line": 0}, "line"),
            ({"side": "CENTER"}, "side"),
        ],
    )
    def test_create_review_thread_validates_arguments(self, arguments: dict[str, Any], message: str) -> None:
        values: dict[str, Any] = {
            "pr_number": 4,
            "commit_sha": "head-sha",
            "path": "src/app.py",
            "line": 9,
            "side": "RIGHT",
            "body": "Finding",
        }
        values.update(arguments)

        with pytest.raises(ValueError, match=message):
            GitHubActionsProvider(repo="owner/repo").create_review_thread(**values)

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_create_review_thread_propagates_provider_errors(self, mock_gh_api, monkeypatch) -> None:
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")
        mock_gh_api.side_effect = RuntimeError("GitHub API unavailable")
        provider = GitHubActionsProvider(repo="owner/repo")

        with (
            patch.object(provider, "get_pr_metadata", return_value=SimpleNamespace(head_sha="head-sha")),
            patch.object(provider, "get_bookkeeping_token_login", return_value="github-actions[bot]"),
            pytest.raises(RuntimeError, match="GitHub API unavailable"),
        ):
            provider.create_review_thread(
                pr_number=4,
                commit_sha="head-sha",
                path="src/app.py",
                line=9,
                side="RIGHT",
                body="Finding",
            )

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_create_review_thread_propagates_non_rate_limit_retryable_error(self, mock_gh_api, monkeypatch) -> None:
        """A transient non-rate-limit failure from the POST keeps its original exception type."""
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")
        error = RetryableError("GitHub API unavailable", is_rate_limit=False)
        mock_gh_api.side_effect = error
        provider = GitHubActionsProvider(repo="owner/repo")

        with (
            patch.object(provider, "get_pr_metadata", return_value=SimpleNamespace(head_sha="head-sha")),
            patch.object(provider, "get_bookkeeping_token_login", return_value="github-actions[bot]"),
            pytest.raises(RetryableError) as exc_info,
        ):
            provider.create_review_thread(
                pr_number=4,
                commit_sha="head-sha",
                path="src/app.py",
                line=9,
                side="RIGHT",
                body="Finding",
            )

        assert exc_info.value is error
        mock_gh_api.assert_called_once()

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_create_review_thread_converts_rate_limit_without_retrying(self, mock_gh_api, monkeypatch) -> None:
        """A rate-limited promotion POST propagates cooldown metadata without retrying the uncertain write."""
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")
        error = RetryableError(
            "GitHub API rate limited (HTTP 429)",
            retry_after=37,
            reset_timestamp=1234567890,
            remaining=0,
            provider="github",
            credential_identity="AI_PR_LOOP_BOOKKEEPING_TOKEN",
            source="response-header",
            is_rate_limit=True,
        )
        mock_gh_api.side_effect = error
        provider = GitHubActionsProvider(repo="owner/repo")

        with (
            patch.object(provider, "get_pr_metadata", return_value=SimpleNamespace(head_sha="head-sha")),
            patch.object(provider, "get_bookkeeping_token_login", return_value="github-actions[bot]"),
            pytest.raises(ProviderRateLimitError) as exc_info,
        ):
            provider.create_review_thread(
                pr_number=4,
                commit_sha="head-sha",
                path="src/app.py",
                line=9,
                side="RIGHT",
                body="Finding",
            )

        assert exc_info.value.metadata == error.metadata
        mock_gh_api.assert_called_once()

    @pytest.mark.parametrize("comment_id", [0, "123"])
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_create_review_thread_rejects_malformed_response_id(self, mock_gh_api, comment_id, monkeypatch) -> None:
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")
        mock_gh_api.return_value = json.dumps({"id": comment_id})
        provider = GitHubActionsProvider(repo="owner/repo")

        with (
            patch.object(provider, "get_pr_metadata", return_value=SimpleNamespace(head_sha="head-sha")),
            patch.object(provider, "get_bookkeeping_token_login", return_value="github-actions[bot]"),
            pytest.raises(RuntimeError, match="malformed review-comment ID"),
        ):
            provider.create_review_thread(
                pr_number=4,
                commit_sha="head-sha",
                path="src/app.py",
                line=9,
                side="RIGHT",
                body="Finding",
            )

    @patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value="[]")
    def test_create_review_thread_rejects_non_object_response(self, _mock_gh_api, monkeypatch) -> None:
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")
        provider = GitHubActionsProvider(repo="owner/repo")

        with (
            patch.object(provider, "get_pr_metadata", return_value=SimpleNamespace(head_sha="head-sha")),
            patch.object(provider, "get_bookkeeping_token_login", return_value="github-actions[bot]"),
            pytest.raises(RuntimeError, match="malformed review-comment response"),
        ):
            provider.create_review_thread(
                pr_number=4,
                commit_sha="head-sha",
                path="src/app.py",
                line=9,
                side="RIGHT",
                body="Finding",
            )

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_create_review_thread_does_not_fall_back_to_human_token(self, mock_gh_api, monkeypatch) -> None:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        monkeypatch.delenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", raising=False)
        monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "human-token")
        provider = GitHubActionsProvider(repo="owner/repo")

        with (
            patch.object(provider, "get_pr_metadata", return_value=SimpleNamespace(head_sha="head-sha")),
            pytest.raises(RuntimeError, match="AI_PR_LOOP_BOOKKEEPING_TOKEN"),
        ):
            provider.create_review_thread(
                pr_number=4,
                commit_sha="head-sha",
                path="src/app.py",
                line=9,
                side="RIGHT",
                body="Finding",
            )

        mock_gh_api.assert_not_called()

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_create_review_thread_rejects_a_stale_head(self, mock_gh_api) -> None:
        provider = GitHubActionsProvider(repo="owner/repo")
        with patch.object(provider, "get_pr_metadata", return_value=SimpleNamespace(head_sha="new-head")):
            with pytest.raises(RuntimeError, match="current HEAD is new-head"):
                provider.create_review_thread(
                    pr_number=4,
                    commit_sha="captured-head",
                    path="src/app.py",
                    line=9,
                    side="RIGHT",
                    body="Finding",
                )

        mock_gh_api.assert_not_called()

    @patch.object(GitHubActionsProvider, "get_commit_range_diff")
    @patch.object(GitHubActionsProvider, "list_all_review_comments")
    @patch.object(GitHubActionsProvider, "create_review_thread")
    def test_promotes_each_missed_occurrence_as_a_distinct_native_thread(
        self, mock_create, mock_list_comments, mock_diff
    ) -> None:
        body = (
            "<!-- ccr-overview-v2 -->\n0 open findings\n"
            "<details><summary>Previously missed (2)</summary>\n"
            "### [P1] Repeat this wording\n**File:** `src/a.py`\n**Line:** 2\nFirst.\n"
            "### [P1] Repeat this wording\n**File:** `src/a.py`\n**Line:** 2\nSecond.\n"
            "</details>"
        )
        mock_diff.return_value = (
            "diff --git a/src/a.py b/src/a.py\n--- a/src/a.py\n+++ b/src/a.py\n@@ -2,1 +2,2 @@\n+added\n context\n"
        )
        mock_list_comments.return_value = []
        mock_create.side_effect = [
            ReviewCommentInfo(id=101, path="src/a.py", body="first", html_url="url-1"),
            ReviewCommentInfo(id=102, path="src/a.py", body="second", html_url="url-2"),
        ]
        reviews = [
            ReviewInfo(
                id=55,
                user="copilot-pull-request-reviewer[bot]",
                state="COMMENTED",
                body=body,
                commit_sha="head-sha",
            )
        ]
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.promote_ccr_findings(
            pr_number=4,
            commit_sha="head-sha",
            base_sha="base-sha",
            reviews=reviews,
        )

        assert [comment.id for comment in result] == [101, 102]
        assert "ccr-promoted:55:previously_missed:1" in mock_create.call_args_list[0].kwargs["body"]
        assert "ccr-promoted:55:previously_missed:2" in mock_create.call_args_list[1].kwargs["body"]
        assert all(call.kwargs["line"] == 2 for call in mock_create.call_args_list)
        assert all(comment.source_review_id == 55 for comment in result)
        assert provider._get_pr_review_comment_inventory(4) == result
        mock_list_comments.assert_called_once_with(4)

    @pytest.mark.parametrize("state", ["DISMISSED", "PENDING"])
    @patch.object(GitHubActionsProvider, "get_commit_range_diff")
    @patch.object(GitHubActionsProvider, "list_all_review_comments")
    @patch.object(GitHubActionsProvider, "create_review_thread")
    def test_does_not_promote_findings_from_non_actionable_reviews(
        self, mock_create, mock_list_comments, mock_diff, state
    ) -> None:
        review = ReviewInfo(
            id=56,
            user="copilot-pull-request-reviewer[bot]",
            state=state,
            body=(
                "<details><summary>Previously missed (1)</summary>\n"
                "### [P1] Finding\n**File:** `src/a.py`\n**Line:** 2\nDetails\n</details>"
            ),
            commit_sha="head-sha",
        )

        result = GitHubActionsProvider(repo="owner/repo").promote_ccr_findings(
            pr_number=4,
            commit_sha="head-sha",
            base_sha="base-sha",
            reviews=[review],
        )

        assert result == []
        mock_diff.assert_not_called()
        mock_list_comments.assert_not_called()
        mock_create.assert_not_called()

    @patch.object(GitHubActionsProvider, "get_commit_range_diff")
    @patch.object(GitHubActionsProvider, "list_all_review_comments")
    @patch.object(GitHubActionsProvider, "create_review_thread")
    def test_same_finding_in_distinct_reviews_gets_distinct_occurrence_markers(
        self, mock_create, mock_list_comments, mock_diff
    ) -> None:
        body = (
            "<details><summary>Previously missed (1)</summary>\n"
            "### Same title\n**File:** `src/a.py`\n**Line:** 2\nSame body\n</details>"
        )
        mock_diff.return_value = "diff --git a/src/a.py b/src/a.py\n+++ b/src/a.py\n@@ -1 +1,2 @@\n+new\n"
        mock_list_comments.return_value = []
        mock_create.side_effect = [
            ReviewCommentInfo(401, "src/a.py", "first", "url-1"),
            ReviewCommentInfo(402, "src/a.py", "second", "url-2"),
        ]
        reviews = [
            ReviewInfo(51, "Copilot", "COMMENTED", body=body),
            ReviewInfo(52, "Copilot", "COMMENTED", body=body),
        ]

        GitHubActionsProvider(repo="owner/repo").promote_ccr_findings(
            pr_number=4,
            commit_sha="head",
            base_sha="base",
            reviews=reviews,
        )

        markers = [call.kwargs["body"] for call in mock_create.call_args_list]
        assert "ccr-promoted:51:previously_missed:1" in markers[0]
        assert "ccr-promoted:52:previously_missed:1" in markers[1]

    @pytest.mark.parametrize(
        ("matched_source_path", "selection_is_none"),
        [(True, False), (False, False), (False, True)],
    )
    @patch.object(GitHubActionsProvider, "get_commit_range_diff", return_value="diff")
    @patch.object(GitHubActionsProvider, "list_all_review_comments", return_value=[])
    @patch.object(GitHubActionsProvider, "create_review_thread")
    @patch("agentic_devtools.cli.ci.github_provider.select_review_anchor")
    def test_promotion_handles_anchor_selection_and_sdk_fallback(
        self, mock_select, mock_create, _mock_list_comments, _mock_diff, matched_source_path, selection_is_none
    ) -> None:
        initial = (
            None
            if selection_is_none
            else AnchorSelection(
                ReviewThreadAnchor("src/a.py", 10),
                used_fallback=False,
                matched_source_path=matched_source_path,
            )
        )
        suggested = AnchorSelection(ReviewThreadAnchor("src/related.py", 5), used_fallback=True)
        mock_select.side_effect = [initial] if matched_source_path or selection_is_none else [initial, suggested]
        mock_create.return_value = ReviewCommentInfo(601, "src/a.py", "body", "url")
        provider = GitHubActionsProvider(repo="owner/repo")
        review = ReviewInfo(
            60,
            "Copilot",
            "COMMENTED",
            body=(
                "<details><summary>Previously missed (1)</summary>\n"
                "### Finding\n**File:** `src/a.py`\n**Line:** 10\nDetails\n</details>"
            ),
        )

        with patch.object(
            provider,
            "_select_related_review_anchor_via_sdk",
            return_value=("src/related.py", 5),
        ) as sdk_selector:
            if selection_is_none:
                with pytest.raises(RuntimeError, match="no changed-line anchor"):
                    provider.promote_ccr_findings(
                        pr_number=4,
                        commit_sha="head",
                        base_sha="base",
                        reviews=[review],
                    )
            else:
                provider.promote_ccr_findings(
                    pr_number=4,
                    commit_sha="head",
                    base_sha="base",
                    reviews=[review],
                )

        if initial is None:
            sdk_selector.assert_not_called()
            mock_create.assert_not_called()
        elif initial.matched_source_path:
            sdk_selector.assert_not_called()
            assert mock_select.call_count == 1
            assert mock_create.call_args.kwargs["path"] == initial.anchor.path
        else:
            sdk_selector.assert_called_once()
            assert mock_select.call_count == 2
            assert mock_select.call_args.kwargs["suggested_path"] == "src/related.py"
            assert mock_select.call_args.kwargs["suggested_line"] == 5
            assert mock_create.call_args.kwargs["path"] == suggested.anchor.path
            assert mock_create.call_args.kwargs["line"] == suggested.anchor.line

    @patch.object(GitHubActionsProvider, "get_pr_token_login", return_value="workflow[bot]")
    @patch.object(GitHubActionsProvider, "get_commit_range_diff")
    @patch.object(GitHubActionsProvider, "list_all_review_comments")
    @patch.object(GitHubActionsProvider, "create_review_thread")
    def test_marker_quoted_by_an_earlier_finding_does_not_reuse_its_thread(
        self, mock_create, mock_list_comments, mock_diff, _mock_login
    ) -> None:
        second_marker = "<!-- ccr-promoted:55:previously_missed:2 -->"
        body = (
            "<details><summary>Previously missed (2)</summary>\n"
            "### First finding\n**File:** `src/a.py`\n**Line:** 2\n"
            f"Quoted marker: {second_marker}\n"
            "### Second finding\n**File:** `src/a.py`\n**Line:** 3\nSecond body\n</details>"
        )
        mock_diff.return_value = "diff --git a/src/a.py b/src/a.py\n+++ b/src/a.py\n@@ -1 +1,3 @@\n+one\n+two\n"
        mock_list_comments.return_value = []
        created: list[ReviewCommentInfo] = []

        def create_thread(**kwargs) -> ReviewCommentInfo:
            comment = ReviewCommentInfo(
                id=501 + len(created),
                path=kwargs["path"],
                body=kwargs["body"],
                html_url=f"url-{len(created)}",
                author_login="workflow[bot]",
            )
            created.append(comment)
            return comment

        mock_create.side_effect = create_thread
        review = ReviewInfo(55, "Copilot", "COMMENTED", body=body)

        result = GitHubActionsProvider(repo="owner/repo").promote_ccr_findings(
            pr_number=4,
            commit_sha="head",
            base_sha="base",
            reviews=[review],
        )

        assert [comment.id for comment in result] == [501, 502]
        assert mock_create.call_count == 2

    def test_nonzero_unrecoverable_count_fails_closed(self) -> None:
        review = ReviewInfo(
            55,
            "Copilot",
            "COMMENTED",
            body="<details><summary>Previously missed (2)</summary></details>",
        )

        with pytest.raises(RuntimeError, match="review 55 section previously_missed recovered 0/2"):
            GitHubActionsProvider(repo="owner/repo").promote_ccr_findings(
                pr_number=4,
                commit_sha="head",
                base_sha="base",
                reviews=[review],
            )

    @patch.object(GitHubActionsProvider, "get_commit_range_diff")
    @patch.object(GitHubActionsProvider, "list_all_review_comments")
    def test_missing_captured_sha_blocks_outstanding_promotions(self, mock_list_comments, mock_diff) -> None:
        mock_diff.return_value = ""
        mock_list_comments.return_value = []
        review = ReviewInfo(
            55,
            "Copilot",
            "COMMENTED",
            body=(
                "<details><summary>Previously missed (1)</summary>\n### Finding\n**File:** `src/a.py`\nBody\n</details>"
            ),
        )

        with pytest.raises(RuntimeError, match="captured base and head SHAs"):
            GitHubActionsProvider(repo="owner/repo").promote_ccr_findings(
                pr_number=4,
                commit_sha="head",
                base_sha="",
                reviews=[review],
            )

    @patch.object(GitHubActionsProvider, "get_commit_range_diff")
    @patch.object(GitHubActionsProvider, "list_all_review_comments")
    @patch.object(GitHubActionsProvider, "create_review_thread")
    def test_missing_repository_identity_blocks_promotions(
        self, mock_create, mock_list_comments, mock_diff, monkeypatch
    ) -> None:
        monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
        mock_diff.return_value = "diff --git a/src/a.py b/src/a.py\n+++ b/src/a.py\n@@ -1 +1,2 @@\n+new\n"
        mock_list_comments.return_value = []
        review = ReviewInfo(
            55,
            "Copilot",
            "COMMENTED",
            body=(
                "<details><summary>Previously missed (1)</summary>\n"
                "### Finding\n**File:** `src/a.py`\n**Line:** 2\nBody\n</details>"
            ),
        )

        with pytest.raises(RuntimeError, match="repository identity is unavailable"):
            GitHubActionsProvider().promote_ccr_findings(
                pr_number=4,
                commit_sha="head",
                base_sha="base",
                reviews=[review],
            )
        mock_create.assert_not_called()

    @patch.object(GitHubActionsProvider, "get_commit_range_diff")
    @patch.object(GitHubActionsProvider, "list_all_review_comments")
    @patch.object(GitHubActionsProvider, "create_review_thread")
    def test_uncertain_create_response_is_recovered_by_marker_lookup(
        self, mock_create, mock_list_comments, mock_diff
    ) -> None:
        marker = "<!-- ccr-promoted:55:previously_missed:1 -->"
        recovered = ReviewCommentInfo(501, "src/a.py", marker, "recovered-url", author_login="workflow[bot]")
        mock_diff.return_value = "diff --git a/src/a.py b/src/a.py\n+++ b/src/a.py\n@@ -1 +1,2 @@\n+new\n"
        mock_list_comments.side_effect = [[], [recovered]]
        mock_create.side_effect = RuntimeError("response lost")
        review = ReviewInfo(
            55,
            "Copilot",
            "COMMENTED",
            body=(
                "<details><summary>Previously missed (1)</summary>\n"
                "### Finding\n**File:** `src/a.py`\n**Line:** 2\nBody\n</details>"
            ),
        )

        provider = GitHubActionsProvider(repo="owner/repo")
        with (
            patch.object(provider, "get_bookkeeping_token_login", return_value=""),
            patch.object(provider, "get_pr_token_login", return_value="workflow[bot]"),
        ):
            result = provider.promote_ccr_findings(
                pr_number=4,
                commit_sha="head",
                base_sha="base",
                reviews=[review],
            )

        assert [comment.id for comment in result] == [501]
        assert [comment.id for comment in provider._get_pr_review_comment_inventory(4)] == [501]

    @patch.object(GitHubActionsProvider, "get_commit_range_diff")
    @patch.object(GitHubActionsProvider, "list_all_review_comments", return_value=[])
    @patch.object(GitHubActionsProvider, "create_review_thread")
    def test_oversized_promoted_finding_reserves_the_final_occurrence_marker(
        self, mock_create, _mock_list_comments, mock_diff
    ) -> None:
        marker = "<!-- ccr-promoted:55:previously_missed:1 -->"
        mock_diff.return_value = "diff --git a/src/a.py b/src/a.py\n+++ b/src/a.py\n@@ -1 +1,2 @@\n+new\n"
        mock_create.return_value = ReviewCommentInfo(601, "src/a.py", "", "url")
        review = ReviewInfo(
            55,
            "Copilot",
            "COMMENTED",
            body=(
                "<details><summary>Previously missed (1)</summary>\n"
                "### Finding\n**File:** `src/a.py`\n**Line:** 2\n"
                f"{'x' * _MAX_COMMENT_BODY_CHARS}\n</details>"
            ),
        )

        GitHubActionsProvider(repo="owner/repo").promote_ccr_findings(
            pr_number=4,
            commit_sha="head",
            base_sha="base",
            reviews=[review],
        )

        comment_body = mock_create.call_args.kwargs["body"]
        assert len(comment_body) <= _MAX_COMMENT_BODY_CHARS
        assert comment_body.rstrip().endswith(marker)
        assert "[… embedded content trimmed to fit comment size limit …]" in comment_body

    @patch.object(GitHubActionsProvider, "get_commit_range_diff")
    @patch.object(GitHubActionsProvider, "list_all_review_comments", return_value=[])
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_neutralizes_mentions_before_budgeting_promoted_finding(
        self, mock_gh_api, _mock_list_comments, mock_diff, monkeypatch
    ) -> None:
        marker = "<!-- ccr-promoted:55:previously_missed:1 -->"
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")
        mock_diff.return_value = "diff --git a/src/a.py b/src/a.py\n+++ b/src/a.py\n@@ -1 +1,2 @@\n+new\n"
        mock_gh_api.return_value = json.dumps({"id": 601, "path": "src/a.py", "line": 2})
        review = ReviewInfo(
            55,
            "Copilot",
            "COMMENTED",
            body=(
                "<details><summary>Previously missed (1)</summary>\n"
                "### Finding\n**File:** `src/a.py`\n**Line:** 2\n"
                f"{'@copilot ' * 6600}\n</details>"
            ),
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        with (
            patch.object(provider, "get_pr_metadata", return_value=SimpleNamespace(head_sha="head")),
            patch.object(provider, "get_bookkeeping_token_login", return_value="github-actions[bot]"),
        ):
            provider.promote_ccr_findings(
                pr_number=4,
                commit_sha="head",
                base_sha="base",
                reviews=[review],
            )

        comment_body = mock_gh_api.call_args.kwargs["body"]["body"]
        assert len(comment_body) <= _MAX_COMMENT_BODY_CHARS
        assert comment_body.endswith(f"{marker}\n\n🤖 AI PR Loop ·")
        assert "@\u200bcopilot" in comment_body

    @patch.object(GitHubActionsProvider, "get_commit_range_diff")
    @patch.object(GitHubActionsProvider, "list_all_review_comments")
    @patch.object(GitHubActionsProvider, "create_review_thread")
    def test_create_error_is_preserved_when_marker_lookup_fails(
        self, mock_create, mock_list_comments, mock_diff
    ) -> None:
        mock_diff.return_value = "diff --git a/src/a.py b/src/a.py\n+++ b/src/a.py\n@@ -1 +1,2 @@\n+new\n"
        mock_list_comments.side_effect = [[], RuntimeError("lookup failed")]
        mock_create.side_effect = RuntimeError("create failed")
        review = ReviewInfo(
            55,
            "Copilot",
            "COMMENTED",
            body=(
                "<details><summary>Previously missed (1)</summary>\n"
                "### Finding\n**File:** `src/a.py`\n**Line:** 2\nBody\n</details>"
            ),
        )

        with pytest.raises(RuntimeError, match="create failed"):
            GitHubActionsProvider(repo="owner/repo").promote_ccr_findings(
                pr_number=4,
                commit_sha="head",
                base_sha="base",
                reviews=[review],
            )

    @patch.object(GitHubActionsProvider, "get_commit_range_diff")
    @patch.object(GitHubActionsProvider, "list_all_review_comments")
    @patch.object(GitHubActionsProvider, "create_review_thread")
    def test_uncertain_create_ignores_marker_from_another_author(
        self, mock_create, mock_list_comments, mock_diff
    ) -> None:
        marker = "<!-- ccr-promoted:55:previously_missed:1 -->"
        untrusted = ReviewCommentInfo(502, "src/a.py", marker, "attacker-url", author_login="attacker")
        mock_diff.return_value = "diff --git a/src/a.py b/src/a.py\n+++ b/src/a.py\n@@ -1 +1,2 @@\n+new\n"
        mock_list_comments.side_effect = [[], [untrusted]]
        mock_create.side_effect = RuntimeError("response lost")
        review = ReviewInfo(
            55,
            "Copilot",
            "COMMENTED",
            body=(
                "<details><summary>Previously missed (1)</summary>\n"
                "### Finding\n**File:** `src/a.py`\n**Line:** 2\nBody\n</details>"
            ),
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        with (
            patch.object(provider, "get_bookkeeping_token_login", return_value="github-actions[bot]"),
            patch.object(provider, "get_pr_token_login", return_value="workflow[bot]"),
            pytest.raises(RuntimeError, match="response lost"),
        ):
            provider.promote_ccr_findings(
                pr_number=4,
                commit_sha="head",
                base_sha="base",
                reviews=[review],
            )

    @patch.object(GitHubActionsProvider, "_run_prompt_via_sdk")
    def test_sdk_review_anchor_candidate_is_parsed(self, mock_prompt) -> None:
        mock_prompt.return_value = json.dumps({"path": "src/related.py", "line": 8})
        finding = CCRFinding("previously_missed", 1, "P1", "Title", "body", "src/original.py", 12)

        result = GitHubActionsProvider()._select_related_review_anchor_via_sdk(finding, "diff")

        assert result == ("src/related.py", 8)
        assert mock_prompt.call_args.kwargs["timeout_seconds"] == 30

    @pytest.mark.parametrize(
        "raw",
        [
            None,
            "not-json",
            "[]",
            '{"path": "", "line": 1}',
            '{"path": 3, "line": 1}',
            '{"path": "a.py"}',
            '{"path": "a.py", "line": true}',
            '{"path": "a.py", "line": 0}',
        ],
    )
    @patch.object(GitHubActionsProvider, "_run_prompt_via_sdk")
    def test_sdk_anchor_malformed_or_invalid_candidates_are_rejected(self, mock_prompt, raw) -> None:
        mock_prompt.return_value = raw
        finding = CCRFinding("previously_missed", 1, "", "Title", "body", "src/a.py", None)

        assert GitHubActionsProvider()._select_related_review_anchor_via_sdk(finding, "diff") == ("", None)

    @patch.object(GitHubActionsProvider, "_run_prompt_via_sdk")
    def test_sdk_anchor_selection_failure_degrades_to_diff_order_fallback(self, mock_prompt) -> None:
        mock_prompt.side_effect = RuntimeError("SDK unavailable")
        finding = CCRFinding("previously_missed", 1, "", "Title", "body", "src/a.py", None)

        assert GitHubActionsProvider()._select_related_review_anchor_via_sdk(finding, "diff") == ("", None)

    @patch.object(GitHubActionsProvider, "get_commit_range_diff")
    @patch.object(GitHubActionsProvider, "list_all_review_comments")
    @patch.object(GitHubActionsProvider, "create_review_thread")
    def test_create_error_without_recovered_marker_is_not_reported_as_success(
        self, mock_create, mock_list_comments, mock_diff
    ) -> None:
        mock_diff.return_value = "diff --git a/src/a.py b/src/a.py\n+++ b/src/a.py\n@@ -1 +1,2 @@\n+new\n"
        mock_list_comments.side_effect = [[], []]
        mock_create.side_effect = RuntimeError("create failed")
        review = ReviewInfo(
            55,
            "Copilot",
            "COMMENTED",
            body=(
                "<details><summary>Previously missed (1)</summary>\n"
                "### Finding\n**File:** `src/a.py`\n**Line:** 2\nBody\n</details>"
            ),
        )

        with pytest.raises(RuntimeError, match="create failed"):
            GitHubActionsProvider(repo="owner/repo").promote_ccr_findings(
                pr_number=4,
                commit_sha="head",
                base_sha="base",
                reviews=[review],
            )

    def test_partial_promotion_cache_remains_visible_after_later_create_fails(self) -> None:
        body = (
            "<details><summary>Previously missed (2)</summary>\n"
            "### First finding\n**File:** `src/a.py`\n**Line:** 1\nFirst body\n"
            "### Second finding\n**File:** `src/a.py`\n**Line:** 2\nSecond body\n</details>"
        )
        review = ReviewInfo(55, "Copilot", "COMMENTED", body=body)
        first_native = ReviewCommentInfo(501, "src/a.py", "First finding", "first-url", source_review_id=55)
        provider = GitHubActionsProvider(repo="owner/repo")

        def review_endpoint_response(url: str, *_args: object, **_kwargs: object) -> str:
            if url.endswith("/pulls/4/reviews/55/comments"):
                return "[]"
            if url.endswith("/pulls/4/reviews/55"):
                return json.dumps({"body": body})
            raise AssertionError(f"Unexpected GitHub endpoint: {url}")

        with (
            patch.object(
                provider,
                "get_commit_range_diff",
                return_value=(
                    "diff --git a/src/a.py b/src/a.py\n--- a/src/a.py\n+++ b/src/a.py\n@@ -1 +1,3 @@\n+first\n+second\n"
                ),
            ),
            patch.object(provider, "list_all_review_comments", return_value=[]),
            patch.object(
                provider,
                "create_review_thread",
                side_effect=[first_native, RuntimeError("second create failed")],
            ),
            patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=review_endpoint_response),
        ):
            with pytest.raises(RuntimeError, match="second create failed"):
                provider.promote_ccr_findings(
                    pr_number=4,
                    commit_sha="head",
                    base_sha="base",
                    reviews=[review],
                )
            assert provider.list_review_comments(4, 55) == [first_native]

    def test_partial_suppressed_promotion_replaces_only_its_synthetic_occurrence(self) -> None:
        body = (
            "<details><summary>Comments suppressed due to low confidence (2)</summary>\n"
            "**src/a.py**: First body\n"
            "**src/a.py**: Second body\n"
            "</details>"
        )
        review = ReviewInfo(55, "Copilot", "COMMENTED", body=body)
        first_native = ReviewCommentInfo(501, "src/a.py", "First body", "first-url", source_review_id=55)
        provider = GitHubActionsProvider(repo="owner/repo")

        def review_endpoint_response(url: str, *_args: object, **_kwargs: object) -> str:
            if url.endswith("/pulls/4/reviews/55/comments"):
                return "[]"
            if url.endswith("/pulls/4/reviews/55"):
                return json.dumps({"body": body})
            raise AssertionError(f"Unexpected GitHub endpoint: {url}")

        with (
            patch.object(
                provider,
                "get_commit_range_diff",
                return_value=(
                    "diff --git a/src/a.py b/src/a.py\n--- a/src/a.py\n+++ b/src/a.py\n@@ -1 +1,3 @@\n+first\n+second\n"
                ),
            ),
            patch.object(provider, "list_all_review_comments", return_value=[]),
            patch.object(
                provider,
                "create_review_thread",
                side_effect=[first_native, RuntimeError("second create failed")],
            ),
            patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=review_endpoint_response),
        ):
            with pytest.raises(RuntimeError, match="second create failed"):
                provider.promote_ccr_findings(
                    pr_number=4,
                    commit_sha="head",
                    base_sha="base",
                    reviews=[review],
                )

            comments = provider.list_review_comments(4, 55)
            assert [(comment.id, comment.body) for comment in comments] == [(-2, "Second body"), (501, "First body")]

    def test_skips_and_replaces_explicitly_resolved_suppressed_occurrence(self) -> None:
        review = ReviewInfo(
            55,
            "Copilot",
            "COMMENTED",
            body=(
                "<details><summary>Comments suppressed due to low confidence (1)</summary>\n"
                "**src/a.py**: Resolved since the previous review.\n"
                "</details>"
            ),
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        assert (
            provider.promote_ccr_findings(
                pr_number=4,
                commit_sha="head",
                base_sha="base",
                reviews=[review],
            )
            == []
        )
        assert provider._ccr_replaced_suppressed_occurrences == {55: {1}}

    def test_inventory_recovery_ignores_explicitly_resolved_findings_without_markers(self) -> None:
        review_body = (
            "<details><summary>Previously missed (2)</summary>\n"
            "### [P1] Existing promotion\n"
            "**File:** `src/a.py`\n"
            "**Line:** 2\n"
            "Needs action.\n"
            "### [P1] Resolved finding\n"
            "**File:** `src/a.py`\n"
            "**Line:** 3\n"
            "Resolved since the previous review.\n"
            "</details>"
        )
        marker = "<!-- ccr-promoted:55:previously_missed:1 -->"
        promoted_root = ReviewCommentInfo(
            201,
            "src/a.py",
            f"Existing promotion\n\n{marker}",
            "comment-url",
            author_login="legacy-workflow",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        def review_endpoint_response(url: str, *_args: object, **_kwargs: object) -> str:
            if url.endswith("/pulls/4/reviews/55/comments"):
                return "[]"
            if url.endswith("/pulls/4/reviews/55"):
                return json.dumps({"body": review_body})
            raise AssertionError(f"Unexpected GitHub endpoint: {url}")

        with (
            patch.object(provider, "list_all_review_comments", return_value=[promoted_root]),
            patch.object(provider, "get_bookkeeping_token_login", return_value=""),
            patch.object(provider, "get_pr_token_login", return_value="legacy-workflow"),
            patch.object(provider, "_has_unresolved_configured_review_bookkeeping_identity", return_value=False),
            patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=review_endpoint_response),
        ):
            comments = provider.list_review_comments(4, 55)

        assert [comment.id for comment in comments] == [201]
        assert comments[0].source_review_id == 55

    def test_replaced_structured_suppressed_occurrence_filters_all_synthetic_fragments(self) -> None:
        body = (
            "<details><summary>Comments suppressed due to low confidence (1)</summary>\n"
            "### Finding\n"
            "**File:** `src/a.py`\n"
            "**Line:** 12\n"
            "Resolved since the previous review.\n"
            "</details>"
        )
        provider = GitHubActionsProvider(repo="owner/repo")
        provider._ccr_replaced_suppressed_occurrences[55] = {1}

        def review_endpoint_response(url: str, *_args: object, **_kwargs: object) -> str:
            if url.endswith("/pulls/4/reviews/55/comments"):
                return "[]"
            if url.endswith("/pulls/4/reviews/55"):
                return json.dumps({"body": body})
            raise AssertionError(f"Unexpected GitHub endpoint: {url}")

        with (
            patch.object(provider, "list_all_review_comments", return_value=[]),
            patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=review_endpoint_response),
        ):
            comments, recovery_complete = provider._list_review_comments_with_recovery_status(4, 55)

        assert recovery_complete
        assert comments == []

    @patch.object(GitHubActionsProvider, "get_commit_range_diff")
    @patch.object(GitHubActionsProvider, "list_all_review_comments")
    @patch.object(GitHubActionsProvider, "create_review_thread")
    def test_promotion_retry_reuses_existing_marker_without_creating_duplicate(
        self, mock_create, mock_list_comments, mock_diff
    ) -> None:
        marker = "<!-- ccr-promoted:55:previously_missed:1 -->"
        existing = ReviewCommentInfo(
            201,
            "src/a.py",
            f"body\n\n{marker}\n\n🤖 AI PR Loop ·",
            "comment-url",
            author_login="workflow[bot]",
        )
        mock_list_comments.return_value = [existing]
        mock_diff.return_value = "diff --git a/src/a.py b/src/a.py\n+++ b/src/a.py\n@@ -1 +1,2 @@\n+new\n"
        review = ReviewInfo(
            id=55,
            user="Copilot",
            state="COMMENTED",
            body=(
                "<details><summary>Previously missed (1)</summary>\n"
                "### [P1] Finding\n**File:** `src/a.py`\n**Line:** 2\nBody\n</details>"
            ),
        )

        provider = GitHubActionsProvider(repo="owner/repo")
        with patch.object(provider, "get_pr_token_login", return_value="workflow[bot]"):
            result = provider.promote_ccr_findings(
                pr_number=4,
                commit_sha="head",
                base_sha="base",
                reviews=[review],
            )

        assert [comment.id for comment in result] == [201]
        assert result[0].source_review_id == 55
        mock_create.assert_not_called()

    @patch.object(GitHubActionsProvider, "get_commit_range_diff")
    @patch.object(GitHubActionsProvider, "list_all_review_comments")
    @patch.object(GitHubActionsProvider, "create_review_thread")
    def test_unresolved_bookkeeping_identity_blocks_replacing_unmatched_marker(
        self, mock_create, mock_list_comments, mock_diff
    ) -> None:
        marker = "<!-- ccr-promoted:55:previously_missed:1 -->"
        existing = ReviewCommentInfo(
            201,
            "src/a.py",
            f"body\n\n{marker}",
            "comment-url",
            author_login="github-actions[bot]",
        )
        mock_list_comments.return_value = [existing]
        mock_diff.return_value = "diff --git a/src/a.py b/src/a.py\n+++ b/src/a.py\n@@ -1 +1,2 @@\n+new\n"
        review = ReviewInfo(
            id=55,
            user="Copilot",
            state="COMMENTED",
            body=(
                "<details><summary>Previously missed (1)</summary>\n"
                "### Finding\n**File:** `src/a.py`\n**Line:** 2\nBody\n</details>"
            ),
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        with (
            patch.object(provider, "get_bookkeeping_token_login", return_value=""),
            patch.object(provider, "get_pr_token_login", return_value="legacy-workflow"),
            pytest.raises(RuntimeError, match="bookkeeping.*identity"),
        ):
            provider.promote_ccr_findings(
                pr_number=4,
                commit_sha="head",
                base_sha="base",
                reviews=[review],
            )

        mock_create.assert_not_called()

    @patch.object(GitHubActionsProvider, "get_commit_range_diff")
    @patch.object(GitHubActionsProvider, "list_all_review_comments")
    @patch.object(GitHubActionsProvider, "create_review_thread")
    def test_unresolved_legacy_identity_blocks_replacing_unmatched_marker(
        self, mock_create, mock_list_comments, mock_diff, monkeypatch
    ) -> None:
        marker = "<!-- ccr-promoted:55:previously_missed:1 -->"
        existing = ReviewCommentInfo(
            201,
            "src/a.py",
            f"body\n\n{marker}",
            "comment-url",
            author_login="legacy-workflow",
        )
        mock_list_comments.return_value = [existing]
        mock_diff.return_value = "diff --git a/src/a.py b/src/a.py\n+++ b/src/a.py\n@@ -1 +1,2 @@\n+new\n"
        mock_create.return_value = ReviewCommentInfo(202, "src/a.py", "new", "new-comment-url")
        review = ReviewInfo(
            id=55,
            user="Copilot",
            state="COMMENTED",
            body=(
                "<details><summary>Previously missed (1)</summary>\n"
                "### Finding\n**File:** `src/a.py`\n**Line:** 2\nBody\n</details>"
            ),
        )
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")
        monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "legacy-token")
        provider = GitHubActionsProvider(repo="owner/repo")

        with (
            patch.object(provider, "get_bookkeeping_token_login", return_value="github-actions[bot]"),
            patch.object(provider, "get_pr_token_login", return_value=""),
            pytest.raises(RuntimeError, match="configured.*identity"),
        ):
            provider.promote_ccr_findings(
                pr_number=4,
                commit_sha="head",
                base_sha="base",
                reviews=[review],
            )

        mock_create.assert_not_called()

    @patch.object(GitHubActionsProvider, "get_commit_range_diff")
    @patch.object(GitHubActionsProvider, "list_all_review_comments")
    @patch.object(GitHubActionsProvider, "create_review_thread")
    def test_uncertain_promotion_create_recovers_authenticated_bot_root(
        self, mock_create, mock_list_comments, mock_diff
    ) -> None:
        marker = "<!-- ccr-promoted:55:previously_missed:1 -->"
        recovered = ReviewCommentInfo(
            204,
            "src/a.py",
            f"recovered\n\n{marker}",
            "comment-url",
            author_login="github-actions[bot]",
        )
        mock_list_comments.side_effect = [[], [recovered]]
        mock_create.side_effect = RuntimeError("uncertain create response")
        mock_diff.return_value = "diff --git a/src/a.py b/src/a.py\n+++ b/src/a.py\n@@ -1 +1,2 @@\n+new\n"
        review = ReviewInfo(
            id=55,
            user="Copilot",
            state="COMMENTED",
            body=(
                "<details><summary>Previously missed (1)</summary>\n"
                "### Finding\n**File:** `src/a.py`\n**Line:** 2\nBody\n</details>"
            ),
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        with (
            patch.object(provider, "get_bookkeeping_token_login", return_value="github-actions[bot]"),
            patch.object(provider, "get_pr_token_login", return_value="legacy-workflow"),
        ):
            promoted = provider.promote_ccr_findings(
                pr_number=4,
                commit_sha="head",
                base_sha="base",
                reviews=[review],
            )

        assert [comment.id for comment in promoted] == [204]
        assert promoted[0].source_review_id == 55
        mock_create.assert_called_once()
        mock_list_comments.assert_has_calls([call(4), call(4)])

    def test_required_promotion_fails_closed_without_bookkeeping_token(self, monkeypatch) -> None:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        monkeypatch.delenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", raising=False)
        monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "human-token")
        review = ReviewInfo(
            id=55,
            user="Copilot",
            state="COMMENTED",
            body=(
                "<details><summary>Previously missed (1)</summary>\n"
                "### Finding\n**File:** `src/a.py`\n**Line:** 2\nBody\n</details>"
            ),
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        with (
            patch.object(
                provider,
                "get_commit_range_diff",
                return_value=("diff --git a/src/a.py b/src/a.py\n+++ b/src/a.py\n@@ -1 +1,2 @@\n+new\n"),
            ),
            patch.object(provider, "list_all_review_comments", side_effect=[[], []]),
            patch.object(provider, "get_pr_metadata", return_value=SimpleNamespace(head_sha="head")),
            pytest.raises(RuntimeError, match="AI_PR_LOOP_BOOKKEEPING_TOKEN"),
        ):
            provider.promote_ccr_findings(
                pr_number=4,
                commit_sha="head",
                base_sha="base",
                reviews=[review],
            )

    @patch.object(GitHubActionsProvider, "get_commit_range_diff")
    @patch.object(GitHubActionsProvider, "list_all_review_comments")
    @patch.object(GitHubActionsProvider, "create_review_thread")
    def test_untrusted_author_marker_does_not_prevent_promotion(
        self, mock_create, mock_list_comments, mock_diff
    ) -> None:
        marker = "<!-- ccr-promoted:55:previously_missed:1 -->"
        untrusted = ReviewCommentInfo(202, "src/a.py", marker, "comment-url", author_login="attacker")
        workflow_reply = ReviewCommentInfo(
            203,
            "src/a.py",
            marker,
            "reply-url",
            author_login="workflow[bot]",
            in_reply_to_id=201,
        )
        mock_list_comments.return_value = [untrusted, workflow_reply]
        mock_diff.return_value = "diff --git a/src/a.py b/src/a.py\n+++ b/src/a.py\n@@ -1 +1,2 @@\n+new\n"
        mock_create.return_value = ReviewCommentInfo(203, "src/a.py", marker, "new-comment-url")
        review = ReviewInfo(
            id=55,
            user="Copilot",
            state="COMMENTED",
            body=(
                "<details><summary>Previously missed (1)</summary>\n"
                "### Finding\n**File:** `src/a.py`\n**Line:** 2\nBody\n</details>"
            ),
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        with patch.object(provider, "get_pr_token_login", return_value="workflow[bot]"):
            with patch.object(provider, "get_bookkeeping_token_login", return_value="github-actions[bot]"):
                result = provider.promote_ccr_findings(
                    pr_number=4,
                    commit_sha="head",
                    base_sha="base",
                    reviews=[review],
                )

        assert [comment.id for comment in result] == [203]
        mock_create.assert_called_once()

    @patch.object(GitHubActionsProvider, "get_commit_range_diff")
    @patch.object(GitHubActionsProvider, "list_all_review_comments")
    def test_marker_lookup_fails_closed_when_authenticated_author_is_unknown(
        self, mock_list_comments, mock_diff
    ) -> None:
        marker = "<!-- ccr-promoted:55:previously_missed:1 -->"
        mock_list_comments.return_value = [ReviewCommentInfo(202, "src/a.py", marker, "comment-url")]
        mock_diff.return_value = "diff --git a/src/a.py b/src/a.py\n+++ b/src/a.py\n@@ -1 +1,2 @@\n+new\n"
        review = ReviewInfo(
            id=55,
            user="Copilot",
            state="COMMENTED",
            body=(
                "<details><summary>Previously missed (1)</summary>\n"
                "### Finding\n**File:** `src/a.py`\n**Line:** 2\nBody\n</details>"
            ),
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        with (
            patch.object(provider, "get_pr_token_login", return_value=""),
            pytest.raises(RuntimeError, match="cannot establish the authenticated workflow identity"),
        ):
            provider.promote_ccr_findings(
                pr_number=4,
                commit_sha="head",
                base_sha="base",
                reviews=[review],
            )

    def test_fresh_provider_recovers_promoted_thread_and_replies_for_resolution(self) -> None:
        marker = "<!-- ccr-promoted:55:previously_missed:1 -->"
        promoted_root = ReviewCommentInfo(
            501,
            "src/a.py",
            f"Recovered finding\n\n{marker}\n\n🤖 AI PR Loop ·",
            "root-url",
            source_review_id=900,
            author_login="workflow[bot]",
        )
        reply = ReviewCommentInfo(
            502,
            "src/a.py",
            "Resolution evidence",
            "reply-url",
            source_review_id=900,
            author_login="copilot-swe-agent[bot]",
            in_reply_to_id=501,
        )
        nested_reply = ReviewCommentInfo(
            504,
            "src/a.py",
            "Nested resolution evidence",
            "nested-reply-url",
            source_review_id=900,
            author_login="copilot-swe-agent[bot]",
            in_reply_to_id=502,
        )
        unrelated = ReviewCommentInfo(
            503,
            "src/b.py",
            f"Untrusted\n\n{marker}",
            "unrelated-url",
            source_review_id=900,
            author_login="contributor",
        )
        malformed = ReviewCommentInfo(
            508,
            "src/b.py",
            f"Malformed\n\n{marker}\n\n🤖 AI PR Loop · ",
            "malformed-url",
            source_review_id=900,
            author_login="workflow[bot]",
        )
        orphan = ReviewCommentInfo(
            505,
            "src/b.py",
            "Orphan reply",
            "orphan-url",
            source_review_id=900,
            in_reply_to_id=888,
        )
        cyclic_first = ReviewCommentInfo(506, "src/b.py", "Cycle one", "cycle-1", in_reply_to_id=507)
        cyclic_second = ReviewCommentInfo(507, "src/b.py", "Cycle two", "cycle-2", in_reply_to_id=506)
        provider = GitHubActionsProvider(repo="owner/repo")

        def review_endpoint_response(url: str, *_args: object, **_kwargs: object) -> str:
            if url.endswith("/pulls/4/reviews/55/comments"):
                return "[]"
            if url.endswith("/pulls/4/reviews/55"):
                return json.dumps(
                    {
                        "body": (
                            "<details><summary>Previously missed (1)</summary>\n"
                            "### Finding\n**File:** `src/a.py`\n**Line:** 2\nDetails\n</details>"
                        )
                    }
                )
            raise AssertionError(f"Unexpected GitHub endpoint: {url}")

        with (
            patch.object(provider, "get_pr_token_login", return_value="workflow[bot]"),
            patch.object(
                provider,
                "list_all_review_comments",
                return_value=[
                    promoted_root,
                    reply,
                    nested_reply,
                    unrelated,
                    malformed,
                    orphan,
                    cyclic_first,
                    cyclic_second,
                ],
            ),
            patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=review_endpoint_response),
        ):
            comments = provider.list_review_comments(4, 55)

        assert [(comment.id, comment.source_review_id) for comment in comments] == [(501, 55), (502, 55), (504, 55)]
        assert comments[1].in_reply_to_id == comments[0].id

    def test_fresh_provider_fails_closed_when_workflow_identity_is_unknown(self) -> None:
        marker = "<!-- ccr-promoted:55:previously_missed:1 -->"
        promoted_root = ReviewCommentInfo(501, "src/a.py", marker, "root-url", author_login="workflow[bot]")
        provider = GitHubActionsProvider(repo="owner/repo")

        def review_endpoint_response(url: str, *_args: object, **_kwargs: object) -> str:
            if url.endswith("/pulls/4/reviews/55/comments"):
                return "[]"
            if url.endswith("/pulls/4/reviews/55"):
                return json.dumps(
                    {
                        "body": (
                            "<details><summary>Previously missed (1)</summary>\n"
                            "### Finding\n**File:** `src/a.py`\n**Line:** 2\nDetails\n</details>"
                        )
                    }
                )
            raise AssertionError(f"Unexpected GitHub endpoint: {url}")

        with (
            patch.object(provider, "get_pr_token_login", return_value=""),
            patch.object(provider, "list_all_review_comments", return_value=[promoted_root]),
            patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=review_endpoint_response),
            pytest.raises(RuntimeError, match="cannot establish the authenticated workflow identity"),
        ):
            provider.list_review_comments(4, 55)

    @pytest.mark.parametrize(
        ("bookkeeping_login", "legacy_login", "author_login"),
        [
            ("github-actions[bot]", "", "legacy-workflow"),
            ("", "legacy-workflow", "github-actions[bot]"),
        ],
    )
    def test_fresh_provider_fails_closed_when_configured_identity_is_unresolved(
        self, bookkeeping_login, legacy_login, author_login, monkeypatch
    ) -> None:
        marker = "<!-- ccr-promoted:55:previously_missed:1 -->"
        promoted_root = ReviewCommentInfo(
            501,
            "src/a.py",
            marker,
            "root-url",
            author_login=author_login,
        )
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")
        monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "legacy-token")
        provider = GitHubActionsProvider(repo="owner/repo")

        def review_endpoint_response(url: str, *_args: object, **_kwargs: object) -> str:
            if url.endswith("/pulls/4/reviews/55/comments"):
                return "[]"
            if url.endswith("/pulls/4/reviews/55"):
                return json.dumps(
                    {
                        "body": (
                            "<details><summary>Previously missed (1)</summary>\n"
                            "### Finding\n**File:** `src/a.py`\n**Line:** 2\nDetails\n</details>"
                        )
                    }
                )
            raise AssertionError(f"Unexpected GitHub endpoint: {url}")

        with (
            patch.object(provider, "get_bookkeeping_token_login", return_value=bookkeeping_login),
            patch.object(provider, "get_pr_token_login", return_value=legacy_login),
            patch.object(provider, "list_all_review_comments", return_value=[promoted_root]),
            patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=review_endpoint_response),
            pytest.raises(RuntimeError, match="configured.*identity"),
        ):
            provider.list_review_comments(4, 55)

    @pytest.mark.parametrize(
        ("bookkeeping_token", "author_login", "expected_ids"),
        [
            (None, "github-actions[bot]", None),
            ("bot-token", "untrusted", []),
            ("bot-token", "github-actions[bot]", [501]),
        ],
    )
    def test_marker_inventory_requires_bookkeeping_identity_for_unmatched_roots(
        self, monkeypatch, bookkeeping_token, author_login, expected_ids
    ) -> None:
        """An unmatched root requires a bookkeeping identity; verified roots remain recoverable."""
        marker = "<!-- ccr-promoted:55:previously_missed:1 -->"
        promoted_root = ReviewCommentInfo(
            501,
            "src/a.py",
            marker,
            "root-url",
            author_login=author_login,
        )
        if bookkeeping_token is None:
            monkeypatch.delenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", raising=False)
        else:
            monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", bookkeeping_token)
        monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "legacy-token")
        provider = GitHubActionsProvider(repo="owner/repo")

        def review_endpoint_response(url: str, *_args: object, **_kwargs: object) -> str:
            if url.endswith("/pulls/4/reviews/55/comments"):
                return "[]"
            if url.endswith("/pulls/4/reviews/55"):
                return json.dumps(
                    {
                        "body": (
                            "<details><summary>Previously missed (1)</summary>\n"
                            "### Finding\n**File:** `src/a.py`\n**Line:** 2\nDetails\n</details>"
                        )
                    }
                )
            raise AssertionError(f"Unexpected GitHub endpoint: {url}")

        with (
            patch.object(
                provider,
                "get_bookkeeping_token_login",
                return_value="github-actions[bot]" if bookkeeping_token else "",
            ),
            patch.object(provider, "get_pr_token_login", return_value="legacy-workflow"),
            patch.object(provider, "list_all_review_comments", return_value=[promoted_root]),
            patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=review_endpoint_response),
        ):
            if expected_ids is None:
                with pytest.raises(RuntimeError, match="bookkeeping identity"):
                    provider.list_review_comments(4, 55)
            else:
                assert [comment.id for comment in provider.list_review_comments(4, 55)] == expected_ids

    @patch.object(GitHubActionsProvider, "get_commit_range_diff")
    @patch.object(GitHubActionsProvider, "list_all_review_comments")
    @patch.object(GitHubActionsProvider, "create_review_thread")
    def test_missing_source_line_fallback_discloses_path_without_inventing_line(
        self, mock_create, mock_list_comments, mock_diff
    ) -> None:
        mock_diff.return_value = "diff --git a/src/a.py b/src/a.py\n+++ b/src/a.py\n@@ -1 +1,2 @@\n+new\n"
        mock_list_comments.return_value = []
        mock_create.return_value = ReviewCommentInfo(302, "src/a.py", "body", "url")
        review = ReviewInfo(
            78,
            "Copilot",
            "COMMENTED",
            body=(
                "<details><summary>Previously missed (1)</summary>\n"
                "### Finding\n**File:** `src/a.py`\nDetails\n</details>"
            ),
        )

        GitHubActionsProvider(repo="owner/repo").promote_ccr_findings(
            pr_number=4,
            commit_sha="head",
            base_sha="base",
            reviews=[review],
        )

        posted_body = mock_create.call_args.kwargs["body"]
        assert "Original CCR source location: `src/a.py`." in posted_body
        assert "proper source line could not be determined for the current diff" in posted_body

    def test_only_resolved_findings_skip_diff_and_cache_recovery(self, caplog) -> None:
        caplog.set_level("INFO")
        provider = GitHubActionsProvider(repo="owner/repo")
        review = ReviewInfo(
            55,
            "Copilot",
            "COMMENTED",
            body=(
                "<details><summary>Previously missed (1)</summary>\n"
                "### Finding\n**File:** `src/a.py`\nResolved since previous review.\n</details>"
            ),
        )

        assert (
            provider.promote_ccr_findings(
                pr_number=4,
                commit_sha="head",
                base_sha="base",
                reviews=[review],
            )
            == []
        )
        provider._cache_ccr_promoted_comments({})

        assert provider._ccr_promoted_comments == {55: []}
        assert "skipping explicitly resolved CCR occurrence 55:previously_missed:1" in caplog.text

    @pytest.mark.parametrize(
        ("reviews", "commit_sha", "base_sha", "repo"),
        [
            ([ReviewInfo(1, "human", "COMMENTED", body="")], "", "", "owner/repo"),
            (
                [
                    ReviewInfo(
                        1,
                        "Copilot",
                        "COMMENTED",
                        body="<details><summary>Previously missed (0)</summary></details>",
                    )
                ],
                "",
                "",
                "owner/repo",
            ),
        ],
    )
    def test_skips_reviews_without_outstanding_findings(self, reviews, commit_sha, base_sha, repo) -> None:
        provider = GitHubActionsProvider(repo=repo)

        assert (
            provider.promote_ccr_findings(
                pr_number=4,
                commit_sha=commit_sha,
                base_sha=base_sha,
                reviews=reviews,
            )
            == []
        )


class TestGitHubActionsProviderIsCodeqlConfigured:
    @pytest.mark.parametrize(
        "rules,expected",
        [
            ([], False),
            ([{"type": "branch_name_pattern", "parameters": {}}], False),
            ([{"type": "code_scanning", "parameters": {"code_scanning_tools": [{"tool": "Other"}]}}], False),
            (
                [
                    {
                        "type": "code_scanning",
                        "parameters": {"code_scanning_tools": [{"tool": "Other"}, {"tool": "CodeQL"}]},
                    }
                ],
                True,
            ),
        ],
    )
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_detects_effective_branch_rules(self, api, rules, expected, monkeypatch):
        monkeypatch.delenv("AI_PR_LOOP_EXPECT_CODEQL", raising=False)
        api.side_effect = [json.dumps({"state": "not-configured"}), json.dumps(rules)]
        provider = GitHubActionsProvider(repo="owner/repo")
        assert provider.is_codeql_configured(base_branch="release/1") is expected
        assert provider.is_codeql_configured(base_branch="release/1") is expected
        assert [c.args[0] for c in api.call_args_list] == [
            "/repos/owner/repo/code-scanning/default-setup",
            "/repos/owner/repo/rules/branches/release%2F1",
        ]
        assert api.call_args_list[1].kwargs == {"paginate": True, "token": None}

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_default_setup_configured_is_cached(self, api, monkeypatch):
        monkeypatch.delenv("AI_PR_LOOP_EXPECT_CODEQL", raising=False)
        api.return_value = json.dumps({"state": "configured"})
        provider = GitHubActionsProvider(repo="owner/repo")
        assert provider.is_codeql_configured(base_branch="main") is True
        assert provider.is_codeql_configured(base_branch="main") is True
        api.assert_called_once_with("/repos/owner/repo/code-scanning/default-setup", token=None)

    @pytest.mark.parametrize("response", ["null", "[]", "{}", '{"state":"unexpected"}', '{"state":[]}', "invalid-json"])
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_malformed_default_setup_fails_closed_uncached(self, api, response, monkeypatch):
        monkeypatch.delenv("AI_PR_LOOP_EXPECT_CODEQL", raising=False)
        api.return_value = response
        provider = GitHubActionsProvider(repo="owner/repo")
        assert provider.is_codeql_configured(base_branch="main") is True
        assert provider.is_codeql_configured(base_branch="main") is True
        assert api.call_count == 2
        assert not provider._codeql_configured_cache

    @pytest.mark.parametrize("status", [403, 404])
    @pytest.mark.parametrize(
        "rules,expected",
        [([], False), ([{"type": "code_scanning", "parameters": {"code_scanning_tools": [{"tool": "CodeQL"}]}}], True)],
    )
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_unavailable_default_setup_falls_through_to_branch_rules(self, api, status, rules, expected, monkeypatch):
        monkeypatch.delenv("AI_PR_LOOP_EXPECT_CODEQL", raising=False)
        api.side_effect = [
            RuntimeError(f"GitHub API error: Code Security must be enabled (HTTP {status})"),
            json.dumps(rules),
        ]
        assert GitHubActionsProvider(repo="owner/repo").is_codeql_configured(base_branch="main") is expected
        assert api.call_count == 2

    @pytest.mark.parametrize(
        "rules",
        [
            None,
            {},
            [None],
            ["invalid"],
            [{"type": "code_scanning", "parameters": None}],
            [{"type": "code_scanning", "parameters": []}],
            [{"type": "code_scanning"}],
            [{"type": "code_scanning", "parameters": {}}],
            [{"type": "code_scanning", "parameters": {"code_scanning_tools": "invalid"}}],
            [{"type": "code_scanning", "parameters": {"code_scanning_tools": [None]}}],
            [{"type": "code_scanning", "parameters": {"code_scanning_tools": [{}]}}],
        ],
    )
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_malformed_effective_rules_fail_closed_uncached(self, api, rules, monkeypatch):
        monkeypatch.delenv("AI_PR_LOOP_EXPECT_CODEQL", raising=False)
        api.side_effect = [json.dumps({"state": "not-configured"}), json.dumps(rules)] * 2
        provider = GitHubActionsProvider(repo="owner/repo")
        assert provider.is_codeql_configured(base_branch="main") is True
        assert provider.is_codeql_configured(base_branch="main") is True
        assert api.call_count == 4
        assert not provider._codeql_configured_cache

    @pytest.mark.parametrize("error", [RuntimeError("HTTP 500"), RuntimeError("API unavailable")])
    @pytest.mark.parametrize("at_rules", [False, True])
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_detection_errors_fail_closed_uncached(self, api, error, at_rules, monkeypatch):
        monkeypatch.delenv("AI_PR_LOOP_EXPECT_CODEQL", raising=False)
        api.side_effect = [json.dumps({"state": "not-configured"}), error] if at_rules else error
        provider = GitHubActionsProvider(repo="owner/repo")
        assert provider.is_codeql_configured(base_branch="main") is True
        assert not provider._codeql_configured_cache

    @pytest.mark.parametrize("at_rules", [False, True])
    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_rate_limit_propagates(self, api, _mock_sleep, at_rules, monkeypatch):
        """``_gh_api``'s real ``RetryableError`` must survive retries as ``ProviderRateLimitError``.

        ``_gh_api`` never raises ``ProviderRateLimitError`` itself (only the
        ``@retry_with_backoff`` decorator does, once retries are exhausted), so
        the mock here raises the actual exception type to exercise that path.
        """
        monkeypatch.delenv("AI_PR_LOOP_EXPECT_CODEQL", raising=False)
        error = RetryableError("GitHub API rate limited (HTTP 429)", retry_after=1, is_rate_limit=True)
        api.side_effect = (
            itertools.cycle([json.dumps({"state": "not-configured"}), error]) if at_rules else itertools.repeat(error)
        )
        with pytest.raises(ProviderRateLimitError):
            GitHubActionsProvider(repo="owner/repo").is_codeql_configured(base_branch="main")

    @pytest.mark.parametrize("at_rules", [False, True])
    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_transient_server_error_retries_then_propagates(self, api, _mock_sleep, at_rules, monkeypatch):
        """A transient (non-rate-limit) ``RetryableError`` from ``_gh_api`` must not be swallowed."""
        monkeypatch.delenv("AI_PR_LOOP_EXPECT_CODEQL", raising=False)
        error = RetryableError("GitHub API server error (HTTP 503)", is_rate_limit=False)
        api.side_effect = (
            itertools.cycle([json.dumps({"state": "not-configured"}), error]) if at_rules else itertools.repeat(error)
        )
        with pytest.raises(RetryableError):
            GitHubActionsProvider(repo="owner/repo").is_codeql_configured(base_branch="main")

    @pytest.mark.parametrize("override,expected", [(" TRUE ", True), ("1", True), ("false", False), ("0", False)])
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_override_precedes_detection(self, api, override, expected, monkeypatch):
        monkeypatch.setenv("AI_PR_LOOP_EXPECT_CODEQL", override)
        assert GitHubActionsProvider(repo="owner/repo").is_codeql_configured(base_branch="main") is expected
        api.assert_not_called()

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_missing_branch_fails_closed_uncached(self, api, monkeypatch):
        monkeypatch.delenv("AI_PR_LOOP_EXPECT_CODEQL", raising=False)
        api.return_value = json.dumps({"state": "not-configured"})
        provider = GitHubActionsProvider(repo="owner/repo")
        assert provider.is_codeql_configured() is True
        assert not provider._codeql_configured_cache

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_cache_scoped_to_effective_repository_and_branch(self, api, monkeypatch):
        monkeypatch.setenv("AI_PR_LOOP_EXPECT_CODEQL", "unknown")
        api.side_effect = [
            json.dumps({"state": "not-configured"}),
            "[]",
            json.dumps({"state": "configured"}),
            json.dumps({"state": "not-configured"}),
            "[]",
        ]
        provider = GitHubActionsProvider(repo="owner/repo")
        assert provider.is_codeql_configured(base_branch="main") is False
        assert provider.is_codeql_configured(base_branch="release") is True
        assert provider.is_codeql_configured(repo="other/project", base_branch="main") is False
        assert provider.is_codeql_configured(repo="owner/repo", base_branch="main") is False
        assert provider.is_codeql_configured(base_branch="release") is True
        assert api.call_count == 5
        assert api.call_args_list[3].args[0] == "/repos/other/project/code-scanning/default-setup"

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_environment_repository_changes_do_not_reuse_cache(self, api, monkeypatch):
        monkeypatch.delenv("AI_PR_LOOP_EXPECT_CODEQL", raising=False)
        monkeypatch.setenv("GITHUB_REPOSITORY", "owner/first")
        api.side_effect = [json.dumps({"state": "not-configured"}), "[]"] * 2
        provider = GitHubActionsProvider()
        assert provider.is_codeql_configured(base_branch="main") is False
        monkeypatch.setenv("GITHUB_REPOSITORY", "owner/second")
        assert provider.is_codeql_configured(base_branch="main") is False
        assert api.call_args_list[2].args[0] == "/repos/owner/second/code-scanning/default-setup"
