"""Tests for reading removed source content."""

from subprocess import CompletedProcess
from unittest.mock import patch

import pytest

from agentic_devtools.cli.checks.changed_files import _removed_python_lines


@pytest.mark.parametrize("failure", [OSError(), CompletedProcess([], 1, "")])
def test_unavailable_patch_is_empty(tmp_path, failure):
    with patch("agentic_devtools.cli.checks.changed_files.subprocess.run") as run:
        if isinstance(failure, OSError):
            run.side_effect = failure
        else:
            run.return_value = failure
        assert _removed_python_lines(["git", "diff"], "HEAD~1..HEAD", "old.py", tmp_path) == set()


def test_only_removed_content_is_used(tmp_path):
    with patch("agentic_devtools.cli.checks.changed_files.subprocess.run") as run:
        run.return_value = CompletedProcess([], 0, "--- a/old.py\n+++ b/old.py\n-old()\n+new()\n context\n")
        assert _removed_python_lines(["git", "diff"], "HEAD~1..HEAD", "old.py", tmp_path) == {"old()"}
