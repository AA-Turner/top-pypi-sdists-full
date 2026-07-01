"""Tests for GlueSparkSessionManager."""

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

    # Mock the interceptors module
    mock_interceptors = Mock()
    mock_interceptors.CustomChannelBuilder = Mock()
    sys.modules["sagemaker_studio.utils.spark.session.glue.interceptors"] = mock_interceptors

    from sagemaker_studio.project import ClientConfig
    from sagemaker_studio.utils.spark.session.glue.glue_spark_session_manager import (
        GlueSparkSessionManager,
    )


@pytest.fixture
def mock_glue_connection():
    """Create a mock Glue connection with sparkGlueProperties."""
    conn = MagicMock()
    conn._Connection__connection_data = {
        "props": {
            "sparkGlueProperties": {
                "glueVersion": "5.0",
                "idleTimeout": 60,
                "numberOfWorkers": 10,
                "workerType": "G.1X",
                "glueConnectionName": "my-glue-network-conn",
            }
        },
        "configurations": [
            {
                "classification": "GlueDefaultArgument",
                "properties": {"--enable-lakeformation-fine-grained-access": "true"},
            },
            {
                "classification": "SparkConfiguration",
                "properties": {"spark.custom.key": "custom-value"},
            },
        ],
        "physicalEndpoints": [
            {
                "awsLocation": {"awsAccountId": "123456789012", "awsRegion": "us-east-2"},
                "glueConnectionNames": ["conn-a", "conn-b"],
            }
        ],
    }
    conn.name = "default.spark"
    conn.type = "SPARK"
    return conn


@pytest.fixture
def mock_internal_utils():
    """Mock InternalUtils and _ensure_project for Glue session manager."""
    with patch(
        "sagemaker_studio.utils.spark.session.glue.glue_spark_session_manager.InternalUtils"
    ) as mock_utils, patch(
        "sagemaker_studio.utils.spark.session.glue.glue_spark_session_manager._ensure_project"
    ) as mock_ensure_project, patch(
        "sagemaker_studio.utils.spark.session.spark_config_builder._ensure_project"
    ), patch(
        "sagemaker_studio.utils.spark.session.spark_config_builder._generate_s3tables_spark_configs",
        return_value={},
    ), patch(
        "sagemaker_studio.utils.spark.session.spark_config_builder._generate_glue_catalog_spark_configs",
        return_value={},
    ), patch(
        "sagemaker_studio.utils.spark.session.spark_config_builder._generate_workday_irc_spark_configs",
        return_value={},
    ):
        mock_utils.return_value._get_domain_region.return_value = "us-east-2"
        mock_utils.return_value._get_account_id.return_value = "123456789012"
        mock_utils.return_value._get_user_id.return_value = "test-user"
        mock_utils.return_value._get_domain_id.return_value = "dzd-abc123"
        mock_utils.return_value._get_field_from_environment.side_effect = lambda key: {
            "ProjectS3Path": "s3://project-bucket/path",
            "SpaceName": "test-space",
            "ExecutionRoleArn": "arn:aws:iam::123456789012:role/fallback-role",
        }.get(key)
        mock_project = MagicMock()
        mock_project.iam_role = "arn:aws:iam::123456789012:role/test-role"
        mock_project.id = "proj-123"
        mock_project.user_id = "test-user"
        mock_project.domain_id = "dzd-abc123"
        mock_project.s3 = MagicMock()
        mock_project.s3.root = "s3://project-bucket/path"
        mock_project._sagemaker_studio_api = MagicMock()
        mock_ensure_project.return_value = mock_project
        yield mock_utils, mock_ensure_project


@pytest.fixture
def manager(mock_glue_connection):
    """Create a testable GlueSparkSessionManager."""
    return GlueSparkSessionManager(connection_name="default.spark", connection=mock_glue_connection)


# ---------------------------------------------------------------------------
# Initialization and lazy_init tests
# ---------------------------------------------------------------------------


@patch("boto3.client")
@patch("boto3.Session")
def test_lazy_init_extracts_connection_props(
    mock_session_cls, mock_boto_client, manager, mock_internal_utils
):
    """Ensure _lazy_init extracts glue props, configs, connection names, and forces compatibility mode."""
    mock_glue_client = MagicMock()
    mock_session_cls.return_value.client.return_value = mock_glue_client

    manager._lazy_init()

    # Glue props extracted
    assert manager._glue_props["glueVersion"] == "5.0"
    assert manager._glue_props["numberOfWorkers"] == 10
    assert manager._glue_props["workerType"] == "G.1X"
    # Connection-level configs extracted
    assert manager._connection_spark_configs == {"spark.custom.key": "custom-value"}
    assert manager._connection_default_arguments == {
        "--enable-lakeformation-fine-grained-access": "true"
    }
    # Multi-subnet failover: glueConnectionNames from physicalEndpoints[0]
    assert manager._glue_connection_names == ["conn-a", "conn-b"]
    # FGAC forced off for Spark Connect (regardless of connection setting)
    assert manager._is_compatibility_mode is True


@patch("boto3.client")
@patch("boto3.Session")
def test_lazy_init_glue_connection_name_fallback(
    mock_session_cls, mock_boto_client, mock_internal_utils
):
    """Ensure _lazy_init falls back to singular glueConnectionName when glueConnectionNames absent."""
    conn = MagicMock()
    conn._Connection__connection_data = {
        "props": {"sparkGlueProperties": {"glueConnectionName": "single-conn"}},
        "configurations": [],
        "physicalEndpoints": [{"awsLocation": {"awsRegion": "us-east-2"}}],
    }
    mock_session_cls.return_value.client.return_value = MagicMock()

    mgr = GlueSparkSessionManager(connection=conn)
    mgr._lazy_init()

    assert mgr._glue_connection_names == ["single-conn"]


# ---------------------------------------------------------------------------
# create() tests
# ---------------------------------------------------------------------------


def test_create_returns_existing_session(manager):
    """Ensure create() returns existing session without re-creating."""
    manager._spark_session = "existing_session"
    assert manager.create() == "existing_session"


@patch("sagemaker_studio.utils.spark.session.glue.glue_spark_session_manager._SparkSession")
@patch("sagemaker_studio.utils.spark.session.glue.glue_spark_session_manager.CustomChannelBuilder")
def test_create_builds_spark_session(mock_channel_builder, mock_spark_session, manager):
    """Ensure create() calls _start_glue_session and builds a SparkSession."""
    manager._lazy_init = MagicMock()
    manager._start_glue_session = MagicMock(
        return_value=(
            "sess-glue-1",
            "sc://endpoint:443/;use_ssl=true",
            {"AuthToken": "tok123", "AuthTokenExpirationTime": 1779314191},
        )
    )

    builder = MagicMock()
    mock_spark_session.builder.channelBuilder.return_value = builder
    builder.appName.return_value = builder
    builder.getOrCreate.return_value = "mock_spark"

    session = manager.create()

    assert session == "mock_spark"
    assert manager.glue_session_id == "sess-glue-1"
    mock_channel_builder.assert_called_once()
    builder.getOrCreate.assert_called_once()


@patch.object(GlueSparkSessionManager, "stop")
def test_create_calls_stop_on_failure(mock_stop, manager):
    """Ensure create() calls stop() to clean up orphaned sessions on failure."""
    manager._lazy_init = MagicMock(side_effect=RuntimeError("init failed"))

    with pytest.raises(RuntimeError, match="init failed"):
        manager.create()

    mock_stop.assert_called_once()


# ---------------------------------------------------------------------------
# stop() tests
# ---------------------------------------------------------------------------


@patch.object(GlueSparkSessionManager, "_stop_glue_session")
def test_stop_order_spark_first_then_glue(mock_stop_glue, manager):
    """Ensure stop() stops Spark session first (graceful gRPC close), then Glue session."""
    mock_spark = MagicMock()
    call_order = []
    mock_spark.stop.side_effect = lambda: call_order.append("spark_stop")
    mock_stop_glue.side_effect = lambda sid: call_order.append("glue_stop")

    manager._spark_session = mock_spark
    manager.glue_session_id = "sess-123"

    manager.stop()

    assert call_order == ["spark_stop", "glue_stop"]
    assert manager._spark_session is None
    assert manager.glue_session_id is None


