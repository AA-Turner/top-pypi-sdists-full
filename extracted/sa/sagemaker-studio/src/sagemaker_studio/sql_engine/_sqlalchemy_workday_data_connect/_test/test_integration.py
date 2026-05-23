"""Integration tests for Workday Data Connect dialect registration and engine creation.

Tests dialect discovery, registration, and connection creation through SQLAlchemy interfaces.
"""

from unittest.mock import Mock, patch

from sqlalchemy import create_engine
from sqlalchemy.dialects import registry

import sagemaker_studio.sql_engine._sqlalchemy_workday_data_connect as workday_dialect

from ..dialect import WorkdayDataConnectDialect


class TestDialectRegistration:
    """Test dialect registration with SQLAlchemy."""

    def test_dialect_registered_on_import(self):
        dialect_cls = registry.load("workday_data_connect")
        assert dialect_cls == WorkdayDataConnectDialect

    def test_dialect_registered_with_driver_name(self):
        dialect_cls = registry.load("workday_data_connect.workday_data_connect")
        assert dialect_cls == WorkdayDataConnectDialect

    def test_manual_registration_is_idempotent(self):
        workday_dialect.register_dialect()
        workday_dialect.register_dialect()
        dialect_cls = registry.load("workday_data_connect")
        assert dialect_cls == WorkdayDataConnectDialect


class TestEngineCreation:
    """Test SQLAlchemy engine creation with the dialect."""

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_workday_data_connect.dbapi.connection.trino.dbapi.connect"
    )
    def test_create_engine_with_url(self, mock_trino_connect):
        mock_trino_connect.return_value = Mock()

        engine = create_engine(
            "workday_data_connect://host:443" "?client_id=c&isu=i&token_endpoint=t&private_key=k"
        )

        assert engine is not None
        assert engine.dialect.name == "workday_data_connect"

    @patch(
        "sagemaker_studio.sql_engine._sqlalchemy_workday_data_connect.dbapi.connection.trino.dbapi.connect"
    )
    def test_engine_dialect_creates_dbapi_connection(self, mock_trino_connect):
        """Test that the engine's dialect can create a DBAPI connection."""
        mock_trino_connect.return_value = Mock()

        engine = create_engine(
            "workday_data_connect://host:443" "?client_id=c&isu=i&token_endpoint=t&private_key=k"
        )

        # Verify the dialect can produce a raw DBAPI connection
        conn = engine.dialect.connect(
            host="host",
            port=443,
            client_id="c",
            isu="i",
            token_endpoint="t",
            private_key="k",
        )
        assert conn is not None
        mock_trino_connect.assert_called()


class TestModuleInterface:
    """Test the module-level interface."""

    def test_module_exports_dialect(self):
        assert hasattr(workday_dialect, "WorkdayDataConnectDialect")

    def test_module_exports_dbapi(self):
        assert hasattr(workday_dialect, "dbapi")

    def test_module_exports_connect(self):
        assert hasattr(workday_dialect, "connect")

    def test_module_version(self):
        assert workday_dialect.__version__ == "0.1.0"

    def test_dbapi_module_attributes(self):
        dbapi = workday_dialect.dbapi
        assert dbapi.apilevel == "2.0"
        assert dbapi.threadsafety == 2
        assert dbapi.paramstyle == "pyformat"

    def test_dbapi_has_required_exceptions(self):
        dbapi = workday_dialect.dbapi
        assert hasattr(dbapi, "Error")
        assert hasattr(dbapi, "InterfaceError")
        assert hasattr(dbapi, "DatabaseError")
        assert hasattr(dbapi, "OperationalError")
        assert hasattr(dbapi, "ProgrammingError")
        assert hasattr(dbapi, "DataError")
        assert hasattr(dbapi, "IntegrityError")
        assert hasattr(dbapi, "InternalError")
        assert hasattr(dbapi, "NotSupportedError")
        assert hasattr(dbapi, "Warning")
