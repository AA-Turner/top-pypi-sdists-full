# canonmap/services/database/mysql/config.py

import logging
from typing import Optional
from pydantic import BaseModel, Field, PrivateAttr, model_validator

import mysql.connector

from canonmap.services.database.mysql.utils.check_connection_method import _check_connection_method_util
from canonmap.services.database.mysql.utils.connect import _connect_util
from canonmap.services.database.mysql.utils.close import _close_util
from canonmap.services.database.mysql.utils.test_connection import _test_connection_util
from canonmap.services.database.mysql.utils.sql_connection_method import MySQLConnectionMethod

logger = logging.getLogger(__name__)

class MySQLConfig(BaseModel):
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

    # private storage for the last connection we opened
    _last_connection: Optional[mysql.connector.MySQLConnection] = PrivateAttr(None)

    @model_validator(mode="after")
    def _check_connection_method(self):
        return _check_connection_method_util(mysql_config=self)

    def test_connection(self) -> bool:
        return _test_connection_util(mysql_config=self)

    def connect(self, **kwargs) -> mysql.connector.MySQLConnection:
        conn = _connect_util(mysql_config=self, **kwargs)
        self._last_connection = conn
        return conn

    def close(self, connection: Optional[mysql.connector.MySQLConnection] = None) -> None:
        """
        Close the given connection, or if None, close the last one returned by connect().
        """
        conn_to_close = connection or self._last_connection
        _close_util(connection=conn_to_close)
        self._last_connection = None