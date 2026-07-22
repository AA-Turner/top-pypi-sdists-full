"""Tests for EmrEc2SparkSessionManager."""

import sys
from unittest.mock import MagicMock, Mock, patch

import pytest

# Mock Project class before any imports to prevent Domain ID error
with patch("sagemaker_studio.Project"):

    # Mock external dependencies that aren't available in test environment
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
    mock_interceptors.EmrEc2ChannelBuilder = Mock()
    sys.modules["sagemaker_studio.utils.spark.session.emr_ec2.interceptors"] = mock_interceptors

    from sagemaker_studio.utils.spark.session.emr_ec2.emr_ec2_spark_session_manager import (
        EmrEc2SparkSessionManager,
    )


_TEST_COMPUTE_ARN = "arn:aws:elasticmapreduce:us-west-2:123456789012:cluster/j-ABC123"
_TEST_CLUSTER_ID = "j-ABC123"
_TEST_REGION = "us-west-2"


def _make_connection(compute_arn=_TEST_COMPUTE_ARN):
    """Create a mock connection object."""
    conn = MagicMock()
    conn._Connection__connection_data = {
        "type": "SPARK_CONNECT",
        "props": {"sparkEmrProperties": {"computeArn": compute_arn}},
    }
    conn.type = "SPARK_CONNECT"
    conn.name = "test-emr-ec2-connection"
    return conn


@pytest.fixture
def mock_internal_utils():
    """Mocks InternalUtils and _ensure_project on the EMR on EC2 module."""
    with patch(
        "sagemaker_studio.utils.spark.session.emr_ec2.emr_ec2_spark_session_manager.InternalUtils"
    ) as mock_utils, patch(
        "sagemaker_studio.utils.spark.session.emr_ec2.emr_ec2_spark_session_manager._ensure_project"
    ) as mock_ensure_project:
        mock_utils.return_value._get_domain_region.return_value = _TEST_REGION
        mock_utils.return_value._get_datazone_stage.return_value = "prod"
        mock_utils.return_value._get_user_id.return_value = "test-user"
        mock_project = MagicMock()
        mock_project.id = "proj-123"
        mock_project.connection.return_value = _make_connection()
        mock_ensure_project.return_value = mock_project
        yield mock_utils, mock_project


@pytest.fixture
def manager():
    """Create a testable EmrEc2SparkSessionManager with a pre-resolved connection."""
    return EmrEc2SparkSessionManager(connection=_make_connection())


class TestInit:
    def test_init_with_connection(self):
        conn = _make_connection()
        mgr = EmrEc2SparkSessionManager(connection=conn)
        assert mgr._connection is conn
        assert mgr.cluster_id is None  # resolved lazily

    def test_init_with_connection_name(self):
        mgr = EmrEc2SparkSessionManager(connection_name="my-conn")
        assert mgr.connection_name == "my-conn"
        assert mgr._connection is None

    def test_init_with_spark_conf(self):
        conf = {"spark.executor.memory": "4g"}
        mgr = EmrEc2SparkSessionManager(connection=_make_connection(), spark_conf=conf)
        assert mgr._user_spark_conf == conf

    def test_get_session_id_returns_emr_session_id(self):
        mgr = EmrEc2SparkSessionManager(connection=_make_connection())
        mgr.emr_session_id = "sess-abc"
        assert mgr.get_session_id() == "sess-abc"

    def test_get_session_id_returns_none_by_default(self):
        mgr = EmrEc2SparkSessionManager(connection=_make_connection())
        assert mgr.get_session_id() is None


