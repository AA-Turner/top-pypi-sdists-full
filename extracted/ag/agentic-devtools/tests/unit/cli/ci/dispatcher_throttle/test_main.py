"""Tests for the dispatcher throttle command entry point."""

from __future__ import annotations

import subprocess
from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci import dispatcher_throttle
from agentic_devtools.cli.ci.dispatcher_throttle import main


@pytest.mark.parametrize(
    ("repository", "output_path"),
    [(None, None), ("swai-factory/agentic-devtools", None), (None, "/tmp/github-output")],
)
def test_main_requires_github_repository_and_output(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    repository: str | None,
    output_path: str | None,
) -> None:
    if repository is None:
        monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
    else:
        monkeypatch.setenv("GITHUB_REPOSITORY", repository)
    if output_path is None:
        monkeypatch.delenv("GITHUB_OUTPUT", raising=False)
    else:
        monkeypatch.setenv("GITHUB_OUTPUT", output_path)

    with pytest.raises(SystemExit) as exc_info:
        main(["--default-branch", "main"])

    assert exc_info.value.code == 1
    assert "GITHUB_REPOSITORY and GITHUB_OUTPUT must be set" in capsys.readouterr().err


def test_main_runs_the_throttle_check(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    output_path = tmp_path / "github-output"
    monkeypatch.setenv("GITHUB_REPOSITORY", "swai-factory/agentic-devtools")
    monkeypatch.setenv("GITHUB_OUTPUT", str(output_path))
    monkeypatch.setattr(dispatcher_throttle.DispatcherThrottle, "check", lambda self, **kwargs: False)

    main(["--default-branch", "main"])

    assert not output_path.exists()


@pytest.mark.parametrize("error", [OSError("gh missing"), RuntimeError("lookup failed"), ValueError("bad repo")])
def test_main_reports_command_errors(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    tmp_path,
) -> None:
    monkeypatch.setenv("GITHUB_REPOSITORY", "swai-factory/agentic-devtools")
    monkeypatch.setenv("GITHUB_OUTPUT", str(tmp_path / "github-output"))
    monkeypatch.setattr(
        dispatcher_throttle.DispatcherThrottle,
        "check",
        lambda self, **kwargs: (_ for _ in ()).throw(error),
    )

    with pytest.raises(SystemExit) as exc_info:
        main(["--default-branch", "main"])

    assert exc_info.value.code == 1
    assert str(error) in capsys.readouterr().err


def test_main_reports_retry_exhaustion_without_writing_success_output(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    tmp_path,
) -> None:
    output_path = tmp_path / "github-output"
    run = Mock(return_value=subprocess.CompletedProcess(["gh"], 0, stdout=b" \n", stderr=b"< HTTP/2.0 200 OK\n"))
    monkeypatch.setenv("GITHUB_REPOSITORY", "swai-factory/agentic-devtools")
    monkeypatch.setenv("GITHUB_OUTPUT", str(output_path))
    monkeypatch.setattr(dispatcher_throttle, "run_safe", run)
    monkeypatch.setattr(dispatcher_throttle.time, "sleep", lambda _delay: None)
    monkeypatch.setattr(dispatcher_throttle.time, "time", lambda: 1000)

    with pytest.raises(SystemExit) as exc_info:
        main(["--default-branch", "main"])

    assert exc_info.value.code == 1
    assert "throttle state is unknown" in capsys.readouterr().err
    assert run.call_count == dispatcher_throttle.MAX_ATTEMPTS
    assert not output_path.exists()


def test_main_requires_default_branch(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main([])

    assert exc_info.value.code == 2
    assert "--default-branch" in capsys.readouterr().err
