import unittest
from unittest.mock import MagicMock, patch

from abstra_internals.controllers.execution.consumer import ConsumerController
from abstra_internals.controllers.execution.executor_pool import (
    ExecutorPoolNotReadyError,
)
from abstra_internals.settings import SettingsController


class NeverReadyPool:
    def __init__(self):
        self.shutdown_called = False

    def start(self):
        pass

    def shutdown(self):
        self.shutdown_called = True

    def can_start_loop(self):
        return False


class TestExecutorPoolNotReady(unittest.TestCase):
    def setUp(self):
        SettingsController.set_root_path("/tmp")
        SettingsController.set_server_port(3000)

        mock_main_controller = MagicMock()
        mock_main_controller.repositories.mp_context.get_context.return_value = (
            MagicMock()
        )
        mock_main_controller.repositories.producer = MagicMock()

        regular_consumer = MagicMock()
        regular_consumer.iter.return_value = []

        self.controller = ConsumerController(mock_main_controller, regular_consumer)
        self.pool = NeverReadyPool()
        self.controller.executor_pool = self.pool

    def test_start_loop_raises_and_shuts_down_pool_when_never_ready(self):
        # Raising (instead of returning) makes the worker process exit
        # non-zero, so the container restart reason is Error, not Completed.
        with patch("time.sleep"):
            with self.assertRaises(ExecutorPoolNotReadyError):
                self.controller.start_loop()

        self.assertTrue(self.pool.shutdown_called)
