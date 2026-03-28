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
    """Create a MainController with mocked producer and connection.

    recv_sequence: list of values that connection.recv() will return in order.
    """
    controller = MagicMock()

    # Bind the real method so we can test it
    controller.run_page_stage = MainController.run_page_stage.__get__(controller)

    page = MagicMock()
    page.id = "test-page-id"
    page.path = "test-page"
    controller.get_page_stage = MagicMock(return_value=page)

    mock_conn = MagicMock()
    mock_conn.recv = MagicMock(side_effect=recv_sequence)
    mock_conn.poll = MagicMock(return_value=True)
    controller.repositories.producer.enqueue = MagicMock(return_value=mock_conn)

    return controller, mock_conn


class TestRunPageStageDrainsStdioMessages(unittest.TestCase):
    """Tests that run_page_stage correctly drains intermediate stdio messages
    from the RabbitMQ session queue and finds the actual page Response."""

    def test_normal_dict_response(self):
        """When the second recv() returns a proper response dict, it works."""
        recv_sequence = [
            '{"type":"execution:started","data":{"executionId":"abc"}}',
            {
                "headers": {"Content-Type": "text/html"},
                "status": 200,
                "body": "<h1>OK</h1>",
            },
        ]
        controller, mock_conn = _make_controller_and_mock_connection(recv_sequence)
        request = Request(headers={}, body="", query_params={}, method="GET")

        result = controller.run_page_stage("test-page-id", request)

        self.assertEqual(result["status"], 200)
        self.assertEqual(result["body"], "<h1>OK</h1>")
        mock_conn.close.assert_called_once()

    def test_string_response_is_deserialized(self):
        """When the response arrives as a JSON string (text/plain), it is deserialized."""
        recv_sequence = [
            '{"type":"execution:started"}',
            '{"headers": {}, "status": 200, "body": "hello"}',
        ]
        controller, mock_conn = _make_controller_and_mock_connection(recv_sequence)
        request = Request(headers={}, body="", query_params={}, method="GET")

        result = controller.run_page_stage("test-page-id", request)

        self.assertEqual(result["status"], 200)
        self.assertEqual(result["body"], "hello")

    def test_drains_single_stdio_batch_before_response(self):
        """A stdio_batch between execution:started and Response is skipped."""
        recv_sequence = [
            '{"type":"execution:started"}',
            {"type": "stdio_batch", "payload": [{"type": "stdout", "log": "hello"}]},
            {"headers": {}, "status": 200, "body": "<h1>Page</h1>"},
        ]
        controller, mock_conn = _make_controller_and_mock_connection(recv_sequence)
        request = Request(headers={}, body="", query_params={}, method="GET")

        result = controller.run_page_stage("test-page-id", request)

        self.assertEqual(result["status"], 200)
        self.assertEqual(result["body"], "<h1>Page</h1>")

    def test_drains_multiple_stdio_batches_before_response(self):
        """Multiple stdio_batch messages are all drained before the Response."""
        recv_sequence = [
            '{"type":"execution:started"}',
            {"type": "stdio_batch", "payload": [{"type": "stdout", "log": "line1"}]},
            {"type": "stdio_batch", "payload": [{"type": "stdout", "log": "line2"}]},
            {"type": "stdio", "payload": {"type": "stderr", "log": "warn"}},
            {
                "headers": {"Content-Type": "text/html"},
                "status": 200,
                "body": "<h1>OK</h1>",
            },
        ]
        controller, mock_conn = _make_controller_and_mock_connection(recv_sequence)
        request = Request(headers={}, body="", query_params={}, method="GET")

        result = controller.run_page_stage("test-page-id", request)

        self.assertEqual(result["status"], 200)
        self.assertEqual(result["body"], "<h1>OK</h1>")

    def test_response_object_returned_directly(self):
        """When connection.recv() returns a Response instance, it's used directly."""
        response_obj = Response(headers={"X-Custom": "val"}, status=201, body="created")
        recv_sequence = [
            '{"type":"execution:started"}',
            response_obj,
        ]
        controller, mock_conn = _make_controller_and_mock_connection(recv_sequence)
        request = Request(headers={}, body="", query_params={}, method="GET")

        result = controller.run_page_stage("test-page-id", request)

        self.assertEqual(result["status"], 201)
        self.assertEqual(result["body"], "created")
        self.assertEqual(result["headers"], {"X-Custom": "val"})

    def test_execution_ended_string_without_response(self):
        """When execution:ended arrives without a Response (e.g. worker crashed),
        it's parsed as a dict and returns 500 — not a valid page response."""
        recv_sequence = [
            '{"type":"execution:started"}',
            '{"type":"execution:ended","data":{"exitStatus":"EXCEPTION"}}',
        ]
        controller, mock_conn = _make_controller_and_mock_connection(recv_sequence)
        request = Request(headers={}, body="", query_params={}, method="GET")

        result = controller.run_page_stage("test-page-id", request)

        self.assertEqual(result["status"], 500)
        self.assertEqual(result["body"], "Internal Server Error")

    @patch("abstra_internals.controllers.main.flask")
    def test_none_response_aborts_500(self, mock_flask):
        """When connection.recv() returns None, the server aborts with 500."""
        mock_flask.abort = MagicMock(side_effect=Exception("abort"))
        recv_sequence = [
            '{"type":"execution:started"}',
            None,
        ]
        controller, mock_conn = _make_controller_and_mock_connection(recv_sequence)
        request = Request(headers={}, body="", query_params={}, method="GET")

        with self.assertRaises(Exception):
            controller.run_page_stage("test-page-id", request)

        mock_flask.abort.assert_called_once_with(500)


class TestRunPageStageStartMsgValidation(unittest.TestCase):
    """Tests that run_page_stage fails fast when the start message is invalid."""

    @patch("abstra_internals.controllers.main.flask")
    def test_none_start_msg_aborts_500_immediately(self, mock_flask):
        """If first drain returns None (timeout), abort 500 without waiting
        for a second drain that would waste another 30s."""
        mock_flask.abort = MagicMock(side_effect=Exception("abort"))
        controller, mock_conn = _make_controller_and_mock_connection([None])
        request = Request(headers={}, body="", query_params={}, method="GET")

        with self.assertRaises(Exception):
            controller.run_page_stage("test-page-id", request)

        mock_flask.abort.assert_called_once_with(500)
        mock_conn.close.assert_called_once()
