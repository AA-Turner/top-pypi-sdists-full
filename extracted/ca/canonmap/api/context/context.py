import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from canonmap.config.validate_configs import CanonMapArtifactsConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager that sets up and tears down application state.
    """
    # Set up default artifacts config
    app.state.artifacts_config = CanonMapArtifactsConfig(
        artifacts_local_path="./artifacts",
        artifacts_gcp_bucket_name="",
        artifacts_gcp_bucket_prefix="",
        artifacts_gcp_service_account_json_path=""
    )
    
    # Set up embedder (None for now, can be configured later)
    app.state.embedder = None
    
    logger.info("🎉 CanonMap API is ready to go!")
    yield
    
    # Cleanup (if needed)
    logger.info("Shutting down CanonMap API...")

app = FastAPI(lifespan=lifespan)