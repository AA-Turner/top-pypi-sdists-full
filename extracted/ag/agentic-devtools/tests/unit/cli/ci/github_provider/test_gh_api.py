"""Tests for github_provider._gh_api()."""

from __future__ import annotations

import subprocess
from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest

from agentic_devtools.cli.ci import agent_task_diagnostics, github_provider
from agentic_devtools.cli.ci.github_api_error import GitHubApiError
from agentic_devtools.cli.ci.github_provider import _gh_api
from agentic_devtools.cli.ci.read_token_pool import ReadCredential
from agentic_devtools.cli.ci.retry import ProviderRateLimitError, RetryableError


class _Result:
    returncode = 0
    stdout = "{}"
    stderr = ""


@patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=_Result())
def test_gh_api_adds_headers_to_command(mock_run_safe) -> None:
    _gh_api(
        "/repos/owner/repo/copilot/coding-agent/tasks",
        method="POST",
        body={"problem_statement": "test"},
        headers={"X-GitHub-Api-Version": "2022-11-28"},
    )

    cmd = mock_run_safe.call_args.args[0]
    assert "-H" in cmd
    assert "X-GitHub-Api-Version: 2022-11-28" in cmd
    assert "--include" in cmd


def test_gh_api_cross_repository_read_keeps_the_default_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GH_TOKEN", "default-token")
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.github_provider._get_read_token_pool",
        lambda: SimpleNamespace(
            repo="owner/current",
            default_token="default-token",
            default_identity="DEFAULT_CLASSIC_REPO_WORKFLOW_PAT",
        ),
    )
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.github_provider._call_with_read_token_pool",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("cross-repository read must bypass pooling")),
    )
    runner = Mock(return_value=_Result())
    monkeypatch.setattr("agentic_devtools.cli.ci.github_provider.run_safe", runner)

    _gh_api("/agents/repos/owner/private/tasks", token="default-token")

    assert runner.call_args.kwargs["env"]["GH_TOKEN"] == "default-token"


@patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=_Result())
def test_gh_api_can_skip_included_headers_for_raw_body_calls(mock_run_safe) -> None:
    response = _gh_api("/repos/o/r/contents/file.txt", include_headers=False)

    cmd = mock_run_safe.call_args.args[0]
    assert "--include" not in cmd
    assert response == "{}"


def test_gh_api_extracts_rate_limit_headers() -> None:
    result = _Result()
    result.returncode = 1
    result.stdout = "HTTP/1.1 403 Forbidden\nRetry-After: 120\nX-RateLimit-Remaining: 0\n\n"
    result.stderr = ""
    with patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=result):
        with pytest.raises(RetryableError) as exc_info:
            _gh_api("/repos/o/r", credential_identity="COPILOT_GITHUB_TOKEN")
    assert exc_info.value.retry_after == 120
    assert exc_info.value.remaining == 0
    assert exc_info.value.credential_identity == "COPILOT_GITHUB_TOKEN"


def test_gh_api_aggregates_duplicate_rate_limit_headers_conservatively() -> None:
    result = _Result()
    result.returncode = 1
    result.stdout = (
        "HTTP/1.1 403 Forbidden\nRetry-After: 60, 120\nX-RateLimit-Reset: 100, 500\nX-RateLimit-Remaining: 1, 0\n\n"
    )
    result.stderr = ""
    with patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=result):
        with pytest.raises(RetryableError) as exc_info:
            _gh_api("/repos/o/r", credential_identity="COPILOT_GITHUB_TOKEN")
    assert exc_info.value.retry_after == 120
    assert exc_info.value.reset_timestamp == 500
    assert exc_info.value.remaining == 0


def test_gh_api_keeps_plain_forbidden_non_retryable() -> None:
    result = _Result()
    result.returncode = 1
    result.stdout = "HTTP/1.1 403 Forbidden\n\n"
    result.stderr = "HTTP 403: permission denied"
    with patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=result):
        with pytest.raises(RuntimeError):
            _gh_api("/repos/o/r")


def test_gh_api_keeps_reset_only_forbidden_non_retryable() -> None:
    result = _Result()
    result.returncode = 1
    result.stdout = "HTTP/1.1 403 Forbidden\nX-RateLimit-Reset: 500\nX-RateLimit-Remaining: 1\n\n"
    result.stderr = "HTTP 403: resource not accessible by integration"
    with patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=result):
        with pytest.raises(RuntimeError):
            _gh_api("/repos/o/r")


@patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=_Result())
def test_gh_api_passes_bounded_timeout_to_run_safe(mock_run_safe) -> None:
    _gh_api("/repos/o/r")

    assert mock_run_safe.call_args.kwargs["timeout"] == 60


