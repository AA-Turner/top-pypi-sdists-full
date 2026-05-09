"""
Unit tests for VerticaTransformer.

Tests the Vertica connection transformer functionality including
connection string generation, parameter validation, and configuration.
"""

import pytest

from sagemaker_studio.sql_engine.vertica_transformer import VerticaTransformer


class TestVerticaTransformer:
    """Test suite for VerticaTransformer."""

    def test_get_required_fields(self):
        """Test that all required fields are returned."""
        required = VerticaTransformer.get_required_fields()
        assert required == ["host", "port", "database", "user", "password"]

    def test_to_sqlalchemy_config_success(self):
        """Test successful transformation to SQLAlchemy config."""
        connection_data = {
            "host": "vertica.example.com",
            "port": 5433,
            "database": "analytics",
            "user": "dbadmin",
            "password": "secret123",
        }

        config = VerticaTransformer.to_sqlalchemy_config(connection_data)

        assert "connection_string" in config
        expected = "vertica+vertica_python://dbadmin:secret123@vertica.example.com:5433/analytics"
        assert config["connection_string"] == expected

    def test_to_sqlalchemy_config_missing_host(self):
        """Test that missing host raises ValueError."""
        connection_data = {
            "port": 5433,
            "database": "analytics",
            "user": "dbadmin",
            "password": "secret123",
        }

        with pytest.raises(ValueError, match="host is required"):
            VerticaTransformer.to_sqlalchemy_config(connection_data)

    def test_to_sqlalchemy_config_missing_port(self):
        """Test that missing port raises ValueError."""
        connection_data = {
            "host": "vertica.example.com",
            "database": "analytics",
            "user": "dbadmin",
            "password": "secret123",
        }

        with pytest.raises(ValueError, match="port is required"):
            VerticaTransformer.to_sqlalchemy_config(connection_data)

    def test_to_sqlalchemy_config_missing_database(self):
        """Test that missing database raises ValueError."""
        connection_data = {
            "host": "vertica.example.com",
            "port": 5433,
            "user": "dbadmin",
            "password": "secret123",
        }

        with pytest.raises(ValueError, match="database is required"):
            VerticaTransformer.to_sqlalchemy_config(connection_data)

    def test_to_sqlalchemy_config_missing_user(self):
        """Test that missing user raises ValueError."""
        connection_data = {
            "host": "vertica.example.com",
            "port": 5433,
            "database": "analytics",
            "password": "secret123",
        }

        with pytest.raises(ValueError, match="user is required"):
            VerticaTransformer.to_sqlalchemy_config(connection_data)

    def test_to_sqlalchemy_config_missing_password(self):
        """Test that missing password raises ValueError."""
        connection_data = {
            "host": "vertica.example.com",
            "port": 5433,
            "database": "analytics",
            "user": "dbadmin",
        }

        with pytest.raises(ValueError, match="password is required"):
            VerticaTransformer.to_sqlalchemy_config(connection_data)

    def test_to_sqlalchemy_config_with_special_characters(self):
        """Test connection string with special characters in password."""
        connection_data = {
            "host": "vertica.example.com",
            "port": 5433,
            "database": "analytics",
            "user": "dbadmin",
            "password": "p@ssw0rd!#$",
        }

        config = VerticaTransformer.to_sqlalchemy_config(connection_data)

        assert "connection_string" in config
        # Verify URL encoding: @ becomes %40, ! becomes %21, # becomes %23, $ becomes %24
        expected = "vertica+vertica_python://dbadmin:p%40ssw0rd%21%23%24@vertica.example.com:5433/analytics"
        assert config["connection_string"] == expected

    def test_to_sqlalchemy_config_with_special_characters_in_username(self):
        """Test connection string with special characters in both username and password."""
        connection_data = {
            "host": "vertica.example.com",
            "port": 5433,
            "database": "analytics",
            "user": "db@admin",
            "password": "pass:word/123",
        }

        config = VerticaTransformer.to_sqlalchemy_config(connection_data)

        assert "connection_string" in config
        # Verify URL encoding: @ becomes %40, : becomes %3A, / becomes %2F
        expected = "vertica+vertica_python://db%40admin:pass%3Aword%2F123@vertica.example.com:5433/analytics"
        assert config["connection_string"] == expected

    def test_to_sqlalchemy_config_with_different_port(self):
        """Test connection string with non-default port."""
        connection_data = {
            "host": "vertica.example.com",
            "port": 5444,
            "database": "analytics",
            "user": "dbadmin",
            "password": "secret123",
        }

        config = VerticaTransformer.to_sqlalchemy_config(connection_data)

        expected = "vertica+vertica_python://dbadmin:secret123@vertica.example.com:5444/analytics"
        assert config["connection_string"] == expected

    def test_get_loggers(self):
        """Test that correct logger names are returned."""
        loggers = VerticaTransformer.get_loggers()
        assert loggers == ["vertica_python"]

    def test_validate_required_fields_success(self):
        """Test successful validation of required fields."""
        required_fields = ["host", "port", "database"]
        connection_data = {"host": "vertica.example.com", "port": 5433, "database": "analytics"}

        # Should not raise any exception
        VerticaTransformer.validate_required_fields(required_fields, connection_data)

    def test_validate_required_fields_missing(self):
        """Test validation fails when field is missing."""
        required_fields = ["host", "port", "database"]
        connection_data = {"host": "vertica.example.com", "port": 5433}

        with pytest.raises(ValueError, match="database is required"):
            VerticaTransformer.validate_required_fields(required_fields, connection_data)

    def test_validate_required_fields_empty_value(self):
        """Test validation fails when field value is empty."""
        required_fields = ["host", "port", "database"]
        connection_data = {
            "host": "vertica.example.com",
            "port": 5433,
            "database": "",  # Empty string
        }

        with pytest.raises(ValueError, match="database is required"):
            VerticaTransformer.validate_required_fields(required_fields, connection_data)

    def test_to_sqlalchemy_config_none_value_field(self):
        """Test that a None value for a required field raises ValueError."""
        connection_data = {
            "host": "vertica.example.com",
            "port": 5433,
            "database": None,
            "user": "dbadmin",
            "password": "secret123",
        }
        with pytest.raises(ValueError, match="database is required"):
            VerticaTransformer.to_sqlalchemy_config(connection_data)

    def test_get_resources_action_database(self):
        """Test resource action for DATABASE type."""
        definition = VerticaTransformer.get_resources_action("DATABASE")

        assert definition.default_type == "DATABASE"
        assert definition.children == ("TABLE",)

    def test_get_resources_action_table(self):
        """Test resource action for TABLE type."""
        definition = VerticaTransformer.get_resources_action("TABLE")

        assert definition.default_type == "TABLE"
        assert definition.children == ("COLUMN",)

    def test_get_resources_action_column(self):
        """Test resource action for COLUMN type."""
        definition = VerticaTransformer.get_resources_action("COLUMN")

        assert definition.default_type == "COLUMN"
        assert definition.children == ()

    def test_get_resources_action_none(self):
        """Test resource action with None defaults to DATABASE."""
        definition = VerticaTransformer.get_resources_action(None)

        assert definition.default_type == "DATABASE"
        assert definition.children == ("TABLE",)

    def test_get_resources_action_invalid_type(self):
        """Test resource action with invalid type raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported resource type"):
            VerticaTransformer.get_resources_action("INVALID_TYPE")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
