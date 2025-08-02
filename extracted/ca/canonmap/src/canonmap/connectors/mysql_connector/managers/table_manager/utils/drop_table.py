# src/canonmap/connectors/mysql_connector/managers/table_manager/utils/delete_table.py

import logging

from canonmap.connectors.mysql_connector.mysql_connector import MySQLConnector
from canonmap.connectors.mysql_connector.managers.table_manager.validators.requests import DropTableRequest
from canonmap.exceptions import TableManagerError

logger = logging.getLogger(__name__)

def drop_table_util(drop_table_request: DropTableRequest, connector: MySQLConnector) -> None:
    database_name = drop_table_request.database.name
    table_name = drop_table_request.name
    autoconnect = drop_table_request.autoconnect
    
    if not connector.config.autocommit:
        user_confirmation = input(f"Are you sure you want to drop table {table_name}? (y/n): ")
        if user_confirmation.lower() != "y":
            logger.info(f"Table {table_name} not dropped")
            return
    
    try:
        connector.run_query(f"DROP TABLE {database_name}.{table_name}")
        logger.info(f"Table {table_name} dropped")
        if autoconnect:
            connector.connect_to_database(database_name)
            logger.info(f"Connected to database {database_name}")
    except Exception as e:
        raise TableManagerError(f"Failed to drop table {table_name}: {e}")