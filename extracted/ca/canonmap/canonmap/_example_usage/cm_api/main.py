from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from canonmap import (
    CanonMap,
    EntityMappingRequest, 
    ArtifactGenerationRequest,
    ArtifactGenerationResponse,
    EntityMappingResponse
)

from canonmap._example_usage.cm_api.utils.api_logger import setup_logger
from canonmap._example_usage.cm_api.context.context import lifespan

logger = setup_logger(__name__)

app = FastAPI(
    title="CanonMap API",
    description="API for entity matching and artifact generation with comprehensive response models",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"]
)

@app.get("/")
def read_root():
    return {"message": "CanonMap API - Entity Matching and Artifact Generation"}


@app.post("/generate-artifacts", response_model=ArtifactGenerationResponse)
def generate_artifacts(request: Request, generate_artifacts_request: ArtifactGenerationRequest):
    """
    Generate artifacts based on the provided request.
    
    Returns a comprehensive ArtifactGenerationResponse containing:
    - Generated artifacts with metadata
    - Processing statistics
    - Error and warning information
    - GCP upload details (if applicable)
    """
    logger.info("Generating artifacts")
    
    try:
        canonmap: CanonMap = request.app.state.canonmap
        response: ArtifactGenerationResponse = canonmap.generate_artifacts(generate_artifacts_request)
        
        # Log response summary
        logger.info(f"Artifact generation completed with status: {response.status}")
        logger.info(f"Generated {len(response.generated_artifacts)} artifacts")
        
        if response.errors:
            logger.warning(f"Artifact generation completed with {len(response.errors)} errors")
        
        if response.warnings:
            logger.info(f"Artifact generation completed with {len(response.warnings)} warnings")
        
        return response
        
    except Exception as e:
        logger.error(f"Error during artifact generation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Artifact generation failed: {str(e)}")


@app.post("/entity-mapping", response_model=EntityMappingResponse)
def entity_mapping(request: Request, entity_mapping_request: EntityMappingRequest):
    """
    Map entities using existing artifacts.
    
    Returns a comprehensive EntityMappingResponse containing:
    - Detailed mapping results with scores
    - Processing statistics and performance metrics
    - Configuration summary
    - Error and warning information
    """
    logger.info("Mapping entities")
    
    try:
        canonmap: CanonMap = request.app.state.canonmap
        response: EntityMappingResponse = canonmap.map_entities(entity_mapping_request)
        
        # Log response summary
        logger.info(f"Entity mapping completed with status: {response.status}")
        logger.info(f"Processed {response.total_entities_processed} entities")
        logger.info(f"Found {response.total_matches_found} total matches")
        
        if response.errors:
            logger.warning(f"Entity mapping completed with {len(response.errors)} errors")
        
        if response.warnings:
            logger.info(f"Entity mapping completed with {len(response.warnings)} warnings")
        
        return response
        
    except Exception as e:
        logger.error(f"Error during entity mapping: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Entity mapping failed: {str(e)}")


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "CanonMap API",
        "version": "1.0.0"
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "type": type(exc).__name__
        }
    )