import unittest
from unittest.mock import MagicMock, patch

from abstra_internals.controllers.execution.consumer import ConsumerController
from abstra_internals.controllers.execution.executor_pool import ExecutorDiedError
from abstra_internals.entities.execution_context import JobContext
from abstra_internals.repositories.consumer import QueueMessage
from abstra_internals.repositories.models import PreExecution


def _make_queue_message(redelivered: bool = False) -> QueueMessage:
    preexecution = PreExecution(
        execution_id="11111111-1111-1111-1111-111111111111",
        stage_id="abcdef12",
        context=JobContext(),
    )
    return QueueMessage(
        preexecution=preexecution,
        delivery_tag=42,
        redelivered=redelivered,
    )


class _NonLocalProducer:
    pass


class _ConsumerControllerHarness:
    def __init__(self) -> None:
        self.consumer = MagicMock()
        self.control_consumer = MagicMock()
        self.executor_pool = MagicMock()
        self.main_controller = MagicMock()
        self.main_controller.get_stage.return_value = MagicMock(type_name="form")
        self.main_controller.repositories.producer = _NonLocalProducer()

        self.controller = ConsumerController.__new__(ConsumerController)
        self.controller.consumer = self.consumer
        self.controller.control_consumer = self.control_consumer
        self.controller.executor_pool = self.executor_pool
        self.controller.main_controller = self.main_controller
        self.controller.worker_id = "test-worker"


class TestExecutorDiedRetry(unittest.TestCase):
    @patch(
        "abstra_internals.controllers.execution.consumer.RABBITMQ_CONNECTION_URI",
        "amqp://localhost",
    )
    def test_first_death_requeues_without_failing(self) -> None:
        harness = _ConsumerControllerHarness()
        harness.executor_pool.execute.side_effect = ExecutorDiedError(
            "Executor abc-123 died unexpectedly during execution"
        )
        msg = _make_queue_message(redelivered=False)

        harness.controller.run_subprocess(msg)

        harness.consumer.threadsafe_nack.assert_called_once_with(msg, requeue=True)
        harness.consumer.threadsafe_ack.assert_not_called()
        harness.main_controller.fail_execution.assert_not_called()

    @patch(
        "abstra_internals.controllers.execution.consumer.RABBITMQ_CONNECTION_URI",
        "amqp://localhost",
    )
    def test_redelivered_marks_failed_without_rerunning(self) -> None:
        harness = _ConsumerControllerHarness()
        msg = _make_queue_message(redelivered=True)

        harness.controller.run_subprocess(msg)

        harness.executor_pool.execute.assert_not_called()
        harness.main_controller.fail_execution.assert_called_once()
        call_kwargs = harness.main_controller.fail_execution.call_args.kwargs
        self.assertEqual(call_kwargs["execution_id"], msg.preexecution.execution_id)
        self.assertIn("previous delivery", call_kwargs["reason"])
        harness.consumer.threadsafe_ack.assert_called_once_with(msg)
        harness.consumer.threadsafe_nack.assert_not_called()

    @patch(
        "abstra_internals.controllers.execution.consumer.RABBITMQ_CONNECTION_URI",
        "amqp://localhost",
    )
    def test_redelivered_ack_failure_does_not_double_fail(self) -> None:
        harness = _ConsumerControllerHarness()
        harness.consumer.threadsafe_ack.side_effect = Exception("broker gone")
        msg = _make_queue_message(redelivered=True)

        with self.assertRaises(Exception):
            harness.controller.run_subprocess(msg)

        harness.executor_pool.execute.assert_not_called()
        harness.main_controller.fail_execution.assert_called_once()
        harness.consumer.threadsafe_nack.assert_not_called()

    @patch(
        "abstra_internals.controllers.execution.consumer.RABBITMQ_CONNECTION_URI",
        "amqp://localhost",
    )
    def test_redelivered_db_failure_still_acks(self) -> None:
        harness = _ConsumerControllerHarness()
        harness.main_controller.fail_execution.side_effect = Exception("DB down")
        msg = _make_queue_message(redelivered=True)

        harness.controller.run_subprocess(msg)

        harness.main_controller.fail_execution.assert_called_once()
        harness.consumer.threadsafe_ack.assert_called_once_with(msg)
        harness.consumer.threadsafe_nack.assert_not_called()

    @patch(
        "abstra_internals.controllers.execution.consumer.RABBITMQ_CONNECTION_URI",
        "amqp://localhost",
    )
    def test_other_exception_still_fails_and_acks(self) -> None:
        harness = _ConsumerControllerHarness()
        harness.executor_pool.execute.side_effect = TimeoutError(
            "Execution timed out after 7200s"
        )
        msg = _make_queue_message(redelivered=False)

        harness.controller.run_subprocess(msg)

        harness.main_controller.fail_execution.assert_called_once()
        harness.consumer.threadsafe_ack.assert_called_once_with(msg)
        harness.consumer.threadsafe_nack.assert_not_called()


class TestFailExecutionResilience(unittest.TestCase):
    @patch("abstra_internals.controllers.main.AbstraLogger")
    def test_marks_failed_even_when_get_raises(self, mock_logger: MagicMock) -> None:
        from abstra_internals.controllers.main import MainController

        controller = MainController.__new__(MainController)
        controller.execution_repository = MagicMock()
        controller.execution_repository.get.side_effect = NotImplementedError
        controller.execution_logs_repository = MagicMock()
        controller.tasks_repository = MagicMock()

        controller.fail_execution(execution_id="e1", reason="boom")

        controller.execution_logs_repository.save.assert_not_called()
        mock_logger.capture_exception.assert_called_once()
        controller.execution_repository.set_failure_by_id.assert_called_once_with(
            execution_id="e1"
        )
        controller.tasks_repository.set_locked_tasks_to_pending.assert_called_once_with(
            "e1"
        )


class TestQueueMessageRedeliveredDefault(unittest.TestCase):
    def test_redelivered_defaults_to_false(self) -> None:
        msg = _make_queue_message()
        self.assertFalse(msg.redelivered)


if __name__ == "__main__":
    unittest.main()
