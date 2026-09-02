"""Tests for ``_repo_slug_from_gh``."""

import subprocess
from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.speckit.scaffold_new_feature import _repo_slug_from_gh


class TestRepoSlugFromGh:
    """_repo_slug_from_gh returns an owner/repo slug via the GitHub CLI."""

    def test_returns_none_on_oserror(self, tmp_path: Path) -> None:
        with patch("subprocess.run", side_effect=OSError("gh not found")):
            assert _repo_slug_from_gh(tmp_path) is None

    def test_returns_none_on_timeout(self, tmp_path: Path) -> None:
        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("gh", 10)):
            assert _repo_slug_from_gh(tmp_path) is None

    def test_returns_none_on_nonzero_exit(self, tmp_path: Path) -> None:
        result = type("Completed", (), {"stdout": "", "returncode": 1})()
        with patch("subprocess.run", return_value=result):
            assert _repo_slug_from_gh(tmp_path) is None

    def test_returns_normalized_slug_on_success(self, tmp_path: Path) -> None:
        result = type("Completed", (), {"stdout": "owner/repo\n", "returncode": 0})()
        with patch("subprocess.run", return_value=result):
            assert _repo_slug_from_gh(tmp_path) == "owner/repo"
