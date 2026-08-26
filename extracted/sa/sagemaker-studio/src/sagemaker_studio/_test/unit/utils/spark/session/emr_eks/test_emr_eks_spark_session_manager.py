"""Tests for EmrEksSparkSessionManager."""

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

    # Mock the interceptors module to avoid importing the real interceptors.
    mock_interceptors = Mock()
    mock_interceptors.EmrEksChannelBuilder = Mock()
    sys.modules["sagemaker_studio.utils.spark.session.emr_eks.interceptors"] = mock_interceptors

    from sagemaker_studio.utils.spark.session.emr_eks.emr_eks_spark_session_manager import (
        EmrEksSparkSessionManager,
        _parse_emr_eks_arn,
    )

_MODULE = "sagemaker_studio.utils.spark.session.emr_eks.emr_eks_spark_session_manager"

_VC_ID = "vc-123"
_ENDPOINT_ID = "ep-abc"
_REGION = "us-west-2"
_RELEASE_LABEL = "emr-7.11.0-latest"
# Connection carries only the virtual cluster (no endpoint); endpoint is created per session.
_VC_ARN = f"arn:aws:emr-containers:{_REGION}:111122223333:/virtualclusters/{_VC_ID}"
_FULL_ARN = f"{_VC_ARN}/endpoints/{_ENDPOINT_ID}"


def _make_connection(compute_arn=_VC_ARN, release_label=_RELEASE_LABEL):
    conn = MagicMock()
    conn_data = {
        "type": "SPARK_CONNECT",
        "props": {"sparkEmrProperties": {"computeArn": compute_arn}},
    }
    if release_label:
        # Real connection shape: release label lives in the spark-defaults configuration.
        conn_data["configurations"] = [
            {
                "classification": "spark-defaults",
                "properties": {"spark.emr.releaseLabel": release_label},
            }
        ]
    conn._Connection__connection_data = conn_data
    conn.type = "SPARK_CONNECT"
    conn.name = "test-emr-eks-connection"
    return conn


@pytest.fixture
def manager():
    return EmrEksSparkSessionManager(connection=_make_connection())


@pytest.fixture
def mock_internal():
    with patch(f"{_MODULE}.InternalUtils") as mock_utils, patch(
        f"{_MODULE}.Project"
    ) as mock_project:
        mock_utils.return_value._get_domain_region.return_value = _REGION
        mock_project.return_value.iam_role = "arn:aws:iam::111122223333:role/Exec"
        yield mock_utils, mock_project


class TestInit:
    def test_init_with_connection(self):
        conn = _make_connection()
        mgr = EmrEksSparkSessionManager(connection=conn)
        assert mgr._connection is conn
        assert mgr.virtual_cluster_id is None  # resolved lazily
        assert mgr.endpoint_id is None  # created per session in create()

    def test_init_with_connection_name(self):
        mgr = EmrEksSparkSessionManager(connection_name="my-conn")
        assert mgr.connection_name == "my-conn"
        assert mgr._connection is None

    def test_init_stores_spark_conf(self):
        conf = {"spark.executor.memory": "4g"}
        mgr = EmrEksSparkSessionManager(connection=_make_connection(), spark_conf=conf)
        assert mgr._user_spark_conf == conf


class TestParseArn:
    def test_full_arn(self):
        assert _parse_emr_eks_arn(_FULL_ARN) == (_VC_ID, _ENDPOINT_ID, _REGION)

    def test_vc_only(self):
        assert _parse_emr_eks_arn(_VC_ARN) == (_VC_ID, None, _REGION)

    def test_empty(self):
        assert _parse_emr_eks_arn("") == (None, None, "")


class TestToScUrl:
    def test_https(self, manager):
        assert (
            manager._to_sc_url("https://ep.example.com:443")
            == "sc://ep.example.com:443/;use_ssl=true"
        )

    def test_adds_default_port(self, manager):
        assert (
            manager._to_sc_url("https://host.example.com")
            == "sc://host.example.com:443/;use_ssl=true"
        )

    def test_passthrough_sc(self, manager):
        assert manager._to_sc_url("sc://host:443") == "sc://host:443/;use_ssl=true"


