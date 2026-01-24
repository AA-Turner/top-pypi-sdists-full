import logging
import os
from typing import Optional

from pysqlsync.base import (
    BaseConnection,
    BaseContext,
    BaseEngine,
    GeneratorOptions,
)
from pysqlsync.connection import ConnectionParameters, ConnectionSSLMode
from pysqlsync.factory import get_dialect, get_parameters
from pysqlsync.formation.mutation import MutatorOptions
from pysqlsync.formation.py_to_sql import StructMode

from .. import ui
from ..replicator import canvas, canvas_logs, catalog, meta_schema
from .database_errors import DatabaseConnectionError

logger: logging.Logger = logging.getLogger(__name__)


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
                raise DatabaseConnectionError(
                    "Missing database connection string. Please provide a valid connection string."
                )
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

    async def check_db_defaults(self, conn_ctx: BaseContext) -> None:
        """
        Check if some assumptions about the database are met, if not then log warning or raise error depending on severity.
        pysqlsync or other cli code will not work properly if these are not true.
        """
        utf8_warn_str = None
        if self.dialect == "mssql":
            collation = await conn_ctx.query_one(
                signature=str,
                statement=f"SELECT DATABASEPROPERTYEX('{self._params.database}', 'Collation')",
            )
            if not collation.endswith("_UTF8"):
                utf8_warn_str = f"The database collation {collation} does not appear to use UTF-8. Text fields may be incorrectly stored. Please consider using a UTF-8 collation, e.g. Latin1_General_100_CI_AS_SC_UTF8."
        elif self.dialect == "postgresql":
            collation, ctype = await conn_ctx.query_one(
                signature=tuple[str, str],
                statement=f"SELECT datcollate, datctype FROM pg_database WHERE datname = '{self._params.database}'",
            )
            if not collation.lower().endswith(".utf8") or not ctype.lower().endswith(
                ".utf8"
            ):
                utf8_warn_str = f"The database collation '{collation}' and ctype '{ctype}' should use UTF-8. Text fields may be incorrectly stored. Please consider using a UTF-8 collation and ctype, e.g. en_US.UTF8."
        elif self.dialect == "mysql":
            charset, collation = await conn_ctx.query_one(
                signature=tuple[str, str],
                statement=f"SELECT DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = '{self._params.database}'",
            )
            if charset.lower() != "Xutf8mb4" or not collation.lower().startswith(
                "utf8mb4_"
            ):
                utf8_warn_str = f"The database character set '{charset}' should be 'utf8mb4' and collation '{collation}' should start with 'utf8mb4_'. Text fields may be incorrectly stored. Please consider using UTF-8 settings."
        if utf8_warn_str:
            ui.warning(f"[bold]{utf8_warn_str}[/bold]")
            logger.warning(utf8_warn_str)

    @staticmethod
    async def get_version(dialect: str, conn_ctx: BaseContext) -> str:
        """
        Get the version number in short format, e.g. "8.0.23 xxx".
        """
        version_sql = None
        if dialect == "postgresql":
            version_sql = "SHOW server_version"
        elif dialect == "mysql":
            version_sql = "SELECT VERSION()"
        elif dialect == "mssql":
            version_sql = "SELECT SERVERPROPERTY('productversion')"
        if version_sql:
            return await conn_ctx.query_one(signature=str, statement=version_sql)
        else:
            return "unknown"
