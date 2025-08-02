# src/canonmap/connectors/mysql_connector/managers/database_manager/validators/models.py

from pydantic import BaseModel, field_validator

class Database(BaseModel):
    name: str

    @field_validator("name")
    def validate_name(cls, v: str) -> str:
        if not v:
            raise ValueError("Database name cannot be empty")
        return v