@patch.object(GlueSparkSessionManager, "_stop_glue_session")
def test_stop_terminates_glue_even_if_spark_stop_fails(mock_stop_glue, manager):
    """Ensure Glue session is stopped even if Spark session stop raises."""
    mock_spark = MagicMock()
    mock_spark.stop.side_effect = Exception("gRPC error")
    manager._spark_session = mock_spark
    manager.glue_session_id = "sess-123"

    manager.stop()

    mock_stop_glue.assert_called_once_with("sess-123")
    assert manager._spark_session is None
    assert manager.glue_session_id is None


# ---------------------------------------------------------------------------
# _start_glue_session tests
# ---------------------------------------------------------------------------


@patch("boto3.client")
@patch("boto3.Session")
def test_start_glue_session_bumps_version_to_5_1(
    mock_session_cls, mock_boto_client, manager, mock_internal_utils
):
    """Ensure _start_glue_session bumps glueVersion < 5.1 to 5.1 and caps idle timeout to 15 min."""
    mock_glue_client = MagicMock()
    mock_session_cls.return_value.client.return_value = mock_glue_client
    mock_glue_client.create_session.return_value = {"Session": {"Id": "sess-1"}}
    mock_glue_client.get_session.return_value = {"Session": {"Status": "READY"}}
    mock_glue_client.get_session_endpoint.return_value = {
        "SparkConnect": {
            "Url": "sc://s-123.sessions.glue.us-east-2.amazonaws.com",
            "AuthToken": "token-abc",
            "AuthTokenExpirationTime": 1779314191,
        }
    }

    manager._lazy_init()
    session_id, url, endpoint = manager._start_glue_session()

    # Verify CreateSession was called with bumped version and capped idle timeout
    create_call = mock_glue_client.create_session.call_args
    assert create_call[1]["GlueVersion"] == "5.1"
    assert create_call[1]["IdleTimeout"] == 15
    assert create_call[1]["SessionType"] == "SPARK_CONNECT"
    assert create_call[1]["RequestOrigin"] == "SageMakerUnifiedStudio_NotebookRun"
    # FGAC forced off
    assert (
        create_call[1]["DefaultArguments"]["--enable-lakeformation-fine-grained-access"] == "false"
    )


@patch("boto3.client")
@patch("boto3.Session")
def test_start_glue_session_honors_version_above_5_1(
    mock_session_cls, mock_boto_client, mock_internal_utils
):
    """Ensure _start_glue_session uses connection version when >= 5.1."""
    conn = MagicMock()
    conn._Connection__connection_data = {
        "props": {"sparkGlueProperties": {"glueVersion": "5.2", "numberOfWorkers": 5}},
        "configurations": [],
        "physicalEndpoints": [],
    }

    mock_glue_client = MagicMock()
    mock_session_cls.return_value.client.return_value = mock_glue_client
    mock_glue_client.create_session.return_value = {"Session": {"Id": "sess-2"}}
    mock_glue_client.get_session.return_value = {"Session": {"Status": "READY"}}
    mock_glue_client.get_session_endpoint.return_value = {
        "SparkConnect": {
            "Url": "sc://endpoint",
            "AuthToken": "tok",
            "AuthTokenExpirationTime": 1779314191,
        }
    }

    mgr = GlueSparkSessionManager(connection=conn)
    mgr._lazy_init()
    mgr._start_glue_session()

    create_call = mock_glue_client.create_session.call_args
    assert create_call[1]["GlueVersion"] == "5.2"


@patch("boto3.client")
@patch("boto3.Session")
def test_start_glue_session_passes_connections_and_tags(
    mock_session_cls, mock_boto_client, manager, mock_internal_utils
):
    """Ensure _start_glue_session passes Connections and Tags to CreateSession."""
    mock_glue_client = MagicMock()
    mock_session_cls.return_value.client.return_value = mock_glue_client
    mock_glue_client.create_session.return_value = {"Session": {"Id": "sess-3"}}
    mock_glue_client.get_session.return_value = {"Session": {"Status": "READY"}}
    mock_glue_client.get_session_endpoint.return_value = {
        "SparkConnect": {
            "Url": "sc://endpoint",
            "AuthToken": "tok",
            "AuthTokenExpirationTime": 1779314191,
        }
    }

    manager._lazy_init()
    manager._start_glue_session()

    create_call = mock_glue_client.create_session.call_args
    # Multi-subnet connections passed
    assert create_call[1]["Connections"] == {"Connections": ["conn-a", "conn-b"]}
    # Tags set
    assert "AmazonDataZoneSessionOwner" in create_call[1]["Tags"]
    assert create_call[1]["Tags"]["AmazonDataZoneProject"] == "proj-123"


@patch("boto3.client")
@patch("boto3.Session")
def test_start_glue_session_merges_spark_configs_in_order(
    mock_session_cls, mock_boto_client, manager, mock_internal_utils
):
    """Ensure spark configs are merged: defaults < connection < user spark_conf."""
    mock_glue_client = MagicMock()
    mock_session_cls.return_value.client.return_value = mock_glue_client
    mock_glue_client.create_session.return_value = {"Session": {"Id": "sess-4"}}
    mock_glue_client.get_session.return_value = {"Session": {"Status": "READY"}}
    mock_glue_client.get_session_endpoint.return_value = {
        "SparkConnect": {"Url": "sc://ep", "AuthToken": "t", "AuthTokenExpirationTime": 123}
    }

    # Add user spark_conf that should override connection config
    manager.spark_conf = {"spark.custom.key": "user-override", "spark.user.new": "val"}
    manager._lazy_init()
    manager._start_glue_session()

    create_call = mock_glue_client.create_session.call_args
    conf_str = create_call[1]["DefaultArguments"]["--conf"]
    # User override wins over connection-level
    assert "spark.custom.key=user-override" in conf_str
    assert "spark.user.new=val" in conf_str


# ---------------------------------------------------------------------------
# Wait and utility tests
# ---------------------------------------------------------------------------


def test_wait_for_glue_session_ready(manager):
    """Ensure _wait_for_glue_session returns True when session reaches READY."""
    manager.glue_client = MagicMock()
    manager.glue_client.get_session.return_value = {"Session": {"Status": "READY"}}

    result = manager._wait_for_glue_session("sess-1", timeout=5, poll_interval=0.1)
    assert result is True


def test_wait_for_glue_session_failed(manager):
    """Ensure _wait_for_glue_session raises RuntimeError on FAILED state."""
    manager.glue_client = MagicMock()
    manager.glue_client.get_session.return_value = {
        "Session": {"Status": "FAILED", "ErrorMessage": "Out of memory"}
    }

    with pytest.raises(RuntimeError, match="Out of memory"):
        manager._wait_for_glue_session("sess-1", timeout=5, poll_interval=0.1)


def test_wait_for_glue_session_timeout(manager):
    """Ensure _wait_for_glue_session raises RuntimeError on timeout."""
    manager.glue_client = MagicMock()
    manager.glue_client.get_session.return_value = {"Session": {"Status": "PROVISIONING"}}

    with pytest.raises(RuntimeError, match="was not ready within the session start timeout"):
        manager._wait_for_glue_session("sess-1", timeout=0.1, poll_interval=0.05)


def test_is_fta_supported_always_true_for_5_1(manager):
    """Ensure _is_fta_supported returns True when compat mode forced ON and version >= 5.0."""
    manager._is_compatibility_mode = True
    assert manager._is_fta_supported("5.1") is True
    assert manager._is_fta_supported("5.0") is True
    assert manager._is_fta_supported("4.0") is False


def test_construct_spark_endpoint_url(manager):
    """Ensure spark endpoint URL is properly constructed with URL-encoded token."""
    endpoint = {"Url": "sc://s-123.sessions.glue.us-east-2.amazonaws.com", "AuthToken": "tok=abc="}
    url = manager._construct_spark_endpoint_url(endpoint)

    assert url.startswith("sc://s-123.sessions.glue.us-east-2.amazonaws.com:443/")
    assert "use_ssl=true" in url
    # Token should be URL-encoded (= becomes %3D)
    assert "tok%3Dabc%3D" in url


def test_get_session_id(manager):
    """Ensure get_session_id returns the stored session id."""
    manager.glue_session_id = "sess-abc"
    assert manager.get_session_id() == "sess-abc"


def test_get_session_id_none(manager):
    """Ensure get_session_id returns None when no session exists."""
    assert manager.get_session_id() is None


def test_get_execution_role_arn_uses_project_role(manager):
    """Ensure _get_execution_role_arn returns project.iam_role."""
    manager.project = MagicMock()
    manager.project.iam_role = "arn:aws:iam::123:role/project-role"
    assert manager._get_execution_role_arn() == "arn:aws:iam::123:role/project-role"


