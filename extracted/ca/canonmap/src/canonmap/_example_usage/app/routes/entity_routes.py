# app/routes/entity_routes.py

import logging

from fastapi import Request, APIRouter
from fastapi.exceptions import HTTPException

from canonmap.mapping import (
    EntityMappingRequest,
    MappingWeights,
    MappingPipeline,
)

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/entity", tags=["entity"])


########################################################
# Example custom weights object
########################################################

# weights = MappingWeights(
#     exact=6.0,
#     levenshtein=1.0,
#     jaro=1.2,
#     token=2.0,
#     trigram=1.0,
#     phonetic=1.0,
#     soundex=1.0,
#     initialism=0.5,
#     multi_bonus=1.0,
# )

@router.post("/map-entity")
async def map_entity(
    request: Request, 
    entity_mapping_request: EntityMappingRequest, 
    mapping_weights: MappingWeights = None,
):
    logger.info(f"Running mapping pipeline")
    mapper: MappingPipeline = request.app.state.mapping_pipeline
    
    try:
        result = mapper.run(entity_mapping_request, mapping_weights)
        return result
    except Exception as e:
        logger.error(f"Error in mapping pipeline: {e}")
        raise HTTPException(status_code=500, detail=f"Mapping error: {str(e)}")
