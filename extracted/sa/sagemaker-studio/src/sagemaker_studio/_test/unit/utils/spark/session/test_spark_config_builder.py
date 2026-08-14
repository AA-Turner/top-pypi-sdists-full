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
        _generate_glue_catalog_spark_configs,
        apply_compatibility_mode_configs,
        build_spark_configs,
        extract_connection_spark_configs,
        generate_s3_access_grants_configs,
    )

_CONFIG_BUILDER_PATH = "sagemaker_studio.utils.spark.session.spark_config_builder"


@pytest.fixture(autouse=True)
def mock_internals(monkeypatch):
    """Mock InternalUtils and _ensure_project for all tests."""
    mock_utils = MagicMock()
    mock_utils._get_domain_region.return_value = "us-west-2"
    mock_utils._get_datazone_stage.return_value = "prod"
    monkeypatch.setattr(spark_config_builder, "_utils", mock_utils)
    monkeypatch.setattr(spark_config_builder, "_region", "us-west-2")
    monkeypatch.setattr(spark_config_builder, "_stage", "prod")

    mock_proj = MagicMock()
    monkeypatch.setattr(f"{_CONFIG_BUILDER_PATH}._ensure_project", lambda: mock_proj)
    return mock_proj


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
        assert result["a"] == "user_a"
        assert result["b"] == "conn_b"
        assert result["c"] == "3"
        assert result["d"] == "service_d"

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
        conn = MagicMock(spec=[])
        result = extract_connection_spark_configs(conn)
        assert result == {}

    def test_returns_empty_on_exception(self):
        conn = MagicMock()
        conn._Connection__connection_data = None
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


# -------------------------------------------------------------------
# Tests for apply_compatibility_mode_configs
# -------------------------------------------------------------------


class TestApplyCompatibilityModeConfigs:
    def test_adds_all_compatibility_keys(self):
        result = apply_compatibility_mode_configs({})
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
            assert key in result

    def test_preserves_existing_configs(self):
        existing = {"spark.custom.key": "custom_val"}
        result = apply_compatibility_mode_configs(existing)
        assert result["spark.custom.key"] == "custom_val"
        assert "spark.hadoop.fs.s3.credentialsResolverClass" in result

    def test_returns_same_dict_mutated(self):
        existing = {"spark.a": "1"}
        result = apply_compatibility_mode_configs(existing)
        assert result is existing

    def test_lakeformation_credential_resolver_value(self):
        result = apply_compatibility_mode_configs({})
        assert result["spark.hadoop.fs.s3.credentialsResolverClass"] == (
            "com.amazonaws.glue.accesscontrol.AWSLakeFormationCredentialResolver"
        )


# -------------------------------------------------------------------
# Tests for _generate_glue_catalog_spark_configs
# -------------------------------------------------------------------


