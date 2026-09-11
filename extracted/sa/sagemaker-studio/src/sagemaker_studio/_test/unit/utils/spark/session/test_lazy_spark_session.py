"""
Unit tests for LazySparkSession.

This module tests the lazy loading functionality for Spark sessions.
"""

import logging
import sys
import types
from unittest.mock import Mock, PropertyMock, patch

import pytest


# Create a proper mock exception class that inherits from Exception
class MockSparkConnectGrpcException(Exception):
    """Mock SparkConnectGrpcException that properly inherits from Exception."""

    pass


# Snapshot `sys.modules` so the stand-ins installed below can be taken back out.
_modules_before = dict(sys.modules)

# Mock PySpark and gRPC modules before importing our code
with patch("sagemaker_studio.Project"):

    sys.modules["aws_embedded_metrics"] = Mock()
    sys.modules["aws_embedded_metrics.sinks"] = Mock()
    sys.modules["aws_embedded_metrics.sinks.stdout_sink"] = Mock()
    sys.modules["aws_embedded_metrics.logger"] = Mock()
    sys.modules["aws_embedded_metrics.logger.metrics_logger"] = Mock()
    sys.modules["aws_embedded_metrics.logger.metrics_context"] = Mock()
    sys.modules["aws_embedded_metrics.environment"] = Mock()
    sys.modules["aws_embedded_metrics.environment.local_environment"] = Mock()

    pyspark_modules = [
        "pyspark",
        "pyspark.sql",
        "pyspark.sql.session",
        "pyspark.sql.connect",
        "pyspark.sql.connect.session",
        "pyspark.sql.connect.client",
        # sagemaker_studio.utils.udf.routed does ``from pyspark.rdd import
        # PythonEvalType`` at module load, so the mocked pyspark must expose
        # ``pyspark.rdd`` with a PythonEvalType.
        "pyspark.rdd",
        "grpc",
        "pyspark.errors",
        "pyspark.errors.exceptions",
        "pyspark.errors.exceptions.connect",
    ]

    for module_name in pyspark_modules:
        if module_name not in sys.modules:
            mock_module = Mock()
            if module_name == "grpc":
                # Mock gRPC specific classes and functions
                mock_module.insecure_channel = Mock()
                mock_module.secure_channel = Mock()
                mock_module.intercept_channel = Mock()
                # Interceptor bases and ClientCallDetails must be real classes
                # because base_interceptors.py subclasses them (see test_base_interceptors.py).
                mock_module.UnaryUnaryClientInterceptor = type(
                    "UnaryUnaryClientInterceptor", (), {}
                )
                mock_module.UnaryStreamClientInterceptor = type(
                    "UnaryStreamClientInterceptor", (), {}
                )
                mock_module.StreamUnaryClientInterceptor = type(
                    "StreamUnaryClientInterceptor", (), {}
                )
                mock_module.StreamStreamClientInterceptor = type(
                    "StreamStreamClientInterceptor", (), {}
                )
                mock_module.ClientCallDetails = type("ClientCallDetails", (tuple,), {})
            elif module_name == "pyspark.sql.connect.client":
                mock_module.ChannelBuilder = Mock()
            elif module_name == "pyspark.errors.exceptions.connect":
                mock_module.SparkConnectGrpcException = MockSparkConnectGrpcException
            elif module_name == "pyspark.rdd":
                # sagemaker_studio.utils.udf.routed imports PythonEvalType from
                # here at module load.
                mock_module.PythonEvalType = Mock()
            sys.modules[module_name] = mock_module

    # Mock interceptors modules to avoid importing actual gRPC interceptors
    mock_athena_interceptors = Mock()
    mock_athena_interceptors.CustomChannelBuilder = Mock()
    sys.modules["sagemaker_studio.utils.spark.session.athena.interceptors"] = (
        mock_athena_interceptors
    )
    mock_emr_interceptors = Mock()
    mock_emr_interceptors.CustomChannelBuilder = Mock()
    sys.modules["sagemaker_studio.utils.spark.session.emr_serverless.interceptors"] = (
        mock_emr_interceptors
    )

    from sagemaker_studio.utils.spark.session.lazy_spark_session import (  # noqa: E402
        LazySparkSession,
    )
    from sagemaker_studio.utils.spark.session.spark_session_manager import (  # noqa: E402
        SparkSessionManager,
    )

# Put `sys.modules` back as this module found it. The stand-ins above are needed
# only for the import that just happened; pytest imports every test module during
# COLLECTION, so one left installed here stays installed for the rest of the
# session and silently changes what every later test imports.
_stand_in_names = {
    _name
    for _name, _module in sys.modules.items()
    if not isinstance(_module, types.ModuleType) and _module is not _modules_before.get(_name)
}
for _name in list(sys.modules):
    if _name in _modules_before:
        if sys.modules[_name] is not _modules_before[_name]:
            sys.modules[_name] = _modules_before[_name]
    elif _name in _stand_in_names or any(
        _name.startswith(_root + ".") for _root in _stand_in_names
    ):
        # A stand-in, or something imported UNDER one. A real submodule reached
        # through a mocked parent is registered without the parent ever gaining the
        # attribute, so a later import of it fails ("cannot import name ...").
        # Drop both kinds so the next importer builds a clean one.
        del sys.modules[_name]