@pytest.mark.parametrize("timeout_seconds", [0, -1, True, "5"])
def test_gh_api_rejects_invalid_timeout(timeout_seconds) -> None:
    with pytest.raises(ValueError, match="timeout_seconds must be a positive integer"):
        _gh_api("/repos/o/r", timeout_seconds=timeout_seconds)


def test_gh_api_raises_retryable_error_on_timeout() -> None:
    with patch(
        "agentic_devtools.cli.ci.github_provider.run_safe",
        side_effect=subprocess.TimeoutExpired(cmd="gh api /repos/o/r", timeout=60),
    ):
        with pytest.raises(RetryableError, match="timed out"):
            _gh_api("/repos/o/r")


def test_gh_api_distinguishes_missing_gh_executable_from_http_404(monkeypatch: pytest.MonkeyPatch) -> None:
    cause = OSError("launch cause")
    launch_error = FileNotFoundError("gh executable is missing")
    launch_error.__cause__ = cause
    http_404 = SimpleNamespace(returncode=1, stdout="HTTP/1.1 404 Not Found\n\n", stderr="Not Found")
    runner = Mock(side_effect=[launch_error, http_404])
    monkeypatch.setattr(github_provider, "run_safe", runner)
    with pytest.raises(FileNotFoundError) as launch:
        _gh_api("/agents/repos/owner/repo/tasks")
    assert launch.value is launch_error and launch.value.__cause__ is cause
    assert "http_status=not captured" in launch.value.__notes__[0]
    with pytest.raises(GitHubApiError, match="http_status=404; http_status_source=response_headers") as http:
        _gh_api("/agents/repos/owner/repo/tasks?per_page=10&page=1", token="request-token")
    assert http.value.http_status == 404
    assert "returncode=1" in str(http.value)


def test_agent_tasks_failure_diagnostics_mark_uncaptured_fields(monkeypatch: pytest.MonkeyPatch) -> None:
    result = SimpleNamespace(returncode=1, stdout="", stderr="HTTP 404: not found")
    monkeypatch.setattr(github_provider, "run_safe", Mock(return_value=result))
    monkeypatch.setattr(agent_task_diagnostics.importlib.metadata, "version", Mock(side_effect=RuntimeError))
    monkeypatch.setattr(agent_task_diagnostics.shutil, "which", Mock(side_effect=OSError("PATH unavailable")))
    with pytest.raises(GitHubApiError) as error:
        _gh_api("/agents/repos/owner/repo/tasks", paginate=True)
    assert error.value.http_status == 404
    assert "url=not captured" in str(error.value)
    assert "http_status=404; http_status_source=stderr; returncode=1; response_body=not captured" in str(error.value)


@pytest.mark.parametrize("status", [500, 502, 503, 504])
@pytest.mark.parametrize("prefix", ["", "Request failed: "])
def test_gh_api_retries_on_bare_midline_server_status(status: int, prefix: str) -> None:
    result = _Result()
    result.returncode = 1
    result.stdout = ""
    result.stderr = f"{prefix}{status} Server Error"
    with patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=result):
        with pytest.raises(RetryableError, match="server error"):
            _gh_api("/repos/o/r")


def test_gh_api_does_not_retry_structured_404_with_issue_url_digits() -> None:
    result = _Result()
    result.returncode = 1
    result.stdout = "HTTP/1.1 404 Not Found\n\n"
    result.stderr = "Not found: https://github.com/o/r/issues/503"
    with patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=result):
        with pytest.raises(RuntimeError):
            _gh_api("/repos/o/r")


def test_gh_api_does_not_treat_issue_url_429_as_rate_limit() -> None:
    result = _Result()
    result.returncode = 1
    result.stdout = ""
    result.stderr = "lookup failed: https://github.com/o/r/issues/429"
    with patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=result):
        with pytest.raises(RuntimeError, match="GitHub API error"):
            _gh_api("/repos/o/r")


def test_gh_api_read_uses_selected_pool_credential_and_updates_rest_budget() -> None:
    credential = ReadCredential("NOEKVIST_EXT_SWICA_CLASSIC_REPO_WORKFLOW_PAT", "pool-token", "pool-user")
    pool = Mock()
    pool.repo = "o/r"
    selection_calls: list[tuple[str, set[str]]] = []

    def select(resource: str, *, excluded: set[str]) -> ReadCredential:
        selection_calls.append((resource, set(excluded)))
        return credential

    pool.select.side_effect = select
    pool.default_is_active = False
    pool.default_token = "default-token"
    pool.default_identity = "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"
    result = _Result()
    result.stdout = "HTTP/1.1 200 OK\nX-RateLimit-Remaining: 38\n\n{}"

    with (
        patch.dict(
            "os.environ",
            {
                "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "default-token",
                "GH_TOKEN": "default-token",
                "AI_PR_LOOP_CREDENTIAL_IDENTITY": "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT",
            },
            clear=False,
        ),
        patch("agentic_devtools.cli.ci.github_provider._get_read_token_pool", return_value=pool),
        patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=result) as run_safe,
    ):
        assert _gh_api("/repos/o/r") == "{}"

    assert run_safe.call_args.kwargs["env"]["GH_TOKEN"] == "pool-token"
    assert selection_calls == [("rest", set())]
    pool.record_remaining.assert_called_once_with(credential.secret_name, "rest", 38)


