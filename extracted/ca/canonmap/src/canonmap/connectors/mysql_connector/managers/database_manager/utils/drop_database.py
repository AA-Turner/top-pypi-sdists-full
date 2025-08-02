# src/canonmap/connectors/mysql_connector/managers/database_manager/utils/drop_database.py

import logging

from canonmap.connectors.mysql_connector.mysql_connector import MySQLConnector
from canonmap.connectors.mysql_connector.managers.database_manager.validators.requests import DropDatabaseRequest
from canonmap.exceptions import DatabaseManagerError

logger = logging.getLogger(__name__)

def drop_database_util(drop_database_request: DropDatabaseRequest, connector: MySQLConnector) -> None:
    database_name = drop_database_request.database_name

    if not connector.config.autocommit:
        user_confirmation = input(f"Are you sure you want to drop database {database_name}? (y/n): ")
        if user_confirmation.lower() != "y":
            logger.info(f"Database {database_name} not dropped")
            return
    
    try:
        connector.run_query(f"DROP DATABASE {database_name}")
        logger.info(f"Database {database_name} dropped")
    except Exception as e:
        raise DatabaseManagerError(f"Failed to drop database {database_name}: {e}")
    