@pytest.fixture
def mock_spark_session():
    """Create a mock SparkSession for testing."""
    return Mock()


class TestLazySparkSession:
    """Test cases for LazySparkSession class."""

    def test_init_with_session_manager(self, mock_spark_session):
        """Test LazySparkSession initialization with session manager."""
        mock_manager = Mock(spec=SparkSessionManager)
        lazy_session = LazySparkSession(mock_manager)

        assert lazy_session._spark is None
        assert lazy_session._session_manager is mock_manager

    def test_init_without_session_manager(self):
        """Test LazySparkSession initialization without session manager."""
        lazy_session = LazySparkSession(None)

        assert lazy_session._spark is None
        assert lazy_session._session_manager is None

    def test_get_spark_creates_session_on_first_call(self, mock_spark_session):
        """Test that _get_spark creates session on first call."""
        mock_manager = Mock(spec=SparkSessionManager)
        mock_manager.create.return_value = mock_spark_session
        mock_project = Mock()
        mock_manager.project = mock_project
        mock_connection = Mock()
        mock_project.connection.return_value = mock_connection
        mock_connection.catalogs = []
        lazy_session = LazySparkSession(mock_manager)

        # First call should create the session
        result = lazy_session._get_spark()

        assert result is mock_spark_session
        assert lazy_session._spark is mock_spark_session
        mock_manager.create.assert_called_once()

    def test_get_spark_returns_existing_session_on_subsequent_calls(self, mock_spark_session):
        """Test that _get_spark returns existing session on subsequent calls."""
        mock_manager = Mock(spec=SparkSessionManager)
        mock_manager.create.return_value = mock_spark_session
        mock_project = Mock()
        mock_manager.project = mock_project
        mock_connection = Mock()
        mock_project.connection.return_value = mock_connection
        mock_connection.catalogs = []
        lazy_session = LazySparkSession(mock_manager)

        # First call creates the session
        first_result = lazy_session._get_spark()
        # Second call should return the same session
        second_result = lazy_session._get_spark()

        assert first_result is second_result
        assert first_result is mock_spark_session
        # create should only be called once
        mock_manager.create.assert_called_once()

    def test_get_spark_handles_creation_exception(self):
        """Test that _get_spark properly handles session creation exceptions."""
        mock_manager = Mock(spec=SparkSessionManager)
        mock_manager.create.side_effect = Exception("Creation failed")

        lazy_session = LazySparkSession(mock_manager)

        with pytest.raises(Exception, match="Creation failed"):
            lazy_session._get_spark()

    def test_getattr_delegates_to_spark_session(self, mock_spark_session):
        """Test that __getattr__ delegates to the underlying SparkSession."""
        mock_manager = Mock(spec=SparkSessionManager)
        mock_manager.create.return_value = mock_spark_session
        mock_project = Mock()
        mock_manager.project = mock_project
        mock_connection = Mock()
        mock_project.connection.return_value = mock_connection
        mock_connection.catalogs = []
        mock_spark_session.sql = Mock(return_value="sql_result")

        lazy_session = LazySparkSession(mock_manager)

        # Access an attribute - should delegate to SparkSession
        result = lazy_session.sql

        assert result is mock_spark_session.sql
        mock_manager.create.assert_called_once()

    @patch(
        "sagemaker_studio.utils.spark.session.lazy_spark_session.SparkConnectGrpcException",
        MockSparkConnectGrpcException,
    )
    def test_getattr_handles_spark_access_exception(self):
        """Test that __getattr__ handles exceptions when accessing Spark attributes."""
        mock_manager = Mock(spec=SparkSessionManager)
        mock_manager.create.side_effect = Exception("Spark access failed")

        lazy_session = LazySparkSession(mock_manager)

        with pytest.raises(Exception, match="Spark access failed"):
            _ = lazy_session.some_attribute

    @patch(
        "sagemaker_studio.utils.spark.session.lazy_spark_session.SparkConnectGrpcException",
        MockSparkConnectGrpcException,
    )
    def test_getattr_handles_spark_connect_grpc_exception(self):
        """Test that __getattr__ handles SparkConnectGrpcException by recreating the session."""
        mock_manager = Mock(spec=SparkSessionManager)
        mock_project = Mock()
        mock_manager.project = mock_project
        mock_connection = Mock()
        mock_project.connection.return_value = mock_connection
        mock_connection.catalogs = []

        # First call to create returns a session that will raise a SparkConnectGrpcException
        bad_spark_session = Mock(spec=LazySparkSession)
        type(bad_spark_session).version = PropertyMock(side_effect=MockSparkConnectGrpcException)

        # Second call to create returns a working session
        working_spark_session = Mock()
        working_spark_session.version = "3.0.0"
        working_spark_session.sql = Mock(return_value="sql_result")

        mock_manager.create.side_effect = [bad_spark_session, working_spark_session]

        lazy_session = LazySparkSession(mock_manager)

        # Access an attribute - should trigger SparkConnectGrpcException handling
        result = lazy_session.sql

        # Verify that:
        # 1. Session manager was called twice (initial + after exception)
        assert mock_manager.create.call_count == 2
        # 2. Stop was called
        mock_manager.stop.assert_called_once()
        # 3. The final result comes from the working session
        assert result is working_spark_session.sql

    def test_repr_returns_spark_session_repr(self, mock_spark_session):
        """Test that __repr__ returns the SparkSession representation."""
        mock_manager = Mock(spec=SparkSessionManager)
        mock_manager.create.return_value = mock_spark_session
        mock_project = Mock()
        mock_manager.project = mock_project
        mock_connection = Mock()
        mock_project.connection.return_value = mock_connection
        mock_connection.catalogs = []
        mock_spark_session.__repr__ = Mock(return_value="<MockSparkSession>")

        lazy_session = LazySparkSession(mock_manager)

        result = repr(lazy_session)

        assert result == "<MockSparkSession>"
        mock_manager.create.assert_called_once()

    def test_repr_handles_exception(self):
        """Test that __repr__ handles exceptions gracefully."""
        mock_manager = Mock(spec=SparkSessionManager)
        mock_project = Mock()
        mock_manager.project = mock_project
        mock_connection = Mock()
        mock_project.connection.return_value = mock_connection
        mock_connection.catalogs = []
        mock_manager.create.side_effect = Exception("Repr failed")

        lazy_session = LazySparkSession(mock_manager)

        result = repr(lazy_session)

        assert "LazySparkSession (error: Repr failed)" in result

    @patch("sagemaker_studio.utils.spark.session.lazy_spark_session._SparkSession")
    def test_class_property_returns_spark_session_class(self, mock_spark_session_class):
        """Test that __class__ property returns SparkSession class."""
        mock_manager = Mock(spec=SparkSessionManager)
        mock_project = Mock()
        mock_manager.project = mock_project
        mock_connection = Mock()
        mock_project.connection.return_value = mock_connection
        mock_connection.catalogs = []
        lazy_session = LazySparkSession(mock_manager)

        result = lazy_session.__class__

        assert result is mock_spark_session_class

    def test_stop_calls_session_manager_stop(self, mock_spark_session):
        """Test that stop() calls session manager stop and resets session."""
        mock_manager = Mock(spec=SparkSessionManager)
        mock_manager.create.return_value = mock_spark_session
        mock_project = Mock()
        mock_manager.project = mock_project
        mock_connection = Mock()
        mock_project.connection.return_value = mock_connection
        mock_connection.catalogs = []

        lazy_session = LazySparkSession(mock_manager)

        # Create the session first
        lazy_session._get_spark()
        assert lazy_session._spark is not None

        # Stop the session
        lazy_session.stop()

        mock_manager.stop.assert_called_once()
        assert lazy_session._spark is None

    def test_stop_handles_session_manager_exception(self, mock_spark_session, caplog):
        """Test that stop() handles session manager exceptions gracefully."""
        mock_manager = Mock(spec=SparkSessionManager)
        mock_manager.create.return_value = mock_spark_session
        mock_manager.stop.side_effect = Exception("Stop failed")
        mock_project = Mock()
        mock_manager.project = mock_project
        mock_connection = Mock()
        mock_project.connection.return_value = mock_connection
        mock_connection.catalogs = []

        lazy_session = LazySparkSession(mock_manager)

        # Create the session first
        lazy_session._get_spark()

        with caplog.at_level(logging.ERROR):
            lazy_session.stop()

        # Should still reset the session even if stop failed
        assert lazy_session._spark is None
        assert "Error while stopping session manager" in caplog.text

    def test_stop_with_no_session_manager(self):
        """Test that stop() works when no session manager is present."""
        lazy_session = LazySparkSession(None)

        # Should not raise an exception
        lazy_session.stop()

        assert lazy_session._spark is None

    def test_init_with_deferred_params(self):
        """Test LazySparkSession initialization with deferred connection_name and config."""
        lazy_session = LazySparkSession(None, connection_name="my-conn", config="my-config")

        assert lazy_session._spark is None
        assert lazy_session._session_manager is None
        assert lazy_session._connection_name == "my-conn"
        assert lazy_session._config == "my-config"

    @patch(
        "sagemaker_studio.utils.spark.session.lazy_spark_session.SparkConnectGrpcException",
        MockSparkConnectGrpcException,
    )
    def test_get_spark_deferred_resolution(self):
        """Test _get_spark resolves session manager lazily when not provided."""
        mock_manager = Mock(spec=SparkSessionManager)
        mock_spark = Mock()
        mock_manager.create.return_value = mock_spark
        mock_manager.get_session_id.return_value = "sess-1"
        mock_project = Mock()
        mock_manager.project = mock_project
        mock_connection = Mock()
        mock_project.connection.return_value = mock_connection
        mock_connection.catalogs = []

        lazy_session = LazySparkSession(None, connection_name="deferred-conn", config="cfg")

        with patch(
            "sagemaker_studio.utils.spark.session.lazy_spark_session._resolve_connection_and_create_session_manager",
            return_value=mock_manager,
        ) as mock_resolve:
            result = lazy_session._get_spark()

        mock_resolve.assert_called_once_with(
            connection_name="deferred-conn", config="cfg", spark_conf=None
        )
        assert result is mock_spark
        assert lazy_session._session_manager is mock_manager

    @patch(
        "sagemaker_studio.utils.spark.session.lazy_spark_session.SparkConnectGrpcException",
        MockSparkConnectGrpcException,
    )
    def test_getattr_client_error_athena_stopped(self):
        """Test __getattr__ handles ClientError for Athena STOPPED state."""
        from botocore.exceptions import ClientError

        mock_manager = Mock(spec=SparkSessionManager)
        mock_project = Mock()
        mock_manager.project = mock_project
        mock_connection = Mock()
        mock_project.connection.return_value = mock_connection
        mock_connection.catalogs = []

        # First session raises ClientError on version access
        bad_session = Mock()
        error_response = {
            "Error": {"Code": "InvalidRequestException", "Message": "Session is in STOPPED state"}
        }
        type(bad_session).version = PropertyMock(
            side_effect=ClientError(error_response, "GetSession")
        )

        # Second session works
        good_session = Mock()
        good_session.version = "3.0.0"
        good_session.sql = Mock(return_value="result")

        mock_manager.create.side_effect = [bad_session, good_session]

        lazy_session = LazySparkSession(mock_manager)

        result = lazy_session.sql
        assert result is good_session.sql
        assert mock_manager.create.call_count == 2
        mock_manager.stop.assert_called_once()

    @patch(
        "sagemaker_studio.utils.spark.session.lazy_spark_session.SparkConnectGrpcException",
        MockSparkConnectGrpcException,
    )
    def test_getattr_client_error_emr_resource_not_found(self):
        """Test __getattr__ handles ClientError for EMR ResourceNotFoundException."""
        from botocore.exceptions import ClientError

        mock_manager = Mock(spec=SparkSessionManager)
        mock_project = Mock()
        mock_manager.project = mock_project
        mock_connection = Mock()
        mock_project.connection.return_value = mock_connection
        mock_connection.catalogs = []

        bad_session = Mock()
        error_response = {
            "Error": {"Code": "ResourceNotFoundException", "Message": "Session not found"}
        }
        type(bad_session).version = PropertyMock(
            side_effect=ClientError(error_response, "GetSession")
        )

        good_session = Mock()
        good_session.version = "3.0.0"
        good_session.sql = Mock(return_value="result")

        mock_manager.create.side_effect = [bad_session, good_session]

        lazy_session = LazySparkSession(mock_manager)

        result = lazy_session.sql
        assert result is good_session.sql
        mock_manager.stop.assert_called_once()

    @patch(
        "sagemaker_studio.utils.spark.session.lazy_spark_session.SparkConnectGrpcException",
        MockSparkConnectGrpcException,
    )
    def test_getattr_client_error_unknown_reraises(self):
        """Test __getattr__ re-raises unknown ClientErrors."""
        from botocore.exceptions import ClientError

        mock_manager = Mock(spec=SparkSessionManager)
        mock_project = Mock()
        mock_manager.project = mock_project
        mock_connection = Mock()
        mock_project.connection.return_value = mock_connection
        mock_connection.catalogs = []

        bad_session = Mock()
        error_response = {"Error": {"Code": "AccessDeniedException", "Message": "Not authorized"}}
        type(bad_session).version = PropertyMock(
            side_effect=ClientError(error_response, "GetSession")
        )

        mock_manager.create.return_value = bad_session

        lazy_session = LazySparkSession(mock_manager)

        with pytest.raises(ClientError):
            _ = lazy_session.sql

    def test_get_athena_session_id_with_athena_manager(self):
        """Test get_athena_session_id returns session ID for Athena managers."""
        # Import the actual AthenaSparkSessionManager class (already mocked at module level)
        from sagemaker_studio.utils.spark.session.athena.athena_spark_session_manager import (
            AthenaSparkSessionManager,
        )

        mock_manager = Mock(spec=AthenaSparkSessionManager)
        mock_manager.get_session_id.return_value = "athena-sess-1"

        lazy_session = LazySparkSession(mock_manager)
        result = lazy_session.get_athena_session_id()

        assert result == "athena-sess-1"

    def test_get_athena_session_id_with_non_athena_manager(self):
        """Test get_athena_session_id returns None for non-Athena managers."""
        mock_manager = Mock(spec=SparkSessionManager)
        lazy_session = LazySparkSession(mock_manager)

        result = lazy_session.get_athena_session_id()

        assert result is None

    def test_get_athena_session_id_no_manager(self):
        """Test get_athena_session_id returns None when no manager."""
        lazy_session = LazySparkSession(None)

        result = lazy_session.get_athena_session_id()

        assert result is None

    def test_get_session_id_with_manager(self):
        """Test get_session_id returns session ID from manager."""
        mock_manager = Mock(spec=SparkSessionManager)
        mock_manager.get_session_id.return_value = "sess-xyz"
        lazy_session = LazySparkSession(mock_manager)

        assert lazy_session.get_session_id() == "sess-xyz"

    def test_get_session_id_no_manager(self):
        """Test get_session_id returns None when no manager."""
        lazy_session = LazySparkSession(None)
        assert lazy_session.get_session_id() is None

    def test_get_session_info_with_active_session(self):
        """Test get_session_info returns dict with session_id and session_type."""
        mock_manager = Mock(spec=SparkSessionManager)
        mock_manager.get_session_id.return_value = "sess-info"
        type(mock_manager).__name__ = "EMRServerlessSparkSessionManager"
        lazy_session = LazySparkSession(mock_manager)

        result = lazy_session.get_session_info()

        assert result == {
            "session_id": "sess-info",
            "session_type": "EMR_SERVERLESS_SPARK_CONNECT",
        }

    def test_get_session_info_athena(self):
        """Test get_session_info returns correct type for Athena."""
        mock_manager = Mock(spec=SparkSessionManager)
        mock_manager.get_session_id.return_value = "athena-sess"
        type(mock_manager).__name__ = "AthenaSparkSessionManager"
        lazy_session = LazySparkSession(mock_manager)

        result = lazy_session.get_session_info()

        assert result == {
            "session_id": "athena-sess",
            "session_type": "ATHENA_SPARK_CONNECT",
        }

    def test_get_session_info_emr_ec2(self):
        """Test get_session_info returns correct type for EMR on EC2."""
        mock_manager = Mock(spec=SparkSessionManager)
        mock_manager.get_session_id.return_value = "emr-ec2-sess"
        type(mock_manager).__name__ = "EmrEc2SparkSessionManager"
        lazy_session = LazySparkSession(mock_manager)

        result = lazy_session.get_session_info()

        assert result == {
            "session_id": "emr-ec2-sess",
            "session_type": "EMR_EC2_SPARK_CONNECT",
        }

    def test_get_session_info_no_manager(self):
        """Test get_session_info returns None when no manager."""
        lazy_session = LazySparkSession(None)
        assert lazy_session.get_session_info() is None

    def test_get_session_info_no_session_id(self):
        """Test get_session_info returns None when session_id is None."""
        mock_manager = Mock(spec=SparkSessionManager)
        mock_manager.get_session_id.return_value = None
        lazy_session = LazySparkSession(mock_manager)

        assert lazy_session.get_session_info() is None

    def test_get_session_info_unknown_manager(self):
        """Test get_session_info uses class name as fallback for unknown managers."""
        mock_manager = Mock(spec=SparkSessionManager)
        mock_manager.get_session_id.return_value = "sess-custom"
        type(mock_manager).__name__ = "CustomSparkManager"
        lazy_session = LazySparkSession(mock_manager)

        result = lazy_session.get_session_info()

        assert result == {
            "session_id": "sess-custom",
            "session_type": "CustomSparkManager",
        }

    def test_stop_logs_session_duration_metric(self, mock_spark_session):
        """Test that stop() logs session duration metric when session was started."""
        mock_manager = Mock(spec=SparkSessionManager)
        mock_manager.create.return_value = mock_spark_session
        mock_manager.get_session_id.return_value = "sess-dur"
        mock_project = Mock()
        mock_manager.project = mock_project
        mock_connection = Mock()
        mock_project.connection.return_value = mock_connection
        mock_connection.catalogs = []
        type(mock_manager).__name__ = "EMRServerlessSparkSessionManager"

        lazy_session = LazySparkSession(mock_manager)
        lazy_session._get_spark()

        with patch("sagemaker_studio.utils.loggerutils.log_session_metric") as mock_log:
            lazy_session.stop()

        mock_log.assert_called()
        # Find the SessionStopped call (there may also be a SessionCreated call from _get_spark)
        stop_calls = [
            c for c in mock_log.call_args_list if c[1].get("metric_name") == "SessionStopped"
        ]
        assert len(stop_calls) == 1
        assert stop_calls[0][1]["session_id"] == "sess-dur"

    def test_stop_metric_logging_exception_handled(self, mock_spark_session, caplog):
        """Test that stop() handles metric logging exceptions gracefully."""
        mock_manager = Mock(spec=SparkSessionManager)
        mock_manager.create.return_value = mock_spark_session
        mock_project = Mock()
        mock_manager.project = mock_project
        mock_connection = Mock()
        mock_project.connection.return_value = mock_connection
        mock_connection.catalogs = []

        lazy_session = LazySparkSession(mock_manager)
        lazy_session._get_spark()

        with patch(
            "sagemaker_studio.utils.loggerutils.log_session_metric",
            side_effect=Exception("metric error"),
        ), caplog.at_level(logging.ERROR):
            lazy_session.stop()

        assert lazy_session._spark is None
        assert "Failed to log session stop metric" in caplog.text

    def test_get_spark_logs_session_creation_metric(self):
        """Test that _get_spark logs SessionCreated metric."""
        mock_manager = Mock(spec=SparkSessionManager)
        mock_spark = Mock()
        mock_manager.create.return_value = mock_spark
        mock_manager.get_session_id.return_value = "sess-metric"
        mock_project = Mock()
        mock_manager.project = mock_project
        mock_connection = Mock()
        mock_project.connection.return_value = mock_connection
        mock_connection.catalogs = []
        type(mock_manager).__name__ = "AthenaSparkSessionManager"

        lazy_session = LazySparkSession(mock_manager)

        with patch("sagemaker_studio.utils.loggerutils.log_session_metric") as mock_log:
            lazy_session._get_spark()

        mock_log.assert_called_once()
        call_kwargs = mock_log.call_args[1]
        assert call_kwargs["metric_name"] == "SessionCreated"
        assert call_kwargs["additional_properties"]["SessionType"] == "ATHENA_SPARK_CONNECT"

    def test_get_spark_metric_logging_failure_does_not_block(self):
        """Test that _get_spark continues even if metric logging fails."""
        mock_manager = Mock(spec=SparkSessionManager)
        mock_spark = Mock()
        mock_manager.create.return_value = mock_spark
        mock_project = Mock()
        mock_manager.project = mock_project
        mock_connection = Mock()
        mock_project.connection.return_value = mock_connection
        mock_connection.catalogs = []

        lazy_session = LazySparkSession(mock_manager)

        with patch(
            "sagemaker_studio.utils.loggerutils.log_session_metric",
            side_effect=Exception("metric fail"),
        ):
            result = lazy_session._get_spark()

        assert result is mock_spark

    @patch(
        "sagemaker_studio.utils.spark.session.lazy_spark_session.SparkConnectGrpcException",
        MockSparkConnectGrpcException,
    )
    @pytest.mark.parametrize(
        "error_code", ["EntityNotFoundException", "IllegalSessionStateException"]
    )
    def test_getattr_client_error_glue_session_recovery(self, error_code):
        """Test __getattr__ handles Glue ClientErrors by stopping and recreating the session."""
        from botocore.exceptions import ClientError

        mock_manager = Mock(spec=SparkSessionManager)
        mock_project = Mock()
        mock_manager.project = mock_project
        mock_connection = Mock()
        mock_project.connection.return_value = mock_connection
        mock_connection.catalogs = []

        bad_session = Mock()
        error_response = {"Error": {"Code": error_code, "Message": f"Glue error: {error_code}"}}
        type(bad_session).version = PropertyMock(
            side_effect=ClientError(error_response, "GetSessionEndpoint")
        )

        good_session = Mock()
        good_session.version = "3.0.0"
        good_session.sql = Mock(return_value="result")

        mock_manager.create.side_effect = [bad_session, good_session]

        lazy_session = LazySparkSession(mock_manager)

        result = lazy_session.sql
        assert result is good_session.sql
        assert mock_manager.create.call_count == 2
        mock_manager.stop.assert_called_once()

    def test_init_stores_spark_conf(self):
        """Test LazySparkSession stores spark_conf when provided."""
        conf = {"spark.executor.memory": "4g"}
        lazy_session = LazySparkSession(None, connection_name="conn", config="cfg", spark_conf=conf)

        assert lazy_session._spark_conf == conf

    def test_init_spark_conf_defaults_to_none(self):
        """Test LazySparkSession spark_conf defaults to None when not provided."""
        lazy_session = LazySparkSession(None, connection_name="conn", config="cfg")

        assert lazy_session._spark_conf is None

    @patch(
        "sagemaker_studio.utils.spark.session.lazy_spark_session.SparkConnectGrpcException",
        MockSparkConnectGrpcException,
    )
    def test_get_spark_deferred_resolution_passes_spark_conf(self):
        """Test _get_spark passes spark_conf to _resolve_connection_and_create_session_manager."""
        mock_manager = Mock(spec=SparkSessionManager)
        mock_spark = Mock()
        mock_manager.create.return_value = mock_spark
        mock_manager.get_session_id.return_value = "sess-1"
        mock_project = Mock()
        mock_manager.project = mock_project
        mock_connection = Mock()
        mock_project.connection.return_value = mock_connection
        mock_connection.catalogs = []

        user_conf = {"spark.sql.catalog.spark_catalog.warehouse": "s3://bucket/warehouse"}
        lazy_session = LazySparkSession(
            None, connection_name="my-conn", config="cfg", spark_conf=user_conf
        )

        with patch(
            "sagemaker_studio.utils.spark.session.lazy_spark_session._resolve_connection_and_create_session_manager",
            return_value=mock_manager,
        ) as mock_resolve:
            lazy_session._get_spark()

        mock_resolve.assert_called_once_with(
            connection_name="my-conn", config="cfg", spark_conf=user_conf
        )

    @patch(
        "sagemaker_studio.utils.spark.session.lazy_spark_session.SparkConnectGrpcException",
        MockSparkConnectGrpcException,
    )
    def test_getattr_raises_after_max_reconnect_attempts_grpc(self):
        """Test __getattr__ raises RuntimeError after exceeding max reconnect attempts for gRPC."""
        mock_manager = Mock(spec=SparkSessionManager)
        mock_project = Mock()
        mock_manager.project = mock_project
        mock_connection = Mock()
        mock_project.connection.return_value = mock_connection
        mock_connection.catalogs = []

        # Every session always fails with SparkConnectGrpcException
        bad_session = Mock()
        type(bad_session).version = PropertyMock(side_effect=MockSparkConnectGrpcException)
        mock_manager.create.return_value = bad_session

        lazy_session = LazySparkSession(mock_manager)

        with pytest.raises(RuntimeError, match="reconnection failed after"):
            # Access attribute repeatedly — each call increments reconnect counter
            for _ in range(4):
                lazy_session.sql

    @patch(
        "sagemaker_studio.utils.spark.session.lazy_spark_session.SparkConnectGrpcException",
        MockSparkConnectGrpcException,
    )
    def test_getattr_raises_after_max_reconnect_attempts_athena_stopped(self):
        """Test __getattr__ raises RuntimeError after max attempts for Athena STOPPED."""
        from botocore.exceptions import ClientError

        mock_manager = Mock(spec=SparkSessionManager)
        mock_project = Mock()
        mock_manager.project = mock_project
        mock_connection = Mock()
        mock_project.connection.return_value = mock_connection
        mock_connection.catalogs = []

        bad_session = Mock()
        error_response = {
            "Error": {"Code": "InvalidRequestException", "Message": "Session is in STOPPED state"}
        }
        type(bad_session).version = PropertyMock(
            side_effect=ClientError(error_response, "GetSession")
        )
        mock_manager.create.return_value = bad_session

        lazy_session = LazySparkSession(mock_manager)

        with pytest.raises(RuntimeError, match="reconnection failed after"):
            for _ in range(4):
                lazy_session.sql

    @patch(
        "sagemaker_studio.utils.spark.session.lazy_spark_session.SparkConnectGrpcException",
        MockSparkConnectGrpcException,
    )
    def test_getattr_raises_after_max_reconnect_attempts_emr_resource_not_found(self):
        """Test __getattr__ raises RuntimeError after max attempts for EMR ResourceNotFoundException."""
        from botocore.exceptions import ClientError

        mock_manager = Mock(spec=SparkSessionManager)
        mock_project = Mock()
        mock_manager.project = mock_project
        mock_connection = Mock()
        mock_project.connection.return_value = mock_connection
        mock_connection.catalogs = []

        bad_session = Mock()
        error_response = {
            "Error": {"Code": "ResourceNotFoundException", "Message": "Session not found"}
        }
        type(bad_session).version = PropertyMock(
            side_effect=ClientError(error_response, "GetSession")
        )
        mock_manager.create.return_value = bad_session

        lazy_session = LazySparkSession(mock_manager)

        with pytest.raises(RuntimeError, match="reconnection failed after"):
            for _ in range(4):
                lazy_session.sql

    @patch(
        "sagemaker_studio.utils.spark.session.lazy_spark_session.SparkConnectGrpcException",
        MockSparkConnectGrpcException,
    )
    def test_getattr_raises_after_max_reconnect_attempts_glue(self):
        """Test __getattr__ raises RuntimeError after max attempts for Glue EntityNotFoundException."""
        from botocore.exceptions import ClientError

        mock_manager = Mock(spec=SparkSessionManager)
        mock_project = Mock()
        mock_manager.project = mock_project
        mock_connection = Mock()
        mock_project.connection.return_value = mock_connection
        mock_connection.catalogs = []

        bad_session = Mock()
        error_response = {
            "Error": {"Code": "EntityNotFoundException", "Message": "Session not found"}
        }
        type(bad_session).version = PropertyMock(
            side_effect=ClientError(error_response, "GetSession")
        )
        mock_manager.create.return_value = bad_session

        lazy_session = LazySparkSession(mock_manager)

        with pytest.raises(RuntimeError, match="reconnection failed after"):
            for _ in range(4):
                lazy_session.sql

    @patch(
        "sagemaker_studio.utils.spark.session.lazy_spark_session.SparkConnectGrpcException",
        MockSparkConnectGrpcException,
    )
    def test_getattr_resets_reconnect_counter_on_next_successful_call(self):
        """Test reconnect counter resets on the next successful __getattr__ call."""
        mock_manager = Mock(spec=SparkSessionManager)
        mock_project = Mock()
        mock_manager.project = mock_project
        mock_connection = Mock()
        mock_project.connection.return_value = mock_connection
        mock_connection.catalogs = []

        # First access: bad session → stop → _get_spark returns good session for fall-through
        bad_session = Mock()
        type(bad_session).version = PropertyMock(side_effect=MockSparkConnectGrpcException)

        good_session = Mock()
        good_session.version = "3.0.0"
        good_session.sql = Mock(return_value="result")

        mock_manager.create.side_effect = [bad_session, good_session]

        lazy_session = LazySparkSession(mock_manager)
        # First call: bad → stop → good (counter=1 after exception, not reset in fall-through)
        lazy_session.sql
        assert lazy_session._reconnect_attempts == 1

        # Second call: good session still cached, version succeeds → counter resets to 0
        result = lazy_session.sql
        assert result is good_session.sql
        assert lazy_session._reconnect_attempts == 0


