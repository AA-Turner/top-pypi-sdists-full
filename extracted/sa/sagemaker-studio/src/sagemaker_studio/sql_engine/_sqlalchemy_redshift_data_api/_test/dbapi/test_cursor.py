"""
Unit tests for the Cursor class and StatementExecutor.

This module tests the statement execution and polling mechanism
with mocked boto3 responses.
"""

import inspect
from decimal import Decimal
from unittest.mock import Mock, patch

import pytest
from botocore.exceptions import ClientError, ParamValidationError
from botocore.model import OperationNotFoundError

from ...dbapi.connection import Connection
from ...dbapi.connection_params import ConnectionParams
from ...dbapi.cursor import Cursor, ResultConverter, StatementExecutor
from ...dbapi.exceptions import (
    InterfaceError,
    OperationalError,
    ProgrammingError,
    StatementExecutionError,
)


@pytest.fixture
def mock_connection():
    """Create a mock connection for testing."""
    connection = Mock(spec=Connection)
    connection.client = Mock()
    connection.connection_params = ConnectionParams(
        cluster_identifier="test-cluster",
        database_name="testdb",
        db_user="test_user",
        region="us-east-1",
    )
    connection.get_transaction_id.return_value = None
    connection._closed = False
    connection._persist_session = True
    connection._session_id = None
    connection._session_keep_alive_seconds = 900
    connection._invalidate_session_if_expired = Mock()
    connection._update_last_query_time = Mock()
    return connection


@pytest.fixture
def statement_executor(mock_connection):
    """Create a StatementExecutor for testing."""
    return StatementExecutor(mock_connection)


@pytest.fixture
def cursor(mock_connection):
    """Create a Cursor for testing."""
    return Cursor(mock_connection)


class TestStatementExecutor:
    """Test cases for the StatementExecutor class."""

    def test_execute_statement_success(self, statement_executor):
        """Test successful statement execution."""
        # Mock execute_statement response
        statement_executor.client.execute_statement.return_value = {"Id": "test-statement-id-123"}

        # Mock describe_statement response (completed)
        statement_executor.client.describe_statement.return_value = {
            "Status": "FINISHED",
            "HasResultSet": True,
            "ResultMetadata": {"ColumnMetadata": []},
            "RecordsUpdated": 0,
        }

        result = statement_executor.execute_statement("SELECT 1")

        assert result["statement_id"] == "test-statement-id-123"
        assert result["status"] == "FINISHED"
        assert result["has_result_set"] is True

        # Verify execute_statement was called with correct parameters
        statement_executor.client.execute_statement.assert_called_once()
        call_args = statement_executor.client.execute_statement.call_args[1]
        assert call_args["Database"] == "testdb"
        assert call_args["Sql"] == "SELECT 1"
        assert call_args["ClusterIdentifier"] == "test-cluster"
        assert call_args["DbUser"] == "test_user"
        assert "StatementName" in call_args

    def test_execute_statement_with_workgroup(self, mock_connection):
        """Test statement execution with workgroup instead of cluster."""
        mock_connection.connection_params.cluster_identifier = None
        mock_connection.connection_params.workgroup_name = "test-workgroup"

        executor = StatementExecutor(mock_connection)

        # Mock responses
        executor.client.execute_statement.return_value = {"Id": "test-id"}
        executor.client.describe_statement.return_value = {"Status": "FINISHED"}

        executor.execute_statement("SELECT 1")

        call_args = executor.client.execute_statement.call_args[1]
        assert "WorkgroupName" in call_args
        assert call_args["WorkgroupName"] == "test-workgroup"
        assert "ClusterIdentifier" not in call_args

    def test_execute_statement_with_secret_arn(self, mock_connection):
        """Test statement execution with secret ARN."""
        mock_connection.connection_params.secret_arn = (
            "arn:aws:secretsmanager:us-east-1:123456789012:secret:test"
        )

        executor = StatementExecutor(mock_connection)

        # Mock responses
        executor.client.execute_statement.return_value = {"Id": "test-id"}
        executor.client.describe_statement.return_value = {"Status": "FINISHED"}

        executor.execute_statement("SELECT 1")

        call_args = executor.client.execute_statement.call_args[1]
        assert "SecretArn" in call_args
        assert call_args["SecretArn"] == "arn:aws:secretsmanager:us-east-1:123456789012:secret:test"
        assert "DbUser" not in call_args

    def test_execute_statement_without_db_user(self, mock_connection):
        """Test statement execution when db_user is None."""
        mock_connection.connection_params.db_user = None

        # Mock responses
        mock_connection.client.execute_statement.return_value = {"Id": "test-id"}
        mock_connection.client.describe_statement.return_value = {"Status": "FINISHED"}

        cursor = Cursor(mock_connection)
        cursor.execute("SELECT 1")

        call_args = mock_connection.client.execute_statement.call_args[1]
        assert "DbUser" not in call_args
        assert call_args["Database"] == "testdb"
        assert call_args["ClusterIdentifier"] == "test-cluster"

    def test_execute_statement_with_transaction(self, statement_executor):
        """Test statement execution within a transaction."""
        statement_executor.connection.get_transaction_id.return_value = "txn-123"

        # Mock responses
        statement_executor.client.execute_statement.return_value = {"Id": "test-id"}
        statement_executor.client.describe_statement.return_value = {"Status": "FINISHED"}

        statement_executor.execute_statement("INSERT INTO test VALUES (1)")

        call_args = statement_executor.client.execute_statement.call_args[1]
        assert call_args["TransactionId"] == "txn-123"

    def test_execute_statement_with_parameters(self, statement_executor):
        """Test statement execution with parameters."""
        # Mock responses
        statement_executor.client.execute_statement.return_value = {"Id": "test-id"}
        statement_executor.client.describe_statement.return_value = {"Status": "FINISHED"}

        parameters = ["test_string", 42, 3.14, True, None]
        statement_executor.execute_statement(
            "SELECT * FROM test WHERE col1 = ? AND col2 = ?", parameters
        )

        call_args = statement_executor.client.execute_statement.call_args[1]
        assert "Parameters" in call_args

        params = call_args["Parameters"]
        assert len(params) == 5

        # Check string parameter
        assert params[0]["name"] == "param_0"
        assert params[0]["value"] == "test_string"

        # Check integer parameter
        assert params[1]["name"] == "param_1"
        assert params[1]["value"] == "42"

        # Check float parameter
        assert params[2]["name"] == "param_2"
        assert params[2]["value"] == "3.14"

        # Check boolean parameter
        assert params[3]["name"] == "param_3"
        assert params[3]["value"] == "true"

        # Check null parameter
        assert params[4]["name"] == "param_4"
        assert params[4]["value"] == ""

    def test_execute_statement_no_cluster_or_workgroup(self, mock_connection):
        """Test error when neither cluster nor workgroup is specified."""
        mock_connection.connection_params.cluster_identifier = None
        mock_connection.connection_params.workgroup_name = None

        executor = StatementExecutor(mock_connection)

        with pytest.raises(
            ProgrammingError, match="Either cluster_identifier or workgroup_name must be specified"
        ):
            executor.execute_statement("SELECT 1")

    def test_polling_with_multiple_statuses(self, statement_executor):
        """Test polling mechanism with multiple status changes."""
        # Mock execute_statement response
        statement_executor.client.execute_statement.return_value = {"Id": "test-id"}

        # Mock describe_statement responses - simulate progression
        status_responses = [
            {"Status": "SUBMITTED"},
            {"Status": "PICKED"},
            {"Status": "STARTED"},
            {"Status": "FINISHED", "HasResultSet": False, "RecordsUpdated": 1},
        ]

        statement_executor.client.describe_statement.side_effect = status_responses

        with patch("time.sleep") as mock_sleep:
            result = statement_executor.execute_statement("UPDATE test SET col1 = 'value'")

        assert result["status"] == "FINISHED"
        assert result["records_updated"] == 1
        assert mock_sleep.call_count == 3  # Called for first 3 statuses

    def test_polling_exponential_backoff(self, statement_executor):
        """Test that polling uses exponential backoff."""
        # Mock execute_statement response
        statement_executor.client.execute_statement.return_value = {"Id": "test-id"}

        # Mock describe_statement responses - multiple running statuses
        status_responses = [
            {"Status": "SUBMITTED"},
            {"Status": "STARTED"},
            {"Status": "STARTED"},
            {"Status": "FINISHED", "HasResultSet": False},
        ]

        statement_executor.client.describe_statement.side_effect = status_responses

        with patch("time.sleep") as mock_sleep:
            statement_executor.execute_statement("SELECT 1")

        # Check that sleep intervals increase (exponential backoff)
        sleep_calls = [call[0][0] for call in mock_sleep.call_args_list]
        assert len(sleep_calls) == 3
        assert sleep_calls[0] == 0.1  # Initial interval
        assert abs(sleep_calls[1] - 0.15) < 1e-10  # 0.1 * 1.5 (handle floating point precision)
        assert abs(sleep_calls[2] - 0.225) < 1e-10  # 0.15 * 1.5 (handle floating point precision)

    def test_mock_client_without_service_model_uses_classic_polling(self, statement_executor):
        assert statement_executor._long_poll_supported() is False

    def test_service_model_without_describe_statement_uses_classic_polling(self, mock_connection):
        operation_model = mock_connection.client.meta.service_model.operation_model
        operation_model.side_effect = OperationNotFoundError("DescribeStatement")

        assert StatementExecutor(mock_connection)._long_poll_supported() is False

    @staticmethod
    def _long_poll_connection(mock_connection):
        operation_model = mock_connection.client.meta.service_model.operation_model
        operation_model.return_value.input_shape.members = {
            "Id": object(),
            "WaitTimeSeconds": object(),
        }
        return mock_connection

    def test_long_poll_passes_wait_time_and_does_not_sleep(self, mock_connection):
        executor = StatementExecutor(self._long_poll_connection(mock_connection))
        executor.client.execute_statement.return_value = {"Id": "test-id"}
        executor.client.describe_statement.side_effect = [
            {"Status": "STARTED"},
            {"Status": "FINISHED", "HasResultSet": False, "RecordsUpdated": 1},
        ]

        with patch("time.sleep") as mock_sleep:
            result = executor.execute_statement("SELECT 1")

        assert result["status"] == "FINISHED"
        mock_sleep.assert_not_called()
        for call in executor.client.describe_statement.call_args_list:
            assert call.kwargs == {"Id": "test-id", "WaitTimeSeconds": 30}

    def test_long_poll_does_not_swallow_other_describe_errors(self, mock_connection):
        executor = StatementExecutor(self._long_poll_connection(mock_connection))
        executor.client.execute_statement.return_value = {"Id": "test-id"}
        executor.client.describe_statement.side_effect = ClientError(
            {"Error": {"Code": "ResourceNotFoundException", "Message": "Statement not found"}},
            "DescribeStatement",
        )

        with pytest.raises(Exception, match="Statement not found"):
            executor.execute_statement("SELECT 1")

        assert executor._long_poll_supported() is True

    def test_statement_failed(self, statement_executor):
        """Test handling of failed statement."""
        # Mock execute_statement response
        statement_executor.client.execute_statement.return_value = {"Id": "test-failed-id"}

        # Mock describe_statement response - failed status
        statement_executor.client.describe_statement.return_value = {
            "Status": "FAILED",
            "Error": "Syntax error in SQL statement",
        }

        with pytest.raises(
            OperationalError, match="Statement execution failed: Syntax error in SQL statement"
        ):
            statement_executor.execute_statement("SELECT * FROM nonexistent_table")

    def test_finished_statement_returns_redshift_query_id(self, statement_executor):
        """FINISHED describe_statement surfaces RedshiftQueryId."""
        statement_executor.client.execute_statement.return_value = {"Id": "stmt-with-ids"}
        statement_executor.client.describe_statement.return_value = {
            "Status": "FINISHED",
            "HasResultSet": True,
            "RedshiftQueryId": 123456,
        }

        result = statement_executor.execute_statement("SELECT 1")

        assert result["statement_id"] == "stmt-with-ids"
        assert result["redshift_query_id"] == 123456

    def test_finished_statement_without_redshift_query_id(self, statement_executor):
        """Missing RedshiftQueryId comes back as None, not KeyError."""
        statement_executor.client.execute_statement.return_value = {"Id": "stmt-no-ids"}
        statement_executor.client.describe_statement.return_value = {"Status": "FINISHED"}

        result = statement_executor.execute_statement("SELECT 1")

        assert result["redshift_query_id"] is None

    def test_statement_failed_error_carries_ids(self, statement_executor):
        """FAILED raises StatementExecutionError with statement_id and redshift_query_id."""
        statement_executor.client.execute_statement.return_value = {"Id": "test-failed-id"}
        statement_executor.client.describe_statement.return_value = {
            "Status": "FAILED",
            "Error": "Syntax error in SQL statement",
            "RedshiftQueryId": 424242,
        }

        with pytest.raises(StatementExecutionError) as exc_info:
            statement_executor.execute_statement("SELECT * FROM nonexistent_table")

        assert exc_info.value.statement_id == "test-failed-id"
        assert exc_info.value.redshift_query_id == 424242

    def test_statement_failed_error_without_redshift_query_id(self, statement_executor):
        """FAILED without RedshiftQueryId still carries statement_id; redshift_query_id is None."""
        statement_executor.client.execute_statement.return_value = {"Id": "test-failed-id"}
        statement_executor.client.describe_statement.return_value = {
            "Status": "FAILED",
            "Error": "Syntax error in SQL statement",
        }

        with pytest.raises(StatementExecutionError) as exc_info:
            statement_executor.execute_statement("SELECT * FROM nonexistent_table")

        assert exc_info.value.statement_id == "test-failed-id"
        assert exc_info.value.redshift_query_id is None

    def test_statement_aborted(self, statement_executor):
        """Test handling of aborted statement."""
        # Mock execute_statement response
        statement_executor.client.execute_statement.return_value = {"Id": "test-aborted-id"}

        # Mock describe_statement response - aborted status
        statement_executor.client.describe_statement.return_value = {"Status": "ABORTED"}

        with pytest.raises(OperationalError, match="Statement was cancelled: test-aborted-id"):
            statement_executor.execute_statement("SELECT 1")

    def test_unknown_status(self, statement_executor):
        """Test handling of unknown statement status."""
        # Mock execute_statement response
        statement_executor.client.execute_statement.return_value = {"Id": "test-unknown-id"}

        # Mock describe_statement response - unknown status
        statement_executor.client.describe_statement.return_value = {"Status": "UNKNOWN_STATUS"}

        with pytest.raises(OperationalError, match="Unknown statement status: UNKNOWN_STATUS"):
            statement_executor.execute_statement("SELECT 1")

    def test_get_statement_result(self, statement_executor):
        """Test getting statement results."""
        mock_result = {
            "Records": [
                [{"stringValue": "value1"}, {"longValue": 123}],
                [{"stringValue": "value2"}, {"longValue": 456}],
            ],
            "ColumnMetadata": [
                {"name": "col1", "typeName": "varchar"},
                {"name": "col2", "typeName": "int8"},
            ],
        }

        statement_executor.client.get_statement_result.return_value = mock_result

        result = statement_executor.get_statement_result("test-statement-id")

        assert result == mock_result
        statement_executor.client.get_statement_result.assert_called_once_with(
            Id="test-statement-id"
        )

    def test_get_statement_result_with_pagination(self, statement_executor):
        """Test getting statement results with pagination token."""
        mock_result = {"Records": [], "ColumnMetadata": []}
        statement_executor.client.get_statement_result.return_value = mock_result

        statement_executor.get_statement_result("test-statement-id", next_token="next-page-token")

        statement_executor.client.get_statement_result.assert_called_once_with(
            Id="test-statement-id", NextToken="next-page-token"
        )


