"""Tests for EMRServerlessSparkSessionManager."""

import sys
from unittest.mock import MagicMock, Mock, patch

import pytest

# Mock Project class before any imports to prevent Domain ID error
with patch("sagemaker_studio.Project"):

    # Mock pyspark before importing  # noqa: E402
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

    # Mock the interceptors module to avoid importing the actual interceptors
    mock_interceptors = Mock()
    mock_interceptors.CustomChannelBuilder = Mock()
    sys.modules["sagemaker_studio.utils.spark.session.emr_serverless.interceptors"] = (
        mock_interceptors
    )

    from sagemaker_studio.utils.spark.session.emr_serverless.emr_serverless_spark_session_manager import (
        EMRServerlessSparkSessionManager,
    )


@pytest.fixture
def mock_boto3_clients():
    """Mocks boto3 clients for EMR Serverless and STS."""
    emr_client = MagicMock()
    sts_client = MagicMock()
    sts_client.get_caller_identity.return_value = {
        "UserId": "abc:random-user-id",
        "Account": "1234567890",
    }

    with patch("boto3.client") as mock_boto_client:
        mock_boto_client.side_effect = lambda service_name, **kwargs: (
            emr_client if service_name == "emr-serverless" else sts_client
        )
        yield emr_client, sts_client


@pytest.fixture
def mock_internal_utils():
    """Mocks InternalUtils and Project on the EMR-S module."""
    mock_conn = MagicMock()
    mock_conn.data.compute_arn = "arn:aws:emr-serverless:us-west-2:1234567890:/applications/app-123"
    mock_conn._Connection__connection_data = {
        "props": {
            "sparkEmrProperties": {
                "computeArn": "arn:aws:emr-serverless:us-west-2:1234567890:/applications/app-123",
                "runtimeRole": "arn:aws:iam::1234567890:role/emr-runtime-role",
            }
        },
        "configurations": [],
    }

    with patch(
        "sagemaker_studio.utils.spark.session.emr_serverless.emr_serverless_spark_session_manager.InternalUtils"
    ) as mock_utils, patch(
        "sagemaker_studio.utils.spark.session.emr_serverless.emr_serverless_spark_session_manager.Project"
    ) as mock_project:
        mock_utils.return_value._get_domain_region.return_value = "us-west-2"
        mock_utils.return_value._get_account_id.return_value = "1234567890"
        mock_utils.return_value._get_user_id.return_value = "test-user"
        mock_utils.return_value._get_domain_id.return_value = "dom-123"
        mock_project.return_value.connection.return_value = mock_conn
        mock_project.return_value.iam_role = "arn:aws:iam::1234567890:role/test-role"
        mock_project.return_value.id = "proj-123"
        mock_project.return_value._sagemaker_studio_api = MagicMock()
        yield mock_utils, mock_project


@pytest.fixture
def manager(mock_boto3_clients, mock_internal_utils):
    """Create a testable EMRServerlessSparkSessionManager with mocks injected."""
    mgr = EMRServerlessSparkSessionManager(connection_name="test_connection")
    return mgr


@patch("boto3.client")
@patch("boto3.Session")
def test_lazy_init_creates_clients(mock_session_cls, mock_boto_client, manager):
    """Ensure _lazy_init sets up EMR-S client and extracts application_id."""
    mock_emr_client = MagicMock()
    mock_session_cls.return_value.client.return_value = mock_emr_client
    mock_sts = MagicMock()
    mock_boto_client.return_value = mock_sts

    manager._lazy_init()

    assert manager.emr_serverless_client is mock_emr_client
    assert manager.application_id == "app-123"


def test_lazy_init_raises_without_connection_or_name():
    """Ensure _lazy_init raises ValueError when no connection or connection_name provided."""
    mgr = EMRServerlessSparkSessionManager()
    with patch(
        "sagemaker_studio.utils.spark.session.emr_serverless.emr_serverless_spark_session_manager.InternalUtils"
    ) as mock_utils, patch(
        "sagemaker_studio.utils.spark.session.emr_serverless.emr_serverless_spark_session_manager.Project"
    ), patch(
        "boto3.client"
    ), patch(
        "boto3.Session"
    ):
        mock_utils.return_value._get_domain_region.return_value = "us-west-2"
        with pytest.raises(ValueError, match="requires a connection or connection_name"):
            mgr._lazy_init()


@patch(
    "sagemaker_studio.utils.spark.session.emr_serverless.emr_serverless_spark_session_manager._SparkSession"
)
@patch(
    "sagemaker_studio.utils.spark.session.emr_serverless.emr_serverless_spark_session_manager.CustomChannelBuilder"
)
def test_create_starts_session(mock_channel_builder, mock_spark_session, manager):
    """Ensure create() builds a SparkSession."""
    manager._lazy_init = MagicMock()
    manager._start_emr_serverless_session = MagicMock(
        return_value=(
            "sess-1",
            "sc://endpoint",
            {"authToken": "tok", "authTokenExpiresAt": None},
        )
    )

    builder = MagicMock()
    mock_spark_session.builder.channelBuilder.return_value = builder
    builder.appName.return_value = builder
    builder.getOrCreate.return_value = "mock_spark"

    session = manager.create()

    assert session == "mock_spark"
    assert manager.emr_serverless_session_id == "sess-1"
    mock_channel_builder.assert_called_once()
    builder.getOrCreate.assert_called_once()


