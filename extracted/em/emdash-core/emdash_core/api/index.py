"""Indexing endpoints with SSE streaming."""

import asyncio
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from ..sse.stream import SSEHandler, EventType

router = APIRouter(prefix="/index", tags=["indexing"])

_executor = ThreadPoolExecutor(max_workers=2)


class IndexOptions(BaseModel):
    """Options for indexing operation."""
    changed_only: bool = Field(default=False, description="Only index changed files")
    index_git: bool = Field(default=False, description="Index git history")
    index_github: int = Field(default=0, description="Number of GitHub PRs to index")
    detect_communities: bool = Field(default=True, description="Run community detection")
    describe_communities: bool = Field(default=False, description="Use LLM to describe communities")
    community_limit: int = Field(default=20, description="Max communities to describe")
    model: Optional[str] = Field(default=None, description="Model for descriptions")


class IndexRequest(BaseModel):
    """Request to start indexing."""
    repo_path: str = Field(..., description="Path to repository")
    options: IndexOptions = Field(default_factory=IndexOptions)


class IndexStatus(BaseModel):
    """Current indexing status."""
    is_indexed: bool
    last_indexed: Optional[str]
    last_commit: Optional[str]
    file_count: int
    function_count: int
    class_count: int
    community_count: int


def _run_index_sync(
    repo_path: str,
    options: IndexOptions,
    sse_handler: SSEHandler,
):
    """Run indexing synchronously in thread pool."""
    from pathlib import Path

    try:
        from ..graph.connection import configure_for_repo
        from ..ingestion.orchestrator import IngestionOrchestrator

        sse_handler.emit(EventType.PROGRESS, {"step": "Starting indexing", "percent": 0})

        # Configure database for target repo
        repo_root = Path(repo_path).resolve()
        configure_for_repo(repo_root)

        # Create orchestrator (uses configured connection)
        orchestrator = IngestionOrchestrator()

        sse_handler.emit(EventType.PROGRESS, {"step": "Indexing codebase", "percent": 10})

        # Progress callback to emit SSE events during parsing
        def progress_callback(step: str, percent: float):
            sse_handler.emit(EventType.PROGRESS, {"step": step, "percent": percent})

        # Run indexing with progress callback
        result = orchestrator.index(
            repo_path=repo_path,
            changed_only=options.changed_only,
            skip_git=not options.index_git,
            pr_limit=options.index_github,
            progress_callback=progress_callback,
        )

        sse_handler.emit(EventType.PROGRESS, {"step": "Building graph", "percent": 75})

        if options.detect_communities:
            sse_handler.emit(EventType.PROGRESS, {"step": "Detecting communities", "percent": 85})

        sse_handler.emit(EventType.PROGRESS, {"step": "Indexing complete", "percent": 100})

        sse_handler.emit(EventType.RESPONSE, {
            "success": True,
            "stats": result if isinstance(result, dict) else {},
        })

    except Exception as e:
        sse_handler.emit(EventType.ERROR, {
            "message": str(e),
        })
    finally:
        sse_handler.close()


@router.post("/start")
async def index_start(request: IndexRequest):
    """Start indexing a repository with SSE streaming progress.

    Returns a Server-Sent Events stream with progress updates.
    """
    if os.environ.get("EMDASH_INDEXING_ENABLED", "true").lower() != "true":
        raise HTTPException(status_code=403, detail="Indexing is disabled via settings")

    sse_handler = SSEHandler(agent_name="Indexer")

    async def run_indexing():
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            _executor,
            _run_index_sync,
            request.repo_path,
            request.options,
            sse_handler,
        )

    asyncio.create_task(run_indexing())

    return StreamingResponse(
        sse_handler,
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


@router.get("/status", response_model=IndexStatus)
async def index_status(repo_path: str):
    """Get current indexing status for a repository."""
    try:
        from pathlib import Path
        from ..graph.connection import configure_for_repo

        # Configure database for the target repo
        repo_root = Path(repo_path).resolve()
        conn = configure_for_repo(repo_root)
        info = conn.get_database_info()

        return IndexStatus(
            is_indexed=info.get("node_count", 0) > 0,
            last_indexed=None,  # TODO: Track this
            last_commit=None,
            file_count=info.get("file_count", 0),
            function_count=info.get("function_count", 0),
            class_count=info.get("class_count", 0),
            community_count=info.get("community_count", 0),
        )
    except Exception:
        return IndexStatus(
            is_indexed=False,
            last_indexed=None,
            last_commit=None,
            file_count=0,
            function_count=0,
            class_count=0,
            community_count=0,
        )
