"""Tests for _run_tests_and_wait function."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.release.commands import _run_tests_and_wait
from agentic_devtools.cli.release.helpers import ReleaseError
from agentic_devtools.task_state import TaskStatus


class TestRunTestsAndWait:
    """Tests for _run_tests_and_wait function."""

    def test_returns_zero_on_success(self):
        """Should return 0 when tests pass."""
        mock_task = MagicMock()
        mock_task.id = "test-task-1"

        completed_task = MagicMock()
        completed_task.status = TaskStatus.COMPLETED
        completed_task.exit_code = 0

        with patch(
            "agentic_devtools.cli.release.commands.run_function_in_background",
            return_value=mock_task,
        ):
            with patch(
                "agentic_devtools.cli.release.commands.get_task_by_id",
                return_value=completed_task,
            ):
                with patch("time.sleep"):
                    result = _run_tests_and_wait(timeout_seconds=10)

        assert result == 0

    def test_returns_exit_code_on_failure(self):
        """Should return exit code when tests fail."""
        mock_task = MagicMock()
        mock_task.id = "test-task-2"

        failed_task = MagicMock()
        failed_task.status = TaskStatus.FAILED
        failed_task.exit_code = 1

        with patch(
            "agentic_devtools.cli.release.commands.run_function_in_background",
            return_value=mock_task,
        ):
            with patch(
                "agentic_devtools.cli.release.commands.get_task_by_id",
                return_value=failed_task,
            ):
                with patch("time.sleep"):
                    result = _run_tests_and_wait(timeout_seconds=10)

        assert result == 1

    def test_returns_one_when_exit_code_is_none(self):
        """Should return 1 when exit code is None (unexpected termination)."""
        mock_task = MagicMock()
        mock_task.id = "test-task-3"

        failed_task = MagicMock()
        failed_task.status = TaskStatus.FAILED
        failed_task.exit_code = None

        with patch(
            "agentic_devtools.cli.release.commands.run_function_in_background",
            return_value=mock_task,
        ):
            with patch(
                "agentic_devtools.cli.release.commands.get_task_by_id",
                return_value=failed_task,
            ):
                with patch("time.sleep"):
                    result = _run_tests_and_wait(timeout_seconds=10)

        assert result == 1

    def test_raises_on_timeout(self):
        """Should raise ReleaseError when timeout is reached."""
        mock_task = MagicMock()
        mock_task.id = "test-task-4"

        running_task = MagicMock()
        running_task.status = TaskStatus.RUNNING
        running_task.exit_code = None

        with patch(
            "agentic_devtools.cli.release.commands.run_function_in_background",
            return_value=mock_task,
        ):
            with patch(
                "agentic_devtools.cli.release.commands.get_task_by_id",
                return_value=running_task,
            ):
                with patch("time.sleep"):
                    with patch("time.time", side_effect=[0, 0, 100]):
                        with pytest.raises(ReleaseError, match="timed out"):
                            _run_tests_and_wait(timeout_seconds=1)
