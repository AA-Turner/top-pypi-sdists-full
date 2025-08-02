# app/routes/query.py

import logging

from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException
from canonmap.connectors.mysql_connector.matching.matcher import Matcher
from canonmap.connectors.mysql_connector.matching.validation.requests import EntityMappingRequest, EntityMappingResponse
from canonmap.exceptions import MatchingError

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/match")
async def match_entities(request: Request, entity_mapping_request: EntityMappingRequest) -> EntityMappingResponse:
    """
    Accepts a JSON entity mapping request, returns match results.
    """
    matcher: Matcher = request.app.state.matcher
    try:
        results = matcher.match(entity_mapping_request)
        # logger.info(f"Matching results: {results}")
        return results
    except Exception as e:
        logger.error(f"Matching failed: {e}")
        raise MatchingError(f"Matching failed: {e}")