from dataclasses import make_dataclass

from sagemaker_studio.connections.sql_helper.oracle_sql_helper import OracleSQLHelper

oracle_connection = make_dataclass("Connection", ["secret", "connection_creds", "data"])(
    {"username": "ADMIN", "password": "OraclePass123"},
    make_dataclass("ConnectionCredentials", [])(),
    make_dataclass("ConnectionData", ["physical_endpoints"])(
        [
            make_dataclass("PhysicalEndpoint", ["awsLocation", "glueConnection"])(
                awsLocation={"awsRegion": "eu-central-1"},
                glueConnection=make_dataclass("GlueConnection", ["connectionProperties"])(
                    connectionProperties={
                        "DATABASE": "myservice_high.adb.oraclecloud.com",
                        "HOST": "adb.eu-frankfurt-1.oraclecloud.com",
                        "PORT": "1521",
                    },
                ),
            )
        ]
    ),
)


class TestOracleSQLHelper:
    """Test suite for OracleSQLHelper."""

    def test_to_sql_config_returns_expected_keys(self):
        """Test that to_sql_config returns all required keys."""
        config = OracleSQLHelper.to_sql_config(oracle_connection)

        assert "host" in config
        assert "port" in config
        assert "user" in config
        assert "password" in config
        assert "database" in config

    def test_to_sql_config_extracts_host(self):
        """Test that host is extracted from connection properties."""
        config = OracleSQLHelper.to_sql_config(oracle_connection)

        assert config["host"] == "adb.eu-frankfurt-1.oraclecloud.com"

    def test_to_sql_config_extracts_port_as_int(self):
        """Test that port is extracted and converted to int."""
        config = OracleSQLHelper.to_sql_config(oracle_connection)

        assert config["port"] == 1521
        assert isinstance(config["port"], int)

    def test_to_sql_config_extracts_database(self):
        """Test that database (service name) is extracted from connection properties."""
        config = OracleSQLHelper.to_sql_config(oracle_connection)

        assert config["database"] == "myservice_high.adb.oraclecloud.com"

    def test_to_sql_config_extracts_user_from_secret(self):
        """Test that user is extracted from the connection secret."""
        config = OracleSQLHelper.to_sql_config(oracle_connection)

        assert config["user"] == "ADMIN"

    def test_to_sql_config_extracts_password_from_secret(self):
        """Test that password is extracted from the connection secret."""
        config = OracleSQLHelper.to_sql_config(oracle_connection)

        assert config["password"] == "OraclePass123"