class TestLazyInit:
    @patch("boto3.client")
    @patch("boto3.Session")
    def test_extracts_cluster_id_and_region(
        self, mock_session_cls, mock_boto_client, mock_internal_utils
    ):
        mgr = EmrEc2SparkSessionManager(connection=_make_connection())
        mock_session_cls.return_value.client.return_value = MagicMock()

        with patch("os.path.isdir", return_value=True), patch("botocore.loaders.Loader"), patch(
            "botocore.session.get_session"
        ):
            mgr._lazy_init()

        assert mgr.cluster_id == _TEST_CLUSTER_ID
        assert mgr.region == _TEST_REGION

    @patch("boto3.client")
    @patch("boto3.Session")
    def test_falls_back_to_domain_region(
        self, mock_session_cls, mock_boto_client, mock_internal_utils
    ):
        conn = _make_connection("arn:aws:elasticmapreduce:::cluster/j-NORGN")
        mgr = EmrEc2SparkSessionManager(connection=conn)
        mock_session_cls.return_value.client.return_value = MagicMock()

        with patch("os.path.isdir", return_value=True), patch("botocore.loaders.Loader"), patch(
            "botocore.session.get_session"
        ):
            mgr._lazy_init()

        assert mgr.cluster_id == "j-NORGN"
        assert mgr.region == _TEST_REGION

    @patch("boto3.client")
    @patch("boto3.Session")
    def test_endpoint_from_config(self, mock_session_cls, mock_boto_client, mock_internal_utils):
        from sagemaker_studio.data_models import ClientConfig

        config = ClientConfig(
            overrides={"emr": {"endpoint_url": "https://custom-endpoint.example.com"}}
        )
        mgr = EmrEc2SparkSessionManager(connection=_make_connection(), config=config)
        mock_session_cls.return_value.client.return_value = MagicMock()

        with patch("os.path.isdir", return_value=True), patch("botocore.loaders.Loader"), patch(
            "botocore.session.get_session"
        ):
            mgr._lazy_init()

        assert mgr.endpoint_url == "https://custom-endpoint.example.com"

    @patch("boto3.client")
    @patch("boto3.Session")
    def test_no_endpoint_when_config_empty(
        self, mock_session_cls, mock_boto_client, mock_internal_utils
    ):
        mgr = EmrEc2SparkSessionManager(connection=_make_connection())
        mock_session_cls.return_value.client.return_value = MagicMock()

        with patch("os.path.isdir", return_value=True), patch("botocore.loaders.Loader"), patch(
            "botocore.session.get_session"
        ):
            mgr._lazy_init()

        assert mgr.endpoint_url is None

    def test_raises_without_connection_or_name(self, mock_internal_utils):
        mgr = EmrEc2SparkSessionManager()
        with pytest.raises(ValueError, match="requires a connection or connection_name"):
            mgr._lazy_init()

    def test_raises_when_compute_arn_missing(self, mock_internal_utils):
        conn = MagicMock()
        conn._Connection__connection_data = {
            "type": "SPARK_CONNECT",
            "props": {"sparkEmrProperties": {}},
        }
        mgr = EmrEc2SparkSessionManager(connection=conn)
        with pytest.raises(ValueError, match="Could not resolve cluster_id"):
            mgr._lazy_init()

    def test_falls_back_when_model_path_missing(self, mock_internal_utils):
        mgr = EmrEc2SparkSessionManager(connection=_make_connection())
        with patch("os.path.isdir", return_value=False), patch("boto3.client"), patch(
            "boto3.Session"
        ) as mock_session:
            mock_session.return_value.client.return_value = MagicMock()
            mgr._lazy_init()
        # Should not raise; falls back to default boto3 session
        assert mgr._emr_client is not None

    @patch("boto3.client")
    @patch("boto3.Session")
    def test_resolves_connection_by_name(
        self, mock_session_cls, mock_boto_client, mock_internal_utils
    ):
        """Test _lazy_init resolves connection from connection_name when no connection object."""
        mock_utils, mock_project = mock_internal_utils
        mock_project.connection.return_value = _make_connection()
        mock_session_cls.return_value.client.return_value = MagicMock()

        mgr = EmrEc2SparkSessionManager(connection_name="my-emr-conn")

        with patch("os.path.isdir", return_value=True), patch("botocore.loaders.Loader"), patch(
            "botocore.session.get_session"
        ):
            mgr._lazy_init()

        mock_project.connection.assert_called_once_with("my-emr-conn")
        assert mgr.cluster_id == _TEST_CLUSTER_ID


