"""
Unit tests for comprehensive error handling and logging functionality.

This module tests the enhanced error handling, retry mechanisms, and
structured logging features added to the Redshift Data API dialect.
"""

import time
from unittest.mock import Mock, patch

import pytest
from botocore.exceptions import ClientError, NoCredentialsError, ParamValidationError

from ...dbapi.connection import Connection
from ...dbapi.cursor import StatementExecutor
from ...dbapi.exceptions import (
    AuthenticationError,
    ClusterNotFoundError,
    DatabaseError,
    InvalidParameterError,
    OperationalError,
    StatementLimitExceededError,
    StatementTimeoutError,
    TransientError,
    _extract_cluster_id_from_message,
    _extract_statement_id_from_message,
    map_boto3_exception,
)
from ...dbapi.retry import (
    CircuitBreaker,
    RetryConfig,
    RetryContext,
    retry_on_transient_error,
    with_retry,
)


class TestEnhancedExceptions:
    """Test enhanced exception classes with execution context."""

    def test_statement_timeout_error_with_context(self):
        """Test StatementTimeoutError with execution context."""
        context = {
            "sql": "SELECT * FROM large_table",
            "database_name": "test_db",
            "cluster_identifier": "test-cluster",
        }

        error = StatementTimeoutError(
            "Statement timed out",
            statement_id="stmt-123",
            timeout_seconds=300,
            execution_context=context,
        )

        assert error.statement_id == "stmt-123"
        assert error.timeout_seconds == 300
        assert error.execution_context == context

        error_str = str(error)
        assert "Statement ID: stmt-123" in error_str
        assert "Timeout: 300s" in error_str
        assert "sql: SELECT * FROM large_table" in error_str

    def test_statement_limit_exceeded_error_with_context(self):
        """Test StatementLimitExceededError with execution context."""
        context = {"region": "us-east-1"}

        error = StatementLimitExceededError(
            "Too many active statements",
            limit_type="active_statements",
            current_count=10,
            max_count=10,
            execution_context=context,
        )

        assert error.limit_type == "active_statements"
        assert error.current_count == 10
        assert error.max_count == 10

        error_str = str(error)
        assert "Limit type: active_statements" in error_str
        assert "Usage: 10/10" in error_str
        assert "region: us-east-1" in error_str

    def test_cluster_not_found_error_with_context(self):
        """Test ClusterNotFoundError with execution context."""
        context = {"operation": "connect"}

        error = ClusterNotFoundError(
            "Cluster not found",
            cluster_identifier="test-cluster",
            workgroup_name="test-workgroup",
            execution_context=context,
        )

        assert error.cluster_identifier == "test-cluster"
        assert error.workgroup_name == "test-workgroup"

        error_str = str(error)
        assert "Cluster: test-cluster" in error_str
        assert "Workgroup: test-workgroup" in error_str
        assert "operation: connect" in error_str

    def test_authentication_error_with_context(self):
        """Test AuthenticationError with execution context."""
        context = {"credential_source": "environment"}

        error = AuthenticationError(
            "Invalid credentials",
            auth_method="iam_role",
            region="us-west-2",
            execution_context=context,
        )

        assert error.auth_method == "iam_role"
        assert error.region == "us-west-2"

        error_str = str(error)
        assert "Auth method: iam_role" in error_str
        assert "Region: us-west-2" in error_str
        assert "credential_source: environment" in error_str

    def test_transient_error_with_retry_info(self):
        """Test TransientError with retry information."""
        context = {"request_id": "req-123"}

        error = TransientError(
            "Service temporarily unavailable",
            retry_after=30,
            attempt_count=2,
            max_attempts=5,
            execution_context=context,
        )

        assert error.retry_after == 30
        assert error.attempt_count == 2
        assert error.max_attempts == 5

        error_str = str(error)
        assert "Retry after: 30s" in error_str
        assert "Attempt: 2/5" in error_str
        assert "request_id: req-123" in error_str