def test_create_returns_existing_session(manager):
    """Ensure create() returns existing session without re-creating."""
    manager._spark_session = "existing_session"
    assert manager.create() == "existing_session"


@patch.object(EMRServerlessSparkSessionManager, "stop")
def test_create_calls_stop_on_failure(mock_stop, manager):
    """Ensure create() calls stop() to clean up orphaned sessions on failure."""
    manager._lazy_init = MagicMock(side_effect=RuntimeError("init failed"))

    with pytest.raises(RuntimeError, match="init failed"):
        manager.create()

    mock_stop.assert_called_once()


def test_construct_spark_endpoint_url(manager):
    """Ensure spark endpoint URL is properly constructed."""
    response = {"endpoint": "https://emr.aws.com/session", "authToken": "XYZ"}
    url = manager._construct_spark_endpoint_url(response)

    assert url.startswith("sc://emr.aws.com")
    assert "x-aws-proxy-auth=XYZ" in url
    assert ":443/" in url


def test_wait_for_session_ready(manager, mock_boto3_clients):
    """Ensure wait returns True when session reaches STARTED state."""
    emr_client, _ = mock_boto3_clients
    emr_client.get_session.return_value = {"session": {"state": "STARTED"}}
    manager.emr_serverless_client = emr_client

    result = manager._wait_for_emr_serverless_session(
        "app-1", "sess-1", timeout=5, poll_interval=0.1
    )
    assert result is True


def test_wait_for_session_failure(manager, mock_boto3_clients):
    """Ensure wait raises RuntimeError on FAILED state."""
    emr_client, _ = mock_boto3_clients
    emr_client.get_session.return_value = {
        "session": {"state": "FAILED", "stateDetails": "Out of memory"}
    }
    manager.emr_serverless_client = emr_client

    with pytest.raises(RuntimeError):
        manager._wait_for_emr_serverless_session("app-1", "sess-1", timeout=5, poll_interval=0.1)


def test_wait_for_session_timeout(manager, mock_boto3_clients):
    """Ensure wait raises RuntimeError when session doesn't become ready within timeout."""
    emr_client, _ = mock_boto3_clients
    emr_client.get_session.return_value = {"session": {"state": "STARTING"}}
    manager.emr_serverless_client = emr_client

    with pytest.raises(RuntimeError, match="was not ready within the session start timeout"):
        manager._wait_for_emr_serverless_session("app-1", "sess-1", timeout=0.1, poll_interval=0.05)


def test_terminate_session_calls_aws(manager, mock_boto3_clients):
    """Ensure terminate calls EMR-S client."""
    emr_client, _ = mock_boto3_clients
    manager.emr_serverless_client = emr_client
    manager.application_id = "app-1"

    manager._terminate_emr_serverless_session("sess-1")
    emr_client.terminate_session.assert_called_once_with(applicationId="app-1", sessionId="sess-1")


@patch.object(EMRServerlessSparkSessionManager, "_terminate_emr_serverless_session")
def test_stop_stops_spark_before_emr_session(mock_terminate, manager):
    """Ensure stop() stops Spark session first (graceful gRPC close), then terminates EMR-S."""
    mock_spark = MagicMock()
    call_order = []
    mock_spark.stop.side_effect = lambda: call_order.append("spark_stop")
    mock_terminate.side_effect = lambda sid: call_order.append("emr_terminate")

    manager._spark_session = mock_spark
    manager.emr_serverless_session_id = "sess-123"

    manager.stop()

    assert call_order == ["spark_stop", "emr_terminate"]
    assert manager._spark_session is None
    assert manager.emr_serverless_session_id is None


@patch.object(EMRServerlessSparkSessionManager, "_terminate_emr_serverless_session")
def test_stop_terminates_emr_even_if_spark_stop_fails(mock_terminate, manager):
    """Ensure EMR-S session is terminated even if Spark session stop raises."""
    mock_spark = MagicMock()
    mock_spark.stop.side_effect = Exception("gRPC error")
    manager._spark_session = mock_spark
    manager.emr_serverless_session_id = "sess-123"

    manager.stop()

    mock_terminate.assert_called_once_with("sess-123")
    assert manager._spark_session is None
    assert manager.emr_serverless_session_id is None


