# src/canonmap/connectors/mysql_connector/managers/database_manager/utils/create_database.py

import logging

from canonmap.connectors.mysql_connector.mysql_connector import MySQLConnector
from canonmap.connectors.mysql_connector.managers.database_manager.validators.requests import CreateDatabaseRequest
from canonmap.connectors.mysql_connector.validators.models import IfExists
from canonmap.connectors.mysql_connector.utils.check_existence import check_database_existence
from canonmap.exceptions import DatabaseManagerError

logger = logging.getLogger(__name__)

def create_database_util(create_database_request: CreateDatabaseRequest, connector: MySQLConnector) -> dict:
    database_name = create_database_request.database_name
    autoconnect = create_database_request.autoconnect
    if_exists = create_database_request.if_exists
    
    # Check if database exists and handle according to if_exists parameter
    database_exists = check_database_existence(database_name, connector)
    if database_exists:
        if if_exists == IfExists.REPLACE:
            # Drop the existing database for REPLACE mode
            drop_query = f"DROP DATABASE {database_name}"
            try:
                connector.run_query(drop_query)
                logger.info(f"Database {database_name} dropped for REPLACE mode.")
            except Exception as e:
                logger.error(f"Failed to drop database {database_name}: {e}")
                raise DatabaseManagerError(f"Failed to drop existing database '{database_name}': {e}")
        elif if_exists == IfExists.APPEND:
            logger.info(f"Database {database_name} already exists (APPEND mode); skipping creation.")
            if autoconnect:
                connector.connect_to_database(database_name)
                logger.info(f"Connected to database {database_name}")
            return {"action": "skipped", "reason": "database_exists", "mode": "append"}  # Do nothing for APPEND mode
        elif if_exists == IfExists.ERROR:
            logger.warning(f"Database {database_name} already exists and ERROR mode set.")
            raise DatabaseManagerError(f"Database '{database_name}' already exists (ERROR mode).")
        elif if_exists == IfExists.SKIP:
            logger.info(f"Database {database_name} already exists; skipping creation (SKIP mode).")
            if autoconnect:
                connector.connect_to_database(database_name)
                logger.info(f"Connected to database {database_name}")
            return {"action": "skipped", "reason": "database_exists", "mode": "skip"}  # Do nothing

    # User confirmation for database creation
    if not connector.config.autocommit:
        user_confirmation = input(f"Are you sure you want to create database {database_name}? (y/n): ")
        if user_confirmation.lower() != "y":
            logger.info(f"Database {database_name} not created")
            return {"action": "cancelled", "reason": "user_cancelled"}

    try:
        connector.run_query(f"CREATE DATABASE {database_name}")
        logger.info(f"Database {database_name} created")
        if autoconnect:
            connector.connect_to_database(database_name)
            logger.info(f"Connected to database {database_name}")
        return {"action": "created", "reason": "new_database"}
    except Exception as e:
        raise DatabaseManagerError(f"Failed to create database {database_name}: {e}")