class TestExceptionMapping:
    """Test boto3 exception mapping with execution context."""

    def test_map_no_credentials_error(self):
        """Test mapping NoCredentialsError."""
        context = {"auth_method": "environment", "region": "us-east-1"}
        boto3_error = NoCredentialsError()

        mapped = map_boto3_exception(boto3_error, context)

        assert isinstance(mapped, AuthenticationError)
        assert mapped.auth_method == "environment"
        assert mapped.region == "us-east-1"
        assert mapped.execution_context == context

    def test_map_client_error_cluster_not_found(self):
        """Test mapping ClientError for cluster not found."""
        context = {"cluster_identifier": "test-cluster"}

        boto3_error = ClientError(
            error_response={
                "Error": {
                    "Code": "ClusterNotFoundFault",
                    "Message": "Cluster test-cluster not found",
                },
                "ResponseMetadata": {"RequestId": "req-123"},
            },
            operation_name="execute_statement",
        )

        mapped = map_boto3_exception(boto3_error, context)

        assert isinstance(mapped, ClusterNotFoundError)
        assert mapped.cluster_identifier == "test-cluster"
        assert "aws_request_id" in mapped.execution_context
        assert mapped.execution_context["aws_request_id"] == "req-123"

    def test_map_client_error_statement_timeout(self):
        """Test mapping ClientError for statement timeout."""
        context = {"statement_id": "stmt-456", "timeout_seconds": 300}

        boto3_error = ClientError(
            error_response={
                "Error": {
                    "Code": "StatementTimeoutException",
                    "Message": "Statement stmt-456 timed out",
                }
            },
            operation_name="describe_statement",
        )

        mapped = map_boto3_exception(boto3_error, context)

        assert isinstance(mapped, StatementTimeoutError)
        assert mapped.statement_id == "stmt-456"
        assert mapped.timeout_seconds == 300

    @pytest.mark.parametrize(
        "context",
        [
            {},
            {"statement_id": "stmt-456"},
            {
                "statement_id": "stmt-456",
                "database_name": "test_db",
                "cluster_identifier": "test-cluster",
            },
        ],
        ids=["empty_context", "statement_id_only", "statement_id_plus_unrelated_keys"],
    )
    def test_map_client_error_statement_timeout_without_timeout_in_context(self, context):
        """Feature: remove-redshift-data-api-query-timeout, Property 16: A context without a
        timeout omits the timeout detail.

        Every execution context the driver builds now omits ``timeout_seconds``, so the mapper's
        ``execution_context.get("timeout_seconds")`` yields ``None`` and the ``if
        self.timeout_seconds:`` guard in ``StatementTimeoutError.__str__`` drops the detail.

        Validates: Requirements 3.3
        """
        boto3_error = ClientError(
            error_response={
                "Error": {
                    "Code": "StatementTimeoutException",
                    "Message": "Statement stmt-456 timed out",
                }
            },
            operation_name="describe_statement",
        )

        mapped = map_boto3_exception(boto3_error, context)

        assert isinstance(mapped, StatementTimeoutError)
        # The mapper resolves the statement id from the error message first and only falls back
        # to the context, so "stmt-456" is recovered even from the empty context.
        assert mapped.statement_id == "stmt-456"
        assert mapped.timeout_seconds is None
        assert "Timeout:" not in str(mapped)

    def test_map_client_error_throttling(self):
        """Test mapping ClientError for throttling (transient error)."""
        context = {"operation": "execute_statement"}

        boto3_error = ClientError(
            error_response={
                "Error": {"Code": "ThrottlingException", "Message": "Request rate exceeded"},
                "ResponseMetadata": {"HTTPHeaders": {"retry-after": "5"}},
            },
            operation_name="execute_statement",
        )

        mapped = map_boto3_exception(boto3_error, context)

        assert isinstance(mapped, TransientError)
        assert mapped.retry_after == 5

    def test_extract_cluster_id_from_message(self):
        """Test extracting cluster ID from error messages."""
        # Test "Cluster: identifier" format
        message1 = "Cluster: my-test-cluster not found"
        assert _extract_cluster_id_from_message(message1) == "my-test-cluster"

        # Test "cluster identifier" format
        message2 = "cluster my-cluster-123 is not available"
        assert _extract_cluster_id_from_message(message2) == "my-cluster-123"

        # Test no match
        message3 = "Some other error message"
        assert _extract_cluster_id_from_message(message3) is None

    def test_extract_statement_id_from_message(self):
        """Test extracting statement ID from error messages."""
        # Test "Statement: identifier" format
        message1 = "Statement: abc-123-def timed out"
        assert _extract_statement_id_from_message(message1) == "abc-123-def"

        # Test "statement identifier" format
        message2 = "statement xyz-456-ghi failed to execute"
        assert _extract_statement_id_from_message(message2) == "xyz-456-ghi"

        # Test no match
        message3 = "Some other error message"
        assert _extract_statement_id_from_message(message3) is None


class TestRetryConfig:
    """Test retry configuration and delay calculation."""

    def test_default_config(self):
        """Test default retry configuration."""
        config = RetryConfig()

        assert config.max_attempts == 3
        assert config.base_delay == 1.0
        assert config.max_delay == 60.0
        assert config.backoff_multiplier == 2.0
        assert config.jitter is True

    def test_calculate_delay_exponential_backoff(self):
        """Test exponential backoff delay calculation."""
        config = RetryConfig(base_delay=1.0, backoff_multiplier=2.0, jitter=False)

        assert config.calculate_delay(0) == 1.0  # 1.0 * 2^0
        assert config.calculate_delay(1) == 2.0  # 1.0 * 2^1
        assert config.calculate_delay(2) == 4.0  # 1.0 * 2^2

    def test_calculate_delay_with_max_delay(self):
        """Test delay calculation with maximum delay cap."""
        config = RetryConfig(base_delay=10.0, max_delay=15.0, backoff_multiplier=2.0, jitter=False)

        assert config.calculate_delay(0) == 10.0
        assert config.calculate_delay(1) == 15.0  # Capped at max_delay
        assert config.calculate_delay(2) == 15.0  # Still capped

    def test_calculate_delay_with_retry_after(self):
        """Test delay calculation with server-suggested retry-after."""
        config = RetryConfig(base_delay=1.0, jitter=False)

        # Server suggests 5 seconds
        assert config.calculate_delay(0, retry_after=5.0) == 5.0
        assert config.calculate_delay(1, retry_after=5.0) == 5.0

    def test_calculate_delay_with_jitter(self):
        """Test delay calculation with jitter."""
        config = RetryConfig(base_delay=10.0, jitter=True)

        # With jitter, delay should be within 10% of base delay
        delay = config.calculate_delay(0)
        assert 9.0 <= delay <= 11.0

    def test_should_retry_transient_error(self):
        """Test retry decision for transient errors."""
        config = RetryConfig(max_attempts=3)

        transient_error = TransientError("Service unavailable")

        assert config.should_retry(transient_error, 0) is True
        assert config.should_retry(transient_error, 1) is True
        assert config.should_retry(transient_error, 2) is True
        assert config.should_retry(transient_error, 3) is False  # Max attempts reached

    def test_should_retry_boto3_client_error(self):
        """Test retry decision for boto3 ClientError."""
        config = RetryConfig(max_attempts=3)

        # Throttling exception should be retried
        throttling_error = ClientError(
            error_response={"Error": {"Code": "ThrottlingException"}}, operation_name="test"
        )
        assert config.should_retry(throttling_error, 0) is True

        # Validation exception should not be retried
        validation_error = ClientError(
            error_response={"Error": {"Code": "ValidationException"}}, operation_name="test"
        )
        assert config.should_retry(validation_error, 0) is False


