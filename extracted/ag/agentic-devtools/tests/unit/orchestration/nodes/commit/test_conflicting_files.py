"""Tests for agentic_devtools.orchestration.nodes.commit._conflicting_files."""

from unittest.mock import MagicMock, patch

from agentic_devtools.orchestration.nodes import commit as commit_mod

_MOD = "agentic_devtools.orchestration.nodes.commit"


def _proc(stdout: str = "", returncode: int = 0, stderr: str = ""):
    return MagicMock(returncode=returncode, stdout=stdout, stderr=stderr)


class TestConflictingFiles:
    def test_parses_non_blank_conflicts(self):
        with patch(f"{_MOD}.run_git_capture", return_value=_proc(stdout="a.py\n\nb.py\n")):
            assert commit_mod._conflicting_files("/wt") == ["a.py", "b.py"]
