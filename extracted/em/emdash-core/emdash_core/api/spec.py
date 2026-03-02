"""Feature specification endpoints with SSE streaming."""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from ..sse.stream import SSEHandler, EventType

router = APIRouter(prefix="/spec", tags=["specification"])

_executor = ThreadPoolExecutor(max_workers=2)


class SpecRequest(BaseModel):
    """Request to generate a feature specification."""
    feature: str = Field(..., description="Feature description")
    project_md: Optional[str] = Field(default=None, description="PROJECT.md content")
    model: Optional[str] = Field(default=None, description="LLM model to use")
    verbose: bool = Field(default=False, description="Verbose output")


class SpecResponse(BaseModel):
    """Feature specification response."""
    title: str
    content: str
    file_path: Optional[str] = None


def _run_spec_sync(
    feature: str,
    model: Optional[str],
    sse_handler: SSEHandler,
):
    """Run spec generation synchronously."""
    try:
        from ..agent.specification import SpecificationAgent
        from ..agent.events import AgentEventEmitter

        # Bridge events to SSE
        class SSEBridge:
            def __init__(self, handler):
                self._handler = handler

            def handle(self, event):
                self._handler.handle(event)

        emitter = AgentEventEmitter(agent_name="Specification")
        emitter.add_handler(SSEBridge(sse_handler))

        # Use default model if not specified
        from ..agent.providers.factory import DEFAULT_MODEL
        agent = SpecificationAgent(model=model or DEFAULT_MODEL, emitter=emitter, interactive=False)
        spec = agent.generate_spec(feature)

        sse_handler.emit(EventType.RESPONSE, {
            "title": spec.title,
            "content": spec.content,
        })

    except Exception as e:
        sse_handler.emit(EventType.ERROR, {"message": str(e)})
    finally:
        sse_handler.close()


@router.post("/generate")
async def generate_spec(request: SpecRequest):
    """Generate a feature specification with SSE streaming.

    Returns a detailed specification for implementing a feature.
    """
    sse_handler = SSEHandler(agent_name="Specification")

    sse_handler.emit(EventType.SESSION_START, {
        "agent_name": "Specification",
        "feature": request.feature,
    })

    async def run():
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            _executor,
            _run_spec_sync,
            request.feature,
            request.model,
            sse_handler,
        )

    asyncio.create_task(run())

    return StreamingResponse(
        sse_handler,
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )
