import unittest
from unittest.mock import MagicMock

import requests

from abstra_internals.repositories.tasks import (
    ProductionTasksRepository,
    TaskDTO,
)


def _make_response(json_data, status_code: int = 200) -> requests.Response:
    """Build a real requests.Response so raise_for_status() and json() behave like prod."""
    response = requests.Response()
    response.status_code = status_code
    response._content = (
        json_data
        if isinstance(json_data, (bytes, bytearray))
        else __import__("json").dumps(json_data).encode("utf-8")
    )
    response.headers["Content-Type"] = "application/json"
    return response


SAMPLE_TASK = {
    "id": "task-1",
    "type": "test",
    "payload": {},
    "status": "pending",
    "target_stage_id": "stage-1",
    "created": {
        "at": "2026-05-07T00:00:00Z",
        "by_execution_id": None,
        "by_stage_id": None,
    },
    "locked": None,
    "completed": None,
}


class TestProductionTasksRepositoryHappyPath(unittest.TestCase):
    """Sanity: success responses still parse correctly after the raise_for_status fix."""

    def setUp(self):
        self.mock_client = MagicMock()
        self.repo = ProductionTasksRepository(client=self.mock_client)

    def test_get_pending_tasks_parses_ok_response(self):
        self.mock_client.get.return_value = _make_response({"tasks": [SAMPLE_TASK]})

        result = self.repo.get_pending_tasks("stage-1", limit=10, offset=0, where={})

        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], TaskDTO)
        self.assertEqual(result[0].id, "task-1")

    def test_get_sent_tasks_parses_ok_response(self):
        self.mock_client.get.return_value = _make_response({"tasks": [SAMPLE_TASK]})

        result = self.repo.get_sent_tasks("stage-1", limit=10, offset=0, where={})

        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], TaskDTO)

    def test_get_stage_tasks_parses_ok_response(self):
        self.mock_client.get.return_value = _make_response({"tasks": [SAMPLE_TASK]})

        result = self.repo.get_stage_tasks("stage-1")

        self.assertEqual(len(result), 1)

    def test_get_by_id_parses_ok_response(self):
        self.mock_client.get.return_value = _make_response(SAMPLE_TASK)

        result = self.repo.get_by_id("task-1")

        self.assertIsInstance(result, TaskDTO)
        self.assertEqual(result.id, "task-1")


class TestProductionTasksRepositoryRaisesOnHttpError(unittest.TestCase):
    """
    Regression: when cloud-api responds with an HTTP error (e.g. 5xx during PG saturation),
    the repository must surface a requests.HTTPError instead of a misleading
    KeyError('tasks') / pydantic.ValidationError caused by parsing an error body
    such as {"error": "..."} as if it were a successful payload.

    Background: real production incidents on 2026-05-02 (pg pool exhaustion) and
    2026-05-05 (Postgres max_connections) returned bodies like
    {"error": "remaining connection slots are reserved..."} with status 500.
    """

    def setUp(self):
        self.mock_client = MagicMock()
        self.repo = ProductionTasksRepository(client=self.mock_client)

    def test_get_pending_tasks_raises_http_error_on_500(self):
        self.mock_client.get.return_value = _make_response(
            {"error": "Internal Server Error"}, status_code=500
        )

        with self.assertRaises(requests.HTTPError):
            self.repo.get_pending_tasks("stage-1", limit=10, offset=0, where={})

    def test_get_sent_tasks_raises_http_error_on_500(self):
        self.mock_client.get.return_value = _make_response(
            {"error": "Internal Server Error"}, status_code=500
        )

        with self.assertRaises(requests.HTTPError):
            self.repo.get_sent_tasks("stage-1", limit=10, offset=0, where={})

    def test_get_stage_tasks_raises_http_error_on_500(self):
        self.mock_client.get.return_value = _make_response(
            {"error": "Internal Server Error"}, status_code=500
        )

        with self.assertRaises(requests.HTTPError):
            self.repo.get_stage_tasks("stage-1")

    def test_get_by_id_raises_http_error_on_500(self):
        self.mock_client.get.return_value = _make_response(
            {
                "error": "remaining connection slots are reserved for "
                "non-replication superuser and rds_superuser connections"
            },
            status_code=500,
        )

        with self.assertRaises(requests.HTTPError):
            self.repo.get_by_id("task-1")

    def test_get_pending_tasks_raises_http_error_on_400(self):
        self.mock_client.get.return_value = _make_response(
            {"error": "Invalid tasks filter"}, status_code=400
        )

        with self.assertRaises(requests.HTTPError):
            self.repo.get_pending_tasks("stage-1", limit=10, offset=0, where={})


if __name__ == "__main__":
    unittest.main()
