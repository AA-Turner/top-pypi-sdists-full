"""
Unit tests for TeraDataTransformer.

Tests the Teradata connection transformer functionality including
URL.create() usage for injection prevention, TLS enforcement,
parameter validation, and configuration.
"""

from unittest.mock import patch

import pytest
from sqlalchemy.engine import URL

from sagemaker_studio.sql_engine.teradata_transformer import TeraDataTransformer


@patch("sagemaker_studio.sql_engine.teradata_transformer._TERADATA_DEPS_AVAILABLE", True)
class TestTeraDataTransformer:
    """Test suite for TeraDataTransformer."""

    def test_get_required_fields(self):
        """Test that all required fields are returned."""
        required = TeraDataTransformer.get_required_fields()
        assert required == ["host", "port", "database", "user", "password"]

    def test_get_dialect(self):
        """Test that the correct dialect is returned for Teradata SQL parsing."""
        assert TeraDataTransformer.get_dialect() == "teradata"

    def test_to_sqlalchemy_config_success(self):
        """Test successful transformation to SQLAlchemy config."""
        connection_data = {
            "host": "teradata.example.com",
            "port": 1025,
            "database": "analytics",
            "user": "dbadmin",
            "password": "secret123",
        }

        config = TeraDataTransformer.to_sqlalchemy_config(connection_data)

        assert "connection_string" in config
        assert "connect_args" in config
        # connection_string should be a SQLAlchemy URL object
        assert isinstance(config["connection_string"], URL)
        url = config["connection_string"]
        assert url.drivername == "teradatasql"
        assert url.username == "dbadmin"
        assert url.password == "secret123"
        assert url.host == "teradata.example.com"
        assert url.query == {"database": "analytics"}
        # connect_args should include dbs_port and TLS enforcement
        assert config["connect_args"]["dbs_port"] == 1025
        assert config["connect_args"]["sslmode"] == "REQUIRE"

    def test_to_sqlalchemy_config_enforces_tls(self):
        """Test that TLS is enforced via sslmode=REQUIRE in connect_args."""
        connection_data = {
            "host": "teradata.example.com",
            "port": 1025,
            "database": "analytics",
            "user": "dbadmin",
            "password": "secret123",
        }

        config = TeraDataTransformer.to_sqlalchemy_config(connection_data)

        assert "sslmode" in config["connect_args"]
        assert config["connect_args"]["sslmode"] == "REQUIRE"

    def test_to_sqlalchemy_config_returns_url_object(self):
        """Test that connection_string is a SQLAlchemy URL object (not an f-string)."""
        connection_data = {
            "host": "teradata.example.com",
            "port": 1025,
            "database": "analytics",
            "user": "dbadmin",
            "password": "secret123",
        }

        config = TeraDataTransformer.to_sqlalchemy_config(connection_data)

        # Must be a URL object, not a raw string
        assert isinstance(config["connection_string"], URL)
        assert not isinstance(config["connection_string"], str)

    def test_to_sqlalchemy_config_missing_host(self):
        """Test that missing host raises ValueError."""
        connection_data = {
            "port": 1025,
            "database": "analytics",
            "user": "dbadmin",
            "password": "secret123",
        }

        with pytest.raises(ValueError, match="host is required"):
            TeraDataTransformer.to_sqlalchemy_config(connection_data)

    def test_to_sqlalchemy_config_missing_port(self):
        """Test that missing port raises ValueError."""
        connection_data = {
            "host": "teradata.example.com",
            "database": "analytics",
            "user": "dbadmin",
            "password": "secret123",
        }

        with pytest.raises(ValueError, match="port is required"):
            TeraDataTransformer.to_sqlalchemy_config(connection_data)

    def test_to_sqlalchemy_config_missing_database(self):
        """Test that missing database raises ValueError."""
        connection_data = {
            "host": "teradata.example.com",
            "port": 1025,
            "user": "dbadmin",
            "password": "secret123",
        }

        with pytest.raises(ValueError, match="database is required"):
            TeraDataTransformer.to_sqlalchemy_config(connection_data)

    def test_to_sqlalchemy_config_missing_user(self):
        """Test that missing user raises ValueError."""
        connection_data = {
            "host": "teradata.example.com",
            "port": 1025,
            "database": "analytics",
            "password": "secret123",
        }

        with pytest.raises(ValueError, match="user is required"):
            TeraDataTransformer.to_sqlalchemy_config(connection_data)

    def test_to_sqlalchemy_config_missing_password(self):
        """Test that missing password raises ValueError."""
        connection_data = {
            "host": "teradata.example.com",
            "port": 1025,
            "database": "analytics",
            "user": "dbadmin",
        }

        with pytest.raises(ValueError, match="password is required"):
            TeraDataTransformer.to_sqlalchemy_config(connection_data)

    def test_to_sqlalchemy_config_with_special_characters_in_password(self):
        """Test that special characters in password are safely encoded via URL.create()."""
        connection_data = {
            "host": "teradata.example.com",
            "port": 1025,
            "database": "analytics",
            "user": "dbadmin",
            "password": "p@ssw0rd!#$",
        }

        config = TeraDataTransformer.to_sqlalchemy_config(connection_data)

        # URL.create() safely handles special characters
        url = config["connection_string"]
        assert isinstance(url, URL)
        assert url.password == "p@ssw0rd!#$"
        assert url.username == "dbadmin"
        assert url.host == "teradata.example.com"

    def test_to_sqlalchemy_config_with_special_characters_in_username(self):
        """Test that special characters in username are safely encoded via URL.create()."""
        connection_data = {
            "host": "teradata.example.com",
            "port": 1025,
            "database": "analytics",
            "user": "db@admin",
            "password": "pass:word/123",
        }

        config = TeraDataTransformer.to_sqlalchemy_config(connection_data)

        # URL.create() safely handles special characters - no injection possible
        url = config["connection_string"]
        assert isinstance(url, URL)
        assert url.username == "db@admin"
        assert url.password == "pass:word/123"
        assert url.host == "teradata.example.com"
        assert url.query == {"database": "analytics"}

    def test_to_sqlalchemy_config_prevents_host_injection(self):
        """Test that malicious host values cannot redirect connections."""
        connection_data = {
            "host": "evil.com?redirect=true@legit.com",
            "port": 1025,
            "database": "analytics",
            "user": "dbadmin",
            "password": "secret123",
        }

        config = TeraDataTransformer.to_sqlalchemy_config(connection_data)

        # URL.create() treats the host literally, not as part of URL structure
        url = config["connection_string"]
        assert isinstance(url, URL)
        # The host is stored as-is in the URL object, not parsed as URL components
        assert url.host == "evil.com?redirect=true@legit.com"

    def test_to_sqlalchemy_config_with_different_port(self):
        """Test connection config with non-default port."""
        connection_data = {
            "host": "teradata.example.com",
            "port": 9999,
            "database": "analytics",
            "user": "dbadmin",
            "password": "secret123",
        }

        config = TeraDataTransformer.to_sqlalchemy_config(connection_data)

        url = config["connection_string"]
        assert isinstance(url, URL)
        assert url.drivername == "teradatasql"
        assert url.host == "teradata.example.com"
        assert config["connect_args"]["dbs_port"] == 9999
        assert config["connect_args"]["sslmode"] == "REQUIRE"

    def test_to_sqlalchemy_config_none_value_field(self):
        """Test that a None value for a required field raises ValueError."""
        connection_data = {
            "host": "teradata.example.com",
            "port": 1025,
            "database": None,
            "user": "dbadmin",
            "password": "secret123",
        }
        with pytest.raises(ValueError, match="database is required"):
            TeraDataTransformer.to_sqlalchemy_config(connection_data)

    def test_get_loggers(self):
        """Test that correct logger names are returned."""
        loggers = TeraDataTransformer.get_loggers()
        assert loggers == ["sqlalchemy.dialects.teradata", "teradatasql"]

    def test_validate_required_fields_success(self):
        """Test successful validation of required fields."""
        required_fields = ["host", "port", "database"]
        connection_data = {
            "host": "teradata.example.com",
            "port": 1025,
            "database": "analytics",
        }

        # Should not raise any exception
        TeraDataTransformer.validate_required_fields(required_fields, connection_data)

    def test_validate_required_fields_missing(self):
        """Test validation fails when field is missing."""
        required_fields = ["host", "port", "database"]
        connection_data = {
            "host": "teradata.example.com",
            "port": 1025,
        }

        with pytest.raises(ValueError, match="database is required"):
            TeraDataTransformer.validate_required_fields(required_fields, connection_data)

    def test_validate_required_fields_empty_value(self):
        """Test validation fails when field value is empty."""
        required_fields = ["host", "port", "database"]
        connection_data = {
            "host": "teradata.example.com",
            "port": 1025,
            "database": "",  # Empty string
        }

        with pytest.raises(ValueError, match="database is required"):
            TeraDataTransformer.validate_required_fields(required_fields, connection_data)

    def test_get_resources_action_database(self):
        """Test resource action for DATABASE type."""
        definition = TeraDataTransformer.get_resources_action("DATABASE")

        assert definition.default_type == "DATABASE"
        assert definition.children == ("TABLE",)

    def test_get_resources_action_table(self):
        """Test resource action for TABLE type."""
        definition = TeraDataTransformer.get_resources_action("TABLE")

        assert definition.default_type == "TABLE"
        assert definition.children == ("COLUMN",)

    def test_get_resources_action_column(self):
        """Test resource action for COLUMN type."""
        definition = TeraDataTransformer.get_resources_action("COLUMN")

        assert definition.default_type == "COLUMN"
        assert definition.children == ()

    def test_get_resources_action_none(self):
        """Test resource action with None defaults to DATABASE."""
        definition = TeraDataTransformer.get_resources_action(None)

        assert definition.default_type == "DATABASE"
        assert definition.children == ("TABLE",)

    def test_get_resources_action_invalid_type(self):
        """Test resource action with invalid type raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported resource type"):
            TeraDataTransformer.get_resources_action("INVALID_TYPE")

    def test_teradata_registered_in_sql_executor(self):
        """Test that TERADATA is registered as a supported connection type in SqlExecutor."""
        with patch("sagemaker_studio.sql_engine.sql_executor._TERADATA_AVAILABLE", True):
            from sagemaker_studio.sql_engine.sql_executor import SqlExecutor

            executor = SqlExecutor()
            assert "TERADATA" in executor.get_supported_connection_types()


@patch("sagemaker_studio.sql_engine.teradata_transformer._TERADATA_DEPS_AVAILABLE", False)
class TestTeraDataTransformerDepsUnavailable:
    """Tests for TeraDataTransformer when teradata dependencies are not installed."""

    def test_to_sqlalchemy_config_raises_import_error_when_deps_unavailable(self):
        """Test that to_sqlalchemy_config raises ImportError when teradatasql is not installed."""
        connection_data = {
            "host": "teradata.example.com",
            "port": 1025,
            "database": "analytics",
            "user": "dbadmin",
            "password": "secret123",
        }

        with pytest.raises(ImportError, match="teradatasql"):
            TeraDataTransformer.to_sqlalchemy_config(connection_data)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


class TestTeraDataTransformerModuleImport:
    """Tests that cover module-level import behavior of teradata_transformer.py."""

    def test_module_sets_deps_unavailable_when_teradatasql_missing(self):
        """Test that _TERADATA_DEPS_AVAILABLE is False when teradatasql is not installed.

        This covers the except ImportError branch in teradata_transformer.py.
        """
        import importlib
        import sys

        import sagemaker_studio.sql_engine.teradata_transformer as tt_module

        original_teradatasql = sys.modules.get("teradatasql")
        original_teradatasqlalchemy = sys.modules.get("teradatasqlalchemy")

        try:
            # Make teradatasql import fail
            sys.modules["teradatasql"] = None  # None entry causes ImportError on import

            # Reload the module so the try/except block re-executes
            importlib.reload(tt_module)

            assert tt_module._TERADATA_DEPS_AVAILABLE is False
        finally:
            # Restore original state
            if original_teradatasql is not None:
                sys.modules["teradatasql"] = original_teradatasql
            else:
                sys.modules.pop("teradatasql", None)
            if original_teradatasqlalchemy is not None:
                sys.modules["teradatasqlalchemy"] = original_teradatasqlalchemy
            else:
                sys.modules.pop("teradatasqlalchemy", None)
            # Reload to restore normal state
            importlib.reload(tt_module)