class TestRetryContext:
    """Test retry context for tracking attempts."""

    def test_retry_context_initialization(self):
        """Test retry context initialization."""
        context = RetryContext("test_operation", {"key": "value"})

        assert context.operation_name == "test_operation"
        assert context.execution_context == {"key": "value"}
        assert context.attempt_count == 0
        assert context.last_exception is None
        assert context.total_delay == 0.0


class TestRetryDecorator:
    """Test retry decorator functionality."""

    def test_with_retry_success_no_retries(self):
        """Test successful execution without retries."""
        call_count = 0

        @with_retry(RetryConfig(max_attempts=3))
        def test_function():
            nonlocal call_count
            call_count += 1
            return "success"

        result = test_function()

        assert result == "success"
        assert call_count == 1

    def test_with_retry_success_after_retries(self):
        """Test successful execution after retries."""
        call_count = 0

        @with_retry(RetryConfig(max_attempts=3, base_delay=0.01))
        def test_function():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise TransientError("Temporary failure")
            return "success"

        result = test_function()

        assert result == "success"
        assert call_count == 3

    def test_with_retry_failure_after_max_attempts(self):
        """Test failure after exhausting all retry attempts."""
        call_count = 0

        @with_retry(RetryConfig(max_attempts=2, base_delay=0.01))
        def test_function():
            nonlocal call_count
            call_count += 1
            raise TransientError("Persistent failure")

        with pytest.raises(TransientError, match="Persistent failure"):
            test_function()

        assert call_count == 3  # Initial attempt + 2 retries

    def test_with_retry_non_retryable_exception(self):
        """Test immediate failure for non-retryable exceptions."""
        call_count = 0

        @with_retry(RetryConfig(max_attempts=3))
        def test_function():
            nonlocal call_count
            call_count += 1
            raise ValueError("Not retryable")

        with pytest.raises(ValueError, match="Not retryable"):
            test_function()

        assert call_count == 1  # No retries for non-retryable exception


class TestRetryFunction:
    """Test retry_on_transient_error function."""

    def test_retry_function_success(self):
        """Test successful function execution."""

        def test_func(x, y):
            return x + y

        result = retry_on_transient_error(
            test_func, args=(2, 3), config=RetryConfig(max_attempts=3)
        )

        assert result == 5

    def test_retry_function_with_kwargs(self):
        """Test function execution with keyword arguments."""

        def test_func(x, y=10):
            return x * y

        result = retry_on_transient_error(
            test_func, args=(5,), kwargs={"y": 3}, config=RetryConfig(max_attempts=3)
        )

        assert result == 15

    def test_retry_function_with_boto3_exception_mapping(self):
        """Test function execution with boto3 exception mapping."""
        call_count = 0

        def test_func():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                # Simulate a throttling exception
                raise ClientError(
                    error_response={"Error": {"Code": "ThrottlingException"}}, operation_name="test"
                )
            return "success"

        result = retry_on_transient_error(
            test_func,
            config=RetryConfig(max_attempts=3, base_delay=0.01),
            execution_context={"operation": "test"},
        )

        assert result == "success"
        assert call_count == 3


class TestCircuitBreaker:
    """Test circuit breaker pattern."""

    def test_circuit_breaker_closed_state(self):
        """Test circuit breaker in closed state (normal operation)."""
        breaker = CircuitBreaker(failure_threshold=3)

        def test_func():
            return "success"

        result = breaker.call(test_func)
        assert result == "success"
        assert breaker.state == "CLOSED"
        assert breaker.failure_count == 0

    def test_circuit_breaker_opens_after_failures(self):
        """Test circuit breaker opens after failure threshold."""
        breaker = CircuitBreaker(failure_threshold=2, expected_exception=ValueError)

        def failing_func():
            raise ValueError("Test failure")

        # First failure
        with pytest.raises(ValueError):
            breaker.call(failing_func)
        assert breaker.state == "CLOSED"
        assert breaker.failure_count == 1

        # Second failure - should open circuit
        with pytest.raises(ValueError):
            breaker.call(failing_func)
        assert breaker.state == "OPEN"
        assert breaker.failure_count == 2

    def test_circuit_breaker_open_state_blocks_calls(self):
        """Test circuit breaker blocks calls when open."""
        breaker = CircuitBreaker(failure_threshold=1, recovery_timeout=1.0)

        def failing_func():
            raise Exception("Test failure")

        # Trigger circuit opening
        with pytest.raises(Exception):
            breaker.call(failing_func)

        # Circuit should be open and block subsequent calls
        from ...dbapi.exceptions import OperationalError

        with pytest.raises(OperationalError, match="Circuit breaker is OPEN"):
            breaker.call(failing_func)

    def test_circuit_breaker_half_open_recovery(self):
        """Test circuit breaker recovery through half-open state."""
        breaker = CircuitBreaker(failure_threshold=1, recovery_timeout=0.01)

        def initially_failing_func():
            return "recovered"

        # Trigger circuit opening
        def failing_func():
            raise Exception("Test failure")

        with pytest.raises(Exception):
            breaker.call(failing_func)
        assert breaker.state == "OPEN"

        # Wait for recovery timeout
        time.sleep(0.02)

        # Next call should enter half-open state and succeed
        result = breaker.call(initially_failing_func)
        assert result == "recovered"
        assert breaker.state == "CLOSED"
        assert breaker.failure_count == 0


