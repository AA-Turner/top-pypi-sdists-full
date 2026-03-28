import unittest
from unittest.mock import MagicMock

from abstra_internals.settings import Settings

Settings.set_root_path("/tmp")


class TestPlayerStringResponseDoesNotLeakInternals(unittest.TestCase):
    """Tests that unparseable string responses don't leak internal info."""

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

    def test_traceback_string_not_leaked_to_client(self):
        """When response is an unparseable string (e.g. a traceback),
        the body should NOT contain that string — it would leak internals."""
        recv_sequence = [
            '{"type":"execution:started"}',
            "Traceback (most recent call last):\n  File 'worker.py', line 42\nKeyError: 'secret_key'",
        ]
        client, _ = self._setup_app_and_mock(recv_sequence)

        res = client.get("/_page/test-page")

        self.assertEqual(res.status_code, 500)
        self.assertNotIn(b"Traceback", res.data)
        self.assertNotIn(b"secret_key", res.data)

    def test_arbitrary_string_not_leaked(self):
        """Any arbitrary string should not be sent as-is to the client."""
        recv_sequence = [
            '{"type":"execution:started"}',
            "internal error details: password=hunter2",
        ]
        client, _ = self._setup_app_and_mock(recv_sequence)

        res = client.get("/_page/test-page")

        self.assertEqual(res.status_code, 500)
        self.assertNotIn(b"hunter2", res.data)


if __name__ == "__main__":
    unittest.main()