class TestLazyInit:
    @patch("boto3.client")
    @patch("boto3.Session")
    def test_resolves_vc_release_region(self, mock_session_cls, _mock_client, mock_internal):
        mgr = EmrEksSparkSessionManager(connection=_make_connection())
        mock_session_cls.return_value.client.return_value = MagicMock()
        with patch("os.path.isdir", return_value=True), patch("boto3.client"), patch(
            "botocore.loaders.Loader"
        ), patch("botocore.session.get_session"):
            mgr._lazy_init()
        assert mgr.virtual_cluster_id == _VC_ID
        assert mgr.release_label == _RELEASE_LABEL
        assert mgr.region == _REGION
        assert mgr.endpoint_id is None  # not created until create()
        assert mgr._emr_client is not None

    def test_raises_when_release_label_absent(self, mock_internal):
        mgr = EmrEksSparkSessionManager(connection=_make_connection(release_label=None))
        with patch("os.path.isdir", return_value=False), patch("boto3.Session") as mock_session:
            mock_session.return_value.client.return_value = MagicMock()
            with pytest.raises(ValueError, match="spark.emr.releaseLabel"):
                mgr._lazy_init()

    def test_release_label_from_configurations(self, mock_internal):
        conn = _make_connection(release_label=None)
        conn._Connection__connection_data["configurations"] = [
            {
                "classification": "spark-defaults",
                "properties": {"spark.emr.releaseLabel": "emr-7.9.0"},
            }
        ]
        mgr = EmrEksSparkSessionManager(connection=conn)
        with patch("os.path.isdir", return_value=False), patch("boto3.client"), patch(
            "boto3.Session"
        ) as mock_session:
            mock_session.return_value.client.return_value = MagicMock()
            mgr._lazy_init()
        assert mgr.release_label == "emr-7.9.0"

    def test_raises_without_vc(self, mock_internal):
        mgr = EmrEksSparkSessionManager(
            connection=_make_connection(compute_arn="arn:aws:emr-containers:::/foo/bar")
        )
        with pytest.raises(ValueError, match="virtual_cluster_id"):
            mgr._lazy_init()


class TestCreateManagedEndpointSession:
    def _client(self, state="ACTIVE", host="https://ep.host:443"):
        client = MagicMock()
        client.create_managed_endpoint.return_value = {
            "id": _ENDPOINT_ID,
            "name": "sc-endpoint-x",
            "arn": "arn:aws:emr-containers:us-west-2:111122223333:/virtualclusters/vc-123/endpoints/ep-abc",
            "virtualClusterId": _VC_ID,
        }
        endpoint = {"state": state}
        if host:
            endpoint["authProxyUrl"] = host
        client.describe_managed_endpoint.return_value = {"endpoint": endpoint}
        client.get_managed_endpoint_session_credentials.return_value = {
            "credentials": {"token": "tok"},
            "expiresAt": None,
        }
        return client

    def _prime(self, manager, client):
        manager._emr_client = client
        manager.virtual_cluster_id = _VC_ID
        manager.release_label = _RELEASE_LABEL
        manager.project = MagicMock(iam_role="role", id="proj-123", domain_id="dzd-test")
        manager.sts_client = MagicMock()
        manager.connection_spark_configs = {}
        manager._get_user_id_account_id = MagicMock(return_value=("test-user", "111122223333"))

    def _patch_build_spark_configs(self):
        """Patch build_spark_configs to bypass _ensure_project and return merged configs directly."""

        def _fake_build(
            account_id, service_configs=None, connection_configs=None, user_configs=None
        ):
            configs = {}
            if service_configs:
                configs.update(service_configs)
            if connection_configs:
                configs.update(connection_configs)
            if user_configs:
                configs.update(user_configs)
            return configs

        return patch(f"{_MODULE}.build_spark_configs", side_effect=_fake_build)

    def test_creates_endpoint_and_returns_url_token(self, manager):
        client = self._client()
        self._prime(manager, client)
        with self._patch_build_spark_configs():
            url, token, _ = manager._create_managed_endpoint_session(
                manager._build_endpoint_params()
            )
        assert url == "sc://ep.host:443/;use_ssl=true"
        assert token == "tok"
        assert manager.endpoint_id == _ENDPOINT_ID
        kwargs = client.create_managed_endpoint.call_args.kwargs
        assert kwargs["virtualClusterId"] == _VC_ID
        assert kwargs["type"] == "SPARK_CONNECT"
        assert kwargs["releaseLabel"] == _RELEASE_LABEL
        assert kwargs["executionRoleArn"] == "role"

    def test_spark_conf_passed_as_configuration_overrides(self, manager):
        client = self._client()
        self._prime(manager, client)
        manager.set_user_spark_conf(
            {"spark.executor.memory": "4g", "spark.sql.shuffle.partitions": "10"}
        )
        with self._patch_build_spark_configs():
            manager._create_managed_endpoint_session(manager._build_endpoint_params())
        kwargs = client.create_managed_endpoint.call_args.kwargs
        app_cfg = kwargs["configurationOverrides"]["applicationConfiguration"][0]
        assert app_cfg["classification"] == "spark-defaults"
        props = app_cfg["properties"]
        # User spark_conf passed through build_spark_configs
        assert props["spark.executor.memory"] == "4g"
        assert props["spark.sql.shuffle.partitions"] == "10"

    def test_no_spark_conf_includes_openlineage_overrides(self, manager):
        client = self._client()
        self._prime(manager, client)
        with self._patch_build_spark_configs():
            manager._create_managed_endpoint_session(manager._build_endpoint_params())
        kwargs = client.create_managed_endpoint.call_args.kwargs
        # configurationOverrides always present (build_spark_configs produces service configs)
        assert "configurationOverrides" in kwargs

    def test_falls_back_to_server_url(self, manager):
        client = self._client(host=None)
        client.describe_managed_endpoint.return_value = {
            "endpoint": {"state": "ACTIVE", "serverUrl": "https://nlb.host:443"}
        }
        self._prime(manager, client)
        with self._patch_build_spark_configs():
            url, _, _ = manager._create_managed_endpoint_session(manager._build_endpoint_params())
        assert url == "sc://nlb.host:443/;use_ssl=true"

    def test_terminated_endpoint_raises(self, manager):
        client = self._client(state="TERMINATED_WITH_ERRORS", host=None)
        self._prime(manager, client)
        with self._patch_build_spark_configs():
            with pytest.raises(RuntimeError, match="TERMINATED_WITH_ERRORS"):
                manager._create_managed_endpoint_session(manager._build_endpoint_params())
        # endpoint_id still set so stop() can attempt cleanup
        assert manager.endpoint_id == _ENDPOINT_ID


