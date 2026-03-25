import unittest
from multiprocessing import Queue
from unittest.mock import MagicMock, patch

from abstra_internals.controllers.execution.executor_process import (
    ExecutorState,
    _validate_session_queues,
    handle_execute,
)
from abstra_internals.controllers.execution.executor_types import (
    ExecuteRequest,
    ExecutorCommand,
    RabbitMQParams,
)

VALID_UUID = "550e8400-e29b-41d4-a716-446655440000"


class TestValidateSessionQueues(unittest.TestCase):
    """Tests for queue name validation."""

    def test_valid_queues(self):
        """Valid session queue names should not raise."""
        _validate_session_queues(
            f"session_s2w_{VALID_UUID}",
            f"session_w2s_{VALID_UUID}",
            VALID_UUID,
        )

    def test_invalid_queue_name_format(self):
        """Arbitrary queue names should be rejected."""
        with self.assertRaises(ValueError) as ctx:
            _validate_session_queues(
                "arbitrary_queue_name",
                f"session_w2s_{VALID_UUID}",
                VALID_UUID,
            )
        self.assertIn("Invalid session queue name", str(ctx.exception))

    def test_execution_id_mismatch(self):
        """Queue with different UUID than execution_id should be rejected."""
        other_uuid = "00000000-0000-0000-0000-000000000001"
        with self.assertRaises(ValueError) as ctx:
            _validate_session_queues(
                f"session_s2w_{other_uuid}",
                f"session_w2s_{VALID_UUID}",
                VALID_UUID,
            )
        self.assertIn("mismatch", str(ctx.exception))

    def test_system_queue_rejected(self):
        """RabbitMQ system queue names should be rejected."""
        with self.assertRaises(ValueError):
            _validate_session_queues(
                "amq.rabbitmq.reply-to",
                f"session_w2s_{VALID_UUID}",
                VALID_UUID,
            )

    def test_queue_expire_ms_low_value_kept(self):
        """queue_expire_ms below 60_000 should be kept (cloud-api is authoritative)."""
        params = RabbitMQParams(
            connection_uri="amqp://localhost",
            execution_id=VALID_UUID,
            send_queue=f"session_s2w_{VALID_UUID}",
            recv_queue=f"session_w2s_{VALID_UUID}",
            queue_expire_ms=1000,
        )
        self.assertEqual(params.queue_expire_ms, 1000)

    def test_queue_expire_ms_high_value_kept(self):
        """queue_expire_ms above 86_400_000 should be kept (cloud-api is authoritative)."""
        params = RabbitMQParams(
            connection_uri="amqp://localhost",
            execution_id=VALID_UUID,
            queue_expire_ms=100_000_000,
        )
        self.assertEqual(params.queue_expire_ms, 100_000_000)


