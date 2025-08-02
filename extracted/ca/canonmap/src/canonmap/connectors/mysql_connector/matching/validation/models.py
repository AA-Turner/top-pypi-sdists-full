# src/canonmap/connectors/mysql_connector/matching/validation/models.py

from typing import List
from pydantic import BaseModel

class SingleMappedEntity(BaseModel):
    raw_entity: str
    canonical_entity: str
    canonical_table_name: str
    canonical_field_name: str
    score: float
