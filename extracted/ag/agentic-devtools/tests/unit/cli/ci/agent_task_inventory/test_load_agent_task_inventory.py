"""Tests for loading paginated Agent Tasks inventory."""

import json
import subprocess
from unittest.mock import patch

import pytest

from agentic_devtools.ai_providers.agent_tasks_payload import AGENT_TASKS_API_VERSION
from agentic_devtools.cli.ci.agent_task_inventory import load_agent_task_inventory
from agentic_devtools.cli.ci.models import AgentTaskInventoryLoadResult
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError

MODULE = "agentic_devtools.cli.ci.agent_task_inventory"
PROVIDER_MODULE = "agentic_devtools.cli.ci.github_provider"


def _response(payload: object, *, returncode: int = 0, stderr: str = "") -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(["gh", "api"], returncode, json.dumps(payload), stderr)


def test_loads_pages_in_order_and_preserves_request_contract() -> None:
    first_page = [{"id": f"task-{index}", "state": "running"} for index in range(100)]
    final_page = [{"id": "last", "status": "completed"}]
    with (
        patch(f"{MODULE}.run_safe") as mock_runner,
        patch(
            f"{PROVIDER_MODULE}._run_readonly_gh_command",
            side_effect=[_response(first_page), _response({"tasks": final_page})],
        ) as mock_command,
    ):
        result = load_agent_task_inventory("org/repo", pr_number=42)
    assert isinstance(result, AgentTaskInventoryLoadResult)
    assert result.tasks == tuple([*first_page, *final_page])
    assert result.complete is True
    assert result.availability == "complete"
    assert result.failure_category is None
    assert result.incomplete_reasons == ()
    assert [call.args[0][1] for call in mock_command.call_args_list] == [
        "agents/repos/org/repo/tasks?per_page=100&page=1",
        "agents/repos/org/repo/tasks?per_page=100&page=2",
    ]
    assert mock_command.call_args.kwargs == {"timeout_seconds": 10, "runner": mock_runner}
    assert mock_command.call_args.args[0][2:] == [
        "--header",
        "Accept: application/vnd.github+json",
        "--header",
        f"X-GitHub-Api-Version: {AGENT_TASKS_API_VERSION}",
    ]


@pytest.mark.parametrize(
    ("status", "category"),
    [
        (404, "http_not_found"),
        (401, "authentication"),
        (403, "permission"),
        (500, "provider_unavailable"),
    ],
)
@pytest.mark.parametrize("later_page", [False, True])
def test_explicit_http_failures_preserve_prior_rows(status, category, later_page) -> None:
    rows = [{"state": "running"}] * 100 if later_page else []
    responses = ([_response(rows)] if later_page else []) + [_response({"status": str(status)}, returncode=1)]
    with patch(f"{PROVIDER_MODULE}._run_readonly_gh_command", side_effect=responses):
        result = load_agent_task_inventory("org/repo", pr_number=42)
    assert result.tasks == tuple(rows)
    assert result.complete is False
    assert result.availability == ("partial" if rows else "unavailable")
    assert result.failure_category == category
    assert result.http_status == status
    assert result.incomplete_reasons


def test_never_guesses_status_from_stderr() -> None:
    with patch(
        f"{PROVIDER_MODULE}._run_readonly_gh_command",
        return_value=_response({}, returncode=1, stderr="HTTP 404 not supported"),
    ):
        result = load_agent_task_inventory("org/repo", pr_number=42)
    assert result.http_status is None
    assert result.failure_category == "provider_unavailable"
    assert not result.complete


@pytest.mark.parametrize("payload", [None, {}, {"tasks": None}, "text", 17])
def test_malformed_containers_are_unavailable(payload) -> None:
    with patch(f"{PROVIDER_MODULE}._run_readonly_gh_command", return_value=_response(payload)):
        result = load_agent_task_inventory("org/repo", pr_number=42)
    assert result.tasks == ()
    assert result.failure_category == "malformed_response"
    assert result.availability == "unavailable"


