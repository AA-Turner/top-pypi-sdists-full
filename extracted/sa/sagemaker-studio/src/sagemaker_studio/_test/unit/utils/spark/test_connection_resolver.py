"""Tests for connection_resolver module."""

import sys
from unittest.mock import MagicMock, Mock, patch

import pytest

# Mock Project class before any imports to prevent Domain ID error
with patch("sagemaker_studio.Project"):

    sys.modules["pyspark"] = Mock()
    sys.modules["pyspark.sql"] = Mock()
    sys.modules["pyspark.sql.connect"] = Mock()
    sys.modules["pyspark.sql.connect.session"] = Mock()
    sys.modules["pyspark.sql.connect.client"] = Mock()
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
        "grpc",
        "pyspark.errors",
        "pyspark.errors.exceptions",
        "pyspark.errors.exceptions.connect",
    ]

    for module_name in pyspark_modules:
        if module_name not in sys.modules:
            mock_module = Mock()
            if module_name == "grpc":
                mock_module.insecure_channel = Mock()
                mock_module.secure_channel = Mock()
                mock_module.intercept_channel = Mock()
                mock_module.UnaryUnaryClientInterceptor = Mock()
                mock_module.UnaryStreamClientInterceptor = Mock()
                mock_module.StreamUnaryClientInterceptor = Mock()
                mock_module.StreamStreamClientInterceptor = Mock()
                mock_module.ClientCallDetails = Mock()
            elif module_name == "pyspark.sql.connect.client":
                mock_module.ChannelBuilder = Mock()
            sys.modules[module_name] = mock_module

    # Mock interceptors modules
    for interceptor_path in [
        "sagemaker_studio.utils.spark.session.athena.interceptors",
        "sagemaker_studio.utils.spark.session.emr_serverless.interceptors",
    ]:
        mock_interceptors = Mock()
        mock_interceptors.CustomChannelBuilder = Mock()
        sys.modules[interceptor_path] = mock_interceptors

    from sagemaker_studio.utils.spark.connection_resolver import (
        _create_session_manager,
        _identify_service_from_props,
    )


# ---------------------------------------------------------------------------
# _identify_service_from_props tests
# ---------------------------------------------------------------------------


def _make_connection(props=None):
    """Helper to create a mock connection with given props."""
    conn = MagicMock()
    conn._Connection__connection_data = {"props": props or {}}
    return conn


def test_identify_emr_serverless():
    """Ensure EMR_SERVERLESS is returned for emr-serverless computeArn."""
    conn = _make_connection(
        {
            "sparkEmrProperties": {
                "computeArn": "arn:aws:emr-serverless:us-west-2:123:/applications/app-1"
            }
        }
    )
    assert _identify_service_from_props(conn) == "EMR_SERVERLESS"


def test_identify_emr_eks():
    """Ensure EMR_EKS is returned for emr-containers computeArn."""
    conn = _make_connection(
        {
            "sparkEmrProperties": {
                "computeArn": "arn:aws:emr-containers:us-west-2:123:/virtualclusters/vc-1"
            }
        }
    )
    assert _identify_service_from_props(conn) == "EMR_EKS"


def test_identify_emr_ec2():
    """Ensure EMR_EC2 is returned for elasticmapreduce computeArn."""
    conn = _make_connection(
        {"sparkEmrProperties": {"computeArn": "arn:aws:elasticmapreduce:us-west-2:123:cluster/j-1"}}
    )
    assert _identify_service_from_props(conn) == "EMR_EC2"


def test_identify_unknown_compute_arn():
    """Ensure UNKNOWN is returned for unrecognized computeArn pattern."""
    conn = _make_connection(
        {"sparkEmrProperties": {"computeArn": "arn:aws:some-other-service:us-west-2:123:resource"}}
    )
    assert _identify_service_from_props(conn) == "UNKNOWN"


def test_identify_glue():
    """Ensure GLUE is returned when sparkGlueProperties exists."""
    conn = _make_connection({"sparkGlueProperties": {"someKey": "someValue"}})
    assert _identify_service_from_props(conn) == "GLUE"


def test_identify_athena():
    """Ensure ATHENA is returned when athenaProperties exists."""
    conn = _make_connection({"athenaProperties": {"workgroupName": "wg-1"}})
    assert _identify_service_from_props(conn) == "ATHENA"


def test_identify_no_recognized_props_returns_unknown():
    """Ensure UNKNOWN is returned when no recognized props exist (not ATHENA)."""
    conn = _make_connection({})
    assert _identify_service_from_props(conn) == "UNKNOWN"


def test_identify_empty_connection_data_returns_unknown():
    """Ensure UNKNOWN is returned when connection data is empty."""
    conn = MagicMock()
    conn._Connection__connection_data = {}
    assert _identify_service_from_props(conn) == "UNKNOWN"


def test_identify_exception_returns_unknown():
    """Ensure UNKNOWN is returned when an exception occurs during identification."""
    conn = MagicMock()
    # Force an exception by making __connection_data a non-dict that raises on .get()
    type(conn)._Connection__connection_data = property(
        lambda self: (_ for _ in ()).throw(RuntimeError("boom"))
    )
    assert _identify_service_from_props(conn) == "UNKNOWN"


# ---------------------------------------------------------------------------
# _create_session_manager tests
# ---------------------------------------------------------------------------