class TestCreate:
    @patch(
        "sagemaker_studio.utils.spark.session.emr_ec2.emr_ec2_spark_session_manager._SparkSession"
    )
    @patch(
        "sagemaker_studio.utils.spark.session.emr_ec2.emr_ec2_spark_session_manager.EmrEc2ChannelBuilder"
    )
    def test_create_starts_session(self, mock_channel_builder, mock_spark_session, manager):
        manager._lazy_init = MagicMock()
        manager._build_session_params = MagicMock(return_value=("user-1", {"key": "val"}))
        manager._start_session = MagicMock(
            return_value=(
                "sess-1",
                "sc://host:443/;use_ssl=true",
                {"AuthToken": "tok", "AuthTokenExpirationTime": None, "Credentials": {}},
            )
        )
        manager.cluster_id = _TEST_CLUSTER_ID
        manager._emr_client = MagicMock()
        manager.emr_session_id = "sess-1"

        builder = MagicMock()
        mock_spark_session.builder.channelBuilder.return_value = builder
        builder.appName.return_value = builder
        builder.getOrCreate.return_value = "mock_spark"

        session = manager.create()

        assert session == "mock_spark"
        assert manager.emr_session_id == "sess-1"
        manager._build_session_params.assert_called_once()
        manager._start_session.assert_called_once_with("user-1", {"key": "val"})
        mock_channel_builder.assert_called_once()
        builder.getOrCreate.assert_called_once()

    def test_create_returns_existing_session(self, manager):
        manager._spark_session = "existing_session"
        assert manager.create() == "existing_session"

    @patch.object(EmrEc2SparkSessionManager, "stop")
    def test_create_calls_stop_on_failure(self, mock_stop, manager):
        manager._lazy_init = MagicMock(side_effect=RuntimeError("init failed"))

        with pytest.raises(RuntimeError, match="init failed"):
            manager.create()

        mock_stop.assert_called_once()


class TestStop:
    def test_stop_terminates_session_and_spark(self, manager):
        mock_spark = MagicMock()
        mock_emr_client = MagicMock()
        manager._spark_session = mock_spark
        manager._emr_client = mock_emr_client
        manager.emr_session_id = "sess-1"
        manager.cluster_id = _TEST_CLUSTER_ID

        manager.stop()

        mock_spark.stop.assert_called_once()
        mock_emr_client.terminate_session.assert_called_once_with(
            ClusterId=_TEST_CLUSTER_ID, SessionId="sess-1"
        )
        assert manager._spark_session is None
        assert manager.emr_session_id is None

    def test_stop_handles_no_session(self, manager):
        manager._spark_session = None
        manager.emr_session_id = None
        manager.stop()  # should not raise

    def test_stop_handles_spark_stop_error(self, manager):
        mock_spark = MagicMock()
        mock_spark.stop.side_effect = Exception("spark error")
        manager._spark_session = mock_spark
        manager._emr_client = MagicMock()
        manager.emr_session_id = "sess-1"
        manager.cluster_id = _TEST_CLUSTER_ID

        manager.stop()  # should not raise
        assert manager._spark_session is None

    def test_stop_terminates_emr_session_only(self, manager):
        """Test stop with EMR session but no spark session -- covers terminate success log."""
        mock_emr_client = MagicMock()
        manager._spark_session = None
        manager._emr_client = mock_emr_client
        manager.emr_session_id = "sess-2"
        manager.cluster_id = _TEST_CLUSTER_ID

        manager.stop()

        mock_emr_client.terminate_session.assert_called_once_with(
            ClusterId=_TEST_CLUSTER_ID, SessionId="sess-2"
        )
        assert manager.emr_session_id is None

    def test_stop_handles_terminate_session_error(self, manager):
        """Test stop handles terminate_session failure gracefully."""
        mock_emr_client = MagicMock()
        mock_emr_client.terminate_session.side_effect = Exception("terminate failed")
        manager._spark_session = None
        manager._emr_client = mock_emr_client
        manager.emr_session_id = "sess-3"
        manager.cluster_id = _TEST_CLUSTER_ID

        manager.stop()  # should not raise
        assert manager.emr_session_id is None