def test_get_execution_role_arn_falls_back_to_metadata(manager):
    """Ensure _get_execution_role_arn falls back to ExecutionRoleArn from metadata."""
    manager.project = MagicMock()
    manager.project.iam_role = property(lambda self: (_ for _ in ()).throw(Exception("no role")))
    type(manager.project).iam_role = property(
        lambda self: (_ for _ in ()).throw(Exception("no role"))
    )

    with patch(
        "sagemaker_studio.utils.spark.session.glue.glue_spark_session_manager.InternalUtils"
    ) as mock_utils:
        mock_utils.return_value._get_field_from_environment.return_value = (
            "arn:aws:iam::123:role/fallback"
        )
        role = manager._get_execution_role_arn()

    assert role == "arn:aws:iam::123:role/fallback"


def test_stop_glue_session_calls_api(manager):
    """Ensure _stop_glue_session calls glue_client.stop_session."""
    manager.glue_client = MagicMock()
    manager._stop_glue_session("sess-to-stop")
    manager.glue_client.stop_session.assert_called_once_with(Id="sess-to-stop")


# ---------------------------------------------------------------------------
# _get_s3_access_grants_configs tests
# ---------------------------------------------------------------------------


def test_get_s3_access_grants_configs_enabled(manager):
    """Ensure S3 Access Grants configs are returned when enabled in provisioned resources."""
    manager.project = MagicMock()
    mock_api = MagicMock()
    manager.project._sagemaker_studio_api.project_api = mock_api
    mock_api.get_project_default_environment.return_value = {
        "provisionedResources": [
            {"name": "enableS3AccessGrantsForTools", "value": "true"},
        ]
    }

    with patch(
        "sagemaker_studio.utils.spark.session.glue.glue_spark_session_manager.InternalUtils"
    ) as mock_utils:
        mock_utils.return_value._get_domain_id.return_value = "dzd-abc123"
        result = manager._get_s3_access_grants_configs()

    assert result == {
        "spark.hadoop.fs.s3.s3AccessGrants.enabled": "true",
        "spark.hadoop.fs.s3.s3AccessGrants.fallbackToIAM": "true",
    }


def test_get_s3_access_grants_configs_returns_empty_when_disabled_or_error(manager):
    """Ensure empty dict when S3AG is disabled or API call fails."""
    manager.project = MagicMock()
    mock_api = MagicMock()
    manager.project._sagemaker_studio_api.project_api = mock_api

    with patch(
        "sagemaker_studio.utils.spark.session.glue.glue_spark_session_manager.InternalUtils"
    ) as mock_utils:
        mock_utils.return_value._get_domain_id.return_value = "dzd-abc123"

        # Case 1: disabled
        mock_api.get_project_default_environment.return_value = {
            "provisionedResources": [
                {"name": "enableS3AccessGrantsForTools", "value": "false"},
            ]
        }
        assert manager._get_s3_access_grants_configs() == {}

        # Case 2: API exception
        mock_api.get_project_default_environment.side_effect = Exception("API error")
        assert manager._get_s3_access_grants_configs() == {}


# ---------------------------------------------------------------------------
# _get_user_id_account_id and _get_account_id tests
# ---------------------------------------------------------------------------


def test_get_user_id_account_id_from_project_and_internal_utils(manager):
    """Ensure _get_user_id_account_id returns project.user_id and account from InternalUtils."""
    manager.project = MagicMock()
    manager.project.user_id = "project-user-xyz"
    manager.sts_client = MagicMock()

    with patch(
        "sagemaker_studio.utils.spark.session.glue.glue_spark_session_manager.InternalUtils"
    ) as mock_utils:
        mock_utils.return_value._get_account_id.return_value = "111222333444"
        user_id, account_id = manager._get_user_id_account_id()

    assert user_id == "project-user-xyz"
    assert account_id == "111222333444"
    manager.sts_client.get_caller_identity.assert_not_called()


def test_get_account_id_from_internal_utils(manager):
    """Ensure _get_account_id returns value from InternalUtils when available."""
    manager.sts_client = MagicMock()

    with patch(
        "sagemaker_studio.utils.spark.session.glue.glue_spark_session_manager.InternalUtils"
    ) as mock_utils:
        mock_utils.return_value._get_account_id.return_value = "111222333444"
        account_id = manager._get_account_id()

    assert account_id == "111222333444"
    manager.sts_client.get_caller_identity.assert_not_called()


def test_get_account_id_fallback_to_sts(manager):
    """Ensure _get_account_id falls back to STS when InternalUtils returns None."""
    manager.sts_client = MagicMock()
    manager.sts_client.get_caller_identity.return_value = {
        "Account": "999888777666",
        "UserId": "AROA123:john.doe",
    }

    with patch(
        "sagemaker_studio.utils.spark.session.glue.glue_spark_session_manager.InternalUtils"
    ) as mock_utils:
        mock_utils.return_value._get_account_id.return_value = None
        account_id = manager._get_account_id()

    assert account_id == "999888777666"


# ---------------------------------------------------------------------------
# _wait_for_glue_session exception propagation test
# ---------------------------------------------------------------------------


def test_wait_for_glue_session_api_exception_propagates(manager):
    """Ensure _wait_for_glue_session propagates non-RuntimeError exceptions from get_session."""
    manager.glue_client = MagicMock()
    manager.glue_client.get_session.side_effect = Exception("Network error")

    with pytest.raises(Exception, match="Network error"):
        manager._wait_for_glue_session("sess-1", timeout=5, poll_interval=0.1)


# ---------------------------------------------------------------------------
# _start_glue_session: FTA not supported path
# ---------------------------------------------------------------------------


@patch("boto3.client")
@patch("boto3.Session")
def test_start_glue_session_fta_not_supported_removes_compat_keys(
    mock_session_cls, mock_boto_client, mock_internal_utils
):
    """Ensure compat keys are removed when FTA is not supported (glueVersion < 5.0)."""
    conn = MagicMock()
    conn._Connection__connection_data = {
        "props": {"sparkGlueProperties": {"glueVersion": "4.0", "numberOfWorkers": 5}},
        "configurations": [],
        "physicalEndpoints": [],
    }

    mock_glue_client = MagicMock()
    mock_session_cls.return_value.client.return_value = mock_glue_client
    mock_glue_client.create_session.return_value = {"Session": {"Id": "sess-fta"}}
    mock_glue_client.get_session.return_value = {"Session": {"Status": "READY"}}
    mock_glue_client.get_session_endpoint.return_value = {
        "SparkConnect": {"Url": "sc://ep", "AuthToken": "t", "AuthTokenExpirationTime": 123}
    }

    mgr = GlueSparkSessionManager(connection=conn)
    mgr._lazy_init()

    # Force compatibility mode off to trigger the "FTA not supported" branch
    mgr._is_compatibility_mode = False
    mgr._start_glue_session()

    create_call = mock_glue_client.create_session.call_args
    conf_str = create_call[1]["DefaultArguments"]["--conf"]
    # Compat keys should NOT be present
    assert "spark.hadoop.fs.s3.credentialsResolverClass" not in conf_str
    assert "spark.sql.catalog.spark_catalog.glue.lakeformation-enabled" not in conf_str


# ---------------------------------------------------------------------------
# _start_glue_session: scheduled run request origin
# ---------------------------------------------------------------------------


