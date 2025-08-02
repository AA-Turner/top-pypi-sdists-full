# src/canonmap/connectors/mysql_connector/managers/table_manager/validators/models.py

from enum import Enum

from pydantic import BaseModel, field_validator

from canonmap.connectors.mysql_connector.managers.database_manager.validators.models import Database

class Table(BaseModel):
    database: Database
    name: str

    @field_validator("name")
    def validate_name(cls, v: str) -> str:
        if not v:
            raise ValueError("Table name cannot be empty")
        return v
    
# class IfExists(Enum):
#     REPLACE = "replace"
#     APPEND = "append"
#     ERROR = "error"
#     SKIP = "skip"
    