class TestCursor:
    """Test cases for the Cursor class."""

    def test_cursor_initialization(self, cursor):
        """Test cursor initialization."""
        assert cursor.connection is not None
        assert cursor.description is None
        assert cursor._result_data == []
        assert cursor._current_row == 0
        assert cursor._statement_id is None
        assert cursor._closed is False
        assert cursor.rowcount == -1

    def test_execute_simple_statement(self, cursor):
        """Test executing a simple SQL statement."""
        # Mock the executor's execute_statement method
        cursor._executor.execute_statement = Mock(
            return_value={
                "statement_id": "test-stmt-123",
                "status": "FINISHED",
                "has_result_set": False,
                "records_updated": 1,
            }
        )

        cursor.execute("INSERT INTO test VALUES (1, 'test')")

        assert cursor._statement_id == "test-stmt-123"
        cursor._executor.execute_statement.assert_called_once_with(
            "INSERT INTO test VALUES (1, 'test')", None
        )

    def test_execute_stores_redshift_query_id_and_resets_it_on_next_execute(self, cursor):
        """execute() keeps RedshiftQueryId from the result and clears a stale one."""
        cursor._executor.execute_statement = Mock(
            side_effect=[
                {
                    "statement_id": "stmt-1",
                    "status": "FINISHED",
                    "has_result_set": False,
                    "redshift_query_id": 111,
                },
                {"statement_id": "stmt-2", "status": "FINISHED", "has_result_set": False},
            ]
        )

        cursor.execute("SELECT 1")
        assert cursor._redshift_query_id == 111

        cursor.execute("SELECT 2")
        assert cursor._statement_id == "stmt-2"
        assert cursor._redshift_query_id is None

    def test_execute_with_list_parameters(self, cursor):
        """Test executing statement with list parameters."""
        cursor._executor.execute_statement = Mock(
            return_value={
                "statement_id": "test-stmt-456",
                "status": "FINISHED",
                "has_result_set": True,
            }
        )

        parameters = ["test_value", 42]
        cursor.execute("SELECT * FROM test WHERE col1 = ? AND col2 = ?", parameters)

        cursor._executor.execute_statement.assert_called_once_with(
            "SELECT * FROM test WHERE col1 = ? AND col2 = ?", parameters
        )

    def test_execute_with_dict_parameters(self, cursor):
        """Test executing statement with dict parameters."""
        cursor._executor.execute_statement = Mock(
            return_value={
                "statement_id": "test-stmt-789",
                "status": "FINISHED",
                "has_result_set": True,
            }
        )

        parameters = {"param1": "test_value", "param2": 42}
        cursor.execute("SELECT * FROM test WHERE col1 = :param1 AND col2 = :param2", parameters)

        # Dict parameters should be preserved as dict for named parameter support
        cursor._executor.execute_statement.assert_called_once_with(
            "SELECT * FROM test WHERE col1 = :param1 AND col2 = :param2", parameters
        )

    def test_execute_closed_cursor(self, cursor):
        """Test executing on a closed cursor raises error."""
        cursor.close()

        with pytest.raises(InterfaceError, match="Cursor is closed"):
            cursor.execute("SELECT 1")

    def test_execute_resets_cursor_state(self, cursor):
        """Test that execute resets cursor state."""
        # Set some initial state
        cursor.description = [("col1", "varchar")]
        cursor._result_data = [["old_data"]]
        cursor._current_row = 5
        cursor._statement_id = "old-statement-id"

        cursor._executor.execute_statement = Mock(
            return_value={
                "statement_id": "new-stmt-id",
                "status": "FINISHED",
                "has_result_set": False,
            }
        )

        cursor.execute("SELECT 2")

        # State should be reset
        assert cursor.description is None
        assert cursor._result_data == []
        assert cursor._current_row == 0
        assert cursor._statement_id == "new-stmt-id"

    def test_fetch_methods_no_result_set(self, cursor):
        """Test fetch methods when there's no result set."""
        # Execute a statement without results
        cursor._executor.execute_statement = Mock(
            return_value={
                "statement_id": "test-stmt-123",
                "status": "FINISHED",
                "has_result_set": False,
                "records_updated": 1,
            }
        )

        cursor.execute("INSERT INTO test VALUES (1)")

        # Fetch methods should return None/empty list for non-result statements
        assert cursor.fetchone() is None
        assert cursor.fetchall() == []
        assert cursor.fetchmany(5) == []

    def test_cursor_close(self, cursor):
        """Test cursor close method."""
        # Set some state
        cursor.description = [("col1", "varchar")]
        cursor._result_data = [["data"]]
        cursor._current_row = 1
        cursor._statement_id = "stmt-id"
        cursor._redshift_query_id = 123

        cursor.close()

        assert cursor._closed is True
        assert cursor.description is None
        assert cursor._result_data == []
        assert cursor._current_row == 0
        assert cursor._statement_id is None
        assert cursor._redshift_query_id is None

    def test_cursor_context_manager(self, cursor):
        """Test cursor as context manager."""
        with cursor as c:
            assert c is cursor
            assert not cursor._closed

        # Should be closed after exiting context
        assert cursor._closed

    def test_cursor_rowcount_property(self, cursor):
        """Test cursor rowcount property."""
        # Should return -1 until properly implemented in task 7
        assert cursor.rowcount == -1


class TestStatementExecutorErrorHandling:
    """Test error handling in StatementExecutor."""

    def test_boto3_client_error_mapping(self, statement_executor):
        """Test that boto3 ClientError exceptions are properly mapped."""
        # Mock execute_statement to raise ClientError
        client_error = ClientError(
            error_response={
                "Error": {"Code": "ValidationException", "Message": "Invalid SQL syntax"}
            },
            operation_name="ExecuteStatement",
        )

        statement_executor.client.execute_statement.side_effect = client_error

        with pytest.raises(Exception):  # Should be mapped to appropriate DB-API exception
            statement_executor.execute_statement("INVALID SQL")


class TestParameterFormatting:
    """Test parameter formatting functionality."""

    def test_format_parameters_various_types(self, statement_executor):
        """Test formatting of various parameter types."""
        parameters = [
            "string_value",
            42,
            3.14159,
            True,
            False,
            None,
            b"bytes_value",  # Should be converted to string
        ]

        formatted = statement_executor._format_parameters(parameters)

        assert len(formatted) == 7

        # String parameter
        assert formatted[0] == {"name": "param_0", "value": "string_value"}

        # Integer parameter
        assert formatted[1] == {"name": "param_1", "value": "42"}

        # Float parameter
        assert formatted[2] == {"name": "param_2", "value": "3.14159"}

        # Boolean parameters
        assert formatted[3] == {"name": "param_3", "value": "true"}
        assert formatted[4] == {"name": "param_4", "value": "false"}

        # Null parameter
        assert formatted[5] == {"name": "param_5", "value": ""}

        # Bytes parameter (converted to string)
        assert formatted[6] == {"name": "param_6", "value": "b'bytes_value'"}

    def test_format_parameters_empty_list(self, statement_executor):
        """Test formatting empty parameter list."""
        formatted = statement_executor._format_parameters([])
        assert formatted == []

    def test_format_parameters_complex_types(self, statement_executor):
        """Test formatting of complex types that get converted to strings."""
        import datetime

        parameters = [datetime.date(2023, 12, 25), {"key": "value"}, [1, 2, 3]]

        formatted = statement_executor._format_parameters(parameters)

        assert len(formatted) == 3

        # All should be converted to string values
        assert all(isinstance(param["value"], str) for param in formatted)
        assert formatted[0]["value"] == "2023-12-25"
        assert formatted[1]["value"] == "{'key': 'value'}"
        assert formatted[2]["value"] == "[1, 2, 3]"

    def test_format_parameters_named_dict(self, statement_executor):
        """Test formatting of named parameters (dict)."""
        parameters = {
            "name": "John Doe",
            "age": 30,
            "active": True,
            "salary": 75000.50,
            "notes": None,
        }

        formatted = statement_executor._format_parameters(parameters)

        assert len(formatted) == 5

        # Check that parameter names are preserved
        param_names = {param["name"] for param in formatted}
        expected_names = {"name", "age", "active", "salary", "notes"}
        assert param_names == expected_names

        # Check specific parameter values (all should be strings for Data API)
        param_dict = {param["name"]: param["value"] for param in formatted}

        assert param_dict["name"] == "John Doe"
        assert param_dict["age"] == "30"
        assert param_dict["active"] == "true"
        assert param_dict["salary"] == "75000.5"
        assert param_dict["notes"] == ""  # Empty string for NULL