class TestCreate:
    def test_returns_existing(self, manager):
        manager._spark_session = "existing"
        assert manager.create() == "existing"

    def test_happy_path(self, manager):
        manager._lazy_init = MagicMock()
        manager.virtual_cluster_id, manager.endpoint_id = _VC_ID, _ENDPOINT_ID
        manager._emr_client = MagicMock()
        manager.project = MagicMock(iam_role="role")
        manager._build_endpoint_params = MagicMock(return_value={})
        manager._create_managed_endpoint_session = MagicMock(
            return_value=("sc://host:443/;use_ssl=true", "tok", None)
        )
        with patch(f"{_MODULE}._SparkSession") as mock_spark, patch(
            f"{_MODULE}.EmrEksChannelBuilder"
        ) as mock_cb:
            builder = MagicMock()
            mock_spark.builder.channelBuilder.return_value = builder
            builder.appName.return_value = builder
            builder.getOrCreate.return_value = "mock_spark_session"
            assert manager.create() == "mock_spark_session"
        mock_cb.assert_called_once()
        manager._create_managed_endpoint_session.assert_called_once()
        # appName has a random suffix (comment #5)
        app_name_arg = builder.appName.call_args.args[0]
        assert app_name_arg.startswith("EmrEksSparkSession-")
        assert app_name_arg != "EmrEksSparkSession-"

    @patch.object(EmrEksSparkSessionManager, "stop")
    def test_calls_stop_on_failure(self, mock_stop, manager):
        manager._lazy_init = MagicMock(side_effect=RuntimeError("boom"))
        with pytest.raises(RuntimeError, match="boom"):
            manager.create()
        mock_stop.assert_called_once()


class TestStop:
    def test_stops_spark_and_deletes_endpoint(self, manager):
        spark = MagicMock()
        client = MagicMock()
        manager._spark_session = spark
        manager._emr_client = client
        manager.virtual_cluster_id = _VC_ID
        manager.endpoint_id = _ENDPOINT_ID
        manager.stop()
        spark.stop.assert_called_once()
        client.delete_managed_endpoint.assert_called_once_with(
            id=_ENDPOINT_ID, virtualClusterId=_VC_ID
        )
        assert manager._spark_session is None
        assert manager.endpoint_id is None

    def test_deletes_endpoint_without_spark(self, manager):
        client = MagicMock()
        manager._spark_session = None
        manager._emr_client = client
        manager.virtual_cluster_id = _VC_ID
        manager.endpoint_id = _ENDPOINT_ID
        manager.stop()
        client.delete_managed_endpoint.assert_called_once_with(
            id=_ENDPOINT_ID, virtualClusterId=_VC_ID
        )
        assert manager.endpoint_id is None

    def test_no_session_no_endpoint(self, manager):
        manager._spark_session = None
        manager.endpoint_id = None
        manager.stop()  # must not raise


