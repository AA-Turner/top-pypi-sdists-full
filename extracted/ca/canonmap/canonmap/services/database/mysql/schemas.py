from typing import List, Optional
from enum import Enum
from pydantic import BaseModel

class CreateDDLResponse(BaseModel):
    ddl: str
    ddl_path: Optional[str] = None

class FieldTransformType(str, Enum):
    INITIALISM = "initialism"
    PHONETIC = "phonetic"
    SOUNDEX = "soundex"

class Database(BaseModel):
    database_name: str

class Table(BaseModel):
    table_name: str

class TableField(BaseModel):
    table_name: Table
    field_name: str

class EntityMappingRequest(BaseModel):
    entity_name: str
    select_field: TableField
    top_n: int = 20
    max_prefilter: int = 1000

class SingleMappedEntity(BaseModel):
    raw_entity: str
    canonical_entity: str
    canonical_table_name: str
    canonical_field_name: str
    score: float

class EntityMappingResponse(BaseModel):
    results: List[SingleMappedEntity]
