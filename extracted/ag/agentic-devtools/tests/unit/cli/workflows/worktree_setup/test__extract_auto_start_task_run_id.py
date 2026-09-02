"""Tests for _extract_auto_start_task_run_id."""

from agentic_devtools.cli.workflows.worktree_setup import (
    _extract_auto_start_task_run_id,
)


class TestExtractAutoStartTaskRunId:
    """Tests for the _extract_auto_start_task_run_id helper."""

    def test_handles_non_task_shapes(self):
        """Run-id extraction returns None for non-dict or malformed args."""
        assert _extract_auto_start_task_run_id("not-a-task") is None
        assert _extract_auto_start_task_run_id({"args": "not-a-list"}) is None
        assert _extract_auto_start_task_run_id({"args": ["--run-id", 123]}) is None
        assert _extract_auto_start_task_run_id({"args": ["--foo", "bar"]}) is None
        assert _extract_auto_start_task_run_id({"args": ["--run-id"]}) is None

    def test_returns_stripped_run_id(self):
        """Run-id extraction returns the trimmed value after --run-id."""
        assert _extract_auto_start_task_run_id({"args": ["--run-id", " run-42 "]}) == "run-42"