def test_start_session_assigns_id_early(manager, mock_boto3_clients):
    """Ensure session_id is assigned to self before wait/endpoint calls (resource leak fix)."""
    emr_client, sts_client = mock_boto3_clients
    manager.emr_serverless_client = emr_client
    manager.sts_client = sts_client
    manager.application_id = "app-1"
    manager.project = MagicMock()
    manager.project.id = "proj-123"
    manager.emr_serverless_runtime_role = "arn:aws:iam::123:role/role"
    manager.connection_spark_configs = {}
    manager.resolved_connection_name = "test_connection"

    emr_client.start_session.return_value = {"sessionId": "sess-early"}
    emr_client.get_application.return_value = {
        "application": {"state": "STARTED", "releaseLabel": "emr-7.5.0"}
    }

    # Make _wait raise to simulate timeout — session_id should already be assigned
    with patch.object(
        manager, "_get_user_id_account_id", return_value=("test-user", "1234567890")
    ), patch(
        "sagemaker_studio.utils.spark.session.emr_serverless.emr_serverless_spark_session_manager.generate_spark_configs",
        return_value={},
    ), patch.object(
        manager, "_wait_for_emr_serverless_session", side_effect=RuntimeError("timeout")
    ):
        with pytest.raises(RuntimeError, match="timeout"):
            manager._start_emr_serverless_session("app-1")

    assert manager.emr_serverless_session_id == "sess-early"


def test_get_session_id(manager):
    """Ensure get_session_id returns the stored session id."""
    manager.emr_serverless_session_id = "sess-abc"
    assert manager.get_session_id() == "sess-abc"


def test_get_session_id_none(manager):
    """Ensure get_session_id returns None when no session exists."""
    assert manager.get_session_id() is None


def test_get_execution_role_arn_uses_runtime_role(manager):
    """Ensure _get_execution_role_arn returns runtimeRole when available."""
    manager.emr_serverless_runtime_role = "arn:aws:iam::123:role/runtime"
    assert manager._get_execution_role_arn() == "arn:aws:iam::123:role/runtime"


def test_get_execution_role_arn_falls_back_to_project(manager):
    """Ensure _get_execution_role_arn falls back to project IAM role when runtimeRole is empty."""
    manager.emr_serverless_runtime_role = ""
    manager.project = MagicMock()
    manager.project.iam_role = "arn:aws:iam::123:role/project-role"
    assert manager._get_execution_role_arn() == "arn:aws:iam::123:role/project-role"


def test_is_release_at_least_true():
    """Ensure _is_release_at_least returns True for equal or greater releases."""
    assert EMRServerlessSparkSessionManager._is_release_at_least("emr-7.8.0", "emr-7.5.0") is True
    assert EMRServerlessSparkSessionManager._is_release_at_least("emr-7.5.0", "emr-7.5.0") is True
    assert EMRServerlessSparkSessionManager._is_release_at_least("emr-8.0.0", "emr-7.5.0") is True


def test_is_release_at_least_false():
    """Ensure _is_release_at_least returns False for older releases."""
    assert EMRServerlessSparkSessionManager._is_release_at_least("emr-7.4.0", "emr-7.5.0") is False


def test_is_release_at_least_invalid():
    """Ensure _is_release_at_least returns False for malformed labels."""
    assert EMRServerlessSparkSessionManager._is_release_at_least("invalid", "emr-7.5.0") is False
    assert EMRServerlessSparkSessionManager._is_release_at_least("", "emr-7.5.0") is False


def test_user_msg(capsys):
    """Ensure _user_msg prints to stdout."""
    EMRServerlessSparkSessionManager._user_msg("hello")
    captured = capsys.readouterr()
    assert "hello" in captured.out


def test_is_compatibility_mode_enabled_true():
    """Ensure _is_compatibility_mode_enabled returns True when LF is explicitly false."""
    app = {
        "runtimeConfiguration": [
            {
                "classification": "spark-defaults",
                "properties": {"spark.emr-serverless.lakeformation.enabled": "false"},
            }
        ]
    }
    assert EMRServerlessSparkSessionManager._is_compatibility_mode_enabled(app) is True


def test_is_compatibility_mode_enabled_false_when_lf_enabled():
    """Ensure _is_compatibility_mode_enabled returns False when LF is true."""
    app = {
        "runtimeConfiguration": [
            {
                "classification": "spark-defaults",
                "properties": {"spark.emr-serverless.lakeformation.enabled": "true"},
            }
        ]
    }
    assert EMRServerlessSparkSessionManager._is_compatibility_mode_enabled(app) is False


def test_is_compatibility_mode_enabled_no_runtime_config():
    """Ensure _is_compatibility_mode_enabled returns False when runtimeConfiguration is None."""
    assert EMRServerlessSparkSessionManager._is_compatibility_mode_enabled({}) is False
    assert (
        EMRServerlessSparkSessionManager._is_compatibility_mode_enabled(
            {"runtimeConfiguration": None}
        )
        is False
    )


