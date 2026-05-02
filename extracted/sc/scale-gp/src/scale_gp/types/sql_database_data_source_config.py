# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["SqlDatabaseDataSourceConfig"]


class SqlDatabaseDataSourceConfig(BaseModel):
    database: str
    """Name of the database to connect to."""

    dialect: Literal["postgresql", "mssql", "sqlite", "snowflake"]
    """SQL dialect to use for connection"""

    source: Literal["SQLDatabase"]

    account: Optional[str] = None
    """Snowflake account identifier (e.g., 'xy12345' or 'xy12345.us-east-2.azure').

    Do NOT include the '.snowflakecomputing.com' suffix.
    """

    connect_timeout: Optional[int] = None
    """Connection timeout in seconds"""

    connection_options: Optional[Dict[str, str]] = None
    """
    Additional connection parameters appended to the URL (e.g., {'sslrootcert':
    '/path/to/ca.pem', 'application_name': 'myapp'})
    """

    driver: Optional[str] = None
    """ODBC driver name for MSSQL connections.

    Defaults to 'ODBC Driver 18 for SQL Server' if not specified.
    """

    host: Optional[str] = None
    """Database server hostname or IP address"""

    port: Optional[int] = None
    """Database server port"""

    role: Optional[str] = None
    """Snowflake role for authentication.

    Uses the default role for the user if not specified.
    """

    schema_name: Optional[str] = None
    """Snowflake schema name. Defaults to 'PUBLIC' if not specified."""

    ssl_mode: Optional[str] = None
    """SSL mode for PostgreSQL connections (e.g., 'require', 'verify-full')"""

    username: Optional[str] = None
    """Username for authentication"""

    warehouse: Optional[str] = None
    """Snowflake warehouse name for query execution. Required for Snowflake."""
