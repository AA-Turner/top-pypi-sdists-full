"""Tests for the _run_gh symbol."""

from __future__ import annotations

import subprocess
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.read_token_pool import ReadCredential
from agentic_devtools.cli.ci.supervision_control_command import _run_gh
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError


def test_run_gh_keeps_user_identity_lookup_on_default_fixed_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "default-token")
    with patch(
        "agentic_devtools.cli.ci.github_provider._run_readonly_gh_command",
        return_value=SimpleNamespace(returncode=0, stdout='{"login":"writer"}', stderr=""),
    ) as run_readonly:
        assert _run_gh(["api", "user"]) == {"login": "writer"}

    assert run_readonly.call_args.args[0] == ["api", "user"]
    assert run_readonly.call_args.kwargs["token"] == "default-token"
    assert run_readonly.call_args.kwargs["read_pool"] is False


def test_run_gh_uses_explicit_environment_without_read_pool() -> None:
    explicit_env = {"GH_TOKEN": "bookkeeping-token"}
    with patch(
        "agentic_devtools.cli.ci.github_provider._run_readonly_gh_command",
        return_value=SimpleNamespace(returncode=0, stdout="{}", stderr=""),
    ) as run_readonly:
        _run_gh(["api", "graphql", "-F", "query=query { viewer { login } }"], env=explicit_env)

    assert run_readonly.call_args.kwargs["base_env"] is explicit_env
    assert run_readonly.call_args.kwargs["read_pool"] is False


def test_run_gh_uses_graphql_budget_for_graphql_api_calls() -> None:
    with patch(
        "agentic_devtools.cli.ci.github_provider._run_readonly_gh_command",
        return_value=SimpleNamespace(returncode=0, stdout="{}", stderr=""),
    ) as run_readonly:
        _run_gh(["api", "graphql", "-F", "query=query { viewer { login } }"])

    assert run_readonly.call_args.kwargs["resource"] == "graphql"


def test_run_gh_fails_over_on_graphql_rate_limit_payload(monkeypatch: pytest.MonkeyPatch) -> None:
    reader = ReadCredential("TEAM_PAT", "alternate-token", "reader")

    class _Pool:
        default_identity = "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"
        default_token = "default-token"
        default_is_active = False
        repo = "owner/repo"

        def __init__(self) -> None:
            self.rate_limited = False

        def select(self, _resource: str, *, excluded: set[str]) -> ReadCredential | None:
            return None if self.rate_limited or reader.secret_name in excluded else reader

        def record_remaining(self, *_args: object) -> None:
            pass

        def mark_rate_limited(self, identity: str, _error: RetryableError) -> None:
            assert identity == reader.secret_name
            self.rate_limited = True

    pool = _Pool()
    monkeypatch.setenv("GITHUB_REPOSITORY", "owner/repo")
    monkeypatch.setenv("GH_TOKEN", "default-token")
    limited = SimpleNamespace(
        returncode=0,
        stdout='{"errors":[{"type":"RATE_LIMITED","message":"rate limit exceeded"}]}',
        stderr="",
    )
    successful = SimpleNamespace(returncode=0, stdout='{"data":{"viewer":{"login":"default"}}}', stderr="")
    with (
        patch("agentic_devtools.cli.ci.github_provider._get_read_token_pool", return_value=pool),
        patch(
            "agentic_devtools.cli.ci.supervision_control_command.run_safe",
            side_effect=[limited, successful],
        ) as run_safe,
    ):
        result = _run_gh(["api", "graphql", "-F", "query=query { viewer { login } }"])

    assert result == {"data": {"viewer": {"login": "default"}}}
    assert pool.rate_limited
    assert [call.kwargs["env"]["GH_TOKEN"] for call in run_safe.call_args_list] == [
        "alternate-token",
        "default-token",
    ]


@pytest.mark.parametrize(
    "arguments",
    [
        ["pr", "view", "7"],
        ["pr", "list"],
        ["issue", "list"],
    ],
)
def test_run_gh_uses_graphql_budget_for_high_level_reads(arguments: list[str]) -> None:
    with patch(
        "agentic_devtools.cli.ci.github_provider._run_readonly_gh_command",
        return_value=SimpleNamespace(returncode=0, stdout="[]", stderr=""),
    ) as run_readonly:
        _run_gh(arguments)

    assert run_readonly.call_args.kwargs["resource"] == "graphql"


def test_run_gh_returns_none_for_empty_stdout() -> None:
    with patch(
        "agentic_devtools.cli.ci.supervision_control_command.run_safe",
        return_value=SimpleNamespace(returncode=0, stdout="  ", stderr=""),
    ) as run_safe:
        assert _run_gh(["issue", "comment"]) is None

    assert run_safe.call_args_list[0].kwargs["shell"] is False


@pytest.mark.parametrize("failure", [OSError("missing gh"), subprocess.TimeoutExpired("gh", 60)])
def test_run_gh_wraps_process_start_and_timeout_errors(failure: Exception, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "default-token")
    with patch(
        "agentic_devtools.cli.ci.supervision_control_command.run_safe",
        side_effect=failure,
    ):
        with pytest.raises(RuntimeError, match="GitHub CLI operation failed"):
            _run_gh(["api", "user"])


@pytest.mark.parametrize(
    "failure",
    [
        RetryableError("temporarily unavailable"),
        ProviderRateLimitError(provider="github", credential_identity="reader"),
    ],
)
def test_run_gh_wraps_pooled_read_errors(failure: Exception) -> None:
    with patch(
        "agentic_devtools.cli.ci.github_provider._run_readonly_gh_command",
        side_effect=failure,
    ):
        with pytest.raises(RuntimeError, match="GitHub CLI operation failed"):
            _run_gh(["pr", "view", "7"])


def test_run_gh_raises_provider_error_from_stderr(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "default-token")
    with patch(
        "agentic_devtools.cli.ci.supervision_control_command.run_safe",
        return_value=SimpleNamespace(returncode=1, stdout="", stderr="denied"),
    ):
        with pytest.raises(RuntimeError, match="denied"):
            _run_gh(["api", "user"])


def test_run_gh_rejects_invalid_json(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "default-token")
    with patch(
        "agentic_devtools.cli.ci.supervision_control_command.run_safe",
        return_value=SimpleNamespace(returncode=0, stdout="not-json", stderr=""),
    ):
        with pytest.raises(RuntimeError, match="invalid JSON"):
            _run_gh(["api", "user"])


@pytest.mark.parametrize("ambient_token", ["ambient-token", None])
def test_run_gh_uses_local_authentication_when_default_token_is_missing(
    monkeypatch: pytest.MonkeyPatch,
    ambient_token: str | None,
) -> None:
    monkeypatch.delenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", raising=False)
    if ambient_token is None:
        monkeypatch.delenv("GH_TOKEN", raising=False)
    else:
        monkeypatch.setenv("GH_TOKEN", ambient_token)

    with patch(
        "agentic_devtools.cli.ci.github_provider._run_readonly_gh_command",
        return_value=SimpleNamespace(returncode=0, stdout='{"login":"local-user"}', stderr=""),
    ) as run_readonly:
        assert _run_gh(["api", "user"]) == {"login": "local-user"}

    assert run_readonly.call_args.kwargs["token"] is None
    assert run_readonly.call_args.kwargs["read_pool"] is False
    assert "credential_identity" not in run_readonly.call_args.kwargs
