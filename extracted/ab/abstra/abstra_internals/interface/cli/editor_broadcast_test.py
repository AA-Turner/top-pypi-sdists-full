import unittest
from unittest.mock import MagicMock, patch


class TestEditorBroadcastConsumer(unittest.TestCase):
    """Tests that editor imports and calls start_stdio_broadcast_consumer."""

    def test_start_stdio_broadcast_consumer_is_imported(self):
        """editor.py should import start_stdio_broadcast_consumer."""
        from abstra_internals.interface.cli import editor

        self.assertTrue(
            hasattr(editor, "start_stdio_broadcast_consumer"),
            "editor.py should import start_stdio_broadcast_consumer",
        )

    @patch("abstra_internals.interface.cli.editor.start_stdio_broadcast_consumer")
    @patch("abstra_internals.interface.cli.editor.WORKER_LOG_TO_QUEUE", True)
    @patch(
        "abstra_internals.interface.cli.editor.RABBITMQ_CONNECTION_URI",
        "amqp://localhost",
    )
    @patch("abstra_internals.interface.cli.editor.EDITOR_MODE", "web")
    @patch("abstra_internals.interface.cli.editor.make_server")
    @patch("abstra_internals.interface.cli.editor.get_local_app")
    @patch("abstra_internals.interface.cli.editor.MainController")
    @patch("abstra_internals.interface.cli.editor.build_web_editor_repositories")
    @patch("abstra_internals.interface.cli.editor.StdioPatcher")
    @patch("abstra_internals.interface.cli.editor.CodebaseEventController")
    @patch("abstra_internals.interface.cli.editor.FileWatcher")
    @patch("abstra_internals.interface.cli.editor.LogsWatcher")
    @patch("abstra_internals.interface.cli.editor.TasksWatcher")
    @patch("abstra_internals.interface.cli.editor.connect_tunnel")
    @patch("abstra_internals.interface.cli.editor.check_latest_version")
    @patch("abstra_internals.interface.cli.editor.serve_message")
    @patch("abstra_internals.interface.cli.editor.load_dotenv")
    @patch("abstra_internals.interface.cli.editor.AbstraLogger")
    @patch("abstra_internals.interface.cli.editor.Settings")
    @patch("abstra_internals.interface.cli.editor.WebEditorHeartbeat")
    def test_starts_broadcast_consumer_when_flag_on(
        self,
        mock_heartbeat,
        mock_settings,
        mock_logger,
        mock_dotenv,
        mock_serve,
        mock_check,
        mock_tunnel,
        mock_tasks_w,
        mock_logs_w,
        mock_file_w,
        mock_codebase,
        mock_patcher,
        mock_build_repos,
        mock_main_ctrl,
        mock_get_app,
        mock_make_server,
        mock_start_consumer,
    ):
        """When WORKER_LOG_TO_QUEUE=true, start broadcast consumer."""
        mock_server = MagicMock()
        mock_make_server.return_value = mock_server
        mock_server.serve_forever.side_effect = KeyboardInterrupt()

        from abstra_internals.interface.cli.editor import editor

        try:
            editor(headless=True)
        except KeyboardInterrupt:
            pass

        mock_start_consumer.assert_called_once_with("amqp://localhost")