class TestStatementExecutorErrorHandling:
    """Test error handling in StatementExecutor."""

    @pytest.fixture
    def mock_connection(self):
        """Create a mock connection for testing."""
        connection = Mock()
        connection.connection_params = Mock()
        connection.connection_params.database_name = "test_db"
        connection.connection_params.cluster_identifier = "test-cluster"
        connection.connection_params.workgroup_name = None
        connection.connection_params.region = "us-east-1"
        connection.connection_params.secret_arn = None
        connection.connection_params.db_user = "test_user"
        connection.get_transaction_id.return_value = None

        # Mock the boto3 client
        mock_client = Mock()
        connection.client = mock_client

        return connection

    def test_execute_statement(self, mock_connection):
        """Test statement execution."""
        executor = StatementExecutor(mock_connection)

        # Mock successful execution
        mock_connection.client.execute_statement.return_value = {"Id": "stmt-123"}
        mock_connection.client.describe_statement.return_value = {
            "Status": "FINISHED",
            "HasResultSet": True,
            "ResultMetadata": {"ColumnMetadata": []},
            "RecordsUpdated": 0,
        }

        result = executor.execute_statement("SELECT 1")

        assert result["statement_id"] == "stmt-123"

    def test_execute_statement_submission_failure(self, mock_connection):
        """Test statement submission failure with error mapping."""
        executor = StatementExecutor(mock_connection)

        # Mock submission failure
        boto3_error = ClientError(
            error_response={
                "Error": {"Code": "ValidationException", "Message": "Invalid SQL syntax"}
            },
            operation_name="execute_statement",
        )
        mock_connection.client.execute_statement.side_effect = boto3_error

        with pytest.raises(InvalidParameterError, match="Invalid SQL syntax"):
            executor.execute_statement("INVALID SQL")

    def test_polling_statement_failure(self, mock_connection):
        """Test handling of statement execution failure."""
        executor = StatementExecutor(mock_connection)

        # Mock statement submission
        mock_connection.client.execute_statement.return_value = {"Id": "stmt-123"}

        # Mock statement failure
        mock_connection.client.describe_statement.return_value = {
            "Status": "FAILED",
            "Error": "Syntax error at line 1",
            "QueryString": "INVALID SQL",
        }

        from ...dbapi.exceptions import OperationalError

        with pytest.raises(
            OperationalError, match="Statement execution failed: Syntax error at line 1"
        ):
            executor.execute_statement("INVALID SQL")


class TestConnectionErrorHandling:
    """Test error handling in Connection class."""

    @pytest.fixture
    def mock_connection_params(self):
        """Create mock connection parameters."""
        params = Mock()
        params.database_name = "test_db"
        params.cluster_identifier = "test-cluster"
        params.workgroup_name = None
        params.region = "us-east-1"
        params.secret_arn = None
        params.db_user = "test_user"
        return params

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_redshift_data_api.dbapi.connection.create_connection_params"
    )
    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_redshift_data_api.dbapi.connection.RedshiftDataAPIClient"
    )
    def test_transaction_commit_failure(
        self, mock_client_class, mock_create_params, mock_connection_params
    ):
        """Test transaction commit failure with error mapping."""
        mock_create_params.return_value = mock_connection_params

        # Mock client manager
        mock_client_manager = Mock()
        mock_client = Mock()
        mock_client_manager.client = mock_client
        mock_client_class.return_value = mock_client_manager

        # Create connection
        conn = Connection("test-cluster", "test_db", "test_user", "us-east-1")
        conn.transaction_id = "txn-123"

        # Mock commit failure
        boto3_error = ClientError(
            error_response={
                "Error": {"Code": "InternalServerException", "Message": "Internal service error"}
            },
            operation_name="commit_transaction",
        )
        mock_client.commit_transaction.side_effect = boto3_error

        with pytest.raises(DatabaseError, match="Failed to commit transaction"):
            conn.commit()

        assert conn.transaction_id == "txn-123"  # Transaction ID should remain on failure

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_redshift_data_api.dbapi.connection.create_connection_params"
    )
    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_redshift_data_api.dbapi.connection.RedshiftDataAPIClient"
    )
    def test_transaction_rollback_success(
        self, mock_client_class, mock_create_params, mock_connection_params
    ):
        """Test successful transaction rollback."""
        mock_create_params.return_value = mock_connection_params

        # Mock client manager
        mock_client_manager = Mock()
        mock_client = Mock()
        mock_client_manager.client = mock_client
        mock_client_class.return_value = mock_client_manager

        # Create connection
        conn = Connection("test-cluster", "test_db", "test_user", "us-east-1")
        conn.transaction_id = "txn-456"

        # Mock successful rollback
        mock_client.rollback_transaction.return_value = {}

        conn.rollback()

        assert conn.transaction_id is None  # Transaction ID should be cleared

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_redshift_data_api.dbapi.connection.create_connection_params"
    )
    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_redshift_data_api.dbapi.connection.RedshiftDataAPIClient"
    )
    def test_begin_transaction_failure(
        self, mock_client_class, mock_create_params, mock_connection_params
    ):
        """Test begin transaction failure with error mapping."""
        mock_create_params.return_value = mock_connection_params

        # Mock client manager
        mock_client_manager = Mock()
        mock_client = Mock()
        mock_client_manager.client = mock_client
        mock_client_class.return_value = mock_client_manager

        # Create connection
        conn = Connection("test-cluster", "test_db", "test_user", "us-east-1")

        # Mock begin transaction failure
        boto3_error = ClientError(
            error_response={
                "Error": {
                    "Code": "ClusterNotFoundFault",
                    "Message": "Cluster test-cluster not found",
                }
            },
            operation_name="begin_transaction",
        )
        mock_client.begin_transaction.side_effect = boto3_error

        with pytest.raises(DatabaseError, match="Failed to begin transaction"):
            conn.begin_transaction()

        assert conn.transaction_id is None  # No transaction should be created


