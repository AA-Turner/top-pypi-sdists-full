import unittest
from multiprocessing import Queue
from unittest.mock import MagicMock, patch

from abstra_internals.controllers.execution.execution_conn import (
    get_broadcast_publisher,
    set_broadcast_publisher,
)
from abstra_internals.controllers.execution.executor_process import (
    ExecuteRequest,
    ExecutorCommand,
    ExecutorState,
    RabbitMQParams,
    handle_execute,
)


class TestHandleExecuteBroadcastPublisher(unittest.TestCase):
    """Tests that handle_execute wires up the broadcast publisher when WORKER_LOG_TO_QUEUE=true."""

    def setUp(self):
        set_broadcast_publisher(None)

    def tearDown(self):
        set_broadcast_publisher(None)

    @patch(
        "abstra_internals.controllers.execution.executor_process.WORKER_LOG_TO_QUEUE",
        True,
    )
    @patch("abstra_internals.controllers.execution.executor_process.RabbitMQConnection")
    @patch("abstra_internals.controllers.execution.executor_process.StdioPatcher")
    @patch(
        "abstra_internals.controllers.execution.executor_process.ExecutionController"
    )
    @patch(
        "abstra_internals.controllers.execution.executor_process.StdioBroadcastPublisher"
    )
    def test_sets_broadcast_publisher_when_flag_on(
        self, mock_publisher_cls, mock_exec_ctrl, mock_patcher, mock_rmq_conn
    ):
        """handle_execute should create and set a broadcast publisher when WORKER_LOG_TO_QUEUE=true."""
        # Setup
        mock_rmq = MagicMock()
        mock_rmq.execution_id = "exec-123"
        mock_rmq_conn.return_value = mock_rmq

        mock_publisher = MagicMock()
        mock_publisher_cls.get_or_create.return_value = mock_publisher

        state = ExecutorState(verbose=False)
        state.warmup_complete = True
        state.controller = MagicMock()

        request = ExecuteRequest(
            command=ExecutorCommand.EXECUTE,
            worker_id="w1",
            execution_id="exec-123",
            stage=MagicMock(),
            request=MagicMock(),
            connection=None,
            rabbitmq_params=RabbitMQParams(
                connection_uri="amqp://localhost", execution_id="exec-123"
            ),
        )

        response_queue = Queue()

        handle_execute(state, request, response_queue, "/tmp", 8080)

        # Publisher should have been created (called in setup + finally for execution:ended)
        mock_publisher_cls.get_or_create.assert_called_with("amqp://localhost")
        self.assertGreaterEqual(mock_publisher_cls.get_or_create.call_count, 1)

    @patch(
        "abstra_internals.controllers.execution.executor_process.WORKER_LOG_TO_QUEUE",
        True,
    )
    @patch("abstra_internals.controllers.execution.executor_process.RabbitMQConnection")
    @patch("abstra_internals.controllers.execution.executor_process.StdioPatcher")
    @patch(
        "abstra_internals.controllers.execution.executor_process.ExecutionController"
    )
    @patch(
        "abstra_internals.controllers.execution.executor_process.StdioBroadcastPublisher"
    )
    def test_clears_broadcast_publisher_in_finally(
        self, mock_publisher_cls, mock_exec_ctrl, mock_patcher, mock_rmq_conn
    ):
        """handle_execute should clear the broadcast publisher in the finally block."""
        mock_rmq = MagicMock()
        mock_rmq.execution_id = "exec-123"
        mock_rmq_conn.return_value = mock_rmq

        mock_publisher = MagicMock()
        mock_publisher_cls.get_or_create.return_value = mock_publisher

        state = ExecutorState(verbose=False)
        state.warmup_complete = True
        state.controller = MagicMock()

        request = ExecuteRequest(
            command=ExecutorCommand.EXECUTE,
            worker_id="w1",
            execution_id="exec-123",
            stage=MagicMock(),
            request=MagicMock(),
            connection=None,
            rabbitmq_params=RabbitMQParams(
                connection_uri="amqp://localhost", execution_id="exec-123"
            ),
        )

        response_queue = Queue()
        handle_execute(state, request, response_queue, "/tmp", 8080)

        # After handle_execute, broadcast publisher should be cleared
        self.assertIsNone(get_broadcast_publisher())

    @patch(
        "abstra_internals.controllers.execution.executor_process.WORKER_LOG_TO_QUEUE",
        False,
    )
    @patch("abstra_internals.controllers.execution.executor_process.RabbitMQConnection")
    @patch("abstra_internals.controllers.execution.executor_process.StdioPatcher")
    @patch(
        "abstra_internals.controllers.execution.executor_process.ExecutionController"
    )
    def test_no_broadcast_publisher_when_flag_off(
        self, mock_exec_ctrl, mock_patcher, mock_rmq_conn
    ):
        """handle_execute should NOT create a broadcast publisher when WORKER_LOG_TO_QUEUE=false."""
        mock_rmq = MagicMock()
        mock_rmq.execution_id = "exec-123"
        mock_rmq_conn.return_value = mock_rmq

        state = ExecutorState(verbose=False)
        state.warmup_complete = True
        state.controller = MagicMock()

        request = ExecuteRequest(
            command=ExecutorCommand.EXECUTE,
            worker_id="w1",
            execution_id="exec-123",
            stage=MagicMock(),
            request=MagicMock(),
            connection=None,
            rabbitmq_params=RabbitMQParams(
                connection_uri="amqp://localhost", execution_id="exec-123"
            ),
        )

        response_queue = Queue()
        handle_execute(state, request, response_queue, "/tmp", 8080)

        # No broadcast publisher should be set
        self.assertIsNone(get_broadcast_publisher())