class TestGenerateGlueCatalogSparkConfigs:
    def test_generates_configs_for_non_federated_catalogs(self, mock_internals):
        catalog = MagicMock()
        catalog.type = "GLUE"
        catalog.spark_catalog_name = "my_catalog"
        catalog.id = "cat-123"
        catalog.resource_arn = "arn:aws:glue:us-west-2:111222333444:catalog/my_catalog"
        mock_internals.connection.return_value.catalogs = [catalog]

        result = _generate_glue_catalog_spark_configs(mock_internals)

        assert result["spark.sql.catalog.my_catalog"] == "org.apache.iceberg.spark.SparkCatalog"
        assert (
            result["spark.sql.catalog.my_catalog.catalog-impl"]
            == "org.apache.iceberg.aws.glue.GlueCatalog"
        )
        assert result["spark.sql.catalog.my_catalog.glue.id"] == "cat-123"
        assert result["spark.sql.catalog.my_catalog.glue.account-id"] == "111222333444"
        assert (
            result["spark.sql.catalog.my_catalog.glue.catalog-arn"]
            == "arn:aws:glue:us-west-2:111222333444:catalog/my_catalog"
        )
        assert result["spark.sql.catalog.my_catalog.client.region"] == "us-west-2"
        assert result["spark.sql.catalog.my_catalog.glue.lakeformation-enabled"] == "true"

    def test_skips_federated_catalogs(self, mock_internals):
        federated_catalog = MagicMock()
        federated_catalog.type = "FEDERATED"

        non_federated_catalog = MagicMock()
        non_federated_catalog.type = "GLUE"
        non_federated_catalog.spark_catalog_name = "good_catalog"
        non_federated_catalog.id = "cat-456"
        non_federated_catalog.resource_arn = "arn:aws:glue:us-west-2:111222333444:catalog/good"

        mock_internals.connection.return_value.catalogs = [federated_catalog, non_federated_catalog]

        result = _generate_glue_catalog_spark_configs(mock_internals)

        assert "spark.sql.catalog.good_catalog" in result
        assert len([k for k in result if k.startswith("spark.sql.catalog.good_catalog")]) == 7

    def test_respects_catalog_limit(self, mock_internals):
        catalogs = []
        for i in range(10):
            cat = MagicMock()
            cat.type = "GLUE"
            cat.spark_catalog_name = f"cat_{i}"
            cat.id = f"id-{i}"
            cat.resource_arn = f"arn:aws:glue:us-west-2:111222333444:catalog/cat_{i}"
            catalogs.append(cat)

        mock_internals.connection.return_value.catalogs = catalogs

        result = _generate_glue_catalog_spark_configs(mock_internals)

        # Should only have configs for CATALOG_LIMIT (7) catalogs
        catalog_names = set()
        for key in result:
            parts = key.split(".")
            if len(parts) >= 4:
                catalog_names.add(parts[3])
        assert len(catalog_names) == 7

    def test_returns_empty_when_no_catalogs(self, mock_internals):
        mock_internals.connection.return_value.catalogs = []
        result = _generate_glue_catalog_spark_configs(mock_internals)
        assert result == {}


# -------------------------------------------------------------------
# Tests for generate_s3_access_grants_configs
# -------------------------------------------------------------------


def _project_with_provisioned_resources(resources):
    proj = MagicMock()
    proj.domain_id = "dzd-s3ag-test"
    proj.id = "proj-s3ag"
    proj._sagemaker_studio_api.project_api.get_project_default_environment.return_value = {
        "provisionedResources": resources
    }
    return proj


class TestGenerateS3AccessGrantsConfigs:
    def test_returns_configs_when_enabled(self):
        proj = _project_with_provisioned_resources(
            [{"name": "enableS3AccessGrantsForTools", "value": "true"}]
        )

        result = generate_s3_access_grants_configs(proj)

        proj._sagemaker_studio_api.project_api.get_project_default_environment.assert_called_once_with(
            "dzd-s3ag-test", "proj-s3ag"
        )
        assert result == {
            "spark.hadoop.fs.s3.s3AccessGrants.enabled": "true",
            "spark.hadoop.fs.s3.s3AccessGrants.fallbackToIAM": "true",
        }

    def test_value_is_case_insensitive(self):
        proj = _project_with_provisioned_resources(
            [{"name": "enableS3AccessGrantsForTools", "value": "TRUE"}]
        )
        assert (
            generate_s3_access_grants_configs(proj)["spark.hadoop.fs.s3.s3AccessGrants.enabled"]
            == "true"
        )

    def test_returns_empty_when_disabled(self):
        proj = _project_with_provisioned_resources(
            [{"name": "enableS3AccessGrantsForTools", "value": "false"}]
        )
        assert generate_s3_access_grants_configs(proj) == {}

    def test_returns_empty_when_resource_absent(self):
        proj = _project_with_provisioned_resources([{"name": "somethingElse", "value": "true"}])
        assert generate_s3_access_grants_configs(proj) == {}

    def test_returns_empty_when_no_provisioned_resources_key(self):
        proj = MagicMock()
        proj._sagemaker_studio_api.project_api.get_project_default_environment.return_value = {}
        assert generate_s3_access_grants_configs(proj) == {}

    def test_returns_empty_on_api_exception(self):
        proj = MagicMock()
        proj._sagemaker_studio_api.project_api.get_project_default_environment.side_effect = (
            Exception("API error")
        )
        assert generate_s3_access_grants_configs(proj) == {}

    def test_returns_empty_when_project_is_none(self):
        """Callers pass getattr(self, "project", None), so None must not raise."""
        assert generate_s3_access_grants_configs(None) == {}
