"""Tests for resolve_repo_root."""

from pathlib import Path
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.azure_devops.pr_review_manifest import resolve_repo_root

_MODULE = "agentic_devtools.cli.azure_devops.pr_review_manifest"


class TestResolveRepoRoot:
    def test_success(self):
        result = MagicMock(returncode=0, stdout="/repo/root\n")
        with patch(f"{_MODULE}.run_safe", return_value=result):
            assert resolve_repo_root() == "/repo/root"

    def test_nonzero_returncode_falls_back_to_cwd(self):
        result = MagicMock(returncode=1, stdout="")
        with patch(f"{_MODULE}.run_safe", return_value=result):
            with patch.object(Path, "cwd", return_value=Path("/cwd")):
                assert resolve_repo_root() == str(Path("/cwd"))

    def test_zero_returncode_empty_stdout_falls_back(self):
        result = MagicMock(returncode=0, stdout="")
        with patch(f"{_MODULE}.run_safe", return_value=result):
            with patch.object(Path, "cwd", return_value=Path("/cwd")):
                assert resolve_repo_root() == str(Path("/cwd"))

    def test_exception_falls_back_to_cwd(self):
        with patch(f"{_MODULE}.run_safe", side_effect=OSError("boom")):
            with patch.object(Path, "cwd", return_value=Path("/cwd")):
                assert resolve_repo_root() == str(Path("/cwd"))
