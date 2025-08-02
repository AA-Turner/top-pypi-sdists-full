from pydantic import BaseModel, field_validator
from enum import Enum

from canonmap.connectors.mysql_connector.managers.table_manager.validators.models import Table

class FieldTransformType(str, Enum):
    INITIALISM = "initialism"
    PHONETIC = "phonetic"
    SOUNDEX = "soundex"

class TableField(BaseModel):
    table: Table
    name: str

    @field_validator("name")
    def validate_name(cls, v: str) -> str:
        if not v:
            raise ValueError("Field name cannot be empty")
        return v