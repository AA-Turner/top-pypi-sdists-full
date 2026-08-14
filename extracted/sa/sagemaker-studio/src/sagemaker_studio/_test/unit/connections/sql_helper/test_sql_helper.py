from dataclasses import make_dataclass

from sagemaker_studio.connections.sql_helper.athena_sql_helper import AthenaSqlHelper
from sagemaker_studio.connections.sql_helper.big_query_sql_helper import BigQuerySqlHelper
from sagemaker_studio.connections.sql_helper.ddb_sql_helper import DDBSQLHelper
from sagemaker_studio.connections.sql_helper.mssql_sql_helper import MSSQLHelper
from sagemaker_studio.connections.sql_helper.mysql_sql_helper import MySQLHelper
from sagemaker_studio.connections.sql_helper.postgresql_helper import PostgreSQLHelper
from sagemaker_studio.connections.sql_helper.redshift_sql_helper import RedshiftSqlHelper
from sagemaker_studio.connections.sql_helper.snowflake_sql_helper import SnowflakeSqlHelper
from sagemaker_studio.connections.sql_helper.teradata_sql_helper import TeraDataSQLHelper
from sagemaker_studio.sql_engine.snowflake_transformer import SnowflakeAuthType

connection = make_dataclass("Connection", ["secret", "connection_creds", "data"])(
    {"username": "admin", "password": "secret"},
    make_dataclass("ConnectionCredentials", [])(),
    make_dataclass("ConnectionData", ["physical_endpoints"])(
        [
            make_dataclass("PhysicalEndpoint", ["awsLocation", "glueConnection"])(
                awsLocation={"awsRegion": "us-east-1"},
                glueConnection=make_dataclass("GlueConnection", ["connectionProperties"])(
                    connectionProperties={
                        "DATABASE": "sales",
                        "HOST": "db.example.com",
                        "PORT": "1433",
                        "WAREHOUSE": "wh1",
                    },
                ),
            )
        ]
    ),
)

snowflake_connection = make_dataclass("Connection", ["secret", "connection_creds", "data"])(
    {"username": "admin", "password": "secret"},
    make_dataclass("ConnectionCredentials", [])(),
    make_dataclass("ConnectionData", ["physical_endpoints"])(
        [
            make_dataclass("PhysicalEndpoint", ["awsLocation", "glueConnection"])(
                awsLocation={"awsRegion": "us-east-1"},
                glueConnection=make_dataclass("GlueConnection", ["connectionProperties"])(
                    connectionProperties={
                        "DATABASE": "sales",
                        "HOST": "db.example.com.snowflakecomputing.com",
                        "PORT": "1433",
                        "WAREHOUSE": "wh1",
                    },
                ),
            )
        ]
    ),
)

snowflake_pem_connection = make_dataclass("Connection", ["secret", "connection_creds", "data"])(
    {"sfUser": "SVC_ACCOUNT", "pem_private_key": "MIIBfakekey=="},
    make_dataclass("ConnectionCredentials", [])(),
    make_dataclass("ConnectionData", ["physical_endpoints"])(
        [
            make_dataclass("PhysicalEndpoint", ["awsLocation", "glueConnection"])(
                awsLocation={"awsRegion": "us-east-1"},
                glueConnection=make_dataclass("GlueConnection", ["connectionProperties"])(
                    connectionProperties={
                        "DATABASE": "sales",
                        "HOST": "db.example.com.snowflakecomputing.com",
                        "PORT": "1433",
                        "WAREHOUSE": "wh1",
                    },
                ),
            )
        ]
    ),
)

athena_connection = make_dataclass("Connection", ["secret", "connection_creds", "data"])(
    {},
    make_dataclass(
        "ConnectionCredentials", ["access_key_id", "secret_access_key", "session_token"]
    )(
        access_key_id="dummy_access_key_id",
        secret_access_key="dummy_secret_access_key",
        session_token="dummy_session_token",
    ),
    make_dataclass("ConnectionData", ["physical_endpoints", "workgroup_name", "connection_creds"])(
        physical_endpoints=[
            make_dataclass("PhysicalEndpoint", ["awsLocation"])(
                awsLocation={"awsRegion": "us-east-1"}
            )
        ],
        workgroup_name="test-workgroup",
        connection_creds={
            "access_key_id": "dummy_access_key_id",
            "secret_access_key": "dummy_secret_access_key",
            "session_token": "dummy_session_token",
        },
    ),
)


redshift_connection = make_dataclass(
    "Connection", ["secret", "connection_creds", "data", "_find_secret_arn"]
)(
    {},
    make_dataclass(
        "ConnectionCredentials", ["access_key_id", "secret_access_key", "session_token"]
    )(
        access_key_id="dummy_access_key_id",
        secret_access_key="dummy_secret_access_key",
        session_token="dummy_session_token",
    ),
    make_dataclass(
        "ConnectionData",
        ["physical_endpoints", "database_name", "storage", "connection_creds"],
    )(
        physical_endpoints=[
            make_dataclass("PhysicalEndpoint", ["awsLocation"])(
                awsLocation={"awsRegion": "us-west-2"}
            )
        ],
        database_name="default_db",
        storage={"workgroupName": "my-workgroup", "clusterName": "my-cluster"},
        connection_creds={
            "access_key_id": "dummy_access_key_id",
            "secret_access_key": "dummy_secret_access_key",
            "session_token": "dummy_session_token",
        },
    ),
    lambda: (_ for _ in ()).throw(Exception("no secret arn")),
)


def test_to_big_query_helper_sql_config_returns_secret_identity():
    result = BigQuerySqlHelper.to_sql_config(connection)
    assert result == {"password": "secret", "username": "admin"}


def test_to_ddb_helper_sql_config_returns_secret_identity():
    result = DDBSQLHelper.to_sql_config(connection)
    assert result == {"region": "us-east-1"}


def test_to_mssql_helper_sql_config_returns_secret_identity():
    result = MSSQLHelper.to_sql_config(connection)
    assert result == {
        "host": "db.example.com",
        "port": 1433,
        "user": "admin",
        "database": "sales",
        "password": "secret",
    }


def test_to_mysql_helper_sql_config_returns_secret_identity():
    result = MySQLHelper.to_sql_config(connection)
    assert result == {
        "host": "db.example.com",
        "port": 1433,
        "user": "admin",
        "database": "sales",
        "password": "secret",
    }


def test_to_postgres_helper_sql_config_returns_secret_identity():
    result = PostgreSQLHelper.to_sql_config(connection)
    assert result == {
        "host": "db.example.com",
        "port": 1433,
        "user": "admin",
        "database": "sales",
        "password": "secret",
    }


def test_to_teradata_helper_sql_config_returns_secret_identity():
    result = TeraDataSQLHelper.to_sql_config(connection)
    assert result == {
        "host": "db.example.com",
        "port": 1433,
        "user": "admin",
        "database": "sales",
        "password": "secret",
    }


def test_to_snowflake_helper_sql_config_returns_secret_identity():
    result = SnowflakeSqlHelper.to_sql_config(snowflake_connection)
    assert result == {
        "host": "db.example.com.snowflakecomputing.com",
        "port": 1433,
        "user": "admin",
        "database": "sales",
        "password": "secret",
        "account": "db.example.com.us-east-1",
        "region": "us-east-1",
        "warehouse": "wh1",
        "auth_type": SnowflakeAuthType.USERNAME_PASSWORD,
    }


def test_to_snowflake_helper_sql_config_pem_private_key():
    result = SnowflakeSqlHelper.to_sql_config(snowflake_pem_connection)
    assert result["auth_type"] == SnowflakeAuthType.PEM_PRIVATE_KEY
    assert result["user"] == "SVC_ACCOUNT"
    assert result["private_key"] == "MIIBfakekey=="
    assert "password" not in result
    assert "sfUser" not in result
    assert "pem_private_key" not in result


def test_to_athena_helper_sql_config_returns_basic_config():
    result = AthenaSqlHelper.to_sql_config(athena_connection)
    assert result == {
        "region": "us-east-1",
        "work_group": "test-workgroup",
        "aws_access_key_id": "dummy_access_key_id",
        "aws_secret_access_key": "dummy_secret_access_key",
        "aws_session_token": "dummy_session_token",
    }


def test_to_athena_helper_sql_config_with_override():
    result = AthenaSqlHelper.to_sql_config(
        athena_connection, catalog_name="test_catalog", schema_name="test_schema"
    )
    assert result == {
        "region": "us-east-1",
        "work_group": "test-workgroup",
        "aws_access_key_id": "dummy_access_key_id",
        "aws_secret_access_key": "dummy_secret_access_key",
        "aws_session_token": "dummy_session_token",
        "catalog_name": "test_catalog",
        "schema_name": "test_schema",
    }


def test_to_redshift_helper_sql_config_uses_connection_default_database():
    result = RedshiftSqlHelper.to_sql_config(redshift_connection)
    assert result["database_name"] == "default_db"
    assert result["region"] == "us-west-2"
    assert result["workgroup_name"] == "my-workgroup"
    assert result["cluster_identifier"] == "my-cluster"
    assert result["secret_arn"] is None
    assert result["aws_access_key_id"] == "dummy_access_key_id"
    assert result["aws_secret_access_key"] == "dummy_secret_access_key"
    assert result["aws_session_token"] == "dummy_session_token"