class _Cfg:
    """Minimal ClientConfig stand-in exposing an overrides dict."""

    def __init__(self, overrides):
        self.overrides = overrides


class TestParseArnEdges:
    def test_virtualclusters_keyword_without_id(self):
        arn = f"arn:aws:emr-containers:{_REGION}:111122223333:/virtualclusters"
        assert _parse_emr_eks_arn(arn) == (None, None, _REGION)

    def test_endpoints_keyword_without_id(self):
        arn = f"arn:aws:emr-containers:{_REGION}:111122223333:/virtualclusters/{_VC_ID}/endpoints"
        assert _parse_emr_eks_arn(arn) == (_VC_ID, None, _REGION)


class TestLazyInitMore:
    def test_resolves_by_connection_name(self, mock_internal):
        _, mock_project = mock_internal
        conn = _make_connection()
        mock_project.return_value.connection.return_value = conn
        mgr = EmrEksSparkSessionManager(connection_name="my-conn")
        with patch("os.path.isdir", return_value=False), patch("boto3.client"), patch(
            "boto3.Session"
        ) as ms:
            ms.return_value.client.return_value = MagicMock()
            mgr._lazy_init()
        assert mgr.virtual_cluster_id == _VC_ID
        mock_project.return_value.connection.assert_called_once_with("my-conn")

    def test_raises_without_connection_or_name(self, mock_internal):
        mgr = EmrEksSparkSessionManager()
        with pytest.raises(ValueError, match="connection or connection_name"):
            mgr._lazy_init()

    def test_config_override_release_label_not_used(self, mock_internal):
        # release_label is no longer sourced from config overrides; absence must raise.
        mgr = EmrEksSparkSessionManager(
            connection=_make_connection(release_label=None),
            config=_Cfg({"emr-containers": {"release_label": "emr-7.5.0"}}),
        )
        with patch("os.path.isdir", return_value=False), patch("boto3.client"), patch(
            "boto3.Session"
        ) as ms:
            ms.return_value.client.return_value = MagicMock()
            with pytest.raises(ValueError, match="spark.emr.releaseLabel"):
                mgr._lazy_init()

    def test_release_label_skips_non_spark_defaults_config(self, mock_internal):
        conn = _make_connection(release_label=None)
        conn._Connection__connection_data["configurations"] = [
            {"classification": "other", "properties": {"foo": "bar"}},  # ignored
            {
                "classification": "spark-defaults",
                "properties": {"spark.emr.releaseLabel": "emr-7.6.0"},
            },
        ]
        mgr = EmrEksSparkSessionManager(connection=conn)
        with patch("os.path.isdir", return_value=False), patch("boto3.client"), patch(
            "boto3.Session"
        ) as ms:
            ms.return_value.client.return_value = MagicMock()
            mgr._lazy_init()
        assert mgr.release_label == "emr-7.6.0"

    def test_release_label_secondary_from_spark_emr_properties(self, mock_internal):
        # No spark-defaults config, but sparkEmrProperties carries releaseLabel (secondary path).
        conn = _make_connection(release_label=None)
        conn._Connection__connection_data["props"]["sparkEmrProperties"][
            "releaseLabel"
        ] = "emr-7.7.0"
        mgr = EmrEksSparkSessionManager(connection=conn)
        with patch("os.path.isdir", return_value=False), patch("boto3.client"), patch(
            "boto3.Session"
        ) as ms:
            ms.return_value.client.return_value = MagicMock()
            mgr._lazy_init()
        assert mgr.release_label == "emr-7.7.0"

    def test_release_label_ignores_non_dict_config_entry(self, mock_internal):
        conn = _make_connection(release_label=None)
        conn._Connection__connection_data["configurations"] = [
            None,  # non-dict entry must be skipped, not crash
            {
                "classification": "spark-defaults",
                "properties": {"spark.emr.releaseLabel": "emr-7.8.0"},
            },
        ]
        mgr = EmrEksSparkSessionManager(connection=conn)
        with patch("os.path.isdir", return_value=False), patch("boto3.client"), patch(
            "boto3.Session"
        ) as ms:
            ms.return_value.client.return_value = MagicMock()
            mgr._lazy_init()
        assert mgr.release_label == "emr-7.8.0"

    def test_endpoint_url_override_passed_to_client(self, mock_internal):
        mgr = EmrEksSparkSessionManager(
            connection=_make_connection(),
            config=_Cfg(
                {
                    "emr-containers": {
                        "endpoint_url": "https://emr-containers.us-west-2.amazonaws.com"
                    }
                }
            ),
        )
        captured = {}

        def fake_client(name, **kw):
            captured.update(kw)
            return MagicMock()

        with patch("os.path.isdir", return_value=False), patch("boto3.client"), patch(
            "boto3.Session"
        ) as ms:
            ms.return_value.client.side_effect = fake_client
            mgr._lazy_init()
        assert mgr.endpoint_url == "https://emr-containers.us-west-2.amazonaws.com"
        assert captured.get("endpoint_url") == "https://emr-containers.us-west-2.amazonaws.com"


