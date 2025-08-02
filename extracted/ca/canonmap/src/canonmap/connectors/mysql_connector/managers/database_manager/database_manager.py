# src/canonmap/connectors/mysql_connector/managers/database_manager/database_manager.py

import logging

from canonmap.connectors.mysql_connector.mysql_connector import MySQLConnector
from canonmap.connectors.mysql_connector.managers.database_manager.validators.requests import CreateDatabaseRequest, GenerateSchemaRequest
from canonmap.connectors.mysql_connector.managers.database_manager.utils.create_database import create_database_util
from canonmap.connectors.mysql_connector.managers.database_manager.validators.requests import DropDatabaseRequest
from canonmap.connectors.mysql_connector.managers.database_manager.utils.drop_database import drop_database_util
from canonmap.connectors.mysql_connector.managers.database_manager.utils.generate_schema import generate_schema_util
from canonmap.connectors.mysql_connector.utils.check_existence import check_database_existence
from canonmap.exceptions import DatabaseManagerError

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, connector: MySQLConnector):
        self.connector = connector

    def create_database(self, request: CreateDatabaseRequest) -> dict:
        return create_database_util(request, self.connector)
        
    def drop_database(self, request: DropDatabaseRequest) -> None:
        return drop_database_util(request, self.connector)
        
    def generate_schema(self, request: GenerateSchemaRequest) -> str:
        """
        Generate a schema file containing table structure and sample data.
        
        Args:
            request: The request containing schema generation parameters
            
        Returns:
            str: Path to the generated schema file
        """
        return generate_schema_util(request, self.connector)

