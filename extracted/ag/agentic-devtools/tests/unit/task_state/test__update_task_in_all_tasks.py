"""Tests for _update_task_in_all_tasks function."""

from unittest.mock import patch

from agentic_devtools.task_state import (
    BackgroundTask,
    _update_task_in_all_tasks,
    add_task,
    get_all_tasks,
)


class TestUpdateTaskInAllTasks:
    """Tests for _update_task_in_all_tasks function."""

    def test_updates_existing_task(self, tmp_path):
        """Update a task that already exists in the all-tasks file."""
        with (
            patch("agentic_devtools.task_state.get_state_dir", return_value=tmp_path),
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
        ):
            task = BackgroundTask.create(command="agdt-test-cmd")
            add_task(task, use_locking=False)

            # Mark the task as running and update it
            task.mark_running()
            _update_task_in_all_tasks(task)

            # Verify update persisted
            all_tasks = get_all_tasks()
            found = [t for t in all_tasks if t.id == task.id]
            assert len(found) == 1
            assert found[0].status.value == "running"

    def test_updates_task_after_nonmatching_entry(self):
        """Continue scanning the all-tasks file after an unrelated task."""
        first_task = BackgroundTask.create(command="first")
        task = BackgroundTask.create(command="target")
        task.mark_running()

        with (
            patch(
                "agentic_devtools.task_state._load_all_tasks_file",
                return_value=[first_task.to_dict(), task.to_dict()],
            ),
            patch("agentic_devtools.task_state._save_all_tasks_file") as mock_save,
        ):
            _update_task_in_all_tasks(task)

        saved_tasks = mock_save.call_args.args[0]
        assert saved_tasks[1]["status"] == "running"