@patch("boto3.client")
@patch("boto3.Session")
def test_start_glue_session_scheduled_run_request_origin(mock_session_cls, mock_boto_client):
    """Ensure RequestOrigin is NotebookScheduledRun when SpaceName is absent."""
    conn = MagicMock()
    conn._Connection__connection_data = {
        "props": {"sparkGlueProperties": {"glueVersion": "5.1"}},
        "configurations": [],
        "physicalEndpoints": [],
    }

    mock_glue_client = MagicMock()
    mock_session_cls.return_value.client.return_value = mock_glue_client
    mock_glue_client.create_session.return_value = {"Session": {"Id": "sess-sched"}}
    mock_glue_client.get_session.return_value = {"Session": {"Status": "READY"}}
    mock_glue_client.get_session_endpoint.return_value = {
        "SparkConnect": {"Url": "sc://ep", "AuthToken": "t", "AuthTokenExpirationTime": 123}
    }

    with patch(
        "sagemaker_studio.utils.spark.session.glue.glue_spark_session_manager.InternalUtils"
    ) as mock_utils, patch(
        "sagemaker_studio.utils.spark.session.glue.glue_spark_session_manager._ensure_project"
    ) as mock_ensure_project, patch(
        "sagemaker_studio.utils.spark.session.spark_config_builder._ensure_project"
    ), patch(
        "sagemaker_studio.utils.spark.session.spark_config_builder._generate_s3tables_spark_configs",
        return_value={},
    ), patch(
        "sagemaker_studio.utils.spark.session.spark_config_builder._generate_glue_catalog_spark_configs",
        return_value={},
    ), patch(
        "sagemaker_studio.utils.spark.session.spark_config_builder._generate_workday_irc_spark_configs",
        return_value={},
    ):
        mock_utils.return_value._get_domain_region.return_value = "us-east-2"
        mock_utils.return_value._get_account_id.return_value = "123456789012"
        mock_utils.return_value._get_user_id.return_value = "test-user"
        mock_utils.return_value._get_domain_id.return_value = "dzd-abc123"
        # SpaceName is None → scheduled run
        mock_utils.return_value._get_field_from_environment.side_effect = lambda key: {
            "ProjectS3Path": "s3://bucket/path",
            "SpaceName": None,
            "ExecutionRoleArn": "arn:aws:iam::123:role/role",
        }.get(key)
        mock_project = MagicMock()
        mock_project.iam_role = "arn:aws:iam::123:role/role"
        mock_project.id = "proj-123"
        mock_project.user_id = "test-user"
        mock_project.domain_id = "dzd-abc123"
        mock_project.s3 = MagicMock()
        mock_project.s3.root = "s3://bucket/path"
        mock_project._sagemaker_studio_api = MagicMock()
        mock_ensure_project.return_value = mock_project

        mgr = GlueSparkSessionManager(connection=conn)
        mgr._lazy_init()
        mgr._start_glue_session()

    create_call = mock_glue_client.create_session.call_args
    assert create_call[1]["RequestOrigin"] == "SageMakerUnifiedStudio_NotebookScheduledRun"


# ---------------------------------------------------------------------------
# _get_session_endpoint_with_retry tests
# ---------------------------------------------------------------------------


def test_get_session_endpoint_with_retry_succeeds_first_attempt(manager):
    """Ensure _get_session_endpoint_with_retry returns on first success without retrying."""
    manager.glue_client = MagicMock()
    manager.glue_client.get_session_endpoint.return_value = {
        "SparkConnect": {"Url": "sc://ep", "AuthToken": "tok", "AuthTokenExpirationTime": 123}
    }

    result = manager._get_session_endpoint_with_retry("sess-1", max_retries=3, backoff=0.01)

    assert result["SparkConnect"]["Url"] == "sc://ep"
    manager.glue_client.get_session_endpoint.assert_called_once_with(SessionId="sess-1")


def test_get_session_endpoint_with_retry_retries_on_transient_errors(manager):
    """Ensure transient errors (InternalServiceException, OperationTimeoutException) are retried."""
    from botocore.exceptions import ClientError

    manager.glue_client = MagicMock()
    manager.glue_client.get_session_endpoint.side_effect = [
        ClientError(
            {"Error": {"Code": "InternalServiceException", "Message": "transient"}},
            "GetSessionEndpoint",
        ),
        ClientError(
            {"Error": {"Code": "OperationTimeoutException", "Message": "timeout"}},
            "GetSessionEndpoint",
        ),
        {"SparkConnect": {"Url": "sc://ep", "AuthToken": "tok", "AuthTokenExpirationTime": 123}},
    ]

    result = manager._get_session_endpoint_with_retry("sess-1", max_retries=3, backoff=0.01)

    assert result["SparkConnect"]["Url"] == "sc://ep"
    assert manager.glue_client.get_session_endpoint.call_count == 3


def test_get_session_endpoint_with_retry_raises_non_retryable_error(manager):
    """Ensure non-retryable errors (AccessDeniedException) are raised immediately."""
    from botocore.exceptions import ClientError

    manager.glue_client = MagicMock()
    manager.glue_client.get_session_endpoint.side_effect = ClientError(
        {"Error": {"Code": "AccessDeniedException", "Message": "denied"}}, "GetSessionEndpoint"
    )

    with pytest.raises(ClientError, match="AccessDeniedException"):
        manager._get_session_endpoint_with_retry("sess-1", max_retries=3, backoff=0.01)

    manager.glue_client.get_session_endpoint.assert_called_once()


def test_get_session_endpoint_with_retry_exhausts_retries(manager):
    """Ensure error is raised after all retries are exhausted."""
    from botocore.exceptions import ClientError

    manager.glue_client = MagicMock()
    manager.glue_client.get_session_endpoint.side_effect = ClientError(
        {"Error": {"Code": "InternalServiceException", "Message": "persistent"}},
        "GetSessionEndpoint",
    )

    with pytest.raises(ClientError, match="InternalServiceException"):
        manager._get_session_endpoint_with_retry("sess-1", max_retries=1, backoff=0.01)

    # 1 initial + 1 retry = 2 total attempts
    assert manager.glue_client.get_session_endpoint.call_count == 2


# ---------------------------------------------------------------------------
# Additional coverage tests
# ---------------------------------------------------------------------------


def test_stop_logs_error_when_stop_glue_session_fails(manager):
    """Ensure stop() logs error but still clears state when _stop_glue_session raises."""
    manager._spark_session = MagicMock()
    manager.glue_session_id = "sess-fail"
    manager.glue_client = MagicMock()
    manager.glue_client.stop_session.side_effect = Exception("stop failed")

    manager.stop()

    # State should still be cleared despite the error
    assert manager._spark_session is None
    assert manager.glue_session_id is None


def test_get_execution_role_arn_raises_when_both_sources_fail(manager):
    """Ensure _get_execution_role_arn raises RuntimeError when project and metadata both fail."""
    manager.project = MagicMock()
    type(manager.project).iam_role = property(
        lambda self: (_ for _ in ()).throw(Exception("no role"))
    )

    with patch(
        "sagemaker_studio.utils.spark.session.glue.glue_spark_session_manager.InternalUtils"
    ) as mock_utils:
        mock_utils.return_value._get_field_from_environment.return_value = None
        with pytest.raises(RuntimeError, match="Could not resolve execution role"):
            manager._get_execution_role_arn()


@patch("boto3.client")
@patch("boto3.Session")
def test_start_glue_session_no_project_s3_path(
    mock_session_cls, mock_boto_client, mock_internal_utils
):
    """Ensure _start_glue_session handles missing ProjectS3Path gracefully."""
    mock_utils_cls, mock_project = mock_internal_utils
    # Override project.s3.root to None
    mock_project.return_value.s3.root = None

    conn = MagicMock()
    conn._Connection__connection_data = {
        "props": {"sparkGlueProperties": {"glueVersion": "5.1"}},
        "configurations": [],
        "physicalEndpoints": [],
    }

    mock_glue_client = MagicMock()
    mock_session_cls.return_value.client.return_value = mock_glue_client
    mock_glue_client.create_session.return_value = {"Session": {"Id": "sess-no-s3"}}
    mock_glue_client.get_session.return_value = {"Session": {"Status": "READY"}}
    mock_glue_client.get_session_endpoint.return_value = {
        "SparkConnect": {"Url": "sc://ep", "AuthToken": "t", "AuthTokenExpirationTime": 123}
    }

    mgr = GlueSparkSessionManager(connection=conn)
    mgr._lazy_init()
    mgr._start_glue_session()

    create_call = mock_glue_client.create_session.call_args
    args = create_call[1]["DefaultArguments"]
    # S3 log paths should NOT be present
    assert "--spark-event-logs-path" not in args
    assert "--spark-logs-s3-uri" not in args


@patch("boto3.client")
@patch("boto3.Session")
def test_start_glue_session_invalid_glue_version_string(
    mock_session_cls, mock_boto_client, mock_internal_utils
):
    """Ensure _start_glue_session handles non-numeric glueVersion without crashing."""
    conn = MagicMock()
    conn._Connection__connection_data = {
        "props": {"sparkGlueProperties": {"glueVersion": "invalid"}},
        "configurations": [],
        "physicalEndpoints": [],
    }

    mock_glue_client = MagicMock()
    mock_session_cls.return_value.client.return_value = mock_glue_client
    mock_glue_client.create_session.return_value = {"Session": {"Id": "sess-inv"}}
    mock_glue_client.get_session.return_value = {"Session": {"Status": "READY"}}
    mock_glue_client.get_session_endpoint.return_value = {
        "SparkConnect": {"Url": "sc://ep", "AuthToken": "t", "AuthTokenExpirationTime": 123}
    }

    mgr = GlueSparkSessionManager(connection=conn)
    mgr._lazy_init()
    mgr._start_glue_session()

    create_call = mock_glue_client.create_session.call_args
    # Non-numeric version passes through unchanged (ValueError caught)
    assert create_call[1]["GlueVersion"] == "invalid"