def test_is_compatibility_mode_enabled_no_spark_defaults():
    """Ensure _is_compatibility_mode_enabled returns False when spark-defaults not present."""
    app = {"runtimeConfiguration": [{"classification": "other", "properties": {}}]}
    assert EMRServerlessSparkSessionManager._is_compatibility_mode_enabled(app) is False


def test_is_compatibility_mode_enabled_no_properties():
    """Ensure _is_compatibility_mode_enabled returns False when properties is None."""
    app = {"runtimeConfiguration": [{"classification": "spark-defaults", "properties": None}]}
    assert EMRServerlessSparkSessionManager._is_compatibility_mode_enabled(app) is False


def test_is_compatibility_mode_enabled_lf_key_absent():
    """Ensure _is_compatibility_mode_enabled returns True when LF key is absent (defaults to false)."""
    app = {
        "runtimeConfiguration": [
            {"classification": "spark-defaults", "properties": {"some.other.key": "value"}}
        ]
    }
    assert EMRServerlessSparkSessionManager._is_compatibility_mode_enabled(app) is True


def test_is_fta_supported_true():
    """Ensure _is_fta_supported returns True when compat mode + release >= 7.8.0."""
    app = {
        "releaseLabel": "emr-7.8.0",
        "runtimeConfiguration": [
            {
                "classification": "spark-defaults",
                "properties": {"spark.emr-serverless.lakeformation.enabled": "false"},
            }
        ],
    }
    assert EMRServerlessSparkSessionManager._is_fta_supported(app) is True


def test_is_fta_supported_false_no_compat():
    """Ensure _is_fta_supported returns False when compat mode is off."""
    app = {
        "releaseLabel": "emr-7.8.0",
        "runtimeConfiguration": [
            {
                "classification": "spark-defaults",
                "properties": {"spark.emr-serverless.lakeformation.enabled": "true"},
            }
        ],
    }
    assert EMRServerlessSparkSessionManager._is_fta_supported(app) is False


def test_is_fta_supported_false_old_release():
    """Ensure _is_fta_supported returns False when release < 7.8.0."""
    app = {
        "releaseLabel": "emr-7.5.0",
        "runtimeConfiguration": [
            {
                "classification": "spark-defaults",
                "properties": {"spark.emr-serverless.lakeformation.enabled": "false"},
            }
        ],
    }
    assert EMRServerlessSparkSessionManager._is_fta_supported(app) is False


def test_is_fta_supported_false_no_release_label():
    """Ensure _is_fta_supported returns False when releaseLabel is empty."""
    app = {
        "releaseLabel": "",
        "runtimeConfiguration": [
            {
                "classification": "spark-defaults",
                "properties": {"spark.emr-serverless.lakeformation.enabled": "false"},
            }
        ],
    }
    assert EMRServerlessSparkSessionManager._is_fta_supported(app) is False


def test_get_compatibility_mode_configs():
    """Ensure _get_compatibility_mode_configs returns expected keys."""
    configs = EMRServerlessSparkSessionManager._get_compatibility_mode_configs()
    assert "spark.hadoop.fs.s3.credentialsResolverClass" in configs
    assert "spark.sql.catalog.spark_catalog.glue.lakeformation-enabled" in configs
    assert len(configs) == 7


def test_get_s3_access_grants_configs_enabled(manager):
    """Ensure _get_s3_access_grants_configs returns configs when S3AG is enabled."""
    manager.project = MagicMock()
    mock_api = manager.project._sagemaker_studio_api.project_api
    mock_api.get_project_default_environment.return_value = {
        "provisionedResources": [
            {"name": "enableS3AccessGrantsForTools", "value": "true"},
        ]
    }
    with patch(
        "sagemaker_studio.utils.spark.session.emr_serverless.emr_serverless_spark_session_manager.InternalUtils"
    ) as mock_utils:
        mock_utils.return_value._get_domain_id.return_value = "dom-123"
        configs = manager._get_s3_access_grants_configs()

    assert configs["spark.hadoop.fs.s3.s3AccessGrants.enabled"] == "true"
    assert configs["spark.hadoop.fs.s3.s3AccessGrants.fallbackToIAM"] == "true"


def test_get_s3_access_grants_configs_disabled(manager):
    """Ensure _get_s3_access_grants_configs returns empty when S3AG is disabled."""
    manager.project = MagicMock()
    mock_api = manager.project._sagemaker_studio_api.project_api
    mock_api.get_project_default_environment.return_value = {
        "provisionedResources": [
            {"name": "enableS3AccessGrantsForTools", "value": "false"},
        ]
    }
    with patch(
        "sagemaker_studio.utils.spark.session.emr_serverless.emr_serverless_spark_session_manager.InternalUtils"
    ) as mock_utils:
        mock_utils.return_value._get_domain_id.return_value = "dom-123"
        configs = manager._get_s3_access_grants_configs()

    assert configs == {}


