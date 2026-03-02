"""Planning endpoints."""

from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/plan", tags=["planning"])


class PlanContextRequest(BaseModel):
    """Request for planning context."""
    repo_path: str = Field(..., description="Path to repository")
    description: str = Field(..., description="Feature description")
    similar_prs: int = Field(default=5, description="Number of similar PRs to find")


class SimilarPR(BaseModel):
    """A similar PR."""
    number: int
    title: str
    score: float
    files: list[str] = Field(default_factory=list)


class PlanContextResponse(BaseModel):
    """Planning context response."""
    description: str
    similar_prs: list[SimilarPR]
    relevant_files: list[str]
    relevant_functions: list[str]
    suggested_approach: Optional[str] = None


def _get_toolkit():
    """Get agent toolkit."""
    from ..agent.toolkit import AgentToolkit
    return AgentToolkit()


@router.post("/context", response_model=PlanContextResponse)
async def get_plan_context(request: PlanContextRequest):
    """Get planning context for a feature.

    Returns similar PRs, relevant files, and suggested approach.
    """
    from pathlib import Path
    from ..graph.connection import configure_for_repo

    try:
        # Configure database for the repo
        repo_root = Path(request.repo_path).resolve()
        configure_for_repo(repo_root)

        toolkit = _get_toolkit()

        # Search for relevant code
        search_result = toolkit.search(query=request.description, limit=10)

        relevant_files = []
        relevant_functions = []
        if search_result.success:
            for r in search_result.data.get("results", []):
                if r.get("type") == "File":
                    relevant_files.append(r.get("file_path", ""))
                else:
                    relevant_functions.append(r.get("qualified_name", ""))

        # TODO: Find similar PRs using embedding search
        similar_prs = []

        return PlanContextResponse(
            description=request.description,
            similar_prs=similar_prs,
            relevant_files=relevant_files[:10],
            relevant_functions=relevant_functions[:10],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/similar")
async def find_similar_prs(repo_path: str, description: str, limit: int = 5):
    """Find PRs similar to a feature description."""
    from pathlib import Path
    from ..graph.connection import configure_for_repo

    try:
        # Configure database for the repo
        repo_root = Path(repo_path).resolve()
        configure_for_repo(repo_root)

        from ..planning.similarity import SimilaritySearch

        search = SimilaritySearch()
        results = search.find_similar_prs(description, limit=limit)

        return {
            "similar_prs": [
                SimilarPR(
                    number=pr.get("number", 0),
                    title=pr.get("title", ""),
                    score=pr.get("score", 0.0),
                    files=pr.get("files", []),
                )
                for pr in results
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
