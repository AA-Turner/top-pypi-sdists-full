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
                # Mock gRPC specific classes and functions
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

    # Mock the interceptors module to avoid importing the actual interceptors
    mock_interceptors = Mock()
    mock_interceptors.CustomChannelBuilder = Mock()
    sys.modules["sagemaker_studio.utils.spark.session.athena.interceptors"] = mock_interceptors

    from sagemaker_studio.utils.spark.session import spark_config_builder

_CONFIG_BUILDER_PATH = "sagemaker_studio.utils.spark.session.spark_config_builder"


@pytest.fixture(autouse=True)
def mock_utils_and_project(monkeypatch):
    """Fixture to mock InternalUtils and Project setup."""
    mock_utils = MagicMock()
    mock_utils._get_domain_region.return_value = "us-west-2"
    mock_utils._get_datazone_stage.return_value = "prod"
    monkeypatch.setattr(spark_config_builder, "_utils", mock_utils)
    monkeypatch.setattr(spark_config_builder, "_region", "us-west-2")
    monkeypatch.setattr(spark_config_builder, "_stage", "prod")

    mock_proj = MagicMock()
    monkeypatch.setattr(f"{_CONFIG_BUILDER_PATH}.Project", mock_proj)
    # Also mock _ensure_project so _generate_workday_irc_spark_configs gets the mock project
    monkeypatch.setattr(
        f"{_CONFIG_BUILDER_PATH}._ensure_project",
        lambda: mock_proj.return_value,
    )
    return mock_proj.return_value


# -------------------------------------------------------------------
# Tests for _get_account_id_from_arn
# -------------------------------------------------------------------
def test_get_account_id_from_arn_valid():
    arn = "arn:aws:iam::123456789012:role/MyRole"

    assert spark_config_builder._get_account_id_from_arn(arn) == "123456789012"


# -------------------------------------------------------------------
# Tests for _generate_spark_catalog_spark_configs
# -------------------------------------------------------------------
def test_generate_spark_catalog_spark_configs():
    configs = spark_config_builder._generate_spark_catalog_spark_configs("999888777666")
    assert (
        configs["spark.sql.catalog.spark_catalog.catalog-impl"]
        == "org.apache.iceberg.aws.glue.GlueCatalog"
    )
    assert configs["spark.sql.catalog.spark_catalog.glue.account-id"] == "999888777666"
    assert configs["spark.sql.catalog.spark_catalog.client.region"] == "us-west-2"
    assert "spark.sql.catalog.spark_catalog" in configs


# -------------------------------------------------------------------
# Tests for _generate_s3tables_spark_configs
# -------------------------------------------------------------------
def test_generate_s3tables_spark_configs_with_federated_catalog(mock_utils_and_project):
    catalog = MagicMock()
    catalog.type = "FEDERATED"
    catalog.name = "prod_catalog"
    catalog.id = "cat-prod"
    catalog.resource_arn = "arn:aws:glue:us-west-2:123456789012:catalog/prod_catalog"
    catalog.federated_catalog = {"ConnectionName": "aws:s3tables", "Identifier": "s3://bucket/prod"}

    mock_utils_and_project.connection.return_value.catalogs = [catalog]

    conf = spark_config_builder._generate_s3tables_spark_configs()
    assert conf["spark.sql.catalog.prod_catalog"] == "org.apache.iceberg.spark.SparkCatalog"
    assert (
        conf["spark.sql.catalog.prod_catalog.catalog-impl"]
        == "org.apache.iceberg.aws.glue.GlueCatalog"
    )
    assert conf["spark.sql.catalog.prod_catalog.glue.catalog-arn"] == catalog.resource_arn
    assert conf["spark.sql.catalog.prod_catalog.client.region"] == "us-west-2"
    assert conf["spark.sql.catalog.prod_catalog.glue.lakeformation-enabled"] == "true"
    assert conf["spark.sql.catalog.prod_catalog.glue.lakeformation-enabled"] == "true"


def test_generate_s3tables_spark_configs_ignores_non_federated(mock_utils_and_project):
    catalog = MagicMock()
    catalog.type = "OTHER"
    catalog.federated_catalog = {}
    mock_utils_and_project.connection.return_value.catalogs = [catalog]

    conf = spark_config_builder._generate_s3tables_spark_configs()
    assert conf == {}  # no config should be generated