def test_gh_api_copies_pooled_response_metadata_to_caller() -> None:
    credential = ReadCredential("NOEKVIST_EXT_SWICA_CLASSIC_REPO_WORKFLOW_PAT", "pool-token", "pool-user")
    pool = Mock()
    pool.repo = "o/r"
    pool.select.return_value = credential
    pool.default_is_active = False
    pool.default_token = "default-token"
    pool.default_identity = "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"
    result = _Result()
    result.stdout = "HTTP/1.1 200 OK\nX-RateLimit-Remaining: 38\n\n{}"
    metadata: dict[str, float | int | None] = {}

    with (
        patch.dict(
            "os.environ",
            {
                "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "default-token",
                "GH_TOKEN": "default-token",
                "AI_PR_LOOP_CREDENTIAL_IDENTITY": "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT",
            },
            clear=False,
        ),
        patch("agentic_devtools.cli.ci.github_provider._get_read_token_pool", return_value=pool),
        patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=result),
    ):
        assert _gh_api("/repos/o/r", response_metadata=metadata) == "{}"

    assert metadata["remaining"] == 38


def test_gh_api_read_fails_over_after_rate_limit() -> None:
    first = ReadCredential("NOEKVIST_EXT_SWICA_CLASSIC_REPO_WORKFLOW_PAT", "first-token", "first")
    second = ReadCredential("CTRUX_EXT_SWICA_CLASSIC_REPO_WORKFLOW_PAT", "second-token", "second")
    pool = Mock()
    pool.repo = "o/r"
    selection_calls: list[tuple[str, set[str]]] = []
    selections = iter([first, second])

    def select(resource: str, *, excluded: set[str]) -> ReadCredential:
        selection_calls.append((resource, set(excluded)))
        return next(selections)

    pool.select.side_effect = select
    pool.default_is_active = False
    pool.default_token = "default-token"
    pool.default_identity = "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"
    limited = _Result()
    limited.returncode = 1
    limited.stdout = "HTTP/1.1 403 Forbidden\nRetry-After: 45\nX-RateLimit-Remaining: 0\n\n"
    success = _Result()

    with (
        patch.dict(
            "os.environ",
            {
                "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "default-token",
                "GH_TOKEN": "default-token",
                "AI_PR_LOOP_CREDENTIAL_IDENTITY": "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT",
            },
            clear=False,
        ),
        patch("agentic_devtools.cli.ci.github_provider._get_read_token_pool", return_value=pool),
        patch("agentic_devtools.cli.ci.github_provider.run_safe", side_effect=[limited, success]) as run_safe,
    ):
        assert _gh_api("/repos/o/r") == "{}"

    assert [call.kwargs["env"]["GH_TOKEN"] for call in run_safe.call_args_list] == [
        "first-token",
        "second-token",
    ]
    pool.mark_rate_limited.assert_called_once()
    pool.record_remaining.assert_any_call(first.secret_name, "rest", 0)
    assert selection_calls == [
        ("rest", set()),
        ("rest", {first.secret_name}),
    ]


def test_gh_api_falls_back_to_healthy_default_after_all_pool_tokens_are_limited() -> None:
    first = ReadCredential("NOEKVIST_EXT_SWICA_CLASSIC_REPO_WORKFLOW_PAT", "first-token", "first")
    second = ReadCredential("CTRUX_EXT_SWICA_CLASSIC_REPO_WORKFLOW_PAT", "second-token", "second")
    pool = Mock()
    pool.repo = "o/r"
    selections = iter([first, second, None])
    pool.select.side_effect = lambda _resource, *, excluded: next(selections)
    pool.default_is_active = False
    pool.default_token = "default-token"
    pool.default_identity = "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"
    limited = _Result()
    limited.returncode = 1
    limited.stdout = "HTTP/1.1 403 Forbidden\nRetry-After: 45\nX-RateLimit-Remaining: 0\n\n"

    with (
        patch.dict(
            "os.environ",
            {
                "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "default-token",
                "GH_TOKEN": "default-token",
                "AI_PR_LOOP_CREDENTIAL_IDENTITY": "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT",
            },
            clear=False,
        ),
        patch("agentic_devtools.cli.ci.github_provider._get_read_token_pool", return_value=pool),
        patch(
            "agentic_devtools.cli.ci.github_provider.run_safe",
            side_effect=[limited, limited, _Result()],
        ) as run_safe,
    ):
        assert _gh_api("/repos/o/r") == "{}"

    assert [call.kwargs["env"]["GH_TOKEN"] for call in run_safe.call_args_list] == [
        "first-token",
        "second-token",
        "default-token",
    ]


