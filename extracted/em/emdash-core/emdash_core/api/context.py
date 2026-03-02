"""Session context endpoints."""

from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(prefix="/context", tags=["context"])


class ContextEntity(BaseModel):
    """An entity in the context."""
    qualified_name: str
    entity_type: str
    file_path: str
    relevance: float


class SessionContext(BaseModel):
    """Current session context."""
    entities: list[ContextEntity] = Field(default_factory=list)
    files: list[str] = Field(default_factory=list)
    summary: Optional[str] = None


@router.get("", response_model=SessionContext)
async def get_context():
    """Get current session context."""
    try:
        from ..context.service import ContextService

        service = ContextService()
        ctx = service.get_context()

        return SessionContext(
            entities=[
                ContextEntity(
                    qualified_name=e.get("qualified_name", ""),
                    entity_type=e.get("type", ""),
                    file_path=e.get("file_path", ""),
                    relevance=e.get("relevance", 0.0),
                )
                for e in ctx.get("entities", [])
            ],
            files=ctx.get("files", []),
            summary=ctx.get("summary"),
        )
    except Exception:
        return SessionContext()


@router.delete("")
async def clear_context():
    """Clear session context."""
    try:
        from ..context.service import ContextService

        service = ContextService()
        service.clear()

        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


@router.get("/prompt")
async def get_context_prompt():
    """Get context as a prompt for system prompt injection."""
    try:
        from ..context.service import ContextService

        service = ContextService()
        prompt = service.get_prompt()

        return {"prompt": prompt}
    except Exception:
        return {"prompt": ""}