class TestWaitForIdle:
    def test_returns_when_idle(self, manager):
        mock_client = MagicMock()
        mock_client.get_session.return_value = {"Session": {"State": "IDLE"}}
        manager._emr_client = mock_client
        manager.cluster_id = _TEST_CLUSTER_ID

        manager._wait_for_idle("sess-1")
        mock_client.get_session.assert_called_once()

    def test_raises_on_failed_state(self, manager):
        mock_client = MagicMock()
        mock_client.get_session.return_value = {
            "Session": {"State": "FAILED", "StateChangeReason": "out of memory"}
        }
        manager._emr_client = mock_client
        manager.cluster_id = _TEST_CLUSTER_ID

        with pytest.raises(RuntimeError, match="FAILED.*out of memory"):
            manager._wait_for_idle("sess-1")

    @patch("time.sleep")
    def test_raises_on_timeout(self, mock_sleep, manager):
        mock_client = MagicMock()
        mock_client.get_session.return_value = {"Session": {"State": "STARTING"}}
        manager._emr_client = mock_client
        manager.cluster_id = _TEST_CLUSTER_ID

        with pytest.raises(RuntimeError, match="Timed out"):
            manager._wait_for_idle("sess-1")


class TestGetSparkConnectUrl:
    def test_converts_https_to_sc(self, manager):
        mock_client = MagicMock()
        mock_client.get_session_endpoint.return_value = {
            "Endpoint": "https://spark.example.com/path",
            "AuthToken": "token123",
            "AuthTokenExpirationTime": None,
        }
        manager._emr_client = mock_client
        manager.cluster_id = _TEST_CLUSTER_ID

        url, resp = manager._get_spark_connect_url("sess-1")
        assert url == "sc://spark.example.com:443/;use_ssl=true"
        assert resp["AuthToken"] == "token123"

    def test_passthrough_non_https(self, manager):
        mock_client = MagicMock()
        mock_client.get_session_endpoint.return_value = {
            "Endpoint": "sc://already-correct:443",
            "AuthToken": "tok",
            "AuthTokenExpirationTime": None,
        }
        manager._emr_client = mock_client
        manager.cluster_id = _TEST_CLUSTER_ID

        url, _ = manager._get_spark_connect_url("sess-1")
        assert url == "sc://already-correct:443"


class TestGetServiceSpecificConfigs:
    def test_returns_compatibility_mode_configs(self, manager):
        configs = manager._get_service_specific_configs()
        assert "spark.hadoop.fs.s3.credentialsResolverClass" in configs
        assert configs["spark.hadoop.fs.s3.useDirectoryHeaderAsFolderObject"] == "true"
        assert configs["spark.sql.catalog.spark_catalog.glue.lakeformation-enabled"] == "true"

    def test_returns_all_expected_keys(self, manager):
        configs = manager._get_service_specific_configs()
        expected_keys = [
            "spark.hadoop.fs.s3.credentialsResolverClass",
            "spark.hadoop.fs.s3.useDirectoryHeaderAsFolderObject",
            "spark.hadoop.fs.s3.folderObject.autoAction.disabled",
            "spark.sql.catalog.createDirectoryAfterTable.enabled",
            "spark.sql.catalog.dropDirectoryBeforeTable.enabled",
            "spark.sql.catalog.spark_catalog.glue.lakeformation-enabled",
            "spark.sql.catalog.skipLocationValidationOnCreateTable.enabled",
        ]
        for key in expected_keys:
            assert key in configs

    def test_includes_openlineage_configs(self, manager):
        """OpenLineage configs should be present for data lineage tracking."""
        manager.project = MagicMock()
        manager.project.domain_id = "dzd-test-domain"
        configs = manager._get_service_specific_configs()
        assert (
            configs["spark.extraListeners"] == "io.openlineage.spark.agent.OpenLineageSparkListener"
        )
        assert configs["spark.openlineage.transport.type"] == "amazon_datazone_api"
        assert configs["spark.openlineage.transport.domainId"] == "dzd-test-domain"

    def test_openlineage_domain_id_from_project(self, manager):
        """domainId should come from self.project.domain_id."""
        manager.project = MagicMock()
        manager.project.domain_id = "dzd-test-domain-123"
        configs = manager._get_service_specific_configs()
        assert configs["spark.openlineage.transport.domainId"] == "dzd-test-domain-123"

    def test_no_glue_specific_configs(self, manager):
        """Should NOT include Glue-specific keys."""
        manager.project = MagicMock()
        manager.project.domain_id = "dzd-test"
        configs = manager._get_service_specific_configs()
        assert "spark.glue.accountId" not in configs
        assert "spark.glue.JOB_NAME" not in configs
        assert "spark.openlineage.facets.custom_environment_variables" not in configs

    def test_openlineage_graceful_failure_without_project(self, manager):
        """If project is not set, OpenLineage configs should be skipped gracefully."""
        # project not set — accessing self.project.domain_id raises AttributeError
        configs = manager._get_service_specific_configs()
        # Compatibility mode configs should still be present
        assert "spark.hadoop.fs.s3.credentialsResolverClass" in configs
        # OpenLineage configs should be absent (caught by try/except)
        assert "spark.extraListeners" not in configs


