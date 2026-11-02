"""Tests for _append_to_all_tasks function."""

from unittest.mock import patch

from agentic_devtools.task_state import BackgroundTask, _append_to_all_tasks


class TestAppendToAllTasks:
    """Tests for appending new tasks to the all-tasks file."""

    def test_duplicate_task_is_not_appended(self):
        """An existing task ID is not duplicated in the all-tasks file."""
        task = BackgroundTask.create(command="cmd")

        with (
            patch("agentic_devtools.task_state._load_all_tasks_file", return_value=[task.to_dict()]),
            patch("agentic_devtools.task_state._save_all_tasks_file") as mock_save,
        ):
            _append_to_all_tasks([task])

        assert mock_save.call_args.args[0] == [task.to_dict()]
