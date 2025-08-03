# src/canonmap/connectors/mysql_connector/managers/table_manager/validators/requests.py

from typing import List, Optional
from pydantic import BaseModel

from canonmap.connectors.mysql_connector.utils.mysql_data_types import MySQLDataType
from canonmap.connectors.mysql_connector.validators.models import IfExists
from canonmap.connectors.mysql_connector.managers.database_manager.validators.models import Database

class NewTableField(BaseModel):
    name: str
    data_type: MySQLDataType
    is_primary_key: bool = False
    is_unique: bool = False
    is_not_null: bool = False

class CreateTableRequest(BaseModel):
    database: Database
    name: str
    fields: Optional[List[NewTableField]] = None
    data: Optional[str] = None
    primary_key_field: Optional[str] = None
    if_exists: IfExists = IfExists.ERROR
    autoconnect: bool = False

class DropTableRequest(BaseModel):
    database: Database
    name: str
    autoconnect: bool = False
