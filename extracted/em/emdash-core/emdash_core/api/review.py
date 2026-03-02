"""PR review endpoints with SSE streaming."""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from ..sse.stream import SSEHandler, EventType

router = APIRouter(prefix="/review", tags=["review"])

_executor = ThreadPoolExecutor(max_workers=2)


class ReviewRequest(BaseModel):
    """Request for PR review."""
    pr_number: Optional[int] = Field(default=None, description="PR number")
    pr_url: Optional[str] = Field(default=None, description="PR URL")
    search: Optional[str] = Field(default=None, description="Search for PR by text")
    state: str = Field(default="open", description="PR state filter: open, closed, all")
    model: Optional[str] = Field(default=None, description="LLM model to use")
    post_review: bool = Field(default=False, description="Post review to GitHub")
    verdict: bool = Field(default=False, description="Include APPROVE/REQUEST_CHANGES")


class ReviewComment(BaseModel):
    """A review comment."""
    file: str
    line: int
    comment: str
    severity: str  # info, suggestion, warning, error


class ReviewResponse(BaseModel):
    """PR review response."""
    pr_number: int
    pr_title: str
    summary: str
    comments: list[ReviewComment]
    verdict: Optional[str] = None  # APPROVE, REQUEST_CHANGES, COMMENT


def _run_review_sync(
    pr_number: Optional[int],
    model: Optional[str],
    sse_handler: SSEHandler,
):
    """Run PR review synchronously."""
    try:
        from ..agent.code_reviewer import CodeReviewer
        from ..agent.events import AgentEventEmitter

        class SSEBridge:
            def __init__(self, handler):
                self._handler = handler

            def handle(self, event):
                self._handler.handle(event)

        emitter = AgentEventEmitter(agent_name="Review")
        emitter.add_handler(SSEBridge(sse_handler))

        reviewer = CodeReviewer(model=model, emitter=emitter)

        sse_handler.emit(EventType.PROGRESS, {
            "step": "Fetching PR",
            "percent": 10,
        })

        result = reviewer.review(pr_number=pr_number)

        sse_handler.emit(EventType.RESPONSE, {
            "pr_number": pr_number,
            "pr_title": result.get("title", ""),
            "summary": result.get("summary", ""),
            "comments": result.get("comments", []),
            "verdict": result.get("verdict"),
        })

    except Exception as e:
        sse_handler.emit(EventType.ERROR, {"message": str(e)})
    finally:
        sse_handler.close()


@router.post("")
async def review_pr(request: ReviewRequest):
    """Generate a PR review.

    Analyzes the PR diff and generates review comments.
    """
    if not request.pr_number and not request.pr_url and not request.search:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=400,
            detail="Must provide pr_number, pr_url, or search"
        )

    sse_handler = SSEHandler(agent_name="Review")

    sse_handler.emit(EventType.SESSION_START, {
        "agent_name": "Review",
        "pr_number": request.pr_number,
    })

    async def run():
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            _executor,
            _run_review_sync,
            request.pr_number,
            request.model,
            sse_handler,
        )

    asyncio.create_task(run())

    return StreamingResponse(
        sse_handler,
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


@router.post("/create-profile")
async def create_reviewer_profile(
    top_reviewers: int = 5,
    top_contributors: int = 10,
    max_prs: int = 50,
    model: Optional[str] = None,
):
    """Create a reviewer profile by analyzing repository reviewers."""
    sse_handler = SSEHandler(agent_name="ReviewerProfile")

    async def run():
        try:
            from ..agent.reviewer_profile import ReviewerProfileBuilder

            builder = ReviewerProfileBuilder(model=model)
            result = builder.build(
                top_reviewers=top_reviewers,
                top_contributors=top_contributors,
                max_prs=max_prs,
            )

            sse_handler.emit(EventType.RESPONSE, result)
        except Exception as e:
            sse_handler.emit(EventType.ERROR, {"message": str(e)})
        finally:
            sse_handler.close()

    asyncio.create_task(run())

    return StreamingResponse(
        sse_handler,
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )
