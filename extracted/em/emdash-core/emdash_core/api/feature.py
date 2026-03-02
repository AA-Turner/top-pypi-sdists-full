"""Feature analysis endpoints."""

from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/feature", tags=["feature"])


class FeatureContextRequest(BaseModel):
    """Request for feature context."""
    query: str = Field(..., description="Feature query")
    hops: int = Field(default=2, description="Graph traversal hops")


class FeatureEntity(BaseModel):
    """An entity related to a feature."""
    qualified_name: str
    name: str
    entity_type: str
    file_path: str
    relationship: str  # calls, called_by, imports, etc.


class FeatureContextResponse(BaseModel):
    """Feature context response."""
    query: str
    root_entities: list[FeatureEntity]
    related_entities: list[FeatureEntity]
    files: list[str]


class FeatureExplainRequest(BaseModel):
    """Request for LLM feature explanation."""
    query: str = Field(..., description="Feature query")
    hops: int = Field(default=2, description="Graph traversal hops")
    style: str = Field(default="technical", description="Style: technical, simple, detailed")
    model: Optional[str] = Field(default=None, description="LLM model")


@router.post("/context", response_model=FeatureContextResponse)
async def get_feature_context(request: FeatureContextRequest):
    """Find a feature and expand its AST graph.

    Searches for code matching the query and expands the graph
    to find related entities.
    """
    try:
        import sys
        from pathlib import Path

        from ..agent.toolkit import AgentToolkit

        toolkit = AgentToolkit()

        # Search for matching entities
        search_result = toolkit.search(query=request.query, limit=5)

        if not search_result.success:
            raise HTTPException(status_code=500, detail=search_result.error)

        root_entities = []
        related_entities = []
        files = set()

        for r in search_result.data.get("results", []):
            entity = FeatureEntity(
                qualified_name=r.get("qualified_name", ""),
                name=r.get("name", ""),
                entity_type=r.get("type", ""),
                file_path=r.get("file_path", ""),
                relationship="root",
            )
            root_entities.append(entity)
            files.add(r.get("file_path", ""))

            # Expand each entity
            if request.hops > 0:
                expand_result = toolkit.expand(
                    entity_type=r.get("type", "Function"),
                    qualified_name=r.get("qualified_name", ""),
                )

                if expand_result.success:
                    for rel_type in ["callers", "callees", "dependencies"]:
                        for related in expand_result.data.get(rel_type, []):
                            related_entities.append(FeatureEntity(
                                qualified_name=related.get("qualified_name", ""),
                                name=related.get("name", ""),
                                entity_type=related.get("type", ""),
                                file_path=related.get("file_path", ""),
                                relationship=rel_type,
                            ))
                            files.add(related.get("file_path", ""))

        return FeatureContextResponse(
            query=request.query,
            root_entities=root_entities,
            related_entities=related_entities[:20],  # Limit
            files=list(files)[:20],
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/explain")
async def explain_feature(request: FeatureExplainRequest):
    """Explain a feature using LLM based on AST graph."""
    try:
        import sys
        from pathlib import Path

        from ..planning.llm_explainer import LLMExplainer

        explainer = LLMExplainer(model=request.model)

        # Get context first
        context_request = FeatureContextRequest(
            query=request.query,
            hops=request.hops,
        )
        context = await get_feature_context(context_request)

        # Generate explanation
        explanation = explainer.explain(
            query=request.query,
            context=context.model_dump(),
            style=request.style,
        )

        return {
            "query": request.query,
            "explanation": explanation,
            "entities_analyzed": len(context.root_entities) + len(context.related_entities),
            "files_analyzed": len(context.files),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