def test_get_s3_access_grants_configs_exception(manager):
    """Ensure _get_s3_access_grants_configs returns empty on exception."""
    manager.project = MagicMock()
    manager.project._sagemaker_studio_api.project_api.get_project_default_environment.side_effect = Exception(
        "API error"
    )
    with patch(
        "sagemaker_studio.utils.spark.session.emr_serverless.emr_serverless_spark_session_manager.InternalUtils"
    ) as mock_utils:
        mock_utils.return_value._get_domain_id.return_value = "dom-123"
        configs = manager._get_s3_access_grants_configs()

    assert configs == {}


def test_ensure_application_started_already_started(manager, mock_boto3_clients):
    """Ensure _ensure_application_started returns immediately when app is STARTED."""
    emr_client, _ = mock_boto3_clients
    manager.emr_serverless_client = emr_client
    emr_client.get_application.return_value = {
        "application": {"state": "STARTED", "releaseLabel": "emr-7.5.0"}
    }

    result = manager._ensure_application_started("app-1")
    assert result["state"] == "STARTED"


def test_ensure_application_started_from_stopped(manager, mock_boto3_clients):
    """Ensure _ensure_application_started starts a STOPPED application."""
    emr_client, _ = mock_boto3_clients
    manager.emr_serverless_client = emr_client

    # First call: STOPPED, then after start_application + wait: STARTED
    emr_client.get_application.side_effect = [
        {"application": {"state": "STOPPED", "releaseLabel": "emr-7.5.0"}},
        # _wait_for_application_state polls
        {"application": {"state": "STARTED", "releaseLabel": "emr-7.5.0"}},
        # re-fetch after STARTED
        {"application": {"state": "STARTED", "releaseLabel": "emr-7.5.0"}},
    ]

    result = manager._ensure_application_started("app-1", timeout=5, poll_interval=0.01)
    assert result["state"] == "STARTED"
    emr_client.start_application.assert_called_once_with(applicationId="app-1")


def test_ensure_application_started_from_transient(manager, mock_boto3_clients):
    """Ensure _ensure_application_started waits through transient states then starts if needed."""
    emr_client, _ = mock_boto3_clients
    manager.emr_serverless_client = emr_client

    # STARTING -> STARTED
    emr_client.get_application.side_effect = [
        {"application": {"state": "STARTING", "releaseLabel": "emr-7.5.0"}},
        # _wait exits transient
        {"application": {"state": "STARTED", "releaseLabel": "emr-7.5.0"}},
        # re-fetch
        {"application": {"state": "STARTED", "releaseLabel": "emr-7.5.0"}},
    ]

    result = manager._ensure_application_started("app-1", timeout=5, poll_interval=0.01)
    assert result["state"] == "STARTED"


def test_ensure_application_started_unexpected_state(manager, mock_boto3_clients):
    """Ensure _ensure_application_started raises on unexpected terminal state."""
    emr_client, _ = mock_boto3_clients
    manager.emr_serverless_client = emr_client

    emr_client.get_application.return_value = {
        "application": {"state": "TERMINATED", "releaseLabel": "emr-7.5.0"}
    }

    with pytest.raises(RuntimeError, match="unexpected state"):
        manager._ensure_application_started("app-1")


def test_wait_for_application_state_exits(manager, mock_boto3_clients):
    """Ensure _wait_for_application_state returns when state exits waiting set."""
    emr_client, _ = mock_boto3_clients
    manager.emr_serverless_client = emr_client

    emr_client.get_application.side_effect = [
        {"application": {"state": "STARTING"}},
        {"application": {"state": "STARTED"}},
    ]

    result = manager._wait_for_application_state(
        "app-1", ("STARTING",), timeout=5, poll_interval=0.01
    )
    assert result == "STARTED"


def test_wait_for_application_state_timeout(manager, mock_boto3_clients):
    """Ensure _wait_for_application_state raises on timeout."""
    emr_client, _ = mock_boto3_clients
    manager.emr_serverless_client = emr_client

    emr_client.get_application.return_value = {"application": {"state": "STARTING"}}

    with pytest.raises(RuntimeError, match="Timed out"):
        manager._wait_for_application_state("app-1", ("STARTING",), timeout=0.1, poll_interval=0.05)


def test_wait_for_emr_serverless_session_reraises_runtime_error(manager, mock_boto3_clients):
    """Ensure RuntimeError from FAILED state is re-raised without wrapping."""
    emr_client, _ = mock_boto3_clients
    emr_client.get_session.return_value = {
        "session": {"state": "TERMINATED", "stateDetails": "Killed"}
    }
    manager.emr_serverless_client = emr_client

    with pytest.raises(RuntimeError, match="Killed"):
        manager._wait_for_emr_serverless_session("app-1", "sess-1", timeout=5, poll_interval=0.1)


