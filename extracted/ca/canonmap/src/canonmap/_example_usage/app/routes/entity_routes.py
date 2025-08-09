# app/routes/entity_routes.py

import logging

from fastapi import Request, APIRouter
from fastapi.exceptions import HTTPException

from canonmap.mapping.models import EntityMappingRequest, MappingWeights
from canonmap.mapping.mapping_pipeline import MappingPipeline

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/entity", tags=["entity"])

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
