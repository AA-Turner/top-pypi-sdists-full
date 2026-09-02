"""Tests for assign_issue_to_agent()."""

from __future__ import annotations

import json
import logging
from typing import cast
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.agent_assignment import (
    _build_assignment_instructions,
    _event_id,
    _extract_retryable_failure_message,
    _gh_api_call,
    _is_bad_credentials_error,
    _is_copilot_assigned,
    _parse_clamped_env_int,
    _resolve_copilot_actor_id,
    _validate_assignment_token,
    _validate_repo_format,
    _wait_for_started_session_event,
    assign_issue_to_agent,
)
from agentic_devtools.cli.ci.exceptions import AgentAssignmentError, ProviderRateLimitError
from agentic_devtools.cli.ci.retry import RetryableError


def _suggested_actors_response(*, include_copilot: bool = True) -> str:
    nodes = [{"id": "BOT_copilot", "login": "copilot-swe-agent"}] if include_copilot else []
    return json.dumps({"data": {"repository": {"suggestedActors": {"nodes": nodes}}}})


@patch("agentic_devtools.cli.ci.retry.time.sleep", return_value=None)
class TestAssignIssueToAgent:
    """Tests for shared coding-agent assignment orchestration."""

    def test_returns_failed_result_when_no_token_available(self, _mock_sleep: MagicMock) -> None:
        with patch.dict("os.environ", {}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="test",
            )

        assert result.success is False
        assert result.token_identity == ""
        assert "SPECKIT_PR_TOKEN" in result.error
        assert "COPILOT_GITHUB_TOKEN" in result.error

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_returns_actionable_failure_when_token_preflight_is_401(self, mock_gh_api, _mock_sleep: MagicMock) -> None:
        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                raise RuntimeError("GitHub API error: gh: Bad credentials (HTTP 401)")
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
            )

        assert result.success is False
        assert result.attempts == 0
        assert result.token_identity == "SPECKIT_PR_TOKEN"
        assert "failed authentication (HTTP 401 Bad credentials)" in result.error
        assert "Rotate the secret and retry" in result.error

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_returns_failure_when_token_preflight_raises_non_401(self, mock_gh_api, _mock_sleep: MagicMock) -> None:
        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                raise RuntimeError("GitHub API error: gh: denied (HTTP 403)")
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
            )

        assert result.success is False
        assert result.attempts == 0
        assert "Assignment token preflight failed for 'SPECKIT_PR_TOKEN'" in result.error

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_raises_provider_rate_limit_when_token_preflight_raises_retryable_error(
        self, mock_gh_api, _mock_sleep: MagicMock
    ) -> None:
        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                raise RetryableError("rate limited (HTTP 429)", retry_after=5.0, is_rate_limit=True)
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            with pytest.raises(ProviderRateLimitError):
                assign_issue_to_agent(
                    repo="owner/repo",
                    issue_number=42,
                    problem_statement="run task",
                    max_attempts_per_method=3,
                )

        # /user is called once per attempt (initial + 2 retries = 3 total)
        assert mock_gh_api.call_count == 3

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_returns_clear_failure_when_copilot_not_in_suggested_actors(
        self,
        mock_gh_api,
        _mock_sleep: MagicMock,
    ) -> None:
        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint.endswith("/issues/42") and method == "GET":
                return json.dumps({"number": 42, "assignees": []})
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response(include_copilot=False)
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
            )

        assert result.success is False
        assert result.attempts == 0
        assert "Copilot coding agent is not enabled for owner/repo" in result.error
        assert "suggestedActors did not include copilot-swe-agent" in result.error

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_falls_back_when_copilot_verification_api_errors(
        self,
        mock_gh_api,
        _mock_sleep: MagicMock,
    ) -> None:
        event_reads: dict[str, int] = {"count": 0}

        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint.endswith("/issues/42") and method == "GET":
                return json.dumps({"number": 42, "assignees": []})
            if endpoint == "/graphql" and method == "POST":
                raise RuntimeError("GraphQL unavailable")
            if endpoint.endswith("/issues/42/events") and method == "GET":
                event_reads["count"] += 1
                if event_reads["count"] >= 2:
                    return json.dumps([{"id": 10, "url": "https://example/events/10", "event": "copilot_work_started"}])
                return json.dumps([])
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                return json.dumps({"number": 42, "assignees": [{"login": "copilot-swe-agent[bot]"}]})
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
            )

        assert result.success is True
        assert result.method == "agent_assignment"
        assert result.outcome == "confirmed_success"
        assert result.session_confirmed is True
        assert not any("/copilot/coding-agent/tasks" in call.args[0] for call in mock_gh_api.call_args_list)

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_falls_back_when_copilot_verification_response_shape_is_invalid(
        self,
        mock_gh_api,
        _mock_sleep: MagicMock,
    ) -> None:
        event_reads: dict[str, int] = {"count": 0}

        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint.endswith("/issues/42") and method == "GET":
                return json.dumps({"number": 42, "assignees": []})
            if endpoint == "/graphql" and method == "POST":
                return json.dumps({"data": {"repository": None}})
            if endpoint.endswith("/issues/42/events") and method == "GET":
                event_reads["count"] += 1
                if event_reads["count"] >= 2:
                    return json.dumps([{"id": 11, "url": "https://example/events/11", "event": "copilot_work_started"}])
                return json.dumps([])
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                return json.dumps({"number": 42, "assignees": [{"login": "copilot-swe-agent[bot]"}]})
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
            )

        assert result.success is True
        assert result.method == "agent_assignment"
        assert result.outcome == "confirmed_success"
        assert result.session_confirmed is True
        assert not any("/copilot/coding-agent/tasks" in call.args[0] for call in mock_gh_api.call_args_list)

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_falls_back_when_copilot_verification_raises_retryable_error(
        self,
        mock_gh_api,
        _mock_sleep: MagicMock,
    ) -> None:
        event_reads: dict[str, int] = {"count": 0}

        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint.endswith("/issues/42") and method == "GET":
                return json.dumps({"number": 42, "assignees": []})
            if endpoint == "/graphql" and method == "POST":
                raise RetryableError("GraphQL rate limited (HTTP 429)")
            if endpoint.endswith("/issues/42/events") and method == "GET":
                event_reads["count"] += 1
                if event_reads["count"] >= 2:
                    return json.dumps([{"id": 12, "url": "https://example/events/12", "event": "copilot_work_started"}])
                return json.dumps([])
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                return json.dumps({"number": 42, "assignees": [{"login": "copilot-swe-agent[bot]"}]})
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
                max_attempts_per_method=3,
            )

        assert result.success is True
        assert result.method == "agent_assignment"
        assert result.outcome == "confirmed_success"
        assert result.session_confirmed is True
        # /graphql is called once per attempt (initial + 2 retries = 3 total)
        graphql_calls = [c for c in mock_gh_api.call_args_list if c.args[0] == "/graphql"]
        assert len(graphql_calls) == 3
        assert not any("/copilot/coding-agent/tasks" in call.args[0] for call in mock_gh_api.call_args_list)

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_raises_provider_rate_limit_when_copilot_verification_raises_rate_limit(
        self,
        mock_gh_api,
        _mock_sleep: MagicMock,
    ) -> None:
        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint.endswith("/issues/42") and method == "GET":
                return json.dumps({"number": 42, "assignees": []})
            if endpoint == "/graphql" and method == "POST":
                raise RetryableError("GraphQL rate limited (HTTP 429)", retry_after=5.0, is_rate_limit=True)
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            with pytest.raises(ProviderRateLimitError):
                assign_issue_to_agent(
                    repo="owner/repo",
                    issue_number=42,
                    problem_statement="run task",
                    max_attempts_per_method=3,
                )

        graphql_calls = [c for c in mock_gh_api.call_args_list if c.args[0] == "/graphql"]
        assert len(graphql_calls) == 3
        assert not any("/copilot/coding-agent/tasks" in call.args[0] for call in mock_gh_api.call_args_list)

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_raises_provider_rate_limit_when_copilot_verification_graphql_errors_are_rate_limited(
        self,
        mock_gh_api,
        _mock_sleep: MagicMock,
    ) -> None:
        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint == "/graphql" and method == "POST":
                metadata = kwargs.get("response_metadata", {})
                if isinstance(metadata, dict):
                    cast("dict[str, float | int | None]", metadata).update(retry_after=5.0, remaining=0)
                return json.dumps({"errors": [{"type": "RATE_LIMITED", "message": "API rate limit exceeded"}]})
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            with pytest.raises(ProviderRateLimitError):
                assign_issue_to_agent(
                    repo="owner/repo",
                    issue_number=42,
                    problem_statement="run task",
                    max_attempts_per_method=3,
                )

        graphql_calls = [c for c in mock_gh_api.call_args_list if c.args[0] == "/graphql"]
        assert len(graphql_calls) == 3

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_prefers_primary_token_and_succeeds_via_task_endpoint(
        self,
        mock_gh_api,
        _mock_sleep: MagicMock,
    ) -> None:
        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint.endswith("/issues/42") and method == "GET":
                return json.dumps({"number": 42, "assignees": []})
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/copilot/coding-agent/tasks") and method == "POST":
                return json.dumps({"id": "task-123", "url": "https://example/task-123"})
            if "/copilot/coding-agent/tasks/task-123" in endpoint and method == "GET":
                return json.dumps({"status": "in_progress"})
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect

        with patch.dict(
            "os.environ",
            {
                "SPECKIT_PR_TOKEN": "primary-token",
                "COPILOT_GITHUB_TOKEN": "fallback-token",
            },
            clear=True,
        ):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
            )

        assert result.success is True
        assert result.method == "coding_agent_task"
        assert result.task_id == "task-123"
        assert result.task_url == "https://example/task-123"
        assert result.token_identity == "SPECKIT_PR_TOKEN"
        assert result.attempts == 1
        # The GET poll also uses the versioned API header
        last_call_headers = mock_gh_api.call_args.kwargs["headers"]
        assert last_call_headers["X-GitHub-Api-Version"] == "2022-11-28"

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_preexisting_assignment_returns_before_actor_lookup(self, mock_gh_api, _mock_sleep: MagicMock) -> None:
        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint.endswith("/issues/42") and method == "GET":
                return json.dumps({"number": 42, "assignees": [{"login": "copilot-swe-agent[bot]"}]})
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
            )

        assert result.success is True
        assert result.outcome == "confirmed_success"
        assert result.attempts == 0
        assert not any(call.args[0] == "/graphql" for call in mock_gh_api.call_args_list)

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_raises_provider_rate_limit_when_primary_task_method_is_exhausted(
        self,
        mock_gh_api,
        _mock_sleep: MagicMock,
    ) -> None:
        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint.endswith("/issues/42") and method == "GET":
                return json.dumps({"number": 42, "assignees": []})
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/copilot/coding-agent/tasks") and method == "POST":
                raise ProviderRateLimitError(provider="github", credential_identity="SPECKIT_PR_TOKEN")
            if endpoint.endswith("/issues/42/assignees"):
                raise AssertionError("fallback assignment must not run after provider rate limit exhaustion")
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect

        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "primary-token"}, clear=True):
            with pytest.raises(ProviderRateLimitError):
                assign_issue_to_agent(
                    repo="owner/repo",
                    issue_number=42,
                    problem_statement="run task",
                )

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_preexisting_assignment_is_not_terminal_when_disabled(self, mock_gh_api, _mock_sleep: MagicMock) -> None:
        event_reads: dict[str, int] = {"count": 0}

        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/issues/42") and method == "GET":
                return json.dumps({"number": 42, "assignees": [{"login": "copilot-swe-agent[bot]"}]})
            if endpoint.endswith("/issues/42/events") and method == "GET":
                event_reads["count"] += 1
                if event_reads["count"] >= 2:
                    return json.dumps([{"id": 17, "url": "https://example/events/17", "event": "copilot_work_started"}])
                return json.dumps([])
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                return json.dumps({"number": 42, "assignees": [{"login": "copilot-swe-agent[bot]"}]})
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
                custom_agent="speckit.clarify",
                allow_preexisting_assignment=False,
            )

        assert result.success is True
        assert result.method == "agent_assignment"
        assert result.outcome == "confirmed_success"
        assert result.session_confirmed is True
        assert any(call.args[0].endswith("/issues/42/assignees") for call in mock_gh_api.call_args_list)

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_custom_agent_bypasses_primary_and_succeeds_via_fallback(
        self,
        mock_gh_api,
        _mock_sleep: MagicMock,
    ) -> None:
        """When custom_agent is provided, the primary tasks endpoint must be skipped."""
        event_reads: dict[str, int] = {"count": 0}
        event_url = "https://api.github.com/repos/owner/repo/issues/events/10"

        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint.endswith("/issues/42") and method == "GET":
                return json.dumps({"number": 42, "assignees": []})
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if "/copilot/coding-agent/tasks" in endpoint:
                raise AssertionError("primary tasks endpoint must NOT be called when custom_agent is set")
            if endpoint.endswith("/issues/42/events") and method == "GET":
                event_reads["count"] += 1
                if event_reads["count"] >= 2:
                    return json.dumps([{"id": 10, "url": event_url, "event": "copilot_work_started"}])
                return json.dumps([])
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                return json.dumps({"number": 42, "assignees": [{"login": "copilot-swe-agent[bot]"}]})
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect

        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token-value"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
                custom_instructions="instr",
                custom_agent="speckit.implement",
                max_attempts_per_method=2,
            )

        assert result.success is True
        assert result.method == "agent_assignment"
        assert result.task_id == "10"
        assert result.task_url == event_url
        assert result.session_confirmed is True
        assert result.attempts == 1

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_raises_provider_rate_limit_when_fallback_assignment_is_exhausted(
        self,
        mock_gh_api,
        _mock_sleep: MagicMock,
    ) -> None:
        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint.endswith("/issues/42") and method == "GET":
                return json.dumps({"number": 42, "assignees": []})
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/issues/42/events") and method == "GET":
                return json.dumps([])
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                raise ProviderRateLimitError(provider="github", credential_identity="SPECKIT_PR_TOKEN")
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect

        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token-value"}, clear=True):
            with pytest.raises(ProviderRateLimitError):
                assign_issue_to_agent(
                    repo="owner/repo",
                    issue_number=42,
                    problem_statement="run task",
                    custom_instructions="instr",
                    custom_agent="speckit.implement",
                )

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_model_only_bypasses_primary_and_succeeds_via_fallback(
        self,
        mock_gh_api,
        _mock_sleep: MagicMock,
    ) -> None:
        """When only model is provided, the primary tasks endpoint must be skipped."""
        event_reads: dict[str, int] = {"count": 0}
        event_url = "https://api.github.com/repos/owner/repo/issues/events/20"

        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if "/copilot/coding-agent/tasks" in endpoint:
                raise AssertionError("primary tasks endpoint must NOT be called when model is set")
            if endpoint.endswith("/issues/42/events") and method == "GET":
                event_reads["count"] += 1
                if event_reads["count"] >= 2:
                    return json.dumps([{"id": 20, "url": event_url, "event": "copilot_work_started"}])
                return json.dumps([])
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                return json.dumps({"number": 42, "assignees": [{"login": "copilot-swe-agent[bot]"}]})
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect

        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token-value"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
                model="claude-opus-4.6",
                max_attempts_per_method=2,
            )

        assert result.success is True
        assert result.method == "agent_assignment"
        assert result.task_id == "20"
        assert result.task_url == event_url
        assert result.session_confirmed is True
        assert result.attempts == 1

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_fallback_uses_highest_started_event_id_for_task_metadata(
        self,
        mock_gh_api,
        _mock_sleep: MagicMock,
    ) -> None:
        """Fallback should select the newest started event deterministically."""
        event_reads: dict[str, int] = {"count": 0}
        newer_event_url = "https://api.github.com/repos/owner/repo/issues/events/20"
        older_event_url = "https://api.github.com/repos/owner/repo/issues/events/10"

        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/issues/42/events") and method == "GET":
                event_reads["count"] += 1
                if event_reads["count"] >= 2:
                    return json.dumps(
                        [
                            {"id": 20, "url": newer_event_url, "event": "copilot_work_started"},
                            {"id": 10, "url": older_event_url, "event": "copilot_work_started"},
                        ],
                    )
                return json.dumps([])
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                return json.dumps({"number": 42, "assignees": [{"login": "copilot-swe-agent[bot]"}]})
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect

        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token-value"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
                custom_instructions="instr",
                max_attempts_per_method=2,
            )

        assert result.success is True
        assert result.method == "agent_assignment"
        assert result.task_id == "20"
        assert result.task_url == newer_event_url
        assert result.session_confirmed is True
        assert result.attempts == 1

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_fallback_success_reports_total_attempts_across_methods(
        self,
        mock_gh_api,
        _mock_sleep: MagicMock,
    ) -> None:
        event_reads: dict[str, int] = {"count": 0}
        event_url = "https://api.github.com/repos/owner/repo/issues/events/30"

        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint.endswith("/issues/42") and method == "GET":
                return json.dumps({"number": 42, "assignees": []})
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/copilot/coding-agent/tasks") and method == "POST":
                return "{}"
            if endpoint.endswith("/issues/42/events") and method == "GET":
                event_reads["count"] += 1
                if event_reads["count"] >= 2:
                    return json.dumps([{"id": 30, "url": event_url, "event": "copilot_work_started"}])
                return json.dumps([])
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                return json.dumps({"number": 42, "assignees": [{"login": "copilot-swe-agent[bot]"}]})
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect

        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token-value"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
                max_attempts_per_method=1,
            )

        assert result.success is True
        assert result.method == "agent_assignment"
        assert result.task_id == "30"
        assert result.task_url == event_url
        assert result.session_confirmed is True
        assert result.attempts == 2

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_returns_success_when_assignment_confirmed_but_session_not_started(
        self,
        mock_gh_api,
        _mock_sleep: MagicMock,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        clock = {"now": 0.0}
        _mock_sleep.side_effect = lambda seconds: clock.__setitem__("now", clock["now"] + seconds)
        event_reads = {"count": 0}

        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/copilot/coding-agent/tasks") and method == "POST":
                return "{}"
            if endpoint.endswith("/issues/42/events") and method == "GET":
                event_reads["count"] += 1
                return json.dumps([])
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                return json.dumps({"number": 42, "assignees": [{"login": "copilot-swe-agent[bot]"}]})
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect

        with (
            caplog.at_level(logging.WARNING, logger="agentic_devtools.cli.ci.agent_assignment"),
            patch("agentic_devtools.cli.ci.retry.time.monotonic", side_effect=lambda: clock["now"]),
            patch.dict("os.environ", {"COPILOT_GITHUB_TOKEN": "fallback-token"}, clear=True),
        ):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
                custom_instructions="instr",
                max_attempts_per_method=2,
            )

        assert result.success is True
        assert result.method == "agent_assignment"
        assert result.session_confirmed is False
        assert result.token_identity == "COPILOT_GITHUB_TOKEN"
        assert result.error == ""
        assert [call.args[0] for call in _mock_sleep.call_args_list[-5:]] == [15.0, 30.0, 60.0, 120.0, 75.0]
        assert event_reads["count"] == 6
        assert "session_confirmed=False" in caplog.text
        assert "poll_timeout_seconds=300" in caplog.text
        assert "rate limit" not in caplog.text.lower()

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_respects_env_override_for_session_poll_schedule(
        self,
        mock_gh_api,
        _mock_sleep: MagicMock,
    ) -> None:
        clock = {"now": 0.0}
        _mock_sleep.side_effect = lambda seconds: clock.__setitem__("now", clock["now"] + seconds)

        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/copilot/coding-agent/tasks") and method == "POST":
                return "{}"
            if endpoint.endswith("/issues/42/events") and method == "GET":
                return json.dumps([])
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                return json.dumps({"number": 42, "assignees": [{"login": "copilot-swe-agent[bot]"}]})
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect

        with (
            patch("agentic_devtools.cli.ci.retry.time.monotonic", side_effect=lambda: clock["now"]),
            patch.dict(
                "os.environ",
                {
                    "COPILOT_GITHUB_TOKEN": "fallback-token",
                    "AGDT_AGENT_START_POLL_INITIAL_SECONDS": "10",
                    "AGDT_AGENT_START_POLL_TIMEOUT_SECONDS": "100",
                },
                clear=True,
            ),
        ):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
                custom_instructions="instr",
                max_attempts_per_method=2,
            )

        assert result.success is True
        assert result.session_confirmed is False
        assert [call.args[0] for call in _mock_sleep.call_args_list[-4:]] == [10.0, 20.0, 40.0, 30.0]

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_performs_single_deadline_check_when_initial_equals_timeout(
        self,
        mock_gh_api,
        _mock_sleep: MagicMock,
    ) -> None:
        clock = {"now": 0.0}
        _mock_sleep.side_effect = lambda seconds: clock.__setitem__("now", clock["now"] + seconds)

        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/copilot/coding-agent/tasks") and method == "POST":
                return "{}"
            if endpoint.endswith("/issues/42/events") and method == "GET":
                return json.dumps([])
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                return json.dumps({"number": 42, "assignees": [{"login": "copilot-swe-agent[bot]"}]})
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect

        with (
            patch("agentic_devtools.cli.ci.retry.time.monotonic", side_effect=lambda: clock["now"]),
            patch.dict(
                "os.environ",
                {
                    "COPILOT_GITHUB_TOKEN": "fallback-token",
                    "AGDT_AGENT_START_POLL_INITIAL_SECONDS": "60",
                    "AGDT_AGENT_START_POLL_TIMEOUT_SECONDS": "60",
                },
                clear=True,
            ),
        ):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
                custom_instructions="instr",
                max_attempts_per_method=2,
            )

        assert result.success is True
        assert result.session_confirmed is False
        assert [call.args[0] for call in _mock_sleep.call_args_list[-1:]] == [60.0]

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_fallback_retries_when_assignment_response_missing_copilot_assignee(
        self,
        mock_gh_api,
        _mock_sleep: MagicMock,
    ) -> None:
        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/issues/42/events") and method == "GET":
                return json.dumps([])
            if endpoint.endswith("/issues/42") and method == "GET":
                return json.dumps({"number": 42, "assignees": []})
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                return json.dumps({"number": 42, "assignees": [{"login": "octocat"}]})
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
                custom_instructions="instr",
                max_attempts_per_method=1,
            )

        assert result.success is False
        assert "Issue assignment response did not include copilot-swe-agent[bot]" in result.error
        assert "Provider rate limit exhausted" not in result.error
        assert result.outcome == "confirmed_failure"

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_fallback_retries_negative_readback_until_attempt_budget_exhausted(
        self,
        mock_gh_api,
        _mock_sleep: MagicMock,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/issues/42/events") and method == "GET":
                return json.dumps([])
            if endpoint.endswith("/issues/42") and method == "GET":
                return json.dumps({"number": 42, "assignees": []})
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                return json.dumps({"number": 42, "assignees": [{"login": "octocat"}]})
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with (
            patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True),
            caplog.at_level(logging.INFO, logger="agentic_devtools.cli.ci.agent_assignment"),
        ):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
                custom_instructions="instr",
                max_attempts_per_method=3,
            )

        assert result.success is False
        assert result.outcome == "confirmed_failure"
        assert result.attempts == 3
        post_calls = [call for call in mock_gh_api.call_args_list if call.args[0].endswith("/issues/42/assignees")]
        assert len(post_calls) == 3
        assert (
            "assignment outcome=confirmed_failure token_identity=SPECKIT_PR_TOKEN "
            "response=missing_copilot_identity read_back=copilot_not_assigned attempt=3 final_state=unassigned"
        ) in caplog.text

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_fallback_reconciles_confirmed_success_via_readback_when_assignment_response_is_invalid_json(
        self,
        mock_gh_api,
        _mock_sleep: MagicMock,
    ) -> None:
        issue_reads = 0

        def side_effect(endpoint: str, **kwargs: object) -> str:
            nonlocal issue_reads
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/issues/42/events") and method == "GET":
                return json.dumps([])
            if endpoint.endswith("/issues/42") and method == "GET":
                issue_reads += 1
                assignees = [] if issue_reads <= 2 else [{"login": "copilot-swe-agent[bot]"}]
                return json.dumps({"number": 42, "assignees": assignees})
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                return "not-valid-json"
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
                custom_instructions="instr",
                max_attempts_per_method=1,
            )

        assert result.success is True
        assert result.outcome == "confirmed_success"
        assert any(call.args[0].endswith("/issues/42/assignees") for call in mock_gh_api.call_args_list)

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_secret_never_appears_in_logs_or_errors(
        self,
        mock_gh_api,
        _mock_sleep: MagicMock,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        secret = "super-secret-token"
        clock = {"now": 0.0}
        _mock_sleep.side_effect = lambda seconds: clock.__setitem__("now", clock["now"] + seconds)

        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/issues/42/events") and method == "GET":
                return json.dumps([])
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                return json.dumps({"number": 42, "assignees": [{"login": "copilot-swe-agent[bot]"}]})
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect

        with (
            patch("agentic_devtools.cli.ci.retry.time.monotonic", side_effect=lambda: clock["now"]),
            patch.dict("os.environ", {"SPECKIT_PR_TOKEN": secret}, clear=True),
        ):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
                custom_instructions="instr",
                max_attempts_per_method=1,
            )

        assert secret not in result.error
        assert result.success is True
        assert result.session_confirmed is False
        for rec in caplog.records:
            assert secret not in rec.getMessage()


