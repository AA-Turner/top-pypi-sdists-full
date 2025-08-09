from typing import List

from pydantic import BaseModel


class SingleMappedEntity(BaseModel):
    raw_entity: str
    canonical_entity: str
    canonical_table_name: str
    canonical_field_name: str
    score: float

class EntityMappingRequest(BaseModel):
    entity_name: str
    candidate_table_name: str
    candidate_field_name: str
    top_n: int = 20
    max_prefilter: int = 1000
    semantic_rerank: bool = False

class EntityMappingResponse(BaseModel):
    results: List[SingleMappedEntity]

class MappingWeights(BaseModel):
    exact: float = 6.0
    levenshtein: float = 1.0
    jaro: float = 1.2
    token: float = 2.0
    trigram: float = 1.0
    phonetic: float = 1.0
    soundex: float = 1.0
    initialism: float = 0.5
    multi_bonus: float = 1.0