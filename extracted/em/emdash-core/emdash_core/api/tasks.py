"""Task generation endpoints with SSE streaming."""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from ..sse.stream import SSEHandler, EventType

router = APIRouter(prefix="/tasks", tags=["tasks"])

_executor = ThreadPoolExecutor(max_workers=2)


class TasksRequest(BaseModel):
    """Request to generate implementation tasks."""
    spec_name: Optional[str] = Field(default=None, description="Specification name")
    spec_content: Optional[str] = Field(default=None, description="Specification content")
    project_md: Optional[str] = Field(default=None, description="PROJECT.md content")
    model: Optional[str] = Field(default=None, description="LLM model to use")


class Task(BaseModel):
    """A single implementation task."""
    id: int
    title: str
    description: str
    files: list[str] = Field(default_factory=list)
    dependencies: list[int] = Field(default_factory=list)


class TasksResponse(BaseModel):
    """Task generation response."""
    tasks: list[Task]
    total: int


def _run_tasks_sync(
    spec_content: Optional[str],
    model: Optional[str],
    sse_handler: SSEHandler,
):
    """Run task generation synchronously."""
    import sys
    from pathlib import Path

    try:
        # Note: ImplementationAgent is actually ImplementationPlanAgent in the module
        # The generate_tasks method needs to be added or this endpoint refactored
        from ..agent.events import AgentEventEmitter

        class SSEBridge:
            def __init__(self, handler):
                self._handler = handler

            def handle(self, event):
                self._handler.handle(event)

        emitter = AgentEventEmitter(agent_name="Tasks")
        emitter.add_handler(SSEBridge(sse_handler))

        agent = ImplementationAgent(model=model, emitter=emitter)
        result = agent.generate_tasks(spec_content or "")

        tasks = result.get("tasks", [])
        sse_handler.emit(EventType.RESPONSE, {
            "tasks": tasks,
            "total": len(tasks),
        })

    except Exception as e:
        sse_handler.emit(EventType.ERROR, {"message": str(e)})
    finally:
        sse_handler.close()


@router.post("/generate")
async def generate_tasks(request: TasksRequest):
    """Generate implementation tasks from a specification.

    Returns a list of tasks with dependencies for implementing the spec.
    """
    sse_handler = SSEHandler(agent_name="Tasks")

    sse_handler.emit(EventType.SESSION_START, {
        "agent_name": "Tasks",
        "spec_name": request.spec_name,
    })

    async def run():
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            _executor,
            _run_tasks_sync,
            request.spec_content,
            request.model,
            sse_handler,
        )

    asyncio.create_task(run())

    return StreamingResponse(
        sse_handler,
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )
