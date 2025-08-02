# src/canonmap/connectors/mysql_connector/managers/user_manager/utils/create_user.py

import logging

from canonmap.connectors.mysql_connector.mysql_connector import MySQLConnector
from canonmap.connectors.mysql_connector.managers.user_manager.validators.requests import CreateUserRequest
from canonmap.connectors.mysql_connector.validators.models import IfExists
from canonmap.connectors.mysql_connector.utils.check_existence import check_user_existence
from canonmap.exceptions import UserManagerError

logger = logging.getLogger(__name__)

def create_user_util(create_user_request: CreateUserRequest, connector: MySQLConnector) -> None:
    username = create_user_request.username
    password = create_user_request.password
    role = create_user_request.role
    if_exists = create_user_request.if_exists

    # Check if user exists and handle according to if_exists parameter
    user_exists = check_user_existence(username, connector)
    if user_exists:
        if if_exists == IfExists.REPLACE:
            # Drop the existing user for REPLACE mode
            drop_query = f"DROP USER '{username}'@'%'"
            try:
                connector.run_query(drop_query)
                logger.info(f"User {username} dropped for REPLACE mode.")
            except Exception as e:
                logger.error(f"Failed to drop user {username}: {e}")
                raise UserManagerError(f"Failed to drop existing user '{username}': {e}")
        elif if_exists == IfExists.APPEND:
            logger.info(f"User {username} already exists (APPEND mode); skipping creation.")
            return  # Do nothing for APPEND mode
        elif if_exists == IfExists.ERROR:
            logger.warning(f"User {username} already exists and ERROR mode set.")
            raise UserManagerError(f"User '{username}' already exists (ERROR mode).")
        elif if_exists == IfExists.SKIP:
            logger.info(f"User {username} already exists; skipping creation (SKIP mode).")
            return  # Do nothing

    try:
        query = f"CREATE USER '{username}'@'%' IDENTIFIED BY '{password}'"
        connector.run_query(query)

        query = f"GRANT {role} ON *.* TO '{username}'@'%'"
        connector.run_query(query)

        query = f"FLUSH PRIVILEGES"
        connector.run_query(query)

        logger.info(f"User {username} created successfully")
    except Exception as e:
        raise UserManagerError(f"Failed to create user {username}: {e}")
