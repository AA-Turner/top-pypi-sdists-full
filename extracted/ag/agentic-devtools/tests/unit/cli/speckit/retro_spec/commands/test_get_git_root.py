"""Tests for _get_git_root in retro_spec/commands.py."""

from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.speckit.retro_spec.commands import _get_git_root

_MOD = "agentic_devtools.cli.speckit.retro_spec.commands"


class TestGetGitRoot:
    """Tests for the _get_git_root helper function."""

    def test_returns_path_when_git_succeeds(self) -> None:
        """Test that the repo root is returned when git exits cleanly."""
        fake_result = subprocess.CompletedProcess([], 0, "/repo/root\n", "")
        with patch(f"{_MOD}.subprocess.run", return_value=fake_result):
            result = _get_git_root()
        assert result == Path("/repo/root")

    def test_returns_none_when_git_fails(self) -> None:
        """Test that None is returned when git exits with a non-zero code."""
        fake_result = subprocess.CompletedProcess([], 128, "", "not a git repo")
        with patch(f"{_MOD}.subprocess.run", return_value=fake_result):
            result = _get_git_root()
        assert result is None

    def test_returns_none_when_git_raises_oserror(self) -> None:
        """Test that None is returned when git executable cannot be invoked."""
        with patch(f"{_MOD}.subprocess.run", side_effect=OSError("git missing")):
            result = _get_git_root()
        assert result is None