class TestStatementExecutorIntegration:
    """Integration tests for StatementExecutor with realistic scenarios."""

    def test_complete_select_statement_flow(self, statement_executor):
        """Test complete flow for a SELECT statement."""
        # Mock execute_statement response
        statement_executor.client.execute_statement.return_value = {"Id": "select-stmt-123"}

        # Mock describe_statement response
        statement_executor.client.describe_statement.return_value = {
            "Status": "FINISHED",
            "HasResultSet": True,
            "ResultMetadata": {
                "ColumnMetadata": [
                    {"name": "id", "typeName": "int8"},
                    {"name": "name", "typeName": "varchar"},
                ]
            },
            "RecordsUpdated": 0,
        }

        result = statement_executor.execute_statement(
            "SELECT id, name FROM users WHERE active = ?", [True]
        )

        assert result["statement_id"] == "select-stmt-123"
        assert result["status"] == "FINISHED"
        assert result["has_result_set"] is True
        assert result["records_updated"] == 0
        assert result["result_metadata"] is not None

    def test_complete_insert_statement_flow(self, statement_executor):
        """Test complete flow for an INSERT statement."""
        # Mock execute_statement response
        statement_executor.client.execute_statement.return_value = {"Id": "insert-stmt-456"}

        # Mock describe_statement response
        statement_executor.client.describe_statement.return_value = {
            "Status": "FINISHED",
            "HasResultSet": False,
            "RecordsUpdated": 1,
        }

        result = statement_executor.execute_statement(
            "INSERT INTO users (name, email, active) VALUES (?, ?, ?)",
            ["John Doe", "john@example.com", True],
        )

        assert result["statement_id"] == "insert-stmt-456"
        assert result["status"] == "FINISHED"
        assert result["has_result_set"] is False
        assert result["records_updated"] == 1

    def test_transaction_statement_flow(self, statement_executor):
        """Test statement execution within a transaction."""
        # Set up transaction
        statement_executor.connection.get_transaction_id.return_value = "txn-abc123"

        # Mock execute_statement response
        statement_executor.client.execute_statement.return_value = {"Id": "txn-stmt-789"}

        # Mock describe_statement response
        statement_executor.client.describe_statement.return_value = {
            "Status": "FINISHED",
            "HasResultSet": False,
            "RecordsUpdated": 5,
        }

        result = statement_executor.execute_statement(
            "UPDATE users SET last_login = ? WHERE active = ?", ["2023-12-25 10:30:00", True]
        )

        # Verify transaction ID was included in the request
        call_args = statement_executor.client.execute_statement.call_args[1]
        assert call_args["TransactionId"] == "txn-abc123"

        assert result["records_updated"] == 5


class TestResultConverter:
    """Test cases for the ResultConverter class."""

    def test_convert_column_metadata_basic_types(self):
        """Test conversion of basic column metadata."""
        column_metadata = [
            {"name": "id", "typeName": "int8", "precision": None, "scale": None, "nullable": False},
            {
                "name": "name",
                "typeName": "varchar",
                "precision": 255,
                "scale": None,
                "nullable": True,
            },
            {"name": "price", "typeName": "numeric", "precision": 10, "scale": 2, "nullable": True},
        ]

        description = ResultConverter.convert_column_metadata(column_metadata)

        assert len(description) == 3

        # Check id column
        assert description[0][0] == "id"
        assert description[0][1] == "NUMBER"
        assert description[0][4] is None  # precision
        assert description[0][5] is None  # scale
        assert description[0][6] is False  # nullable

        # Check name column
        assert description[1][0] == "name"
        assert description[1][1] == "STRING"
        assert description[1][4] == 255  # precision
        assert description[1][6] is True  # nullable

        # Check price column
        assert description[2][0] == "price"
        assert description[2][1] == "NUMBER"
        assert description[2][4] == 10  # precision
        assert description[2][5] == 2  # scale

    def test_convert_column_metadata_redshift_types(self):
        """Test conversion of Redshift-specific types."""
        column_metadata = [
            {"name": "json_data", "typeName": "super"},
            {"name": "location", "typeName": "geometry"},
            {"name": "created_at", "typeName": "timestamptz"},
            {"name": "is_active", "typeName": "bool"},
        ]

        description = ResultConverter.convert_column_metadata(column_metadata)

        assert description[0][1] == "JSON"  # super -> JSON
        assert description[1][1] == "BINARY"  # geometry -> BINARY
        assert description[2][1] == "DATETIME"  # timestamptz -> DATETIME
        assert description[3][1] == "BOOLEAN"  # bool -> BOOLEAN

    def test_map_type_name_to_code(self):
        """Test type name mapping."""
        # String types
        assert ResultConverter._map_type_name_to_code("varchar") == "STRING"
        assert ResultConverter._map_type_name_to_code("char") == "STRING"
        assert ResultConverter._map_type_name_to_code("text") == "STRING"

        # Numeric types
        assert ResultConverter._map_type_name_to_code("int8") == "NUMBER"
        assert ResultConverter._map_type_name_to_code("integer") == "NUMBER"
        assert ResultConverter._map_type_name_to_code("numeric") == "NUMBER"
        assert ResultConverter._map_type_name_to_code("float8") == "NUMBER"

        # Boolean types
        assert ResultConverter._map_type_name_to_code("bool") == "BOOLEAN"
        assert ResultConverter._map_type_name_to_code("boolean") == "BOOLEAN"

        # Date/time types
        assert ResultConverter._map_type_name_to_code("date") == "DATETIME"
        assert ResultConverter._map_type_name_to_code("timestamp") == "DATETIME"

        # Redshift specific
        assert ResultConverter._map_type_name_to_code("super") == "JSON"
        assert ResultConverter._map_type_name_to_code("geometry") == "BINARY"

        # Unknown type defaults to STRING
        assert ResultConverter._map_type_name_to_code("unknown_type") == "STRING"

    def test_convert_records_various_types(self):
        """Test conversion of records with various data types."""
        records = [
            [
                {"stringValue": "John Doe"},
                {"longValue": 42},
                {"doubleValue": 3.14},
                {"booleanValue": True},
                {"isNull": True},
                {"stringValue": "2023-12-25"},
            ],
            [
                {"stringValue": "Jane Smith"},
                {"longValue": 24},
                {"doubleValue": 2.71},
                {"booleanValue": False},
                {"stringValue": "not null"},
                {"stringValue": "2023-12-26"},
            ],
        ]

        column_metadata = [
            {"typeName": "varchar"},
            {"typeName": "int8"},
            {"typeName": "float8"},
            {"typeName": "bool"},
            {"typeName": "varchar"},
            {"typeName": "date"},
        ]

        converted = ResultConverter.convert_records(records, column_metadata)

        assert len(converted) == 2

        # First row
        assert converted[0][0] == "John Doe"
        assert converted[0][1] == 42
        assert converted[0][2] == 3.14
        assert converted[0][3] is True
        assert converted[0][4] is None  # NULL value
        assert converted[0][5] == "2023-12-25"

        # Second row
        assert converted[1][0] == "Jane Smith"
        assert converted[1][1] == 24
        assert converted[1][2] == 2.71
        assert converted[1][3] is False
        assert converted[1][4] == "not null"
        assert converted[1][5] == "2023-12-26"

    def test_convert_field_value_null(self):
        """Test conversion of NULL field values."""
        field = {"isNull": True}
        result = ResultConverter._convert_field_value(field, "varchar")
        assert result is None

    def test_convert_field_value_string(self):
        """Test conversion of string field values."""
        field = {"stringValue": "test string"}
        result = ResultConverter._convert_field_value(field, "varchar")
        assert result == "test string"

    def test_convert_field_value_decimal(self):
        """Test NUMERIC/DECIMAL stringValue is returned as an exact Decimal."""
        convert = ResultConverter._convert_field_value

        assert convert({"stringValue": "0.0875"}, "numeric") == Decimal("0.0875")
        assert convert({"stringValue": "-0.35"}, "decimal") == Decimal("-0.35")

        full_precision = convert({"stringValue": "1234567890.1234567890"}, "numeric")
        assert str(full_precision) == "1234567890.1234567890"

    def test_convert_field_value_decimal_invalid_falls_back_to_string(self):
        """Test an unparseable DECIMAL value falls back to the raw string."""
        assert ResultConverter._convert_field_value({"stringValue": "n/a"}, "numeric") == "n/a"

    def test_convert_records_decimal_column(self):
        """Test DECIMAL conversion through the convert_records path."""
        records = [[{"stringValue": "123.45"}, {"stringValue": "0.0875"}]]
        column_metadata = [{"typeName": "numeric"}, {"typeName": "decimal"}]

        assert ResultConverter.convert_records(records, column_metadata) == [
            [Decimal("123.45"), Decimal("0.0875")]
        ]

    def test_convert_field_value_numbers(self):
        """Test conversion of numeric field values."""
        # Long value
        field = {"longValue": 123456}
        result = ResultConverter._convert_field_value(field, "int8")
        assert result == 123456

        # Double value
        field = {"doubleValue": 123.456}
        result = ResultConverter._convert_field_value(field, "float8")
        assert result == 123.456

    def test_convert_field_value_boolean(self):
        """Test conversion of boolean field values."""
        field = {"booleanValue": True}
        result = ResultConverter._convert_field_value(field, "bool")
        assert result is True

        field = {"booleanValue": False}
        result = ResultConverter._convert_field_value(field, "bool")
        assert result is False

    def test_convert_field_value_blob(self):
        """Test conversion of blob field values."""
        field = {"blobValue": b"binary data"}
        result = ResultConverter._convert_field_value(field, "geometry")
        assert result == b"binary data"

    def test_convert_field_value_array(self):
        """Test conversion of array field values (SUPER type)."""
        field = {"arrayValue": [{"stringValue": "item1"}, {"stringValue": "item2"}]}
        result = ResultConverter._convert_field_value(field, "super")
        assert result == [{"stringValue": "item1"}, {"stringValue": "item2"}]

    def test_convert_field_value_unknown_field_type(self):
        """Test conversion of unknown field types."""
        field = {"unknownField": "some value"}
        result = ResultConverter._convert_field_value(field, "varchar")
        assert result == field  # Should return the field as-is


