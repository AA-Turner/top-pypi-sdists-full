"""
Unit tests for OracleTransformer.

Tests the Oracle connection transformer functionality including
connection string generation, parameter validation, and configuration.
"""

from unittest.mock import MagicMock, patch

import pytest

from sagemaker_studio.sql_engine.oracle_transformer import OracleTransformer


@pytest.fixture(autouse=True)
def mock_oracledb():
    """Mock oracledb module for all tests since it may not be installed in the build environment."""
    mock_module = MagicMock()
    with patch.dict("sys.modules", {"oracledb": mock_module}):
        yield mock_module


class TestOracleTransformer:
    """Test suite for OracleTransformer."""

    def test_get_required_fields(self):
        """Test that all required fields are returned."""
        required = OracleTransformer.get_required_fields()
        assert required == ["host", "port", "database", "user", "password"]

    def test_get_dialect(self):
        """Test that the correct dialect is returned."""
        assert OracleTransformer.get_dialect() == "oracle"

    def test_to_sqlalchemy_config_success(self):
        """Test successful transformation to SQLAlchemy config."""
        connection_data = {
            "host": "oracle.example.com",
            "port": 1521,
            "database": "ORCL",
            "user": "dbadmin",
            "password": "secret123",
        }

        config = OracleTransformer.to_sqlalchemy_config(connection_data)

        assert config["connection_string"] == "oracle+oracledb://@"
        assert callable(config["creator"])
        assert config["isolation_level"] == "AUTOCOMMIT"
        assert config["thick_mode"] is False

    def test_to_sqlalchemy_config_missing_host(self):
        """Test that missing host raises ValueError."""
        connection_data = {
            "port": 1521,
            "database": "ORCL",
            "user": "dbadmin",
            "password": "secret123",
        }

        with pytest.raises(ValueError, match="host is required"):
            OracleTransformer.to_sqlalchemy_config(connection_data)

    def test_to_sqlalchemy_config_missing_port(self):
        """Test that missing port raises ValueError."""
        connection_data = {
            "host": "oracle.example.com",
            "database": "ORCL",
            "user": "dbadmin",
            "password": "secret123",
        }

        with pytest.raises(ValueError, match="port is required"):
            OracleTransformer.to_sqlalchemy_config(connection_data)

    def test_to_sqlalchemy_config_missing_database(self):
        """Test that missing database raises ValueError."""
        connection_data = {
            "host": "oracle.example.com",
            "port": 1521,
            "user": "dbadmin",
            "password": "secret123",
        }

        with pytest.raises(ValueError, match="database is required"):
            OracleTransformer.to_sqlalchemy_config(connection_data)

    def test_to_sqlalchemy_config_missing_user(self):
        """Test that missing user raises ValueError."""
        connection_data = {
            "host": "oracle.example.com",
            "port": 1521,
            "database": "ORCL",
            "password": "secret123",
        }

        with pytest.raises(ValueError, match="user is required"):
            OracleTransformer.to_sqlalchemy_config(connection_data)

    def test_to_sqlalchemy_config_missing_password(self):
        """Test that missing password raises ValueError."""
        connection_data = {
            "host": "oracle.example.com",
            "port": 1521,
            "database": "ORCL",
            "user": "dbadmin",
        }

        with pytest.raises(ValueError, match="password is required"):
            OracleTransformer.to_sqlalchemy_config(connection_data)

    def test_to_sqlalchemy_config_with_special_characters(self):
        """Test config with special characters in password still produces a creator."""
        connection_data = {
            "host": "oracle.example.com",
            "port": 1521,
            "database": "ORCL",
            "user": "dbadmin",
            "password": "p@ssw0rd!#$",
        }

        config = OracleTransformer.to_sqlalchemy_config(connection_data)

        assert "creator" in config
        assert callable(config["creator"])
        assert config["connection_string"] == "oracle+oracledb://@"

    def test_to_sqlalchemy_config_with_special_characters_in_username(self):
        """Test config with special characters in both username and password."""
        connection_data = {
            "host": "oracle.example.com",
            "port": 1521,
            "database": "ORCL",
            "user": "db@admin",
            "password": "pass:word/123",
        }

        config = OracleTransformer.to_sqlalchemy_config(connection_data)

        assert "creator" in config
        assert callable(config["creator"])
        assert config["connection_string"] == "oracle+oracledb://@"

    def test_to_sqlalchemy_config_with_different_port(self):
        """Test config with non-default port."""
        connection_data = {
            "host": "oracle.example.com",
            "port": 1522,
            "database": "ORCL",
            "user": "dbadmin",
            "password": "secret123",
        }

        config = OracleTransformer.to_sqlalchemy_config(connection_data)

        assert "creator" in config
        assert config["connection_string"] == "oracle+oracledb://@"

    def test_get_loggers(self):
        """Test that correct logger names are returned."""
        loggers = OracleTransformer.get_loggers()
        assert loggers == ["oracledb"]

    def test_validate_required_fields_success(self):
        """Test successful validation of required fields."""
        required_fields = ["host", "port", "database"]
        connection_data = {"host": "oracle.example.com", "port": 1521, "database": "ORCL"}

        # Should not raise any exception
        OracleTransformer.validate_required_fields(required_fields, connection_data)

    def test_validate_required_fields_missing(self):
        """Test validation fails when field is missing."""
        required_fields = ["host", "port", "database"]
        connection_data = {"host": "oracle.example.com", "port": 1521}

        with pytest.raises(ValueError, match="database is required"):
            OracleTransformer.validate_required_fields(required_fields, connection_data)

    def test_validate_required_fields_empty_value(self):
        """Test validation fails when field value is empty."""
        required_fields = ["host", "port", "database"]
        connection_data = {
            "host": "oracle.example.com",
            "port": 1521,
            "database": "",  # Empty string
        }

        with pytest.raises(ValueError, match="database is required"):
            OracleTransformer.validate_required_fields(required_fields, connection_data)

    def test_to_sqlalchemy_config_none_value_field(self):
        """Test that a None value for a required field raises ValueError."""
        connection_data = {
            "host": "oracle.example.com",
            "port": 1521,
            "database": None,
            "user": "dbadmin",
            "password": "secret123",
        }
        with pytest.raises(ValueError, match="database is required"):
            OracleTransformer.to_sqlalchemy_config(connection_data)

    def test_to_sqlalchemy_config_creator_calls_oracledb_connect(self, mock_oracledb):
        """Test that the creator function calls oracledb.connect with correct params."""
        connection_data = {
            "host": "oracle.example.com",
            "port": 1521,
            "database": "ORCL",
            "user": "dbadmin",
            "password": "secret123",
        }

        config = OracleTransformer.to_sqlalchemy_config(connection_data)
        creator = config["creator"]

        # Call the creator
        creator()

        # Verify oracledb.connect was called with the correct DSN
        mock_oracledb.connect.assert_called_once_with(
            user="dbadmin",
            password="secret123",
            dsn=(
                "(description="
                "(retry_count=20)(retry_delay=3)"
                "(address=(protocol=tcps)(port=1521)(host=oracle.example.com))"
                "(connect_data=(service_name=ORCL))"
                "(security=(ssl_server_dn_match=yes)))"
            ),
        )

    def test_to_sqlalchemy_config_dsn_format(self, mock_oracledb):
        """Test that the DSN descriptor is correctly formatted."""
        connection_data = {
            "host": "adb.us-east-1.oraclecloud.com",
            "port": 1522,
            "database": "myservice_high.adb.oraclecloud.com",
            "user": "ADMIN",
            "password": "MyPass123",
        }

        config = OracleTransformer.to_sqlalchemy_config(connection_data)
        creator = config["creator"]
        creator()

        call_args = mock_oracledb.connect.call_args
        dsn = call_args.kwargs["dsn"]

        assert "(retry_count=20)" in dsn
        assert "(retry_delay=3)" in dsn
        assert "(protocol=tcps)" in dsn
        assert "(port=1522)" in dsn
        assert "(host=adb.us-east-1.oraclecloud.com)" in dsn
        assert "(service_name=myservice_high.adb.oraclecloud.com)" in dsn
        assert "(ssl_server_dn_match=yes)" in dsn

    def test_get_resources_action_database(self):
        """Test resource action for DATABASE type."""
        definition = OracleTransformer.get_resources_action("DATABASE")

        assert definition.default_type == "DATABASE"
        assert definition.children == ("TABLE",)

    def test_get_resources_action_table(self):
        """Test resource action for TABLE type."""
        definition = OracleTransformer.get_resources_action("TABLE")

        assert definition.default_type == "TABLE"
        assert definition.children == ("COLUMN",)

    def test_get_resources_action_column(self):
        """Test resource action for COLUMN type."""
        definition = OracleTransformer.get_resources_action("COLUMN")

        assert definition.default_type == "COLUMN"
        assert definition.children == ()

    def test_get_resources_action_none(self):
        """Test resource action with None defaults to DATABASE."""
        definition = OracleTransformer.get_resources_action(None)

        assert definition.default_type == "DATABASE"
        assert definition.children == ("TABLE",)

    def test_get_resources_action_invalid_type(self):
        """Test resource action with invalid type raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported resource type"):
            OracleTransformer.get_resources_action("INVALID_TYPE")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
