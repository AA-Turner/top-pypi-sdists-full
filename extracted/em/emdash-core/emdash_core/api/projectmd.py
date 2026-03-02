"""PROJECT.md generation API endpoint with SSE streaming."""

import asyncio
import traceback
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from ..sse.stream import SSEHandler, EventType
from ..utils.logger import log

router = APIRouter(prefix="/projectmd", tags=["projectmd"])

# Thread pool for running blocking agent code
_executor = ThreadPoolExecutor(max_workers=2)


class ProjectMDRequest(BaseModel):
    """Request for PROJECT.md generation."""
    output: str = "PROJECT.md"
    save: bool = True
    model: Optional[str] = None


class ProjectMDResponse(BaseModel):
    """Response from PROJECT.md generation."""
    success: bool
    content: Optional[str] = None
    output_path: Optional[str] = None
    error: Optional[str] = None


def _generate_projectmd_sync(
    output: str,
    save: bool,
    model: str,
    sse_handler: SSEHandler,
):
    """Run PROJECT.md generation synchronously (in thread pool).

    This function runs in a background thread and emits events
    to the SSE handler for streaming to the client.
    """
    try:
        # Import discovery agent
        from ..agent.discovery import ProjectDiscoveryAgent

        # Emit start
        sse_handler.emit(EventType.SESSION_START, {
            "agent_name": "Project Discovery",
            "model": model,
            "output": output,
        })

        # Create and run discovery agent
        agent = ProjectDiscoveryAgent(
            model=model,
            verbose=True,
        )

        # Generate PROJECT.md content
        content = agent.run()

        # Save if requested
        output_path = None
        if save and content:
            from pathlib import Path
            output_path = Path(output)
            output_path.write_text(content)
            sse_handler.emit(EventType.THINKING, {
                "message": f"Saved to {output_path}",
            })

        # Emit final response
        sse_handler.emit(EventType.RESPONSE, {
            "content": content,
            "saved": save,
            "output_path": str(output_path) if output_path else None,
        })

        return content

    except ImportError as e:
        # Discovery agent not available, use simpler approach
        sse_handler.emit(EventType.WARNING, {
            "message": f"Discovery agent not available: {e}. Using basic generation.",
        })

        try:
            from ..agent.runner import AgentRunner
            from ..agent.events import AgentEventEmitter

            # Create emitter that forwards to SSE handler
            class SSEBridgeHandler:
                def __init__(self, sse_handler: SSEHandler):
                    self._sse = sse_handler

                def handle(self, event):
                    self._sse.handle(event)

            emitter = AgentEventEmitter(agent_name="Project Discovery")
            emitter.add_handler(SSEBridgeHandler(sse_handler))

            runner = AgentRunner(
                model=model,
                verbose=True,
                max_iterations=100,
                emitter=emitter,
            )

            # Use a simple prompt for PROJECT.md generation
            prompt = """Explore this codebase and generate a PROJECT.md document that describes:
1. What this project is and does
2. The main architecture and components
3. Key files and their purposes
4. How to get started

Use the available tools to explore the codebase structure and key files.
After exploration, write a comprehensive PROJECT.md document.
IMPORTANT: After exploring, output the complete PROJECT.md content as your final response."""

            content = runner.run(prompt)

            if save and content:
                from pathlib import Path
                output_path = Path(output)
                output_path.write_text(content)

            return content

        except Exception as inner_e:
            tb = traceback.format_exc()
            log.error(f"ProjectMD inner error: {inner_e}\n{tb}")
            sse_handler.emit(EventType.ERROR, {
                "message": f"{inner_e}\n\nTraceback:\n{tb}",
            })
            raise

    except Exception as e:
        tb = traceback.format_exc()
        log.error(f"ProjectMD error: {e}\n{tb}")
        sse_handler.emit(EventType.ERROR, {
            "message": f"{e}\n\nTraceback:\n{tb}",
        })
        raise


async def _generate_projectmd_async(
    request: ProjectMDRequest,
    sse_handler: SSEHandler,
):
    """Generate PROJECT.md and stream events."""
    from ..config import get_config

    config = get_config()
    model = request.model or config.default_model

    loop = asyncio.get_event_loop()

    try:
        await loop.run_in_executor(
            _executor,
            _generate_projectmd_sync,
            request.output,
            request.save,
            model,
            sse_handler,
        )

        sse_handler.emit(EventType.SESSION_END, {
            "success": True,
        })

    except Exception as e:
        sse_handler.emit(EventType.SESSION_END, {
            "success": False,
            "error": str(e),
        })

    finally:
        sse_handler.close()


@router.post("/generate")
async def generate_projectmd(request: ProjectMDRequest):
    """Generate PROJECT.md by exploring the codebase.

    Uses AI to analyze the code graph and generate a comprehensive
    project document that describes architecture, patterns, and
    key components.

    The response is a Server-Sent Events stream containing:
    - session_start: Initial session info
    - tool_start/tool_result: Exploration progress
    - thinking: Agent reasoning
    - response: Final PROJECT.md content
    - session_end: Completion status

    Example:
        curl -N -X POST http://localhost:8765/api/projectmd/generate \\
            -H "Content-Type: application/json" \\
            -d '{"output": "PROJECT.md", "save": true}'
    """
    sse_handler = SSEHandler(agent_name="Project Discovery")

    asyncio.create_task(_generate_projectmd_async(request, sse_handler))

    return StreamingResponse(
        sse_handler,
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
