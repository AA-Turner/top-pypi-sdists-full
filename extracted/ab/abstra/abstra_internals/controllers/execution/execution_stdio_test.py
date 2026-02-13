import unittest
from unittest.mock import MagicMock, patch

from abstra_internals.controllers.execution.execution_stdio import BroadcastController
from abstra_internals.entities.execution import Execution
from abstra_internals.entities.execution_context import ScriptContext


def _make_broadcast_controller():
    main_controller = MagicMock()
    main_controller.execution_logs_repository = MagicMock()
    main_controller.execution_repository = MagicMock()
    return BroadcastController(
        main_controller=main_controller,
        sys_stdout_write=lambda x: len(x),
        sys_stderr_write=lambda x: len(x),
    )


def _make_execution():
    return Execution.create(
        id="exec-123",
        context=ScriptContext(task_id="task-1"),
        stage_id="stage-456",
        worker_id="worker-1",
    )


class TestSendStdioQueueBroadcast(unittest.TestCase):
    @patch(
        "abstra_internals.controllers.execution.execution_stdio.WORKER_LOG_TO_QUEUE",
        False,
    )
    @patch(
        "abstra_internals.controllers.execution.execution_conn.get_stdio_buffer",
    )
    def test_send_stdio_without_flag_does_not_add_to_buffer(self, mock_get_buffer):
        mock_buffer = MagicMock()
        mock_get_buffer.return_value = mock_buffer

        bc = _make_broadcast_controller()
        execution = _make_execution()

        bc.send_stdio(execution, "stdout", "hello world")

        mock_buffer.add.assert_not_called()

    @patch(
        "abstra_internals.controllers.execution.execution_stdio.WORKER_LOG_TO_QUEUE",
        True,
    )
    @patch(
        "abstra_internals.controllers.execution.execution_conn.get_stdio_buffer",
    )
    def test_send_stdio_with_flag_adds_to_buffer(self, mock_get_buffer):
        mock_buffer = MagicMock()
        mock_get_buffer.return_value = mock_buffer

        bc = _make_broadcast_controller()
        execution = _make_execution()

        bc.send_stdio(execution, "stdout", "hello world")

        mock_buffer.add.assert_called_once()
        msg = mock_buffer.add.call_args[0][0]
        self.assertEqual(msg["type"], "stdout")
        self.assertEqual(msg["log"], "hello world")
        self.assertEqual(msg["execution_id"], "exec-123")
        self.assertEqual(msg["stage_id"], "stage-456")

    @patch(
        "abstra_internals.controllers.execution.execution_stdio.WORKER_LOG_TO_QUEUE",
        True,
    )
    @patch(
        "abstra_internals.controllers.execution.execution_conn.get_stdio_buffer",
        return_value=None,
    )
    def test_send_stdio_with_flag_but_no_buffer_does_not_crash(self, _):
        bc = _make_broadcast_controller()
        execution = _make_execution()

        # Should not raise
        bc.send_stdio(execution, "stdout", "hello world")

    @patch(
        "abstra_internals.controllers.execution.execution_stdio.WORKER_LOG_TO_QUEUE",
        True,
    )
    @patch(
        "abstra_internals.controllers.execution.execution_conn.get_stdio_buffer",
    )
    def test_send_stdio_buffer_error_does_not_break_execution(self, mock_get_buffer):
        mock_buffer = MagicMock()
        mock_buffer.add.side_effect = Exception("Buffer full")
        mock_get_buffer.return_value = mock_buffer

        bc = _make_broadcast_controller()
        execution = _make_execution()

        # Should not raise despite buffer.add() failing
        # (the exception is caught by _handle_stdio's try/except)
        bc.send_stdio(execution, "stderr", "error msg")

    @patch(
        "abstra_internals.controllers.execution.execution_stdio.WORKER_LOG_TO_QUEUE",
        True,
    )
    @patch(
        "abstra_internals.controllers.execution.execution_conn.get_stdio_buffer",
    )
    def test_send_stdio_still_writes_to_repository(self, mock_get_buffer):
        mock_buffer = MagicMock()
        mock_get_buffer.return_value = mock_buffer

        bc = _make_broadcast_controller()
        execution = _make_execution()

        bc.send_stdio(execution, "stdout", "hello")

        bc.execution_logs_repository.insert_stdio.assert_called_once_with(  # type: ignore[union-attr]
            "exec-123", "stage-456", "stdout", "hello"
        )


if __name__ == "__main__":
    unittest.main()