# --- Long-poll fallback helpers -------------------------------------------------------
#
# The resolved botocore's DescribeStatementRequest declares members ['Id'] only, so
# faking the service model is the only way to reach long-poll mode at all. Every case
# below fakes it; none depends on the real model carrying the parameter.

_LONG_POLL_MEMBER = "WaitTimeSeconds"
_LONG_POLL_WAIT_SECONDS = 30
_NON_TERMINAL_STATUSES = ("SUBMITTED", "PICKED", "STARTED")

# Codes map_boto3_exception treats as parameter problems. A rejection needs one of
# these *and* a message naming the member, so all three are exercised.
_PARAM_REJECTION_ERROR_CODES = ("ValidationException", "InvalidParameterValue", "MissingParameter")

_FINISHED_RESPONSE = {"Status": "FINISHED", "HasResultSet": True, "RecordsUpdated": 0}


def _expected_backoff(poll_count):
    """The classic schedule: min(0.1 * 1.5**k, 1.0) for k in range(poll_count)."""
    return [min(0.1 * 1.5**k, 1.0) for k in range(poll_count)]


def _param_validation_rejection():
    """
    The rejection shape botocore itself produces, verified against the resolved
    botocore: describe_statement(Id=..., WaitTimeSeconds=30) against a model that
    declares only Id raises ParamValidationError, not ClientError.
    """
    return ParamValidationError(
        report='Unknown parameter in input: "WaitTimeSeconds", must be one of: Id'
    )


def _client_error_rejection(error_code="ValidationException"):
    """A service-side rejection: a parameter error code whose message names the member."""
    return ClientError(
        error_response={
            "Error": {
                "Code": error_code,
                "Message": "The parameter WaitTimeSeconds is not supported by this endpoint",
            }
        },
        operation_name="describe_statement",
    )


def _long_poll_connection():
    """A mock connection shaped like the one the other classes in this file build."""
    connection = Mock()
    connection.connection_params = Mock()
    connection.connection_params.database_name = "test_db"
    connection.connection_params.cluster_identifier = "test-cluster"
    connection.connection_params.workgroup_name = None
    connection.connection_params.region = "us-east-1"
    connection.connection_params.secret_arn = None
    connection.connection_params.db_user = "test_user"
    connection.get_transaction_id.return_value = None
    connection.client = Mock()
    return connection


def _fake_supporting_service_model(executor):
    """
    Make the executor's client advertise WaitTimeSeconds on DescribeStatement, so the
    capability check succeeds and the first poll runs in long-poll mode.
    """
    executor.client.meta.service_model.operation_model.return_value.input_shape.members = {
        "Id": object(),
        _LONG_POLL_MEMBER: object(),
    }
    return executor


def _rejection_side_effect(rejection, polls_before, polls_after):
    """
    Build a describe_statement side_effect that reports `polls_before` non-terminal
    statuses, then raises `rejection` on the next call, then reports `polls_after`
    non-terminal statuses before FINISHED.
    """
    responses = [
        {"Status": _NON_TERMINAL_STATUSES[index % len(_NON_TERMINAL_STATUSES)]}
        for index in range(polls_before)
    ]
    responses.append(rejection)
    responses.extend(
        {"Status": _NON_TERMINAL_STATUSES[index % len(_NON_TERMINAL_STATUSES)]}
        for index in range(polls_after)
    )
    responses.append(dict(_FINISHED_RESPONSE))
    return responses


def _describe_kwargs(executor):
    return [call.kwargs for call in executor.client.describe_statement.call_args_list]


def _recorded_sleeps(mock_sleep):
    return [call.args[0] for call in mock_sleep.call_args_list]


# (non-terminal polls before the rejection, non-terminal polls after it). The first
# entry is the scenario named in the plan: rejection on the first poll, then two
# non-terminal statuses and FINISHED. The last has a post-fallback tail long enough
# for the backoff schedule to saturate at its 1.0 second cap.
_REJECTION_SEQUENCES = [
    pytest.param(0, 2, id="reject_first_poll_then_two_non_terminal"),
    pytest.param(0, 0, id="reject_first_poll_then_finished"),
    pytest.param(1, 3, id="reject_second_poll"),
    pytest.param(3, 1, id="reject_fourth_poll"),
    pytest.param(2, 10, id="reject_third_poll_then_saturating_tail"),
]