class TestCursorResultProcessing:
    """Test cases for cursor result processing functionality."""

    @pytest.fixture
    def cursor_with_results(self, mock_connection):
        """Create a cursor with mocked result data."""
        cursor = Cursor(mock_connection)

        # Mock executor to return result data
        cursor._executor.execute_statement = Mock(
            return_value={
                "statement_id": "test-stmt-123",
                "status": "FINISHED",
                "has_result_set": True,
                "result_metadata": {
                    "ColumnMetadata": [
                        {"name": "id", "typeName": "int8"},
                        {"name": "name", "typeName": "varchar"},
                    ]
                },
            }
        )

        cursor._executor.get_statement_result = Mock()
        return cursor

    def test_execute_with_result_metadata(self, cursor_with_results):
        """Test that execute properly sets up result metadata."""
        cursor_with_results.execute("SELECT id, name FROM users")

        # Check that description is set
        assert cursor_with_results.description is not None
        assert len(cursor_with_results.description) == 2
        assert cursor_with_results.description[0][0] == "id"
        assert cursor_with_results.description[1][0] == "name"

        # Check result set flags
        assert cursor_with_results._has_result_set is True
        assert cursor_with_results._statement_id == "test-stmt-123"

    def test_fetchone_single_batch(self, cursor_with_results):
        """Test fetchone with single batch of results."""
        # Set up mock result data
        cursor_with_results._executor.get_statement_result.return_value = {
            "Records": [
                [{"longValue": 1}, {"stringValue": "Alice"}],
                [{"longValue": 2}, {"stringValue": "Bob"}],
            ],
            "ColumnMetadata": [
                {"name": "id", "typeName": "int8"},
                {"name": "name", "typeName": "varchar"},
            ],
        }

        cursor_with_results.execute("SELECT id, name FROM users")

        # First fetchone should load data and return first row
        row1 = cursor_with_results.fetchone()
        assert row1 == [1, "Alice"]

        # Second fetchone should return second row
        row2 = cursor_with_results.fetchone()
        assert row2 == [2, "Bob"]

        # Third fetchone should return None
        row3 = cursor_with_results.fetchone()
        assert row3 is None

    def test_fetchall_single_batch(self, cursor_with_results):
        """Test fetchall with single batch of results."""
        cursor_with_results._executor.get_statement_result.return_value = {
            "Records": [
                [{"longValue": 1}, {"stringValue": "Alice"}],
                [{"longValue": 2}, {"stringValue": "Bob"}],
                [{"longValue": 3}, {"stringValue": "Charlie"}],
            ],
            "ColumnMetadata": [
                {"name": "id", "typeName": "int8"},
                {"name": "name", "typeName": "varchar"},
            ],
        }

        cursor_with_results.execute("SELECT id, name FROM users")

        rows = cursor_with_results.fetchall()
        assert len(rows) == 3
        assert rows[0] == [1, "Alice"]
        assert rows[1] == [2, "Bob"]
        assert rows[2] == [3, "Charlie"]

        # Subsequent fetchall should return empty list
        rows2 = cursor_with_results.fetchall()
        assert rows2 == []

    def test_fetchmany_default_size(self, cursor_with_results):
        """Test fetchmany with default arraysize."""
        cursor_with_results._executor.get_statement_result.return_value = {
            "Records": [
                [{"longValue": 1}, {"stringValue": "Alice"}],
                [{"longValue": 2}, {"stringValue": "Bob"}],
                [{"longValue": 3}, {"stringValue": "Charlie"}],
            ],
            "ColumnMetadata": [
                {"name": "id", "typeName": "int8"},
                {"name": "name", "typeName": "varchar"},
            ],
        }

        cursor_with_results.execute("SELECT id, name FROM users")

        # Default arraysize is 1
        rows = cursor_with_results.fetchmany()
        assert len(rows) == 1
        assert rows[0] == [1, "Alice"]

    def test_fetchmany_custom_size(self, cursor_with_results):
        """Test fetchmany with custom size."""
        cursor_with_results._executor.get_statement_result.return_value = {
            "Records": [
                [{"longValue": 1}, {"stringValue": "Alice"}],
                [{"longValue": 2}, {"stringValue": "Bob"}],
                [{"longValue": 3}, {"stringValue": "Charlie"}],
            ],
            "ColumnMetadata": [
                {"name": "id", "typeName": "int8"},
                {"name": "name", "typeName": "varchar"},
            ],
        }

        cursor_with_results.execute("SELECT id, name FROM users")

        # Fetch 2 rows
        rows = cursor_with_results.fetchmany(2)
        assert len(rows) == 2
        assert rows[0] == [1, "Alice"]
        assert rows[1] == [2, "Bob"]

        # Fetch remaining row
        rows2 = cursor_with_results.fetchmany(2)
        assert len(rows2) == 1
        assert rows2[0] == [3, "Charlie"]

    def test_pagination_handling(self, cursor_with_results):
        """Test pagination with multiple batches."""
        # First batch with next token
        first_batch = {
            "Records": [
                [{"longValue": 1}, {"stringValue": "Alice"}],
                [{"longValue": 2}, {"stringValue": "Bob"}],
            ],
            "ColumnMetadata": [
                {"name": "id", "typeName": "int8"},
                {"name": "name", "typeName": "varchar"},
            ],
            "NextToken": "next-page-token",
        }

        # Second batch without next token (last page)
        second_batch = {
            "Records": [
                [{"longValue": 3}, {"stringValue": "Charlie"}],
                [{"longValue": 4}, {"stringValue": "David"}],
            ],
            "ColumnMetadata": [
                {"name": "id", "typeName": "int8"},
                {"name": "name", "typeName": "varchar"},
            ],
        }

        # Mock get_statement_result to return different batches
        cursor_with_results._executor.get_statement_result.side_effect = [first_batch, second_batch]

        cursor_with_results.execute("SELECT id, name FROM users")

        # Fetch all rows - should trigger pagination
        rows = cursor_with_results.fetchall()

        assert len(rows) == 4
        assert rows[0] == [1, "Alice"]
        assert rows[1] == [2, "Bob"]
        assert rows[2] == [3, "Charlie"]
        assert rows[3] == [4, "David"]

        # Verify get_statement_result was called twice
        assert cursor_with_results._executor.get_statement_result.call_count == 2

        # Check the calls - first without token, second with token
        calls = cursor_with_results._executor.get_statement_result.call_args_list
        # Each call now includes execution_context as the third argument
        assert calls[0][0][:2] == ("test-stmt-123", None)  # Check first two args
        assert calls[1][0][:2] == ("test-stmt-123", "next-page-token")  # Check first two args

    def test_fetch_closed_cursor(self, cursor_with_results):
        """Test that fetch methods raise error on closed cursor."""
        cursor_with_results.close()

        with pytest.raises(InterfaceError, match="Cursor is closed"):
            cursor_with_results.fetchone()

        with pytest.raises(InterfaceError, match="Cursor is closed"):
            cursor_with_results.fetchall()

        with pytest.raises(InterfaceError, match="Cursor is closed"):
            cursor_with_results.fetchmany()

    def test_result_loading_error_handling(self, cursor_with_results):
        """Test error handling during result loading."""
        cursor_with_results._executor.get_statement_result.side_effect = Exception("API Error")

        cursor_with_results.execute("SELECT id, name FROM users")

        with pytest.raises(OperationalError, match="AWS service error: API Error"):
            cursor_with_results.fetchone()

    def test_mixed_fetch_operations(self, cursor_with_results):
        """Test mixing different fetch operations."""
        cursor_with_results._executor.get_statement_result.return_value = {
            "Records": [
                [{"longValue": 1}, {"stringValue": "Alice"}],
                [{"longValue": 2}, {"stringValue": "Bob"}],
                [{"longValue": 3}, {"stringValue": "Charlie"}],
                [{"longValue": 4}, {"stringValue": "David"}],
                [{"longValue": 5}, {"stringValue": "Eve"}],
            ],
            "ColumnMetadata": [
                {"name": "id", "typeName": "int8"},
                {"name": "name", "typeName": "varchar"},
            ],
        }

        cursor_with_results.execute("SELECT id, name FROM users")

        # Fetch one row
        row1 = cursor_with_results.fetchone()
        assert row1 == [1, "Alice"]

        # Fetch two rows
        rows2 = cursor_with_results.fetchmany(2)
        assert len(rows2) == 2
        assert rows2[0] == [2, "Bob"]
        assert rows2[1] == [3, "Charlie"]

        # Fetch remaining rows
        remaining = cursor_with_results.fetchall()
        assert len(remaining) == 2
        assert remaining[0] == [4, "David"]
        assert remaining[1] == [5, "Eve"]

    def test_rowcount_for_select_statement(self, cursor_with_results):
        """Test rowcount for SELECT statements."""
        cursor_with_results.execute("SELECT id, name FROM users")

        # For SELECT statements, rowcount should be -1
        assert cursor_with_results.rowcount == -1

    def test_rowcount_for_insert_statement(self, cursor_with_results):
        """Test rowcount for INSERT statements."""
        cursor_with_results._executor.execute_statement = Mock(
            return_value={
                "statement_id": "insert-stmt-123",
                "status": "FINISHED",
                "has_result_set": False,
                "records_updated": 3,
            }
        )

        cursor_with_results.execute("INSERT INTO users VALUES (...)")

        # For INSERT statements, rowcount should reflect records updated
        assert cursor_with_results.rowcount == 3


class TestCursorLargeResultSets:
    """Test cases for handling large result sets and performance."""

    @pytest.fixture
    def cursor_large_results(self, mock_connection):
        """Create a cursor for testing large result sets."""
        cursor = Cursor(mock_connection)
        cursor._executor.execute_statement = Mock(
            return_value={
                "statement_id": "large-stmt-123",
                "status": "FINISHED",
                "has_result_set": True,
                "result_metadata": {
                    "ColumnMetadata": [
                        {"name": "id", "typeName": "int8"},
                        {"name": "data", "typeName": "varchar"},
                    ]
                },
            }
        )
        cursor._executor.get_statement_result = Mock()
        return cursor

    def test_large_result_set_pagination(self, cursor_large_results):
        """Test handling of large result sets with multiple pages."""
        # Simulate 3 pages of results
        pages = []
        for page in range(3):
            records = []
            for i in range(1000):  # 1000 records per page
                record_id = page * 1000 + i + 1
                records.append([{"longValue": record_id}, {"stringValue": f"data_{record_id}"}])

            page_data = {
                "Records": records,
                "ColumnMetadata": [
                    {"name": "id", "typeName": "int8"},
                    {"name": "data", "typeName": "varchar"},
                ],
            }

            # Add NextToken for all pages except the last
            if page < 2:
                page_data["NextToken"] = f"page_{page + 1}_token"

            pages.append(page_data)

        cursor_large_results._executor.get_statement_result.side_effect = pages
        cursor_large_results.execute("SELECT id, data FROM large_table")

        # Fetch all results
        all_rows = cursor_large_results.fetchall()

        # Should have 3000 total rows
        assert len(all_rows) == 3000

        # Check first and last rows
        assert all_rows[0] == [1, "data_1"]
        assert all_rows[-1] == [3000, "data_3000"]

        # Verify all pages were fetched
        assert cursor_large_results._executor.get_statement_result.call_count == 3

    def test_incremental_loading_with_fetchmany(self, cursor_large_results):
        """Test that results are loaded incrementally with fetchmany."""
        # Create two pages of results
        page1 = {
            "Records": [[{"longValue": i}, {"stringValue": f"data_{i}"}] for i in range(1, 501)],
            "ColumnMetadata": [
                {"name": "id", "typeName": "int8"},
                {"name": "data", "typeName": "varchar"},
            ],
            "NextToken": "page_2_token",
        }

        page2 = {
            "Records": [[{"longValue": i}, {"stringValue": f"data_{i}"}] for i in range(501, 1001)],
            "ColumnMetadata": [
                {"name": "id", "typeName": "int8"},
                {"name": "data", "typeName": "varchar"},
            ],
        }

        cursor_large_results._executor.get_statement_result.side_effect = [page1, page2]
        cursor_large_results.execute("SELECT id, data FROM large_table")

        # Fetch first 100 rows - should only load first page
        rows1 = cursor_large_results.fetchmany(100)
        assert len(rows1) == 100
        assert cursor_large_results._executor.get_statement_result.call_count == 1

        # Fetch next 600 rows - should load second page to fulfill request
        rows2 = cursor_large_results.fetchmany(600)
        assert (
            len(rows2) == 600
        )  # Should get all 600 requested rows (400 from page 1 + 200 from page 2)
        assert cursor_large_results._executor.get_statement_result.call_count == 2

        # Fetch more rows - should trigger loading of second page
        rows3 = cursor_large_results.fetchmany(100)
        assert len(rows3) == 100
        assert cursor_large_results._executor.get_statement_result.call_count == 2

    def test_various_data_types_conversion(self, cursor_large_results):
        """Test conversion of various Redshift data types."""
        cursor_large_results._executor.get_statement_result.return_value = {
            "Records": [
                [
                    {"longValue": 123},  # int8
                    {"stringValue": "test string"},  # varchar
                    {"doubleValue": 123.456},  # float8
                    {"booleanValue": True},  # bool
                    {"isNull": True},  # NULL
                    {"stringValue": "2023-12-25"},  # date
                    {"stringValue": "2023-12-25 10:30:00"},  # timestamp
                    {"arrayValue": [{"stringValue": "item1"}]},  # super (array)
                    {"blobValue": b"binary_data"},  # geometry/binary
                ]
            ],
            "ColumnMetadata": [
                {"name": "id", "typeName": "int8"},
                {"name": "name", "typeName": "varchar"},
                {"name": "price", "typeName": "float8"},
                {"name": "active", "typeName": "bool"},
                {"name": "deleted_at", "typeName": "timestamp"},
                {"name": "created_date", "typeName": "date"},
                {"name": "updated_at", "typeName": "timestamp"},
                {"name": "metadata", "typeName": "super"},
                {"name": "location", "typeName": "geometry"},
            ],
        }

        cursor_large_results.execute("SELECT * FROM mixed_types_table")

        row = cursor_large_results.fetchone()

        assert row[0] == 123  # int8
        assert row[1] == "test string"  # varchar
        assert row[2] == 123.456  # float8
        assert row[3] is True  # bool
        assert row[4] is None  # NULL
        assert row[5] == "2023-12-25"  # date
        assert row[6] == "2023-12-25 10:30:00"  # timestamp
        assert row[7] == [{"stringValue": "item1"}]  # super
        assert row[8] == b"binary_data"  # geometry

    def test_empty_result_set(self, cursor_large_results):
        """Test handling of empty result sets."""
        cursor_large_results._executor.get_statement_result.return_value = {
            "Records": [],
            "ColumnMetadata": [
                {"name": "id", "typeName": "int8"},
                {"name": "name", "typeName": "varchar"},
            ],
        }

        cursor_large_results.execute("SELECT id, name FROM users WHERE 1=0")

        # All fetch methods should return empty results
        assert cursor_large_results.fetchone() is None
        assert cursor_large_results.fetchall() == []
        assert cursor_large_results.fetchmany(10) == []


