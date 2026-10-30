"""
DB-API 2.0 Cursor class for Redshift Data API.

This module provides the Cursor class that handles SQL statement execution
and result fetching through the Redshift Data API.
"""

import time
import uuid
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List, Optional, Tuple, Union

from botocore.exceptions import ClientError, ParamValidationError

from .exceptions import (
    InterfaceError,
    OperationalError,
    ProgrammingError,
    StatementExecutionError,
    map_boto3_exception,
)
from .retry import RetryConfig, retry_on_transient_error

# Long polling on DescribeStatement. No client-side timeout, so always the max wait.
LONG_POLL_WAIT_SECONDS = 30
_LONG_POLL_MEMBER = "WaitTimeSeconds"

# Parameter-problem codes; matched only alongside _LONG_POLL_MEMBER in the message.
_PARAM_REJECTION_ERROR_CODES = frozenset(
    {"ValidationException", "InvalidParameterValue", "MissingParameter"}
)

# Classic-mode backoff schedule.
_INITIAL_POLL_INTERVAL = 0.1
_MAX_POLL_INTERVAL = 1.0  # was 5.0
_POLL_BACKOFF_MULTIPLIER = 1.5


class _LongPollRejected(OperationalError):
    """
    Signal that describe_statement was rejected for carrying WaitTimeSeconds.

    Subclasses OperationalError so retry_on_transient_error re-raises it unchanged
    instead of mapping it into a DB-API error.
    """


def _is_long_poll_rejection(exc: Exception) -> bool:
    """
    Whether exc indicates WaitTimeSeconds was unknown or unaccepted.

    A service error qualifies only when its code is a parameter-problem code and its
    message names the member, so an unrelated ValidationException is not absorbed.
    """

    if isinstance(exc, ParamValidationError):
        return _LONG_POLL_MEMBER in str(exc)
    if isinstance(exc, ClientError):
        error = exc.response.get("Error", {})
        error_code = error.get("Code", "")
        error_message = error.get("Message", "")
        return error_code in _PARAM_REJECTION_ERROR_CODES and _LONG_POLL_MEMBER in error_message
    return False


