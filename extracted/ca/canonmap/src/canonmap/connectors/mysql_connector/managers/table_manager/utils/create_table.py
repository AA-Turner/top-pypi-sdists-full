# src/canonmap/connectors/mysql_connector/managers/table_manager/utils/create_table.py

import logging

from canonmap.connectors.mysql_connector.mysql_connector import MySQLConnector
from canonmap.connectors.mysql_connector.managers.table_manager.validators.requests import CreateTableRequest
from canonmap.connectors.mysql_connector.validators.models import IfExists
from canonmap.connectors.mysql_connector.utils.check_existence import check_table_existence
from canonmap.connectors.mysql_connector.managers.table_manager.utils._generate_table_fields_str import generate_table_fields_str
from canonmap.exceptions import TableManagerError

logger = logging.getLogger(__name__)

def create_table_util(create_table_request: CreateTableRequest, connector: MySQLConnector) -> dict:
    database_name = create_table_request.database.name
    table_name = create_table_request.name
    fields = create_table_request.fields
    if_exists = create_table_request.if_exists
    autoconnect = create_table_request.autoconnect

    # Check if table exists and handle according to if_exists parameter
    table_exists = check_table_existence(database_name, table_name, connector)
    if table_exists:
        if if_exists == IfExists.REPLACE:
            # Drop the existing table for REPLACE mode
            drop_query = f"DROP TABLE {database_name}.{table_name}"
            try:
                connector.run_query(drop_query)
                logger.info(f"Table {table_name} dropped for REPLACE mode.")
            except Exception as e:
                logger.error(f"Failed to drop table {table_name}: {e}")
                raise TableManagerError(f"Failed to drop existing table '{table_name}': {e}")
        elif if_exists == IfExists.APPEND:
            logger.info(f"Table {table_name} already exists (APPEND mode); skipping creation.")
            if autoconnect:
                connector.connect_to_database(database_name)
                logger.info(f"Connected to database {database_name}")
            return {"action": "skipped", "reason": "table_exists", "mode": "append"}  # Do nothing for APPEND mode (no data to append)
        elif if_exists == IfExists.ERROR:
            logger.warning(f"Table {table_name} already exists and ERROR mode set.")
            raise TableManagerError(f"Table '{database_name}.{table_name}' already exists (ERROR mode).")
        elif if_exists == IfExists.SKIP:
            logger.info(f"Table {table_name} already exists; skipping creation (SKIP mode).")
            if autoconnect:
                connector.connect_to_database(database_name)
                logger.info(f"Connected to database {database_name}")
            return {"action": "skipped", "reason": "table_exists", "mode": "skip"}  # Do nothing

    # Create the table
    if fields:
        fields_str: str = generate_table_fields_str(fields)
        query = f"CREATE TABLE {database_name}.{table_name} ({fields_str})"
    else:
        query = f"CREATE TABLE {database_name}.{table_name} (id INT AUTO_INCREMENT PRIMARY KEY)"

    try:
        connector.run_query(query)
        logger.info(f"Table {table_name} created successfully")
        if autoconnect:
            connector.connect_to_database(database_name)
            logger.info(f"Connected to database {database_name}")
        return {"action": "created", "reason": "new_table"}
    except Exception as e:
        logger.error(f"Failed to create table {table_name} with query: {query}")
        raise TableManagerError(f"Failed to create table {table_name}: {e}")
