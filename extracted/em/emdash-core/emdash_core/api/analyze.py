"""Analytics endpoints."""

from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/analyze", tags=["analytics"])


class PageRankResult(BaseModel):
    """PageRank result for an entity."""
    qualified_name: str
    name: str
    entity_type: str
    file_path: str
    score: float


class PageRankResponse(BaseModel):
    """PageRank response."""
    results: list[PageRankResult]
    damping: float


class CommunityMember(BaseModel):
    """A member of a community."""
    qualified_name: str
    name: str
    entity_type: str
    file_path: str


class Community(BaseModel):
    """A detected community."""
    id: int
    size: int
    description: Optional[str] = None
    members: list[CommunityMember] = Field(default_factory=list)
    top_files: list[str] = Field(default_factory=list)


class CommunityResponse(BaseModel):
    """Community detection response."""
    communities: list[Community]
    total: int


class AreaImportance(BaseModel):
    """Importance metrics for a directory/file."""
    path: str
    commit_count: int
    author_count: int
    churn: int
    importance_score: float


class AreasResponse(BaseModel):
    """Areas importance response."""
    areas: list[AreaImportance]


class BetweennessResult(BaseModel):
    """Betweenness centrality result."""
    qualified_name: str
    name: str
    entity_type: str
    score: float


def _get_analytics():
    """Get analytics engine."""
    from ..analytics.engine import AnalyticsEngine
    return AnalyticsEngine()


@router.get("/pagerank", response_model=PageRankResponse)
async def get_pagerank(top: int = 20, damping: float = 0.85):
    """Compute PageRank scores to identify important code.

    PageRank identifies code that is heavily depended upon.
    """
    try:
        engine = _get_analytics()
        results = engine.compute_pagerank(top=top, damping=damping)

        return PageRankResponse(
            results=[
                PageRankResult(
                    qualified_name=r.get("qualified_name", ""),
                    name=r.get("name", ""),
                    entity_type=r.get("type", ""),
                    file_path=r.get("file_path", ""),
                    score=r.get("score", 0.0),
                )
                for r in results
            ],
            damping=damping,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/communities", response_model=CommunityResponse)
async def get_communities(
    top: int = 10,
    resolution: float = 1.0,
    include_members: bool = False,
    query: Optional[str] = None,
):
    """Detect code communities using Louvain algorithm.

    Communities are clusters of tightly related code.

    Args:
        top: Number of top communities to return
        resolution: Louvain resolution parameter
        include_members: Include community members in response
        query: Filter communities by semantic query
    """
    try:
        engine = _get_analytics()
        communities = engine.detect_communities(
            resolution=resolution,
            top=top,
        )

        result = []
        for c in communities:
            community = Community(
                id=c.get("id", 0),
                size=c.get("size", 0),
                description=c.get("description"),
                top_files=c.get("top_files", []),
            )
            if include_members:
                community.members = [
                    CommunityMember(
                        qualified_name=m.get("qualified_name", ""),
                        name=m.get("name", ""),
                        entity_type=m.get("type", ""),
                        file_path=m.get("file_path", ""),
                    )
                    for m in c.get("members", [])
                ]
            result.append(community)

        return CommunityResponse(
            communities=result,
            total=len(result),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/communities/{community_id}")
async def get_community(community_id: int):
    """Get details of a specific community."""
    try:
        engine = _get_analytics()
        community = engine.get_community(community_id)

        if not community:
            raise HTTPException(status_code=404, detail="Community not found")

        return Community(
            id=community.get("id", community_id),
            size=community.get("size", 0),
            description=community.get("description"),
            top_files=community.get("top_files", []),
            members=[
                CommunityMember(
                    qualified_name=m.get("qualified_name", ""),
                    name=m.get("name", ""),
                    entity_type=m.get("type", ""),
                    file_path=m.get("file_path", ""),
                )
                for m in community.get("members", [])
            ],
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/areas", response_model=AreasResponse)
async def get_areas(
    depth: int = 2,
    days: int = 90,
    top: int = 20,
    sort: str = "importance",
    include_files: bool = False,
):
    """Get importance metrics by directory/file.

    Args:
        depth: Directory depth to analyze
        days: Number of days of history to consider
        top: Number of top areas to return
        sort: Sort by: importance, commits, churn, authors
        include_files: Include individual files (not just directories)
    """
    try:
        engine = _get_analytics()
        areas = engine.get_area_importance(
            depth=depth,
            days=days,
            top=top,
            sort_by=sort,
            include_files=include_files,
        )

        return AreasResponse(
            areas=[
                AreaImportance(
                    path=a.get("path", ""),
                    commit_count=a.get("commit_count", 0),
                    author_count=a.get("author_count", 0),
                    churn=a.get("churn", 0),
                    importance_score=a.get("importance_score", 0.0),
                )
                for a in areas
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/betweenness")
async def get_betweenness(top: int = 20):
    """Compute betweenness centrality.

    Identifies bridge entities that connect different parts of the codebase.
    """
    try:
        engine = _get_analytics()
        results = engine.compute_betweenness(top=top)

        return {
            "results": [
                BetweennessResult(
                    qualified_name=r.get("qualified_name", ""),
                    name=r.get("name", ""),
                    entity_type=r.get("type", ""),
                    score=r.get("score", 0.0),
                )
                for r in results
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/commit-importance")
async def get_commit_importance(top: int = 20):
    """Score files by commit frequency and author diversity."""
    try:
        engine = _get_analytics()
        results = engine.get_commit_importance(top=top)

        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