class TestCursorGetExecutionMetadata:
    """Tests for Cursor.get_execution_metadata()."""

    def test_returns_none_when_no_statement_executed(self, mock_connection):
        cursor = Cursor(mock_connection)
        assert cursor.get_execution_metadata() is None

    def test_returns_metadata_with_session_and_result_stats(self, mock_connection):
        mock_connection._session_id = "session-xyz"
        cursor = Cursor(mock_connection)
        cursor._statement_id = "stmt-abc"
        cursor._has_result_set = True
        cursor._rowcount = -1
        cursor._result_rows = 50
        cursor._result_size = 2048

        result = cursor.get_execution_metadata()

        assert result["statement_id"] == "stmt-abc"
        assert result["has_result_set"] is True
        assert result["session_id"] == "session-xyz"
        assert result["result_rows"] == 50
        assert result["result_size_bytes"] == 2048
        assert "records_updated" not in result

    def test_includes_records_updated_for_dml(self, mock_connection):
        mock_connection._session_id = None
        cursor = Cursor(mock_connection)
        cursor._statement_id = "stmt-dml"
        cursor._has_result_set = False
        cursor._rowcount = 42
        cursor._result_rows = None
        cursor._result_size = None

        result = cursor.get_execution_metadata()

        assert result["statement_id"] == "stmt-dml"
        assert result["records_updated"] == 42
        assert "session_id" not in result
        assert "result_rows" not in result
        assert "result_size_bytes" not in result

    def test_excludes_none_result_stats(self, mock_connection):
        mock_connection._session_id = "s-1"
        cursor = Cursor(mock_connection)
        cursor._statement_id = "stmt-1"
        cursor._has_result_set = True
        cursor._rowcount = -1
        cursor._result_rows = None
        cursor._result_size = None

        result = cursor.get_execution_metadata()

        assert "result_rows" not in result
        assert "result_size_bytes" not in result

    def test_metadata_includes_redshift_query_id(self, mock_connection):
        cursor = Cursor(mock_connection)
        cursor._statement_id = "stmt-ids"
        cursor._redshift_query_id = 987654

        result = cursor.get_execution_metadata()

        assert result["statement_id"] == "stmt-ids"
        assert result["redshift_query_id"] == 987654
        assert "engine_query_id" not in result

    def test_metadata_omits_redshift_query_id_when_absent(self, mock_connection):
        cursor = Cursor(mock_connection)
        cursor._statement_id = "stmt-no-ids"
        cursor._redshift_query_id = None

        result = cursor.get_execution_metadata()

        assert result["statement_id"] == "stmt-no-ids"
        assert "redshift_query_id" not in result

    def test_metadata_omits_redshift_query_id_when_zero(self, mock_connection):
        """A zero RedshiftQueryId means 'not assigned' and is not emitted."""
        cursor = Cursor(mock_connection)
        cursor._statement_id = "stmt-zero"
        cursor._redshift_query_id = 0

        result = cursor.get_execution_metadata()

        assert result["statement_id"] == "stmt-zero"
        assert "redshift_query_id" not in result

    def test_metadata_omits_redshift_query_id_when_minus_one(self, mock_connection):
        """The Data API reports -1 when Redshift assigned no query id (leader-node-only query)."""
        mock_connection.client.execute_statement.return_value = {"Id": "stmt-leader"}
        mock_connection.client.describe_statement.return_value = {
            "Status": "FINISHED",
            "HasResultSet": True,
            "RedshiftQueryId": -1,
            "RedshiftPid": 1234,
        }
        cursor = Cursor(mock_connection)

        cursor.execute("SELECT 'plain' AS s_plain, NULL::int AS i_null")
        result = cursor.get_execution_metadata()

        assert result["statement_id"] == "stmt-leader"
        assert "redshift_query_id" not in result

    def test_metadata_after_execute_carries_describe_statement_query_id(self, mock_connection):
        """End to end through execute(): RedshiftQueryId from describe_statement is emitted."""
        mock_connection.client.execute_statement.return_value = {"Id": "stmt-e2e"}
        mock_connection.client.describe_statement.return_value = {
            "Status": "FINISHED",
            "HasResultSet": False,
            "RecordsUpdated": 3,
            "RedshiftQueryId": 55,
            "RedshiftPid": 66,
        }
        cursor = Cursor(mock_connection)

        cursor.execute("DELETE FROM t")
        result = cursor.get_execution_metadata()

        assert result["statement_id"] == "stmt-e2e"
        assert result["redshift_query_id"] == 55
        assert result["records_updated"] == 3
        assert "redshift_pid" not in result


# ---------------------------------------------------------------------------
# Feature: remove-redshift-data-api-query-timeout
#
# Support for the clock-independence tests below. The polling loop has no
# time-based exit any more: only the status Redshift reports ends it.
# ---------------------------------------------------------------------------

_NON_TERMINAL_STATUSES = ("SUBMITTED", "PICKED", "STARTED")

# The keys _poll_statement_completion documents on a FINISHED result. redshift_query_id
# is surfaced alongside the eight core fields.
_FINISHED_RESULT_KEYS = {
    "statement_id",
    "status",
    "has_result_set",
    "result_metadata",
    "records_updated",
    "result_rows",
    "result_size",
    "sub_statements",
    "redshift_query_id",
}

# The default each optional key takes when the describe_statement response omits
# the field it reads.
_FINISHED_FIELD_DEFAULTS = {
    "has_result_set": False,
    "result_metadata": None,
    "records_updated": 0,
    "result_rows": None,
    "result_size": None,
    "sub_statements": [],
}

# A FINISHED response carrying every optional field the loop reads, so the
# multi-poll cases assert carried-through values rather than defaults.
_FULL_FINISHED_RESPONSE = {
    "Status": "FINISHED",
    "HasResultSet": True,
    "ResultMetadata": {"ColumnMetadata": [{"name": "col1", "typeName": "varchar"}]},
    "RecordsUpdated": 7,
    "ResultRows": 42,
    "ResultSize": 4096,
    "SubStatements": [{"Id": "sub-1", "Status": "FINISHED"}],
}

_FULL_FINISHED_EXPECTED = {
    "has_result_set": True,
    "result_metadata": {"ColumnMetadata": [{"name": "col1", "typeName": "varchar"}]},
    "records_updated": 7,
    "result_rows": 42,
    "result_size": 4096,
    "sub_statements": [{"Id": "sub-1", "Status": "FINISHED"}],
}


class _SteppingClock:
    """
    Stand-in for time.time() that advances by a fixed step on every call.

    A callable object rather than a Mock with a finite side_effect list: the number of
    clock reads during a run is not the test's to predict, so the stand-in must not be
    exhaustible. Measured against the current loop, the driver's retry helper reads it
    once per poll, so a 60-second step over ~20 polls drives the clock roughly 1260
    seconds forward -- past the removed 300-second cap several times over.
    """

    def __init__(self, step_seconds, start=1_000_000.0):
        self.step_seconds = float(step_seconds)
        self.now = float(start)

    def __call__(self):
        value = self.now
        self.now += self.step_seconds
        return value


def _non_terminal_then_finished(poll_count, finished_response=None):
    """Build poll_count non-terminal describe_statement responses, then one FINISHED."""
    responses = [
        {"Status": _NON_TERMINAL_STATUSES[index % len(_NON_TERMINAL_STATUSES)]}
        for index in range(poll_count)
    ]
    responses.append(dict(finished_response or _FULL_FINISHED_RESPONSE))
    return responses


# (label, seconds the patched clock advances per read). The minutes- and hours-per-call
# clocks race past the removed 300-second cap during the longer sequences; the
# milliseconds-per-call clock barely moves. The outcome must not depend on which.
_CLOCK_BEHAVIORS = [
    ("milliseconds_per_call", 0.001),
    ("minutes_per_call", 60.0),
    ("hours_per_call", 3600.0),
]


