# canonmap/services/database/mysql/utils/check_connection_method.py
import logging
logger = logging.getLogger(__name__)

from typing import TYPE_CHECKING

from canonmap.services.database.mysql.utils.sql_connection_method import MySQLConnectionMethod

if TYPE_CHECKING:
    from canonmap.services.database.mysql.config import MySQLConfig

def _check_connection_method_util(mysql_config: "MySQLConfig"):
    method = mysql_config.connection_method
    has_host = bool(mysql_config.host)
    has_socket = bool(mysql_config.unix_socket)

    if method == MySQLConnectionMethod.TCP and not has_host:
        logger.error("`tcp` mode requires `host` to be set")
        raise ValueError("`tcp` mode requires `host` to be set")
    if method == MySQLConnectionMethod.SOCKET and not has_socket:
        logger.error("`socket` mode requires `unix_socket` to be set")
        raise ValueError("`socket` mode requires `unix_socket` to be set")
    if method == MySQLConnectionMethod.AUTO and not (has_host or has_socket):
        logger.error("`auto` mode needs either `host` or `unix_socket`")
        raise ValueError("`auto` mode needs either `host` or `unix_socket`")
    logger.info(f"MySQLConfig validated: method={method}, host={mysql_config.host}, unix_socket={mysql_config.unix_socket}")
    return mysql_config