def test_create_session_manager_athena():
    """Ensure Athena session manager is created for ATHENA service with connection passed through."""
    conn = _make_connection({"athenaProperties": {"workgroupName": "wg-1"}})
    conn.type = "SPARK_CONNECT"

    mgr = _create_session_manager(conn, "my-conn", "conn-id-1", MagicMock())
    from sagemaker_studio.utils.spark.session.athena.athena_spark_session_manager import (
        AthenaSparkSessionManager,
    )

    assert isinstance(mgr, AthenaSparkSessionManager)
    # Verify pre-resolved connection is passed to avoid redundant API call
    assert mgr._connection is conn
    assert mgr.connection_name == "my-conn"
    assert mgr.connection_id == "conn-id-1"


def test_create_session_manager_emr_serverless():
    """Ensure EMR Serverless session manager is created for EMR_SERVERLESS service."""
    conn = _make_connection(
        {
            "sparkEmrProperties": {
                "computeArn": "arn:aws:emr-serverless:us-west-2:123:/applications/app-1"
            }
        }
    )
    conn.type = "SPARK_CONNECT"

    from sagemaker_studio.utils.spark.session.emr_serverless.emr_serverless_spark_session_manager import (
        EMRServerlessSparkSessionManager,
    )

    mgr = _create_session_manager(conn, "my-conn", None, MagicMock())
    assert isinstance(mgr, EMRServerlessSparkSessionManager)


def test_create_session_manager_glue_raises():
    """Ensure RuntimeError is raised for GLUE connections."""
    conn = _make_connection({"sparkGlueProperties": {"someKey": "val"}})
    conn.type = "SPARK_CONNECT"

    with pytest.raises(RuntimeError, match="not yet supported for GLUE"):
        _create_session_manager(conn, "my-conn", None, MagicMock())


def test_create_session_manager_emr_eks_raises():
    """Ensure RuntimeError is raised for EMR_EKS connections."""
    conn = _make_connection(
        {"sparkEmrProperties": {"computeArn": "arn:aws:emr-containers:us-west-2:123:/vc/vc-1"}}
    )
    conn.type = "SPARK_CONNECT"

    with pytest.raises(RuntimeError, match="not yet supported for EMR_EKS"):
        _create_session_manager(conn, "my-conn", None, MagicMock())


def test_create_session_manager_emr_ec2_raises():
    """Ensure RuntimeError is raised for EMR_EC2 connections."""
    conn = _make_connection(
        {"sparkEmrProperties": {"computeArn": "arn:aws:elasticmapreduce:us-west-2:123:cluster/j-1"}}
    )
    conn.type = "SPARK_CONNECT"

    with pytest.raises(RuntimeError, match="not yet supported for EMR_EC2"):
        _create_session_manager(conn, "my-conn", None, MagicMock())


def test_create_session_manager_unknown_props_raises():
    """Ensure RuntimeError is raised when no recognized props exist on SPARK_CONNECT."""
    conn = _make_connection({})
    conn.type = "SPARK_CONNECT"

    with pytest.raises(RuntimeError, match="Could not identify the Spark backend"):
        _create_session_manager(conn, "my-conn", None, MagicMock())


def test_create_session_manager_unrecognized_compute_arn_raises():
    """Ensure RuntimeError is raised for unrecognized computeArn patterns."""
    conn = _make_connection(
        {"sparkEmrProperties": {"computeArn": "arn:aws:mystery:us-west-2:123:thing"}}
    )
    conn.type = "SPARK_CONNECT"

    with pytest.raises(RuntimeError, match="Could not identify the Spark backend"):
        _create_session_manager(conn, "my-conn", None, MagicMock())


def test_create_session_manager_unhandled_service_raises():
    """Ensure RuntimeError is raised for a service type returned by _identify_service_from_props that is not explicitly handled."""
    conn = _make_connection({"athenaProperties": {"workgroupName": "wg-1"}})
    conn.type = "SPARK_CONNECT"

    with patch(
        "sagemaker_studio.utils.spark.connection_resolver._identify_service_from_props",
        return_value="NEW_SERVICE",
    ):
        with pytest.raises(RuntimeError, match="Unhandled Spark Connect service type: NEW_SERVICE"):
            _create_session_manager(conn, "my-conn", None, MagicMock())


def test_create_session_manager_non_spark_connect_explicit_raises():
    """Ensure RuntimeError is raised for non-SPARK_CONNECT type when explicitly chosen."""
    conn = _make_connection({})
    conn.type = "JDBC"

    with pytest.raises(RuntimeError, match="not a recognized Spark Connect type"):
        _create_session_manager(conn, "my-conn", None, MagicMock(), is_explicit_choice=True)


def test_create_session_manager_non_spark_connect_default_falls_back():
    """Ensure Athena fallback for non-SPARK_CONNECT type on default path (with warning)."""
    conn = _make_connection({})
    conn.type = "JDBC"

    import warnings

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        mgr = _create_session_manager(conn, None, None, MagicMock(), is_explicit_choice=False)

    from sagemaker_studio.utils.spark.session.athena.athena_spark_session_manager import (
        AthenaSparkSessionManager,
    )

    assert isinstance(mgr, AthenaSparkSessionManager)
    assert len(w) == 1
    assert "not a recognized Spark Connect type" in str(w[0].message)
