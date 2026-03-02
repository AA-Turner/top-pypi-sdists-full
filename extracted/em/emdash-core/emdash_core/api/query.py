"""Graph query endpoints."""

from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/query", tags=["query"])


class EntityResult(BaseModel):
    """A code entity result."""
    qualified_name: str
    name: str
    entity_type: str
    file_path: str
    line_number: Optional[int] = None
    source: Optional[str] = None


class ExpandRequest(BaseModel):
    """Request to expand a node."""
    entity_type: str = Field(..., description="Type: File, Class, Function")
    qualified_name: str = Field(..., description="Qualified name of entity")
    max_hops: int = Field(default=2, description="Max traversal depth")
    include_source: bool = Field(default=True, description="Include source code")


class ExpandResponse(BaseModel):
    """Expanded node with relationships."""
    entity: EntityResult
    callers: list[EntityResult] = Field(default_factory=list)
    callees: list[EntityResult] = Field(default_factory=list)
    dependencies: list[EntityResult] = Field(default_factory=list)
    dependents: list[EntityResult] = Field(default_factory=list)


class KnowledgeSilo(BaseModel):
    """A knowledge silo - critical code with few maintainers."""
    file_path: str
    importance_score: float
    author_count: int
    authors: list[str]
    function_count: int


def _get_toolkit():
    """Get agent toolkit."""
    from ..agent.toolkit import AgentToolkit
    return AgentToolkit()


@router.get("/find-class/{name}")
async def find_class(name: str):
    """Find a class by name."""
    try:
        toolkit = _get_toolkit()
        result = toolkit.text_search(query=name, entity_types=["Class"])

        if not result.success:
            raise HTTPException(status_code=500, detail=result.error)

        return {
            "results": [
                EntityResult(
                    qualified_name=r.get("qualified_name", ""),
                    name=r.get("name", ""),
                    entity_type="Class",
                    file_path=r.get("file_path", ""),
                    line_number=r.get("line_number"),
                )
                for r in result.data.get("results", [])
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/find-function/{name}")
async def find_function(name: str):
    """Find a function by name."""
    try:
        toolkit = _get_toolkit()
        result = toolkit.text_search(query=name, entity_types=["Function"])

        if not result.success:
            raise HTTPException(status_code=500, detail=result.error)

        return {
            "results": [
                EntityResult(
                    qualified_name=r.get("qualified_name", ""),
                    name=r.get("name", ""),
                    entity_type="Function",
                    file_path=r.get("file_path", ""),
                    line_number=r.get("line_number"),
                )
                for r in result.data.get("results", [])
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/expand", response_model=ExpandResponse)
async def expand_node(request: ExpandRequest):
    """Expand a node to see its relationships.

    Returns callers, callees, dependencies, and dependents.
    """
    try:
        toolkit = _get_toolkit()
        result = toolkit.expand(
            entity_type=request.entity_type,
            qualified_name=request.qualified_name,
        )

        if not result.success:
            raise HTTPException(status_code=500, detail=result.error)

        data = result.data
        entity_data = data.get("entity", {})

        return ExpandResponse(
            entity=EntityResult(
                qualified_name=entity_data.get("qualified_name", request.qualified_name),
                name=entity_data.get("name", ""),
                entity_type=request.entity_type,
                file_path=entity_data.get("file_path", ""),
                line_number=entity_data.get("line_number"),
                source=entity_data.get("source") if request.include_source else None,
            ),
            callers=[
                EntityResult(
                    qualified_name=c.get("qualified_name", ""),
                    name=c.get("name", ""),
                    entity_type=c.get("type", ""),
                    file_path=c.get("file_path", ""),
                )
                for c in data.get("callers", [])
            ],
            callees=[
                EntityResult(
                    qualified_name=c.get("qualified_name", ""),
                    name=c.get("name", ""),
                    entity_type=c.get("type", ""),
                    file_path=c.get("file_path", ""),
                )
                for c in data.get("callees", [])
            ],
            dependencies=[
                EntityResult(
                    qualified_name=d.get("qualified_name", ""),
                    name=d.get("name", ""),
                    entity_type=d.get("type", ""),
                    file_path=d.get("file_path", ""),
                )
                for d in data.get("dependencies", [])
            ],
            dependents=[
                EntityResult(
                    qualified_name=d.get("qualified_name", ""),
                    name=d.get("name", ""),
                    entity_type=d.get("type", ""),
                    file_path=d.get("file_path", ""),
                )
                for d in data.get("dependents", [])
            ],
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/callers/{qualified_name:path}")
async def get_callers(qualified_name: str, depth: int = 1):
    """Get all callers of a function."""
    try:
        toolkit = _get_toolkit()
        result = toolkit.get_callers(qualified_name=qualified_name, depth=depth)

        if not result.success:
            raise HTTPException(status_code=500, detail=result.error)

        return {
            "callers": [
                EntityResult(
                    qualified_name=c.get("qualified_name", ""),
                    name=c.get("name", ""),
                    entity_type=c.get("type", "Function"),
                    file_path=c.get("file_path", ""),
                )
                for c in result.data.get("callers", [])
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/callees/{qualified_name:path}")
async def get_callees(qualified_name: str, depth: int = 1):
    """Get all callees of a function."""
    try:
        toolkit = _get_toolkit()
        result = toolkit.get_callees(qualified_name=qualified_name, depth=depth)

        if not result.success:
            raise HTTPException(status_code=500, detail=result.error)

        return {
            "callees": [
                EntityResult(
                    qualified_name=c.get("qualified_name", ""),
                    name=c.get("name", ""),
                    entity_type=c.get("type", "Function"),
                    file_path=c.get("file_path", ""),
                )
                for c in result.data.get("callees", [])
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/hierarchy/{class_name:path}")
async def get_class_hierarchy(class_name: str, direction: str = "both"):
    """Get class inheritance hierarchy.

    Args:
        class_name: Qualified name of class
        direction: 'up' (parents), 'down' (children), or 'both'
    """
    try:
        toolkit = _get_toolkit()
        result = toolkit.get_class_hierarchy(
            class_name=class_name,
            direction=direction,
        )

        if not result.success:
            raise HTTPException(status_code=500, detail=result.error)

        return result.data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dependencies/{file_path:path}")
async def get_file_dependencies(file_path: str, direction: str = "both"):
    """Get file import dependencies.

    Args:
        file_path: Path to file
        direction: 'imports', 'imported_by', or 'both'
    """
    try:
        toolkit = _get_toolkit()
        result = toolkit.get_file_dependencies(
            file_path=file_path,
            direction=direction,
        )

        if not result.success:
            raise HTTPException(status_code=500, detail=result.error)

        return result.data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/knowledge-silos")
async def get_knowledge_silos(
    threshold: float = 0.7,
    max_authors: int = 2,
    top: int = 20,
):
    """Detect knowledge silos - critical code with few maintainers.

    Args:
        threshold: Minimum importance score
        max_authors: Maximum number of authors to be considered a silo
        top: Number of silos to return
    """
    try:
        from ..analytics.engine import AnalyticsEngine

        engine = AnalyticsEngine()
        silos = engine.detect_knowledge_silos(
            importance_threshold=threshold,
            max_authors=max_authors,
            top=top,
        )

        return {
            "silos": [
                KnowledgeSilo(
                    file_path=s.get("file_path", ""),
                    importance_score=s.get("importance_score", 0.0),
                    author_count=s.get("author_count", 0),
                    authors=s.get("authors", []),
                    function_count=s.get("function_count", 0),
                )
                for s in silos
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
