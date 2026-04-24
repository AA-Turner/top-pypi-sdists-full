"""
Extended tests for OpenSearch DB-API Cursor — covers branches
missed by test_cursor.py.
"""

from unittest.mock import MagicMock, patch

import pytest

from sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.cursor import (
    Cursor,
    QueryExecutor,
    ResultConverter,
)
from sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.exceptions import (
    InterfaceError,
    OperationalError,
    ProgrammingError,
)


class TestCursorExecuteExtended:
    """Extended Cursor.execute tests."""

    @pytest.fixture
    def cursor_with_mock(self):
        mock_conn = MagicMock()
        mock_conn.client = MagicMock()
        mock_conn.connection_params = MagicMock()
        mock_conn.connection_params.host = "localhost"
        mock_conn.connection_params.port = 9200
        mock_conn.connection_params.index = "test"
        return Cursor(mock_conn)

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.retry.time.sleep")
    def test_execute_maps_unmapped_exception(self, mock_sleep, cursor_with_mock):
        """Exceptions not already DB-API should be mapped."""
        cursor = cursor_with_mock
        cursor._executor.client.transport.perform_request.side_effect = RuntimeError("boom")
        with pytest.raises(OperationalError):
            cursor.execute("SELECT 1")

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.retry.time.sleep")
    def test_execute_maps_database_error_subclass(self, mock_sleep, cursor_with_mock):
        """DatabaseError subclasses not in the isinstance check should be mapped."""
        from sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.exceptions import (
            DataError,
        )

        cursor = cursor_with_mock
        # DataError is a DatabaseError but not InterfaceError/ProgrammingError/OperationalError
        # so it hits the isinstance check and re-raises directly
        cursor._executor.client.transport.perform_request.side_effect = DataError("data issue")
        with pytest.raises(DataError, match="data issue"):
            cursor.execute("SELECT 1")

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.retry.time.sleep")
    def test_execute_maps_integrity_error(self, mock_sleep, cursor_with_mock):
        """IntegrityError should go through the mapping branch."""
        from sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.exceptions import (
            IntegrityError,
        )

        cursor = cursor_with_mock
        cursor._executor.client.transport.perform_request.side_effect = IntegrityError("conflict")
        # IntegrityError is not in (InterfaceError, ProgrammingError, OperationalError)
        # so it hits map_opensearch_exception which returns it as-is (it's already an Error)
        with pytest.raises(IntegrityError):
            cursor.execute("SELECT 1")

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.retry.time.sleep")
    def test_execute_reraises_interface_error(self, mock_sleep, cursor_with_mock):
        """InterfaceError should be re-raised as-is."""
        cursor = cursor_with_mock
        cursor._executor.client.transport.perform_request.side_effect = InterfaceError("iface err")
        with pytest.raises(InterfaceError, match="iface err"):
            cursor.execute("SELECT 1")

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.retry.time.sleep")
    def test_execute_reraises_programming_error(self, mock_sleep, cursor_with_mock):
        """ProgrammingError should be re-raised as-is."""
        cursor = cursor_with_mock
        cursor._executor.client.transport.perform_request.side_effect = ProgrammingError("bad sql")
        with pytest.raises(ProgrammingError, match="bad sql"):
            cursor.execute("SELECT 1")

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.retry.time.sleep")
    def test_execute_with_empty_result(self, mock_sleep, cursor_with_mock):
        """Execute with empty schema and datarows."""
        cursor = cursor_with_mock
        cursor._executor.client.transport.perform_request.return_value = {
            "schema": [],
            "datarows": [],
            "total": 0,
        }
        cursor.execute("SELECT 1 WHERE 1=0")
        assert cursor.description == []
        assert cursor._result_data == []
        assert cursor.rowcount == 0

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.retry.time.sleep")
    def test_execute_with_parameters(self, mock_sleep, cursor_with_mock):
        """Execute with parameters."""
        cursor = cursor_with_mock
        cursor._executor.client.transport.perform_request.return_value = {
            "schema": [{"name": "val", "type": "long"}],
            "datarows": [[42]],
            "total": 1,
        }
        cursor.execute("SELECT :val", {"val": 42})
        assert cursor.rowcount == 1


class TestProcessResultExtended:
    """Extended _process_result tests."""

    def test_process_result_no_schema(self):
        """Result with no schema should set empty description."""
        mock_conn = MagicMock()
        cursor = Cursor(mock_conn)
        result = {"datarows": [[1, 2]], "total": 1}
        cursor._process_result(result)
        assert cursor.description == []
        assert cursor._result_data == []

    def test_process_result_schema_but_no_datarows(self):
        """Result with schema but no datarows."""
        mock_conn = MagicMock()
        cursor = Cursor(mock_conn)
        result = {
            "schema": [{"name": "id", "type": "long"}],
            "datarows": [],
            "total": 0,
        }
        cursor._process_result(result)
        assert len(cursor.description) == 1
        assert cursor._result_data == []
        assert cursor.rowcount == 0

    def test_process_result_total_none(self):
        """When total is None, use datarows length."""
        mock_conn = MagicMock()
        cursor = Cursor(mock_conn)
        result = {
            "schema": [{"name": "x", "type": "long"}],
            "datarows": [[1], [2]],
            "total": None,
        }
        cursor._process_result(result)
        assert cursor.rowcount == 2


