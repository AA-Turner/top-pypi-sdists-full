"""Tests for the _run_gh_text symbol."""

from __future__ import annotations

import subprocess
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.supervision_control_command import _run_gh_text


def test_run_gh_text_returns_stripped_stdout_and_uses_default_writer_token(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "fixed-writer-token")
    monkeypatch.setenv("GH_TOKEN", "ambient-token")
    with patch(
        "agentic_devtools.cli.ci.supervision_control_command.run_safe",
        return_value=SimpleNamespace(returncode=0, stdout="  result\n", stderr=""),
    ) as run_safe:
        assert _run_gh_text(["issue", "create"]) == "result"

    assert run_safe.call_args.kwargs["shell"] is False
    assert run_safe.call_args.kwargs["env"]["GH_TOKEN"] == "fixed-writer-token"


def test_run_gh_text_preserves_an_explicit_writer_environment() -> None:
    explicit_env = {"GH_TOKEN": "bookkeeping-token"}
    with patch(
        "agentic_devtools.cli.ci.supervision_control_command.run_safe",
        return_value=SimpleNamespace(returncode=0, stdout="result", stderr=""),
    ) as run_safe:
        assert _run_gh_text(["issue", "comment"], env=explicit_env) == "result"

    assert run_safe.call_args.kwargs["env"] is explicit_env


@pytest.mark.parametrize("ambient_token", ["ambient-token", None])
def test_run_gh_text_preserves_local_authentication_when_default_is_missing(
    monkeypatch: pytest.MonkeyPatch,
    ambient_token: str | None,
) -> None:
    monkeypatch.delenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", raising=False)
    if ambient_token is None:
        monkeypatch.delenv("GH_TOKEN", raising=False)
    else:
        monkeypatch.setenv("GH_TOKEN", ambient_token)

    with patch(
        "agentic_devtools.cli.ci.supervision_control_command.run_safe",
        return_value=SimpleNamespace(returncode=0, stdout="result", stderr=""),
    ) as run_safe:
        assert _run_gh_text(["issue", "create"]) == "result"

    call_env = run_safe.call_args.kwargs["env"]
    if ambient_token is None:
        assert "GH_TOKEN" not in call_env
    else:
        assert call_env["GH_TOKEN"] == ambient_token


@pytest.mark.parametrize("failure", [OSError("missing gh"), subprocess.TimeoutExpired("gh", 60)])
def test_run_gh_text_wraps_process_start_and_timeout_errors(
    failure: Exception,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "fixed-writer-token")
    with patch(
        "agentic_devtools.cli.ci.supervision_control_command.run_safe",
        side_effect=failure,
    ):
        with pytest.raises(RuntimeError, match="GitHub CLI operation failed"):
            _run_gh_text(["issue", "create"])


@pytest.mark.parametrize(
    ("stderr", "message"),
    [("denied", "denied"), ("  ", "GitHub CLI operation failed")],
)
def test_run_gh_text_raises_provider_error_from_stderr(
    stderr: str,
    message: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "fixed-writer-token")
    with patch(
        "agentic_devtools.cli.ci.supervision_control_command.run_safe",
        return_value=SimpleNamespace(returncode=1, stdout="", stderr=stderr),
    ):
        with pytest.raises(RuntimeError, match=message):
            _run_gh_text(["issue", "create"])
