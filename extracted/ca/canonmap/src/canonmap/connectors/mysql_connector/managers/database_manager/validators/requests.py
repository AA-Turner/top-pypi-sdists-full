# src/canonmap/connectors/mysql_connector/managers/database_manager/requests/requests.py

from typing import Optional, Union, Any, List
from pathlib import Path
import pandas as pd

from pydantic import BaseModel, field_validator, ConfigDict
from canonmap.connectors.mysql_connector.validators.models import IfExists
from canonmap.connectors.mysql_connector.managers.field_manager.validators.models import TableField
from canonmap.connectors.mysql_connector.managers.database_manager.validators.models import Database

class CreateDatabaseRequest(BaseModel):
    database_name: str
    autoconnect: bool = False
    if_exists: IfExists = IfExists.ERROR

    @field_validator("database_name")
    def validate_db_name(cls, v: str) -> str:
        if not v:
            raise ValueError("Database name cannot be empty")
        return v
    
    @field_validator("autoconnect")
    def validate_autoconnect(cls, v: bool) -> bool:
        return v
    
class DropDatabaseRequest(BaseModel):
    database_name: str

    @field_validator("database_name")
    def validate_database_name(cls, v: str) -> str:
        if not v:
            raise ValueError("Database name cannot be empty")
        return v
    
# def create_mysql_ddl(table_name: str, data: Union[str, pd.DataFrame, list, Path], save_dir=None):

class CreateDDLRequest(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    table_name: str
    data: Union[str, pd.DataFrame, list, Path]
    save_dir: Optional[str] = None

class GenerateSchemaRequest(BaseModel):
    database: Database
    schema_name: str
    fields_to_include: Optional[List[TableField]] = None
    fields_to_exclude: Optional[List[TableField]] = None
    num_examples: int = 10
    include_helper_fields: bool = False
    save_dir: str = "."
    save_json_version: Optional[str] = None

    @field_validator("schema_name")
    def validate_schema_name(cls, v: str) -> str:
        if not v:
            raise ValueError("Schema name cannot be empty")
        return v
    
    @field_validator("num_examples")
    def validate_num_examples(cls, v: int) -> int:
        if v < 1:
            raise ValueError("num_examples must be at least 1")
        if v > 1000:
            raise ValueError("num_examples cannot exceed 1000")
        return v
