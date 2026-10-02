"""Unit tests for killstats Celery signals."""

# Standard Library
from unittest.mock import MagicMock, Mock, patch

# Third Party
from celery import signals

# Django
from django.core.cache import cache

# AA Killstats
from killstats import __title__
from killstats import signals as killstats_signals
from killstats.tests import AuthTestCase

MODULE_PATH = "killstats.signals"


class TestWorkerReadyHandler(AuthTestCase):
    @patch(f"{MODULE_PATH}.logger")
    def test_worker_ready_handler_should_clear_shutdown_flag_in_cache(
        self, mock_logger
    ):
        # Test Data
        shutdown_key = f"{__title__.upper()}_WORKER_SHUTDOWN"
        cache.set(shutdown_key, True, timeout=120)
        sender = "celery@worker1"

        # Test Action
        killstats_signals.worker_ready_handler(sender=sender)

        # Expected Result
        self.assertIsNone(cache.get(shutdown_key))
        mock_logger.debug.assert_called_once_with(
            "Worker ready signal successfully processed for %s", sender
        )

    @patch(f"{MODULE_PATH}.cache")
    def test_worker_ready_signal_dispatch_should_call_handler(self, mock_cache):
        # Test Data
        shutdown_key = f"{__title__.upper()}_WORKER_SHUTDOWN"
        sender = "celery@worker2"

        # Test Action
        signals.worker_ready.send(sender=sender)

        # Expected Result
        mock_cache.delete.assert_called_with(shutdown_key)


class TestWorkerShuttingDownHandler(AuthTestCase):
    @patch(f"{MODULE_PATH}.logger")
    def test_worker_shutting_down_handler_should_set_shutdown_flag_in_cache(
        self, mock_logger
    ):
        # Test Data
        shutdown_key = f"{__title__.upper()}_WORKER_SHUTDOWN"
        cache.delete(shutdown_key)
        sender = "celery@worker1"

        # Test Action
        killstats_signals.worker_shutting_down_handler(sender=sender)

        # Expected Result
        self.assertTrue(cache.get(shutdown_key))
        mock_logger.debug.assert_called_once_with(
            "Worker shutting down signal successfully processed for %s", sender
        )

    @patch(f"{MODULE_PATH}.cache")
    def test_worker_shutting_down_signal_dispatch_should_call_handler(self, mock_cache):
        # Test Data
        shutdown_key = f"{__title__.upper()}_WORKER_SHUTDOWN"
        sender = "celery@worker2"

        # Test Action
        signals.worker_shutting_down.send(sender=sender)

        # Expected Result
        mock_cache.set.assert_called_with(shutdown_key, True, timeout=120)


class TestWorkerShutdownHandler(AuthTestCase):
    @patch(f"{MODULE_PATH}.logger")
    @patch(f"{MODULE_PATH}.get_redis_client", return_value=None)
    def test_worker_shutdown_handler_should_skip_when_redis_unavailable(
        self, mock_get_redis_client, mock_logger
    ):
        # Test Data
        sender = "celery@worker1"

        # Test Action
        killstats_signals.worker_shutdown_handler(sender=sender)

        # Expected Result
        mock_logger.debug.assert_called_once_with(
            "No redis client available; skipping QueueOnce lock clear"
        )

    @patch(f"{MODULE_PATH}.logger")
    @patch(f"{MODULE_PATH}.cache")
    @patch(f"{MODULE_PATH}.get_redis_client")
    def test_worker_shutdown_handler_should_delete_queue_once_lock_when_redis_available(
        self, mock_get_redis_client, mock_cache, mock_logger
    ):
        # Test Data
        mock_get_redis_client.return_value = MagicMock()
        mock_cache.delete.return_value = 1
        sender = "celery@worker1"

        # Test Action
        killstats_signals.worker_shutdown_handler(sender=sender)

        # Expected Result
        mock_cache.delete.assert_called_once_with("qo_killstats.tasks.run_tracker_zkb")
        mock_logger.debug.assert_any_call(
            "Cleared QueueOnce lock for %s on shutdown (key=%s, deleted=%s)",
            "killstats.tasks.run_tracker_zkb",
            "qo_killstats.tasks.run_tracker_zkb",
            1,
        )
        mock_logger.debug.assert_any_call(
            "Worker shutdown signal successfully processed for %s", sender
        )

    @patch(f"{MODULE_PATH}.logger")
    @patch(f"{MODULE_PATH}.import_module")
    @patch(f"{MODULE_PATH}.get_redis_client")
    def test_worker_shutdown_handler_should_skip_when_task_not_found(
        self, mock_get_redis_client, mock_import_module, mock_logger
    ):
        # Test Data
        mock_get_redis_client.return_value = MagicMock()
        mock_module = Mock(spec=[])
        mock_import_module.return_value = mock_module
        sender = "celery@worker1"

        # Test Action
        killstats_signals.worker_shutdown_handler(sender=sender)

        # Expected Result
        mock_logger.debug.assert_called_once_with(
            "run_tracker_zkb task not found or has no name attribute"
        )

    @patch(f"{MODULE_PATH}.logger")
    @patch(f"{MODULE_PATH}.import_module", side_effect=RuntimeError("Import failure"))
    @patch(f"{MODULE_PATH}.get_redis_client")
    def test_worker_shutdown_handler_should_handle_and_log_exception(
        self, mock_get_redis_client, mock_import_module, mock_logger
    ):
        # Test Data
        mock_get_redis_client.return_value = MagicMock()
        sender = "celery@worker1"

        # Test Action
        killstats_signals.worker_shutdown_handler(sender=sender)

        # Expected Result
        mock_logger.exception.assert_called_once_with(
            "Failed to clear QueueOnce lock for run_tracker_zkb"
        )

    @patch(f"{MODULE_PATH}.cache")
    @patch(f"{MODULE_PATH}.get_redis_client")
    def test_worker_shutdown_signal_dispatch_should_call_handler(
        self, mock_get_redis_client, mock_cache
    ):
        # Test Data
        mock_get_redis_client.return_value = MagicMock()
        sender = "celery@worker2"

        # Test Action
        signals.worker_shutdown.send(sender=sender)

        # Expected Result
        mock_cache.delete.assert_called_with("qo_killstats.tasks.run_tracker_zkb")
