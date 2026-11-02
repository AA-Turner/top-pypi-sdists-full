"""Tests for pooled read-only GitHub CLI execution."""

from __future__ import annotations

import subprocess
from collections.abc import Callable
from datetime import UTC, datetime
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci.github_provider import _run_readonly_gh_command
from agentic_devtools.cli.ci.retry import RetryableError


def _completed(
    *,
    returncode: int = 0,
    stdout: str = "",
    stderr: str = "",
) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(["gh"], returncode, stdout, stderr)


def test_runs_direct_command_with_explicit_token_and_removes_secrets_json(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AGDT_GITHUB_SECRETS_JSON", '{"OTHER_PAT":"do-not-forward"}')
    runner = Mock(return_value=_completed(stdout="ok"))
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.github_provider._should_use_read_token_pool",
        lambda **_kwargs: False,
    )

    result = _run_readonly_gh_command(["run", "view"], token="selected-token", runner=runner)

    assert result.stdout == "ok"
    args, kwargs = runner.call_args
    assert args == (["gh", "run", "view"],)
    assert kwargs["shell"] is False
    assert kwargs["env"]["GH_TOKEN"] == "selected-token"
    assert "AGDT_GITHUB_SECRETS_JSON" not in kwargs["env"]


def test_explicit_pool_bypass_keeps_identity_lookup_on_fixed_token(monkeypatch: pytest.MonkeyPatch) -> None:
    runner = Mock(return_value=_completed(stdout='{"login":"writer"}'))
    should_use_pool = Mock(return_value=True)
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.github_provider._should_use_read_token_pool",
        should_use_pool,
    )

    result = _run_readonly_gh_command(
        ["api", "user"],
        token="fixed-token",
        credential_identity="DEFAULT_CLASSIC_REPO_WORKFLOW_PAT",
        read_pool=False,
        runner=runner,
    )

    assert result.stdout == '{"login":"writer"}'
    should_use_pool.assert_called_once_with(
        token="fixed-token",
        credential_identity="DEFAULT_CLASSIC_REPO_WORKFLOW_PAT",
        read_pool=False,
        target_repository=None,
    )
    assert runner.call_args.kwargs["env"]["GH_TOKEN"] == "fixed-token"


@pytest.mark.parametrize(
    "arguments",
    [
        ["run", "view", "--repo", "owner/private"],
        [
            "api",
            "graphql",
            "-F",
            "query=query { repository(owner: $owner, name: $repo) { id } }",
            "-F",
            "owner=owner",
            "-F",
            "repo=private",
        ],
    ],
)
def test_cross_repository_command_keeps_the_default_token(
    monkeypatch: pytest.MonkeyPatch,
    arguments: list[str],
) -> None:
    monkeypatch.setenv("GITHUB_REPOSITORY", "owner/current")
    monkeypatch.setenv("GH_TOKEN", "default-token")
    monkeypatch.setenv("AGDT_GITHUB_SECRETS_JSON", '{"ALTERNATE_PAT":"alternate-token"}')
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
    runner = Mock(return_value=_completed(stdout="ok"))

    result = _run_readonly_gh_command(arguments, runner=runner)

    assert result.stdout == "ok"
    assert runner.call_args.kwargs["env"]["GH_TOKEN"] == "default-token"


def test_runs_direct_command_without_constructing_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    runner = Mock(return_value=_completed(stdout="ok"))
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.github_provider._should_use_read_token_pool",
        lambda **_kwargs: False,
    )

    _run_readonly_gh_command(["workflow", "list"], runner=runner)

    assert runner.call_args.kwargs["env"] is None


def test_removes_secrets_json_when_no_token_is_selected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AGDT_GITHUB_SECRETS_JSON", '{"OTHER_PAT":"do-not-forward"}')
    runner = Mock(return_value=_completed(stdout="ok"))
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.github_provider._should_use_read_token_pool",
        lambda **_kwargs: False,
    )

    _run_readonly_gh_command(["workflow", "list"], runner=runner)

    assert "AGDT_GITHUB_SECRETS_JSON" not in runner.call_args.kwargs["env"]


