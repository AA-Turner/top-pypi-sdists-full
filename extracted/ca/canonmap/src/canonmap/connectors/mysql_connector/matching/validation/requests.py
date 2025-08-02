# src/canonmap/connectors/mysql_connector/matching/validation/requests.py

from typing import List
from pydantic import BaseModel
from canonmap.connectors.mysql_connector.managers.field_manager.validators.models import TableField
from canonmap.connectors.mysql_connector.matching.validation.models import SingleMappedEntity

class EntityMappingRequest(BaseModel):
    entity_name: str
    select_field: TableField
    top_n: int = 20
    max_prefilter: int = 1000
    semantic_rerank: bool = False

class EntityMappingResponse(BaseModel):
    results: List[SingleMappedEntity]