def test_to_redshift_helper_sql_config_uses_user_selected_database():
    result = RedshiftSqlHelper.to_sql_config(redshift_connection, database_name="user_selected_db")
    assert result["database_name"] == "user_selected_db"


def test_to_athena_helper_sql_config_with_credential_provider():
    """Test Athena helper uses credential_provider when provided"""

    def mock_credential_provider():
        return {
            "access_key_id": "refreshed_key",
            "secret_access_key": "refreshed_secret",
            "session_token": "refreshed_token",
        }

    result = AthenaSqlHelper.to_sql_config(
        athena_connection, credential_provider=mock_credential_provider
    )

    assert result == {
        "region": "us-east-1",
        "work_group": "test-workgroup",
        "credential_provider": mock_credential_provider,
    }
    assert "aws_access_key_id" not in result
    assert "aws_secret_access_key" not in result


def test_to_redshift_helper_sql_config_with_credential_provider():
    """Test Redshift helper uses credential_provider when provided"""
    from sagemaker_studio.connections.sql_helper.redshift_sql_helper import RedshiftSqlHelper

    redshift_connection = make_dataclass(
        "Connection", ["secret", "connection_creds", "data", "_find_secret_arn"]
    )(
        {},
        make_dataclass(
            "ConnectionCredentials", ["access_key_id", "secret_access_key", "session_token"]
        )(
            access_key_id="dummy_access_key_id",
            secret_access_key="dummy_secret_access_key",
            session_token="dummy_session_token",
        ),
        make_dataclass(
            "ConnectionData", ["physical_endpoints", "database_name", "storage", "connection_creds"]
        )(
            physical_endpoints=[
                make_dataclass("PhysicalEndpoint", ["awsLocation"])(
                    awsLocation={"awsRegion": "us-east-1"}
                )
            ],
            database_name="test-db",
            storage={"workgroupName": "test-workgroup"},
            connection_creds={
                "access_key_id": "dummy_access_key_id",
                "secret_access_key": "dummy_secret_access_key",
                "session_token": "dummy_session_token",
            },
        ),
        lambda: None,  # _find_secret_arn method
    )

    def mock_credential_provider():
        return {
            "access_key_id": "refreshed_key",
            "secret_access_key": "refreshed_secret",
            "session_token": "refreshed_token",
        }

    result = RedshiftSqlHelper.to_sql_config(
        redshift_connection, credential_provider=mock_credential_provider
    )

    assert result["credential_provider"] == mock_credential_provider
    assert "aws_access_key_id" not in result
    assert "aws_secret_access_key" not in result
    assert result["region"] == "us-east-1"
    assert result["workgroup_name"] == "test-workgroup"
    assert result["database_name"] == "test-db"


def test_to_redshift_helper_sql_config_without_credential_provider():
    """Test Redshift helper uses static credentials when credential_provider not provided"""
    from sagemaker_studio.connections.sql_helper.redshift_sql_helper import RedshiftSqlHelper

    redshift_connection = make_dataclass(
        "Connection", ["secret", "connection_creds", "data", "_find_secret_arn"]
    )(
        {},
        make_dataclass(
            "ConnectionCredentials", ["access_key_id", "secret_access_key", "session_token"]
        )(
            access_key_id="dummy_access_key_id",
            secret_access_key="dummy_secret_access_key",
            session_token="dummy_session_token",
        ),
        make_dataclass(
            "ConnectionData", ["physical_endpoints", "database_name", "storage", "connection_creds"]
        )(
            physical_endpoints=[
                make_dataclass("PhysicalEndpoint", ["awsLocation"])(
                    awsLocation={"awsRegion": "us-east-1"}
                )
            ],
            database_name="test-db",
            storage={"workgroupName": "test-workgroup"},
            connection_creds={
                "access_key_id": "dummy_access_key_id",
                "secret_access_key": "dummy_secret_access_key",
                "session_token": "dummy_session_token",
            },
        ),
        lambda: None,  # _find_secret_arn method
    )

    result = RedshiftSqlHelper.to_sql_config(redshift_connection)

    assert result["aws_access_key_id"] == "dummy_access_key_id"
    assert result["aws_secret_access_key"] == "dummy_secret_access_key"
    assert result["aws_session_token"] == "dummy_session_token"
    assert "credential_provider" not in result
