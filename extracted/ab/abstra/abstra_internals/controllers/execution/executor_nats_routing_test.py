"""Tests for NATS vs RabbitMQ routing in handle_execute.

Exercises handle_execute directly (not a re-implemented predicate) so
that changes to the production routing logic break CI.
"""

from multiprocessing import Queue
from typing import Optional
from unittest import TestCase
from unittest.mock import MagicMock, patch

from abstra_internals.controllers.execution.executor_process import (
    ExecutorState,
    handle_execute,
)
from abstra_internals.controllers.execution.executor_types import (
    ExecuteRequest,
    ExecutorCommand,
    RabbitMQParams,
)


def _make_state() -> ExecutorState:
    state = ExecutorState(verbose=False)
    state.warmup_complete = True
    state.controller = MagicMock()
    return state


def _make_request(stage_type: str, rabbitmq_params=True) -> ExecuteRequest:
    stage = MagicMock()
    stage.type_name = stage_type
    return ExecuteRequest(
        command=ExecutorCommand.EXECUTE,
        worker_id="worker-1",
        execution_id="exec-123",
        stage=stage,
        request=MagicMock(),
        connection=MagicMock(),
        rabbitmq_params=RabbitMQParams(
            connection_uri="amqp://localhost",
            execution_id="exec-123",
        )
        if rabbitmq_params
        else None,
    )


# Patches applied to every test: prevent real connections and execution
_COMMON_PATCHES = {
    "nats_conn_cls": "abstra_internals.controllers.execution.executor_process.NATSConnection",
    "nats_persistent_cls": "abstra_internals.controllers.execution.executor_process.NATSPersistentConnection",
    "rmq_conn_cls": "abstra_internals.controllers.execution.executor_process.RabbitMQConnection",
    "exec_controller": "abstra_internals.controllers.execution.executor_process.ExecutionController",
    "stdio_patcher": "abstra_internals.controllers.execution.executor_process.StdioPatcher",
    "set_exec_conn": "abstra_internals.controllers.execution.executor_process.set_execution_conn",
    "set_broadcast": "abstra_internals.controllers.execution.executor_process.set_broadcast_publisher",
}


class TestHandleExecuteNATSRouting(TestCase):
    """Exercises handle_execute and checks which connection type is instantiated."""

    def _run(
        self,
        stage_type: str,
        nats_url: Optional[str] = "nats://host",
        nats_creds: Optional[str] = "creds",
        rabbitmq_params: bool = True,
    ):
        """Call handle_execute with the given config and return (mock_nats_conn, mock_rmq_conn)."""
        state = _make_state()
        request = _make_request(stage_type, rabbitmq_params=rabbitmq_params)
        response_queue = Queue()

        patches = {k: patch(v) for k, v in _COMMON_PATCHES.items()}
        mocks = {k: p.start() for k, p in patches.items()}

        # Make the execution controller's run() a no-op
        mocks["exec_controller"].return_value.run = MagicMock()

        env_patches = {
            "abstra_internals.controllers.execution.executor_process.NATS_URL": nats_url,
            "abstra_internals.controllers.execution.executor_process.NATS_CREDS": nats_creds,
            "abstra_internals.controllers.execution.executor_process.WORKER_LOG_TO_QUEUE": False,
        }
        env_mocks = {k: patch(k, v) for k, v in env_patches.items()}
        for p in env_mocks.values():
            p.start()

        try:
            handle_execute(state, request, response_queue, "/tmp", 8080)
        finally:
            for p in patches.values():
                p.stop()
            for p in env_mocks.values():
                p.stop()

        return mocks["nats_conn_cls"], mocks["rmq_conn_cls"], response_queue

    def test_hook_uses_nats(self):
        nats_cls, rmq_cls, _ = self._run("hook")
        nats_cls.assert_called_once()
        rmq_cls.assert_not_called()

    def test_page_uses_nats(self):
        nats_cls, rmq_cls, _ = self._run("page")
        nats_cls.assert_called_once()
        rmq_cls.assert_not_called()

    def test_job_uses_nats(self):
        nats_cls, rmq_cls, _ = self._run("job")
        nats_cls.assert_called_once()
        rmq_cls.assert_not_called()

    def test_form_uses_rabbitmq(self):
        nats_cls, rmq_cls, _ = self._run("form")
        nats_cls.assert_not_called()
        rmq_cls.assert_called_once()

    def test_no_nats_url_uses_rabbitmq(self):
        nats_cls, rmq_cls, _ = self._run("hook", nats_url=None)
        nats_cls.assert_not_called()
        rmq_cls.assert_called_once()

    def test_no_nats_creds_uses_rabbitmq(self):
        nats_cls, rmq_cls, _ = self._run("hook", nats_creds=None)
        nats_cls.assert_not_called()
        rmq_cls.assert_called_once()

    def test_empty_nats_url_uses_rabbitmq(self):
        nats_cls, rmq_cls, _ = self._run("hook", nats_url="")
        nats_cls.assert_not_called()
        rmq_cls.assert_called_once()

    def test_no_rabbitmq_params_uses_request_connection(self):
        """When rabbitmq_params is None, neither NATS nor RabbitMQ is created."""
        nats_cls, rmq_cls, _ = self._run("hook", rabbitmq_params=False)
        nats_cls.assert_not_called()
        rmq_cls.assert_not_called()

    def test_nats_subjects_use_correct_directions(self):
        """Worker sends on w2s, receives on s2w."""
        nats_cls, _, _ = self._run("hook")
        call_kwargs = nats_cls.call_args
        self.assertEqual(call_kwargs.kwargs["send_subject"], "exec-123.w2s")
        self.assertEqual(call_kwargs.kwargs["recv_subject"], "exec-123.s2w")

    def test_execution_succeeds_with_nats(self):
        _, _, response_queue = self._run("hook")
        response = response_queue.get(timeout=5)
        self.assertTrue(response.success)

    def test_execution_succeeds_with_rabbitmq(self):
        _, _, response_queue = self._run("form")
        response = response_queue.get(timeout=5)
        self.assertTrue(response.success)