class TestWaitForEndpointActive:
    def _prime(self, manager, client):
        manager._emr_client = client
        manager.virtual_cluster_id = _VC_ID
        manager.endpoint_id = _ENDPOINT_ID

    def test_polls_until_active(self, manager):
        client = MagicMock()
        client.describe_managed_endpoint.side_effect = [
            {"endpoint": {"state": "CREATING"}},
            {"endpoint": {"state": "ACTIVE", "authProxyUrl": "https://ep:443"}},
        ]
        self._prime(manager, client)
        with patch(f"{_MODULE}.time.sleep"):
            endpoint = manager._wait_for_endpoint_active(max_poll=5, poll_interval=0)
        assert endpoint["state"] == "ACTIVE"
        assert client.describe_managed_endpoint.call_count == 2

    def test_max_poll_exhausted_raises(self, manager):
        client = MagicMock()
        client.describe_managed_endpoint.return_value = {"endpoint": {"state": "CREATING"}}
        self._prime(manager, client)
        with patch(f"{_MODULE}.time.sleep"):
            with pytest.raises(RuntimeError, match="Timed out"):
                manager._wait_for_endpoint_active(max_poll=3, poll_interval=0)
        # bounded by max_poll -- no infinite loop
        assert client.describe_managed_endpoint.call_count == 3


class TestCreateManagedEndpointSessionRaises:
    def test_raises_when_no_host(self, manager):
        client = MagicMock()
        client.create_managed_endpoint.return_value = {"id": _ENDPOINT_ID}
        client.describe_managed_endpoint.return_value = {"endpoint": {"state": "ACTIVE"}}
        manager._emr_client = client
        manager.virtual_cluster_id = _VC_ID
        manager.release_label = _RELEASE_LABEL
        manager.project = MagicMock(iam_role="role", id="proj-123", domain_id="dzd-test")
        manager.connection_spark_configs = {}
        manager._get_user_id_account_id = MagicMock(return_value=("test-user", "111122223333"))
        manager._get_service_specific_configs = MagicMock(return_value={})
        with patch(f"{_MODULE}.build_spark_configs", return_value={}):
            with pytest.raises(RuntimeError, match="authProxyUrl or serverUrl"):
                manager._create_managed_endpoint_session(manager._build_endpoint_params())


