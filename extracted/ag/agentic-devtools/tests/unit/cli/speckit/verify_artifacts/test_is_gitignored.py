"""Tests for ``is_gitignored()``."""

import subprocess
from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.speckit.verify_artifacts import is_gitignored


class TestIsGitignored:
    """``git check-ignore --quiet`` decides whether a file is committable."""

    def test_returns_false_when_git_returns_nonzero(self, tmp_path: Path) -> None:
        p = tmp_path / "file.txt"
        completed = subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="")
        with patch(
            "agentic_devtools.cli.speckit.verify_artifacts.subprocess.run",
            return_value=completed,
        ):
            assert is_gitignored(p) is False

    def test_returns_true_when_git_returns_zero(self, tmp_path: Path) -> None:
        p = tmp_path / "research.md"
        completed = subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")
        with patch(
            "agentic_devtools.cli.speckit.verify_artifacts.subprocess.run",
            return_value=completed,
        ):
            assert is_gitignored(p) is True

    def test_returns_false_when_git_is_unavailable(self, tmp_path: Path) -> None:
        p = tmp_path / "file.txt"
        with patch(
            "agentic_devtools.cli.speckit.verify_artifacts.subprocess.run",
            side_effect=OSError("git not found"),
        ):
            assert is_gitignored(p) is False

    def test_invokes_git_check_ignore_without_shell(self, tmp_path: Path) -> None:
        p = tmp_path / "file.txt"
        completed = subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="")
        with patch(
            "agentic_devtools.cli.speckit.verify_artifacts.subprocess.run",
            return_value=completed,
        ) as mock_run:
            is_gitignored(p)

        assert mock_run.call_args.kwargs["shell"] is False
        assert mock_run.call_args.args[0] == [
            "git",
            "-C",
            str(tmp_path),
            "check-ignore",
            "--quiet",
            str(p),
        ]