@patch("boto3.client")
@patch("boto3.Session")
def test_lazy_init_model_path_not_found(mock_session_cls, mock_boto_client, mock_internal_utils):
    """Ensure _lazy_init falls back to default boto3 session when model path doesn't exist."""
    conn = MagicMock()
    conn._Connection__connection_data = {
        "props": {"sparkGlueProperties": {}},
        "configurations": [],
        "physicalEndpoints": [],
    }

    mock_session_cls.return_value.client.return_value = MagicMock()

    mgr = GlueSparkSessionManager(connection=conn)

    with patch("os.path.isdir", return_value=False):
        mgr._lazy_init()

    # Should still have a glue_client (from default boto3 session)
    assert mgr.glue_client is not None


# ---------------------------------------------------------------------------
# Project caching tests
# ---------------------------------------------------------------------------


@patch("boto3.client")
@patch("boto3.Session")
def test_lazy_init_caches_project(mock_session_cls, mock_boto_client, mock_internal_utils):
    """Ensure _lazy_init uses _ensure_project() for cached singleton access."""
    _, mock_ensure_project = mock_internal_utils
    conn = MagicMock()
    conn._Connection__connection_data = {
        "props": {"sparkGlueProperties": {}},
        "configurations": [],
        "physicalEndpoints": [],
    }

    mock_session_cls.return_value.client.return_value = MagicMock()

    mgr = GlueSparkSessionManager(connection=conn)
    mgr._lazy_init()
    mgr._lazy_init()

    # _ensure_project() is called each time but returns cached singleton internally
    assert mgr.project is mock_ensure_project.return_value


@patch("boto3.client")
@patch("boto3.Session")
def test_lazy_init_respects_preexisting_project(
    mock_session_cls, mock_boto_client, mock_internal_utils
):
    """Ensure _lazy_init does not overwrite an externally-set project instance."""
    _, mock_ensure_project = mock_internal_utils
    conn = MagicMock()
    conn._Connection__connection_data = {
        "props": {"sparkGlueProperties": {}},
        "configurations": [],
        "physicalEndpoints": [],
    }

    mock_session_cls.return_value.client.return_value = MagicMock()

    mgr = GlueSparkSessionManager(connection=conn)
    existing_project = MagicMock()
    existing_project.id = "pre-existing-proj"
    mgr.project = existing_project
    mgr._lazy_init()

    # Should not overwrite the pre-existing project
    assert mgr.project.id == "pre-existing-proj"


# ---------------------------------------------------------------------------
# _get_domain_id deprecated method test
# ---------------------------------------------------------------------------


def test_get_domain_id_delegates_to_project(manager):
    """Ensure _get_domain_id returns self.project.domain_id."""
    manager.project = MagicMock()
    manager.project.domain_id = "dzd-test-domain"
    assert manager._get_domain_id() == "dzd-test-domain"


def test_get_domain_id_returns_empty_when_none(manager):
    """Ensure _get_domain_id returns empty string when project.domain_id is None."""
    manager.project = MagicMock()
    manager.project.domain_id = None
    assert manager._get_domain_id() == ""


# ---------------------------------------------------------------------------
# _start_glue_session: user_id from project and domain_id from project
# ---------------------------------------------------------------------------


@patch("boto3.client")
@patch("boto3.Session")
def test_start_glue_session_uses_project_user_id(
    mock_session_cls, mock_boto_client, mock_internal_utils
):
    """Ensure _start_glue_session uses self.project.user_id for session tags."""
    _, mock_project = mock_internal_utils
    mock_project.return_value.user_id = "custom-project-user"

    conn = MagicMock()
    conn._Connection__connection_data = {
        "props": {"sparkGlueProperties": {"glueVersion": "5.1"}},
        "configurations": [],
        "physicalEndpoints": [],
    }

    mock_glue_client = MagicMock()
    mock_session_cls.return_value.client.return_value = mock_glue_client
    mock_glue_client.create_session.return_value = {"Session": {"Id": "sess-uid"}}
    mock_glue_client.get_session.return_value = {"Session": {"Status": "READY"}}
    mock_glue_client.get_session_endpoint.return_value = {
        "SparkConnect": {"Url": "sc://ep", "AuthToken": "t", "AuthTokenExpirationTime": 123}
    }

    mgr = GlueSparkSessionManager(connection=conn)
    mgr._lazy_init()
    mgr._start_glue_session()

    create_call = mock_glue_client.create_session.call_args
    assert create_call[1]["Tags"]["AmazonDataZoneSessionOwner"] == "custom-project-user"


@patch("boto3.client")
@patch("boto3.Session")
def test_start_glue_session_uses_project_domain_id_for_openlineage(
    mock_session_cls, mock_boto_client, mock_internal_utils
):
    """Ensure _start_glue_session uses self.project.domain_id in OpenLineage config."""
    _, mock_project = mock_internal_utils
    mock_project.return_value.domain_id = "dzd-openlineage-test"

    conn = MagicMock()
    conn._Connection__connection_data = {
        "props": {"sparkGlueProperties": {"glueVersion": "5.1"}},
        "configurations": [],
        "physicalEndpoints": [],
    }

    mock_glue_client = MagicMock()
    mock_session_cls.return_value.client.return_value = mock_glue_client
    mock_glue_client.create_session.return_value = {"Session": {"Id": "sess-ol"}}
    mock_glue_client.get_session.return_value = {"Session": {"Status": "READY"}}
    mock_glue_client.get_session_endpoint.return_value = {
        "SparkConnect": {"Url": "sc://ep", "AuthToken": "t", "AuthTokenExpirationTime": 123}
    }

    mgr = GlueSparkSessionManager(connection=conn)
    mgr._lazy_init()
    mgr._start_glue_session()

    create_call = mock_glue_client.create_session.call_args
    conf_str = create_call[1]["DefaultArguments"]["--conf"]
    assert "spark.openlineage.transport.domainId=dzd-openlineage-test" in conf_str


@patch("boto3.client")
@patch("boto3.Session")
def test_start_glue_session_uses_project_s3_root(
    mock_session_cls, mock_boto_client, mock_internal_utils
):
    """Ensure _start_glue_session uses self.project.s3.root for log paths."""
    _, mock_project = mock_internal_utils
    mock_project.return_value.s3.root = "s3://my-project-bucket/root"

    conn = MagicMock()
    conn._Connection__connection_data = {
        "props": {"sparkGlueProperties": {"glueVersion": "5.1"}},
        "configurations": [],
        "physicalEndpoints": [],
    }

    mock_glue_client = MagicMock()
    mock_session_cls.return_value.client.return_value = mock_glue_client
    mock_glue_client.create_session.return_value = {"Session": {"Id": "sess-s3"}}
    mock_glue_client.get_session.return_value = {"Session": {"Status": "READY"}}
    mock_glue_client.get_session_endpoint.return_value = {
        "SparkConnect": {"Url": "sc://ep", "AuthToken": "t", "AuthTokenExpirationTime": 123}
    }

    mgr = GlueSparkSessionManager(connection=conn)
    mgr._lazy_init()
    mgr._start_glue_session()

    create_call = mock_glue_client.create_session.call_args
    args = create_call[1]["DefaultArguments"]
    assert (
        args["--spark-event-logs-path"]
        == "s3://my-project-bucket/root/glue/glue-spark-events-logs/"
    )
    assert args["--spark-logs-s3-uri"] == "s3://my-project-bucket/root/glue/glue-spark-system-logs/"