@pytest.mark.parametrize(
    ("bad_row", "category"),
    [
        (None, "malformed_response"),
        (17, "malformed_response"),
        ([], "malformed_response"),
        ({}, "unknown_task_state"),
        ({"state": "paused"}, "unknown_task_state"),
        ({"state": 42}, "unknown_task_state"),
    ],
)
@pytest.mark.parametrize("include_usable", [False, True])
def test_bad_rows_do_not_discard_usable_rows(bad_row, category, include_usable) -> None:
    rows = [{"id": "usable", "state": "running"}] if include_usable else []
    with patch(f"{PROVIDER_MODULE}._run_readonly_gh_command", return_value=_response([*rows, bad_row])):
        result = load_agent_task_inventory("org/repo", pr_number=42)
    assert result.tasks == tuple(rows)
    assert result.failure_category == category
    assert result.availability == ("partial" if rows else "unavailable")
    assert result.incomplete_reasons


@pytest.mark.parametrize("later_page", [False, True])
@pytest.mark.parametrize(
    ("failure", "category"),
    [
        (subprocess.TimeoutExpired("gh", 1), "retrieval_exhausted"),
        (OSError("unavailable"), "provider_unavailable"),
        (json.JSONDecodeError("bad JSON", "{", 0), "malformed_response"),
        (ValueError("bad"), "malformed_response"),
        (TypeError("bad"), "malformed_response"),
        (ProviderRateLimitError(is_rate_limit=False), "provider_unavailable"),
        (RuntimeError("transport failed"), "provider_unavailable"),
        (RetryableError("provider unavailable"), "provider_unavailable"),
    ],
)
def test_exceptions_are_typed_and_keep_rows(failure, category, later_page) -> None:
    rows = [{"state": "running"}] * 100 if later_page else []
    responses = ([_response(rows)] if later_page else []) + [failure]
    with patch(f"{PROVIDER_MODULE}._run_readonly_gh_command", side_effect=responses):
        result = load_agent_task_inventory("org/repo", pr_number=42)
    assert result.tasks == tuple(rows)
    assert result.failure_category == category
    assert not result.complete


def test_malformed_json_is_unavailable() -> None:
    response = subprocess.CompletedProcess(["gh", "api"], 0, "{", "")
    with patch(f"{PROVIDER_MODULE}._run_readonly_gh_command", return_value=response):
        result = load_agent_task_inventory("org/repo", pr_number=42)
    assert result.failure_category == "malformed_response"
    assert result.availability == "unavailable"


def test_page_limit_preserves_all_rows() -> None:
    rows = [{"state": "running"}] * 100
    with patch(f"{PROVIDER_MODULE}._run_readonly_gh_command", return_value=_response(rows)) as command:
        result = load_agent_task_inventory("org/repo", pr_number=42)
    assert result.tasks == tuple(rows * 10)
    assert result.failure_category == "retrieval_exhausted"
    assert result.availability == "partial"
    assert command.call_count == 10


def test_bad_rows_do_not_shorten_pagination() -> None:
    with patch(
        f"{PROVIDER_MODULE}._run_readonly_gh_command",
        side_effect=[_response([None] * 100), _response([{"state": "running"}])],
    ) as command:
        result = load_agent_task_inventory("org/repo", pr_number=42)
    assert command.call_count == 2
    assert result.tasks == ({"state": "running"},)
    assert result.availability == "partial"


def test_rate_limit_propagates_unchanged() -> None:
    failure = ProviderRateLimitError(is_rate_limit=True)
    with patch(f"{PROVIDER_MODULE}._run_readonly_gh_command", side_effect=failure):
        with pytest.raises(ProviderRateLimitError) as caught:
            load_agent_task_inventory("org/repo", pr_number=42)
    assert caught.value is failure


def test_retryable_rate_limit_is_converted_without_retrying() -> None:
    failure = RetryableError(
        "rate limited",
        retry_after=20,
        remaining=0,
        provider="github",
        credential_identity="default",
        source="response",
        is_rate_limit=True,
    )
    with patch(f"{PROVIDER_MODULE}._run_readonly_gh_command", side_effect=failure) as command:
        with pytest.raises(ProviderRateLimitError) as caught:
            load_agent_task_inventory("org/repo", pr_number=42)
    assert caught.value.retry_after_seconds == 20
    assert caught.value.remaining == 0
    assert caught.value.provider == "github"
    assert caught.value.credential_identity == "default"
    assert caught.value.source == "response"
    assert command.call_count == 1


def test_empty_success_is_complete() -> None:
    with patch(f"{PROVIDER_MODULE}._run_readonly_gh_command", return_value=_response([])):
        result = load_agent_task_inventory("org/repo", pr_number=42)
    assert result.tasks == ()
    assert result.complete
