# src/canonmap/connectors/mysql_connector/mysql_db_client.py

from typing import Any, List, Optional

from canonmap.connectors.mysql_connector.models import DmlResult, CreateHelperFieldsPayload
from canonmap.connectors.mysql_connector.mysql_connector import MySQLConnector
from canonmap.connectors.mysql_connector.utils.create_helper_fields_util import _create_helper_fields


class DBClient:
    """High-level DB client using MySQLConnector."""
    def __init__(self, connector: MySQLConnector):
        self._connector = connector

    def execute_read(self, query: str, params: Optional[List[Any]] = None) -> List[dict]:
        return self._connector.execute_query(query, params, allow_writes=False)  # type: ignore

    def execute_write(self, query: str, params: Optional[List[Any]] = None) -> DmlResult:
        return self._connector.execute_query(query, params, allow_writes=True)  # type: ignore
    
    def create_helper_fields(
        self,
        payload: "dict | CreateHelperFieldsPayload",
    ) -> None:
        """Facade method; delegates to the standalone helper implementation.

        Preferred input is a plain dict or CreateHelperFieldsPayload.
        """
        _create_helper_fields(self._connector, payload)