@patch("boto3.client")
@patch("boto3.Session")
def test_start_glue_session_strips_trailing_slash_from_s3_root(
    mock_session_cls, mock_boto_client, mock_internal_utils
):
    """Ensure trailing slash in project.s3.root is stripped before building log paths."""
    _, mock_project = mock_internal_utils
    mock_project.return_value.s3.root = "s3://bucket/path/"

    conn = MagicMock()
    conn._Connection__connection_data = {
        "props": {"sparkGlueProperties": {"glueVersion": "5.1"}},
        "configurations": [],
        "physicalEndpoints": [],
    }

    mock_glue_client = MagicMock()
    mock_session_cls.return_value.client.return_value = mock_glue_client
    mock_glue_client.create_session.return_value = {"Session": {"Id": "sess-slash"}}
    mock_glue_client.get_session.return_value = {"Session": {"Status": "READY"}}
    mock_glue_client.get_session_endpoint.return_value = {
        "SparkConnect": {"Url": "sc://ep", "AuthToken": "t", "AuthTokenExpirationTime": 123}
    }

    mgr = GlueSparkSessionManager(connection=conn)
    mgr._lazy_init()
    mgr._start_glue_session()

    create_call = mock_glue_client.create_session.call_args
    args = create_call[1]["DefaultArguments"]
    # Should not have double slashes
    assert args["--spark-event-logs-path"] == "s3://bucket/path/glue/glue-spark-events-logs/"


# ---------------------------------------------------------------------------
# _get_s3_access_grants_configs uses project.domain_id
# ---------------------------------------------------------------------------


def test_get_s3_access_grants_configs_uses_project_domain_id(manager):
    """Ensure _get_s3_access_grants_configs uses self.project.domain_id."""
    manager.project = MagicMock()
    manager.project.domain_id = "dzd-s3ag-test"
    manager.project.id = "proj-s3ag"
    mock_api = MagicMock()
    manager.project._sagemaker_studio_api.project_api = mock_api
    mock_api.get_project_default_environment.return_value = {
        "provisionedResources": [
            {"name": "enableS3AccessGrantsForTools", "value": "true"},
        ]
    }

    result = manager._get_s3_access_grants_configs()

    mock_api.get_project_default_environment.assert_called_once_with("dzd-s3ag-test", "proj-s3ag")
    assert result == {
        "spark.hadoop.fs.s3.s3AccessGrants.enabled": "true",
        "spark.hadoop.fs.s3.s3AccessGrants.fallbackToIAM": "true",
    }


# ---------------------------------------------------------------------------
# _start_glue_session: JOB_NAME uses project.user_id
# ---------------------------------------------------------------------------


@patch("boto3.client")
@patch("boto3.Session")
def test_start_glue_session_job_name_uses_project_user_id(
    mock_session_cls, mock_boto_client, mock_internal_utils
):
    """Ensure JOB_NAME in OpenLineage config uses project.user_id."""
    _, mock_project = mock_internal_utils
    mock_project.return_value.user_id = "job-name-user"
    mock_project.return_value.id = "proj-job"

    conn = MagicMock()
    conn._Connection__connection_data = {
        "props": {"sparkGlueProperties": {"glueVersion": "5.1"}},
        "configurations": [],
        "physicalEndpoints": [],
    }

    mock_glue_client = MagicMock()
    mock_session_cls.return_value.client.return_value = mock_glue_client
    mock_glue_client.create_session.return_value = {"Session": {"Id": "sess-jn"}}
    mock_glue_client.get_session.return_value = {"Session": {"Status": "READY"}}
    mock_glue_client.get_session_endpoint.return_value = {
        "SparkConnect": {"Url": "sc://ep", "AuthToken": "t", "AuthTokenExpirationTime": 123}
    }

    mgr = GlueSparkSessionManager(connection=conn)
    mgr._lazy_init()
    mgr._start_glue_session()

    create_call = mock_glue_client.create_session.call_args
    conf_str = create_call[1]["DefaultArguments"]["--conf"]
    assert "spark.glue.JOB_NAME=Interactive/proj-job/job-name-user" in conf_str


# ---------------------------------------------------------------------------
# __init__ default state test
# ---------------------------------------------------------------------------


def test_init_sets_project_to_none():
    """Ensure __init__ initializes project as None for lazy caching."""
    mgr = GlueSparkSessionManager(connection_name="test-conn")
    assert mgr.project is None
    assert mgr.glue_session_id is None
    assert mgr._spark_session is None
    assert mgr.glue_client is None
    assert mgr.sts_client is None


def test_init_stores_spark_conf():
    """Ensure __init__ stores user-provided spark_conf."""
    conf = {"spark.key": "value"}
    mgr = GlueSparkSessionManager(spark_conf=conf)
    assert mgr.spark_conf == {"spark.key": "value"}


# ---------------------------------------------------------------------------
# _start_glue_session: connection default arguments merged
# ---------------------------------------------------------------------------


@patch("boto3.client")
@patch("boto3.Session")
def test_start_glue_session_connection_default_args_merged(
    mock_session_cls, mock_boto_client, manager, mock_internal_utils
):
    """Ensure connection-level GlueDefaultArgument properties are merged into DefaultArguments."""
    mock_glue_client = MagicMock()
    mock_session_cls.return_value.client.return_value = mock_glue_client
    mock_glue_client.create_session.return_value = {"Session": {"Id": "sess-da"}}
    mock_glue_client.get_session.return_value = {"Session": {"Status": "READY"}}
    mock_glue_client.get_session_endpoint.return_value = {
        "SparkConnect": {"Url": "sc://ep", "AuthToken": "t", "AuthTokenExpirationTime": 123}
    }

    manager._lazy_init()
    manager._start_glue_session()

    create_call = mock_glue_client.create_session.call_args
    default_args = create_call[1]["DefaultArguments"]
    # FGAC should be forced to false even though connection had it as true
    assert default_args["--enable-lakeformation-fine-grained-access"] == "false"
    # Other default arguments should be present
    assert default_args["--enable-glue-datacatalog"] == "true"
    assert default_args["--enable-auto-scaling"] == "true"
    assert default_args["--datalake-formats"] == "iceberg"


# ---------------------------------------------------------------------------
# _start_glue_session: no connections when list is empty
# ---------------------------------------------------------------------------


@patch("boto3.client")
@patch("boto3.Session")
def test_start_glue_session_no_connections_param_when_empty(
    mock_session_cls, mock_boto_client, mock_internal_utils
):
    """Ensure Connections param is not passed when glueConnectionNames is empty."""
    conn = MagicMock()
    conn._Connection__connection_data = {
        "props": {"sparkGlueProperties": {"glueVersion": "5.1"}},
        "configurations": [],
        "physicalEndpoints": [],  # No endpoints → no connection names
    }

    mock_glue_client = MagicMock()
    mock_session_cls.return_value.client.return_value = mock_glue_client
    mock_glue_client.create_session.return_value = {"Session": {"Id": "sess-noconn"}}
    mock_glue_client.get_session.return_value = {"Session": {"Status": "READY"}}
    mock_glue_client.get_session_endpoint.return_value = {
        "SparkConnect": {"Url": "sc://ep", "AuthToken": "t", "AuthTokenExpirationTime": 123}
    }

    mgr = GlueSparkSessionManager(connection=conn)
    mgr._lazy_init()
    mgr._start_glue_session()

    create_call = mock_glue_client.create_session.call_args
    assert "Connections" not in create_call[1]


# ---------------------------------------------------------------------------
# Additional coverage: uncovered branches
# ---------------------------------------------------------------------------


@patch("boto3.client")
@patch("boto3.Session")
def test_lazy_init_with_glue_endpoint_url(mock_session_cls, mock_boto_client, mock_internal_utils):
    """Ensure _lazy_init passes endpoint_url when configured in overrides."""
    conn = MagicMock()
    conn._Connection__connection_data = {
        "props": {"sparkGlueProperties": {}},
        "configurations": [],
        "physicalEndpoints": [],
    }

    mock_glue_client = MagicMock()
    mock_session_cls.return_value.client.return_value = mock_glue_client

    mgr = GlueSparkSessionManager(
        connection=conn,
        config=ClientConfig(
            overrides={"glue": {"endpoint_url": "https://glue-gamma.us-east-2.amazonaws.com"}}
        ),
    )
    mgr._lazy_init()

    # Verify the custom endpoint was passed to the glue client
    mock_session_cls.return_value.client.assert_called_with(
        "glue",
        region_name="us-east-2",
        endpoint_url="https://glue-gamma.us-east-2.amazonaws.com",
    )


@patch("boto3.client")
@patch("boto3.Session")
def test_lazy_init_connection_lookup_by_name(
    mock_session_cls, mock_boto_client, mock_internal_utils
):
    """Ensure _lazy_init looks up connection by name when _connection is None."""
    _, mock_ensure_project = mock_internal_utils
    mock_project = mock_ensure_project.return_value

    mock_conn = MagicMock()
    mock_conn._Connection__connection_data = {
        "props": {"sparkGlueProperties": {"glueVersion": "5.1"}},
        "configurations": [],
        "physicalEndpoints": [],
    }
    mock_project.connection.return_value = mock_conn

    mock_session_cls.return_value.client.return_value = MagicMock()

    mgr = GlueSparkSessionManager(connection_name="my-glue-conn")
    mgr._lazy_init()

    mock_project.connection.assert_called_with("my-glue-conn")