class TestQueryExecutorExtended:
    """Extended QueryExecutor tests."""

    @pytest.fixture
    def executor(self):
        mock_conn = MagicMock()
        mock_conn.client = MagicMock()
        mock_conn.connection_params = MagicMock()
        mock_conn.connection_params.host = "localhost"
        mock_conn.connection_params.port = 9200
        mock_conn.connection_params.index = "test"
        return QueryExecutor(mock_conn)

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.retry.time.sleep")
    def test_execute_query_long_sql_truncated(self, mock_sleep, executor):
        """Long SQL should be truncated in execution context."""
        long_sql = "SELECT " + "a, " * 200
        executor.client.transport.perform_request.return_value = {
            "schema": [],
            "datarows": [],
        }
        # Should not raise
        executor.execute_query(long_sql)

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.retry.time.sleep")
    def test_execute_query_no_parameters(self, mock_sleep, executor):
        """Execute without parameters should not include parameters in body."""
        executor.client.transport.perform_request.return_value = {"schema": [], "datarows": []}
        executor.execute_query("SELECT 1")
        call_args = executor.client.transport.perform_request.call_args
        body = call_args[1]["body"] if "body" in call_args[1] else call_args[0][2]
        assert "parameters" not in body

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.retry.time.sleep")
    def test_execute_query_empty_parameters(self, mock_sleep, executor):
        """Execute with empty dict parameters should not include parameters."""
        executor.client.transport.perform_request.return_value = {"schema": [], "datarows": []}
        executor.execute_query("SELECT 1", {})
        call_args = executor.client.transport.perform_request.call_args
        body = call_args[1]["body"] if "body" in call_args[1] else call_args[0][2]
        # Empty dict is falsy, so parameters should not be added
        assert "parameters" not in body

    def test_format_parameters_empty_dict(self, executor):
        result = executor._format_parameters({})
        assert result == {}

    def test_format_parameters_empty_list(self, executor):
        result = executor._format_parameters([])
        assert result == {}


class TestResultConverterExtended:
    """Extended ResultConverter tests."""

    def test_convert_datarows_field_beyond_schema(self):
        """Fields beyond schema length should use 'text' type."""
        schema = [{"type": "long"}]
        datarows = [[42, "extra_field"]]
        result = ResultConverter.convert_datarows(datarows, schema)
        assert result == [[42, "extra_field"]]

    def test_convert_field_value_nested_json_list(self):
        result = ResultConverter._convert_field_value("[1, 2, 3]", "nested")
        assert result == [1, 2, 3]

    def test_convert_field_value_nested_dict(self):
        """Dict value for nested type should be returned as-is."""
        result = ResultConverter._convert_field_value({"key": "val"}, "nested")
        assert result == {"key": "val"}

    def test_convert_field_value_object_dict(self):
        """Dict value for object type should be returned as-is."""
        result = ResultConverter._convert_field_value({"key": "val"}, "object")
        assert result == {"key": "val"}

    def test_convert_column_metadata_all_types(self):
        """Test all type mappings in column metadata."""
        schema = [
            {"name": "a", "type": "text"},
            {"name": "b", "type": "keyword"},
            {"name": "c", "type": "long"},
            {"name": "d", "type": "integer"},
            {"name": "e", "type": "short"},
            {"name": "f", "type": "byte"},
            {"name": "g", "type": "double"},
            {"name": "h", "type": "float"},
            {"name": "i", "type": "half_float"},
            {"name": "j", "type": "scaled_float"},
            {"name": "k", "type": "boolean"},
            {"name": "l", "type": "date"},
            {"name": "m", "type": "binary"},
            {"name": "n", "type": "ip"},
            {"name": "o", "type": "geo_point"},
            {"name": "p", "type": "geo_shape"},
            {"name": "q", "type": "object"},
            {"name": "r", "type": "nested"},
        ]
        desc = ResultConverter.convert_column_metadata(schema)
        assert len(desc) == 18
        expected_types = [
            "STRING",
            "STRING",
            "NUMBER",
            "NUMBER",
            "NUMBER",
            "NUMBER",
            "NUMBER",
            "NUMBER",
            "NUMBER",
            "NUMBER",
            "BOOLEAN",
            "DATETIME",
            "BINARY",
            "STRING",
            "STRING",
            "STRING",
            "JSON",
            "JSON",
        ]
        for i, expected in enumerate(expected_types):
            assert (
                desc[i][1] == expected
            ), f"Column {schema[i]['name']}: expected {expected}, got {desc[i][1]}"