def test_wait_for_emr_serverless_session_generic_exception(manager, mock_boto3_clients):
    """Ensure generic exceptions from get_session are re-raised."""
    emr_client, _ = mock_boto3_clients
    emr_client.get_session.side_effect = ConnectionError("network down")
    manager.emr_serverless_client = emr_client

    with pytest.raises(ConnectionError, match="network down"):
        manager._wait_for_emr_serverless_session("app-1", "sess-1", timeout=5, poll_interval=0.1)


def test_terminate_session_raises_on_error(manager, mock_boto3_clients):
    """Ensure _terminate_emr_serverless_session re-raises exceptions."""
    emr_client, _ = mock_boto3_clients
    emr_client.terminate_session.side_effect = Exception("terminate failed")
    manager.emr_serverless_client = emr_client
    manager.application_id = "app-1"

    with pytest.raises(Exception, match="terminate failed"):
        manager._terminate_emr_serverless_session("sess-1")


@patch("boto3.client")
@patch("boto3.Session")
def test_lazy_init_with_endpoint_override(mock_session_cls, mock_boto_client, mock_internal_utils):
    """Ensure _lazy_init passes endpoint_url when configured."""
    mock_utils, mock_project = mock_internal_utils
    mock_emr_client = MagicMock()
    mock_session_cls.return_value.client.return_value = mock_emr_client

    mgr = EMRServerlessSparkSessionManager(
        connection_name="test",
        config=MagicMock(overrides={"emr-serverless": {"endpoint_url": "https://custom.endpoint"}}),
    )
    mgr._lazy_init()

    # Verify endpoint_url was passed to the client constructor
    call_kwargs = mock_session_cls.return_value.client.call_args
    assert call_kwargs[1].get("endpoint_url") == "https://custom.endpoint"


@patch("boto3.client")
@patch("boto3.Session")
def test_lazy_init_with_pre_resolved_connection(mock_session_cls, mock_boto_client):
    """Ensure _lazy_init uses pre-resolved connection when provided."""
    mock_conn = MagicMock()
    mock_conn.data.compute_arn = "arn:aws:emr-serverless:us-west-2:123:/applications/app-pre"
    mock_conn._Connection__connection_data = {
        "props": {"sparkEmrProperties": {"runtimeRole": "arn:aws:iam::123:role/rt"}},
        "configurations": [],
    }
    mock_conn.name = "pre-resolved"

    mock_emr_client = MagicMock()
    mock_session_cls.return_value.client.return_value = mock_emr_client

    with patch(
        "sagemaker_studio.utils.spark.session.emr_serverless.emr_serverless_spark_session_manager.InternalUtils"
    ) as mu, patch(
        "sagemaker_studio.utils.spark.session.emr_serverless.emr_serverless_spark_session_manager.Project"
    ) as mp:
        mu.return_value._get_domain_region.return_value = "us-west-2"
        mp.return_value.id = "proj-1"

        mgr = EMRServerlessSparkSessionManager(connection=mock_conn)
        mgr._lazy_init()

    assert mgr.application_id == "app-pre"
    assert mgr.resolved_connection_name == "pre-resolved"


@patch("boto3.client")
@patch("boto3.Session")
def test_lazy_init_no_compute_arn_raises(mock_session_cls, mock_boto_client):
    """Ensure _lazy_init raises ValueError when compute_arn is missing."""
    mock_conn = MagicMock()
    mock_conn.data.compute_arn = None
    mock_conn._Connection__connection_data = {
        "props": {"sparkEmrProperties": {}},
        "configurations": [],
    }

    mock_session_cls.return_value.client.return_value = MagicMock()

    with patch(
        "sagemaker_studio.utils.spark.session.emr_serverless.emr_serverless_spark_session_manager.InternalUtils"
    ) as mu, patch(
        "sagemaker_studio.utils.spark.session.emr_serverless.emr_serverless_spark_session_manager.Project"
    ):
        mu.return_value._get_domain_region.return_value = "us-west-2"

        mgr = EMRServerlessSparkSessionManager(connection=mock_conn)
        with pytest.raises(ValueError, match="compute_arn"):
            mgr._lazy_init()


@patch("boto3.client")
@patch("boto3.Session")
def test_lazy_init_connection_spark_configs(mock_session_cls, mock_boto_client):
    """Ensure _lazy_init extracts SparkConfiguration from connection configurations."""
    mock_conn = MagicMock()
    mock_conn.data.compute_arn = "arn:aws:emr-serverless:us-west-2:123:/applications/app-cfg"
    mock_conn._Connection__connection_data = {
        "props": {"sparkEmrProperties": {"runtimeRole": "arn:aws:iam::123:role/rt"}},
        "configurations": [
            {"classification": "SparkConfiguration", "properties": {"spark.custom.key": "val"}},
        ],
    }
    mock_conn.name = "cfg-conn"

    mock_session_cls.return_value.client.return_value = MagicMock()

    with patch(
        "sagemaker_studio.utils.spark.session.emr_serverless.emr_serverless_spark_session_manager.InternalUtils"
    ) as mu, patch(
        "sagemaker_studio.utils.spark.session.emr_serverless.emr_serverless_spark_session_manager.Project"
    ) as mp:
        mu.return_value._get_domain_region.return_value = "us-west-2"
        mp.return_value.id = "proj-1"

        mgr = EMRServerlessSparkSessionManager(connection=mock_conn)
        mgr._lazy_init()

    assert mgr.connection_spark_configs == {"spark.custom.key": "val"}