class TestPollingIsClockIndependent:
    """
    Feature: remove-redshift-data-api-query-timeout

    Polling runs until Redshift reports a terminal status, with no client-side time
    limit. These cases run in classic polling mode: the fixtures build the client as a
    plain Mock(), whose `members` raises TypeError under `in`, so the long-poll
    capability check fails open. The long-poll modes are covered separately.

    The correctness properties these realize are specified as property-based, but the
    package declares only pytest and has no property-testing dependency,
    so they are parameterized pytest cases over a table of sequences and clocks --
    matching how the rest of this suite is written.
    """

    @pytest.mark.parametrize(
        "clock_label, clock_step",
        _CLOCK_BEHAVIORS,
        ids=[label for label, _ in _CLOCK_BEHAVIORS],
    )
    @pytest.mark.parametrize("poll_count", [1, 3, 20, 45])
    def test_any_number_of_non_terminal_polls_reaches_finished(
        self, statement_executor, poll_count, clock_label, clock_step
    ):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 1: Any number of
        non-terminal polls still reaches a result

        Feature: remove-redshift-data-api-query-timeout, Property 2: The outcome is
        invariant under the wall clock

        Feature: remove-redshift-data-api-query-timeout, Property 3: A FINISHED result
        carries every documented field

        For the 20-poll case this is the task's named scenario: 20 non-terminal
        responses then one FINISHED, with describe_statement expected to be called 21
        times. A reintroduced clock-based exit would raise StatementTimeoutError part
        way through the minutes- and hours-per-call runs instead of returning, so this
        fails loudly rather than quietly polling fewer times.

        **Validates: Requirements 1.1, 1.2, 1.3, 6.2, 8.3**
        """
        statement_executor.client.execute_statement.return_value = {"Id": "long-poll-stmt"}
        statement_executor.client.describe_statement.side_effect = _non_terminal_then_finished(
            poll_count
        )
        clock = _SteppingClock(clock_step)

        with patch("time.sleep"), patch("time.time", new=clock):
            result = statement_executor.execute_statement("SELECT pg_sleep(1000)")

        assert statement_executor.client.describe_statement.call_count == poll_count + 1

        assert result["statement_id"] == "long-poll-stmt"
        assert result["status"] == "FINISHED"
        assert set(result) == _FINISHED_RESULT_KEYS
        for key, expected in _FULL_FINISHED_EXPECTED.items():
            assert result[key] == expected, f"{key} under {clock_label}"

    @pytest.mark.parametrize(
        "response, expected",
        [
            pytest.param(_FULL_FINISHED_RESPONSE, _FULL_FINISHED_EXPECTED, id="all_fields_present"),
            pytest.param(
                {"Status": "FINISHED"},
                _FINISHED_FIELD_DEFAULTS,
                id="no_optional_fields",
            ),
            pytest.param(
                {"Status": "FINISHED", "HasResultSet": True, "ResultRows": 3, "ResultSize": 128},
                {
                    **_FINISHED_FIELD_DEFAULTS,
                    "has_result_set": True,
                    "result_rows": 3,
                    "result_size": 128,
                },
                id="result_set_fields_only",
            ),
            pytest.param(
                {"Status": "FINISHED", "HasResultSet": False, "RecordsUpdated": 11},
                {**_FINISHED_FIELD_DEFAULTS, "records_updated": 11},
                id="dml_fields_only",
            ),
            pytest.param(
                {
                    "Status": "FINISHED",
                    "HasResultSet": False,
                    "ResultMetadata": {},
                    "RecordsUpdated": 0,
                    "ResultRows": 0,
                    "ResultSize": 0,
                    "SubStatements": [],
                },
                {
                    "has_result_set": False,
                    "result_metadata": {},
                    "records_updated": 0,
                    "result_rows": 0,
                    "result_size": 0,
                    "sub_statements": [],
                },
                id="falsy_values_present",
            ),
        ],
    )
    def test_finished_result_carries_every_documented_field(
        self, statement_executor, response, expected
    ):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 3: A FINISHED result
        carries every documented field

        Each case reaches FINISHED after several non-terminal polls, so the payload is
        read off the last response rather than the first. The falsy-values case
        separates `.get(key, default)` from `.get(key) or default`: a present zero or
        empty collection must carry through as itself, not be replaced by the default.

        **Validates: Requirements 1.1, 1.2, 6.2, 8.3**
        """
        statement_executor.client.execute_statement.return_value = {"Id": "fields-stmt"}
        statement_executor.client.describe_statement.side_effect = _non_terminal_then_finished(
            3, finished_response=response
        )

        with patch("time.sleep"), patch("time.time", new=_SteppingClock(60.0)):
            result = statement_executor.execute_statement("SELECT 1")

        assert set(result) == _FINISHED_RESULT_KEYS
        assert result["statement_id"] == "fields-stmt"
        assert result["status"] == "FINISHED"
        for key, value in expected.items():
            assert result[key] == value, key

    @staticmethod
    def _outcome(mock_connection, responses, clock_step):
        """
        Run one statement on a fresh client under a stepping clock and describe what
        came out, so two clock behaviors can be compared as values.
        """
        mock_connection.client = Mock()
        executor = StatementExecutor(mock_connection)
        executor.client.execute_statement.return_value = {"Id": "invariant-stmt"}
        executor.client.describe_statement.side_effect = list(responses)
        clock = _SteppingClock(clock_step)

        with patch("time.sleep"), patch("time.time", new=clock):
            try:
                return ("returned", executor.execute_statement("SELECT 1"))
            except Exception as exc:
                return ("raised", type(exc), str(exc))

    @pytest.mark.parametrize(
        "responses",
        [
            pytest.param(_non_terminal_then_finished(20), id="finishes_after_20_polls"),
            pytest.param(
                _non_terminal_then_finished(6, finished_response={"Status": "FINISHED"}),
                id="finishes_with_no_optional_fields",
            ),
            pytest.param(
                [{"Status": "STARTED"}] * 8 + [{"Status": "FAILED", "Error": "disk full"}],
                id="fails_after_8_polls",
            ),
            pytest.param(
                [{"Status": "SUBMITTED"}] * 8 + [{"Status": "ABORTED"}],
                id="aborts_after_8_polls",
            ),
            pytest.param(
                [{"Status": "PICKED"}] * 8 + [{"Status": "WEDGED"}],
                id="unknown_status_after_8_polls",
            ),
        ],
    )
    def test_outcome_is_invariant_under_the_wall_clock(self, mock_connection, responses):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 2: The outcome is
        invariant under the wall clock

        The same sequence is run under a clock advancing by milliseconds and one jumping
        an hour ahead per read, and the two outcomes are compared as values: the same
        returned result, or the same exception type and message. The hours-per-call run
        drives the patched clock days past the removed 300-second cap, so any surviving
        clock-based exit would make the two disagree.

        **Validates: Requirements 1.1, 1.2, 1.3, 6.2, 8.3**
        """
        milliseconds = self._outcome(mock_connection, responses, 0.001)
        hours = self._outcome(mock_connection, responses, 3600.0)

        assert milliseconds == hours


# ---------------------------------------------------------------------------
# Feature: remove-redshift-data-api-query-timeout
#
# Support for the classic-mode backoff-cap tests below. The schedule starts at
# 0.1 s, multiplies by 1.5 after each poll, and is clamped at 1.0 s (lowered
# from 5.0 s by this change).
# ---------------------------------------------------------------------------

_INITIAL_SLEEP = 0.1
_SLEEP_MULTIPLIER = 1.5
_SLEEP_CAP = 1.0

# 0.1 * 1.5**k first reaches the 1.0 cap at k == 6: the unclamped terms are
# 0.1, 0.15, 0.225, 0.3375, 0.50625, 0.759375, then 1.139... which clamps.
_SATURATION_INDEX = 6


def _expected_backoff_schedule(poll_count):
    """The sleep durations classic mode should request for poll_count non-terminal polls."""
    return [min(_INITIAL_SLEEP * _SLEEP_MULTIPLIER**k, _SLEEP_CAP) for k in range(poll_count)]


class TestClassicBackoffIsCappedAtOneSecond:
    """
    Feature: remove-redshift-data-api-query-timeout

    These cases run in classic polling mode: the fixtures build the client as a plain
    Mock(), whose `members` raises TypeError under `in`, so the long-poll capability
    check fails open and the loop sleeps between polls. The service model is not faked
    here -- the classic path is what these assert.

    `test_polling_exponential_backoff` above remains the small example case; its three
    asserted sleeps (0.1, 0.15, 0.225) all sit below the cap, so it cannot distinguish
    a 1.0 s cap from the old 5.0 s one. These cases carry the schedule past saturation,
    which is where the lowered cap is observable.

    Property 5 is specified as property-based, but the package declares only
    pytest and has no property-testing dependency, so it is realized as
    parameterized pytest cases over a table of poll counts -- matching how the rest of
    this suite is written.
    """

    @staticmethod
    def _recorded_sleeps(statement_executor, poll_count):
        """Run one statement over poll_count non-terminal polls and return the sleeps asked for."""
        statement_executor.client.execute_statement.return_value = {"Id": "backoff-stmt"}
        statement_executor.client.describe_statement.side_effect = _non_terminal_then_finished(
            poll_count
        )

        with patch("time.sleep") as mock_sleep, patch("time.time", new=_SteppingClock(60.0)):
            result = statement_executor.execute_statement("SELECT pg_sleep(1000)")

        assert result["status"] == "FINISHED"
        return [call[0][0] for call in mock_sleep.call_args_list]

    @pytest.mark.parametrize("poll_count", [1, 3, 6, 7, 12, 30])
    def test_classic_backoff_follows_the_capped_geometric_schedule(
        self, statement_executor, poll_count
    ):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 5: Classic backoff
        follows the geometric schedule capped at one second

        For n consecutive non-terminal polls the loop asks for exactly n sleeps, and the
        kth equals min(0.1 * 1.5**k, 1.0). The poll counts straddle saturation: 1, 3 and
        6 stay on the geometric run, while 7, 12 and 30 cross it, so the table covers
        both the growth and the clamp. The terms are compared with pytest.approx because
        the loop reaches them by repeated multiplication rather than by exponentiation.

        **Validates: Requirements 2.5, 10.1, 10.2, 10.3, 11.6**
        """
        sleeps = self._recorded_sleeps(statement_executor, poll_count)

        assert len(sleeps) == poll_count
        assert sleeps == pytest.approx(_expected_backoff_schedule(poll_count))
        assert sleeps[0] == _INITIAL_SLEEP

    @pytest.mark.parametrize("poll_count", [7, 12, 30])
    def test_classic_backoff_saturates_at_exactly_one_second(self, statement_executor, poll_count):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 5: Classic backoff
        follows the geometric schedule capped at one second

        Once the schedule saturates, every later entry is the cap itself rather than a
        value merely near it, so the tail is asserted exactly. This is the assertion
        that distinguishes the new 1.0 s cap from the old 5.0 s one: under a 5.0 s cap
        these entries would read 1.139..., 1.709..., 2.563... and so on.

        **Validates: Requirements 2.5, 10.1, 10.2, 10.3, 11.6**
        """
        sleeps = self._recorded_sleeps(statement_executor, poll_count)
        tail = sleeps[_SATURATION_INDEX:]

        assert tail, "poll count must cross saturation for this case to mean anything"
        assert tail == [_SLEEP_CAP] * len(tail)

    @pytest.mark.parametrize("poll_count", [1, 3, 6, 7, 12, 30])
    def test_no_classic_sleep_exceeds_one_second(self, statement_executor, poll_count):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 5: Classic backoff
        follows the geometric schedule capped at one second

        The cap read as a bound rather than as a schedule: however many polls a
        statement takes, no single client-side wait may exceed 1.0 s. Stated separately
        from the schedule because this is the user-visible guarantee -- completion is
        noticed within a second of Redshift reporting it.

        **Validates: Requirements 2.5, 10.3, 11.6**
        """
        sleeps = self._recorded_sleeps(statement_executor, poll_count)

        assert sleeps, "classic mode must sleep between non-terminal polls"
        assert max(sleeps) <= _SLEEP_CAP
        assert all(sleep > 0 for sleep in sleeps)


# ---------------------------------------------------------------------------
# Feature: remove-redshift-data-api-query-timeout
#
# Support for the request-shape and no-client-wait tests below.
#
# The resolved botocore in this workspace declares DescribeStatementRequest
# members ['Id'] only -- no WaitTimeSeconds -- so the capability check fails
# against the real model and the long-poll branch is unreachable without a
# fake. Every long-poll case here therefore fakes the service model, and no
# case depends on the resolved model declaring the member.
# ---------------------------------------------------------------------------

# The wait every long-poll request must carry. Written as a literal rather than
# imported from the driver on purpose: importing LONG_POLL_WAIT_SECONDS would make
# these cases agree with whatever the module happens to say, and the point is to pin
# the value the design fixes -- the service maximum, 30. The design adapted this from
# CR-311220612's min(30, remaining timeout) because this change removes the
# client-side timeout, so there is no remaining-timeout term to clamp against.
_EXPECTED_WAIT_SECONDS = 30


def _declare_long_poll_support(executor):
    """
    Fake a DescribeStatement input shape that declares WaitTimeSeconds.

    This is the only way to reach long-poll mode in a unit test: the capability
    check reads `"WaitTimeSeconds" in input_shape.members` off the client's botocore
    service model, and the resolved model does not list it.
    """
    operation_model = executor.client.meta.service_model.operation_model
    operation_model.return_value.input_shape.members = {
        "Id": object(),
        "WaitTimeSeconds": object(),
    }


def _describe_calls(client):
    """Every describe_statement call as an (args, kwargs) pair."""
    return [(call.args, call.kwargs) for call in client.describe_statement.call_args_list]


class TestDescribeRequestShapeFollowsTheMode:
    """
    Feature: remove-redshift-data-api-query-timeout

    The describe_statement request carries WaitTimeSeconds in long-poll mode and
    nothing but Id in classic mode. Each call's keyword arguments are compared by
    exact dict equality rather than by membership, so an unexpected extra parameter
    fails these cases instead of slipping past them.

    Property 8 is specified as property-based, but the package declares only
    pytest and has no property-testing dependency, so it is realized as
    parameterized pytest cases over a table of poll counts -- matching how the rest
    of this suite is written.
    """

    @pytest.mark.parametrize("poll_count", [0, 1, 3, 7, 20])
    def test_long_poll_mode_sends_the_wait_on_every_poll(self, statement_executor, poll_count):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 8: The request shape
        follows the mode

        Every poll of a long-poll statement -- the non-terminal ones and the FINISHED
        one alike -- carries exactly {"Id": ..., "WaitTimeSeconds": 30}. The request
        count equals the number of responses consumed, so the mode cannot buy its
        completion with extra calls.

        **Validates: Requirements 8.1, 8.2, 8.4, 11.1**
        """
        responses = _non_terminal_then_finished(poll_count)
        _declare_long_poll_support(statement_executor)
        statement_executor.client.execute_statement.return_value = {"Id": "long-poll-shape-stmt"}
        statement_executor.client.describe_statement.side_effect = responses

        with patch("time.sleep"), patch("time.time", new=_SteppingClock(60.0)):
            result = statement_executor.execute_statement("SELECT pg_sleep(1000)")

        assert result["status"] == "FINISHED"

        calls = _describe_calls(statement_executor.client)
        assert len(calls) == len(responses)
        expected = {"Id": "long-poll-shape-stmt", "WaitTimeSeconds": _EXPECTED_WAIT_SECONDS}
        for index, (args, kwargs) in enumerate(calls):
            assert args == (), f"poll {index} passed positional arguments"
            assert kwargs == expected, f"poll {index}"

    @pytest.mark.parametrize("poll_count", [0, 1, 3, 7, 20])
    def test_classic_mode_sends_only_the_id(self, statement_executor, poll_count):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 8: The request shape
        follows the mode

        The client is left as the plain Mock() the fixtures build, whose `members`
        raises TypeError under `in`, so the capability check fails open and the loop
        runs classic. Every poll must then carry exactly {"Id": ...}: a driver that
        sent the wait regardless of the model would be rejected by the service on
        every call against the resolved botocore.

        **Validates: Requirements 8.4, 11.2**
        """
        responses = _non_terminal_then_finished(poll_count)
        statement_executor.client.execute_statement.return_value = {"Id": "classic-shape-stmt"}
        statement_executor.client.describe_statement.side_effect = responses

        with patch("time.sleep"), patch("time.time", new=_SteppingClock(60.0)):
            result = statement_executor.execute_statement("SELECT pg_sleep(1000)")

        assert result["status"] == "FINISHED"

        calls = _describe_calls(statement_executor.client)
        assert len(calls) == len(responses)
        for index, (args, kwargs) in enumerate(calls):
            assert args == (), f"poll {index} passed positional arguments"
            assert kwargs == {"Id": "classic-shape-stmt"}, f"poll {index}"
            assert "WaitTimeSeconds" not in kwargs, f"poll {index}"


class TestLongPollModePerformsNoClientSideWait:
    """
    Feature: remove-redshift-data-api-query-timeout

    In long-poll mode the service holds the describe call open, so the driver does no
    waiting of its own. The contrast case runs the same sequences in classic mode and
    asserts the sleeps do appear there, which keeps a zero count from being read as
    evidence when it is really an artifact of a patched clock or a short sequence.

    Property 9 is specified as property-based; as above, it is realized as
    parameterized pytest cases over a table of poll counts.
    """

    @pytest.mark.parametrize("poll_count", [1, 3, 20, 45])
    def test_long_poll_mode_requests_no_sleep(self, statement_executor, poll_count):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 9: Long-poll mode
        performs no client-side waiting

        However many non-terminal polls a long-poll statement takes, time.sleep is
        never called. The other half of Property 9 -- that the backoff interval is not
        advanced -- has no behavioral witness while the mode holds, since the interval
        is a loop local that only a sleep can expose; it becomes observable after a
        fallback, where test_error_handling.py asserts the schedule restarts at 0.1.

        **Validates: Requirements 8.2, 11.3**
        """
        _declare_long_poll_support(statement_executor)
        statement_executor.client.execute_statement.return_value = {"Id": "no-wait-stmt"}
        statement_executor.client.describe_statement.side_effect = _non_terminal_then_finished(
            poll_count
        )

        with patch("time.sleep") as mock_sleep, patch("time.time", new=_SteppingClock(60.0)):
            result = statement_executor.execute_statement("SELECT pg_sleep(1000)")

        assert result["status"] == "FINISHED"
        assert statement_executor.client.describe_statement.call_count == poll_count + 1
        assert mock_sleep.call_count == 0

    @pytest.mark.parametrize("poll_count", [1, 3, 20, 45])
    def test_classic_mode_does_sleep_over_the_same_sequence(self, statement_executor, poll_count):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 9: Long-poll mode
        performs no client-side waiting

        The control for the case above: the identical sequence on a classic-mode client
        sleeps once per non-terminal poll. Without this, a zero sleep count in
        long-poll mode would be equally consistent with the sequence never reaching
        the non-terminal branch at all.

        **Validates: Requirements 8.2, 11.3**
        """
        statement_executor.client.execute_statement.return_value = {"Id": "classic-wait-stmt"}
        statement_executor.client.describe_statement.side_effect = _non_terminal_then_finished(
            poll_count
        )

        with patch("time.sleep") as mock_sleep, patch("time.time", new=_SteppingClock(60.0)):
            result = statement_executor.execute_statement("SELECT pg_sleep(1000)")

        assert result["status"] == "FINISHED"
        assert mock_sleep.call_count == poll_count