class TestAgentAssignmentHelpers:
    """Coverage-focused tests for private helper branches."""

    def test_gh_api_call_proxies_to_github_provider(self) -> None:
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value="{}") as mock_gh_api:
            result = _gh_api_call("/repos/owner/repo/issues/1", method="GET", token="token")

        assert result == "{}"
        mock_gh_api.assert_called_once()

    def test_build_assignment_instructions_includes_optional_model(self) -> None:
        payload = _build_assignment_instructions(
            custom_instructions="do work",
            custom_agent="speckit.implement",
            model="claude-opus-4.6",
            repo="owner/repo",
            base_branch="main",
        )

        assignment = payload["agent_assignment"]
        assert payload["assignees"] == ["copilot-swe-agent[bot]"]
        assert assignment["custom_agent"] == "speckit.implement"
        assert assignment["model"] == "claude-opus-4.6"

    def test_validate_assignment_token_returns_actionable_error_on_401(self) -> None:
        with patch(
            "agentic_devtools.cli.ci.agent_assignment._gh_api_call",
            side_effect=RuntimeError("GitHub API error: gh: Bad credentials (HTTP 401)"),
        ):
            error = _validate_assignment_token(token="x", token_identity="SPECKIT_PR_TOKEN")

        assert "SPECKIT_PR_TOKEN" in error
        assert "failed authentication (HTTP 401 Bad credentials)" in error

    def test_validate_assignment_token_raises_non_401_errors(self) -> None:
        with patch(
            "agentic_devtools.cli.ci.agent_assignment._gh_api_call",
            side_effect=RuntimeError("GitHub API error: gh: Not Found (HTTP 404)"),
        ):
            with pytest.raises(RuntimeError, match="HTTP 404"):
                _validate_assignment_token(token="x", token_identity="SPECKIT_PR_TOKEN")

    def test_is_bad_credentials_error_helper(self) -> None:
        assert _is_bad_credentials_error("gh: Bad credentials (HTTP 401)") is True
        assert _is_bad_credentials_error("http 401 from gateway") is True
        assert _is_bad_credentials_error("HTTP 403 forbidden") is False
        assert _is_bad_credentials_error("Related to PR #401 only") is False

    def test_is_copilot_assigned(self) -> None:
        assert _is_copilot_assigned({"assignees": [{"login": "copilot-swe-agent[bot]"}]}) is True
        assert _is_copilot_assigned({"assignees": [{"login": "copilot-swe-agent"}]}) is True
        assert _is_copilot_assigned({"assignees": [{"login": "app/copilot-swe-agent"}]}) is True
        assert _is_copilot_assigned({"assignees": [{"name": "Copilot"}]}) is True
        assert _is_copilot_assigned({"assignee": {"login": "copilot-swe-agent[bot]"}}) is True
        assert _is_copilot_assigned({"assignees": [{"login": "octocat"}]}) is False

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_missing_identity_uses_issue_readback_without_retry(self, mock_gh_api: MagicMock) -> None:
        issue_reads = 0

        def side_effect(endpoint: str, **kwargs: object) -> str:
            nonlocal issue_reads
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/issues/42/events") and method == "GET":
                return json.dumps([])
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                return json.dumps({"number": 42, "assignees": [{"name": "accepted"}]})
            if endpoint.endswith("/issues/42") and method == "GET":
                issue_reads += 1
                assignees = [{"login": "Copilot"}] if issue_reads > 2 else []
                return json.dumps({"number": 42, "assignees": assignees})
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
                custom_instructions="instr",
                max_attempts_per_method=3,
            )

        assert result.success is True
        assert result.outcome == "confirmed_success"
        assert result.attempts == 1
        assert mock_gh_api.call_args_list[-1].args[0] == "/repos/owner/repo/issues/42"

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_existing_assignment_is_idempotent_without_post(self, mock_gh_api: MagicMock) -> None:
        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/issues/42") and method == "GET":
                return json.dumps({"number": 42, "assignees": [{"login": "app/copilot-swe-agent"}]})
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
                custom_instructions="instr",
                max_attempts_per_method=3,
            )

        assert result.success is True
        assert result.outcome == "confirmed_success"
        assert result.attempts == 0
        assert not any(call.args[0].endswith("/assignees") for call in mock_gh_api.call_args_list)

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_pre_post_idempotency_check_prevents_duplicate_coding_agent_task(self, mock_gh_api: MagicMock) -> None:
        """When Copilot is already assigned and use_primary=True, the pre-POST check returns
        confirmed_success before either assignment method POSTs a new session."""

        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/issues/42") and method == "GET":
                return json.dumps({"number": 42, "assignees": [{"login": "copilot-swe-agent[bot]"}]})
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
            )

        assert result.success is True
        assert result.outcome == "confirmed_success"
        assert result.attempts == 0
        assert not any("/copilot/coding-agent/tasks" in call.args[0] for call in mock_gh_api.call_args_list), (
            "coding-agent task POST must not be called when Copilot is already assigned"
        )
        assert not any(call.args[0].endswith("/assignees") for call in mock_gh_api.call_args_list)

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_inner_check_catches_concurrent_assignment_between_precheck_and_post(self, mock_gh_api: MagicMock) -> None:
        """If the pre-POST check finds no assignment but Copilot is assigned by the time the
        inner fallback check runs, the inner check returns confirmed_success without a POST."""
        reads: dict[str, int] = {"count": 0}

        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/issues/42") and method == "GET":
                reads["count"] += 1
                # pre-check: not assigned; inner check: assigned
                if reads["count"] == 1:
                    return json.dumps({"number": 42, "assignees": []})
                return json.dumps({"number": 42, "assignees": [{"login": "app/copilot-swe-agent"}]})
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
                custom_instructions="instr",
                max_attempts_per_method=3,
            )

        assert result.success is True
        assert result.outcome == "confirmed_success"
        assert result.attempts == 1
        assert not any(call.args[0].endswith("/assignees") for call in mock_gh_api.call_args_list)

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_accepted_assignment_with_inconclusive_readback_is_not_retried(self, mock_gh_api: MagicMock) -> None:
        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/issues/42/events") and method == "GET":
                return json.dumps([])
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                return json.dumps({"number": 42, "assignees": [{"name": "accepted"}]})
            if endpoint.endswith("/issues/42") and method == "GET":
                raise RuntimeError("temporary read failure")
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
                custom_instructions="instr",
                max_attempts_per_method=3,
            )

        assert result.success is True
        assert result.outcome == "accepted_unconfirmed"
        assert result.attempts == 1
        assert mock_gh_api.call_count == 8
        assert not any(call.args[0] == "/graphql" for call in mock_gh_api.call_args_list)

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_fallback_post_error_returns_confirmed_success_when_readback_confirms_assignment(
        self, mock_gh_api: MagicMock
    ) -> None:
        readbacks = {"count": 0}

        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint.endswith("/issues/42/events") and method == "GET":
                return json.dumps([])
            if endpoint.endswith("/issues/42") and method == "GET":
                readbacks["count"] += 1
                if readbacks["count"] <= 2:
                    return json.dumps({"number": 42, "assignees": []})
                return json.dumps({"number": 42, "assignees": [{"login": "copilot-swe-agent[bot]"}]})
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                raise RuntimeError("connection dropped after acceptance")
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
                custom_instructions="instr",
                max_attempts_per_method=3,
            )

        assert result.success is True
        assert result.method == "agent_assignment"
        assert result.outcome == "confirmed_success"
        assert result.attempts == 1

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_fallback_post_error_retries_when_readback_confirms_unassigned(self, mock_gh_api: MagicMock) -> None:
        issue_reads = {"count": 0}
        post_attempts = {"count": 0}
        event_reads = {"count": 0}

        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint.endswith("/issues/42/events") and method == "GET":
                event_reads["count"] += 1
                if post_attempts["count"] >= 2 and event_reads["count"] >= 2:
                    return json.dumps([{"id": 13, "url": "https://example/events/13", "event": "copilot_work_started"}])
                return json.dumps([])
            if endpoint.endswith("/issues/42") and method == "GET":
                issue_reads["count"] += 1
                if issue_reads["count"] <= 4:
                    return json.dumps({"number": 42, "assignees": []})
                return json.dumps({"number": 42, "assignees": [{"login": "copilot-swe-agent[bot]"}]})
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                post_attempts["count"] += 1
                if post_attempts["count"] == 1:
                    raise RuntimeError("connection dropped before response")
                return json.dumps({"number": 42, "assignees": [{"login": "copilot-swe-agent[bot]"}]})
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
                custom_instructions="instr",
                max_attempts_per_method=2,
            )

        assert result.success is True
        assert result.method == "agent_assignment"
        assert result.outcome == "confirmed_success"
        assert result.attempts == 2

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_fallback_post_error_returns_confirmed_failure_after_attempt_budget_exhausted(
        self, mock_gh_api: MagicMock
    ) -> None:
        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint.endswith("/issues/42/events") and method == "GET":
                return json.dumps([])
            if endpoint.endswith("/issues/42") and method == "GET":
                return json.dumps({"number": 42, "assignees": []})
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                raise RuntimeError("connection dropped before response")
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
                custom_instructions="instr",
                max_attempts_per_method=1,
            )

        assert result.success is False
        assert result.method == ""
        assert result.outcome == "confirmed_failure"
        assert result.attempts == 1
        assert "read-back did not confirm Copilot assignment" in result.error

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_fallback_post_error_returns_accepted_unconfirmed_when_readback_is_inconclusive(
        self, mock_gh_api: MagicMock
    ) -> None:
        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint.endswith("/issues/42/events") and method == "GET":
                return json.dumps([])
            if endpoint.endswith("/issues/42") and method == "GET":
                raise RuntimeError("temporary read failure")
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                raise RetryableError("connection dropped after acceptance")
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
                custom_instructions="instr",
                max_attempts_per_method=3,
            )

        assert result.success is True
        assert result.method == "agent_assignment"
        assert result.outcome == "accepted_unconfirmed"
        assert result.attempts == 1
        assert "read-back was inconclusive" in result.error

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_fallback_post_runtime_error_returns_confirmed_failure_when_readback_is_inconclusive(
        self, mock_gh_api: MagicMock
    ) -> None:
        """Definitive RuntimeError (4xx) on the POST must not yield accepted_unconfirmed.

        GitHub raises RuntimeError for definitive failures (403, 404, 422).  An inconclusive
        read-back after a definitive error must not promote the outcome to accepted_unconfirmed;
        it must be confirmed_failure so that the workflow does not apply implementation labels.
        """

        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint.endswith("/issues/42/events") and method == "GET":
                return json.dumps([])
            if endpoint.endswith("/issues/42") and method == "GET":
                raise RuntimeError("temporary read failure")
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                raise RuntimeError("GitHub API error: gh: Resource not found (HTTP 404)")
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
                custom_instructions="instr",
                max_attempts_per_method=1,
            )

        assert result.success is False
        assert result.method == ""
        assert result.outcome == "confirmed_failure"
        assert result.attempts == 1
        assert "read-back did not confirm Copilot assignment" in result.error

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_fallback_post_transport_error_returns_accepted_unconfirmed_when_readback_is_inconclusive(
        self, mock_gh_api: MagicMock
    ) -> None:
        """An unclassified transport RuntimeError (no HTTP 4xx) + inconclusive read-back → accepted_unconfirmed.

        ``_gh_api`` can raise ``RuntimeError`` for transport failures (connection reset,
        CLI crash) that carry no HTTP status code.  In that case the POST may have been
        accepted by GitHub; if read-back is also inconclusive the outcome must be
        ``accepted_unconfirmed``, not ``confirmed_failure``, to avoid masking a live session.
        """

        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint.endswith("/issues/42/events") and method == "GET":
                return json.dumps([])
            if endpoint.endswith("/issues/42") and method == "GET":
                raise RuntimeError("temporary read failure")
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                raise RuntimeError("connection reset by peer")
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
                custom_instructions="instr",
                max_attempts_per_method=1,
            )

        assert result.success is True
        assert result.method == "agent_assignment"
        assert result.outcome == "accepted_unconfirmed"
        assert result.attempts == 1
        assert "read-back was inconclusive" in result.error

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_resolve_copilot_actor_id_uses_graphql_features_header(self, mock_gh_api) -> None:
        mock_gh_api.return_value = _suggested_actors_response()
        actor_id = _resolve_copilot_actor_id(repo="owner/repo", token="token")

        assert actor_id == "BOT_copilot"
        assert "GraphQL-Features" in mock_gh_api.call_args.kwargs["headers"]

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_resolve_copilot_actor_id_returns_empty_when_missing(self, mock_gh_api) -> None:
        mock_gh_api.return_value = _suggested_actors_response(include_copilot=False)

        assert _resolve_copilot_actor_id(repo="owner/repo", token="token") == ""

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_resolve_copilot_actor_id_raises_on_graphql_errors(self, mock_gh_api) -> None:
        mock_gh_api.return_value = json.dumps({"errors": [{"message": "boom"}]})

        with pytest.raises(RuntimeError, match="GitHub GraphQL error"):
            _resolve_copilot_actor_id(repo="owner/repo", token="token")

    @pytest.mark.parametrize("repository", [None, "invalid"])
    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_resolve_copilot_actor_id_raises_on_invalid_repository_shape(self, mock_gh_api, repository) -> None:
        mock_gh_api.return_value = json.dumps({"data": {"repository": repository}})

        with pytest.raises(RuntimeError, match="data.repository"):
            _resolve_copilot_actor_id(repo="owner/repo", token="token")

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_resolve_copilot_actor_id_raises_on_missing_data_shape(self, mock_gh_api) -> None:
        mock_gh_api.return_value = json.dumps({"data": None})

        with pytest.raises(RuntimeError, match="missing object at data"):
            _resolve_copilot_actor_id(repo="owner/repo", token="token")

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_resolve_copilot_actor_id_raises_on_invalid_suggested_actors_shape(self, mock_gh_api) -> None:
        mock_gh_api.return_value = json.dumps({"data": {"repository": {"suggestedActors": None}}})

        with pytest.raises(RuntimeError, match="data.repository.suggestedActors"):
            _resolve_copilot_actor_id(repo="owner/repo", token="token")

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_resolve_copilot_actor_id_returns_empty_for_non_list_nodes(self, mock_gh_api) -> None:
        mock_gh_api.return_value = json.dumps({"data": {"repository": {"suggestedActors": {"nodes": "bad"}}}})

        assert _resolve_copilot_actor_id(repo="owner/repo", token="token") == ""

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_resolve_copilot_actor_id_handles_non_dict_and_non_matching_nodes(self, mock_gh_api) -> None:
        mock_gh_api.return_value = json.dumps(
            {
                "data": {
                    "repository": {
                        "suggestedActors": {"nodes": ["bad-node", {"id": "BOT_other", "login": "other-bot"}]},
                    },
                },
            },
        )

        assert _resolve_copilot_actor_id(repo="owner/repo", token="token") == ""

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_resolve_copilot_actor_id_matches_bot_login_variant(self, mock_gh_api) -> None:
        """GraphQL may return 'copilot-swe-agent[bot]' — must still be recognised."""
        mock_gh_api.return_value = json.dumps(
            {
                "data": {
                    "repository": {
                        "suggestedActors": {"nodes": [{"id": "BOT_copilot", "login": "copilot-swe-agent[bot]"}]}
                    }
                }
            }
        )

        assert _resolve_copilot_actor_id(repo="owner/repo", token="token") == "BOT_copilot"

    def test_is_copilot_assigned_returns_false_when_assignees_not_list(self) -> None:
        assert _is_copilot_assigned({"assignees": {"login": "copilot-swe-agent[bot]"}}) is False

    def test_is_copilot_assigned_ignores_non_dict_entries(self) -> None:
        assert _is_copilot_assigned({"assignees": ["bad-entry", {"login": "octocat"}]}) is False

    @pytest.mark.parametrize(
        ("event", "expected"),
        [
            ({"id": "9"}, 9),
            ({"id": "not-a-number"}, 0),
            ({}, 0),
        ],
    )
    def test_event_id_handles_non_integer_variants(self, event: dict, expected: int) -> None:
        assert _event_id(event) == expected

    @pytest.mark.parametrize(
        ("repo", "expected"),
        [
            ("owner/repo", "owner/repo"),
            ("owner/repo.git", "owner/repo"),
            ("  owner/repo  ", "owner/repo"),
            ("owner/repo/extra", None),
            ("owner/", None),
            ("/repo", None),
            ("invalid-repo", None),
            ("", None),
        ],
    )
    def test_validate_repo_format(self, repo: str, expected: str | None) -> None:
        assert _validate_repo_format(repo) == expected

    def test_extract_retryable_failure_message_for_unknown_exception(self) -> None:
        message = _extract_retryable_failure_message(ValueError("oops"))
        assert message == "ValueError: oops"

    @pytest.mark.parametrize(
        ("raw", "expected"),
        [
            ("0", 1),
            ("120", 60),
            ("", 15),
            ("abc", 15),
            ("17", 17),
        ],
    )
    def test_parse_clamped_env_int_for_initial_wait(self, raw: str, expected: int) -> None:
        with patch.dict("os.environ", {"AGDT_AGENT_START_POLL_INITIAL_SECONDS": raw}, clear=True):
            resolved = _parse_clamped_env_int(
                env_name="AGDT_AGENT_START_POLL_INITIAL_SECONDS",
                default=15,
                minimum=1,
                maximum=60,
            )
        assert resolved == expected

    @pytest.mark.parametrize(
        ("raw", "expected"),
        [
            ("30", 60),
            ("9000", 600),
            ("", 300),
            ("abc", 300),
            ("240", 240),
        ],
    )
    def test_parse_clamped_env_int_for_timeout(self, raw: str, expected: int) -> None:
        with patch.dict("os.environ", {"AGDT_AGENT_START_POLL_TIMEOUT_SECONDS": raw}, clear=True):
            resolved = _parse_clamped_env_int(
                env_name="AGDT_AGENT_START_POLL_TIMEOUT_SECONDS",
                default=300,
                minimum=60,
                maximum=600,
            )
        assert resolved == expected

    def test_extract_retryable_failure_message_for_rate_limit_error(self) -> None:
        message = _extract_retryable_failure_message(ProviderRateLimitError())
        assert "Provider rate limit exhausted" in message

    def test_extract_retryable_failure_message_for_rate_limit_error_includes_cause(self) -> None:
        cause = RetryableError("task never reached in_progress")
        try:
            raise ProviderRateLimitError() from cause
        except ProviderRateLimitError as exc:
            message = _extract_retryable_failure_message(exc)
        assert message == "task never reached in_progress"

    def test_extract_retryable_failure_message_uses_non_rate_limit_cause_text(self) -> None:
        try:
            raise ProviderRateLimitError() from RetryableError(
                "Issue assignment response did not include copilot-swe-agent[bot]"
            )
        except ProviderRateLimitError as exc:
            message = _extract_retryable_failure_message(exc)
        assert message == "Issue assignment response did not include copilot-swe-agent[bot]"

    def test_extract_retryable_failure_message_includes_rate_limit_cause_text(self) -> None:
        try:
            raise ProviderRateLimitError() from RetryableError("GitHub API error: HTTP 429")
        except ProviderRateLimitError as exc:
            message = _extract_retryable_failure_message(exc)
        assert message == "Provider rate limit exhausted; caused by: GitHub API error: HTTP 429"

    def test_wait_for_started_session_event_skips_sleep_when_timeout_elapsed(self) -> None:
        with (
            patch("agentic_devtools.cli.ci.agent_assignment._list_issue_events", return_value=[]),
            patch("agentic_devtools.cli.ci.retry.time.monotonic", return_value=100.0),
            patch("agentic_devtools.cli.ci.retry.time.sleep") as mock_sleep,
        ):
            result = _wait_for_started_session_event(
                repo="owner/repo",
                issue_number=42,
                token="token",
                baseline_event_id=0,
                initial_wait_seconds=15,
                timeout_seconds=0,
            )

        assert result is None
        mock_sleep.assert_not_called()

    @pytest.mark.parametrize(
        "exc",
        [
            RetryableError("HTTP 429 rate limited"),
            RuntimeError("network failure"),
            json.JSONDecodeError("Expecting value", "", 0),
        ],
    )
    def test_wait_for_started_session_event_swallows_list_events_exceptions(
        self, exc: Exception, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Exceptions from _list_issue_events are swallowed and return None (non-fatal)."""
        with (
            patch("agentic_devtools.cli.ci.agent_assignment._list_issue_events", side_effect=exc),
            patch("agentic_devtools.cli.ci.retry.time.monotonic", return_value=0.0),
            patch("agentic_devtools.cli.ci.retry.time.sleep"),
            caplog.at_level(logging.WARNING, logger="agentic_devtools.cli.ci.agent_assignment"),
        ):
            result = _wait_for_started_session_event(
                repo="owner/repo",
                issue_number=42,
                token="token",
                baseline_event_id=0,
                initial_wait_seconds=15,
                timeout_seconds=300,
            )

        assert result is None
        assert "session_confirmed=False" in caplog.text

    def test_wait_for_started_session_event_propagates_rate_limit(self) -> None:
        error = RetryableError("rate limited", provider="github", is_rate_limit=True)
        with (
            patch("agentic_devtools.cli.ci.agent_assignment._list_issue_events", side_effect=error),
            patch("agentic_devtools.cli.ci.retry.time.monotonic", return_value=0.0),
            patch("agentic_devtools.cli.ci.retry.time.sleep"),
        ):
            with pytest.raises(ProviderRateLimitError) as exc_info:
                _wait_for_started_session_event(
                    repo="owner/repo",
                    issue_number=42,
                    token="token",
                    baseline_event_id=0,
                    initial_wait_seconds=15,
                    timeout_seconds=300,
                )

        assert exc_info.value.is_rate_limit is True

    def test_raises_for_invalid_max_attempts(self) -> None:
        with pytest.raises(ValueError, match="max_attempts_per_method"):
            assign_issue_to_agent(
                repo="owner/repo",
                issue_number=1,
                problem_statement="run task",
                max_attempts_per_method=0,
            )

    @pytest.mark.parametrize(
        ("kwargs", "expected_error"),
        [
            (
                {
                    "repo": "owner/repo",
                    "issue_number": 0,
                    "problem_statement": "x",
                },
                "issue_number",
            ),
            (
                {
                    "repo": "invalid-repo",
                    "issue_number": 1,
                    "problem_statement": "x",
                },
                "owner/repo",
            ),
            (
                {
                    "repo": "owner/repo/extra",
                    "issue_number": 1,
                    "problem_statement": "x",
                },
                "owner/repo",
            ),
            (
                {
                    "repo": "owner/",
                    "issue_number": 1,
                    "problem_statement": "x",
                },
                "owner/repo",
            ),
            (
                {
                    "repo": "/repo",
                    "issue_number": 1,
                    "problem_statement": "x",
                },
                "owner/repo",
            ),
            (
                {
                    "repo": "owner/repo",
                    "issue_number": 1,
                    "problem_statement": "   ",
                },
                "problem_statement",
            ),
        ],
    )
    def test_input_validation_errors(self, kwargs: dict, expected_error: str) -> None:
        with pytest.raises(AgentAssignmentError, match=expected_error):
            assign_issue_to_agent(**kwargs)

    @patch("agentic_devtools.cli.ci.retry.time.sleep", return_value=None)
    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_primary_json_decode_path(self, mock_gh_api, _mock_sleep: MagicMock) -> None:
        clock = {"now": 0.0}
        _mock_sleep.side_effect = lambda seconds: clock.__setitem__("now", clock["now"] + seconds)

        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint.endswith("/issues/42") and method == "GET":
                return json.dumps({"number": 42, "assignees": []})
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/copilot/coding-agent/tasks") and method == "POST":
                return "{"
            if endpoint.endswith("/issues/42/events") and method == "GET":
                return json.dumps([])
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                return json.dumps({"number": 42, "assignees": [{"login": "copilot-swe-agent[bot]"}]})
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with (
            patch("agentic_devtools.cli.ci.retry.time.monotonic", side_effect=lambda: clock["now"]),
            patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True),
        ):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
                max_attempts_per_method=1,
            )

        assert result.success is True
        assert result.method == "agent_assignment"
        assert result.session_confirmed is False

    @patch("agentic_devtools.cli.ci.retry.time.sleep", return_value=None)
    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_primary_task_never_reaches_in_progress_returns_accepted_unconfirmed(
        self, mock_gh_api, _mock_sleep: MagicMock, caplog: pytest.LogCaptureFixture
    ) -> None:
        """An accepted task must not trigger a duplicate fallback assignment POST."""
        clock = {"now": 0.0}
        _mock_sleep.side_effect = lambda seconds: clock.__setitem__("now", clock["now"] + seconds)

        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint.endswith("/issues/42") and method == "GET":
                return json.dumps({"number": 42, "assignees": []})
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/copilot/coding-agent/tasks") and method == "POST":
                return json.dumps({"id": "task-1", "url": "https://example/task-1"})
            if "/copilot/coding-agent/tasks/task-1" in endpoint and method == "GET":
                return json.dumps({"id": "task-1", "status": "queued"})
            if endpoint.endswith("/issues/42/events") and method == "GET":
                return json.dumps([])
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                return json.dumps({"number": 42, "assignees": [{"login": "copilot-swe-agent[bot]"}]})
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with (
            caplog.at_level(logging.INFO, logger="agentic_devtools.cli.ci.agent_assignment"),
            patch("agentic_devtools.cli.ci.retry.time.monotonic", side_effect=lambda: clock["now"]),
            patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True),
        ):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
                max_attempts_per_method=1,
            )

        assert result.success is True
        assert result.method == "coding_agent_task"
        assert result.outcome == "accepted_unconfirmed"
        assert result.session_confirmed is False
        assert not any(call.args[0].endswith("/issues/42/assignees") for call in mock_gh_api.call_args_list)
        assert (
            "assignment outcome=accepted_unconfirmed token_identity=SPECKIT_PR_TOKEN "
            "response=task_not_started read_back=copilot_not_assigned attempt=1 final_state=unconfirmed"
        ) in caplog.text

    @patch("agentic_devtools.cli.ci.retry.time.sleep", return_value=None)
    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_fallback_json_decode_path(self, mock_gh_api, _mock_sleep: MagicMock) -> None:
        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/issues/42/events") and method == "GET":
                return "{"
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                return json.dumps({"number": 42, "assignees": [{"login": "copilot-swe-agent[bot]"}]})
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
                custom_instructions="instr",
                max_attempts_per_method=1,
            )

        assert result.success is False
        assert "agent_assignment" in result.error

    def test_extract_retryable_failure_message_for_runtime_error(self) -> None:
        message = _extract_retryable_failure_message(RuntimeError("network failure"))
        assert message == "network failure"

    @patch("agentic_devtools.cli.ci.retry.time.sleep", return_value=None)
    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_primary_missing_task_id_falls_back(self, mock_gh_api, _mock_sleep: MagicMock) -> None:
        """Primary fails fast when task response is missing required id or url."""
        clock = {"now": 0.0}
        _mock_sleep.side_effect = lambda seconds: clock.__setitem__("now", clock["now"] + seconds)

        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint.endswith("/issues/42") and method == "GET":
                return json.dumps({"number": 42, "assignees": []})
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/copilot/coding-agent/tasks") and method == "POST":
                return json.dumps({"url": "https://example/task"})  # id is missing
            if endpoint.endswith("/issues/42/events") and method == "GET":
                return json.dumps([])
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                return json.dumps({"number": 42, "assignees": [{"login": "copilot-swe-agent[bot]"}]})
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with (
            patch("agentic_devtools.cli.ci.retry.time.monotonic", side_effect=lambda: clock["now"]),
            patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True),
        ):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
                max_attempts_per_method=1,
            )

        assert result.success is True
        assert result.method == "agent_assignment"
        assert result.session_confirmed is False

    @patch("agentic_devtools.cli.ci.retry.time.sleep", return_value=None)
    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_events_endpoint_retryable_error_after_assignment_confirmed_succeeds(
        self, mock_gh_api, _mock_sleep: MagicMock, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Events endpoint transient failure after confirmed assignment yields success(session_confirmed=False)."""
        events_call_count = {"n": 0}

        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/issues/42/events") and method == "GET":
                events_call_count["n"] += 1
                if events_call_count["n"] == 1:
                    # First call: baseline (pre-assignment) — succeeds
                    return json.dumps([])
                # Subsequent calls: inside _wait_for_started_session_event — transient error
                raise RetryableError("HTTP 429 rate limited")
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                return json.dumps({"number": 42, "assignees": [{"login": "copilot-swe-agent[bot]"}]})
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect

        with (
            patch("agentic_devtools.cli.ci.retry.time.monotonic", return_value=0.0),
            patch.dict(
                "os.environ",
                {
                    "COPILOT_GITHUB_TOKEN": "token",
                    "AGDT_AGENT_START_POLL_TIMEOUT_SECONDS": "60",
                    "AGDT_AGENT_START_POLL_INITIAL_SECONDS": "60",
                },
                clear=True,
            ),
            caplog.at_level(logging.WARNING, logger="agentic_devtools.cli.ci.agent_assignment"),
        ):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
                custom_instructions="instr",
                max_attempts_per_method=1,
            )

        assert result.success is True
        assert result.method == "agent_assignment"
        assert result.session_confirmed is False
        assert "session_confirmed=False" in caplog.text
        assert "poll_timeout_seconds=60" in caplog.text

    @patch("agentic_devtools.cli.ci.retry.time.sleep", return_value=None)
    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_primary_poll_exception_swallowed_returns_accepted_unconfirmed(
        self, mock_gh_api, _mock_sleep: MagicMock
    ) -> None:
        """Accepted task creation still short-circuits fallback when poll reads stay negative."""
        clock = {"now": 0.0}
        _mock_sleep.side_effect = lambda seconds: clock.__setitem__("now", clock["now"] + seconds)

        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint.endswith("/issues/42") and method == "GET":
                return json.dumps({"number": 42, "assignees": []})
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/copilot/coding-agent/tasks") and method == "POST":
                return json.dumps({"id": "task-1", "url": "https://example/task-1"})
            if "/copilot/coding-agent/tasks/task-1" in endpoint and method == "GET":
                raise RuntimeError("transient poll failure")
            if endpoint.endswith("/issues/42/events") and method == "GET":
                return json.dumps([])
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                return json.dumps({"number": 42, "assignees": [{"login": "copilot-swe-agent[bot]"}]})
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with (
            patch("agentic_devtools.cli.ci.retry.time.monotonic", side_effect=lambda: clock["now"]),
            patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True),
        ):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
                max_attempts_per_method=1,
            )

        assert result.success is True
        assert result.method == "coding_agent_task"
        assert result.outcome == "accepted_unconfirmed"
        assert result.session_confirmed is False
        assert not any(call.args[0].endswith("/issues/42/assignees") for call in mock_gh_api.call_args_list)

    @patch("agentic_devtools.cli.ci.retry.time.sleep", return_value=None)
    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_primary_missing_task_metadata_does_not_retry_post_when_readback_confirms_assignment(
        self, mock_gh_api, _mock_sleep: MagicMock
    ) -> None:
        readbacks = {"count": 0}

        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint.endswith("/issues/42") and method == "GET":
                readbacks["count"] += 1
                if readbacks["count"] == 1:
                    return json.dumps({"number": 42, "assignees": []})
                return json.dumps({"number": 42, "assignees": [{"login": "copilot-swe-agent[bot]"}]})
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/copilot/coding-agent/tasks") and method == "POST":
                return json.dumps({"url": "https://example/task"})
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
                max_attempts_per_method=3,
            )

        assert result.success is True
        assert result.method == "coding_agent_task"
        assert result.outcome == "confirmed_success"
        assert result.session_confirmed is False
        primary_posts = [
            call for call in mock_gh_api.call_args_list if call.args[0].endswith("/copilot/coding-agent/tasks")
        ]
        assert len(primary_posts) == 1
        assert not any(call.args[0].endswith("/assignees") for call in mock_gh_api.call_args_list)

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_primary_request_error_returns_confirmed_success_when_readback_confirms_assignment(
        self, mock_gh_api
    ) -> None:
        readbacks = {"count": 0}

        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint.endswith("/issues/42") and method == "GET":
                readbacks["count"] += 1
                if readbacks["count"] == 1:
                    return json.dumps({"number": 42, "assignees": []})
                return json.dumps({"number": 42, "assignees": [{"login": "copilot-swe-agent[bot]"}]})
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/copilot/coding-agent/tasks") and method == "POST":
                raise RuntimeError("POST failed after acceptance")
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
            )

        assert result.success is True
        assert result.method == "coding_agent_task"
        assert result.outcome == "confirmed_success"
        assert result.session_confirmed is False
        assert not any(call.args[0].endswith("/issues/42/assignees") for call in mock_gh_api.call_args_list)

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_primary_request_error_falls_back_when_readback_is_inconclusive(self, mock_gh_api) -> None:
        """A definitive 4xx primary POST error falls back when read-back is inconclusive.

        When the primary POST returns a structured HTTP 4xx (rejected by GitHub), the
        primary path must not claim accepted_unconfirmed.  The call falls through to the
        agent_assignment fallback, which then succeeds.
        """
        event_reads = {"count": 0}

        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint.endswith("/issues/42") and method == "GET":
                raise RuntimeError("temporary read failure")
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/copilot/coding-agent/tasks") and method == "POST":
                raise RuntimeError("GitHub API error: gh: HTTP 403 Forbidden")
            if endpoint.endswith("/issues/42/events") and method == "GET":
                event_reads["count"] += 1
                if event_reads["count"] >= 2:
                    return json.dumps([{"id": 10, "url": "https://example/events/10", "event": "copilot_work_started"}])
                return json.dumps([])
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                return json.dumps({"number": 42, "assignees": [{"login": "copilot-swe-agent[bot]"}]})
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
            )

        assert result.success is True
        assert result.method == "agent_assignment"
        assert result.outcome == "confirmed_success"
        assert result.session_confirmed is True
        assert any(call.args[0].endswith("/issues/42/assignees") for call in mock_gh_api.call_args_list)

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_primary_transport_error_returns_accepted_unconfirmed_when_readback_is_inconclusive(
        self, mock_gh_api
    ) -> None:
        """An ambiguous transport RuntimeError from the primary POST must not fall back.

        ``_gh_api`` raises ``RuntimeError`` for any non-retryable ``gh`` exit,
        including unclassified transport failures (connection reset, CLI crash).
        When the error carries no HTTP 4xx status the POST may have reached GitHub;
        if read-back is also inconclusive, the outcome must be ``accepted_unconfirmed``
        from the primary path — not a fallback that could create a duplicate session.
        """

        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint.endswith("/issues/42") and method == "GET":
                raise RuntimeError("temporary read failure")
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/copilot/coding-agent/tasks") and method == "POST":
                raise RuntimeError("connection reset by peer")
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                raise AssertionError("fallback assignees POST must not be called for ambiguous transport error")
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
            )

        assert result.success is True
        assert result.method == "coding_agent_task"
        assert result.outcome == "accepted_unconfirmed"
        assert not any(call.args[0].endswith("/issues/42/assignees") for call in mock_gh_api.call_args_list)

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_primary_request_error_falls_back_when_readback_confirms_unassigned(self, mock_gh_api) -> None:
        event_reads = {"count": 0}

        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint.endswith("/issues/42") and method == "GET":
                return json.dumps({"number": 42, "assignees": []})
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/copilot/coding-agent/tasks") and method == "POST":
                raise RuntimeError("POST failed before assignment")
            if endpoint.endswith("/issues/42/events") and method == "GET":
                event_reads["count"] += 1
                if event_reads["count"] >= 2:
                    return json.dumps([{"id": 10, "url": "https://example/events/10", "event": "copilot_work_started"}])
                return json.dumps([])
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                return json.dumps({"number": 42, "assignees": [{"login": "copilot-swe-agent[bot]"}]})
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
            )

        assert result.success is True
        assert result.method == "agent_assignment"
        assert result.session_confirmed is True

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_primary_retryable_error_returns_confirmed_success_when_readback_confirms_assignment(
        self, mock_gh_api
    ) -> None:
        """RetryableError (429/5xx) from primary POST is caught and reconciled via read-back."""
        readbacks = {"count": 0}

        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint.endswith("/issues/42") and method == "GET":
                readbacks["count"] += 1
                if readbacks["count"] == 1:
                    return json.dumps({"number": 42, "assignees": []})
                return json.dumps({"number": 42, "assignees": [{"login": "copilot-swe-agent[bot]"}]})
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/copilot/coding-agent/tasks") and method == "POST":
                raise RetryableError("HTTP 429 rate limited")
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
            )

        assert result.success is True
        assert result.method == "coding_agent_task"
        assert result.outcome == "confirmed_success"
        assert result.session_confirmed is False
        assert not any(call.args[0].endswith("/issues/42/assignees") for call in mock_gh_api.call_args_list)

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_primary_explicit_http_retryable_error_falls_back_when_readback_is_inconclusive(self, mock_gh_api) -> None:
        """Explicit HTTP retryable failures must not become primary accepted_unconfirmed."""
        event_reads = {"count": 0}

        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint.endswith("/issues/42") and method == "GET":
                raise RuntimeError("temporary read failure")
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/copilot/coding-agent/tasks") and method == "POST":
                raise RetryableError("HTTP 429 rate limited")
            if endpoint.endswith("/issues/42/events") and method == "GET":
                event_reads["count"] += 1
                if event_reads["count"] >= 2:
                    return json.dumps([{"id": 10, "url": "https://example/events/10", "event": "copilot_work_started"}])
                return json.dumps([])
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                return json.dumps({"number": 42, "assignees": [{"login": "copilot-swe-agent[bot]"}]})
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
            )

        assert result.success is True
        assert result.method == "agent_assignment"
        assert result.outcome == "confirmed_success"
        assert result.session_confirmed is True
        assert any(call.args[0].endswith("/issues/42/assignees") for call in mock_gh_api.call_args_list)

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_fallback_explicit_http_retryable_error_returns_confirmed_failure_when_readback_is_inconclusive(
        self, mock_gh_api
    ) -> None:
        """Fallback explicit HTTP retryable failures must not become accepted_unconfirmed."""

        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint.endswith("/issues/42/events") and method == "GET":
                return json.dumps([])
            if endpoint.endswith("/issues/42") and method == "GET":
                raise RuntimeError("temporary read failure")
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                raise RetryableError("HTTP 429 rate limited")
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
                custom_instructions="instr",
                max_attempts_per_method=1,
            )

        assert result.success is False
        assert result.method == ""
        assert result.outcome == "confirmed_failure"
        assert "read-back did not confirm Copilot assignment" in result.error

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_primary_invalid_json_returns_accepted_unconfirmed_when_readback_is_inconclusive(self, mock_gh_api) -> None:
        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint.endswith("/issues/42") and method == "GET":
                raise RuntimeError("temporary read failure")
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/copilot/coding-agent/tasks") and method == "POST":
                return "{"
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
            )

        assert result.success is True
        assert result.method == "coding_agent_task"
        assert result.outcome == "accepted_unconfirmed"
        assert result.session_confirmed is False
        assert result.error

    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_primary_non_object_json_returns_accepted_unconfirmed_when_readback_is_inconclusive(
        self, mock_gh_api
    ) -> None:
        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint.endswith("/issues/42") and method == "GET":
                raise RuntimeError("temporary read failure")
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/copilot/coding-agent/tasks") and method == "POST":
                return "[]"
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
            )

        assert result.success is True
        assert result.method == "coding_agent_task"
        assert result.outcome == "accepted_unconfirmed"
        assert result.session_confirmed is False
        assert result.error

    @patch("agentic_devtools.cli.ci.retry.time.sleep", return_value=None)
    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_primary_non_object_json_falls_back_when_readback_confirms_unassigned(
        self, mock_gh_api, _mock_sleep: MagicMock
    ) -> None:
        event_reads = {"count": 0}

        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint.endswith("/issues/42") and method == "GET":
                return json.dumps({"number": 42, "assignees": []})
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/copilot/coding-agent/tasks") and method == "POST":
                return "[]"
            if endpoint.endswith("/issues/42/events") and method == "GET":
                event_reads["count"] += 1
                if event_reads["count"] >= 2:
                    return json.dumps([{"id": 10, "url": "https://example/events/10", "event": "copilot_work_started"}])
                return json.dumps([])
            if endpoint.endswith("/issues/42/assignees") and method == "POST":
                return json.dumps({"number": 42, "assignees": [{"login": "copilot-swe-agent[bot]"}]})
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
            )

        assert result.success is True
        assert result.method == "agent_assignment"
        assert result.outcome == "confirmed_success"
        assert result.session_confirmed is True
        assert any(call.args[0].endswith("/issues/42/assignees") for call in mock_gh_api.call_args_list)

    @patch("agentic_devtools.cli.ci.retry.time.sleep", return_value=None)
    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_primary_task_not_started_returns_confirmed_success_when_readback_confirms_assignment(
        self, mock_gh_api, _mock_sleep: MagicMock, caplog: pytest.LogCaptureFixture
    ) -> None:
        readbacks = {"count": 0}

        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint.endswith("/issues/42") and method == "GET":
                readbacks["count"] += 1
                if readbacks["count"] == 1:
                    return json.dumps({"number": 42, "assignees": []})
                return json.dumps({"number": 42, "assignees": [{"login": "copilot-swe-agent[bot]"}]})
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/copilot/coding-agent/tasks") and method == "POST":
                return json.dumps({"id": "task-1", "url": "https://example/task-1"})
            if "/copilot/coding-agent/tasks/task-1" in endpoint and method == "GET":
                return json.dumps({"id": "task-1", "status": "queued"})
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with (
            patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True),
            caplog.at_level(logging.INFO, logger="agentic_devtools.cli.ci.agent_assignment"),
        ):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
                max_attempts_per_method=3,
            )

        assert result.success is True
        assert result.method == "coding_agent_task"
        assert result.outcome == "confirmed_success"
        assert result.session_confirmed is False
        assert (
            "assignment outcome=confirmed_success token_identity=SPECKIT_PR_TOKEN "
            "response=task_not_started read_back=copilot_assigned attempt=1 final_state=assigned"
        ) in caplog.text

    @patch("agentic_devtools.cli.ci.retry.time.sleep", return_value=None)
    @patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
    def test_primary_task_not_started_returns_accepted_unconfirmed_without_fallback(
        self, mock_gh_api, _mock_sleep: MagicMock
    ) -> None:
        def side_effect(endpoint: str, **kwargs: object) -> str:
            method = kwargs.get("method")
            if endpoint == "/user" and method == "GET":
                return json.dumps({"login": "token-user"})
            if endpoint.endswith("/issues/42") and method == "GET":
                return json.dumps({"number": 42, "assignees": []})
            if endpoint == "/graphql" and method == "POST":
                return _suggested_actors_response()
            if endpoint.endswith("/copilot/coding-agent/tasks") and method == "POST":
                return json.dumps({"id": "task-1", "url": "https://example/task-1"})
            if "/copilot/coding-agent/tasks/task-1" in endpoint and method == "GET":
                return json.dumps({"id": "task-1", "status": "queued"})
            raise AssertionError(f"unexpected call: {endpoint} {method}")

        mock_gh_api.side_effect = side_effect
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token"}, clear=True):
            result = assign_issue_to_agent(
                repo="owner/repo",
                issue_number=42,
                problem_statement="run task",
                max_attempts_per_method=3,
            )

        assert result.success is True
        assert result.method == "coding_agent_task"
        assert result.outcome == "accepted_unconfirmed"
        assert result.session_confirmed is False
        assert result.task_id == "task-1"
        assert result.task_url == "https://example/task-1"
        assert not any(call.args[0].endswith("/issues/42/assignees") for call in mock_gh_api.call_args_list)
