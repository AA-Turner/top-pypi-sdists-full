import unittest
from unittest.mock import MagicMock, patch

from abstra_internals.controllers.main import MainController
from abstra_internals.entities.execution_context import (
    Request,
    Response,
)
from abstra_internals.settings import Settings

Settings.set_root_path("/tmp")


def _make_controller_and_mock_connection(recv_sequence):
    """Create a MainController with mocked producer and connection for hook tests."""
    controller = MagicMock()
    controller.run_hook = MainController.run_hook.__get__(controller)

    hook = MagicMock()
    hook.id = "test-hook-id"
    controller.get_hook = MagicMock(return_value=hook)

    mock_conn = MagicMock()
    mock_conn.recv = MagicMock(side_effect=recv_sequence)
    mock_conn.poll = MagicMock(return_value=True)
    controller.repositories.producer.enqueue = MagicMock(return_value=mock_conn)

    return controller, mock_conn


class TestRunHookDrainsStdioMessages(unittest.TestCase):
    """Tests that run_hook correctly drains intermediate stdio messages."""

    def test_normal_response_without_stdio(self):
        """Basic hook execution without interference."""
        recv_sequence = [
            '{"type":"execution:started","executionId":"abc"}',
            {"headers": {}, "status": 200, "body": '{"ok": true}'},
        ]
        controller, _ = _make_controller_and_mock_connection(recv_sequence)
        request = Request(headers={}, body="{}", query_params={}, method="POST")

        result = controller.run_hook("test-hook-id", request)

        self.assertEqual(result["status"], 200)
        self.assertEqual(result["body"], '{"ok": true}')
        self.assertEqual(result["execution_id"], "abc")

    def test_stdio_batch_before_response_is_drained(self):
        """A stdio_batch between execution:started and Response must be skipped.
        This is the bug: without drain, the stdio_batch is consumed as the response,
        causing .get('headers') to fail or return wrong data."""
        recv_sequence = [
            '{"type":"execution:started","executionId":"abc"}',
            {"type": "stdio_batch", "payload": [{"type": "stdout", "log": "debug"}]},
            {
                "headers": {"Content-Type": "application/json"},
                "status": 200,
                "body": '{"result": 1}',
            },
        ]
        controller, _ = _make_controller_and_mock_connection(recv_sequence)
        request = Request(headers={}, body="{}", query_params={}, method="POST")

        result = controller.run_hook("test-hook-id", request)

        self.assertEqual(result["status"], 200)
        self.assertEqual(result["body"], '{"result": 1}')

    def test_multiple_stdio_before_response(self):
        """Multiple stdio messages are all drained before the Response."""
        recv_sequence = [
            '{"type":"execution:started","executionId":"abc"}',
            {"type": "stdio_batch", "payload": []},
            {"type": "stdio", "payload": {"type": "stderr", "log": "warn"}},
            {"type": "stdio_batch", "payload": []},
            {"headers": {}, "status": 200, "body": "done"},
        ]
        controller, _ = _make_controller_and_mock_connection(recv_sequence)
        request = Request(headers={}, body="{}", query_params={}, method="POST")

        result = controller.run_hook("test-hook-id", request)

        self.assertEqual(result["status"], 200)
        self.assertEqual(result["body"], "done")

    def test_response_object_used_directly(self):
        """When connection returns a Response instance, use it directly."""
        recv_sequence = [
            '{"type":"execution:started","executionId":"abc"}',
            Response(headers={}, status=201, body="created"),
        ]
        controller, _ = _make_controller_and_mock_connection(recv_sequence)
        request = Request(headers={}, body="{}", query_params={}, method="POST")

        result = controller.run_hook("test-hook-id", request)

        self.assertEqual(result["status"], 201)
        self.assertEqual(result["body"], "created")

    def test_string_response_does_not_leak_internals(self):
        """An unparseable string response should not leak internal info."""
        recv_sequence = [
            '{"type":"execution:started","executionId":"abc"}',
            "Traceback (most recent call last): ...",
        ]
        controller, _ = _make_controller_and_mock_connection(recv_sequence)
        request = Request(headers={}, body="{}", query_params={}, method="POST")

        result = controller.run_hook("test-hook-id", request)

        self.assertEqual(result["status"], 500)
        self.assertNotIn("Traceback", result["body"])

    def test_stdio_before_execution_started_is_drained(self):
        """If a stdio_batch arrives before execution:started, it should be
        skipped and execution:started should still be found.
        Without drain on first recv, the stdio_batch is consumed as
        execution:started, causing KeyError on 'executionId'."""
        recv_sequence = [
            {"type": "stdio_batch", "payload": [{"type": "stdout", "log": "early"}]},
            '{"type":"execution:started","executionId":"abc"}',
            {"headers": {}, "status": 200, "body": '{"ok": true}'},
        ]
        controller, _ = _make_controller_and_mock_connection(recv_sequence)
        request = Request(headers={}, body="{}", query_params={}, method="POST")

        result = controller.run_hook("test-hook-id", request)

        self.assertEqual(result["status"], 200)
        self.assertEqual(result["body"], '{"ok": true}')
        self.assertEqual(result["execution_id"], "abc")

    def test_multiple_stdio_before_execution_started(self):
        """Multiple stdio messages before execution:started are all drained."""
        recv_sequence = [
            {"type": "stdio_batch", "payload": []},
            {"type": "stdio", "payload": {"type": "stdout", "log": "init"}},
            {"type": "stdio_batch", "payload": []},
            '{"type":"execution:started","executionId":"xyz"}',
            {"headers": {}, "status": 200, "body": "ok"},
        ]
        controller, _ = _make_controller_and_mock_connection(recv_sequence)
        request = Request(headers={}, body="{}", query_params={}, method="POST")

        result = controller.run_hook("test-hook-id", request)

        self.assertEqual(result["status"], 200)
        self.assertEqual(result["body"], "ok")
        self.assertEqual(result["execution_id"], "xyz")

    @patch("abstra_internals.controllers.main.flask")
    def test_none_response_aborts_500(self, mock_flask):
        """When recv returns None, abort with 500."""
        mock_flask.abort = MagicMock(side_effect=Exception("abort"))
        recv_sequence = [
            '{"type":"execution:started","executionId":"abc"}',
            None,
        ]
        controller, _ = _make_controller_and_mock_connection(recv_sequence)
        request = Request(headers={}, body="{}", query_params={}, method="POST")

        with self.assertRaises(Exception):
            controller.run_hook("test-hook-id", request)

        mock_flask.abort.assert_called_once_with(500)


