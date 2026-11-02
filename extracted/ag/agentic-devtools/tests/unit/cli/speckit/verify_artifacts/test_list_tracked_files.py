"""Tests for ``list_tracked_files()``."""

import subprocess
from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.speckit.verify_artifacts import list_tracked_files


class TestListTrackedFiles:
    """Building the tracked-path index used to resolve references."""

    def test_returns_tracked_paths_from_git(self, tmp_path: Path) -> None:
        completed = subprocess.CompletedProcess(args=[], returncode=0, stdout="a/b.py\0c.md\0", stderr="")
        with patch(
            "agentic_devtools.cli.speckit.verify_artifacts.subprocess.run",
            return_value=completed,
        ):
            assert list_tracked_files(tmp_path) == ("a/b.py", "c.md")

    def test_drops_trailing_empty_entry(self, tmp_path: Path) -> None:
        completed = subprocess.CompletedProcess(args=[], returncode=0, stdout="only.py\0", stderr="")
        with patch(
            "agentic_devtools.cli.speckit.verify_artifacts.subprocess.run",
            return_value=completed,
        ):
            assert list_tracked_files(tmp_path) == ("only.py",)

    def test_returns_empty_tuple_when_git_fails(self, tmp_path: Path) -> None:
        completed = subprocess.CompletedProcess(args=[], returncode=128, stdout="", stderr="fatal")
        with patch(
            "agentic_devtools.cli.speckit.verify_artifacts.subprocess.run",
            return_value=completed,
        ):
            assert list_tracked_files(tmp_path) == ()

    def test_returns_empty_tuple_when_git_is_unavailable(self, tmp_path: Path) -> None:
        with patch(
            "agentic_devtools.cli.speckit.verify_artifacts.subprocess.run",
            side_effect=OSError("git not found"),
        ):
            assert list_tracked_files(tmp_path) == ()

    def test_invokes_git_without_a_shell(self, tmp_path: Path) -> None:
        completed = subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")
        with patch(
            "agentic_devtools.cli.speckit.verify_artifacts.subprocess.run",
            return_value=completed,
        ) as mock_run:
            list_tracked_files(tmp_path)

        assert mock_run.call_args.kwargs["shell"] is False
        assert mock_run.call_args.args[0] == ["git", "-C", str(tmp_path), "ls-files", "-z"]
