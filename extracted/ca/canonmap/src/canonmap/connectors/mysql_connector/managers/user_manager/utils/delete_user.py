# src/canonmap/connectors/mysql_connector/managers/user_manager/utils/delete_user.py

import logging

from canonmap.connectors.mysql_connector.mysql_connector import MySQLConnector
from canonmap.connectors.mysql_connector.managers.user_manager.validators.requests import DeleteUserRequest
from canonmap.exceptions import UserManagerError

logger = logging.getLogger(__name__)

def delete_user_util(delete_user_request: DeleteUserRequest, connector: MySQLConnector) -> None:
    if not connector.config.autocommit:
        user_confirmation = input(f"Are you sure you want to delete user {delete_user_request.username}? (y/n): ")
        if user_confirmation.lower() != "y":
            raise UserManagerError(f"User {delete_user_request.username} not deleted")

    try:
        query = f"DROP USER '{delete_user_request.username}'@'%'"
        connector.run_query(query)

        query = f"FLUSH PRIVILEGES"
        connector.run_query(query)

        logger.info(f"User {delete_user_request.username} deleted successfully")
    except Exception as e:
        raise UserManagerError(f"Failed to delete user {delete_user_request.username}: {e}")