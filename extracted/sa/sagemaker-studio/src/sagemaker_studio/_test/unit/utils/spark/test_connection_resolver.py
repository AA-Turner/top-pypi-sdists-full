"""Tests for connection_resolver module."""

import sys
from unittest.mock import ANY, MagicMock, Mock, patch

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
        "sagemaker_studio.utils.spark.session.glue.interceptors",
    ]:
        mock_interceptors = Mock()
        mock_interceptors.CustomChannelBuilder = Mock()
        sys.modules[interceptor_path] = mock_interceptors

    from sagemaker_studio.utils.spark.connection_resolver import (
        _create_session_manager,
        _identify_service_from_props,
        _resolve_connection_and_create_session_manager,
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


def test_create_session_manager_glue():
    """Ensure Glue session manager is created for GLUE service with SPARK_CONNECT or SPARK type."""
    from sagemaker_studio.utils.spark.session.glue.glue_spark_session_manager import (
        GlueSparkSessionManager,
    )

    # SPARK_CONNECT type
    conn = _make_connection({"sparkGlueProperties": {"glueVersion": "5.1"}})
    conn.type = "SPARK_CONNECT"
    mgr = _create_session_manager(conn, "my-conn", None, MagicMock())
    assert isinstance(mgr, GlueSparkSessionManager)
    assert mgr._connection is conn
    assert mgr.connection_name == "my-conn"

    # SPARK type (DZ creates Glue connections with type=SPARK)
    conn2 = _make_connection({"sparkGlueProperties": {"glueVersion": "5.0"}})
    conn2.type = "SPARK"
    mgr2 = _create_session_manager(conn2, "glue-conn", None, MagicMock())
    assert isinstance(mgr2, GlueSparkSessionManager)
    assert mgr2._connection is conn2


def test_create_session_manager_emr_eks_raises():
    """Ensure RuntimeError is raised for EMR_EKS connections."""
    conn = _make_connection(
        {"sparkEmrProperties": {"computeArn": "arn:aws:emr-containers:us-west-2:123:/vc/vc-1"}}
    )
    conn.type = "SPARK_CONNECT"

    with pytest.raises(RuntimeError, match="not yet supported for EMR_EKS"):
        _create_session_manager(conn, "my-conn", None, MagicMock())


def test_create_session_manager_emr_ec2(monkeypatch):
    """Ensure EMR on EC2 session manager is created for EMR_EC2 service."""
    conn = _make_connection(
        {"sparkEmrProperties": {"computeArn": "arn:aws:elasticmapreduce:us-west-2:123:cluster/j-1"}}
    )
    conn.type = "SPARK_CONNECT"

    # Mock the EMR EC2 interceptors module
    mock_emr_ec2_interceptors = Mock()
    mock_emr_ec2_interceptors.EmrEc2ChannelBuilder = Mock()
    monkeypatch.setitem(
        sys.modules,
        "sagemaker_studio.utils.spark.session.emr_ec2.interceptors",
        mock_emr_ec2_interceptors,
    )

    from sagemaker_studio.utils.spark.session.emr_ec2.emr_ec2_spark_session_manager import (
        EmrEc2SparkSessionManager,
    )

    mgr = _create_session_manager(conn, "my-conn", None, MagicMock())
    assert isinstance(mgr, EmrEc2SparkSessionManager)


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


def test_create_session_manager_unhandled_service_defaults_to_athena():
    """Ensure unhandled service types default to Athena session manager for SPARK_CONNECT."""
    conn = _make_connection({"athenaProperties": {"workgroupName": "wg-1"}})
    conn.type = "SPARK_CONNECT"

    with patch(
        "sagemaker_studio.utils.spark.connection_resolver._identify_service_from_props",
        return_value="NEW_SERVICE",
    ):
        mgr = _create_session_manager(conn, "my-conn", None, MagicMock())

    from sagemaker_studio.utils.spark.session.athena.athena_spark_session_manager import (
        AthenaSparkSessionManager,
    )

    assert isinstance(mgr, AthenaSparkSessionManager)


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


def test_create_session_manager_spark_type_with_emr_serverless_explicit_raises():
    """Ensure RuntimeError when type=SPARK is used with EMR Serverless (only Glue uses SPARK type)."""
    conn = _make_connection(
        {
            "sparkEmrProperties": {
                "computeArn": "arn:aws:emr-serverless:us-west-2:123:/applications/app-1"
            }
        }
    )
    conn.type = "SPARK"

    with pytest.raises(RuntimeError, match="only supported for Glue connections"):
        _create_session_manager(conn, "emr-conn", None, MagicMock(), is_explicit_choice=True)


def test_create_session_manager_spark_type_with_athena_explicit_raises():
    """Ensure RuntimeError when type=SPARK is used with Athena (only Glue uses SPARK type)."""
    conn = _make_connection({"athenaProperties": {"workgroupName": "wg-1"}})
    conn.type = "SPARK"

    with pytest.raises(RuntimeError, match="only supported for Glue connections"):
        _create_session_manager(conn, "athena-conn", None, MagicMock(), is_explicit_choice=True)


def test_create_session_manager_spark_type_with_glue_succeeds():
    """Ensure type=SPARK with sparkGlueProperties routes to GlueSparkSessionManager."""
    from sagemaker_studio.utils.spark.session.glue.glue_spark_session_manager import (
        GlueSparkSessionManager,
    )

    conn = _make_connection({"sparkGlueProperties": {"glueVersion": "5.1"}})
    conn.type = "SPARK"

    mgr = _create_session_manager(conn, "glue-conn", None, MagicMock())
    assert isinstance(mgr, GlueSparkSessionManager)


def test_create_session_manager_spark_type_with_non_glue_default_falls_back_to_athena():
    """Ensure type=SPARK with non-Glue service falls back to Athena on default path (not explicit)."""
    from sagemaker_studio.utils.spark.session.athena.athena_spark_session_manager import (
        AthenaSparkSessionManager,
    )

    conn = _make_connection(
        {
            "sparkEmrProperties": {
                "computeArn": "arn:aws:emr-serverless:us-west-2:123:/applications/app-1"
            }
        }
    )
    conn.type = "SPARK"

    mgr = _create_session_manager(conn, None, None, MagicMock(), is_explicit_choice=False)
    assert isinstance(mgr, AthenaSparkSessionManager)


# ---------------------------------------------------------------------------
# _resolve_connection_and_create_session_manager tests
# ---------------------------------------------------------------------------


@patch("sagemaker_studio.utils.spark.connection_resolver._create_session_manager")
@patch("sagemaker_studio.utils.spark.connection_resolver._ensure_project")
@patch("sagemaker_studio.utils.spark.connection_resolver._resolve_connection_id_from_notebook")
def test_resolve_with_explicit_connection_name(mock_notebook, mock_project, mock_create):
    """Ensure explicit connection_name resolves via project.connection(name) with is_explicit_choice=True."""
    mock_conn = MagicMock()
    mock_project.return_value.connection.return_value = mock_conn
    mock_create.return_value = "manager"

    result = _resolve_connection_and_create_session_manager(connection_name="my-conn")

    mock_project.return_value.connection.assert_called_once_with("my-conn")
    mock_create.assert_called_once_with(mock_conn, "my-conn", None, ANY, True, spark_conf=None)
    assert result == "manager"
    mock_notebook.assert_not_called()


@patch("sagemaker_studio.utils.spark.connection_resolver._create_session_manager")
@patch("sagemaker_studio.utils.spark.connection_resolver._ensure_project")
@patch("sagemaker_studio.utils.spark.connection_resolver._resolve_connection_id_from_notebook")
def test_resolve_with_notebook_metadata_connection_id(mock_notebook, mock_project, mock_create):
    """Ensure notebook metadata connection ID resolves via project.connection(id=...) with is_explicit_choice=True."""
    mock_notebook.return_value = "conn-id-from-notebook"
    mock_conn = MagicMock()
    mock_project.return_value.connection.return_value = mock_conn
    mock_create.return_value = "manager"

    result = _resolve_connection_and_create_session_manager()

    mock_project.return_value.connection.assert_called_once_with(id="conn-id-from-notebook")
    mock_create.assert_called_once_with(
        mock_conn, None, "conn-id-from-notebook", ANY, True, spark_conf=None
    )
    assert result == "manager"


@patch("sagemaker_studio.utils.spark.connection_resolver._create_session_manager")
@patch("sagemaker_studio.utils.spark.connection_resolver._ensure_project")
@patch("sagemaker_studio.utils.spark.connection_resolver._resolve_connection_id_from_notebook")
def test_resolve_default_spark_connect_connection(mock_notebook, mock_project, mock_create):
    """Ensure default path resolves via project.connection(type='SPARK_CONNECT') with is_explicit_choice=False."""
    mock_notebook.return_value = None
    mock_conn = MagicMock()
    mock_project.return_value.connection.return_value = mock_conn
    mock_create.return_value = "manager"

    result = _resolve_connection_and_create_session_manager()

    mock_project.return_value.connection.assert_called_once_with(type="SPARK_CONNECT")
    mock_create.assert_called_once_with(mock_conn, None, None, ANY, False, spark_conf=None)
    assert result == "manager"


@patch("sagemaker_studio.utils.spark.connection_resolver._create_session_manager")
@patch("sagemaker_studio.utils.spark.connection_resolver._ensure_project")
@patch("sagemaker_studio.utils.spark.connection_resolver._resolve_connection_id_from_notebook")
def test_resolve_falls_back_to_default_when_notebook_lookup_fails(
    mock_notebook, mock_project, mock_create
):
    """Ensure notebook metadata lookup failure falls back to default SPARK_CONNECT with is_explicit_choice=False."""
    mock_notebook.side_effect = Exception("notebook API error")
    mock_conn = MagicMock()
    mock_project.return_value.connection.return_value = mock_conn
    mock_create.return_value = "manager"

    result = _resolve_connection_and_create_session_manager()

    mock_project.return_value.connection.assert_called_once_with(type="SPARK_CONNECT")
    mock_create.assert_called_once_with(mock_conn, None, None, ANY, False, spark_conf=None)
    assert result == "manager"


# ---------------------------------------------------------------------------
# spark_conf passthrough tests
# ---------------------------------------------------------------------------


@patch("sagemaker_studio.utils.spark.connection_resolver._create_session_manager")
@patch("sagemaker_studio.utils.spark.connection_resolver._ensure_project")
@patch("sagemaker_studio.utils.spark.connection_resolver._resolve_connection_id_from_notebook")
def test_resolve_passes_spark_conf_to_create_session_manager(
    mock_notebook, mock_project, mock_create
):
    """Ensure spark_conf is passed through to _create_session_manager."""
    mock_conn = MagicMock()
    mock_project.return_value.connection.return_value = mock_conn
    mock_create.return_value = "manager"
    user_conf = {"spark.sql.catalog.spark_catalog.warehouse": "s3://bucket/wh"}

    result = _resolve_connection_and_create_session_manager(
        connection_name="my-conn", spark_conf=user_conf
    )

    mock_create.assert_called_once_with(mock_conn, "my-conn", None, ANY, True, spark_conf=user_conf)
    assert result == "manager"


def test_create_session_manager_glue_receives_spark_conf():
    """Ensure spark_conf is passed to GlueSparkSessionManager."""
    from sagemaker_studio.utils.spark.session.glue.glue_spark_session_manager import (
        GlueSparkSessionManager,
    )

    conn = _make_connection({"sparkGlueProperties": {"glueVersion": "5.1"}})
    conn.type = "SPARK_CONNECT"
    user_conf = {"spark.sql.catalog.spark_catalog.warehouse": "s3://bucket/wh"}

    mgr = _create_session_manager(conn, "my-conn", None, MagicMock(), spark_conf=user_conf)
    assert isinstance(mgr, GlueSparkSessionManager)
    assert mgr.spark_conf == user_conf


def test_create_session_manager_emr_serverless_receives_spark_conf():
    """Ensure spark_conf is passed to EMRServerlessSparkSessionManager."""
    from sagemaker_studio.utils.spark.session.emr_serverless.emr_serverless_spark_session_manager import (
        EMRServerlessSparkSessionManager,
    )

    conn = _make_connection(
        {
            "sparkEmrProperties": {
                "computeArn": "arn:aws:emr-serverless:us-west-2:123:/applications/app-1"
            }
        }
    )
    conn.type = "SPARK_CONNECT"
    user_conf = {"spark.executor.memory": "4g"}

    mgr = _create_session_manager(conn, "my-conn", None, MagicMock(), spark_conf=user_conf)
    assert isinstance(mgr, EMRServerlessSparkSessionManager)
    assert mgr._user_spark_conf == user_conf


def test_create_session_manager_athena_receives_spark_conf():
    """Ensure spark_conf is passed to AthenaSparkSessionManager."""
    from sagemaker_studio.utils.spark.session.athena.athena_spark_session_manager import (
        AthenaSparkSessionManager,
    )

    conn = _make_connection({"athenaProperties": {"workgroupName": "wg-1"}})
    conn.type = "SPARK_CONNECT"
    user_conf = {"spark.sql.catalogImplementation": "in-memory"}

    mgr = _create_session_manager(conn, "my-conn", "conn-id", MagicMock(), spark_conf=user_conf)
    assert isinstance(mgr, AthenaSparkSessionManager)
    assert mgr._user_spark_conf == user_conf