class TestResolveEnginePythonVersion:
    """Unit coverage for the engine -> worker-Python resolution (#1).

    The static Glue-major table and the engine-label convenience map used to
    live on ``LazySparkSession`` and were tested here directly. Both now live
    in ``sagemaker_studio.utils.udf.runtime`` (see
    that module's resolution-order coverage:
    ``test_override_wins_and_costs_nothing``,
    ``test_connection_metadata_is_preferred_over_conf_and_probe``,
    ``test_server_conf_path_is_used_when_metadata_is_absent``,
    ``test_completely_unknown_engine_degrades_to_the_client_version``, etc.).
    ``LazySparkSession``'s own responsibility -- delegating to that resolver
    and keeping the session registered/unregistered -- is covered by the
    module-level tests below (``test_session_is_registered_...``,
    ``test_stop_unregisters_...``,
    ``test_resolve_engine_python_version_delegates_...``,
    ``test_the_static_glue_map_is_no_longer_consulted_first``).
    """

    def test_udf_shadowing_methods_removed(self):
        """The old spark.udf / spark.pandas_udf method shadowing is gone, so the
        native SparkSession.udf property contract is preserved (#2a)."""
        # LazySparkSession no longer defines udf/pandas_udf as class methods.
        assert "udf" not in LazySparkSession.__dict__
        assert "pandas_udf" not in LazySparkSession.__dict__


