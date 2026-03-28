import unittest
from unittest.mock import MagicMock

from abstra_internals.settings import Settings

Settings.set_root_path("/tmp")


class TestPlayerFirstRecvDrainsStdio(unittest.TestCase):
    """Tests that the first recv() in _run_page (waiting for execution:started)
    correctly drains stdio messages that arrive before execution:started."""

    def _setup_app_and_mock(self, recv_sequence):
        from abstra_internals.server.apps import get_cloud_app

        controller = MagicMock()

        page = MagicMock()
        page.id = "test-page-id"
        page.path = "test-page"
        page.file = "test_page.py"
        controller.get_page_stage_by_path = MagicMock(return_value=page)

        mock_conn = MagicMock()
        mock_conn.recv = MagicMock(side_effect=recv_sequence)
        mock_conn.poll = MagicMock(return_value=True)
        controller.repositories.producer.enqueue = MagicMock(return_value=mock_conn)

        app = get_cloud_app(controller)
        client = app.test_client()
        return client, mock_conn

    def test_stdio_before_execution_started_is_drained(self):
        """If a stdio_batch arrives before execution:started, it should be
        skipped and the execution:started should still be found.
        Without drain on first recv, the stdio_batch is consumed as
        execution:started, and the actual execution:started becomes the
        'response', causing malformed output."""
        recv_sequence = [
            {
                "type": "stdio_batch",
                "payload": [{"type": "stdout", "log": "early print"}],
            },
            '{"type":"execution:started"}',
            {
                "headers": {"Content-Type": "text/html"},
                "status": 200,
                "body": "<h1>OK</h1>",
            },
        ]
        client, _ = self._setup_app_and_mock(recv_sequence)

        res = client.get("/_page/test-page")

        self.assertEqual(res.status_code, 200)
        self.assertIn(b"<h1>OK</h1>", res.data)

    def test_multiple_stdio_before_execution_started(self):
        """Multiple stdio messages before execution:started are all drained."""
        recv_sequence = [
            {"type": "stdio_batch", "payload": []},
            {"type": "stdio", "payload": {"type": "stdout", "log": "init"}},
            '{"type":"execution:started"}',
            {"headers": {}, "status": 200, "body": "ok"},
        ]
        client, _ = self._setup_app_and_mock(recv_sequence)

        res = client.get("/_page/test-page")

        self.assertEqual(res.status_code, 200)
        self.assertIn(b"ok", res.data)


class TestPlayerRunPageFailFastOnStartTimeout(unittest.TestCase):
    """Tests that _run_page aborts 500 immediately when start message times out."""

    def _setup_app_and_mock(self, recv_sequence):
        from abstra_internals.server.apps import get_cloud_app

        controller = MagicMock()

        page = MagicMock()
        page.id = "test-page-id"
        page.path = "test-page"
        page.file = "test_page.py"
        controller.get_page_stage_by_path = MagicMock(return_value=page)

        mock_conn = MagicMock()
        mock_conn.recv = MagicMock(side_effect=recv_sequence)
        mock_conn.poll = MagicMock(return_value=True)
        controller.repositories.producer.enqueue = MagicMock(return_value=mock_conn)

        app = get_cloud_app(controller)
        client = app.test_client()
        return client, mock_conn

    def test_none_start_msg_returns_500(self):
        """If first drain returns None, _run_page should abort 500 immediately."""
        recv_sequence = [None]
        client, mock_conn = self._setup_app_and_mock(recv_sequence)

        res = client.get("/_page/test-page")

        self.assertEqual(res.status_code, 500)
        mock_conn.close.assert_called_once()


class TestPlayerHookRunnerDrainsStdio(unittest.TestCase):
    """Tests that hook_runner in the player blueprint drains stdio messages."""

    def _setup_app_and_mock(self, recv_sequence):
        from abstra_internals.server.apps import get_cloud_app

        controller = MagicMock()

        hook = MagicMock()
        hook.id = "test-hook-id"
        hook.path = "test-hook"
        hook.file = "test_hook.py"
        controller.get_hook_by_path = MagicMock(return_value=hook)

        mock_conn = MagicMock()
        mock_conn.recv = MagicMock(side_effect=recv_sequence)
        mock_conn.poll = MagicMock(return_value=True)
        controller.repositories.producer.enqueue = MagicMock(return_value=mock_conn)

        app = get_cloud_app(controller)
        client = app.test_client()
        return client, mock_conn

    def test_stdio_batch_before_hook_response_is_drained(self):
        """A stdio_batch between execution:started and Response must be skipped."""
        recv_sequence = [
            '{"type":"execution:started"}',
            {"type": "stdio_batch", "payload": [{"type": "stdout", "log": "debug"}]},
            {
                "headers": {"Content-Type": "application/json"},
                "status": 200,
                "body": '{"ok": true}',
            },
        ]
        client, _ = self._setup_app_and_mock(recv_sequence)

        res = client.post("/_hooks/test-hook")

        self.assertEqual(res.status_code, 200)
        self.assertIn(b'{"ok": true}', res.data)

    def test_hook_string_response_does_not_leak(self):
        """An unparseable string response should not leak internal info."""
        recv_sequence = [
            '{"type":"execution:started"}',
            "Traceback (most recent call last): ...",
        ]
        client, _ = self._setup_app_and_mock(recv_sequence)

        res = client.post("/_hooks/test-hook")

        self.assertEqual(res.status_code, 500)
        self.assertNotIn(b"Traceback", res.data)


if __name__ == "__main__":
    unittest.main()
