"""Public API endpoints for health checks and system status."""

import os
import sys
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from urllib.parse import urlparse

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from pydantic import BaseModel
from sqlalchemy import func, text
from sqlmodel import Session, select

from src.database import get_session
from src.domain.project import Project
from src.domain.release import Release, ReleaseStatus
from src.domain.ticket import Ticket, TicketStatus
from src.env_loader import get_environment
from src.version import get_version


def _extract_db_host(database_url: str) -> str:
    """Extract just the hostname from a DATABASE_URL, no credentials or path."""
    if not database_url:
        return "(unknown)"
    try:
        host = urlparse(database_url).hostname
        return host or "(unknown)"
    except Exception:
        return "(unknown)"


# Base response model
class BaseResponse(BaseModel):
    """Base response model for all API responses"""


router = APIRouter(prefix="/api/v1/public", tags=["public"])


class HealthResponse(BaseResponse):
    """Health check response model."""

    status: str
    timestamp: datetime
    version: Optional[str] = None
    python_version: str
    database: Optional[str] = None
    uptime_seconds: Optional[float] = None


class StatusResponse(BaseResponse):
    """System status response model."""

    status: str
    timestamp: datetime
    version: Optional[str] = None
    environment: str
    port: int
    env_file: str
    db_host: str
    components: Dict[str, str]
    metrics: Optional[Dict[str, Any]] = None


class ImpactNumbers(BaseResponse):
    """How much work InnoDay is carrying, and how much of it went out.

    **Counts only, never names.** This route is unauthenticated, so what it may
    say is bounded by what a stranger is allowed to know: how many projects are
    tracked, how many releases have gone to production, and how many tickets rode
    them out. Whose projects, whose releases and what they were called are not
    here and must not be added.
    """

    #: Projects InnoDay tracks, across every organization.
    projects: int
    #: Releases that actually went out -- `released`, not planned or in flight.
    releases: int
    #: Tickets somebody is building right now.
    features: int
    #: When these were counted. They are cached, so it is not "now".
    counted_at: datetime


class VersionResponse(BaseResponse):
    """Version information response model."""

    version: str
    api_version: str
    python_version: str
    git_commit: Optional[str] = None
    build_date: Optional[str] = None


# Store startup time for uptime calculation
_startup_time = datetime.now(timezone.utc)


@router.get("/health", response_model=HealthResponse)
async def health_check(
    db: Session = Depends(get_session), response: Response = None
) -> HealthResponse:
    """
    Health check endpoint for monitoring.

    Returns basic health status and database connectivity.
    """
    # Check database connectivity
    db_status = "disconnected"
    try:
        result = db.execute(text("SELECT 1"))
        if result.scalar() == 1:
            db_status = "connected"
    except Exception:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    # Calculate uptime
    uptime = (datetime.now(timezone.utc) - _startup_time).total_seconds()

    version = get_version()

    return HealthResponse(
        status="healthy" if db_status == "connected" else "unhealthy",
        timestamp=datetime.now(timezone.utc),
        version=version,
        python_version=sys.version,
        database=db_status,
        uptime_seconds=uptime,
    )


@router.get("/status", response_model=StatusResponse)
async def system_status(
    request: Request, db: Session = Depends(get_session)
) -> StatusResponse:
    """
    Detailed system status endpoint.

    Returns comprehensive status of all system components.
    """
    components = {}

    # Check database
    try:
        result = db.execute(text("SELECT COUNT(*) FROM organizations"))
        result.scalar()
        components["database"] = "operational"

        # Get table counts for metrics
        metrics = {}
        for table in [
            "organizations",
            "users",
            "projects",
            "repositories",
            "tickets",
            "boards",
        ]:
            try:
                result = db.execute(text(f"SELECT COUNT(*) FROM {table}"))
                metrics[f"{table}_count"] = result.scalar()
            except Exception:
                metrics[f"{table}_count"] = 0
    except Exception:
        components["database"] = "error"
        metrics = None

    # Check API
    components["api"] = "operational"

    # Check integrations (basic check)
    components["github"] = "unknown"
    components["jira"] = "unknown"
    components["trello"] = "unknown"
    components["claude"] = "unknown"

    # Both fields come from the shared resolvers -- src.version.get_version()
    # and src.env_loader.get_environment() -- and so does /health (#619). The
    # three reporting endpoints here each used to read
    # `metadata.version("innoday")`, which is only one of get_version()'s four
    # sources and the wrong one inside a deployed container: it answered
    # `0.1.0b0` while /health, from the version baked into the image, answered
    # `0.1.0-beta` seconds later.
    environment = get_environment()

    version = get_version()

    port = getattr(request.app.state, "port", None) or int(os.getenv("PORT", 8002))
    env_file = getattr(request.app.state, "env_file", "(unknown)")
    db_host = _extract_db_host(os.getenv("DATABASE_URL", ""))

    return StatusResponse(
        status=(
            "operational" if components.get("database") == "operational" else "degraded"
        ),
        timestamp=datetime.now(timezone.utc),
        version=version,
        environment=environment,
        port=port,
        env_file=env_file,
        db_host=db_host,
        components=components,
        metrics=metrics,
    )


#: How long a set of counts is served before the database is asked again.
#:
#: This is the one route on the product's public front page, so it is the one
#: route a crawler, a link unfurl or a bad afternoon can hit without a session.
#: The numbers move a few times a day; asking three aggregates per visitor to
#: track that would be paying continuously for a figure nobody watches change.
_IMPACT_TTL_SECONDS = 300

_impact_cache: Optional[tuple[datetime, "ImpactNumbers"]] = None


def _count_impact(db: Session) -> "ImpactNumbers":
    """The three numbers, in three aggregates.

    **`features` counts work in flight, not work delivered.** It was the second
    for one afternoon, and the answer was 8 against 169 releases -- true, and
    useless: the ticket/release join is free text nobody fills in, so a count of
    tickets tagged to a shipped version measures how diligently versions get
    typed rather than how much went out. What is being built right now is a
    number the boards actually carry.

    **Both spellings of every status.** Enum storage in this schema is
    inconsistent -- some columns hold the lowercase value, some hold the member
    NAME (see `src/services/ticket_release.py`, which filters in Python rather
    than bet on which) -- and a status comparison that guesses wrong here does
    not fail. It answers zero, and a front page reporting zero releases is worse
    than one reporting nothing at all.
    """
    released = [ReleaseStatus.RELEASED.value, ReleaseStatus.RELEASED.name]
    # Being built, which is narrower than "open". A TODO is queued, and counting
    # the queue as work in progress is how a number like this stops being true.
    building = [
        TicketStatus.IN_PROGRESS.value,
        TicketStatus.IN_PROGRESS.name,
        TicketStatus.IN_REVIEW.value,
        TicketStatus.IN_REVIEW.name,
    ]

    projects = db.exec(select(func.count()).select_from(Project)).one()

    releases = db.exec(
        select(func.count())
        .select_from(Release)
        .where(Release.status.in_(released), Release.deleted_at.is_(None))
    ).one()

    features = db.exec(
        select(func.count())
        .select_from(Ticket)
        .where(Ticket.status.in_(building), Ticket.deleted_at.is_(None))
    ).one()

    return ImpactNumbers(
        projects=projects,
        releases=releases,
        features=features,
        counted_at=datetime.now(timezone.utc),
    )


@router.get("/impact", response_model=ImpactNumbers)
async def impact_numbers(db: Session = Depends(get_session)) -> ImpactNumbers:
    """Projects served, releases shipped, features being built. No names.

    The public site says what InnoDay is carrying, and a claim on a front page
    should be the product's own answer rather than a figure somebody typed into
    a template and stopped updating. So it is read from here, live.

    A caller that cannot reach the database gets a 503 rather than zeros --
    "nothing has shipped" is a statement, and it must never be made by accident.
    """
    global _impact_cache

    now = datetime.now(timezone.utc)
    if _impact_cache is not None:
        counted_at, cached = _impact_cache
        if (now - counted_at).total_seconds() < _IMPACT_TTL_SECONDS:
            return cached

    try:
        numbers = _count_impact(db)
    except Exception:
        # Serve a stale answer over no answer: the numbers move slowly, and a
        # front page with yesterday's count is right in every way that matters
        # to a reader.
        if _impact_cache is not None:
            return _impact_cache[1]
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Counts are unavailable.",
        )

    _impact_cache = (numbers.counted_at, numbers)
    return numbers


@router.get("/version", response_model=VersionResponse)
async def version_info() -> VersionResponse:
    """
    Version information endpoint.

    Returns version details for the API and runtime.
    """
    version = get_version()

    # Get git commit if available
    git_commit = os.getenv("GIT_COMMIT", None)

    # Get build date if available
    build_date = os.getenv("BUILD_DATE", None)

    return VersionResponse(
        version=version,
        api_version="v1",
        python_version=sys.version,
        git_commit=git_commit,
        build_date=build_date,
    )


@router.get("/ping")
async def ping() -> Dict[str, str]:
    """
    Simple ping endpoint.

    Returns a pong response for basic connectivity testing.
    """
    return {"message": "pong", "timestamp": datetime.now(timezone.utc).isoformat()}


@router.head("/health")
async def health_check_head(
    db: Session = Depends(get_session), response: Response = None
) -> None:
    """
    HEAD health check endpoint.

    Returns only status code for lightweight monitoring.
    """
    try:
        result = db.execute(text("SELECT 1"))
        if result.scalar() != 1:
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    except Exception:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
