import threading
import unittest
from typing import Any, Dict
from unittest.mock import MagicMock, patch

from abstra_internals.interface.cli.editor import shutdown_editor_components


class _RecordingThread:
    """Captures Thread(target=..., name=..., daemon=...) calls and lets the
    test invoke the target synchronously via .start()."""

    created = []

    def __init__(self, *, target, name=None, daemon=None):
        self.target = target
        self.name = name
        self.daemon = daemon
        self.started = False
        _RecordingThread.created.append(self)

    def start(self):
        self.started = True
        self.target()


class TestShutdownEditorComponents(unittest.TestCase):
    """Unit tests for shutdown_editor_components — the helper wired into
    the SIGTERM callback by editor()."""

    def setUp(self):
        _RecordingThread.created = []

    def _invoke(self, **overrides):
        kwargs: Dict[str, Any] = dict(
            server=MagicMock(),
            watchers=(),
            editor_consumer=None,
            consumer_controller=None,
            stdio_broadcast_stop_event=None,
            thread_factory=_RecordingThread,
        )
        kwargs.update(overrides)
        shutdown_editor_components(**kwargs)
        return kwargs

    def test_schedules_server_shutdown_on_background_thread(self):
        server = MagicMock()

        self._invoke(server=server)

        self.assertEqual(len(_RecordingThread.created), 1)
        thread = _RecordingThread.created[0]
        self.assertTrue(thread.started)
        self.assertTrue(thread.daemon)
        self.assertEqual(thread.name, "WerkzeugShutdown")
        server.shutdown.assert_called_once_with()

    def test_calls_stop_iter_on_editor_consumer(self):
        consumer = MagicMock()

        self._invoke(editor_consumer=consumer)

        consumer.stop_iter.assert_called_once_with()

    def test_calls_shutdown_on_consumer_controller(self):
        controller = MagicMock()

        self._invoke(consumer_controller=controller)

        controller.shutdown.assert_called_once_with()

    def test_sets_stdio_broadcast_stop_event(self):
        stop_event = threading.Event()
        self.assertFalse(stop_event.is_set())

        self._invoke(stdio_broadcast_stop_event=stop_event)

        self.assertTrue(stop_event.is_set())

    def test_stops_every_non_none_watcher(self):
        watcher_a = MagicMock()
        watcher_b = MagicMock()

        self._invoke(watchers=(watcher_a, None, watcher_b))

        watcher_a.stop.assert_called_once_with()
        watcher_b.stop.assert_called_once_with()

    def test_continues_when_one_watcher_raises(self):
        bad = MagicMock()
        bad.stop.side_effect = RuntimeError("boom")
        good = MagicMock()
        server = MagicMock()

        self._invoke(server=server, watchers=(bad, good))

        good.stop.assert_called_once_with()
        server.shutdown.assert_called_once_with()

    def test_continues_when_editor_consumer_raises(self):
        consumer = MagicMock()
        consumer.stop_iter.side_effect = RuntimeError("boom")
        server = MagicMock()

        self._invoke(server=server, editor_consumer=consumer)

        server.shutdown.assert_called_once_with()

    def test_continues_when_consumer_controller_raises(self):
        controller = MagicMock()
        controller.shutdown.side_effect = RuntimeError("boom")
        server = MagicMock()

        self._invoke(server=server, consumer_controller=controller)

        server.shutdown.assert_called_once_with()

    def test_handles_all_none_dependencies(self):
        """With only the server, shutdown must still unblock serve_forever."""
        server = MagicMock()

        self._invoke(server=server)

        server.shutdown.assert_called_once_with()


class TestSigtermRegistersShutdown(unittest.TestCase):
    """Smoke test that editor() wires SignalHandlers and the shutdown helper.

    We don't boot the whole editor — instead we verify that the module
    imports SignalHandlers and shutdown_editor_components so the SIGTERM
    callback can be registered."""

    def test_editor_module_imports_signal_handlers(self):
        from abstra_internals.interface.cli import editor

        self.assertTrue(hasattr(editor, "SignalHandlers"))
        self.assertTrue(hasattr(editor, "shutdown_editor_components"))

    @patch("abstra_internals.interface.cli.editor.connect_tunnel")
    @patch("abstra_internals.interface.cli.editor.TasksWatcher")
    @patch("abstra_internals.interface.cli.editor.LogsWatcher")
    @patch("abstra_internals.interface.cli.editor.FileWatcher")
    @patch("abstra_internals.interface.cli.editor.CodebaseEventController")
    @patch("abstra_internals.interface.cli.editor.StdioPatcher")
    @patch("abstra_internals.interface.cli.editor.MainController")
    @patch("abstra_internals.interface.cli.editor.build_editor_repositories")
    @patch("abstra_internals.interface.cli.editor.get_mp_context_repository")
    @patch("abstra_internals.interface.cli.editor.get_local_app")
    @patch("abstra_internals.interface.cli.editor.make_server")
    @patch("abstra_internals.interface.cli.editor.SignalHandlers")
    @patch("abstra_internals.interface.cli.editor.WebEditorHeartbeat")
    @patch("abstra_internals.interface.cli.editor.EDITOR_MODE", "web")
    @patch("abstra_internals.interface.cli.editor.RABBITMQ_CONNECTION_URI", None)
    @patch("abstra_internals.interface.cli.editor.WORKER_LOG_TO_QUEUE", False)
    @patch("abstra_internals.interface.cli.editor.check_latest_version")
    @patch("abstra_internals.interface.cli.editor.serve_message")
    @patch("abstra_internals.interface.cli.editor.load_dotenv")
    @patch("abstra_internals.interface.cli.editor.AbstraLogger")
    @patch("abstra_internals.interface.cli.editor.Settings")
    @patch("abstra_internals.interface.cli.editor.ensure_certificates")
    def test_editor_registers_sigterm_callback(
        self,
        _ensure_certs,
        _settings,
        _logger,
        _dotenv,
        _serve_message,
        _check_version,
        _heartbeat,
        mock_signal_handlers,
        mock_make_server,
        _get_local_app,
        _get_mp_ctx,
        _build_repos,
        _main_ctrl,
        _stdio_patcher,
        _codebase,
        _file_w,
        _logs_w,
        _tasks_w,
        _connect_tunnel,
    ):
        """editor() must call SignalHandlers.init() and register_sigterm_callback."""
        mock_server = MagicMock()
        mock_make_server.return_value = mock_server
        # make serve_forever return immediately so editor() exits
        mock_server.serve_forever.return_value = None

        from abstra_internals.interface.cli.editor import editor

        editor(headless=True)

        mock_signal_handlers.init.assert_called_once_with()
        mock_signal_handlers.register_sigterm_callback.assert_called_once()
        # callback must be callable
        cb = mock_signal_handlers.register_sigterm_callback.call_args[0][0]
        self.assertTrue(callable(cb))


if __name__ == "__main__":
    unittest.main()
