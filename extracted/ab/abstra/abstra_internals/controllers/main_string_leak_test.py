import unittest
from unittest.mock import MagicMock

from abstra_internals.controllers.main import MainController
from abstra_internals.entities.execution_context import (
    Request,
)
from abstra_internals.settings import Settings

Settings.set_root_path("/tmp")


def _make_controller_and_mock_connection(recv_sequence):
    controller = MagicMock()
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


class TestRunPageStageStringLeaking(unittest.TestCase):
    """Tests that run_page_stage does not leak internal strings in 500 responses."""

    def test_traceback_string_not_in_response_body(self):
        """Unparseable string (traceback) must not appear in the response body."""
        recv_sequence = [
            '{"type":"execution:started","data":{"executionId":"abc"}}',
            "Traceback (most recent call last):\n  File 'worker.py'\nKeyError: 'db_password'",
        ]
        controller, _ = _make_controller_and_mock_connection(recv_sequence)
        request = Request(headers={}, body="", query_params={}, method="GET")

        result = controller.run_page_stage("test-page-id", request)

        self.assertEqual(result["status"], 500)
        self.assertNotIn("Traceback", result["body"])
        self.assertNotIn("db_password", result["body"])

    def test_arbitrary_string_not_in_response_body(self):
        """Any arbitrary string should not be sent as-is to the client."""
        recv_sequence = [
            '{"type":"execution:started","data":{"executionId":"abc"}}',
            "internal error: token=abc123secret",
        ]
        controller, _ = _make_controller_and_mock_connection(recv_sequence)
        request = Request(headers={}, body="", query_params={}, method="GET")

        result = controller.run_page_stage("test-page-id", request)

        self.assertEqual(result["status"], 500)
        self.assertNotIn("abc123secret", result["body"])


if __name__ == "__main__":
    unittest.main()
