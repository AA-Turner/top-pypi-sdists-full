"""Models for mermaid diagram operations."""

from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class MermaidDiagramRequest(BaseModel):
    """Request model for mermaid diagram generation."""

    model_config = ConfigDict(extra="ignore")

    code: str = Field(..., description="Mermaid diagram code")


class MermaidDiagramResponse(BaseModel):
    """Response model for mermaid diagram generation (FILE mode)."""

    model_config = ConfigDict(extra="ignore")

    file_url: str = Field(..., description="URL to the generated diagram file")


# Type aliases for clarity
ContentType = Literal["svg", "png"]
ResponseType = Literal["file", "raw"]
