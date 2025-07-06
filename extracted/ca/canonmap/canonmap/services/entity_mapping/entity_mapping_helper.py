import logging
import pickle
import numpy as np
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

from canonmap.utils.logger import setup_logger
from canonmap.config.validate_configs import CanonMapArtifactsConfig
from canonmap.requests.entity_mapping_request import EntityMappingRequest
from canonmap.responses import EntityMappingResponse, SingleMapping, MatchItem
from canonmap.services.entity_mapping.entity_mapping_service import EntityMapper

logger = setup_logger()


def find_artifact_file(directory: Path, pattern: str, required: bool = True) -> Optional[Path]:
    matches = sorted(directory.glob(pattern))
    if not matches:
        if required:
            raise FileNotFoundError(f"No file matching '{pattern}' found in {directory}")
        return None
    if len(matches) > 1:
        logger.warning(f"Multiple files matching '{pattern}' found in {directory}, using '{matches[0].name}'")
    return matches[0]


def map_entities_helper(
    request: EntityMappingRequest,
    artifacts_config: CanonMapArtifactsConfig,
    embedder: Any,
) -> EntityMappingResponse:
    """
    Map entities using the existing artifacts and embedder.
    
    Args:
        request: EntityMappingRequest specifying what to map
        artifacts_config: CanonMapArtifactsConfig for artifact storage settings
        embedder: Embedding model instance
        
    Returns:
        EntityMappingResponse containing mapping results and metadata
        
    Raises:
        FileNotFoundError: If artifacts don't exist
        ValueError: If request validation fails
        Exception: If mapping process fails
    """
    
    start_time = datetime.now()
    
    # Use artifacts_config for storage settings
    artifacts_path = Path(artifacts_config.artifacts_local_path)
    
    if not artifacts_path.exists():
        raise FileNotFoundError(f"Artifacts path does not exist: {artifacts_path}")
    
    logger.info(f"Loading artifacts from: {artifacts_path}")
    
    # Load canonical entities (flexible, no hardcoding)
    canonical_entities_path = find_artifact_file(artifacts_path, "*_canonical_entities.pkl")
    with open(canonical_entities_path, "rb") as f:
        canonical_entities = pickle.load(f)
    logger.info(f"Loaded {len(canonical_entities)} canonical entities")
    
    # Load embeddings if available and semantic search is requested (flexible, no hardcoding)
    embeddings = None
    nn = None
    if request.use_semantic_search and embedder:
        embeddings_path = find_artifact_file(artifacts_path, "*_canonical_entity_embeddings.npz", required=False)
        if embeddings_path:
            embeddings_data = np.load(embeddings_path)
            embeddings = embeddings_data['embeddings']
            logger.info(f"Loaded embeddings with shape: {embeddings.shape}")
            from sklearn.neighbors import NearestNeighbors
            nn = NearestNeighbors(n_neighbors=min(50, len(embeddings)), metric='cosine')
            nn.fit(embeddings)
            logger.info("Built nearest neighbors index for semantic search")
        else:
            logger.warning("Semantic search requested but no embeddings found. Falling back to fuzzy matching only.")
            request.use_semantic_search = False
    
    # Initialize the entity mapper
    mapper = EntityMapper(
        embedder=embedder,
        canonical_entities=canonical_entities,
        embeddings=embeddings,
        nn=nn,
    )
    
    # Perform entity mapping
    logger.info(f"Mapping {len(request.entities)} entities...")
    response = mapper.map_entities(request)
    
    end_time = datetime.now()
    processing_time = (end_time - start_time).total_seconds()
    
    logger.info("Entity mapping completed successfully")
    
    # Enhance the response with additional metadata
    response.set_processing_stats(
        total_entities=len(request.entities),
        total_matches=sum(len(result.matches) for result in response.results),
        processing_time_seconds=processing_time,
        average_time_ms=processing_time * 1000 / len(request.entities) if request.entities else None
    )
    
    response.set_config_summary(
        num_results=request.num_results,
        threshold=request.threshold,
        weights=request.weights,
        use_semantic_search=request.use_semantic_search
    )
    
    return response 