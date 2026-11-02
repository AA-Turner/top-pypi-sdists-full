"""Tests for the verifier's Git subprocess wrapper."""

import subprocess
from pathlib import Path
from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci.windows_fixture_bytes import _run_git


def test_run_git_uses_argv_without_a_shell(monkeypatch: pytest.MonkeyPatch) -> None:
    result = subprocess.CompletedProcess([], 0, stdout=b"result", stderr=b"")
    run = Mock(return_value=result)
    monkeypatch.setattr(subprocess, "run", run)

    assert _run_git(Path("/repo"), ["rev-parse", "HEAD"]) == b"result"

    run.assert_called_once_with(
        ["git", "-C", str(Path("/repo")), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        shell=False,
    )


@pytest.mark.parametrize("failure", [OSError("git unavailable"), subprocess.CalledProcessError(2, ["git"])])
def test_run_git_propagates_subprocess_failures(monkeypatch: pytest.MonkeyPatch, failure: Exception) -> None:
    monkeypatch.setattr(subprocess, "run", Mock(side_effect=failure))

    with pytest.raises(type(failure)):
        _run_git(Path("/repo"), ["rev-parse", "HEAD"])
