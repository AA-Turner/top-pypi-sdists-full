"""Tests for AthenaTransformer."""

import unittest
from datetime import datetime, timezone
from unittest.mock import MagicMock

from sagemaker_studio.sql_engine.athena_transformer import AthenaTransformer


class TestAthenaTransformerGetExecutionMetadata(unittest.TestCase):
    """Tests for get_execution_metadata extracting PyAthena cursor attributes."""

    def _make_full_cursor(self):
        cursor = MagicMock()
        cursor.query_id = "athena-query-123"
        cursor.data_scanned_in_bytes = 1048576
        cursor.engine_execution_time_in_millis = 500
        cursor.total_execution_time_in_millis = 800
        cursor.query_queue_time_in_millis = 50
        cursor.query_planning_time_in_millis = 100
        cursor.service_processing_time_in_millis = 150
        cursor.submission_date_time = datetime(2025, 1, 15, 10, 0, 0, tzinfo=timezone.utc)
        cursor.completion_date_time = datetime(2025, 1, 15, 10, 0, 1, tzinfo=timezone.utc)
        cursor.state = "SUCCEEDED"
        cursor.output_location = "s3://bucket/results/athena-query-123.csv"
        return cursor

    def test_happy_path_all_attributes(self):
        cursor = self._make_full_cursor()
        result = AthenaTransformer.get_execution_metadata(cursor)

        self.assertIsNotNone(result)
        self.assertEqual(result["query_execution_id"], "athena-query-123")
        self.assertEqual(result["data_scanned_bytes"], 1048576)
        self.assertEqual(result["engine_execution_time_ms"], 500)
        self.assertEqual(result["total_execution_time_ms"], 800)
        self.assertEqual(result["query_queue_time_ms"], 50)
        self.assertEqual(result["query_planning_time_ms"], 100)
        self.assertEqual(result["service_processing_time_ms"], 150)
        self.assertEqual(result["submission_time"], "2025-01-15T10:00:00+00:00")
        self.assertEqual(result["completion_time"], "2025-01-15T10:00:01+00:00")
        self.assertEqual(result["state"], "SUCCEEDED")
        self.assertEqual(result["output_location"], "s3://bucket/results/athena-query-123.csv")

    def test_minimal_cursor_only_query_id(self):
        cursor = MagicMock(spec=[])
        cursor.query_id = "minimal-query-id"
        result = AthenaTransformer.get_execution_metadata(cursor)

        self.assertIsNotNone(result)
        self.assertEqual(result["query_execution_id"], "minimal-query-id")
        self.assertNotIn("data_scanned_bytes", result)
        self.assertNotIn("engine_execution_time_ms", result)

    def test_returns_none_for_empty_cursor(self):
        cursor = MagicMock(spec=[])
        result = AthenaTransformer.get_execution_metadata(cursor)
        self.assertIsNone(result)

    def test_none_values_excluded(self):
        cursor = MagicMock()
        cursor.query_id = "q-1"
        cursor.data_scanned_in_bytes = None
        cursor.engine_execution_time_in_millis = None
        cursor.total_execution_time_in_millis = 200
        cursor.query_queue_time_in_millis = None
        cursor.query_planning_time_in_millis = None
        cursor.service_processing_time_in_millis = None
        cursor.submission_date_time = None
        cursor.completion_date_time = None
        cursor.state = None
        cursor.output_location = None
        result = AthenaTransformer.get_execution_metadata(cursor)

        self.assertIsNotNone(result)
        self.assertEqual(result["query_execution_id"], "q-1")
        self.assertEqual(result["total_execution_time_ms"], 200)
        self.assertNotIn("data_scanned_bytes", result)
        self.assertNotIn("engine_execution_time_ms", result)
        self.assertNotIn("submission_time", result)
        self.assertNotIn("state", result)

    def test_zero_data_scanned_included(self):
        """Zero is valid (query hit cache) and should be included."""
        cursor = MagicMock(spec=[])
        cursor.query_id = "cached-query"
        cursor.data_scanned_in_bytes = 0
        result = AthenaTransformer.get_execution_metadata(cursor)

        self.assertIsNotNone(result)
        self.assertEqual(result.get("data_scanned_bytes"), 0)

    def test_exception_in_cursor_returns_none(self):
        """If cursor raises on attribute access, returns None gracefully."""

        class BrokenCursor:
            @property
            def query_id(self):
                raise RuntimeError("broken")

        result = AthenaTransformer.get_execution_metadata(BrokenCursor())
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
