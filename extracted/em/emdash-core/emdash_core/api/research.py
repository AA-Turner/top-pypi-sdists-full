"""Research endpoints with SSE streaming."""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from ..sse.stream import SSEHandler, EventType

router = APIRouter(prefix="/research", tags=["research"])

_executor = ThreadPoolExecutor(max_workers=2)


class ResearchRequest(BaseModel):
    """Request for deep research."""
    goal: str = Field(..., description="Research goal")
    max_iterations: int = Field(default=5, description="Max research iterations")
    budget: int = Field(default=50000, description="Token budget")
    model: Optional[str] = Field(default=None, description="LLM model for main tasks")
    researcher_model: Optional[str] = Field(default=None, description="LLM for research")


class ResearchResponse(BaseModel):
    """Research response."""
    goal: str
    findings: str
    sources: list[str]
    iterations: int


def _run_research_sync(
    goal: str,
    max_iterations: int,
    model: Optional[str],
    researcher_model: Optional[str],
    sse_handler: SSEHandler,
):
    """Run research synchronously."""
    import sys
    from pathlib import Path

    from ..config import get_config
    config = get_config()
    repo_root = Path(config.repo_root) if config.repo_root else Path.cwd()

    try:
        from ..agent.research.agent import ResearchAgent
        from ..agent.events import AgentEventEmitter

        class SSEBridge:
            def __init__(self, handler):
                self._handler = handler

            def handle(self, event):
                self._handler.handle(event)

        emitter = AgentEventEmitter(agent_name="Research")
        emitter.add_handler(SSEBridge(sse_handler))

        agent = ResearchAgent(
            planner_model=model,
            researcher_model=researcher_model or model,
            critic_model=model,
            synthesizer_model=model,
            emitter=emitter,
        )

        result = agent.research(goal, max_iterations=max_iterations)

        sse_handler.emit(EventType.RESPONSE, {
            "goal": goal,
            "findings": result.get("synthesis", ""),
            "sources": result.get("sources", []),
            "iterations": result.get("iterations", 0),
        })

    except Exception as e:
        sse_handler.emit(EventType.ERROR, {"message": str(e)})
    finally:
        sse_handler.close()


@router.post("")
async def research(request: ResearchRequest):
    """Deep research with multi-LLM loops and critic evaluation.

    Uses multiple specialized agents:
    - Planner: Creates research plan
    - Researcher: Gathers information
    - Critic: Evaluates findings
    - Synthesizer: Produces final report
    """
    sse_handler = SSEHandler(agent_name="Research")

    sse_handler.emit(EventType.SESSION_START, {
        "agent_name": "Research",
        "goal": request.goal,
    })

    async def run():
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            _executor,
            _run_research_sync,
            request.goal,
            request.max_iterations,
            request.model,
            request.researcher_model,
            sse_handler,
        )

    asyncio.create_task(run())

    return StreamingResponse(
        sse_handler,
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )
