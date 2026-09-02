"""
Unified search API endpoints for tickets and repositories.

This module provides organization-scoped search functionality for:
- Full-text search across tickets and repositories
- Semantic search using embeddings
- Search statistics and management
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlmodel import Session, or_, select

from src.database import get_session
from src.domain.organization import Organization
from src.domain.repository import Repository
from src.domain.ticket import Ticket
from src.middleware.rbac import require_org_role

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["search"])


# Request/Response Models
class SearchRequest(BaseModel):
    """Search request parameters"""

    query: str = Field(description="Search query string")
    search_type: str = Field(
        default="all", description="Type: all, tickets, repositories"
    )
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
    include_archived: bool = Field(default=False)
    filters: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional filters"
    )


class SearchResult(BaseModel):
    """Individual search result"""

    id: UUID
    type: str  # ticket, repository
    title: str
    description: Optional[str] = None
    url: Optional[str] = None
    score: float = Field(description="Relevance score")
    highlights: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SearchResponse(BaseModel):
    """Search response with results and metadata"""

    results: List[SearchResult]
    total: int
    query: str
    took_ms: int
    facets: Optional[Dict[str, Any]] = None


class SimilaritySearchRequest(BaseModel):
    """Request for finding similar content"""

    content: str = Field(description="Content to find similar items for")
    limit: int = Field(default=10, ge=1, le=50)
    threshold: float = Field(default=0.7, ge=0.0, le=1.0)
    search_type: str = Field(
        default="all", description="Type: all, tickets, repositories"
    )


class EmbeddingStatistics(BaseModel):
    """Statistics about embeddings in the system"""

    total_documents: int
    embedded_documents: int
    missing_embeddings: int
    last_update: Optional[datetime] = None
    by_type: Dict[str, int]


class EmbeddingRefreshRequest(BaseModel):
    """Request to refresh embeddings"""

    force: bool = Field(
        default=False, description="Force re-embedding of all documents"
    )
    document_types: Optional[List[str]] = Field(
        default=None, description="Specific types to refresh"
    )
    batch_size: int = Field(default=100, ge=1, le=1000)


# Search Endpoints
@router.get("/organizations/{organization_id}/search")
async def search_get(
    organization_id: UUID,
    q: str = Query(..., description="Search query"),
    type: Optional[str] = Query(None, description="Filter by type"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
) -> SearchResponse:
    """
    Perform a search across tickets and repositories.

    Simple GET endpoint for basic search queries.
    """

    # Build search query
    results = []

    # Search tickets if type is 'all' or 'tickets'
    if not type or type in ["all", "tickets"]:
        ticket_query = (
            select(Ticket)
            .where(
                Ticket.organization_id == organization_id,
                # Exclude soft-deleted tickets from user-facing search results.
                Ticket.deleted_at.is_(None),
                or_(
                    Ticket.summary.contains(q),
                    Ticket.description.contains(q),
                ),
            )
            .limit(limit)
            .offset(offset)
        )

        tickets = session.exec(ticket_query).all()
        for ticket in tickets:
            results.append(
                SearchResult(
                    id=ticket.id,
                    type="ticket",
                    title=ticket.summary,
                    description=ticket.description,
                    score=1.0,  # Simple search doesn't calculate scores
                    metadata={
                        "status": ticket.status,
                        "created_at": ticket.created_at.isoformat(),
                    },
                )
            )

    # Search repositories if type is 'all' or 'repositories'
    if not type or type in ["all", "repositories"]:
        repo_query = (
            select(Repository)
            .where(
                Repository.organization_id == organization_id,
                or_(
                    Repository.name.contains(q),
                    Repository.description.contains(q),
                ),
            )
            .limit(limit)
            .offset(offset)
        )

        repos = session.exec(repo_query).all()
        for repo in repos:
            results.append(
                SearchResult(
                    id=repo.id,
                    type="repository",
                    title=repo.name,
                    description=repo.description,
                    url=repo.url,
                    score=1.0,
                    metadata={"platform": repo.platform},
                )
            )

    return SearchResponse(
        results=results,
        total=len(results),
        query=q,
        took_ms=0,  # TODO: Implement timing
    )


@router.post("/organizations/{organization_id}/search")
async def search_post(
    organization_id: UUID,
    request: SearchRequest,
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
) -> SearchResponse:
    """
    Perform an advanced search with filters and options.

    POST endpoint for complex search queries with filters.
    """

    # TODO: Implement advanced search with filters
    # This would support:
    # - Date range filters
    # - Status filters
    # - User filters
    # - Custom field filters

    # For now, delegate to simple search
    return await search_get(
        organization_id=organization_id,
        q=request.query,
        type=request.search_type if request.search_type != "all" else None,
        limit=request.limit,
        offset=request.offset,
        session=session,
    )


@router.post("/organizations/{organization_id}/search/similar")
async def search_similar(
    organization_id: UUID,
    request: SimilaritySearchRequest,
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
) -> SearchResponse:
    """
    Find similar tickets or repositories using semantic search.

    Uses embeddings to find semantically similar content.
    """

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Semantic similarity search is not implemented. Not implemented -- this previously returned a fabricated success. See GitHub issue #374.",
    )


# Embedding Management Endpoints
@router.get("/organizations/{organization_id}/embeddings/statistics")
async def get_embedding_statistics(
    organization_id: UUID,
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
) -> EmbeddingStatistics:
    """
    Get statistics about embeddings in the organization.

    Shows how many documents have embeddings and which need processing.
    """

    # Count tickets
    ticket_count = session.exec(
        select(Ticket).where(Ticket.organization_id == organization_id)
    ).count()

    # Count repositories
    repo_count = session.exec(
        select(Repository).where(Repository.organization_id == organization_id)
    ).count()

    total = ticket_count + repo_count

    # TODO: Implement actual embedding counting
    # This would query the embeddings table/service

    return EmbeddingStatistics(
        total_documents=total,
        embedded_documents=0,  # TODO: Count actual embeddings
        missing_embeddings=total,  # TODO: Calculate actual missing
        last_update=None,
        by_type={
            "tickets": ticket_count,
            "repositories": repo_count,
        },
    )


@router.post("/organizations/{organization_id}/embeddings/refresh")
async def refresh_embeddings(
    organization_id: UUID,
    request: EmbeddingRefreshRequest,
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
) -> dict:
    """
    Refresh embeddings for documents in the organization.

    This triggers background processing to generate or update embeddings.
    """

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Embedding refresh is not implemented. Not implemented -- this previously returned a fabricated success. See GitHub issue #374.",
    )


@router.get("/organizations/{organization_id}/embeddings/missing")
async def get_missing_embeddings(
    organization_id: UUID,
    limit: int = Query(100, ge=1, le=1000),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
) -> dict:
    """
    Get list of documents missing embeddings.

    Useful for debugging and monitoring embedding coverage.
    """

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Embedding coverage reporting is not implemented. Not implemented -- this previously returned a fabricated success. See GitHub issue #374.",
    )