def test_start_session_full_flow_fta_supported(manager, mock_boto3_clients):
    """Ensure _start_emr_serverless_session applies FTA configs when supported."""
    emr_client, _ = mock_boto3_clients
    manager.emr_serverless_client = emr_client
    manager.application_id = "app-1"
    manager.project = MagicMock()
    manager.project.id = "proj-123"
    manager.emr_serverless_runtime_role = "arn:aws:iam::123:role/role"
    manager.connection_spark_configs = {}
    manager.resolved_connection_name = "test_connection"

    fta_app = {
        "state": "STARTED",
        "releaseLabel": "emr-7.8.0",
        "runtimeConfiguration": [
            {
                "classification": "spark-defaults",
                "properties": {"spark.emr-serverless.lakeformation.enabled": "false"},
            }
        ],
    }

    emr_client.start_session.return_value = {"sessionId": "sess-fta"}
    emr_client.get_session.return_value = {"session": {"state": "STARTED"}}
    emr_client.get_session_endpoint.return_value = {
        "endpoint": "https://emr.aws.com/session",
        "authToken": "tok",
        "authTokenExpiresAt": None,
    }

    with patch.object(
        manager, "_get_user_id_account_id", return_value=("test-user", "1234567890")
    ), patch.object(manager, "_ensure_application_started", return_value=fta_app), patch(
        "sagemaker_studio.utils.spark.session.emr_serverless.emr_serverless_spark_session_manager.generate_spark_configs",
        return_value={},
    ), patch.object(
        manager, "_get_s3_access_grants_configs", return_value={}
    ):
        session_id, url, resp = manager._start_emr_serverless_session("app-1")

    assert session_id == "sess-fta"
    assert url.startswith("sc://")
    # Verify FTA configs were applied (check the start_session call)
    call_kwargs = emr_client.start_session.call_args
    spark_props = call_kwargs[1]["configurationOverrides"]["runtimeConfiguration"][0]["properties"]
    assert "spark.hadoop.fs.s3.credentialsResolverClass" in spark_props


def test_start_session_full_flow_fta_not_supported(manager, mock_boto3_clients):
    """Ensure _start_emr_serverless_session removes compat configs when FTA not supported."""
    emr_client, _ = mock_boto3_clients
    manager.emr_serverless_client = emr_client
    manager.application_id = "app-1"
    manager.project = MagicMock()
    manager.project.id = "proj-123"
    manager.emr_serverless_runtime_role = "arn:aws:iam::123:role/role"
    manager.connection_spark_configs = {}
    manager.resolved_connection_name = "test_connection"

    non_fta_app = {"state": "STARTED", "releaseLabel": "emr-7.5.0"}

    emr_client.start_session.return_value = {"sessionId": "sess-nofta"}
    emr_client.get_session.return_value = {"session": {"state": "STARTED"}}
    emr_client.get_session_endpoint.return_value = {
        "endpoint": "https://emr.aws.com/session",
        "authToken": "tok",
        "authTokenExpiresAt": None,
    }

    # generate_spark_configs returns compat keys that should be removed
    compat_keys = EMRServerlessSparkSessionManager._get_compatibility_mode_configs()
    initial_configs = dict(compat_keys)  # copy

    with patch.object(
        manager, "_get_user_id_account_id", return_value=("test-user", "1234567890")
    ), patch.object(manager, "_ensure_application_started", return_value=non_fta_app), patch(
        "sagemaker_studio.utils.spark.session.emr_serverless.emr_serverless_spark_session_manager.generate_spark_configs",
        return_value=initial_configs,
    ), patch.object(
        manager, "_get_s3_access_grants_configs", return_value={}
    ):
        session_id, url, resp = manager._start_emr_serverless_session("app-1")

    assert session_id == "sess-nofta"
    call_kwargs = emr_client.start_session.call_args
    spark_props = call_kwargs[1]["configurationOverrides"]["runtimeConfiguration"][0]["properties"]
    # Compat keys should have been removed
    assert "spark.hadoop.fs.s3.credentialsResolverClass" not in spark_props


def test_stop_no_sessions(manager):
    """Ensure stop() works cleanly when no sessions exist."""
    manager._spark_session = None
    manager.emr_serverless_session_id = None
    manager.stop()  # should not raise
    assert manager._spark_session is None
    assert manager.emr_serverless_session_id is None


# --- Tests for spark.dynamicAllocation.executorIdleTimeout ---


