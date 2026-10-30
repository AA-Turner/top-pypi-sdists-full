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


class TestAthenaTransformerToSqlalchemyConfig(unittest.TestCase):
    """Tests for to_sqlalchemy_config credential handling."""

    def _base_data(self):
        return {"region": "us-east-1", "work_group": "primary"}

    def test_static_credentials_passed_through(self):
        data = {
            **self._base_data(),
            "aws_access_key_id": "AKIA",
            "aws_secret_access_key": "secret",
            "aws_session_token": "token",
        }
        config = AthenaTransformer.to_sqlalchemy_config(data)

        connect_args = config["connect_args"]
        self.assertEqual(
            config["connection_string"], "awsathena+rest://@athena.us-east-1.amazonaws.com"
        )
        self.assertEqual(connect_args["aws_access_key_id"], "AKIA")
        self.assertNotIn("botocore_session", connect_args)
        self.assertNotIn("credential_provider", connect_args)

    def test_required_fields_include_region(self):
        self.assertEqual(AthenaTransformer.get_required_fields(), ["work_group", "region"])

    def test_missing_region_fails_before_building_connection_string(self):
        with self.assertRaisesRegex(ValueError, "region is required for connection"):
            AthenaTransformer.to_sqlalchemy_config({"work_group": "primary"})

    def test_credential_provider_is_passed_to_the_sdk_owned_dialect(self):
        provider = MagicMock()
        data = {**self._base_data(), "credential_provider": provider}

        config = AthenaTransformer.to_sqlalchemy_config(data)

        self.assertIs(config["connect_args"]["credential_provider"], provider)
        provider.assert_not_called()

    def test_native_cursor_metadata_is_used_directly(self):
        cursor = MagicMock()
        cursor.get_execution_metadata.return_value = {"query_execution_id": "q-native"}

        self.assertEqual(
            AthenaTransformer.get_execution_metadata(cursor),
            {"query_execution_id": "q-native"},
        )

    def test_input_dict_not_mutated(self):
        """to_sqlalchemy_config must not mutate its input (callers may retain the dict)."""
        expiry = datetime(2099, 1, 1, tzinfo=timezone.utc).isoformat()

        def credential_provider():
            return {
                "access_key_id": "AKIA",
                "secret_access_key": "secret",
                "expiration": expiry,
            }

        data = {**self._base_data(), "credential_provider": credential_provider}
        original = dict(data)
        AthenaTransformer.to_sqlalchemy_config(data)

        self.assertEqual(data, original)
        self.assertIn("credential_provider", data)
        self.assertNotIn("botocore_session", data)


if __name__ == "__main__":
    unittest.main()