class TestLongPollFallback:
    """
    Feature: remove-redshift-data-api-query-timeout

    A describe_statement call rejected because it carried WaitTimeSeconds must degrade
    to classic polling and finish the same statement, rather than failing it. The
    internal _LongPollRejected sentinel is a private control signal, so these cases
    assert that no exception surfaces and that the statement completes -- not on the
    sentinel's type.

    The correctness properties these realize are specified as property-based, but the
    package declares only pytest and has no property-testing dependency,
    so they are parameterized pytest cases over a table of rejection points --
    matching how the rest of this suite is written.
    """

    @pytest.fixture
    def supporting_executor(self):
        """An executor whose client advertises the long-poll parameter."""
        return _fake_supporting_service_model(StatementExecutor(_long_poll_connection()))

    @staticmethod
    def _assert_fell_back_and_finished(executor, result, polls_before, polls_after, sleeps):
        """
        The shared outcome for every rejection shape and every rejection point: the
        statement completes through classic polls that omit the parameter, and the
        post-fallback waits restart the backoff schedule.
        """
        assert result["status"] == "FINISHED"
        assert result["statement_id"] == "stmt-fallback"

        kwargs = _describe_kwargs(executor)
        # polls_before long-poll responses, the rejected call, polls_after classic
        # responses, then FINISHED.
        assert len(kwargs) == polls_before + polls_after + 2

        # Every call up to and including the rejected one carried the parameter.
        for index, call_kwargs in enumerate(kwargs[: polls_before + 1]):
            assert call_kwargs == {
                "Id": "stmt-fallback",
                _LONG_POLL_MEMBER: _LONG_POLL_WAIT_SECONDS,
            }, f"long-poll call {index}"

        # Every call after it is classic: exactly the statement id, nothing else.
        for index, call_kwargs in enumerate(kwargs[polls_before + 1 :]):
            assert call_kwargs == {"Id": "stmt-fallback"}, f"post-fallback call {index}"

        # Long-poll mode performs no client-side wait and the fallback itself does not
        # sleep, so every recorded sleep belongs to the post-fallback classic polls.
        assert sleeps == pytest.approx(_expected_backoff(polls_after))
        if polls_after:
            assert sleeps[0] == 0.1

    @pytest.mark.parametrize("polls_before, polls_after", _REJECTION_SEQUENCES)
    def test_param_validation_rejection_falls_back_and_finishes(
        self, supporting_executor, polls_before, polls_after
    ):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 11: A parameter
        rejection falls back and completes the same statement

        Feature: remove-redshift-data-api-query-timeout, Property 12: A fallback
        restarts the backoff schedule

        A botocore ParamValidationError naming WaitTimeSeconds is the only rejection
        shape reachable against any botocore resolvable today, and it is the harder of
        the two to handle: it is not a ClientError, so outside the describe_statement
        closure it has already been rewritten into a bare OperationalError and the
        botocore type is gone. Reaching FINISHED here is what proves the detection sits
        inside the closure and that `except _LongPollRejected` precedes
        `except Exception`.

        **Validates: Requirements 9.1, 9.2, 9.3, 9.4, 11.4**
        """
        supporting_executor.client.execute_statement.return_value = {"Id": "stmt-fallback"}
        supporting_executor.client.describe_statement.side_effect = _rejection_side_effect(
            _param_validation_rejection(), polls_before, polls_after
        )

        # No pytest.raises: the call completing is the assertion that the sentinel
        # never escapes to the caller.
        with patch("time.sleep") as mock_sleep:
            result = supporting_executor.execute_statement("SELECT pg_sleep(1000)")

        self._assert_fell_back_and_finished(
            supporting_executor, result, polls_before, polls_after, _recorded_sleeps(mock_sleep)
        )

    @pytest.mark.parametrize("polls_before, polls_after", _REJECTION_SEQUENCES)
    @pytest.mark.parametrize("error_code", _PARAM_REJECTION_ERROR_CODES)
    def test_service_rejection_falls_back_and_finishes(
        self, supporting_executor, error_code, polls_before, polls_after
    ):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 11: A parameter
        rejection falls back and completes the same statement

        Feature: remove-redshift-data-api-query-timeout, Property 12: A fallback
        restarts the backoff schedule

        The second rejection shape: a service error whose code is one of the parameter
        codes and whose message names the member. All three codes are exercised,
        because the discriminator admits any of them in combination with the message.

        **Validates: Requirements 9.1, 9.2, 9.3, 9.4, 11.4**
        """
        supporting_executor.client.execute_statement.return_value = {"Id": "stmt-fallback"}
        supporting_executor.client.describe_statement.side_effect = _rejection_side_effect(
            _client_error_rejection(error_code), polls_before, polls_after
        )

        with patch("time.sleep") as mock_sleep:
            result = supporting_executor.execute_statement("SELECT pg_sleep(1000)")

        self._assert_fell_back_and_finished(
            supporting_executor, result, polls_before, polls_after, _recorded_sleeps(mock_sleep)
        )

    @pytest.mark.parametrize(
        "rejection_factory",
        [
            pytest.param(_param_validation_rejection, id="param_validation_error"),
            pytest.param(_client_error_rejection, id="client_error"),
        ],
    )
    @pytest.mark.parametrize("polls_after", [1, 3, 7, 12])
    def test_post_fallback_backoff_restarts_and_stays_capped(
        self, supporting_executor, rejection_factory, polls_after
    ):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 12: A fallback
        restarts the backoff schedule

        The fallback resets poll_interval rather than inheriting whatever the interval
        happened to be, so the first wait after it is 0.1 seconds and the sequence is
        the full schedule from k=0. The 12-poll case runs past k=6, where
        0.1 * 1.5**k would exceed 1.0, so it also pins the cap.

        **Validates: Requirements 9.3**
        """
        supporting_executor.client.execute_statement.return_value = {"Id": "stmt-fallback"}
        supporting_executor.client.describe_statement.side_effect = _rejection_side_effect(
            rejection_factory(), 0, polls_after
        )

        with patch("time.sleep") as mock_sleep:
            result = supporting_executor.execute_statement("SELECT 1")

        assert result["status"] == "FINISHED"
        sleeps = _recorded_sleeps(mock_sleep)
        assert len(sleeps) == polls_after
        assert sleeps[0] == 0.1
        assert sleeps == pytest.approx(_expected_backoff(polls_after))
        assert max(sleeps) <= 1.0

    def test_fallback_is_scoped_to_the_statement_it_occurred_in(self, supporting_executor):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 11: A parameter
        rejection falls back and completes the same statement

        A fallback is loop-local by design: _long_poll_supported_memo records only the
        service-model inspection, never a runtime rejection, because Requirement 9.1
        scopes a fallback to "the statement execution in which it occurred". So the
        next statement on the same executor tries long poll again. That costs at most
        one wasted request on a client that advertises the parameter but refuses it,
        and it is the design's stated intent -- not a leak to be read as a defect.

        **Validates: Requirements 9.1, 9.2**
        """
        supporting_executor.client.execute_statement.return_value = {"Id": "stmt-fallback"}
        supporting_executor.client.describe_statement.side_effect = _rejection_side_effect(
            _param_validation_rejection(), 0, 1
        )

        with patch("time.sleep"):
            first = supporting_executor.execute_statement("SELECT 1")

        assert first["status"] == "FINISHED"
        assert _describe_kwargs(supporting_executor)[-1] == {"Id": "stmt-fallback"}

        supporting_executor.client.describe_statement.reset_mock()
        supporting_executor.client.describe_statement.side_effect = None
        supporting_executor.client.describe_statement.return_value = dict(_FINISHED_RESPONSE)

        with patch("time.sleep"):
            second = supporting_executor.execute_statement("SELECT 2")

        assert second["status"] == "FINISHED"
        assert _describe_kwargs(supporting_executor) == [
            {"Id": "stmt-fallback", _LONG_POLL_MEMBER: _LONG_POLL_WAIT_SECONDS}
        ]