def test_runs_with_pooled_token_and_records_rest_headers(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AGDT_GITHUB_SECRETS_JSON", '{"OTHER_PAT":"do-not-forward"}')
    runner = Mock(
        return_value=_completed(
            stdout="HTTP/2 200\r\nx-ratelimit-remaining: 73\r\n\r\n[]",
        )
    )
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.github_provider._should_use_read_token_pool",
        lambda **_kwargs: True,
    )
    observed: dict[str, object] = {}

    def invoke(
        resource: str,
        operation: Callable[
            [str | None, str],
            tuple[subprocess.CompletedProcess[str], int | None],
        ],
    ) -> subprocess.CompletedProcess[str]:
        observed["resource"] = resource
        result, remaining = operation("alternate-token", "TEAM_PAT")
        observed["remaining"] = remaining
        return result

    monkeypatch.setattr("agentic_devtools.cli.ci.github_provider._call_with_read_token_pool", invoke)

    result = _run_readonly_gh_command(["api", "repos/o/r/issues", "--include"], runner=runner)

    assert result.returncode == 0
    assert observed == {"resource": "rest", "remaining": 73}
    assert runner.call_args.kwargs["env"]["GH_TOKEN"] == "alternate-token"
    assert "AGDT_GITHUB_SECRETS_JSON" not in runner.call_args.kwargs["env"]


@pytest.mark.parametrize(
    ("stdout", "stderr", "remaining"),
    [
        ("HTTP/2 429\r\nx-ratelimit-remaining: 0\r\n\r\n{}", "", 0),
        ("", "HTTP 429: API rate limit exceeded", None),
    ],
)
def test_pooled_rate_limit_raises_identity_scoped_retryable_error(
    monkeypatch: pytest.MonkeyPatch,
    stdout: str,
    stderr: str,
    remaining: int | None,
) -> None:
    runner = Mock(return_value=_completed(returncode=1, stdout=stdout, stderr=stderr))
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.github_provider._should_use_read_token_pool",
        lambda **_kwargs: True,
    )

    def invoke(
        resource: str,
        operation: Callable[
            [str | None, str],
            tuple[subprocess.CompletedProcess[str], int | None],
        ],
    ) -> subprocess.CompletedProcess[str]:
        assert resource == "rest"
        result, _ = operation("alternate-token", "TEAM_PAT")
        return result

    monkeypatch.setattr("agentic_devtools.cli.ci.github_provider._call_with_read_token_pool", invoke)

    with pytest.raises(RetryableError) as raised:
        _run_readonly_gh_command(["api", "repos/o/r/issues", "--include"], runner=runner)

    assert raised.value.is_rate_limit
    assert raised.value.credential_identity == "TEAM_PAT"
    assert raised.value.provider == "github"
    assert raised.value.remaining == remaining


def test_pooled_rate_limit_preserves_http_date_retry_after(monkeypatch: pytest.MonkeyPatch) -> None:
    from agentic_devtools.cli.ci import github_provider

    runner = Mock(
        return_value=_completed(
            returncode=1,
            stdout=(
                "HTTP/2 403 Forbidden\r\n"
                "retry-after: Thu, 01 Jan 1970 02:30:00 GMT\r\n"
                "\r\n"
                '{"message":"You have exceeded a secondary rate limit."}'
            ),
        )
    )
    monkeypatch.setattr(
        github_provider,
        "datetime",
        Mock(now=Mock(return_value=datetime.fromtimestamp(1000, UTC))),
    )
    monkeypatch.setattr(
        github_provider,
        "_should_use_read_token_pool",
        lambda **_kwargs: True,
    )

    def invoke(
        resource: str,
        operation: Callable[
            [str | None, str],
            tuple[subprocess.CompletedProcess[str], int | None],
        ],
    ) -> subprocess.CompletedProcess[str]:
        assert resource == "rest"
        result, _ = operation("alternate-token", "TEAM_PAT")
        return result

    monkeypatch.setattr(github_provider, "_call_with_read_token_pool", invoke)

    with pytest.raises(RetryableError) as raised:
        _run_readonly_gh_command(["api", "repos/o/r/issues", "--include"], runner=runner)

    assert raised.value.is_rate_limit
    assert raised.value.retry_after == 8000
    assert raised.value.reset_timestamp is None
    assert raised.value.credential_identity == "TEAM_PAT"