class TestEditorFileWatcherGating(unittest.TestCase):
    """The inotify file watcher must be skipped in the cloud (RabbitMQ workers)
    and started locally, with controller-driven linting gated to match."""

    @patch("abstra_internals.interface.cli.editor.start_stdio_broadcast_consumer")
    @patch("abstra_internals.interface.cli.editor.RABBITMQ_CONNECTION_URI", "amqp://x")
    @patch("abstra_internals.interface.cli.editor.EDITOR_MODE", "web")
    @patch("abstra_internals.interface.cli.editor.make_server")
    @patch("abstra_internals.interface.cli.editor.get_local_app")
    @patch("abstra_internals.interface.cli.editor.MainController")
    @patch("abstra_internals.interface.cli.editor.build_web_editor_repositories")
    @patch("abstra_internals.interface.cli.editor.StdioPatcher")
    @patch("abstra_internals.interface.cli.editor.CodebaseEventController")
    @patch("abstra_internals.interface.cli.editor.FileWatcher")
    @patch("abstra_internals.interface.cli.editor.LogsWatcher")
    @patch("abstra_internals.interface.cli.editor.TasksWatcher")
    @patch("abstra_internals.interface.cli.editor.connect_tunnel")
    @patch("abstra_internals.interface.cli.editor.check_latest_version")
    @patch("abstra_internals.interface.cli.editor.serve_message")
    @patch("abstra_internals.interface.cli.editor.load_dotenv")
    @patch("abstra_internals.interface.cli.editor.AbstraLogger")
    @patch("abstra_internals.interface.cli.editor.Settings")
    @patch("abstra_internals.interface.cli.editor.WebEditorHeartbeat")
    def test_web_mode_skips_watcher_and_enables_controller_lint(
        self,
        mock_heartbeat,
        mock_settings,
        mock_logger,
        mock_dotenv,
        mock_serve,
        mock_check,
        mock_tunnel,
        mock_tasks_w,
        mock_logs_w,
        mock_file_w,
        mock_codebase,
        mock_patcher,
        mock_build_repos,
        mock_main_ctrl,
        mock_get_app,
        mock_make_server,
        mock_start_consumer,
    ):
        mock_server = MagicMock()
        mock_make_server.return_value = mock_server
        mock_server.serve_forever.side_effect = KeyboardInterrupt()

        from abstra_internals.interface.cli.editor import editor

        try:
            editor(headless=True)
        except KeyboardInterrupt:
            pass

        mock_file_w.assert_not_called()
        _, kwargs = mock_codebase.configure.call_args
        self.assertTrue(kwargs["controller_driven"])

    @patch("abstra_internals.interface.cli.editor.start_consumer")
    @patch("abstra_internals.interface.cli.editor.build_editor_repositories")
    @patch("abstra_internals.interface.cli.editor.safe_multiprocessing_queue")
    @patch("abstra_internals.interface.cli.editor.get_mp_context_repository")
    @patch("abstra_internals.interface.cli.editor.RABBITMQ_CONNECTION_URI", None)
    @patch("abstra_internals.interface.cli.editor.WORKER_LOG_TO_QUEUE", False)
    @patch("abstra_internals.interface.cli.editor.EDITOR_MODE", "local")
    @patch("abstra_internals.interface.cli.editor.make_server")
    @patch("abstra_internals.interface.cli.editor.get_local_app")
    @patch("abstra_internals.interface.cli.editor.MainController")
    @patch("abstra_internals.interface.cli.editor.StdioPatcher")
    @patch("abstra_internals.interface.cli.editor.CodebaseEventController")
    @patch("abstra_internals.interface.cli.editor.FileWatcher")
    @patch("abstra_internals.interface.cli.editor.LogsWatcher")
    @patch("abstra_internals.interface.cli.editor.TasksWatcher")
    @patch("abstra_internals.interface.cli.editor.connect_tunnel")
    @patch("abstra_internals.interface.cli.editor.check_latest_version")
    @patch("abstra_internals.interface.cli.editor.serve_message")
    @patch("abstra_internals.interface.cli.editor.load_dotenv")
    @patch("abstra_internals.interface.cli.editor.AbstraLogger")
    @patch("abstra_internals.interface.cli.editor.Settings")
    def test_local_mode_starts_watcher_and_disables_controller_lint(
        self,
        mock_settings,
        mock_logger,
        mock_dotenv,
        mock_serve,
        mock_check,
        mock_tunnel,
        mock_tasks_w,
        mock_logs_w,
        mock_file_w,
        mock_codebase,
        mock_patcher,
        mock_main_ctrl,
        mock_get_app,
        mock_make_server,
        mock_ctx,
        mock_queue,
        mock_build_repos,
        mock_start_consumer_fn,
    ):
        mock_server = MagicMock()
        mock_make_server.return_value = mock_server
        mock_server.serve_forever.side_effect = KeyboardInterrupt()
        mock_start_consumer_fn.return_value = (MagicMock(), MagicMock(), MagicMock())

        from abstra_internals.interface.cli.editor import editor

        try:
            editor(headless=True)
        except KeyboardInterrupt:
            pass

        mock_file_w.return_value.start.assert_called_once()
        _, kwargs = mock_codebase.configure.call_args
        self.assertFalse(kwargs["controller_driven"])
