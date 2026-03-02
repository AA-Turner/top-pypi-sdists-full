"""Team analytics endpoints with SSE streaming."""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from ..sse.stream import SSEHandler, EventType

router = APIRouter(prefix="/team", tags=["team"])

_executor = ThreadPoolExecutor(max_workers=2)


class TeamFocusRequest(BaseModel):
    """Request for team focus analysis."""
    days: int = Field(default=7, description="Number of days to analyze")
    model: Optional[str] = Field(default=None, description="LLM model for summaries")
    include_graph: bool = Field(default=True, description="Include graph analysis")


class AuthorFocus(BaseModel):
    """Focus area for an author."""
    author: str
    email: str
    commit_count: int
    files_touched: int
    areas: list[str]
    recent_work: str


class TeamFocusResponse(BaseModel):
    """Team focus response."""
    period_days: int
    authors: list[AuthorFocus]
    summary: Optional[str] = None


def _run_team_focus_sync(
    days: int,
    model: Optional[str],
    include_graph: bool,
    sse_handler: SSEHandler,
):
    """Run team focus analysis synchronously."""
    try:
        from ..planning.team_focus import TeamFocusAnalyzer

        analyzer = TeamFocusAnalyzer(model=model)

        sse_handler.emit(EventType.PROGRESS, {
            "step": "Analyzing git history",
            "percent": 20,
        })

        result = analyzer.analyze(days=days, include_graph=include_graph)

        sse_handler.emit(EventType.PROGRESS, {
            "step": "Generating summary",
            "percent": 80,
        })

        authors = [
            AuthorFocus(
                author=a.get("name", ""),
                email=a.get("email", ""),
                commit_count=a.get("commit_count", 0),
                files_touched=a.get("files_touched", 0),
                areas=a.get("areas", []),
                recent_work=a.get("summary", ""),
            )
            for a in result.get("authors", [])
        ]

        sse_handler.emit(EventType.RESPONSE, {
            "period_days": days,
            "authors": [a.model_dump() for a in authors],
            "summary": result.get("summary"),
        })

    except Exception as e:
        sse_handler.emit(EventType.ERROR, {"message": str(e)})
    finally:
        sse_handler.close()


@router.post("/focus")
async def get_team_focus(request: TeamFocusRequest):
    """Get team's recent focus and work-in-progress.

    Analyzes git history to understand what each team member is working on.
    """
    sse_handler = SSEHandler(agent_name="TeamFocus")

    sse_handler.emit(EventType.SESSION_START, {
        "agent_name": "TeamFocus",
        "days": request.days,
    })

    async def run():
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            _executor,
            _run_team_focus_sync,
            request.days,
            request.model,
            request.include_graph,
            sse_handler,
        )

    asyncio.create_task(run())

    return StreamingResponse(
        sse_handler,
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )
