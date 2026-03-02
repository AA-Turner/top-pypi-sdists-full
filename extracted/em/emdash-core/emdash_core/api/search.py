"""Search endpoints."""

from enum import Enum
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/search", tags=["search"])


class SearchType(str, Enum):
    """Type of search to perform."""
    SEMANTIC = "semantic"
    TEXT = "text"


class SearchRequest(BaseModel):
    """Search request."""
    repo_path: str = Field(..., description="Path to repository")
    query: str = Field(..., description="Search query")
    type: SearchType = Field(default=SearchType.SEMANTIC, description="Search type")
    limit: int = Field(default=20, description="Maximum results")
    entity_types: list[str] = Field(default_factory=list, description="Filter by types: File, Function, Class")
    min_score: float = Field(default=0.0, description="Minimum similarity score")
    include_importance: bool = Field(default=True, description="Include importance ranking")
    include_snippets: bool = Field(default=True, description="Include code snippets")


class SearchResult(BaseModel):
    """A single search result."""
    qualified_name: str
    name: str
    entity_type: str
    file_path: str
    line_number: Optional[int] = None
    score: float
    importance: Optional[float] = None
    snippet: Optional[str] = None


class SearchResponse(BaseModel):
    """Search response."""
    results: list[SearchResult]
    total: int
    query: str
    search_type: str


def _get_toolkit():
    """Get agent toolkit for search."""
    from ..agent.toolkit import AgentToolkit
    return AgentToolkit()


@router.post("", response_model=SearchResponse)
async def search(request: SearchRequest):
    """Search the codebase.

    Supports semantic search (by meaning) and text search (exact match).
    """
    from pathlib import Path
    from ..graph.connection import configure_for_repo

    try:
        # Configure database for the repo
        repo_root = Path(request.repo_path).resolve()
        configure_for_repo(repo_root)

        toolkit = _get_toolkit()

        if request.type == SearchType.SEMANTIC:
            result = toolkit.search(
                query=request.query,
                limit=request.limit,
            )
        else:
            result = toolkit.text_search(
                query=request.query,
                limit=request.limit,
            )

        if not result.success:
            raise HTTPException(status_code=500, detail=result.error)

        # Convert results
        results = []
        for item in result.data.get("results", []):
            results.append(SearchResult(
                qualified_name=item.get("qualified_name", ""),
                name=item.get("name", ""),
                entity_type=item.get("type", ""),
                file_path=item.get("file_path", ""),
                line_number=item.get("line_number"),
                score=item.get("score", 0.0),
                importance=item.get("importance") if request.include_importance else None,
                snippet=item.get("snippet") if request.include_snippets else None,
            ))

        return SearchResponse(
            results=results,
            total=len(results),
            query=request.query,
            search_type=request.type.value,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/quick")
async def quick_search(repo_path: str, q: str, limit: int = 10):
    """Quick semantic search endpoint.

    Simple GET endpoint for quick searches.
    """
    request = SearchRequest(repo_path=repo_path, query=q, limit=limit)
    return await search(request)