class TestRunHookStartMessageTimeout(unittest.TestCase):
    """Tests that run_hook handles timeout/None on the first drain correctly."""

    @patch("abstra_internals.controllers.main.flask")
    def test_none_start_msg_aborts_500_and_closes_connection(self, mock_flask):
        """When drain_until_response returns None for the start message,
        run_hook should abort(500) and close the connection without crashing."""
        mock_flask.abort = MagicMock(side_effect=Exception("abort"))
        recv_sequence = [None]
        controller, mock_conn = _make_controller_and_mock_connection(recv_sequence)
        request = Request(headers={}, body="{}", query_params={}, method="POST")

        with self.assertRaises(Exception):
            controller.run_hook("test-hook-id", request)

        mock_flask.abort.assert_called_once_with(500)
        mock_conn.close.assert_called_once()

    @patch("abstra_internals.controllers.main.flask")
    def test_response_object_start_msg_aborts_500(self, mock_flask):
        """When start_msg is a Response object (not a dict),
        run_hook should abort(500) — it's not a valid execution:started."""
        mock_flask.abort = MagicMock(side_effect=Exception("abort"))
        recv_sequence = [
            Response(headers={}, status=200, body="unexpected"),
        ]
        controller, mock_conn = _make_controller_and_mock_connection(recv_sequence)
        request = Request(headers={}, body="{}", query_params={}, method="POST")

        with self.assertRaises(Exception):
            controller.run_hook("test-hook-id", request)

        mock_flask.abort.assert_called_once_with(500)
        mock_conn.close.assert_called_once()


class TestRunHookStartMsgEdgeCases(unittest.TestCase):
    """Tests for edge cases in start message handling."""

    @patch("abstra_internals.controllers.main.flask")
    def test_unparseable_string_start_msg_aborts_500(self, mock_flask):
        """If drain returns an unparseable string (e.g. traceback),
        json.loads should not raise JSONDecodeError — should abort 500."""
        mock_flask.abort = MagicMock(side_effect=Exception("abort"))
        recv_sequence = ["Traceback (most recent call last): ..."]
        controller, mock_conn = _make_controller_and_mock_connection(recv_sequence)
        request = Request(headers={}, body="{}", query_params={}, method="POST")

        with self.assertRaises(Exception):
            controller.run_hook("test-hook-id", request)

        mock_flask.abort.assert_called_once_with(500)
        mock_conn.close.assert_called_once()

    @patch("abstra_internals.controllers.main.flask")
    def test_dict_without_executionId_aborts_500(self, mock_flask):
        """If start_msg is a dict but has no executionId key (e.g. execution:ended),
        should abort 500 instead of raising KeyError."""
        mock_flask.abort = MagicMock(side_effect=Exception("abort"))
        recv_sequence = [
            {"type": "execution:ended", "data": {"exitStatus": "EXCEPTION"}},
        ]
        controller, mock_conn = _make_controller_and_mock_connection(recv_sequence)
        request = Request(headers={}, body="{}", query_params={}, method="POST")

        with self.assertRaises(Exception):
            controller.run_hook("test-hook-id", request)

        mock_flask.abort.assert_called_once_with(500)
        mock_conn.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