def test_pooled_graphql_command_uses_graphql_budget_and_preserves_non_rate_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = Mock(return_value=_completed(returncode=1, stderr="permission denied"))
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.github_provider._should_use_read_token_pool",
        lambda **_kwargs: True,
    )
    observed: dict[str, object] = {}

    def invoke(
        resource: str,
        operation: Callable[
            [str | None, str],
            tuple[subprocess.CompletedProcess[str], int | None],
        ],
    ) -> subprocess.CompletedProcess[str]:
        observed["resource"] = resource
        result, remaining = operation("alternate-token", "TEAM_PAT")
        observed["remaining"] = remaining
        return result

    monkeypatch.setattr("agentic_devtools.cli.ci.github_provider._call_with_read_token_pool", invoke)

    result = _run_readonly_gh_command(
        ["api", "graphql", "--include"],
        resource="graphql",
        runner=runner,
    )

    assert result.stderr == "permission denied"
    assert observed == {"resource": "graphql", "remaining": None}


def test_returns_rate_limit_result_when_requested_without_pool(monkeypatch: pytest.MonkeyPatch) -> None:
    runner = Mock(return_value=_completed(returncode=1, stderr="HTTP 403: API rate limit exceeded"))
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.github_provider._should_use_read_token_pool",
        lambda **_kwargs: False,
    )

    result = _run_readonly_gh_command(
        ["api", "repos/o/r/issues"],
        return_rate_limit_result=True,
        runner=runner,
    )

    assert result.returncode == 1
    assert result.stderr == "HTTP 403: API rate limit exceeded"


def test_returns_graphql_rate_limit_payload_when_requested_without_pool(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = '{"errors":[{"type":"RATE_LIMITED","message":"rate limit exceeded"}]}'
    runner = Mock(return_value=_completed(stdout=payload))
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.github_provider._should_use_read_token_pool",
        lambda **_kwargs: False,
    )

    result = _run_readonly_gh_command(
        ["api", "graphql"],
        resource="graphql",
        return_rate_limit_result=True,
        runner=runner,
    )

    assert result.returncode == 0
    assert result.stdout == payload


def test_reset_header_and_positive_remaining_do_not_mark_forbidden_as_rate_limited(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = Mock(
        return_value=_completed(
            returncode=1,
            stdout=("HTTP/2 403 Forbidden\r\nx-ratelimit-reset: 2000000000\r\nx-ratelimit-remaining: 52\r\n\r\n"),
            stderr="resource not accessible by integration",
        )
    )
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.github_provider._should_use_read_token_pool",
        lambda **_kwargs: True,
    )

    def invoke(
        _resource: str,
        operation: Callable[
            [str | None, str],
            tuple[subprocess.CompletedProcess[str], int | None],
        ],
    ) -> subprocess.CompletedProcess[str]:
        result, remaining = operation("alternate-token", "TEAM_PAT")
        assert remaining == 52
        return result

    monkeypatch.setattr("agentic_devtools.cli.ci.github_provider._call_with_read_token_pool", invoke)

    result = _run_readonly_gh_command(["api", "repos/o/r", "--include"], runner=runner)

    assert result.returncode == 1


def test_secondary_rate_limit_in_response_body_triggers_pool_failover(monkeypatch: pytest.MonkeyPatch) -> None:
    runner = Mock(
        return_value=_completed(
            returncode=1,
            stdout=(
                "HTTP/2 403 Forbidden\r\n"
                "x-ratelimit-remaining: 42\r\n\r\n"
                '{"message":"You have exceeded a secondary rate limit."}'
            ),
        )
    )
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.github_provider._should_use_read_token_pool",
        lambda **_kwargs: True,
    )

    def invoke(
        _resource: str,
        operation: Callable[
            [str | None, str],
            tuple[subprocess.CompletedProcess[str], int | None],
        ],
    ) -> subprocess.CompletedProcess[str]:
        result, _ = operation("alternate-token", "TEAM_PAT")
        return result

    monkeypatch.setattr("agentic_devtools.cli.ci.github_provider._call_with_read_token_pool", invoke)

    with pytest.raises(RetryableError) as raised:
        _run_readonly_gh_command(["api", "repos/o/r", "--include"], runner=runner)

    assert raised.value.is_rate_limit
    assert raised.value.credential_identity == "TEAM_PAT"
    assert raised.value.remaining == 42


@pytest.mark.parametrize("timeout", [0, -1, True, "60"])
def test_rejects_invalid_timeout(timeout: object) -> None:
    with pytest.raises(ValueError, match="timeout_seconds"):
        _run_readonly_gh_command(["run", "view"], timeout_seconds=timeout)  # type: ignore[arg-type]


def test_rejects_invalid_resource() -> None:
    with pytest.raises(ValueError, match="resource"):
        _run_readonly_gh_command(["run", "view"], resource="write")
