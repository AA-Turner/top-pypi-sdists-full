import json
import unittest
from unittest.mock import MagicMock, patch

from abstra_internals.controllers.main import MainController


def _make_controller():
    """Create a MainController mock with real methods bound for unit testing."""
    controller = MagicMock()

    # Bind the real methods we want to test
    controller.run_tasklet = MainController.run_tasklet.__get__(controller)
    controller.run_job = MainController.run_job.__get__(controller)

    return controller


def _make_conn(execution_id="exec-123"):
    """Create a mock connection that returns an execution:started message."""
    conn = MagicMock()
    conn.recv.return_value = json.dumps({"executionId": execution_id})
    return conn


class TestRunTaskletLogForwarding(unittest.TestCase):
    @patch("abstra_internals.controllers.main.WORKER_LOG_TO_QUEUE", False)
    def test_run_tasklet_without_flag_closes_conn(self):
        """With flag off, conn.close() is called after recv — original behavior."""
        controller = _make_controller()
        controller.get_script.return_value = MagicMock()

        conn = _make_conn()
        controller.repositories.producer.enqueue.return_value = conn

        result = controller.run_tasklet("stage-1", "task-1")

        self.assertTrue(result["ok"])
        self.assertEqual(result["execution_id"], "exec-123")
        conn.close.assert_called_once()
        controller.repositories.producer.consume_and_forward.assert_not_called()

    @patch("abstra_internals.controllers.main.WORKER_LOG_TO_QUEUE", True)
    def test_run_tasklet_with_flag_hands_off_to_consumer(self):
        """With flag on, consume_and_forward is called and conn.close() is NOT called directly."""
        controller = _make_controller()
        controller.get_script.return_value = MagicMock()

        conn = _make_conn()
        controller.repositories.producer.enqueue.return_value = conn

        result = controller.run_tasklet("stage-1", "task-1")

        self.assertTrue(result["ok"])
        self.assertEqual(result["execution_id"], "exec-123")
        conn.close.assert_not_called()
        controller.repositories.producer.consume_and_forward.assert_called_once_with(
            conn, "stage-1"
        )

    @patch("abstra_internals.controllers.main.WORKER_LOG_TO_QUEUE", True)
    @patch(
        "abstra_internals.controllers.execution.execution_stdio.BroadcastController",
    )
    def test_run_tasklet_with_flag_broadcasts_execution_update(self, MockBroadcast):
        """With flag on, an execution:update is broadcast immediately for the frontend."""
        controller = _make_controller()
        controller._broadcast_execution_update = (
            MainController._broadcast_execution_update.__get__(controller)
        )
        controller.get_script.return_value = MagicMock()

        conn = _make_conn("exec-456")
        controller.repositories.producer.enqueue.return_value = conn

        result = controller.run_tasklet("stage-1", "task-1")

        self.assertEqual(result["execution_id"], "exec-456")

        MockBroadcast.broadcast.assert_called_once()
        broadcast_msg = json.loads(MockBroadcast.broadcast.call_args[1]["msg"])
        self.assertEqual(broadcast_msg["type"], "execution:update")
        self.assertEqual(broadcast_msg["payload"]["execution_id"], "exec-456")

    @patch("abstra_internals.controllers.main.WORKER_LOG_TO_QUEUE", False)
    def test_run_tasklet_recv_error_closes_conn(self):
        """If conn.recv() fails, connection is still closed in finally."""
        controller = _make_controller()
        controller.get_script.return_value = MagicMock()

        conn = MagicMock()
        conn.recv.side_effect = Exception("Connection lost")
        controller.repositories.producer.enqueue.return_value = conn

        with self.assertRaises(Exception):
            controller.run_tasklet("stage-1", "task-1")

        conn.close.assert_called_once()


class TestRunJobLogForwarding(unittest.TestCase):
    @patch("abstra_internals.controllers.main.WORKER_LOG_TO_QUEUE", False)
    def test_run_job_without_flag_closes_conn(self):
        """With flag off, conn.close() is called after recv — original behavior."""
        controller = _make_controller()
        controller.get_job_status.return_value = "enabled"

        conn = _make_conn()
        controller.repositories.producer.enqueue.return_value = conn

        result = controller.run_job("job-1")

        self.assertTrue(result["ok"])
        self.assertEqual(result["execution_id"], "exec-123")
        conn.close.assert_called_once()
        controller.repositories.producer.consume_and_forward.assert_not_called()

    @patch("abstra_internals.controllers.main.WORKER_LOG_TO_QUEUE", True)
    def test_run_job_with_flag_hands_off_to_consumer(self):
        """With flag on, consume_and_forward is called and conn.close() is NOT called directly."""
        controller = _make_controller()
        controller.get_job_status.return_value = "enabled"

        conn = _make_conn()
        controller.repositories.producer.enqueue.return_value = conn

        result = controller.run_job("job-1")

        self.assertTrue(result["ok"])
        self.assertEqual(result["execution_id"], "exec-123")
        conn.close.assert_not_called()
        controller.repositories.producer.consume_and_forward.assert_called_once_with(
            conn, "job-1"
        )


class TestProducerInterfaceHasConsumeAndForward(unittest.TestCase):
    def test_consume_and_forward_is_public_method(self):
        """ProducerRepository base class must expose consume_and_forward."""
        from abstra_internals.repositories.producer import ProducerRepository

        self.assertTrue(hasattr(ProducerRepository, "consume_and_forward"))
        self.assertTrue(callable(getattr(ProducerRepository, "consume_and_forward")))


def _make_mock_conn(messages):
    """Create a mock connection that returns messages sequentially from poll/recv."""
    mock_conn = MagicMock()
    remaining = list(messages)

    def poll_side_effect(timeout=0.0):
        if not remaining:
            return False
        return True

    def recv_side_effect(*args, **kwargs):
        if not remaining:
            raise EOFError("No more messages")
        return remaining.pop(0)

    mock_conn.poll.side_effect = poll_side_effect
    mock_conn.recv.side_effect = recv_side_effect
    type(mock_conn).closed = property(lambda self: False)
    return mock_conn


class TestConsumeAndForwardBroadcastOnEnded(unittest.TestCase):
    """Test that consume_and_forward broadcasts execution:update when execution:ended arrives."""

    @patch(
        "abstra_internals.controllers.execution.execution_stdio.BroadcastController",
    )
    def test_execution_ended_with_id_broadcasts_execution_update(self, MockBroadcast):
        """When execution:ended has execution_id, consume_and_forward should broadcast execution:update.
        stdio is NOT broadcast here (fanout consumer handles it)."""
        import time

        from abstra_internals.repositories.producer import RabbitMQProducerRepository

        repo = RabbitMQProducerRepository.__new__(RabbitMQProducerRepository)

        stdio_msg = {"type": "stdio", "payload": {"type": "stdout", "log": "hello"}}
        ended_msg = json.dumps({"type": "execution:ended", "execution_id": "exec-789"})
        mock_conn = _make_mock_conn([stdio_msg, ended_msg])

        repo.consume_and_forward(mock_conn, "stage-1")
        time.sleep(0.5)

        # 1 broadcast: only execution:update (stdio is handled by fanout consumer)
        self.assertEqual(MockBroadcast.broadcast.call_count, 1)

        msg1 = json.loads(MockBroadcast.broadcast.call_args_list[0][1]["msg"])
        self.assertEqual(msg1["type"], "execution:update")
        self.assertEqual(msg1["payload"]["execution_id"], "exec-789")

        mock_conn.close.assert_called()


if __name__ == "__main__":
    unittest.main()
