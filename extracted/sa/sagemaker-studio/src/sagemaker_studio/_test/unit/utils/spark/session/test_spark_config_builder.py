"""Tests for spark_config_builder module."""

import sys
from unittest.mock import MagicMock, Mock, patch

import pytest

with patch("sagemaker_studio.Project"):
    sys.modules["pyspark"] = Mock()
    sys.modules["pyspark.sql"] = Mock()
    sys.modules["pyspark.sql.connect"] = Mock()
    sys.modules["pyspark.sql.connect.session"] = Mock()
    sys.modules["pyspark.sql.connect.client"] = Mock()

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
            elif module_name == "pyspark.sql.connect.client":
                mock_module.ChannelBuilder = Mock()
            sys.modules[module_name] = mock_module

    mock_interceptors = Mock()
    mock_interceptors.CustomChannelBuilder = Mock()
    sys.modules["sagemaker_studio.utils.spark.session.athena.interceptors"] = mock_interceptors
    sys.modules["sagemaker_studio.utils.spark.session.emr_serverless.interceptors"] = (
        mock_interceptors
    )

    from sagemaker_studio.utils.spark.session import spark_config_builder
    from sagemaker_studio.utils.spark.session.spark_config_builder import (
        DEFAULT_SPARK_PROPS,
        build_spark_configs,
        extract_connection_spark_configs,
    )

_CONFIG_BUILDER_PATH = "sagemaker_studio.utils.spark.session.spark_config_builder"


@pytest.fixture(autouse=True)
def mock_internals(monkeypatch):
    """Mock InternalUtils and Project for all tests."""
    mock_utils = MagicMock()
    mock_utils._get_domain_region.return_value = "us-west-2"
    mock_utils._get_datazone_stage.return_value = "prod"
    monkeypatch.setattr(spark_config_builder, "_utils", mock_utils)
    monkeypatch.setattr(spark_config_builder, "_region", "us-west-2")
    monkeypatch.setattr(spark_config_builder, "_stage", "prod")

    mock_proj = MagicMock()
    monkeypatch.setattr(f"{_CONFIG_BUILDER_PATH}.Project", mock_proj)
    return mock_proj.return_value


# -------------------------------------------------------------------
# Tests for DEFAULT_SPARK_PROPS
# -------------------------------------------------------------------


class TestDefaultSparkProps:
    def test_contains_hive_metastore_factory(self):
        assert "spark.hive.metastore.client.factory.class" in DEFAULT_SPARK_PROPS

    def test_contains_catalog_implementation(self):
        assert DEFAULT_SPARK_PROPS["spark.sql.catalogImplementation"] == "hive"

    def test_contains_iceberg_extensions(self):
        assert "spark.sql.extensions" in DEFAULT_SPARK_PROPS
        assert "IcebergSparkSessionExtensions" in DEFAULT_SPARK_PROPS["spark.sql.extensions"]

    def test_does_not_contain_lakeformation_credential_resolver(self):
        assert "spark.hadoop.fs.s3.credentialsResolverClass" not in DEFAULT_SPARK_PROPS

    def test_does_not_contain_compatibility_mode_keys(self):
        compat_keys = [
            "spark.hadoop.fs.s3.useDirectoryHeaderAsFolderObject",
            "spark.hadoop.fs.s3.folderObject.autoAction.disabled",
            "spark.sql.catalog.createDirectoryAfterTable.enabled",
            "spark.sql.catalog.dropDirectoryBeforeTable.enabled",
            "spark.sql.catalog.skipLocationValidationOnCreateTable.enabled",
        ]
        for key in compat_keys:
            assert key not in DEFAULT_SPARK_PROPS

    def test_only_contains_universal_keys(self):
        assert len(DEFAULT_SPARK_PROPS) == 3


# -------------------------------------------------------------------
# Tests for build_spark_configs
# -------------------------------------------------------------------


