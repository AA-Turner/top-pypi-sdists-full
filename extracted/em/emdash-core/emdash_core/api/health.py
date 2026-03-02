"""Health check endpoint."""

import time
from datetime import datetime
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from ..config import get_config

router = APIRouter(prefix="/health", tags=["health"])

# Server start time for uptime calculation
_start_time: float = time.time()


class DatabaseStatus(BaseModel):
    """Database connection status."""

    connected: bool
    node_count: Optional[int] = None
    relationship_count: Optional[int] = None
    error: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response."""

    status: str  # "healthy", "starting", "unhealthy"
    version: str
    uptime_seconds: float
    repo_root: Optional[str]
    database: DatabaseStatus
    timestamp: datetime


def _check_database() -> DatabaseStatus:
    """Check database connection status."""
    config = get_config()

    try:
        # Try to import and connect to database
        # This will be replaced with actual database check once services are moved
        db_path = config.database_full_path
        if db_path.exists():
            return DatabaseStatus(
                connected=True,
                node_count=0,  # TODO: Get actual counts
                relationship_count=0,
            )
        else:
            return DatabaseStatus(
                connected=False,
                error="Database not initialized"
            )
    except Exception as e:
        return DatabaseStatus(
            connected=False,
            error=str(e)
        )


@router.get("", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Check server health status."""
    from .. import __version__

    config = get_config()
    db_status = _check_database()

    status = "healthy" if db_status.connected else "starting"

    return HealthResponse(
        status=status,
        version=__version__,
        uptime_seconds=time.time() - _start_time,
        repo_root=config.repo_root,
        database=db_status,
        timestamp=datetime.now(),
    )


@router.get("/models")
async def model_config_info() -> dict:
    """Return model config path, loaded models, and env file paths."""
    from pathlib import Path

    result: dict = {}

    # Model config
    try:
        from ..agent.providers.models import ModelRegistry
        registry = ModelRegistry.get()
        result["config_path"] = registry.config_path
        result["default_model"] = registry.default_model
        result["vision_model"] = registry.vision_model
        result["fast_model"] = registry.fast_model
        result["models"] = list(registry.models.keys())
    except Exception as e:
        result["config_error"] = str(e)

    # .env files (show which ones exist and were loaded)
    config = get_config()
    env_files = []
    user_env = Path.home() / ".emdash" / ".env"
    if user_env.exists():
        env_files.append(str(user_env))
    if config.repo_root:
        root = Path(config.repo_root)
        project_env = root / ".emdash" / ".env"
        if project_env.exists():
            env_files.append(str(project_env))
        legacy_env = root / ".env"
        if legacy_env.exists():
            env_files.append(str(legacy_env))
    result["env_files"] = env_files

    return result


@router.get("/ready")
async def readiness_check() -> dict:
    """Simple readiness probe for container orchestration."""
    return {"ready": True}


@router.get("/live")
async def liveness_check() -> dict:
    """Simple liveness probe for container orchestration."""
    return {"alive": True}
