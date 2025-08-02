# src/canonmap/connectors/mysql_connector/managers/table_manager/table_manager.py

from canonmap.connectors.mysql_connector.mysql_connector import MySQLConnector
from canonmap.connectors.mysql_connector.managers.table_manager.validators.requests import CreateTableRequest, DropTableRequest
from canonmap.connectors.mysql_connector.managers.table_manager.utils.create_table import create_table_util
from canonmap.connectors.mysql_connector.managers.table_manager.utils.create_table_from_data import create_table_from_data_util
from canonmap.connectors.mysql_connector.managers.table_manager.utils.drop_table import drop_table_util


class TableManager:
    def __init__(self, connector: MySQLConnector):
        self.connector = connector

    def create_table(self, create_table_request: CreateTableRequest) -> dict:
        if create_table_request.data is not None:
            return create_table_from_data_util(create_table_request, self.connector, create_table_request.data)
        else:
            return create_table_util(create_table_request, self.connector)
    
    def drop_table(self, drop_table_request: DropTableRequest) -> None:
        return drop_table_util(drop_table_request, self.connector)