# --- Non-rejection discrimination helpers ---------------------------------------------
#
# The discriminator is deliberately narrower than the error code: a ValidationException
# must *also* name WaitTimeSeconds to count as a parameter rejection. Every failure below
# is one the narrowed discriminator has to let through unchanged.


def _non_rejection_client_error(error_code, message):
    """A describe_statement service error that must not be read as a parameter rejection."""
    return ClientError(
        error_response={"Error": {"Code": error_code, "Message": message}},
        operation_name="describe_statement",
    )


def _executor_in_mode(long_poll):
    """
    An executor polling in long-poll or classic mode.

    Classic mode needs no shaping: `"WaitTimeSeconds" in Mock()` raises TypeError and the
    capability check's fail-open guard turns that into "not supported", which is why the
    rest of this suite polls classically.
    """
    executor = StatementExecutor(_long_poll_connection())
    return _fake_supporting_service_model(executor) if long_poll else executor


# One call, plus the three retries RetryConfig(max_attempts=3) allows. Only the transient
# codes in RetryConfig.should_retry reach this count; everything else raises on the first.
_RETRIED_CALLS = 4

# Each row: the failure describe_statement raises, how many describe_statement calls the
# driver makes, and the exception type and message fragment the caller actually receives.
#
# The expected types were measured by running the chain, not predicted from it. Worth
# knowing when reading them: retry_on_transient_error maps the exception onto a local and
# then re-raises with a bare `raise`, which re-raises the *original* exception rather than
# the mapped local, so the mapping the caller sees is the polling loop's own single
# map_boto3_exception call. A ClientError therefore keeps its per-code mapping
# (InvalidParameterError, TransientError) instead of collapsing into OperationalError,
# while a non-ClientError has no per-code mapping and becomes "AWS service error: ...".
_NON_REJECTION_FAILURES = [
    pytest.param(
        lambda: _non_rejection_client_error("ValidationException", "Invalid session id"),
        1,
        InvalidParameterError,
        "Invalid session id",
        id="validation_exception_not_naming_member",
    ),
    pytest.param(
        lambda: _non_rejection_client_error("ValidationException", "Invalid NextToken"),
        1,
        InvalidParameterError,
        "Invalid NextToken",
        id="validation_exception_invalid_next_token",
    ),
    pytest.param(
        lambda: _non_rejection_client_error(
            "ValidationException", "Statement id abc-123 is not valid"
        ),
        1,
        InvalidParameterError,
        "Statement id abc-123 is not valid",
        id="validation_exception_bad_statement_id",
    ),
    pytest.param(
        # A parameter code is not enough on its own, and naming the member is not enough
        # on its own either: throttling names it here and is still not a rejection,
        # because ThrottlingException is not a parameter code.
        lambda: _non_rejection_client_error(
            "ThrottlingException", "Rate exceeded while waiting WaitTimeSeconds"
        ),
        _RETRIED_CALLS,
        TransientError,
        "Rate exceeded while waiting WaitTimeSeconds",
        id="throttling_exception_naming_member",
    ),
    pytest.param(
        # Not a botocore exception at all, so neither discriminator arm applies however
        # suggestive the text is.
        lambda: RuntimeError("socket closed during WaitTimeSeconds wait"),
        1,
        OperationalError,
        "AWS service error: socket closed during WaitTimeSeconds wait",
        id="non_botocore_error_naming_member",
    ),
    pytest.param(
        # The ParamValidationError arm is exact: botocore enumerates the offending member,
        # so a report about some other parameter is not this parameter's rejection.
        lambda: ParamValidationError(
            report='Unknown parameter in input: "Nonsense", must be one of: Id'
        ),
        1,
        OperationalError,
        "AWS service error: Parameter validation failed",
        id="param_validation_error_not_naming_member",
    ),
]

