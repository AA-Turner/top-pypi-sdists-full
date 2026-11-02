"""Budget runner CLI contract."""

import importlib
import os
import signal
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.checks import pre_push_budget


def test_import_without_posix_process_apis(monkeypatch):
    monkeypatch.delattr(os, "killpg", raising=False)
    monkeypatch.delattr(signal, "SIGKILL", raising=False)
    importlib.reload(pre_push_budget)


def test_main_uses_repository_log_and_existing_checks(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("AGDT_PRE_PUSH_BUDGET_SECONDS", "42")
    with patch.object(pre_push_budget, "run_with_budget", return_value=10) as run:
        assert pre_push_budget.main([]) == 10
    run.assert_called_once_with(
        [sys.executable, "-u", "-m", "agentic_devtools.cli.checks", "--format-fix"],
        42,
        Path(pre_push_budget.__file__).resolve().parents[3] / ".pre-push-output.log",
    )


@pytest.mark.parametrize(
    "error",
    [
        OSError("launch/log failed"),
        ValueError("invalid budget"),
        pre_push_budget.subprocess.TimeoutExpired("checks", 1),
    ],
)
def test_main_errors_block_push(error, capsys):
    with patch.object(pre_push_budget, "run_with_budget", side_effect=error):
        assert pre_push_budget.main() == 1
    assert str(error) in capsys.readouterr().err


@pytest.mark.skipif(os.name != "posix", reason="POSIX shell hook dispatch")
@pytest.mark.parametrize(
    ("actions", "override", "cloud", "status"),
    [
        ("true", "", True, 0),
        ("false", "2", True, 7),
        ("TRUE", "", False, 3),
        ("false", "", False, 0),
        ("true", "", True, 10),
        ("", "2", True, 10),
        ("", "", False, 10),
    ],
)
def test_hook_dispatch_and_status(tmp_path, actions, override, cloud, status):
    import subprocess

    root = Path(pre_push_budget.__file__).resolve().parents[3]
    binaries = tmp_path / "bin"
    binaries.mkdir()
    python = binaries / "python"
    python.write_text(f'#!/bin/sh\nprintf "%s\\n" "$*" > "$CALL_LOG"\nexit {status}\n')
    python.chmod(0o755)
    git = binaries / "git"
    git.write_text('#!/bin/sh\nprintf "%s\\n" "$HOOK_ROOT"\n')
    git.chmod(0o755)
    result = subprocess.run(
        ["sh", str(root / ".githooks/pre-push")],
        cwd=tmp_path,
        env={
            **os.environ,
            "PATH": f"{binaries}:{os.environ['PATH']}",
            "GITHUB_ACTIONS": actions,
            "AGDT_PRE_PUSH_BUDGET_SECONDS": override,
            "CALL_LOG": str(tmp_path / "call"),
            "HOOK_ROOT": str(tmp_path),
        },
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == (1 if status == 10 else status)
    invocation = (tmp_path / "call").read_text()
    assert ("agentic_devtools.cli.checks.pre_push_budget" in invocation) == cloud
    if status == 10:
        assert "Files were reformatted by ruff." in result.stdout
        assert "Run agdt-git-save-work" in result.stdout