# ---------------------------------------------------------------------------
# Feature: remove-redshift-data-api-query-timeout
#
# Support for the capability-check tests below.
#
# The check reads
# client.meta.service_model.operation_model("DescribeStatement").input_shape.members
# and memoizes the answer on the executor. These cases observe it two ways: by
# counting the calls to operation_model, and by reading the mode back off the
# requests the loop actually issued.
# ---------------------------------------------------------------------------


def _spy_on_the_capability_check(executor):
    """
    Attach the inspection and the polls to one parent so their relative order is recorded.

    Call counts alone cannot say which came first, so both mocks are reparented onto a
    single recorder and read back off its mock_calls, where the two appear interleaved in
    the order they were called. attach_mock only reparents them: the return_value and
    side_effect each already carries is left alone, and describe_statement.call_args_list
    keeps working.
    """
    recorder = Mock()
    recorder.attach_mock(executor.client.meta.service_model.operation_model, "inspect")
    recorder.attach_mock(executor.client.describe_statement, "describe")
    return recorder


def _recorded_order(recorder):
    """The names of the calls the recorder saw, in the order they were made."""
    return [call[0] for call in recorder.mock_calls]


def _declare_members(executor, members):
    """Fake the member names the client's DescribeStatementRequest shape declares."""
    operation_model = executor.client.meta.service_model.operation_model
    operation_model.return_value.input_shape.members = members


def _poll_run(executor, poll_count=3, parameters=None, statement_id="capability-stmt"):
    """
    Run one statement to FINISHED and return (result, per-poll kwargs, recorded sleeps).

    The kwargs and the sleeps are how these cases read the mode off behavior rather than
    off the memo: long-poll mode carries WaitTimeSeconds on every poll and never sleeps,
    classic mode carries only Id and sleeps once per non-terminal poll.
    """
    executor.client.execute_statement.return_value = {"Id": statement_id}
    executor.client.describe_statement.side_effect = _non_terminal_then_finished(poll_count)

    with patch("time.sleep") as mock_sleep, patch("time.time", new=_SteppingClock(60.0)):
        result = executor.execute_statement("SELECT pg_sleep(1000)", parameters)

    kwargs = [call_kwargs for _, call_kwargs in _describe_calls(executor.client)]
    sleeps = [call[0][0] for call in mock_sleep.call_args_list]
    return result, kwargs, sleeps


class TestCapabilityCheckHappensAtMostOnce:
    """
    Feature: remove-redshift-data-api-query-timeout

    The service model is inspected once per executor and every poll of every statement
    reuses that outcome. The memo is instance-level and deliberately stronger than
    Requirements 7.1 and 7.2 ask for -- those demand once per statement, the memo gives
    once per executor -- so both outcomes are covered here. A False answer must not be
    re-inspected either, which holds only because the guard tests `is None` rather than
    falsiness; under a falsiness test the classic cases below would inspect once per
    poll.

    Property 6 is specified as property-based, but the package declares only
    pytest and has no property-testing dependency, so it is realized as
    parameterized pytest cases over a table of poll counts -- matching how the rest of
    this suite is written.
    """

    @pytest.mark.parametrize("declares_support", [True, False], ids=["long_poll", "classic"])
    @pytest.mark.parametrize(
        "first_polls, second_polls",
        [(10, 3), (1, 1), (20, 15)],
        ids=["ten_then_three", "one_then_one", "twenty_then_fifteen"],
    )
    def test_two_statements_on_one_executor_inspect_once(
        self, statement_executor, declares_support, first_polls, second_polls
    ):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 6: The capability check
        is performed at most once and reused for every poll

        The task's named scenario: a statement of ~10 polls, then a second statement on
        the same executor. The inspection count is 1 across both, and it lands before the
        first describe_statement call. The poll counts vary while that count does not,
        which is the independence half of the property -- a per-poll check would scale
        with them.

        **Validates: Requirements 7.1, 7.2**
        """
        if declares_support:
            _declare_long_poll_support(statement_executor)
        recorder = _spy_on_the_capability_check(statement_executor)

        statement_executor.client.execute_statement.return_value = {"Id": "check-once-stmt"}
        statement_executor.client.describe_statement.side_effect = _non_terminal_then_finished(
            first_polls
        ) + _non_terminal_then_finished(second_polls)

        with patch("time.sleep"), patch("time.time", new=_SteppingClock(60.0)):
            first = statement_executor.execute_statement("SELECT 1")
            second = statement_executor.execute_statement("SELECT 2")

        assert first["status"] == "FINISHED"
        assert second["status"] == "FINISHED"

        order = _recorded_order(recorder)
        assert order.count("inspect") == 1
        assert order.index("inspect") < order.index("describe")
        assert order.count("describe") == first_polls + second_polls + 2
        assert statement_executor._long_poll_supported_memo is declares_support

    @pytest.mark.parametrize("declares_support", [True, False], ids=["long_poll", "classic"])
    def test_repeated_capability_reads_inspect_once(self, statement_executor, declares_support):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 6: The capability check
        is performed at most once and reused for every poll

        The memo read directly, with no statement around it: 25 reads, one inspection, the
        same answer every time. This is the case that pins the False outcome as cached
        too -- the loop cannot distinguish "memoized False" from "re-inspected to False",
        so only a direct call count can.

        **Validates: Requirements 7.1, 7.2**
        """
        if declares_support:
            _declare_long_poll_support(statement_executor)
        operation_model = statement_executor.client.meta.service_model.operation_model

        outcomes = [statement_executor._long_poll_supported() for _ in range(25)]

        assert outcomes == [declares_support] * 25
        assert operation_model.call_count == 1


# ---------------------------------------------------------------------------
# Feature: remove-redshift-data-api-query-timeout
#
# (label, declared members, whether the loop should run in long-poll mode).
#
# The member sets mix WaitTimeSeconds among other names, and carry three traps
# for an inexact check: two near-miss keys, and a key that contains the member
# name as a substring without being it. `in` on a mapping is key equality, so
# all three must read as "not declared"; a check written against str(members)
# would get the substring row wrong.
# ---------------------------------------------------------------------------

_MEMBER_SETS = [
    ("id_only", {"Id": object()}, False),
    ("id_and_the_member", {"Id": object(), "WaitTimeSeconds": object()}, True),
    (
        "the_member_among_others",
        {
            "ClusterIdentifier": object(),
            "Database": object(),
            "Id": object(),
            "WaitTimeSeconds": object(),
            "WorkgroupName": object(),
        },
        True,
    ),
    (
        "others_without_the_member",
        {
            "ClusterIdentifier": object(),
            "Database": object(),
            "Id": object(),
            "NextToken": object(),
        },
        False,
    ),
    (
        "near_miss_names_only",
        {"Id": object(), "WaitTime": object(), "WaitTimeSecond": object(), "Seconds": object()},
        False,
    ),
    ("member_name_as_a_substring", {"Id": object(), "NotWaitTimeSecondsReally": object()}, False),
    ("empty", {}, False),
    ("tuple_with_the_member", ("Id", "WaitTimeSeconds"), True),
    ("tuple_without_the_member", ("Id", "NextToken"), False),
    ("frozenset_with_the_member", frozenset({"Id", "WaitTimeSeconds"}), True),
]

_DECISIVE_MEMBER_SETS = [
    ("id_only", {"Id": object()}, False),
    ("id_and_the_member", {"Id": object(), "WaitTimeSeconds": object()}, True),
]

# Everything a caller of execute_statement is able to pass. There is no mode or
# wait-value knob to try: the signature is (sql, parameters) and nothing else.
_CALLER_PARAMETERS = [
    ("no_parameters", None),
    ("positional_parameters", ["sample", 7]),
    ("named_parameters", {"name": "sample", "count": 7}),
]


class TestServiceModelAloneSelectsTheMode:
    """
    Feature: remove-redshift-data-api-query-timeout

    The declared member set decides the mode, and nothing else does. Each case fakes a
    member set, runs a statement, and reads the mode back off two independent witnesses:
    whether every request carried WaitTimeSeconds, and whether the loop slept at all.

    Property 7 is specified as property-based; as above, it is realized as parameterized
    pytest cases over a table of member sets.
    """

    @staticmethod
    def _assert_mode(kwargs, sleeps, poll_count, statement_id, expects_long_poll):
        """Assert the requests and the sleeps both report the expected mode."""
        assert len(kwargs) == poll_count + 1

        if expects_long_poll:
            expected = {"Id": statement_id, "WaitTimeSeconds": _EXPECTED_WAIT_SECONDS}
            assert kwargs == [expected] * (poll_count + 1)
            assert sleeps == []
        else:
            assert kwargs == [{"Id": statement_id}] * (poll_count + 1)
            assert all("WaitTimeSeconds" not in call_kwargs for call_kwargs in kwargs)
            assert len(sleeps) == poll_count

    @pytest.mark.parametrize(
        "members, expects_long_poll",
        [pytest.param(members, expected, id=label) for label, members, expected in _MEMBER_SETS],
    )
    def test_mode_follows_the_declared_member_set(
        self, statement_executor, members, expects_long_poll
    ):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 7: The service model
        alone selects the mode

        Long-poll mode runs if and only if the declared set contains WaitTimeSeconds. The
        table covers the member mixed among other names, three near-miss keys, an empty
        set, and non-mapping containers -- `members` is only ever read through `in`, so a
        tuple or a frozenset must work exactly as a mapping does.

        **Validates: Requirements 7.3, 7.4, 5.6**
        """
        _declare_members(statement_executor, members)

        result, kwargs, sleeps = _poll_run(
            statement_executor, poll_count=4, statement_id="mode-stmt"
        )

        assert result["status"] == "FINISHED"
        assert statement_executor._long_poll_supported_memo is expects_long_poll
        self._assert_mode(kwargs, sleeps, 4, "mode-stmt", expects_long_poll)

    @pytest.mark.parametrize(
        "parameters",
        [pytest.param(value, id=label) for label, value in _CALLER_PARAMETERS],
    )
    @pytest.mark.parametrize(
        "members, expects_long_poll",
        [
            pytest.param(members, expected, id=label)
            for label, members, expected in _DECISIVE_MEMBER_SETS
        ],
    )
    @pytest.mark.parametrize("poll_count", [0, 3, 9])
    def test_nothing_the_caller_passes_changes_the_mode(
        self, statement_executor, members, expects_long_poll, parameters, poll_count
    ):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 7: The service model
        alone selects the mode

        The same member set across every argument shape a caller can supply -- no
        parameters, positional parameters, named parameters -- and across poll counts,
        yields the same mode every time. There is nothing stronger to test: the signature
        offers no mode or wait-value argument, so this asserts that what the caller can
        reach does not reach the mode.

        **Validates: Requirements 7.3, 7.4, 5.6**
        """
        _declare_members(statement_executor, members)

        result, kwargs, sleeps = _poll_run(
            statement_executor,
            poll_count=poll_count,
            parameters=parameters,
            statement_id="caller-stmt",
        )

        assert result["status"] == "FINISHED"
        assert statement_executor._long_poll_supported_memo is expects_long_poll
        self._assert_mode(kwargs, sleeps, poll_count, "caller-stmt", expects_long_poll)


# ---------------------------------------------------------------------------
# Feature: remove-redshift-data-api-query-timeout
#
# The failure modes of the inspection path, one builder each. They share no
# exception type, which is why the driver guards the whole inspection with a
# single broad `except Exception` rather than naming them.
# ---------------------------------------------------------------------------


def _remove_meta(executor):
    """A client with no `meta` at all: the attribute access raises AttributeError."""
    del executor.client.meta


def _remove_service_model(executor):
    """A client whose `meta` carries no `service_model`: also an AttributeError."""
    del executor.client.meta.service_model