def _setup_manager_for_session_start(manager, mock_boto3_clients, connection_spark_configs=None):
    """Helper to set up manager for _start_emr_serverless_session tests."""
    emr_client, _ = mock_boto3_clients
    manager.emr_serverless_client = emr_client
    manager.application_id = "app-1"
    manager.project = MagicMock()
    manager.project.id = "proj-123"
    manager.emr_serverless_runtime_role = "arn:aws:iam::123:role/role"
    manager.connection_spark_configs = connection_spark_configs or {}
    manager.resolved_connection_name = "test_connection"

    emr_client.start_session.return_value = {"sessionId": "sess-idle"}
    emr_client.get_session.return_value = {"session": {"state": "STARTED"}}
    emr_client.get_session_endpoint.return_value = {
        "endpoint": "https://emr.aws.com/session",
        "authToken": "tok",
        "authTokenExpiresAt": None,
    }
    return emr_client


def _get_spark_props_from_start_session(emr_client):
    """Extract spark properties dict from the start_session call."""
    call_kwargs = emr_client.start_session.call_args
    return call_kwargs[1]["configurationOverrides"]["runtimeConfiguration"][0]["properties"]


def test_executor_idle_timeout_default(manager, mock_boto3_clients):
    """Ensure executorIdleTimeout is set to 120s by default."""
    emr_client = _setup_manager_for_session_start(manager, mock_boto3_clients)

    app = {"state": "STARTED", "releaseLabel": "emr-7.5.0"}

    with patch.object(
        manager, "_get_user_id_account_id", return_value=("test-user", "1234567890")
    ), patch.object(manager, "_ensure_application_started", return_value=app), patch(
        "sagemaker_studio.utils.spark.session.emr_serverless.emr_serverless_spark_session_manager.generate_spark_configs",
        return_value={"spark.sql.catalogImplementation": "hive"},
    ), patch.object(
        manager, "_get_s3_access_grants_configs", return_value={}
    ):
        manager._start_emr_serverless_session("app-1")

    spark_props = _get_spark_props_from_start_session(emr_client)
    assert spark_props["spark.dynamicAllocation.executorIdleTimeout"] == "120s"
    # Base defaults preserved
    assert spark_props["spark.sql.catalogImplementation"] == "hive"


def test_executor_idle_timeout_overridden_by_connection_config(manager, mock_boto3_clients):
    """Ensure connection-level spark config overrides the SDK default executorIdleTimeout."""
    connection_configs = {"spark.dynamicAllocation.executorIdleTimeout": "300s"}
    emr_client = _setup_manager_for_session_start(
        manager, mock_boto3_clients, connection_spark_configs=connection_configs
    )

    app = {"state": "STARTED", "releaseLabel": "emr-7.5.0"}

    with patch.object(
        manager, "_get_user_id_account_id", return_value=("test-user", "1234567890")
    ), patch.object(manager, "_ensure_application_started", return_value=app), patch(
        "sagemaker_studio.utils.spark.session.emr_serverless.emr_serverless_spark_session_manager.generate_spark_configs",
        return_value={},
    ), patch.object(
        manager, "_get_s3_access_grants_configs", return_value={}
    ):
        manager._start_emr_serverless_session("app-1")

    spark_props = _get_spark_props_from_start_session(emr_client)
    assert spark_props["spark.dynamicAllocation.executorIdleTimeout"] == "300s"


def test_executor_idle_timeout_spark_conf_wins_over_all(manager, mock_boto3_clients):
    """Ensure user spark_conf overrides both SDK default and connection config."""
    connection_configs = {"spark.dynamicAllocation.executorIdleTimeout": "300s"}
    emr_client = _setup_manager_for_session_start(
        manager, mock_boto3_clients, connection_spark_configs=connection_configs
    )
    manager.spark_conf = {
        "spark.dynamicAllocation.executorIdleTimeout": "45s",
        "spark.executor.memory": "4g",
    }

    app = {"state": "STARTED", "releaseLabel": "emr-7.5.0"}

    with patch.object(
        manager, "_get_user_id_account_id", return_value=("test-user", "1234567890")
    ), patch.object(manager, "_ensure_application_started", return_value=app), patch(
        "sagemaker_studio.utils.spark.session.emr_serverless.emr_serverless_spark_session_manager.generate_spark_configs",
        return_value={"spark.sql.catalogImplementation": "hive"},
    ), patch.object(
        manager, "_get_s3_access_grants_configs", return_value={}
    ):
        manager._start_emr_serverless_session("app-1")

    spark_props = _get_spark_props_from_start_session(emr_client)
    # spark_conf wins over connection config and SDK default
    assert spark_props["spark.dynamicAllocation.executorIdleTimeout"] == "45s"
    # spark_conf additions present
    assert spark_props["spark.executor.memory"] == "4g"
    # Base defaults preserved
    assert spark_props["spark.sql.catalogImplementation"] == "hive"
