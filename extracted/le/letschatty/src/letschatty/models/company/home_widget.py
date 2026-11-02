from typing import Any, Optional
from pydantic import BaseModel, Field


class HomeWidget(BaseModel):
    """Un widget del inicio del frontend (spec 2026-10-01). `id` es libre: el catálogo vive en el frontend."""
    id: str
    tam: int = Field(ge=1, le=3)
    config: Optional[dict[str, Any]] = None
