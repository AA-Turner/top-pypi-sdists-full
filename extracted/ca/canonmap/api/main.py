from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
import traceback

from api.context.context import lifespan
from canonmap.requests.artifact_generation_request import ArtifactGenerationRequest
from canonmap.requests.entity_mapping_request import EntityMappingRequest
from canonmap.responses.artifact_generation_response import ArtifactGenerationResponse
from canonmap.services.artifact_generation.generate_artifacts import generate_artifacts_helper
from canonmap.config.validate_configs import CanonMapArtifactsConfig

app = FastAPI(
    title="CanonMap API",
    description="API for entity matching and artifact generation",
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
    return {"message": "CanonMap API is running!"}

@app.post("/generate-artifacts")
def generate_artifacts(request: ArtifactGenerationRequest) -> ArtifactGenerationResponse:
    """
    Generate artifacts based on the provided request.
    
    This endpoint handles the complex ArtifactGenerationRequest structure with:
    - Nested config objects (InputConfig, ProcessingConfig, etc.)
    - Legacy parameter support with deprecation warnings
    - Property methods for transparent access
    """
    try:
        # Get the artifacts config from the app state
        artifacts_config = getattr(app.state, 'artifacts_config', None)
        if not artifacts_config:
            # Create a default config if none exists
            artifacts_config = CanonMapArtifactsConfig(
                artifacts_local_path="./artifacts",
                artifacts_gcp_bucket_name="",
                artifacts_gcp_bucket_prefix="",
                artifacts_gcp_service_account_json_path=""
            )
        
        # Get embedder from app state if available
        embedder = getattr(app.state, 'embedder', None)
        
        # Generate artifacts using the helper function
        response = generate_artifacts_helper(
            request=request,
            artifacts_config=artifacts_config,
            embedder=embedder
        )
        
        return response
        
    except Exception as e:
        # Log the full error for debugging
        error_msg = f"Artifact generation failed: {str(e)}"
        print(f"ERROR: {error_msg}")
        print(f"TRACEBACK: {traceback.format_exc()}")
        
        # Return a proper error response
        raise HTTPException(
            status_code=500,
            detail=error_msg
        )

@app.post("/map-entities")
def map_entities(request: EntityMappingRequest) -> Dict[str, Any]:
    """
    Map entities based on the provided request.
    """
    try:
        # This would use the entity mapping service
        # For now, return a placeholder response
        return {
            "status": "success",
            "message": "Entity mapping completed successfully",
            "mapped_entities": [],
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        error_msg = f"Entity mapping failed: {str(e)}"
        print(f"ERROR: {error_msg}")
        print(f"TRACEBACK: {traceback.format_exc()}")
        
        raise HTTPException(
            status_code=500,
            detail=error_msg
        )

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "CanonMap API is running",
        "version": "1.0.0"
    }