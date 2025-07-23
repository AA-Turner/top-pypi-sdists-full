from typing import List, Optional
from enum import Enum
from pydantic import BaseModel

class CreateDDLResponse(BaseModel):
    ddl: str
    ddl_path: Optional[str] = None

class FieldTransform(str, Enum):
    INITIALISM = "initialism"
    PHONETIC = "phonetic"
    SOUNDEX = "soundex"

class TableField(BaseModel):
    table_name: str
    field_name: str
    field_transform: FieldTransform = None

class EntityMappingRequest(BaseModel):
    entity_name: str
    select_fields: List[TableField]
    top_n: int = 20
    max_prefilter: int = 1000

class SingleMappedEntity(BaseModel):
    raw_entity: str
    canonical_entity: str
    score: float

class EntityMappingResponse(BaseModel):
    results: List[SingleMappedEntity]
