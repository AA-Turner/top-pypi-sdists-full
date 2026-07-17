"""
Unit tests for TeraDataSQLHelper.

Tests the Teradata SQL helper functionality including extraction of
connection properties and secret values into a SQL config dictionary.
"""

from dataclasses import make_dataclass

from sagemaker_studio.connections.sql_helper.teradata_sql_helper import TeraDataSQLHelper

teradata_connection = make_dataclass("Connection", ["secret", "connection_creds", "data"])(
    {"username": "td_user", "password": "TeraPass456"},
    make_dataclass("ConnectionCredentials", [])(),
    make_dataclass("ConnectionData", ["physical_endpoints"])(
        [
            make_dataclass("PhysicalEndpoint", ["awsLocation", "glueConnection"])(
                awsLocation={"awsRegion": "us-west-2"},
                glueConnection=make_dataclass("GlueConnection", ["connectionProperties"])(
                    connectionProperties={
                        "DATABASE": "enterprise_dw",
                        "HOST": "td-server.example.com",
                        "PORT": "1025",
                    },
                ),
            )
        ]
    ),
)


class TestTeraDataSQLHelper:
    """Test suite for TeraDataSQLHelper."""

    def test_to_sql_config_returns_expected_keys(self):
        """Test that to_sql_config returns all required keys."""
        config = TeraDataSQLHelper.to_sql_config(teradata_connection)

        assert "host" in config
        assert "port" in config
        assert "user" in config
        assert "password" in config
        assert "database" in config

    def test_to_sql_config_extracts_host(self):
        """Test that host is extracted from connection properties."""
        config = TeraDataSQLHelper.to_sql_config(teradata_connection)

        assert config["host"] == "td-server.example.com"

    def test_to_sql_config_extracts_port_as_int(self):
        """Test that port is extracted and converted to int."""
        config = TeraDataSQLHelper.to_sql_config(teradata_connection)

        assert config["port"] == 1025
        assert isinstance(config["port"], int)

    def test_to_sql_config_extracts_database(self):
        """Test that database is extracted from connection properties."""
        config = TeraDataSQLHelper.to_sql_config(teradata_connection)

        assert config["database"] == "enterprise_dw"

    def test_to_sql_config_extracts_user_from_secret(self):
        """Test that user is extracted from the connection secret."""
        config = TeraDataSQLHelper.to_sql_config(teradata_connection)

        assert config["user"] == "td_user"

    def test_to_sql_config_extracts_password_from_secret(self):
        """Test that password is extracted from the connection secret."""
        config = TeraDataSQLHelper.to_sql_config(teradata_connection)

        assert config["password"] == "TeraPass456"
