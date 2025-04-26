import os
from typing import Optional

from pysqlsync.base import (
    BaseConnection,
    BaseEngine,
    GeneratorOptions,
)
from pysqlsync.connection import ConnectionParameters, ConnectionSSLMode
from pysqlsync.factory import get_dialect, get_parameters
from pysqlsync.formation.mutation import MutatorOptions
from pysqlsync.formation.py_to_sql import StructMode

from ..replicator import canvas, meta_schema, canvas_logs, catalog
from .database_errors import DatabaseConnectionError


class DatabaseConnectionConfig(ConnectionParameters):
    dialect: str

    def __init__(
        self,
        dialect: str,
        host: Optional[str] = None,
        port: Optional[int] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
        ssl: Optional[ConnectionSSLMode] = None,
    ) -> None:
        self.dialect = dialect

        self.host = host or os.getenv("DAP_DATABASE_HOST")

        self.port = port
        if self.port is None:
            port_env = os.getenv("DAP_DATABASE_PORT")
            if port_env is not None:
                self.port = int(port_env)

        self.username = username or os.getenv("DAP_DATABASE_USERNAME")
        self.password = password or os.getenv("DAP_DATABASE_PASSWORD")
        self.database = database or os.getenv("DAP_DATABASE_NAME")

        self.ssl = ssl
        if self.ssl is None:
            ssl_env = os.getenv("DAP_DATABASE_SSL")
            if ssl_env is not None:
                self.ssl = ConnectionSSLMode(ssl_env)


class DatabaseConnection:
    _params: ConnectionParameters
    engine: BaseEngine
    connection: BaseConnection
    dialect: str

    def __init__(self, connection_string: Optional[str] = None) -> None:
        """
        Initialize the DatabaseConnection instance.
        """
        if connection_string is None:
            connection_string = os.getenv("DAP_CONNECTION_STRING")
            if not connection_string:
                raise DatabaseConnectionError("missing database connection string")
        self.dialect, self._params = get_parameters(connection_string)
        self._create_connection()

    @classmethod
    def from_config(cls, config: DatabaseConnectionConfig) -> "DatabaseConnection":
        """
        Create a DatabaseConnection instance from a DatabaseConnectionConfig.
        """
        instance = cls.__new__(cls)
        instance.dialect = config.dialect
        instance._params = config
        instance._create_connection()
        return instance

    def _create_connection(self) -> None:
        self.engine = get_dialect(self.dialect)
        self.connection = self.engine.create_connection(
            self._params,
            GeneratorOptions(
                struct_mode=StructMode.JSON,
                foreign_constraints=False,
                namespaces={
                    meta_schema: "instructure_dap",
                    canvas: "canvas",
                    canvas_logs: "canvas_logs",
                    catalog: "catalog",
                },
                synchronization=MutatorOptions(
                    allow_drop_enum=False,
                    allow_drop_struct=False,
                    allow_drop_table=False,
                    allow_drop_namespace=False,
                ),
            ),
        )
