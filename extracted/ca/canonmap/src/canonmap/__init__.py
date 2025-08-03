"""
CanonMap - A data matching and canonicalization library with MySQL connector support.
"""

__version__ = "0.4.31"

from canonmap.connectors.mysql_connector.config import MySQLConnectorConfig, MySQLConnectionMethod
from canonmap.connectors.mysql_connector.mysql_connector import MySQLConnector
from canonmap.logger import make_console_handler

__all__ = [
    "MySQLConnectorConfig",
    "MySQLConnectionMethod",
    "MySQLConnector",
    "make_console_handler",
    "__version__",
]