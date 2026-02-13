import unittest
from unittest.mock import MagicMock, patch

from abstra_internals.controllers.execution.execution_conn import set_execution_conn
from abstra_internals.repositories.tasks import LocalTasksRepository


class TestTasksBroadcast(unittest.TestCase):
    def setUp(self):
        with patch.object(LocalTasksRepository, "__init__", lambda self: None):
            self.repo = LocalTasksRepository()
        self.repo.fs_storage = MagicMock()

    def tearDown(self):
        set_execution_conn(None)

    @patch(
        "abstra_internals.repositories.tasks.WORKER_LOG_TO_QUEUE",
        False,
    )
    def test_send_task_without_flag_does_not_broadcast(self):
        mock_conn = MagicMock()
        set_execution_conn(mock_conn)

        self.repo.fs_storage.save = MagicMock()

        self.repo.send_task(
            type="test-task",
            payload={"data": "value"},
            target_stage_id="stage-1",
            source_stage_id="stage-0",
            execution_id="exec-1",
        )

        mock_conn.send.assert_not_called()

    @patch(
        "abstra_internals.repositories.tasks.WORKER_LOG_TO_QUEUE",
        True,
    )
    def test_send_task_with_flag_broadcasts_task_dto(self):
        mock_conn = MagicMock()
        set_execution_conn(mock_conn)

        self.repo.fs_storage.save = MagicMock()

        self.repo.send_task(
            type="test-task",
            payload={"data": "value"},
            target_stage_id="stage-1",
            source_stage_id="stage-0",
            execution_id="exec-1",
        )

        mock_conn.send.assert_called_once()
        msg = mock_conn.send.call_args[0][0]
        self.assertEqual(msg["type"], "task")
        self.assertEqual(msg["payload"]["type"], "test-task")
        self.assertEqual(msg["payload"]["status"], "pending")
        self.assertEqual(msg["payload"]["targetStageId"], "stage-1")

    @patch(
        "abstra_internals.repositories.tasks.WORKER_LOG_TO_QUEUE",
        True,
    )
    def test_lock_task_broadcasts_updated_task(self):
        mock_conn = MagicMock()
        set_execution_conn(mock_conn)

        self.repo.fs_storage.save = MagicMock()

        task = self.repo.send_task(
            type="test-task",
            payload={},
            target_stage_id="stage-1",
            source_stage_id=None,
            execution_id=None,
        )
        mock_conn.reset_mock()

        # Mock get() to return the task we just created
        self.repo.fs_storage.load = MagicMock(return_value=task)

        self.repo.lock_task(task.id, execution_id="exec-2", stage_id="stage-1")

        mock_conn.send.assert_called_once()
        msg = mock_conn.send.call_args[0][0]
        self.assertEqual(msg["type"], "task")
        self.assertEqual(msg["payload"]["status"], "locked")

    @patch(
        "abstra_internals.repositories.tasks.WORKER_LOG_TO_QUEUE",
        True,
    )
    def test_complete_task_broadcasts_updated_task(self):
        mock_conn = MagicMock()
        set_execution_conn(mock_conn)

        self.repo.fs_storage.save = MagicMock()

        task = self.repo.send_task(
            type="test-task",
            payload={},
            target_stage_id="stage-1",
            source_stage_id=None,
            execution_id=None,
        )
        mock_conn.reset_mock()

        # Lock first (required for complete)
        self.repo.fs_storage.load = MagicMock(return_value=task)
        self.repo.lock_task(task.id, execution_id="exec-2", stage_id="stage-1")
        mock_conn.reset_mock()

        self.repo.fs_storage.load = MagicMock(return_value=task)
        self.repo.complete_task(task.id, execution_id="exec-2", stage_id="stage-1")

        mock_conn.send.assert_called_once()
        msg = mock_conn.send.call_args[0][0]
        self.assertEqual(msg["type"], "task")
        self.assertEqual(msg["payload"]["status"], "completed")

    @patch(
        "abstra_internals.repositories.tasks.WORKER_LOG_TO_QUEUE",
        True,
    )
    def test_broadcast_error_does_not_affect_persistence(self):
        mock_conn = MagicMock()
        mock_conn.send.side_effect = Exception("RabbitMQ down")
        set_execution_conn(mock_conn)

        self.repo.fs_storage.save = MagicMock()

        # Should not raise
        self.repo.send_task(
            type="test-task",
            payload={"data": "value"},
            target_stage_id="stage-1",
            source_stage_id=None,
            execution_id=None,
        )

        # fs_storage.save was still called
        self.repo.fs_storage.save.assert_called_once()


if __name__ == "__main__":
    unittest.main()