class TestPersistentConnectionRecovery(TestCase):
    """Tests that the persistent connection lifecycle works correctly."""

    def test_state_starts_without_persistent(self):
        state = ExecutorState()
        self.assertIsNone(state.nats_persistent)

    def test_nats_connection_reuses_persistent_when_alive(self):
        from abstra_internals.utils.nats_connection import NATSConnection

        mock_persistent = MagicMock()
        mock_persistent.is_alive = True

        with patch.object(NATSConnection, "_setup_subscription"):
            conn = NATSConnection(
                nats_url="nats://host",
                nats_creds="creds",
                send_subject="exec.s2w",
                recv_subject="exec.w2s",
                execution_id="exec-123",
                persistent=mock_persistent,
            )
            self.assertFalse(conn._owns_connection)
            self.assertIs(conn._persistent, mock_persistent)

    def test_nats_connection_creates_own_when_persistent_dead(self):
        mock_persistent = MagicMock()
        mock_persistent.is_alive = False

        with patch(
            "abstra_internals.utils.nats_connection.NATSPersistentConnection"
        ) as MockNew:
            mock_new = MagicMock()
            mock_new.is_alive = True
            MockNew.return_value = mock_new

            from abstra_internals.utils.nats_connection import NATSConnection

            with patch.object(NATSConnection, "_setup_subscription"):
                conn = NATSConnection(
                    nats_url="nats://host",
                    nats_creds="creds",
                    send_subject="exec.s2w",
                    recv_subject="exec.w2s",
                    execution_id="exec-123",
                    persistent=mock_persistent,
                )
                self.assertTrue(conn._owns_connection)
                MockNew.assert_called_once()

    def test_nats_connection_creates_own_when_persistent_none(self):
        with patch(
            "abstra_internals.utils.nats_connection.NATSPersistentConnection"
        ) as MockNew:
            mock_new = MagicMock()
            mock_new.is_alive = True
            MockNew.return_value = mock_new

            from abstra_internals.utils.nats_connection import NATSConnection

            with patch.object(NATSConnection, "_setup_subscription"):
                conn = NATSConnection(
                    nats_url="nats://host",
                    nats_creds="creds",
                    send_subject="exec.s2w",
                    recv_subject="exec.w2s",
                    execution_id="exec-123",
                    persistent=None,
                )
                self.assertTrue(conn._owns_connection)
                MockNew.assert_called_once()