@patch("boto3.client")
@patch("boto3.Session")
def test_lazy_init_connection_lookup_by_type(
    mock_session_cls, mock_boto_client, mock_internal_utils
):
    """Ensure _lazy_init looks up SPARK_CONNECT connection when no name or connection provided."""
    _, mock_ensure_project = mock_internal_utils
    mock_project = mock_ensure_project.return_value

    mock_conn = MagicMock()
    mock_conn._Connection__connection_data = {
        "props": {"sparkGlueProperties": {}},
        "configurations": [],
        "physicalEndpoints": [],
    }
    mock_project.connection.return_value = mock_conn

    mock_session_cls.return_value.client.return_value = MagicMock()

    mgr = GlueSparkSessionManager()
    mgr._lazy_init()

    mock_project.connection.assert_called_with(type="SPARK_CONNECT")


@patch("boto3.client")
@patch("boto3.Session")
def test_lazy_init_warns_on_multiple_physical_endpoints(
    mock_session_cls, mock_boto_client, mock_internal_utils, caplog
):
    """Ensure _lazy_init logs a warning when connection has multiple physicalEndpoints."""
    conn = MagicMock()
    conn._Connection__connection_data = {
        "props": {"sparkGlueProperties": {}},
        "configurations": [],
        "physicalEndpoints": [
            {"glueConnectionNames": ["conn-a"]},
            {"glueConnectionNames": ["conn-b"]},
        ],
    }

    mock_session_cls.return_value.client.return_value = MagicMock()

    import logging

    with caplog.at_level(logging.WARNING, logger="SparkConnect.Glue"):
        mgr = GlueSparkSessionManager(connection=conn)
        mgr._lazy_init()

    assert any("2 physicalEndpoints" in msg for msg in caplog.messages)
    # Uses first endpoint
    assert mgr._glue_connection_names == ["conn-a"]


@patch("boto3.client")
@patch("boto3.Session")
def test_start_glue_session_s3ag_configs_merged(
    mock_session_cls, mock_boto_client, mock_internal_utils
):
    """Ensure S3 Access Grants configs are merged into session when enabled."""
    _, mock_ensure_project = mock_internal_utils
    mock_project = mock_ensure_project.return_value
    mock_api = MagicMock()
    mock_project._sagemaker_studio_api.project_api = mock_api
    mock_api.get_project_default_environment.return_value = {
        "provisionedResources": [
            {"name": "enableS3AccessGrantsForTools", "value": "true"},
        ]
    }

    conn = MagicMock()
    conn._Connection__connection_data = {
        "props": {"sparkGlueProperties": {"glueVersion": "5.1"}},
        "configurations": [],
        "physicalEndpoints": [],
    }

    mock_glue_client = MagicMock()
    mock_session_cls.return_value.client.return_value = mock_glue_client
    mock_glue_client.create_session.return_value = {"Session": {"Id": "sess-s3ag"}}
    mock_glue_client.get_session.return_value = {"Session": {"Status": "READY"}}
    mock_glue_client.get_session_endpoint.return_value = {
        "SparkConnect": {"Url": "sc://ep", "AuthToken": "t", "AuthTokenExpirationTime": 123}
    }

    mgr = GlueSparkSessionManager(connection=conn)
    mgr._lazy_init()
    mgr._start_glue_session()

    create_call = mock_glue_client.create_session.call_args
    conf_str = create_call[1]["DefaultArguments"]["--conf"]
    assert "spark.hadoop.fs.s3.s3AccessGrants.enabled=true" in conf_str
    assert "spark.hadoop.fs.s3.s3AccessGrants.fallbackToIAM=true" in conf_str


@patch("boto3.client")
@patch("boto3.Session")
def test_start_glue_session_exception_propagates(
    mock_session_cls, mock_boto_client, mock_internal_utils
):
    """Ensure _start_glue_session propagates exceptions from create_session."""
    conn = MagicMock()
    conn._Connection__connection_data = {
        "props": {"sparkGlueProperties": {"glueVersion": "5.1"}},
        "configurations": [],
        "physicalEndpoints": [],
    }

    mock_glue_client = MagicMock()
    mock_session_cls.return_value.client.return_value = mock_glue_client
    mock_glue_client.create_session.side_effect = Exception("CreateSession failed")

    mgr = GlueSparkSessionManager(connection=conn)
    mgr._lazy_init()

    with pytest.raises(Exception, match="CreateSession failed"):
        mgr._start_glue_session()


# ---------------------------------------------------------------------------
# User-configurable CreateSession fields via ClientConfig.overrides["glue"]
# ---------------------------------------------------------------------------


@patch("boto3.client")
@patch("boto3.Session")
def test_lazy_init_extracts_session_overrides(
    mock_session_cls, mock_boto_client, mock_internal_utils
):
    """Ensure _lazy_init picks up only recognized session fields from overrides['glue']."""
    conn = MagicMock()
    conn._Connection__connection_data = {
        "props": {"sparkGlueProperties": {"glueVersion": "5.1"}},
        "configurations": [],
        "physicalEndpoints": [],
    }
    mock_session_cls.return_value.client.return_value = MagicMock()

    mgr = GlueSparkSessionManager(
        connection=conn,
        config=ClientConfig(
            overrides={
                "glue": {
                    "endpoint_url": "https://glue.us-east-2.amazonaws.com",
                    "workerType": "G.2X",
                    "numberOfWorkers": 25,
                    "idleTimeout": 10,
                    "glueVersion": "5.2",
                    "unrecognizedKey": "ignored",
                }
            }
        ),
    )
    mgr._lazy_init()

    # Only the recognized sizing keys are captured; endpoint_url and unknown keys excluded.
    assert mgr._glue_session_overrides == {
        "workerType": "G.2X",
        "numberOfWorkers": 25,
        "idleTimeout": 10,
        "glueVersion": "5.2",
    }


@patch("boto3.client")
@patch("boto3.Session")
def test_start_glue_session_user_overrides_take_precedence(
    mock_session_cls, mock_boto_client, mock_internal_utils
):
    """Ensure user overrides win over connection sparkGlueProperties in CreateSession."""
    conn = MagicMock()
    conn._Connection__connection_data = {
        "props": {
            "sparkGlueProperties": {
                "glueVersion": "5.1",
                "workerType": "G.1X",
                "numberOfWorkers": 10,
                "idleTimeout": 15,
            }
        },
        "configurations": [],
        "physicalEndpoints": [],
    }

    mock_glue_client = MagicMock()
    mock_session_cls.return_value.client.return_value = mock_glue_client
    mock_glue_client.create_session.return_value = {"Session": {"Id": "sess-ovr"}}
    mock_glue_client.get_session.return_value = {"Session": {"Status": "READY"}}
    mock_glue_client.get_session_endpoint.return_value = {
        "SparkConnect": {"Url": "sc://ep", "AuthToken": "t", "AuthTokenExpirationTime": 123}
    }

    mgr = GlueSparkSessionManager(
        connection=conn,
        config=ClientConfig(
            overrides={
                "glue": {
                    "workerType": "G.2X",
                    "numberOfWorkers": 30,
                    "glueVersion": "5.2",
                    "idleTimeout": 12,
                }
            }
        ),
    )
    mgr._lazy_init()
    mgr._start_glue_session()

    create_call = mock_glue_client.create_session.call_args
    assert create_call[1]["WorkerType"] == "G.2X"
    assert create_call[1]["NumberOfWorkers"] == 30
    assert create_call[1]["GlueVersion"] == "5.2"
    assert create_call[1]["IdleTimeout"] == 12


