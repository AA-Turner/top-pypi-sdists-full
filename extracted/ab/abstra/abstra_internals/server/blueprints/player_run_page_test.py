import unittest
from unittest.mock import MagicMock

from abstra_internals.entities.execution_context import Response
from abstra_internals.settings import Settings

Settings.set_root_path("/tmp")


class TestPlayerRunPageDrainsStdioMessages(unittest.TestCase):
    """Tests that _run_page in the player blueprint correctly drains
    intermediate stdio messages and handles string responses."""

    def _setup_app_and_mock(self, recv_sequence):
        """Create a Flask test client with mocked controller and connection."""
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

    def test_normal_dict_response(self):
        """Page runner returns correct HTML when response is a dict."""
        recv_sequence = [
            '{"type":"execution:started"}',
            {
                "headers": {"Content-Type": "text/html"},
                "status": 200,
                "body": "<h1>Hello</h1>",
            },
        ]
        client, mock_conn = self._setup_app_and_mock(recv_sequence)

        res = client.get("/_page/test-page")

        self.assertEqual(res.status_code, 200)
        self.assertIn(b"<h1>Hello</h1>", res.data)
        mock_conn.close.assert_called_once()

    def test_string_response_is_deserialized(self):
        """When the response arrives as a JSON string, it is deserialized correctly."""
        recv_sequence = [
            '{"type":"execution:started"}',
            '{"headers": {"Content-Type": "text/html"}, "status": 200, "body": "<p>String</p>"}',
        ]
        client, mock_conn = self._setup_app_and_mock(recv_sequence)

        res = client.get("/_page/test-page")

        self.assertEqual(res.status_code, 200)
        self.assertIn(b"<p>String</p>", res.data)

    def test_drains_stdio_batch_before_response(self):
        """stdio_batch messages are skipped until the actual Response is found."""
        recv_sequence = [
            '{"type":"execution:started"}',
            {
                "type": "stdio_batch",
                "payload": [{"type": "stdout", "log": "debug output"}],
            },
            {"headers": {}, "status": 200, "body": "<h1>Page</h1>"},
        ]
        client, mock_conn = self._setup_app_and_mock(recv_sequence)

        res = client.get("/_page/test-page")

        self.assertEqual(res.status_code, 200)
        self.assertIn(b"<h1>Page</h1>", res.data)

    def test_drains_multiple_stdio_messages(self):
        """Multiple stdio and stdio_batch messages are all drained."""
        recv_sequence = [
            '{"type":"execution:started"}',
            {"type": "stdio_batch", "payload": [{"type": "stdout", "log": "line1"}]},
            {"type": "stdio", "payload": {"type": "stderr", "log": "warn"}},
            {"type": "stdio_batch", "payload": [{"type": "stdout", "log": "line2"}]},
            {
                "headers": {"Content-Type": "application/json"},
                "status": 200,
                "body": '{"result": 42}',
            },
        ]
        client, mock_conn = self._setup_app_and_mock(recv_sequence)

        res = client.post("/_page/test-page")

        self.assertEqual(res.status_code, 200)
        self.assertIn(b'{"result": 42}', res.data)

    def test_string_execution_ended_returns_500(self):
        """When execution:ended arrives as string (no Response sent),
        it should return 500 — the worker finished without sending a page response."""
        recv_sequence = [
            '{"type":"execution:started"}',
            '{"type":"execution:ended","data":{"exitStatus":"EXCEPTION"}}',
        ]
        client, mock_conn = self._setup_app_and_mock(recv_sequence)

        res = client.get("/_page/test-page")

        self.assertEqual(res.status_code, 500)

    def test_response_object_used_directly(self):
        """When connection returns a Response instance, it's used directly."""
        recv_sequence = [
            '{"type":"execution:started"}',
            Response(headers={"Content-Type": "text/plain"}, status=200, body="direct"),
        ]
        client, mock_conn = self._setup_app_and_mock(recv_sequence)

        res = client.get("/_page/test-page")

        self.assertEqual(res.status_code, 200)
        self.assertIn(b"direct", res.data)

    def test_stream_response_still_works(self):
        """Streaming responses (generator functions) still work after the fix."""
        recv_sequence = [
            '{"type":"execution:started"}',
            {
                "__page_stream__": "start",
                "status": 200,
                "headers": {"Content-Type": "application/x-ndjson"},
            },
        ]
        # After stream start, the generate() function will call recv() for chunks
        client, mock_conn = self._setup_app_and_mock(recv_sequence)

        # Add chunk responses for the streaming part
        mock_conn.recv.side_effect = [
            recv_sequence[0],  # execution:started
            recv_sequence[1],  # stream start
            {"__page_stream__": "chunk", "data": "hello"},
            {"__page_stream__": "end"},
        ]

        res = client.get("/_page/test-page")

        self.assertEqual(res.status_code, 200)

    def test_stdio_before_stream_start(self):
        """stdio messages before a stream start are drained correctly."""
        recv_sequence = [
            '{"type":"execution:started"}',
            {"type": "stdio_batch", "payload": []},
            {
                "__page_stream__": "start",
                "status": 200,
                "headers": {"Content-Type": "application/x-ndjson"},
            },
        ]
        client, mock_conn = self._setup_app_and_mock(recv_sequence)

        mock_conn.recv.side_effect = [
            recv_sequence[0],
            recv_sequence[1],
            recv_sequence[2],
            {"__page_stream__": "end"},
        ]

        res = client.get("/_page/test-page")

        self.assertEqual(res.status_code, 200)