class TestGetServiceSpecificConfigs:
    def test_returns_compatibility_mode_configs(self, manager):
        manager.project = MagicMock(domain_id="dzd-test-domain")
        configs = manager._get_service_specific_configs()
        assert "spark.hadoop.fs.s3.credentialsResolverClass" in configs
        assert configs["spark.hadoop.fs.s3.useDirectoryHeaderAsFolderObject"] == "true"
        assert configs["spark.sql.catalog.spark_catalog.glue.lakeformation-enabled"] == "true"

    def test_includes_openlineage_configs(self, manager):
        manager.project = MagicMock(domain_id="dzd-test-domain")
        configs = manager._get_service_specific_configs()
        assert (
            configs["spark.extraListeners"] == "io.openlineage.spark.agent.OpenLineageSparkListener"
        )
        assert configs["spark.openlineage.transport.type"] == "amazon_datazone_api"
        assert configs["spark.openlineage.transport.domainId"] == "dzd-test-domain"

    def test_openlineage_domain_id_from_project(self, manager):
        manager.project = MagicMock(domain_id="dzd-custom-123")
        configs = manager._get_service_specific_configs()
        assert configs["spark.openlineage.transport.domainId"] == "dzd-custom-123"

    def test_no_glue_specific_configs(self, manager):
        manager.project = MagicMock(domain_id="dzd-test")
        configs = manager._get_service_specific_configs()
        assert "spark.glue.accountId" not in configs
        assert "spark.glue.JOB_NAME" not in configs
        assert "spark.openlineage.facets.custom_environment_variables" not in configs

    def test_openlineage_graceful_failure_without_project(self, manager):
        # project not set — accessing self.project.domain_id raises AttributeError
        configs = manager._get_service_specific_configs()
        # Compatibility mode configs should still be present
        assert "spark.hadoop.fs.s3.credentialsResolverClass" in configs
        # OpenLineage configs should be absent (caught by try/except)
        assert "spark.extraListeners" not in configs

    def test_openlineage_disabled_via_overrides(self):
        from sagemaker_studio.data_models import ClientConfig

        config = ClientConfig(overrides={"emr-containers": {"enable_open_lineage": False}})
        mgr = EmrEksSparkSessionManager(connection=_make_connection(), config=config)
        mgr.project = MagicMock(domain_id="dzd-test")
        configs = mgr._get_service_specific_configs()
        assert "spark.hadoop.fs.s3.credentialsResolverClass" in configs
        assert "spark.extraListeners" not in configs
        assert "spark.openlineage.transport.type" not in configs

    def test_merges_s3_access_grants_configs(self, manager):
        """S3 Access Grants configs should be merged into the service configs."""
        manager.project = MagicMock(domain_id="dzd-test")
        s3ag_configs = {
            "spark.hadoop.fs.s3.s3AccessGrants.enabled": "true",
            "spark.hadoop.fs.s3.s3AccessGrants.fallbackToIAM": "true",
        }

        with patch.object(manager, "_get_s3_access_grants_configs", return_value=s3ag_configs):
            configs = manager._get_service_specific_configs()

        assert configs["spark.hadoop.fs.s3.s3AccessGrants.enabled"] == "true"
        assert configs["spark.hadoop.fs.s3.s3AccessGrants.fallbackToIAM"] == "true"


class TestGetS3AccessGrantsConfigs:
    """Logic lives in spark_config_builder.generate_s3_access_grants_configs and is tested
    there; these cover this manager's delegation to it."""

    def test_delegates_to_shared_builder_with_project(self, manager):
        manager.project = MagicMock()
        s3ag_configs = {
            "spark.hadoop.fs.s3.s3AccessGrants.enabled": "true",
            "spark.hadoop.fs.s3.s3AccessGrants.fallbackToIAM": "true",
        }
        with patch(
            f"{_MODULE}.generate_s3_access_grants_configs",
            return_value=s3ag_configs,
        ) as mock_generate:
            result = manager._get_s3_access_grants_configs()

        mock_generate.assert_called_once_with(manager.project)
        assert result == s3ag_configs

    def test_returns_empty_without_project(self, manager):
        """project is unset until _lazy_init, so the delegate must not raise."""
        assert manager._get_s3_access_grants_configs() == {}


class TestStopErrorHandling:
    def test_swallows_spark_stop_error(self, manager):
        spark = MagicMock()
        spark.stop.side_effect = RuntimeError("grpc closed")
        client = MagicMock()
        manager._spark_session = spark
        manager._emr_client = client
        manager.virtual_cluster_id = _VC_ID
        manager.endpoint_id = _ENDPOINT_ID
        manager.stop()  # must not raise
        assert manager._spark_session is None
        client.delete_managed_endpoint.assert_called_once()
        assert manager.endpoint_id is None

    def test_swallows_delete_endpoint_error(self, manager):
        client = MagicMock()
        client.delete_managed_endpoint.side_effect = RuntimeError("boom")
        manager._spark_session = None
        manager._emr_client = client
        manager.virtual_cluster_id = _VC_ID
        manager.endpoint_id = _ENDPOINT_ID
        manager.stop()  # must not raise
        assert manager.endpoint_id is None


class TestGetSessionId:
    def test_returns_endpoint_id(self, manager):
        manager.endpoint_id = _ENDPOINT_ID
        assert manager.get_session_id() == _ENDPOINT_ID