class TestBuildSparkConfigs:
    @patch(
        f"{_CONFIG_BUILDER_PATH}.generate_spark_configs",
        return_value={"base.key": "base_value"},
    )
    def test_returns_base_when_no_overrides(self, mock_gen):
        result = build_spark_configs(account_id="123")
        assert result == {"base.key": "base_value"}

    @patch(
        f"{_CONFIG_BUILDER_PATH}.generate_spark_configs",
        return_value={"base.key": "base_value"},
    )
    def test_service_configs_override_base(self, mock_gen):
        result = build_spark_configs(
            account_id="123",
            service_configs={"base.key": "service_override", "service.key": "svc"},
        )
        assert result["base.key"] == "service_override"
        assert result["service.key"] == "svc"

    @patch(
        f"{_CONFIG_BUILDER_PATH}.generate_spark_configs",
        return_value={"base.key": "base_value"},
    )
    def test_connection_configs_override_service(self, mock_gen):
        result = build_spark_configs(
            account_id="123",
            service_configs={"shared.key": "from_service"},
            connection_configs={"shared.key": "from_connection"},
        )
        assert result["shared.key"] == "from_connection"

    @patch(
        f"{_CONFIG_BUILDER_PATH}.generate_spark_configs",
        return_value={"base.key": "base_value"},
    )
    def test_user_configs_override_all(self, mock_gen):
        result = build_spark_configs(
            account_id="123",
            service_configs={"key": "service"},
            connection_configs={"key": "connection"},
            user_configs={"key": "user_wins"},
        )
        assert result["key"] == "user_wins"

    @patch(
        f"{_CONFIG_BUILDER_PATH}.generate_spark_configs",
        return_value={"a": "1", "b": "2", "c": "3"},
    )
    def test_full_layering_order(self, mock_gen):
        """Verify complete 4-layer priority: base < service < connection < user."""
        result = build_spark_configs(
            account_id="123",
            service_configs={"a": "service_a", "d": "service_d"},
            connection_configs={"a": "conn_a", "b": "conn_b"},
            user_configs={"a": "user_a"},
        )
        assert result["a"] == "user_a"  # user wins over all
        assert result["b"] == "conn_b"  # connection wins over base
        assert result["c"] == "3"  # base preserved
        assert result["d"] == "service_d"  # service addition preserved

    @patch(
        f"{_CONFIG_BUILDER_PATH}.generate_spark_configs",
        return_value={"base.key": "val"},
    )
    def test_none_layers_are_skipped(self, mock_gen):
        result = build_spark_configs(
            account_id="123",
            service_configs=None,
            connection_configs=None,
            user_configs=None,
        )
        assert result == {"base.key": "val"}

    @patch(
        f"{_CONFIG_BUILDER_PATH}.generate_spark_configs",
        return_value={"base.key": "val"},
    )
    def test_empty_dict_layers_are_harmless(self, mock_gen):
        result = build_spark_configs(
            account_id="123",
            service_configs={},
            connection_configs={},
            user_configs={},
        )
        assert result == {"base.key": "val"}


# -------------------------------------------------------------------
# Tests for extract_connection_spark_configs
# -------------------------------------------------------------------


class TestExtractConnectionSparkConfigs:
    def test_extracts_spark_configuration(self):
        conn = MagicMock()
        conn._Connection__connection_data = {
            "configurations": [
                {
                    "classification": "SparkConfiguration",
                    "properties": {"spark.custom.key": "custom_value"},
                }
            ]
        }
        result = extract_connection_spark_configs(conn)
        assert result == {"spark.custom.key": "custom_value"}

    def test_returns_empty_when_no_spark_configuration(self):
        conn = MagicMock()
        conn._Connection__connection_data = {
            "configurations": [{"classification": "SomeOtherConfig", "properties": {"key": "val"}}]
        }
        result = extract_connection_spark_configs(conn)
        assert result == {}

    def test_returns_empty_when_configurations_is_empty(self):
        conn = MagicMock()
        conn._Connection__connection_data = {"configurations": []}
        result = extract_connection_spark_configs(conn)
        assert result == {}

    def test_returns_empty_when_configurations_is_missing(self):
        conn = MagicMock()
        conn._Connection__connection_data = {}
        result = extract_connection_spark_configs(conn)
        assert result == {}

    def test_returns_empty_when_connection_data_is_missing(self):
        conn = MagicMock(spec=[])  # no attributes
        result = extract_connection_spark_configs(conn)
        assert result == {}

    def test_returns_empty_on_exception(self):
        conn = MagicMock()
        conn._Connection__connection_data = None  # will cause TypeError on .get()
        result = extract_connection_spark_configs(conn)
        assert result == {}

    def test_handles_multiple_classifications(self):
        conn = MagicMock()
        conn._Connection__connection_data = {
            "configurations": [
                {"classification": "HiveConfiguration", "properties": {"hive.key": "val"}},
                {
                    "classification": "SparkConfiguration",
                    "properties": {"spark.a": "1", "spark.b": "2"},
                },
                {"classification": "YarnConfiguration", "properties": {"yarn.key": "val"}},
            ]
        }
        result = extract_connection_spark_configs(conn)
        assert result == {"spark.a": "1", "spark.b": "2"}

    def test_returns_empty_dict_when_properties_is_empty(self):
        conn = MagicMock()
        conn._Connection__connection_data = {
            "configurations": [{"classification": "SparkConfiguration", "properties": {}}]
        }
        result = extract_connection_spark_configs(conn)
        assert result == {}

    def test_configurations_not_a_list(self):
        conn = MagicMock()
        conn._Connection__connection_data = {"configurations": "not_a_list"}
        result = extract_connection_spark_configs(conn)
        assert result == {}