def test_gh_api_read_falls_back_to_default_when_pool_is_empty() -> None:
    pool = Mock()
    pool.repo = "o/r"
    pool.select.return_value = None
    pool.default_is_active = False
    pool.default_token = "default-token"
    pool.default_identity = "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"

    with (
        patch.dict(
            "os.environ",
            {
                "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "default-token",
                "GH_TOKEN": "default-token",
                "AI_PR_LOOP_CREDENTIAL_IDENTITY": "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT",
            },
            clear=False,
        ),
        patch("agentic_devtools.cli.ci.github_provider._get_read_token_pool", return_value=pool),
        patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=_Result()) as run_safe,
    ):
        _gh_api("/repos/o/r")

    assert run_safe.call_args.kwargs["env"]["GH_TOKEN"] == "default-token"


def test_gh_api_read_does_not_retry_default_when_default_is_on_cooldown() -> None:
    pool = Mock()
    pool.repo = "o/r"
    pool.select.return_value = None
    pool.default_is_active = True
    pool.default_token = "default-token"
    pool.default_identity = "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"

    with (
        patch.dict(
            "os.environ",
            {
                "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "default-token",
                "GH_TOKEN": "default-token",
                "AI_PR_LOOP_CREDENTIAL_IDENTITY": "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT",
            },
            clear=False,
        ),
        patch("agentic_devtools.cli.ci.github_provider._get_read_token_pool", return_value=pool),
        patch("agentic_devtools.cli.ci.github_provider.run_safe") as run_safe,
        pytest.raises(ProviderRateLimitError),
    ):
        _gh_api("/repos/o/r")

    run_safe.assert_not_called()


def test_gh_api_write_keeps_fixed_token_without_pool_selection() -> None:
    pool = Mock()
    result = _Result()

    with (
        patch("agentic_devtools.cli.ci.github_provider._get_read_token_pool", return_value=pool),
        patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=result) as run_safe,
    ):
        _gh_api("/repos/o/r/issues", method="POST", body={"title": "write"}, token="write-token")

    run_safe.assert_called_once()
    assert run_safe.call_args.kwargs["env"]["GH_TOKEN"] == "write-token"
    pool.select.assert_not_called()


def test_gh_api_explicit_nondefault_read_keeps_its_fixed_identity() -> None:
    pool = Mock()
    result = _Result()

    with (
        patch("agentic_devtools.cli.ci.github_provider._get_read_token_pool", return_value=pool),
        patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=result) as run_safe,
    ):
        _gh_api(
            "/user",
            token="copilot-token",
            credential_identity="COPILOT_GITHUB_TOKEN",
        )

    assert run_safe.call_args.kwargs["env"]["GH_TOKEN"] == "copilot-token"
    pool.select.assert_not_called()


def test_gh_api_does_not_use_pool_without_default_token() -> None:
    pool = Mock()
    pool.repo = "o/r"
    pool.default_token = ""
    pool.default_identity = "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"

    with (
        patch("agentic_devtools.cli.ci.github_provider._get_read_token_pool", return_value=pool),
        patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=_Result()) as run_safe,
    ):
        _gh_api("/repos/o/r")

    assert run_safe.call_args.kwargs["env"] is None
    pool.select.assert_not_called()


def test_gh_api_does_not_forward_secrets_json_when_not_pooling() -> None:
    with (
        patch.dict(
            "os.environ",
            {"AGDT_GITHUB_SECRETS_JSON": '{"OTHER_PAT":"do-not-forward"}', "GH_TOKEN": "ambient-token"},
            clear=True,
        ),
        patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=_Result()) as run_safe,
    ):
        _gh_api("/repos/o/r", read_pool=False)

    assert run_safe.call_args.kwargs["env"]["GH_TOKEN"] == "ambient-token"
    assert "AGDT_GITHUB_SECRETS_JSON" not in run_safe.call_args.kwargs["env"]


def test_gh_api_does_not_rotate_an_unrelated_ambient_token() -> None:
    pool = Mock()
    pool.repo = "o/r"
    pool.default_token = "default-token"
    pool.default_identity = "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"

    with (
        patch.dict(
            "os.environ",
            {
                "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "default-token",
                "GH_TOKEN": "copilot-token",
                "AI_PR_LOOP_CREDENTIAL_IDENTITY": "",
            },
            clear=True,
        ),
        patch("agentic_devtools.cli.ci.github_provider._get_read_token_pool", return_value=pool),
        patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=_Result()) as run_safe,
    ):
        _gh_api("/repos/o/r")

    assert run_safe.call_args.kwargs["env"] is None
    pool.select.assert_not_called()
