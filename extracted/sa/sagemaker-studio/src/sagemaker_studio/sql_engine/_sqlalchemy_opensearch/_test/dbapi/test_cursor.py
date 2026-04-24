"""
Unit tests for OpenSearch DB-API Cursor, QueryExecutor, and ResultConverter.
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
)

# ---------------------------------------------------------------------------
# ResultConverter tests
# ---------------------------------------------------------------------------


class TestResultConverterColumnMetadata:
    """Test ResultConverter.convert_column_metadata."""

    def test_empty_schema(self):
        assert ResultConverter.convert_column_metadata([]) == []

    def test_single_column(self):
        schema = [{"name": "id", "type": "long"}]
        desc = ResultConverter.convert_column_metadata(schema)
        assert len(desc) == 1
        name, type_code, *rest = desc[0]
        assert name == "id"
        assert type_code == "NUMBER"

    def test_multiple_columns(self):
        schema = [
            {"name": "msg", "type": "text"},
            {"name": "count", "type": "integer"},
            {"name": "active", "type": "boolean"},
            {"name": "ts", "type": "date"},
        ]
        desc = ResultConverter.convert_column_metadata(schema)
        assert len(desc) == 4
        assert desc[0][0] == "msg"
        assert desc[0][1] == "STRING"
        assert desc[1][1] == "NUMBER"
        assert desc[2][1] == "BOOLEAN"
        assert desc[3][1] == "DATETIME"

    def test_null_ok_always_true(self):
        schema = [{"name": "x", "type": "text"}]
        desc = ResultConverter.convert_column_metadata(schema)
        assert desc[0][6] is True

    def test_missing_type_defaults_to_text(self):
        schema = [{"name": "x"}]
        desc = ResultConverter.convert_column_metadata(schema)
        assert desc[0][1] == "STRING"


class TestResultConverterMapTypeName:
    """Test ResultConverter._map_type_name_to_code."""

    @pytest.mark.parametrize(
        "type_name,expected",
        [
            ("text", "STRING"),
            ("keyword", "STRING"),
            ("long", "NUMBER"),
            ("integer", "NUMBER"),
            ("short", "NUMBER"),
            ("byte", "NUMBER"),
            ("double", "NUMBER"),
            ("float", "NUMBER"),
            ("half_float", "NUMBER"),
            ("scaled_float", "NUMBER"),
            ("boolean", "BOOLEAN"),
            ("date", "DATETIME"),
            ("binary", "BINARY"),
            ("ip", "STRING"),
            ("geo_point", "STRING"),
            ("geo_shape", "STRING"),
            ("object", "JSON"),
            ("nested", "JSON"),
            ("unknown_type", "STRING"),
        ],
    )
    def test_type_mapping(self, type_name, expected):
        assert ResultConverter._map_type_name_to_code(type_name) == expected

    def test_case_insensitive(self):
        assert ResultConverter._map_type_name_to_code("TEXT") == "STRING"
        assert ResultConverter._map_type_name_to_code("Boolean") == "BOOLEAN"


class TestResultConverterDatarows:
    """Test ResultConverter.convert_datarows."""

    def test_empty_datarows(self):
        assert ResultConverter.convert_datarows([], []) == []

    def test_basic_conversion(self):
        schema = [{"type": "text"}, {"type": "long"}]
        datarows = [["hello", 42], ["world", 99]]
        result = ResultConverter.convert_datarows(datarows, schema)
        assert result == [["hello", 42], ["world", 99]]

    def test_null_values(self):
        schema = [{"type": "text"}]
        datarows = [[None]]
        result = ResultConverter.convert_datarows(datarows, schema)
        assert result == [[None]]

    def test_object_json_string(self):
        schema = [{"type": "object"}]
        datarows = [['{"key": "val"}']]
        result = ResultConverter.convert_datarows(datarows, schema)
        assert result == [[{"key": "val"}]]

    def test_nested_json_string(self):
        schema = [{"type": "nested"}]
        datarows = [['[{"a": 1}]']]
        result = ResultConverter.convert_datarows(datarows, schema)
        assert result == [[[{"a": 1}]]]


class TestResultConverterFieldValue:
    """Test ResultConverter._convert_field_value."""

    def test_none_returns_none(self):
        assert ResultConverter._convert_field_value(None, "text") is None

    def test_date_passthrough(self):
        val = "2023-01-01T00:00:00Z"
        assert ResultConverter._convert_field_value(val, "date") == val

    def test_object_json_parse(self):
        assert ResultConverter._convert_field_value('{"a": 1}', "object") == {"a": 1}

    def test_object_invalid_json_passthrough(self):
        assert ResultConverter._convert_field_value("not json", "object") == "not json"

    def test_other_types_passthrough(self):
        assert ResultConverter._convert_field_value(42, "long") == 42
        assert ResultConverter._convert_field_value("hi", "text") == "hi"
        assert ResultConverter._convert_field_value(True, "boolean") is True


# ---------------------------------------------------------------------------
# QueryExecutor tests
# ---------------------------------------------------------------------------


class TestQueryExecutor:
    """Test QueryExecutor."""

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
    def test_execute_query_success(self, mock_sleep, executor):
        expected = {"schema": [], "datarows": []}
        executor.client.transport.perform_request.return_value = expected
        result = executor.execute_query("SELECT 1")
        assert result == expected
        executor.client.transport.perform_request.assert_called_once()

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.retry.time.sleep")
    def test_execute_query_with_dict_params(self, mock_sleep, executor):
        expected = {"schema": [], "datarows": []}
        executor.client.transport.perform_request.return_value = expected
        executor.execute_query("SELECT :val", {"val": 42})
        call_args = executor.client.transport.perform_request.call_args
        body = call_args[1]["body"] if "body" in call_args[1] else call_args[0][2]
        assert body["query"] == "SELECT :val"
        assert "parameters" in body

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.retry.time.sleep")
    def test_execute_query_with_list_params(self, mock_sleep, executor):
        expected = {"schema": [], "datarows": []}
        executor.client.transport.perform_request.return_value = expected
        executor.execute_query("SELECT ?", [42])
        call_args = executor.client.transport.perform_request.call_args
        body = call_args[1]["body"] if "body" in call_args[1] else call_args[0][2]
        assert "parameters" in body

    def test_format_parameters_dict(self, executor):
        result = executor._format_parameters({"name": "test", "val": 42})
        assert result == {"name": "test", "val": 42}

    def test_format_parameters_list(self, executor):
        result = executor._format_parameters([1, "two", True])
        assert result == {"param_0": 1, "param_1": "two", "param_2": True}

    def test_format_parameter_value_basic_types(self, executor):
        assert executor._format_parameter_value(None) is None
        assert executor._format_parameter_value(True) is True
        assert executor._format_parameter_value(42) == 42
        assert executor._format_parameter_value(3.14) == 3.14
        assert executor._format_parameter_value("hello") == "hello"

    def test_format_parameter_value_collections(self, executor):
        assert executor._format_parameter_value([1, 2]) == [1, 2]
        assert executor._format_parameter_value({"a": 1}) == {"a": 1}

    def test_format_parameter_value_other_types(self, executor):
        from datetime import datetime

        dt = datetime(2023, 1, 1)
        assert executor._format_parameter_value(dt) == str(dt)


# ---------------------------------------------------------------------------
# Cursor tests
# ---------------------------------------------------------------------------


class TestCursorInit:
    """Test Cursor initialization."""

    def test_initial_state(self):
        mock_conn = MagicMock()
        cursor = Cursor(mock_conn)
        assert cursor.description is None
        assert cursor.rowcount == -1
        assert cursor.arraysize == 1
        assert cursor._closed is False


class TestCursorExecute:
    """Test Cursor.execute."""

    @pytest.fixture
    def cursor_with_mock(self):
        mock_conn = MagicMock()
        mock_conn.client = MagicMock()
        mock_conn.connection_params = MagicMock()
        mock_conn.connection_params.host = "localhost"
        mock_conn.connection_params.port = 9200
        mock_conn.connection_params.index = "test"
        cursor = Cursor(mock_conn)
        return cursor

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.retry.time.sleep")
    def test_execute_sets_description(self, mock_sleep, cursor_with_mock):
        cursor = cursor_with_mock
        cursor._executor.client.transport.perform_request.return_value = {
            "schema": [{"name": "id", "type": "long"}],
            "datarows": [[1]],
            "total": 1,
        }
        cursor.execute("SELECT id FROM test")
        assert cursor.description is not None
        assert len(cursor.description) == 1
        assert cursor.description[0][0] == "id"

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.retry.time.sleep")
    def test_execute_stores_results(self, mock_sleep, cursor_with_mock):
        cursor = cursor_with_mock
        cursor._executor.client.transport.perform_request.return_value = {
            "schema": [{"name": "val", "type": "text"}],
            "datarows": [["a"], ["b"]],
            "total": 2,
        }
        cursor.execute("SELECT val FROM test")
        assert cursor.rowcount == 2

    def test_execute_raises_when_closed(self, cursor_with_mock):
        cursor = cursor_with_mock
        cursor.close()
        with pytest.raises(InterfaceError, match="Cursor is closed"):
            cursor.execute("SELECT 1")

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.retry.time.sleep")
    def test_execute_resets_state(self, mock_sleep, cursor_with_mock):
        cursor = cursor_with_mock
        cursor._executor.client.transport.perform_request.return_value = {
            "schema": [{"name": "x", "type": "long"}],
            "datarows": [[1], [2]],
            "total": 2,
        }
        cursor.execute("SELECT x FROM t")
        cursor.fetchone()

        # Execute again should reset
        cursor._executor.client.transport.perform_request.return_value = {
            "schema": [{"name": "y", "type": "text"}],
            "datarows": [["a"]],
            "total": 1,
        }
        cursor.execute("SELECT y FROM t")
        assert cursor._current_row == 0
        assert cursor.rowcount == 1


class TestCursorFetch:
    """Test Cursor fetch methods."""

    @pytest.fixture
    def populated_cursor(self):
        mock_conn = MagicMock()
        cursor = Cursor(mock_conn)
        # Manually set up result state
        cursor.description = [
            ("id", "NUMBER", None, None, None, None, True),
            ("name", "STRING", None, None, None, None, True),
        ]
        cursor._result_data = [[1, "alice"], [2, "bob"], [3, "charlie"]]
        cursor._rowcount = 3
        return cursor

    def test_fetchone_returns_first_row(self, populated_cursor):
        row = populated_cursor.fetchone()
        assert row == [1, "alice"]

    def test_fetchone_advances_cursor(self, populated_cursor):
        populated_cursor.fetchone()
        row = populated_cursor.fetchone()
        assert row == [2, "bob"]

    def test_fetchone_returns_none_at_end(self, populated_cursor):
        for _ in range(3):
            populated_cursor.fetchone()
        assert populated_cursor.fetchone() is None

    def test_fetchone_raises_when_closed(self, populated_cursor):
        populated_cursor.close()
        with pytest.raises(InterfaceError, match="Cursor is closed"):
            populated_cursor.fetchone()

    def test_fetchall_returns_all_rows(self, populated_cursor):
        rows = populated_cursor.fetchall()
        assert len(rows) == 3
        assert rows[0] == [1, "alice"]
        assert rows[2] == [3, "charlie"]

    def test_fetchall_returns_remaining_rows(self, populated_cursor):
        populated_cursor.fetchone()  # Skip first
        rows = populated_cursor.fetchall()
        assert len(rows) == 2
        assert rows[0] == [2, "bob"]

    def test_fetchall_returns_empty_at_end(self, populated_cursor):
        populated_cursor.fetchall()
        assert populated_cursor.fetchall() == []

    def test_fetchall_raises_when_closed(self, populated_cursor):
        populated_cursor.close()
        with pytest.raises(InterfaceError, match="Cursor is closed"):
            populated_cursor.fetchall()

    def test_fetchmany_default_size(self, populated_cursor):
        rows = populated_cursor.fetchmany()
        assert len(rows) == 1  # Default arraysize is 1

    def test_fetchmany_custom_size(self, populated_cursor):
        rows = populated_cursor.fetchmany(size=2)
        assert len(rows) == 2
        assert rows[0] == [1, "alice"]
        assert rows[1] == [2, "bob"]

    def test_fetchmany_respects_arraysize(self, populated_cursor):
        populated_cursor.arraysize = 2
        rows = populated_cursor.fetchmany()
        assert len(rows) == 2

    def test_fetchmany_returns_remaining_when_fewer(self, populated_cursor):
        populated_cursor.fetchone()
        populated_cursor.fetchone()
        rows = populated_cursor.fetchmany(size=5)
        assert len(rows) == 1
        assert rows[0] == [3, "charlie"]

    def test_fetchmany_returns_empty_at_end(self, populated_cursor):
        populated_cursor.fetchall()
        assert populated_cursor.fetchmany(size=5) == []

    def test_fetchmany_raises_when_closed(self, populated_cursor):
        populated_cursor.close()
        with pytest.raises(InterfaceError, match="Cursor is closed"):
            populated_cursor.fetchmany()


class TestCursorClose:
    """Test Cursor close behavior."""

    def test_close_resets_state(self):
        mock_conn = MagicMock()
        cursor = Cursor(mock_conn)
        cursor.description = [("x",)]
        cursor._result_data = [[1]]
        cursor._rowcount = 1

        cursor.close()
        assert cursor._closed is True
        assert cursor.description is None
        assert cursor._result_data == []
        assert cursor.rowcount == -1


class TestCursorContextManager:
    """Test Cursor as context manager."""

    def test_context_manager(self):
        mock_conn = MagicMock()
        with Cursor(mock_conn) as cursor:
            assert cursor._closed is False
        assert cursor._closed is True


class TestCursorProcessResult:
    """Test Cursor._process_result."""

    def test_process_result_with_schema_and_data(self):
        mock_conn = MagicMock()
        cursor = Cursor(mock_conn)
        result = {
            "schema": [{"name": "id", "type": "long"}, {"name": "name", "type": "text"}],
            "datarows": [[1, "alice"], [2, "bob"]],
            "total": 2,
        }
        cursor._process_result(result)
        assert len(cursor.description) == 2
        assert len(cursor._result_data) == 2
        assert cursor.rowcount == 2

    def test_process_result_empty(self):
        mock_conn = MagicMock()
        cursor = Cursor(mock_conn)
        result = {"schema": [], "datarows": [], "total": 0}
        cursor._process_result(result)
        assert cursor.description == []
        assert cursor._result_data == []
        assert cursor.rowcount == 0

    def test_process_result_no_total_uses_datarows_length(self):
        mock_conn = MagicMock()
        cursor = Cursor(mock_conn)
        result = {
            "schema": [{"name": "x", "type": "long"}],
            "datarows": [[1], [2], [3]],
        }
        cursor._process_result(result)
        assert cursor.rowcount == 3
