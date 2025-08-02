from decimal import Decimal
from typing import Optional, Union

import mysql.connector
import mysql.connector.errors
from gable.cli.readers.constants import (
    PROXY_DB_CONNECTION_RETIRES,
    PROXY_DB_CONNECTION_TIMEOUT_SECONDS,
)
from loguru import logger
from mysql.connector.conversion import MySQLConverter
from mysql.connector.custom_types import HexLiteral


def create_mysql_connection(
    user: str,
    password: str,
    db: str,
    host: str = "localhost",
    port: int = 3306,
    connect_timeout: int = PROXY_DB_CONNECTION_TIMEOUT_SECONDS,
    connect_retries: int = PROXY_DB_CONNECTION_RETIRES,
):
    """
    Create a connection to a MySQL database.

    :param user:     The database user name.
    :param password: The database password.
    :param db:       The database name.
    :param host:     The database host.
    :param port:     The database port.
    :return:         A MySQLdb Connection instance.
    """
    # logger.debug(
    #     f'Connecting to "server={host}:{port};uid={user};pwd=******;database={db}"'
    # )
    logger.debug(f'Connecting to "mysql://{user}:******@{host}:{port}/{db}"')
    logger.debug(mysql.connector.paramstyle)
    attempt = 0
    while True:
        try:
            conn = mysql.connector.connect(
                database=db,
                user=user,
                passwd=password,
                host=host,
                port=port,
                connect_timeout=connect_timeout,
                converter_class=TupleMySQLConverter,
            )

            return conn
        except mysql.connector.errors.PoolError as e:
            attempt += 1
            logger.debug(f"Connection attempt {attempt}/{connect_retries} failed...")
            logger.trace(str(e))
            if attempt >= connect_retries:
                logger.error(
                    f"Unable to connect to {host}:{port} after {attempt} attempts"
                )
                raise e


class TupleMySQLConverter(MySQLConverter):
    """Stupid class to add stupid support for stupid tuples and stupid lists to the
    extremely stupid MySQL connector because it doesn't support them somehow.

    https://github.com/mysql/mysql-connector-python/blob/trunk/lib/mysql/connector/types.py#L56-L69
    https://github.com/mysql/mysql-connector-python/blob/trunk/lib/mysql/connector/conversion.py#L155
    """

    def __init__(self, charset="utf8", use_unicode=True, converter_str_fallback=False):
        super().__init__(charset, use_unicode, str_fallback=converter_str_fallback)

    def _tuple_to_mysql(self, value: tuple) -> tuple:
        return value

    def _list_to_mysql(self, value: list) -> list:
        return value

    @staticmethod  # type: ignore
    def quote(
        buf: Optional[Union[float, int, Decimal, tuple, list, HexLiteral, bytes]]
    ) -> bytes:
        """
        Override the base class quote method to add support for tuples and lists.
        """
        if isinstance(buf, tuple):
            return bytearray(
                b"("
                + ",".join([f"'{item}'" for item in buf]).encode("utf-8")  # type: ignore[operator]
                + b")"
            )
        if isinstance(buf, list):
            return bytearray(
                b"["
                + ",".join([f"'{item}'" for item in buf]).encode("utf-8")  # type: ignore[operator]
                + b"]"
            )
        return MySQLConverter.quote(buf)