# -------------------------------------------------------------------
# Tests for generate_spark_configs (integration)
# -------------------------------------------------------------------
@patch(
    f"{_CONFIG_BUILDER_PATH}._generate_spark_catalog_spark_configs",
    return_value={"a": "b"},
)
@patch(
    f"{_CONFIG_BUILDER_PATH}._generate_s3tables_spark_configs",
    return_value={"c": "d"},
)
@patch(
    f"{_CONFIG_BUILDER_PATH}._generate_workday_irc_spark_configs",
    return_value={},
)
def test_generate_spark_configs_combines_all(mock_workday, mock_s3, mock_catalog):
    configs = spark_config_builder.generate_spark_configs("999888777666")
    assert configs["a"] == "b"
    assert configs["c"] == "d"
    assert "spark.sql.catalogImplementation" in configs


# -------------------------------------------------------------------
# Tests for _generate_workday_irc_spark_configs
# -------------------------------------------------------------------
def test_generate_workday_irc_spark_configs_single_catalog(mock_utils_and_project):
    mock_conn = MagicMock()
    mock_conn.type = "WORKDAYICEBERGRESTCATALOG"
    mock_conn._spark_catalog_configs.return_value = {
        "SOURCE_CATALOG_LIST": '["wd_catalog"]',
        "INSTANCE_URL": "https://workday.example.com/api",
        "ACCESS_TOKEN": "token_abc",
        "TENANT_ID": "tenant_xyz",
    }
    mock_utils_and_project.connections = [mock_conn]

    conf = spark_config_builder._generate_workday_irc_spark_configs()

    assert conf["spark.sql.catalog.wd_catalog"] == "org.apache.iceberg.spark.SparkCatalog"
    assert conf["spark.sql.catalog.wd_catalog.type"] == "rest"
    assert conf["spark.sql.catalog.wd_catalog.uri"] == "https://workday.example.com/api"
    assert conf["spark.sql.catalog.wd_catalog.warehouse"] == "wd_catalog"
    assert conf["spark.sql.catalog.wd_catalog.header.Polaris-Realm"] == "tenant_xyz"
    assert conf["spark.sql.catalog.wd_catalog.token"] == "token_abc"
    assert (
        conf["spark.sql.catalog.wd_catalog.header.X-Iceberg-Access-Delegation"]
        == "vended-credentials"
    )


def test_generate_workday_irc_spark_configs_multiple_catalogs(mock_utils_and_project):
    mock_conn = MagicMock()
    mock_conn.type = "WORKDAYICEBERGRESTCATALOG"
    mock_conn._spark_catalog_configs.return_value = {
        "SOURCE_CATALOG_LIST": '["cat_a", "cat_b"]',
        "INSTANCE_URL": "https://wd.example.com",
        "ACCESS_TOKEN": "tok",
        "TENANT_ID": "realm1",
    }
    mock_utils_and_project.connections = [mock_conn]

    conf = spark_config_builder._generate_workday_irc_spark_configs()

    assert conf["spark.sql.catalog.cat_a.uri"] == "https://wd.example.com"
    assert conf["spark.sql.catalog.cat_b.uri"] == "https://wd.example.com"
    assert conf["spark.sql.catalog.cat_a.warehouse"] == "cat_a"
    assert conf["spark.sql.catalog.cat_b.warehouse"] == "cat_b"


def test_generate_workday_irc_spark_configs_no_workday_connections(mock_utils_and_project):
    mock_conn = MagicMock()
    mock_conn.type = "ATHENA"
    mock_utils_and_project.connections = [mock_conn]

    conf = spark_config_builder._generate_workday_irc_spark_configs()
    assert conf == {}


def test_generate_workday_irc_spark_configs_no_connections(mock_utils_and_project):
    mock_utils_and_project.connections = []

    conf = spark_config_builder._generate_workday_irc_spark_configs()
    assert conf == {}


def test_generate_workday_irc_spark_configs_mixed_connections(mock_utils_and_project):
    mock_athena = MagicMock()
    mock_athena.type = "ATHENA"

    mock_workday = MagicMock()
    mock_workday.type = "WORKDAYICEBERGRESTCATALOG"
    mock_workday._spark_catalog_configs.return_value = {
        "SOURCE_CATALOG_LIST": '["wdc"]',
        "INSTANCE_URL": "https://wd.test.com",
        "ACCESS_TOKEN": "t",
        "TENANT_ID": "r",
    }
    mock_utils_and_project.connections = [mock_athena, mock_workday]

    conf = spark_config_builder._generate_workday_irc_spark_configs()

    assert "spark.sql.catalog.wdc" in conf
    assert conf["spark.sql.catalog.wdc.token"] == "t"
    mock_athena._spark_catalog_configs.assert_not_called()
