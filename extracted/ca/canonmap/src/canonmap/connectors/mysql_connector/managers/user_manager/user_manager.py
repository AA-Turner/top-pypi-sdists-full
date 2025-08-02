# src/canonmap/connectors/mysql_connector/managers/user_manager/user_manager.py

from canonmap.connectors.mysql_connector.mysql_connector import MySQLConnector
from canonmap.connectors.mysql_connector.managers.user_manager.validators.requests import CreateUserRequest, DeleteUserRequest
from canonmap.connectors.mysql_connector.managers.user_manager.utils.create_user import create_user_util
from canonmap.connectors.mysql_connector.managers.user_manager.utils.delete_user import delete_user_util

class UserManager:
    def __init__(self, connector: MySQLConnector):
        self.connector = connector

    def create_user(self, user_request: CreateUserRequest) -> None:
        return create_user_util(user_request, self.connector)
    
    def delete_user(self, user_request: DeleteUserRequest) -> None:
        return delete_user_util(user_request, self.connector)