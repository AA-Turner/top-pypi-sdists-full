# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Literal, Required, TypedDict

__all__ = ["SqlDatabaseDataSourceConfigParam"]


class SqlDatabaseDataSourceConfigParam(TypedDict, total=False):
    database: Required[str]
    """Name of the database to connect to."""

    dialect: Required[Literal["postgresql", "mssql", "sqlite", "snowflake"]]
    """SQL dialect to use for connection"""

    source: Required[Literal["SQLDatabase"]]

    account: str
    """Snowflake account identifier (e.g., 'xy12345' or 'xy12345.us-east-2.azure').

    Do NOT include the '.snowflakecomputing.com' suffix.
    """

    connect_timeout: int
    """Connection timeout in seconds"""

    connection_options: Dict[str, str]
    """
    Additional connection parameters appended to the URL (e.g., {'sslrootcert':
    '/path/to/ca.pem', 'application_name': 'myapp'})
    """

    driver: str
    """ODBC driver name for MSSQL connections.

    Defaults to 'ODBC Driver 18 for SQL Server' if not specified.
    """

    host: str
    """Database server hostname or IP address"""

    port: int
    """Database server port"""

    role: str
    """Snowflake role for authentication.

    Uses the default role for the user if not specified.
    """

    schema_name: str
    """Snowflake schema name. Defaults to 'PUBLIC' if not specified."""

    ssl_mode: str
    """SSL mode for PostgreSQL connections (e.g., 'require', 'verify-full')"""

    username: str
    """Username for authentication"""

    warehouse: str
    """Snowflake warehouse name for query execution. Required for Snowflake."""