class StatementExecutor:
    """Handles statement execution and polling for the Redshift Data API."""

    def __init__(self, connection):
        """Initialize with connection."""
        self.connection = connection
        self.client = connection.client
        self.connection_params = connection.connection_params
        self._long_poll_supported_memo: Optional[bool] = None

    def execute_statement(
        self, sql: str, parameters: Optional[Union[List, Dict]] = None
    ) -> Dict[str, Any]:
        """
        Execute a SQL statement using the Redshift Data API.

        Args:
            sql: The SQL statement to execute
            parameters: Optional list of parameters for the SQL statement

        Returns:
            Dict containing statement execution results

        Raises:
            StatementTimeoutError: If the Redshift Data API reports a service-side
                statement timeout
            OperationalError: If statement execution fails
            ProgrammingError: If SQL is invalid
        """
        # Create execution context for error handling and logging
        execution_context = {
            "sql": sql[:200] + "..." if len(sql) > 200 else sql,  # Truncate long SQL
            "parameter_count": len(parameters) if parameters else 0,
            "database_name": self.connection_params.database_name,
            "cluster_identifier": self.connection_params.cluster_identifier,
            "workgroup_name": self.connection_params.workgroup_name,
            "region": self.connection_params.region,
            "transaction_id": self.connection.get_transaction_id(),
        }

        # Prepare execute_statement parameters
        execute_params = {"Sql": sql}

        # Invalidate session if it's been idle too long
        self.connection._invalidate_session_if_expired()

        # Add transaction ID if in transaction mode
        transaction_id = self.connection.get_transaction_id()
        if transaction_id:
            execute_params["TransactionId"] = transaction_id

        # Only ONE of: ClusterIdentifier, WorkgroupName, SessionId, Database
        reuse_session = (
            self.connection._persist_session and self.connection._session_id and not transaction_id
        )

        if reuse_session:
            # Reuse existing session
            execute_params["SessionId"] = self.connection._session_id
            execute_params["SessionKeepAliveSeconds"] = self.connection._session_keep_alive_seconds
        else:
            # Add cluster/workgroup and database
            if self.connection_params.cluster_identifier:
                execute_params["ClusterIdentifier"] = self.connection_params.cluster_identifier
            elif self.connection_params.workgroup_name:
                execute_params["WorkgroupName"] = self.connection_params.workgroup_name
            else:
                raise ProgrammingError(
                    "Either cluster_identifier or workgroup_name must be specified"
                )

            execute_params["Database"] = self.connection_params.database_name

            # Add auth params
            if self.connection_params.db_user and not self.connection_params.secret_arn:
                execute_params["DbUser"] = self.connection_params.db_user
            if self.connection_params.secret_arn:
                execute_params["SecretArn"] = self.connection_params.secret_arn

            # Add session keep-alive for first query if enabled
            if self.connection._persist_session and not transaction_id:
                execute_params["SessionKeepAliveSeconds"] = (
                    self.connection._session_keep_alive_seconds
                )

        # Add parameters if provided
        if parameters:
            execute_params["Parameters"] = self._format_parameters(parameters)

        # Add statement name for tracking
        statement_name = f"sqlalchemy_stmt_{uuid.uuid4().hex[:8]}"
        execute_params["StatementName"] = statement_name
        execution_context["statement_name"] = statement_name

        # Submit the statement with retry logic for transient failures
        retry_config = RetryConfig(max_attempts=3, base_delay=1.0, max_delay=10.0)

        try:

            def submit_statement():
                return self.client.execute_statement(**execute_params)

            response = retry_on_transient_error(
                submit_statement,
                config=retry_config,
                operation_name="submit_statement",
                execution_context=execution_context,
            )

            statement_id = response["Id"]
            execution_context["statement_id"] = statement_id

            # Capture session ID from response if session persistency is enabled
            if self.connection._persist_session and not transaction_id and "SessionId" in response:
                self.connection._session_id = response["SessionId"]

        except Exception as e:
            if reuse_session:
                self.connection._session_id = None
            # Map boto3 exceptions with execution context
            mapped_exception = map_boto3_exception(e, execution_context)
            raise mapped_exception

        # Poll for completion
        result = self._poll_statement_completion(statement_id, execution_context)

        # Update last query time after query completes (not during transactions)
        if self.connection._persist_session and not transaction_id:
            self.connection._update_last_query_time()

        return result

    def _format_parameters(self, parameters: Union[List, Dict]) -> List[Dict[str, str]]:
        """
        Format parameters for the Data API.

        Args:
            parameters: List of parameter values (positional) or Dict of parameter names/values (named)

        Returns:
            List of formatted parameter dictionaries for Data API
            Each dict has 'name' (str) and 'value' (str) keys
        """
        formatted_params = []

        if isinstance(parameters, dict):
            # Handle named parameters (:name style)
            for param_name, param_value in parameters.items():
                formatted_param = {
                    "name": param_name,
                    "value": self._format_parameter_value(param_value),
                }
                formatted_params.append(formatted_param)
        else:
            # Handle positional parameters (list)
            for i, param_value in enumerate(parameters):
                formatted_param = {
                    "name": f"param_{i}",
                    "value": self._format_parameter_value(param_value),
                }
                formatted_params.append(formatted_param)

        return formatted_params

    def _format_parameter_value(self, param_value: Any) -> str:
        """
        Format a single parameter value for the Data API.

        Args:
            param_value: The parameter value to format

        Returns:
            String representation of the parameter value for Data API
        """
        if param_value is None:
            return ""  # Empty string for NULL values
        elif isinstance(param_value, bool):
            return "true" if param_value else "false"  # Boolean as string
        else:
            # Convert all other types to string
            return str(param_value)

    def _long_poll_supported(self) -> bool:
        """
        Whether this client's service model accepts WaitTimeSeconds on DescribeStatement.

        Memoized: it records only the service-model inspection, never a runtime
        rejection, which is a fallback scoped to the one statement it occurred in.

        Returns:
            True to poll in long-poll mode, False to poll in classic mode
        """
        if self._long_poll_supported_memo is None:
            self._long_poll_supported_memo = self._detect_long_poll_support()
        return self._long_poll_supported_memo

    def _detect_long_poll_support(self) -> bool:
        """
        Inspect the client's botocore service model for the long-poll member.

        Fails open: any problem reading the model yields classic mode, so the
        inspection can never be why a statement fails. The broad except covers
        unrelated failure types (missing attributes, unresolvable operation,
        non-container members from a Mock client).

        Returns:
            True when DescribeStatementRequest declares the member, False otherwise
        """
        try:
            operation_model = self.client.meta.service_model.operation_model("DescribeStatement")
            input_shape = operation_model.input_shape
            if input_shape is None:
                return False
            return _LONG_POLL_MEMBER in input_shape.members
        except Exception:
            return False

    def _poll_statement_completion(
        self, statement_id: str, execution_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Poll for statement completion until the Data API reports a terminal status.

        No client-side time limit. With WaitTimeSeconds support each poll holds the
        call open server-side; otherwise polls use the classic backoff schedule.

        Args:
            statement_id: The statement ID to poll
            execution_context: Execution context for error handling and logging

        Returns:
            Dict containing statement results

        Raises:
            StatementExecutionError: If the statement reports FAILED
            OperationalError: If the statement was cancelled or reports an unknown status
        """
        poll_interval = _INITIAL_POLL_INTERVAL
        use_long_poll = self._long_poll_supported()

        # Create retry config for describe_statement calls
        retry_config = RetryConfig(max_attempts=3, base_delay=0.5, max_delay=5.0)

        while True:
            # Check statement status with retry logic
            try:

                def describe_statement():
                    params: Dict[str, Any] = {"Id": statement_id}
                    if use_long_poll:
                        params[_LONG_POLL_MEMBER] = LONG_POLL_WAIT_SECONDS
                    try:
                        return self.client.describe_statement(**params)
                    except Exception as exc:
                        # Detect here, where the original botocore type is still intact.
                        if use_long_poll and _is_long_poll_rejection(exc):
                            raise _LongPollRejected(
                                f"Redshift Data API rejected {_LONG_POLL_MEMBER}; "
                                f"falling back to client-side polling"
                            ) from exc
                        raise

                response = retry_on_transient_error(
                    describe_statement,
                    config=retry_config,
                    operation_name="describe_statement",
                    execution_context=execution_context,
                )

            except _LongPollRejected:
                # Must precede `except Exception`, else the signal is mapped to a DB error.
                # Finish this statement in classic mode.
                use_long_poll = False
                poll_interval = _INITIAL_POLL_INTERVAL
                continue

            except Exception as e:
                mapped_exception = map_boto3_exception(e, execution_context)
                raise mapped_exception

            status = response["Status"]

            if status == "FINISHED":
                # Statement completed successfully

                return {
                    "statement_id": statement_id,
                    "status": status,
                    "has_result_set": response.get("HasResultSet", False),
                    "result_metadata": response.get("ResultMetadata"),
                    "records_updated": response.get("RecordsUpdated", 0),
                    "result_rows": response.get("ResultRows"),
                    "result_size": response.get("ResultSize"),
                    "sub_statements": response.get("SubStatements", []),
                    "redshift_query_id": response.get("RedshiftQueryId"),
                }

            elif status == "FAILED":
                # Statement failed
                error_message = response.get("Error", "Statement execution failed")

                raise StatementExecutionError(
                    f"Statement execution failed: {error_message}",
                    statement_id=statement_id,
                    redshift_query_id=response.get("RedshiftQueryId"),
                    query_string=response.get("QueryString"),
                )

            elif status == "ABORTED":
                # Statement was cancelled
                raise OperationalError(f"Statement was cancelled: {statement_id}")

            elif status in ("SUBMITTED", "PICKED", "STARTED"):
                # Still running. In long-poll mode the service already held the call
                # open, so skip the client-side wait and backoff advance.
                if not use_long_poll:
                    time.sleep(poll_interval)

                    # Increase poll interval with exponential backoff
                    poll_interval = min(
                        poll_interval * _POLL_BACKOFF_MULTIPLIER, _MAX_POLL_INTERVAL
                    )

            else:
                # Unknown status

                raise OperationalError(f"Unknown statement status: {status}")

    def _cancel_statement(
        self, statement_id: str, execution_context: Optional[Dict[str, Any]] = None
    ):
        """
        Cancel a running statement.

        No in-driver caller today (the timeout-stanza cancel was removed); retained as
        the cancellation entry point for a caller that needs to stop a statement.

        Args:
            statement_id: The statement ID to cancel
            execution_context: Optional execution context for logging
        """
        execution_context = execution_context or {}

        try:
            self.client.cancel_statement(Id=statement_id)
        except Exception:
            # don't raise it during cleanup
            pass

    def get_statement_result(
        self,
        statement_id: str,
        next_token: Optional[str] = None,
        execution_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Get results from a completed statement.

        Args:
            statement_id: The statement ID
            next_token: Token for pagination
            execution_context: Optional execution context for logging

        Returns:
            Dict containing result data
        """
        execution_context = execution_context or {}
        execution_context["statement_id"] = statement_id
        if next_token:
            execution_context["next_token"] = (
                next_token[:50] + "..." if len(next_token) > 50 else next_token
            )

        params = {"Id": statement_id}
        if next_token:
            params["NextToken"] = next_token

        # Create retry config for result fetching
        retry_config = RetryConfig(max_attempts=3, base_delay=0.5, max_delay=5.0)

        try:

            def fetch_results():
                return self.client.get_statement_result(**params)

            result = retry_on_transient_error(
                fetch_results,
                config=retry_config,
                operation_name="get_statement_result",
                execution_context=execution_context,
            )

            return result

        except Exception as e:
            mapped_exception = map_boto3_exception(e, execution_context)
            raise mapped_exception


class ResultConverter:
    """Converts Data API results to DB-API format."""

    @staticmethod
    def convert_column_metadata(column_metadata: List[Dict[str, Any]]) -> List[Tuple]:
        """
        Convert Data API column metadata to DB-API description format.

        Args:
            column_metadata: List of column metadata from Data API

        Returns:
            List of tuples in DB-API description format:
            (name, type_code, display_size, internal_size, precision, scale, null_ok)
        """
        description = []
        for col in column_metadata:
            name = col.get("name", "")
            type_name = col.get("typeName", "varchar")
            precision = col.get("precision")
            scale = col.get("scale")
            nullable = col.get("nullable", True)

            # Map Redshift types to Python type codes (simplified)
            type_code = ResultConverter._map_type_name_to_code(type_name)

            # DB-API description format: (name, type_code, display_size, internal_size, precision, scale, null_ok)
            description.append(
                (
                    name,
                    type_code,
                    None,  # display_size - not provided by Data API
                    None,  # internal_size - not provided by Data API
                    precision,
                    scale,
                    nullable,
                )
            )

        return description

    @staticmethod
    def _map_type_name_to_code(type_name: str) -> str:
        """
        Map Redshift type names to simplified type codes.

        Args:
            type_name: Redshift type name

        Returns:
            Simplified type code
        """
        type_mapping = {
            "varchar": "STRING",
            "char": "STRING",
            "text": "STRING",
            "bpchar": "STRING",
            "int2": "NUMBER",
            "int4": "NUMBER",
            "int8": "NUMBER",
            "integer": "NUMBER",
            "bigint": "NUMBER",
            "smallint": "NUMBER",
            "float4": "NUMBER",
            "float8": "NUMBER",
            "real": "NUMBER",
            "double precision": "NUMBER",
            "numeric": "NUMBER",
            "decimal": "NUMBER",
            "bool": "BOOLEAN",
            "boolean": "BOOLEAN",
            "date": "DATETIME",
            "timestamp": "DATETIME",
            "timestamptz": "DATETIME",
            "time": "DATETIME",
            "timetz": "DATETIME",
            "super": "JSON",
            "geometry": "BINARY",
            "geography": "BINARY",
        }

        return type_mapping.get(type_name.lower(), "STRING")

    @staticmethod
    def convert_records(
        records: List[List[Dict[str, Any]]], column_metadata: List[Dict[str, Any]]
    ) -> List[List[Any]]:
        """
        Convert Data API records to Python values.

        Args:
            records: List of records from Data API
            column_metadata: Column metadata for type conversion

        Returns:
            List of rows with converted Python values
        """
        converted_rows = []

        for record in records:
            converted_row = []
            for i, field in enumerate(record):
                col_type = (
                    column_metadata[i].get("typeName", "varchar")
                    if i < len(column_metadata)
                    else "varchar"
                )
                converted_value = ResultConverter._convert_field_value(field, col_type)
                converted_row.append(converted_value)
            converted_rows.append(converted_row)

        return converted_rows

    @staticmethod
    def _convert_field_value(field: Dict[str, Any], column_type: str) -> Any:
        """
        Convert a single field value from Data API format to Python value.

        Args:
            field: Field value from Data API
            column_type: Column type name

        Returns:
            Converted Python value
        """
        # Handle NULL values
        if field.get("isNull", False):
            return None

        # Extract the actual value based on the field type
        if "stringValue" in field:
            value = field["stringValue"]
            # Data API returns NUMERIC/DECIMAL as stringValue; keep it numeric and exact.
            if column_type.lower() in ("decimal", "numeric"):
                try:
                    return Decimal(value)
                except InvalidOperation:
                    return value
            # For certain types, we might need additional conversion
            if column_type.lower() in ("date", "timestamp", "timestamptz", "time", "timetz"):
                # Return as string for now - could be enhanced to return datetime objects
                return value
            return value
        elif "longValue" in field:
            return field["longValue"]
        elif "doubleValue" in field:
            return field["doubleValue"]
        elif "booleanValue" in field:
            return field["booleanValue"]
        elif "blobValue" in field:
            return field["blobValue"]
        elif "arrayValue" in field:
            # Handle array values (for SUPER type)
            return field["arrayValue"]
        else:
            # Fallback - return the field as-is
            return field


class Cursor:
    """DB-API 2.0 Cursor class for Redshift Data API."""

    def __init__(self, connection):
        """Initialize cursor with connection."""
        self.connection = connection
        self.description = None
        self._executor = StatementExecutor(connection)
        self._result_data = []
        self._current_row = 0
        self._statement_id = None
        self._closed = False
        self._has_result_set = False
        self._next_token = None
        self._all_results_fetched = False
        self._rowcount = -1
        self._result_rows = None
        self._result_size = None
        self._redshift_query_id = None
        self.arraysize = 1  # DB-API 2.0 default arraysize

    def execute(self, sql: str, parameters: Optional[Union[List, Dict]] = None):
        """
        Execute SQL statement.

        Args:
            sql: The SQL statement to execute
            parameters: Optional parameters for the SQL statement

        Raises:
            InterfaceError: If cursor is closed
            ProgrammingError: If SQL is invalid
            OperationalError: If execution fails
        """
        if self._closed:
            raise InterfaceError("Cursor is closed")

        # Reset cursor state
        self.description = None
        self._result_data = []
        self._current_row = 0
        self._statement_id = None
        self._has_result_set = False
        self._next_token = None
        self._all_results_fetched = False
        self._rowcount = -1
        self._result_rows = None
        self._result_size = None
        self._redshift_query_id = None

        # Keep parameters as-is to preserve parameter names for Data API
        # Dict parameters will be handled as named parameters (:name style)
        # List parameters will be handled as positional parameters

        # Execute the statement
        result = self._executor.execute_statement(sql, parameters)
        self._statement_id = result["statement_id"]
        self._has_result_set = result.get("has_result_set", False)
        self._rowcount = result.get("records_updated", 0) if not self._has_result_set else -1
        self._result_rows = result.get("result_rows")
        self._result_size = result.get("result_size")
        self._redshift_query_id = result.get("redshift_query_id")

        # Set up column metadata if we have results
        if self._has_result_set:
            if result.get("result_metadata") and result["result_metadata"].get("ColumnMetadata"):
                column_metadata = result["result_metadata"]["ColumnMetadata"]
                self.description = ResultConverter.convert_column_metadata(column_metadata)
            else:
                # If we have a result set but no column metadata yet, we need to fetch
                # the first batch to get the metadata. Set a placeholder for now.
                self.description = [("unknown", "STRING", None, None, None, None, True)]
                # The async path only needs statement_id/metadata (already captured above)
                # and reads rows later by statement_id via a fresh client, so eagerly
                # downloading the first page here is pure duplicate work. Skip it when the
                # connection opts out; fetchone/fetchall still load lazily on demand, so a
                # later read of this cursor remains correct (it just resolves the real
                # column metadata on first fetch instead of now).
                if getattr(self.connection, "_skip_eager_result_load", False):
                    pass
                else:
                    # Load the first batch immediately to get proper metadata
                    try:
                        self._load_next_batch()
                    except Exception:
                        # If loading fails, keep the placeholder description
                        pass

    def fetchone(self):
        """
        Fetch single row.

        Returns:
            Single row as a list or None if no more rows

        Raises:
            InterfaceError: If cursor is closed
        """
        if self._closed:
            raise InterfaceError("Cursor is closed")

        if not self._has_result_set:
            return None

        # Ensure we have data loaded
        self._ensure_results_loaded()

        if self._current_row >= len(self._result_data):
            return None

        row = self._result_data[self._current_row]
        self._current_row += 1
        return row

    def fetchall(self):
        """
        Fetch all remaining rows.

        Returns:
            List of all remaining rows

        Raises:
            InterfaceError: If cursor is closed
        """
        if self._closed:
            raise InterfaceError("Cursor is closed")

        if not self._has_result_set:
            return []

        # Load all remaining results
        self._load_all_results()

        # Return all remaining rows
        remaining_rows = self._result_data[self._current_row :]
        self._current_row = len(self._result_data)
        return remaining_rows

    def fetchmany(self, size=None):
        """
        Fetch multiple rows.

        Args:
            size: Number of rows to fetch (default: cursor.arraysize or 1)

        Returns:
            List of up to size rows

        Raises:
            InterfaceError: If cursor is closed
        """
        if self._closed:
            raise InterfaceError("Cursor is closed")

        if not self._has_result_set:
            return []

        if size is None:
            size = getattr(self, "arraysize", 1)

        # Ensure we have enough data loaded
        self._ensure_results_loaded(min_rows=size)

        # Return up to size rows
        end_row = min(self._current_row + size, len(self._result_data))
        rows = self._result_data[self._current_row : end_row]
        self._current_row = end_row
        return rows

    def _ensure_results_loaded(self, min_rows: int = 1):
        """
        Ensure we have at least min_rows loaded from the result set.

        Args:
            min_rows: Minimum number of rows needed
        """
        if not self._statement_id or not self._has_result_set:
            return

        # If we already have enough rows or all results are fetched, return
        available_rows = len(self._result_data) - self._current_row
        if available_rows >= min_rows or self._all_results_fetched:
            return

        # Load more results
        self._load_next_batch()

    def _load_next_batch(self):
        """Load the next batch of results from the Data API."""
        if not self._statement_id or self._all_results_fetched:
            return

        # Create execution context for result fetching
        execution_context = {
            "statement_id": self._statement_id,
            "current_row_count": len(self._result_data),
            "has_next_token": bool(self._next_token),
        }

        try:
            # Get results from the Data API
            result = self._executor.get_statement_result(
                self._statement_id, self._next_token, execution_context
            )

            # Extract records and metadata
            records = result.get("Records", [])
            column_metadata = result.get("ColumnMetadata", [])

            # Convert records to Python values
            if records and column_metadata:
                # Update description if we don't have proper metadata yet
                if (
                    not self.description
                    or len(self.description) == 1
                    and self.description[0][0] == "unknown"
                ):
                    self.description = ResultConverter.convert_column_metadata(column_metadata)

                converted_rows = ResultConverter.convert_records(records, column_metadata)
                self._result_data.extend(converted_rows)

            # Update pagination state
            self._next_token = result.get("NextToken")
            if not self._next_token:
                self._all_results_fetched = True

        except Exception as e:
            # Map to appropriate DB-API exception with context
            mapped_exception = map_boto3_exception(e, execution_context)
            raise mapped_exception

    def _load_all_results(self):
        """Load all remaining results from the Data API."""
        while not self._all_results_fetched:
            self._load_next_batch()

    def close(self):
        """Close the cursor."""
        self._closed = True
        self.description = None
        self._result_data = []
        self._current_row = 0
        self._statement_id = None
        self._has_result_set = False
        self._next_token = None
        self._all_results_fetched = False
        self._rowcount = -1
        self._result_rows = None
        self._result_size = None
        self._redshift_query_id = None

    def get_execution_metadata(self) -> Optional[Dict[str, Any]]:
        """Return engine-specific execution metadata for query history tracking."""
        if not self._statement_id:
            return None

        metadata: Dict[str, Any] = {
            "statement_id": self._statement_id,
            "has_result_set": self._has_result_set,
        }

        if self._redshift_query_id and self._redshift_query_id > 0:
            metadata["redshift_query_id"] = self._redshift_query_id

        # Include session ID if available
        if hasattr(self, "connection") and hasattr(self.connection, "_session_id"):
            if self.connection._session_id:
                metadata["session_id"] = self.connection._session_id

        # Include records updated for DML statements
        if self._rowcount >= 0:
            metadata["records_updated"] = self._rowcount

        # Include result rows and size from describe_statement
        if self._result_rows is not None:
            metadata["result_rows"] = self._result_rows
        if self._result_size is not None:
            metadata["result_size_bytes"] = self._result_size

        return metadata

    @property
    def rowcount(self):
        """Return number of rows affected by last operation."""
        return self._rowcount

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