class TestHandleExecuteSessionQueues(unittest.TestCase):
    """Tests for session queue name inversion in handle_execute."""

    @patch(
        "abstra_internals.controllers.execution.executor_process.WORKER_LOG_TO_QUEUE",
        False,
    )
    @patch("abstra_internals.controllers.execution.executor_process.RabbitMQConnection")
    @patch("abstra_internals.controllers.execution.executor_process.StdioPatcher")
    @patch(
        "abstra_internals.controllers.execution.executor_process.ExecutionController"
    )
    def test_session_queues_inverted(self, mock_exec_ctrl, mock_patcher, mock_rmq_conn):
        """When send_queue and recv_queue are provided, worker inverts the perspective."""
        mock_rmq = MagicMock()
        mock_rmq.execution_id = VALID_UUID
        mock_rmq_conn.return_value = mock_rmq

        state = ExecutorState(verbose=False)
        state.warmup_complete = True
        state.controller = MagicMock()

        request = ExecuteRequest(
            command=ExecutorCommand.EXECUTE,
            worker_id="w1",
            execution_id=VALID_UUID,
            stage=MagicMock(),
            request=MagicMock(),
            connection=None,
            rabbitmq_params=RabbitMQParams(
                connection_uri="amqp://localhost",
                execution_id=VALID_UUID,
                send_queue=f"session_s2w_{VALID_UUID}",
                recv_queue=f"session_w2s_{VALID_UUID}",
            ),
        )

        response_queue = Queue()
        handle_execute(state, request, response_queue, "/tmp", 8080)

        # RabbitMQConnection should be called with inverted queues and is_session=True
        mock_rmq_conn.assert_called_once()
        kwargs = mock_rmq_conn.call_args.kwargs
        # Worker's send_queue = cloud-api's recv_queue (session_w2s_*)
        self.assertEqual(kwargs["send_queue"], f"session_w2s_{VALID_UUID}")
        # Worker's recv_queue = cloud-api's send_queue (session_s2w_*)
        self.assertEqual(kwargs["recv_queue"], f"session_s2w_{VALID_UUID}")
        self.assertTrue(kwargs["is_session"])

    @patch(
        "abstra_internals.controllers.execution.executor_process.WORKER_LOG_TO_QUEUE",
        False,
    )
    @patch("abstra_internals.controllers.execution.executor_process.RabbitMQConnection")
    @patch("abstra_internals.controllers.execution.executor_process.StdioPatcher")
    @patch(
        "abstra_internals.controllers.execution.executor_process.ExecutionController"
    )
    def test_legacy_queues_when_no_session_fields(
        self, mock_exec_ctrl, mock_patcher, mock_rmq_conn
    ):
        """Without send_queue/recv_queue, worker uses legacy queue names."""
        legacy_id = "exec-456"
        mock_rmq = MagicMock()
        mock_rmq.execution_id = legacy_id
        mock_rmq_conn.return_value = mock_rmq

        state = ExecutorState(verbose=False)
        state.warmup_complete = True
        state.controller = MagicMock()

        request = ExecuteRequest(
            command=ExecutorCommand.EXECUTE,
            worker_id="w1",
            execution_id=legacy_id,
            stage=MagicMock(),
            request=MagicMock(),
            connection=None,
            rabbitmq_params=RabbitMQParams(
                connection_uri="amqp://localhost",
                execution_id=legacy_id,
                # No send_queue/recv_queue — legacy mode
            ),
        )

        response_queue = Queue()
        handle_execute(state, request, response_queue, "/tmp", 8080)

        mock_rmq_conn.assert_called_once()
        kwargs = mock_rmq_conn.call_args.kwargs
        self.assertEqual(kwargs["send_queue"], f"worker_to_server_{legacy_id}")
        self.assertEqual(kwargs["recv_queue"], f"server_to_worker_{legacy_id}")
        self.assertFalse(kwargs["is_session"])

    @patch(
        "abstra_internals.controllers.execution.executor_process.WORKER_LOG_TO_QUEUE",
        False,
    )
    @patch("abstra_internals.controllers.execution.executor_process.RabbitMQConnection")
    @patch("abstra_internals.controllers.execution.executor_process.StdioPatcher")
    @patch(
        "abstra_internals.controllers.execution.executor_process.ExecutionController"
    )
    def test_partial_session_fields_fallback_to_legacy(
        self, mock_exec_ctrl, mock_patcher, mock_rmq_conn
    ):
        """If only one of send_queue/recv_queue is set, fall back to legacy mode."""
        mock_rmq = MagicMock()
        mock_rmq.execution_id = VALID_UUID
        mock_rmq_conn.return_value = mock_rmq

        state = ExecutorState(verbose=False)
        state.warmup_complete = True
        state.controller = MagicMock()

        request = ExecuteRequest(
            command=ExecutorCommand.EXECUTE,
            worker_id="w1",
            execution_id=VALID_UUID,
            stage=MagicMock(),
            request=MagicMock(),
            connection=None,
            rabbitmq_params=RabbitMQParams(
                connection_uri="amqp://localhost",
                execution_id=VALID_UUID,
                send_queue=f"session_s2w_{VALID_UUID}",
                recv_queue=None,  # Only one provided
            ),
        )

        response_queue = Queue()
        handle_execute(state, request, response_queue, "/tmp", 8080)

        mock_rmq_conn.assert_called_once()
        kwargs = mock_rmq_conn.call_args.kwargs
        # Should fall back to legacy names
        self.assertEqual(kwargs["send_queue"], f"worker_to_server_{VALID_UUID}")
        self.assertEqual(kwargs["recv_queue"], f"server_to_worker_{VALID_UUID}")
        self.assertFalse(kwargs["is_session"])

    @patch(
        "abstra_internals.controllers.execution.executor_process.WORKER_LOG_TO_QUEUE",
        False,
    )
    @patch("abstra_internals.controllers.execution.executor_process.RabbitMQConnection")
    @patch("abstra_internals.controllers.execution.executor_process.StdioPatcher")
    @patch(
        "abstra_internals.controllers.execution.executor_process.ExecutionController"
    )
    def test_invalid_queue_name_fails_execution(
        self, mock_exec_ctrl, mock_patcher, mock_rmq_conn
    ):
        """Invalid queue names should fail the execution with error response."""
        state = ExecutorState(verbose=False)
        state.warmup_complete = True
        state.controller = MagicMock()

        request = ExecuteRequest(
            command=ExecutorCommand.EXECUTE,
            worker_id="w1",
            execution_id=VALID_UUID,
            stage=MagicMock(),
            request=MagicMock(),
            connection=None,
            rabbitmq_params=RabbitMQParams(
                connection_uri="amqp://localhost",
                execution_id=VALID_UUID,
                send_queue="malicious_queue",
                recv_queue=f"session_w2s_{VALID_UUID}",
            ),
        )

        response_queue = Queue()
        handle_execute(state, request, response_queue, "/tmp", 8080)

        response = response_queue.get(timeout=1.0)
        self.assertFalse(response.success)
        self.assertIn("Invalid session queue name", response.error)


if __name__ == "__main__":
    unittest.main()