class TestStartSession:
    @patch("boto3.client")
    @patch(
        "sagemaker_studio.utils.spark.session.emr_ec2.emr_ec2_spark_session_manager.build_spark_configs",
        return_value={"spark.test.key": "test_val"},
    )
    @patch(
        "sagemaker_studio.utils.spark.session.emr_ec2.emr_ec2_spark_session_manager.extract_connection_spark_configs",
        return_value={"spark.conn.key": "conn_val"},
    )
    def test_start_session_tags_and_configs(
        self, mock_extract, mock_build, mock_boto_client, manager, mock_internal_utils
    ):
        mock_utils, mock_project = mock_internal_utils
        manager._utils = mock_utils.return_value
        manager.project = mock_project
        manager.cluster_id = _TEST_CLUSTER_ID
        manager.endpoint_url = None
        manager.region = _TEST_REGION
        manager.sts_client = MagicMock()
        manager.sts_client.get_caller_identity.return_value = {
            "Account": "123456789012",
            "UserId": "AROAEXAMPLE:test-user",
        }

        mock_emr = MagicMock()
        mock_emr.start_session.return_value = {"Id": "sess-1", "State": "STARTING"}
        manager._emr_client = mock_emr
        manager._wait_for_idle = MagicMock()
        manager._get_spark_connect_url = MagicMock(
            return_value=("sc://host:443/;use_ssl=true", {"AuthToken": "tok"})
        )
        manager._user_msg = MagicMock()

        session_id, url, resp = manager._start_session("test-user", {"spark.test.key": "test_val"})

        assert session_id == "sess-1"
        call_kwargs = mock_emr.start_session.call_args[1]
        assert call_kwargs["ClusterId"] == _TEST_CLUSTER_ID
        tags = {t["Key"]: t["Value"] for t in call_kwargs["Tags"]}
        assert tags["AmazonDataZoneSessionOwner"] == "test-user"
        assert tags["AmazonDataZoneProject"] == "proj-123"
        # Verify EngineConfigurations passed with spark configs
        engine_configs = call_kwargs["EngineConfigurations"]
        assert len(engine_configs) == 1
        assert engine_configs[0]["Classification"] == "spark-defaults"
        assert engine_configs[0]["Properties"] == {"spark.test.key": "test_val"}

    @patch("boto3.client")
    @patch(
        "sagemaker_studio.utils.spark.session.emr_ec2.emr_ec2_spark_session_manager.build_spark_configs",
        return_value={"spark.key": "val"},
    )
    @patch(
        "sagemaker_studio.utils.spark.session.emr_ec2.emr_ec2_spark_session_manager.extract_connection_spark_configs",
        return_value={},
    )
    def test_start_session_passes_user_spark_conf(
        self, mock_extract, mock_build, mock_boto_client, manager, mock_internal_utils
    ):
        mock_utils, mock_project = mock_internal_utils
        manager._utils = mock_utils.return_value
        manager.project = mock_project
        manager.cluster_id = _TEST_CLUSTER_ID
        manager.endpoint_url = None
        manager.region = _TEST_REGION
        manager.sts_client = MagicMock()
        manager.sts_client.get_caller_identity.return_value = {
            "Account": "123456789012",
            "UserId": "AROAEXAMPLE:test-user",
        }
        manager.set_user_spark_conf({"spark.user.override": "user_val"})

        mock_emr = MagicMock()
        mock_emr.start_session.return_value = {"Id": "sess-2", "State": "STARTING"}
        manager._emr_client = mock_emr

        manager._build_session_params()

        # Verify user configs were passed to build_spark_configs
        mock_build.assert_called_once()
        build_kwargs = mock_build.call_args[1]
        assert build_kwargs["user_configs"] == {"spark.user.override": "user_val"}