def _raise_from_operation_model(executor):
    """A service model that cannot resolve the operation, as botocore signals it."""
    # Imported here rather than at module scope: OperationNotFoundError lives in
    # botocore.model, not botocore.exceptions, and this is the only case that wants it.
    from botocore.model import OperationNotFoundError

    executor.client.meta.service_model.operation_model.side_effect = OperationNotFoundError(
        "Unknown operation: DescribeStatement"
    )


def _null_input_shape(executor):
    """An operation that resolves but declares no input shape, caught by an explicit check."""
    executor.client.meta.service_model.operation_model.return_value.input_shape = None


def _leave_members_as_a_bare_mock(executor):
    """
    The shape the existing fixtures already build: `members` is a bare Mock, so
    `"WaitTimeSeconds" in members` raises TypeError. Deliberately a no-op -- this row is
    the one the whole pre-existing suite depends on failing open, and faking anything
    here would stop it being that row.
    """


_BROKEN_CLIENTS = [
    ("no_meta", _remove_meta),
    ("meta_without_service_model", _remove_service_model),
    ("operation_model_raises", _raise_from_operation_model),
    ("input_shape_is_none", _null_input_shape),
    ("members_is_a_bare_mock", _leave_members_as_a_bare_mock),
]


class TestInspectionFailureFailsOpen:
    """
    Feature: remove-redshift-data-api-query-timeout

    An uninspectable client yields "not supported", not an error. The inspection is never
    allowed to be the reason a statement fails, so each broken client is run through a
    whole statement and asserted to reach FINISHED through classic polls.

    The last row is the live one. Every Mock()-client test in this suite -- and in
    test_error_handling.py -- reaches the polling loop through it, so the fail-open guard
    holds up the existing suite, not just these cases.

    Property 10 is specified as property-based; as above, it is realized as parameterized
    pytest cases over a table of broken clients.
    """

    @pytest.mark.parametrize(
        "break_client",
        [pytest.param(builder, id=label) for label, builder in _BROKEN_CLIENTS],
    )
    @pytest.mark.parametrize("poll_count", [0, 1, 5, 20])
    def test_broken_inspection_polls_classic_and_still_finishes(
        self, statement_executor, break_client, poll_count
    ):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 10: An inspection
        failure fails open

        For each broken client the statement completes normally: every request carries
        exactly {"Id": ...}, the loop sleeps once per non-terminal poll, and the result is
        the full FINISHED payload. Nothing raises on account of the inspection -- a
        narrower except in the driver would let one of these rows surface as a query
        failure instead.

        **Validates: Requirements 7.5, 11.7**
        """
        break_client(statement_executor)

        result, kwargs, sleeps = _poll_run(
            statement_executor, poll_count=poll_count, statement_id="fail-open-stmt"
        )

        assert result["status"] == "FINISHED"
        assert set(result) == _FINISHED_RESULT_KEYS
        assert kwargs == [{"Id": "fail-open-stmt"}] * (poll_count + 1)
        assert all("WaitTimeSeconds" not in call_kwargs for call_kwargs in kwargs)
        assert len(sleeps) == poll_count

    @pytest.mark.parametrize(
        "break_client",
        [pytest.param(builder, id=label) for label, builder in _BROKEN_CLIENTS],
    )
    def test_broken_inspection_reports_unsupported_without_raising(
        self, statement_executor, break_client
    ):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 10: An inspection
        failure fails open

        The check read directly, both through the memo and past it. Asserting the
        undecorated detection too matters because the memo would hide a raise behind its
        first call either way, and `is False` rather than a falsiness check keeps a
        returned None from passing.

        **Validates: Requirements 7.5, 11.7**
        """
        break_client(statement_executor)

        assert statement_executor._detect_long_poll_support() is False
        assert statement_executor._long_poll_supported() is False
        assert statement_executor._long_poll_supported_memo is False


# ---------------------------------------------------------------------------
# Feature: remove-redshift-data-api-query-timeout
#
# The signatures the change fixes, and the names it must not grow back.
#
# Every behavioral test above reads the loop through mocks, which cannot see a
# parameter nobody passes. These cases read the signatures directly instead, so
# re-adding the cap as a keyword argument -- or adding a mode or wait-value knob
# -- fails here even though no behavioral test would notice.
# ---------------------------------------------------------------------------

_EXECUTE_STATEMENT_PARAMETERS = ["self", "sql", "parameters"]
_POLL_COMPLETION_PARAMETERS = ["self", "statement_id", "execution_context"]

# The removed cap, plus the knobs Requirement 5.6 forbids: nothing may select the
# polling mode or set the wait value. The wait is the module constant
# LONG_POLL_WAIT_SECONDS and the mode comes from the service model alone.
_FORBIDDEN_PARAMETER_NAMES = [
    "timeout_seconds",
    "timeout",
    "query_timeout",
    "wait_time_seconds",
    "long_poll_wait_seconds",
    "use_long_poll",
    "long_poll",
    "poll_mode",
    "poll_interval",
]

# The methods that between them decide the mode and perform the waiting. An
# environment variable read in any of them would be the knob Requirement 5.6
# forbids by a route no signature check can see.
_MODE_DECIDING_METHODS = [
    ("execute_statement", StatementExecutor.execute_statement),
    ("_poll_statement_completion", StatementExecutor._poll_statement_completion),
    ("_long_poll_supported", StatementExecutor._long_poll_supported),
    ("_detect_long_poll_support", StatementExecutor._detect_long_poll_support),
]

_ENVIRONMENT_READS = ["os.environ", "getenv", "environb"]


class TestNoTimeoutOrModeKnobInTheSignatures:
    """
    Feature: remove-redshift-data-api-query-timeout

    The cheapest durable guard this change has. `timeout_seconds` is gone from both
    methods, and neither grew a replacement: no mode selector, no wait value, nothing a
    caller can pass to influence how the loop waits. Asserted as exact parameter lists
    rather than as absences, so an addition of any kind is caught, and then again as a
    named-absence table whose failure message says which forbidden name came back.
    """

    def test_execute_statement_takes_only_sql_and_parameters(self):
        """
        Feature: remove-redshift-data-api-query-timeout

        The public-facing half. `Cursor.execute` calls this positionally as
        `execute_statement(sql, parameters)`, so the order and the optionality of
        `parameters` are part of the contract, not just the names.

        **Validates: Requirements 1.4, 6.4**
        """
        signature = inspect.signature(StatementExecutor.execute_statement)

        assert list(signature.parameters) == _EXECUTE_STATEMENT_PARAMETERS
        assert signature.parameters["sql"].default is inspect.Parameter.empty
        assert signature.parameters["parameters"].default is None

    def test_poll_statement_completion_takes_only_statement_id_and_context(self):
        """
        Feature: remove-redshift-data-api-query-timeout

        The internal half, where the cap used to sit between the two surviving
        parameters. Both are required, which is what keeps the caller in
        `execute_statement` passing the context it builds.

        **Validates: Requirements 1.4, 5.6**
        """
        signature = inspect.signature(StatementExecutor._poll_statement_completion)

        assert list(signature.parameters) == _POLL_COMPLETION_PARAMETERS
        assert all(
            signature.parameters[name].default is inspect.Parameter.empty
            for name in ("statement_id", "execution_context")
        )

    @pytest.mark.parametrize("forbidden_name", _FORBIDDEN_PARAMETER_NAMES)
    @pytest.mark.parametrize(
        "method",
        [
            pytest.param(StatementExecutor.execute_statement, id="execute_statement"),
            pytest.param(
                StatementExecutor._poll_statement_completion, id="_poll_statement_completion"
            ),
        ],
    )
    def test_neither_method_declares_a_timeout_or_mode_parameter(self, method, forbidden_name):
        """
        Feature: remove-redshift-data-api-query-timeout

        The regression guard, phrased so the failure names the offender: if
        `timeout_seconds` -- or any of the mode and wait-value knobs Requirement 5.6
        rules out -- is re-added to either method, this says which one and where.

        **Validates: Requirements 1.4, 5.6, 6.4**
        """
        declared = list(inspect.signature(method).parameters)

        assert forbidden_name not in declared, (
            f"{method.__qualname__} declares a forbidden parameter "
            f"{forbidden_name!r}; its parameters are {declared}"
        )

    @pytest.mark.parametrize(
        "method",
        [pytest.param(method, id=name) for name, method in _MODE_DECIDING_METHODS],
    )
    def test_no_mode_deciding_method_reads_an_environment_variable(self, method):
        """
        Feature: remove-redshift-data-api-query-timeout

        The other half of Requirement 5.6: no environment variable selects the mode or
        sets the wait value either. A signature check cannot see that route, so this
        reads the source of the four methods that decide and perform the waiting.

        **Validates: Requirements 5.6**
        """
        source = inspect.getsource(method)

        for read in _ENVIRONMENT_READS:
            assert read not in source, (
                f"{method.__qualname__} appears to read the environment via {read!r}; "
                f"the mode comes from the service model and the wait from "
                f"LONG_POLL_WAIT_SECONDS"
            )


# ---------------------------------------------------------------------------
# Feature: remove-redshift-data-api-query-timeout
#
# Failures _cancel_statement has to swallow, one row each.
#
# The method's body is `try: ... except Exception: pass`, so the shapes below are
# interchangeable to it by design. The table is what makes that a tested claim
# rather than a reading of the source: botocore's two error types, a driver
# exception, and a plain one.
# ---------------------------------------------------------------------------

_CANCEL_FAILURES = [
    (
        "client_error",
        ClientError(
            {"Error": {"Code": "ValidationException", "Message": "Statement is not running"}},
            "CancelStatement",
        ),
    ),
    (
        "throttling_client_error",
        ClientError(
            {"Error": {"Code": "ThrottlingException", "Message": "Rate exceeded"}},
            "CancelStatement",
        ),
    ),
    ("param_validation_error", ParamValidationError(report='Unknown parameter in input: "Id"')),
    ("driver_operational_error", OperationalError("Connection is already closed")),
    ("generic_exception", RuntimeError("connection reset by peer")),
]

# The method takes an optional context it only ever defaults; every row must
# behave the same way.
_CANCEL_CONTEXTS = [
    ("context_omitted", None),
    ("empty_context", {}),
    ("populated_context", {"statement_id": "cancel-stmt", "sql": "SELECT pg_sleep(1000)"}),
]


class TestCancelStatementIsBestEffort:
    """
    Feature: remove-redshift-data-api-query-timeout

    `_cancel_statement` has no in-driver caller: task 4.1 removed the best-effort cancel
    from the deleted timeout stanza, and task 4.2 recorded in its docstring that it is
    retained deliberately as the driver's cancellation entry point -- the natural hook
    for cancelling on KeyboardInterrupt or superseding an async run. Requirement 4.3
    keeps it; these cases keep it honestly exercised, so "retained" does not quietly
    become "retained and broken".

    Its contract has two halves: the request it issues is exactly
    cancel_statement(Id=statement_id), and a failure to cancel never becomes the
    caller's problem.
    """

    @pytest.mark.parametrize(
        "execution_context",
        [pytest.param(context, id=label) for label, context in _CANCEL_CONTEXTS],
    )
    def test_cancel_requests_the_statement_by_id(self, statement_executor, execution_context):
        """
        Feature: remove-redshift-data-api-query-timeout

        The success path, asserted on the exact keyword argument: `Id` is the only member
        CancelStatement takes, and the context -- which the method accepts for logging
        and never forwards -- must not reach the request in any form.

        **Validates: Requirements 4.3**
        """
        returned = statement_executor._cancel_statement("cancel-stmt", execution_context)

        assert returned is None
        statement_executor.client.cancel_statement.assert_called_once_with(Id="cancel-stmt")
        args, kwargs = statement_executor.client.cancel_statement.call_args
        assert args == ()
        assert kwargs == {"Id": "cancel-stmt"}

    @pytest.mark.parametrize(
        "execution_context",
        [pytest.param(context, id=label) for label, context in _CANCEL_CONTEXTS],
    )
    @pytest.mark.parametrize(
        "failure",
        [pytest.param(exception, id=label) for label, exception in _CANCEL_FAILURES],
    )
    def test_a_failing_cancel_is_swallowed(self, statement_executor, failure, execution_context):
        """
        Feature: remove-redshift-data-api-query-timeout

        The best-effort half: for every failure shape the attempt is still made and
        nothing propagates, with or without a context. A cancel is always a cleanup
        action on a statement the caller has already given up on, so raising from here
        would replace the caller's own problem with this one.

        **Validates: Requirements 4.3**
        """
        statement_executor.client.cancel_statement.side_effect = failure

        returned = statement_executor._cancel_statement("doomed-stmt", execution_context)

        assert returned is None
        statement_executor.client.cancel_statement.assert_called_once_with(Id="doomed-stmt")