@patch("boto3.client")
@patch("boto3.Session")
def test_start_glue_session_falls_back_to_connection_when_no_override(
    mock_session_cls, mock_boto_client, mock_internal_utils
):
    """Ensure connection props are used for fields not present in user overrides."""
    conn = MagicMock()
    conn._Connection__connection_data = {
        "props": {
            "sparkGlueProperties": {
                "glueVersion": "5.1",
                "workerType": "G.4X",
                "numberOfWorkers": 7,
            }
        },
        "configurations": [],
        "physicalEndpoints": [],
    }

    mock_glue_client = MagicMock()
    mock_session_cls.return_value.client.return_value = mock_glue_client
    mock_glue_client.create_session.return_value = {"Session": {"Id": "sess-mix"}}
    mock_glue_client.get_session.return_value = {"Session": {"Status": "READY"}}
    mock_glue_client.get_session_endpoint.return_value = {
        "SparkConnect": {"Url": "sc://ep", "AuthToken": "t", "AuthTokenExpirationTime": 123}
    }

    # Only override numberOfWorkers; workerType/glueVersion should come from connection.
    mgr = GlueSparkSessionManager(
        connection=conn,
        config=ClientConfig(overrides={"glue": {"numberOfWorkers": 50}}),
    )
    mgr._lazy_init()
    mgr._start_glue_session()

    create_call = mock_glue_client.create_session.call_args
    assert create_call[1]["NumberOfWorkers"] == 50  # user override
    assert create_call[1]["WorkerType"] == "G.4X"  # from connection
    assert create_call[1]["GlueVersion"] == "5.1"  # from connection


@patch("boto3.client")
@patch("boto3.Session")
def test_start_glue_session_override_guards_still_apply(
    mock_session_cls, mock_boto_client, mock_internal_utils
):
    """Ensure version floor (5.1) and idle-timeout cap (15) apply to user overrides too."""
    conn = MagicMock()
    conn._Connection__connection_data = {
        "props": {"sparkGlueProperties": {"glueVersion": "5.1"}},
        "configurations": [],
        "physicalEndpoints": [],
    }

    mock_glue_client = MagicMock()
    mock_session_cls.return_value.client.return_value = mock_glue_client
    mock_glue_client.create_session.return_value = {"Session": {"Id": "sess-guard"}}
    mock_glue_client.get_session.return_value = {"Session": {"Status": "READY"}}
    mock_glue_client.get_session_endpoint.return_value = {
        "SparkConnect": {"Url": "sc://ep", "AuthToken": "t", "AuthTokenExpirationTime": 123}
    }

    # User asks for an unsupported version and an over-long idle timeout.
    mgr = GlueSparkSessionManager(
        connection=conn,
        config=ClientConfig(overrides={"glue": {"glueVersion": "4.0", "idleTimeout": 120}}),
    )
    mgr._lazy_init()
    mgr._start_glue_session()

    create_call = mock_glue_client.create_session.call_args
    # Version floored to 5.1, idle timeout capped at 15.
    assert create_call[1]["GlueVersion"] == "5.1"
    assert create_call[1]["IdleTimeout"] == 15


@patch("boto3.client")
@patch("boto3.Session")
def test_start_glue_session_optional_fields_omitted_by_default(
    mock_session_cls, mock_boto_client, mock_internal_utils
):
    """maxCapacity/securityConfiguration/timeout are absent from CreateSession when unset."""
    conn = MagicMock()
    conn._Connection__connection_data = {
        "props": {"sparkGlueProperties": {"glueVersion": "5.1"}},
        "configurations": [],
        "physicalEndpoints": [],
    }

    mock_glue_client = MagicMock()
    mock_session_cls.return_value.client.return_value = mock_glue_client
    mock_glue_client.create_session.return_value = {"Session": {"Id": "sess-def"}}
    mock_glue_client.get_session.return_value = {"Session": {"Status": "READY"}}
    mock_glue_client.get_session_endpoint.return_value = {
        "SparkConnect": {"Url": "sc://ep", "AuthToken": "t", "AuthTokenExpirationTime": 123}
    }

    mgr = GlueSparkSessionManager(connection=conn)
    mgr._lazy_init()
    mgr._start_glue_session()

    create_call = mock_glue_client.create_session.call_args
    assert "MaxCapacity" not in create_call[1]
    assert "SecurityConfiguration" not in create_call[1]
    assert "Timeout" not in create_call[1]
    # Worker-based sizing still present when maxCapacity is unset.
    assert create_call[1]["WorkerType"] == "G.1X"
    assert create_call[1]["NumberOfWorkers"] == 10


@patch("boto3.client")
@patch("boto3.Session")
def test_start_glue_session_passes_security_config_and_timeout(
    mock_session_cls, mock_boto_client, mock_internal_utils
):
    """securityConfiguration and timeout overrides flow into CreateSession."""
    conn = MagicMock()
    conn._Connection__connection_data = {
        "props": {"sparkGlueProperties": {"glueVersion": "5.1"}},
        "configurations": [],
        "physicalEndpoints": [],
    }

    mock_glue_client = MagicMock()
    mock_session_cls.return_value.client.return_value = mock_glue_client
    mock_glue_client.create_session.return_value = {"Session": {"Id": "sess-sec"}}
    mock_glue_client.get_session.return_value = {"Session": {"Status": "READY"}}
    mock_glue_client.get_session_endpoint.return_value = {
        "SparkConnect": {"Url": "sc://ep", "AuthToken": "t", "AuthTokenExpirationTime": 123}
    }

    mgr = GlueSparkSessionManager(
        connection=conn,
        config=ClientConfig(
            overrides={
                "glue": {
                    "securityConfiguration": "my-sec-config",
                    "timeout": 480,
                }
            }
        ),
    )
    mgr._lazy_init()
    mgr._start_glue_session()

    create_call = mock_glue_client.create_session.call_args
    assert create_call[1]["SecurityConfiguration"] == "my-sec-config"
    assert create_call[1]["Timeout"] == 480
    # Worker sizing untouched when maxCapacity not set.
    assert create_call[1]["WorkerType"] == "G.1X"
    assert create_call[1]["NumberOfWorkers"] == 10


@patch("boto3.client")
@patch("boto3.Session")
def test_start_glue_session_max_capacity_excludes_worker_fields(
    mock_session_cls, mock_boto_client, mock_internal_utils
):
    """maxCapacity is mutually exclusive with WorkerType/NumberOfWorkers in CreateSession."""
    conn = MagicMock()
    conn._Connection__connection_data = {
        "props": {
            "sparkGlueProperties": {
                "glueVersion": "5.1",
                "workerType": "G.1X",
                "numberOfWorkers": 10,
            }
        },
        "configurations": [],
        "physicalEndpoints": [],
    }

    mock_glue_client = MagicMock()
    mock_session_cls.return_value.client.return_value = mock_glue_client
    mock_glue_client.create_session.return_value = {"Session": {"Id": "sess-cap"}}
    mock_glue_client.get_session.return_value = {"Session": {"Status": "READY"}}
    mock_glue_client.get_session_endpoint.return_value = {
        "SparkConnect": {"Url": "sc://ep", "AuthToken": "t", "AuthTokenExpirationTime": 123}
    }

    mgr = GlueSparkSessionManager(
        connection=conn,
        config=ClientConfig(overrides={"glue": {"maxCapacity": 8}}),
    )
    mgr._lazy_init()
    mgr._start_glue_session()

    create_call = mock_glue_client.create_session.call_args
    assert create_call[1]["MaxCapacity"] == 8.0
    assert "WorkerType" not in create_call[1]
    assert "NumberOfWorkers" not in create_call[1]


def test_resolve_session_field_precedence(manager):
    """Ensure _resolve_session_field honors user > connection > default ordering."""
    manager._glue_session_overrides = {"workerType": "G.8X"}
    manager._glue_props = {"workerType": "G.1X", "numberOfWorkers": 4}

    # User override wins.
    assert manager._resolve_session_field("workerType", "G.025X") == "G.8X"
    # Falls back to connection prop.
    assert manager._resolve_session_field("numberOfWorkers", 10) == 4
    # Falls back to default when neither present.
    assert manager._resolve_session_field("idleTimeout", 15) == 15


@patch("boto3.client")
@patch("boto3.Session")
def test_lazy_init_loads_custom_botocore_model(
    mock_session_cls, mock_boto_client, mock_internal_utils
):
    """Ensure _lazy_init loads custom Glue service model when model path exists."""
    conn = MagicMock()
    conn._Connection__connection_data = {
        "props": {"sparkGlueProperties": {}},
        "configurations": [],
        "physicalEndpoints": [],
    }

    mock_session_cls.return_value.client.return_value = MagicMock()

    mgr = GlueSparkSessionManager(connection=conn)

    with patch("os.path.isdir", return_value=True), patch(
        "botocore.loaders.Loader"
    ) as mock_loader, patch("botocore.session.get_session") as mock_bc_session:
        mock_bc_session.return_value = MagicMock()
        mgr._lazy_init()

    # Verify custom loader was created with extra search paths
    mock_loader.assert_called_once()
    assert "boto3_models" in mock_loader.call_args[1]["extra_search_paths"][0]