_POLLING_MODES = [
    pytest.param(True, id="long_poll"),
    pytest.param(False, id="classic"),
]


class TestNonRejectionDiscrimination:
    """
    Feature: remove-redshift-data-api-query-timeout

    The negative half of the fallback: a describe_statement failure that is *not* a
    parameter rejection must reach the caller as the error it is.

    This is what keeps the narrowing in _is_long_poll_rejection honest. If the ClientError
    arm matched on error code alone, redshift-data's ValidationException -- which it also
    returns for a malformed statement id, a stale session id, or a bad NextToken -- would
    be silently converted into a mode switch. The statement would then fail or hang for a
    reason the user never gets told, which is precisely the misreading Requirement 9.1
    warns against.

    Both polling modes are covered because the loop must behave the same way in each: in
    classic mode the discriminator is not even consulted (the `use_long_poll and ...`
    guard short-circuits), and in long-poll mode it is consulted and says no.

    As with the fallback cases, the package declares only pytest and has no
    property-testing dependency, so this property is realized as parameterized cases over
    a table of failure shapes.
    """

    @pytest.mark.parametrize("long_poll", _POLLING_MODES)
    @pytest.mark.parametrize(
        "failure_factory, expected_calls, expected_type, message_fragment",
        _NON_REJECTION_FAILURES,
    )
    def test_non_rejection_describe_failure_propagates_mapped(
        self, long_poll, failure_factory, expected_calls, expected_type, message_fragment
    ):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 13: Every non-rejection
        describe failure propagates mapped

        The failure surfaces as the driver's mapping chain produces it, the mode never
        switches, and the loop neither swallows the error nor keeps polling past it.

        **Validates: Requirements 2.6, 9.5, 11.5**
        """
        executor = _executor_in_mode(long_poll)
        executor.client.execute_statement.return_value = {"Id": "stmt-error"}
        executor.client.describe_statement.side_effect = failure_factory()

        expected_kwargs = {"Id": "stmt-error"}
        if long_poll:
            expected_kwargs[_LONG_POLL_MEMBER] = _LONG_POLL_WAIT_SECONDS

        with patch("time.sleep") as mock_sleep:
            with pytest.raises(expected_type) as exc_info:
                executor.execute_statement("SELECT 1")

        # Pin the exact class, not just the branch of the hierarchy: the point of the
        # property is that this failure is reported as itself.
        assert type(exc_info.value) is expected_type
        assert message_fragment in str(exc_info.value)

        # No fallback: the request shape is the same on every call, so a long-poll call
        # that failed was never retried without the parameter.
        kwargs = _describe_kwargs(executor)
        assert len(kwargs) == expected_calls
        for index, call_kwargs in enumerate(kwargs):
            assert call_kwargs == expected_kwargs, f"describe call {index}"

        # Every recorded wait belongs to the retry helper between its attempts. The loop
        # never reached a non-terminal status, so none of these is a poll interval -- and
        # a fallback-and-continue would have added both a poll and a 0.1 second wait.
        assert len(_recorded_sleeps(mock_sleep)) == expected_calls - 1

    def test_unrelated_validation_error_is_not_absorbed_into_a_mode_switch(self):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 13: Every non-rejection
        describe failure propagates mapped

        The case the narrowing exists for, spelled out: long-poll mode is active, the
        service answers with ValidationException, and the message is about a session --
        nothing to do with WaitTimeSeconds. Exactly one describe call is the assertion
        that matters. A second one would mean the driver had read "ValidationException"
        as "the parameter was refused", dropped the parameter, and re-polled the same
        statement, leaving the real error unreported.

        **Validates: Requirements 2.6, 9.5, 11.5**
        """
        executor = _executor_in_mode(long_poll=True)
        executor.client.execute_statement.return_value = {"Id": "stmt-error"}
        executor.client.describe_statement.side_effect = _non_rejection_client_error(
            "ValidationException", "Invalid session id"
        )

        with patch("time.sleep") as mock_sleep:
            with pytest.raises(InvalidParameterError) as exc_info:
                executor.execute_statement("SELECT 1")

        assert "Invalid session id" in str(exc_info.value)
        assert executor.client.describe_statement.call_count == 1
        assert _describe_kwargs(executor) == [
            {"Id": "stmt-error", _LONG_POLL_MEMBER: _LONG_POLL_WAIT_SECONDS}
        ]
        assert _recorded_sleeps(mock_sleep) == []


if __name__ == "__main__":
    pytest.main([__file__])
