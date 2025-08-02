from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class MySQLConnectionMethod(str, Enum):
    AUTO = "auto"
    TCP = "tcp"
    SOCKET = "socket"

class MySQLConnectorConfig(BaseModel):
    """Configuration for connecting to a MySQL database via TCP or UNIX socket."""
    user: str = Field(..., description="MySQL username")
    password: str = Field(..., description="MySQL password")
    database: Optional[str] = Field(None, description="Database name")
    host: Optional[str] = Field(None, description="TCP host or IP")
    port: int = Field(3306, description="TCP port")
    unix_socket: Optional[str] = Field(None, description="Path to Cloud SQL Auth Proxy UNIX socket")
    connection_method: MySQLConnectionMethod = Field(
        MySQLConnectionMethod.AUTO,
        description="auto=(socket if set else tcp), tcp, or socket",
    )
    autocommit: bool = Field(False, description="Whether to automatically commit transactions")