def test_session_is_registered_with_the_udf_resolver_on_creation():
    from sagemaker_studio.utils.spark.session.lazy_spark_session import LazySparkSession
    from sagemaker_studio.utils.udf import runtime as rt

    rt.clear_cache()
    manager = Mock()
    manager.project.connection.return_value.catalogs = []
    inner = Mock()
    inner._client = object()
    manager.create.return_value = inner

    lazy = LazySparkSession(session_manager=manager)
    lazy._get_spark()

    assert _udf_registered_session(rt, inner._client) is inner


def test_stop_unregisters_the_session_from_the_udf_resolver():
    from sagemaker_studio.utils.spark.session.lazy_spark_session import LazySparkSession
    from sagemaker_studio.utils.udf import runtime as rt

    rt.clear_cache()
    manager = Mock()
    manager.project.connection.return_value.catalogs = []
    inner = Mock()
    inner._client = object()
    manager.create.return_value = inner

    lazy = LazySparkSession(session_manager=manager)
    lazy._get_spark()
    lazy.stop()

    assert _udf_registered_session(rt, inner._client) is None


def test_resolve_engine_python_version_delegates_to_the_runtime_resolver():
    from sagemaker_studio.utils.spark.session.lazy_spark_session import LazySparkSession
    from sagemaker_studio.utils.udf import runtime as rt

    rt.clear_cache()
    manager = Mock()
    manager.project.connection.return_value.catalogs = []
    inner = Mock()
    inner._client = object()
    manager.create.return_value = inner

    lazy = LazySparkSession(session_manager=manager)
    lazy.set_engine_python_version_override("3.13")
    assert lazy.resolve_engine_python_version() == "3.13"
    assert lazy.resolve_worker_runtime().source == "override"


def test_the_static_glue_map_is_no_longer_consulted_first():
    # Regression guard for the handoff's Priority 2: a Glue-6 manager whose
    # runtime signals say 3.11 must resolve to 3.11, not to the map's 3.13.
    from sagemaker_studio.utils.spark.session.lazy_spark_session import LazySparkSession
    from sagemaker_studio.utils.udf import runtime as rt

    rt.clear_cache()
    manager = Mock()
    manager.project.connection.return_value.catalogs = []
    manager.get_glue_version.return_value = "6.0"
    manager.get_connection_python_version.return_value = "3.11"
    inner = Mock()
    inner._client = object()
    manager.create.return_value = inner

    lazy = LazySparkSession(session_manager=manager)
    lazy._get_spark()
    runtime = lazy.resolve_worker_runtime()
    assert runtime.python_version == "3.11"
    assert runtime.source == "connection-metadata"


def _udf_registered_session(rt, client):
    """The session the UDF resolver has registered for ``client``, or ``None``.

    Test-only surface, so it lives here rather than in the resolver, which has no
    production caller for it.
    """
    context = rt._context_get(client)
    return None if context is None else context.session
