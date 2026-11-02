"""Tests for best-effort Python move metadata."""

from subprocess import CompletedProcess
from unittest.mock import patch

import pytest

from agentic_devtools.cli.checks.changed_files import get_python_module_moves

MODULE = "agentic_devtools.cli.checks.changed_files"
OLD = "agentic_devtools/cli/ci/pipeline/session_detector.py"
NEW = "agentic_devtools/cli/ci/agent_task_inventory.py"


@pytest.mark.parametrize("status", [f"R100\0{OLD}\0{NEW}\0", f"D\0{OLD}\0A\0{NEW}\0", f"M\0{OLD}\0A\0{NEW}\0"])
def test_detects_rename_delete_add_and_extraction(status, tmp_path):
    new = tmp_path / NEW
    new.parent.mkdir(parents=True)
    new.write_text("def load_agent_task_inventory():\n    tasks = []\n    return tasks\n", encoding="utf-8")
    removed = "@@ -1,3 +0,0 @@\n-def load_agent_task_inventory():\n-    tasks = []\n-    return tasks\n"
    with patch(f"{MODULE}.subprocess.run") as run:
        run.side_effect = [
            CompletedProcess([], 0, status),
            CompletedProcess([], 0, removed),
        ]
        assert get_python_module_moves(cwd=tmp_path) == [(OLD, NEW)]


@pytest.mark.parametrize("failure", [OSError("no git"), CompletedProcess([], 1, "")])
def test_unavailable_metadata_is_empty(failure, tmp_path):
    with patch(f"{MODULE}.subprocess.run") as run:
        if isinstance(failure, OSError):
            run.side_effect = failure
        else:
            run.return_value = failure
        assert get_python_module_moves(cwd=tmp_path) == []


def test_fallback_uses_successful_revision(tmp_path):
    with patch(f"{MODULE}.subprocess.run") as run:
        run.side_effect = [CompletedProcess([], 1, ""), CompletedProcess([], 0, f"R100\0{OLD}\0{NEW}\0")]
        assert get_python_module_moves(cwd=tmp_path) == [(OLD, NEW)]
        assert "HEAD~10..HEAD" in run.call_args.args[0]
