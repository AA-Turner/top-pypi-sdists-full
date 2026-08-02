"""
HTTP server for the @on_task decorator.

Starts a FastAPI server on port 59321 (configurable via XPANDER_STREAMING_PORT)
with Swagger docs at /docs and ReDoc at /redoc.

Endpoints:
  - POST /invoke  – receives a Task JSON body, executes the handler.
  - GET  /health  – returns 200 OK for readiness checks.

Supports both handler types:
  - Regular handler (returns Task): returns JSON response.
  - Streaming handler (yields TaskUpdateEvent): streams SSE lines.

Authentication is performed via the x-api-key header, validated against
the agent-controller's api_key_allowance endpoint with a 5-minute in-memory cache.
"""

from __future__ import annotations

import asyncio
import hashlib
import json as py_json
import os
import threading
import time
from datetime import datetime, timezone
from inspect import iscoroutinefunction
from typing import Any, AsyncGenerator, Callable, Dict, Optional, Tuple, Union

import httpx
from loguru import logger
from pydantic import BaseModel

from xpander_sdk.consts.api_routes import APIRoute
from xpander_sdk.core.xpander_api_client import APIClient
from xpander_sdk.models.configuration import Configuration
from xpander_sdk.models.events import TaskUpdateEventType
from xpander_sdk.models.shared import OutputFormat
from xpander_sdk.modules.tasks.models.task import AgentExecutionStatus
from xpander_sdk.modules.tasks.sub_modules.task import Task, TaskUpdateEvent

# ---------------------------------------------------------------------------
# In-memory API-key allowance cache  (TTL = 5 minutes)
# ---------------------------------------------------------------------------
_CACHE_TTL_SECONDS = 300  # 5 minutes

# key: (api_key_sha256, agent_id) -> (allowed: bool, expires_at: float)
_allowance_cache: Dict[Tuple[str, str], Tuple[bool, float]] = {}


def _cache_key(api_key: str, agent_id: str) -> Tuple[str, str]:
    """Return a hashable cache key without storing the raw API key."""
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()
    return (key_hash, agent_id)


async def _check_api_key_allowed(
    api_key: str,
    agent_id: str,
    configuration: Configuration,
) -> bool:
    """
    Verify *api_key* is allowed to invoke *agent_id*.

    Checks the in-memory cache first; on miss / expiry, calls the
    agent-controller ``api_key_allowance`` endpoint and caches the result.
    """
    ck = _cache_key(api_key, agent_id)
    now = time.monotonic()

    # Cache hit
    cached = _allowance_cache.get(ck)
    if cached is not None:
        allowed, expires_at = cached
        if now < expires_at:
            return allowed

    # Cache miss / expired – call agent-controller
    try:
        client = APIClient(configuration=configuration)
        response = await client.make_request(
            path=str(APIRoute.GetAPIKeyAllowance),
            method="POST",
            payload={"api_key": api_key},
        )

        # response is a dict: {"api_key": "...", "agent_ids": [...]}
        allowed_agents = (
            response.get("agent_ids", []) if isinstance(response, dict) else []
        )
        allowed = agent_id in allowed_agents
    except Exception as exc:
        logger.warning(f"API key allowance check failed: {exc}")
        # On error, deny by default
        allowed = False

    _allowance_cache[ck] = (allowed, now + _CACHE_TTL_SECONDS)
    return allowed


# ---------------------------------------------------------------------------
# Task lifecycle helpers
# ---------------------------------------------------------------------------


async def _finalize_task(task: Task, error: Optional[str] = None) -> None:
    """Apply the same lifecycle side-effects as Events.handle_task_execution_request."""
    # Direct /invoke has no plan-retry loop, so this is its only finalize-bookkeeping hook.
    try:
        from xpander_sdk.core.context_optimizer.finalize_mode import (
            finalize_task_from_run_end,
        )

        await finalize_task_from_run_end(task)
    except Exception as exc:
        logger.warning(f"[finalize-mode] run-end finalize failed: {exc}")

    task_used_tokens = task.tokens
    task_used_tools = task.used_tools

    if error:
        task.result = error
        task.status = AgentExecutionStatus.Error
    elif task.status == AgentExecutionStatus.Executing:
        task.status = AgentExecutionStatus.Completed

    # structured output → stringify
    try:
        if task.output_format == OutputFormat.Json:
            if isinstance(task.result, BaseModel):
                task.result = task.result.model_dump_json()
            if isinstance(task.result, dict) or isinstance(task.result, list):
                task.result = py_json.dumps(task.result)
    except Exception:
        pass

    await task.asave()
    task.tokens = task_used_tokens
    task.used_tools = task_used_tools

    if task.tokens:
        try:
            await task.areport_metrics()
        except Exception as exc:
            logger.warning(f"Failed to report metrics for task {task.id}: {exc}")


# ---------------------------------------------------------------------------
# FastAPI server
# ---------------------------------------------------------------------------


class InvokeRequestBody(BaseModel):
    """Request body for the /invoke endpoint."""

    id: str
    agent_id: str
    organization_id: str
    input: Dict
    status: Optional[str] = "pending"
    created_at: str
    agent_version: Optional[str] = None
    output_format: Optional[str] = None
    output_schema: Optional[Dict] = None
    events_streaming: Optional[bool] = False
    additional_context: Optional[str] = None
    instructions_override: Optional[str] = None
    deep_planning: Optional[Dict] = None
    execution_attempts: Optional[int] = 1
    mcp_servers: Optional[list] = []
    source: Optional[str] = None

    model_config = {"extra": "allow"}


def _build_app(
    handler: Callable,
    configuration: Configuration,
    agent_id: str,
    is_streaming_handler: bool,
):
    """Build and return the FastAPI application."""
    from fastapi import FastAPI, Header, HTTPException
    from fastapi.responses import JSONResponse, StreamingResponse

    app = FastAPI(
        title="xpander.ai Agent Worker",
        description="Local HTTP server for invoking xpander.ai agent tasks.",
        version="1.0.0",
    )

    async def _authenticate(api_key: Optional[str]) -> None:
        """Validate the x-api-key header."""
        if not api_key:
            raise HTTPException(status_code=401, detail="Missing x-api-key header")
        allowed = await _check_api_key_allowed(api_key, agent_id, configuration)
        if not allowed:
            raise HTTPException(
                status_code=403, detail="API key not allowed for this agent"
            )

    @app.get("/health", summary="Health check", tags=["System"])
    async def health_handler():
        """Returns 200 OK if the server is running."""
        return {"status": "ok"}

    @app.post(
        "/invoke",
        summary="Invoke agent task",
        description=(
            "Execute the agent handler with the given Task payload. "
            "For streaming handlers, returns an SSE stream of TaskUpdateEvent lines. "
            "For regular handlers, returns the completed Task as JSON."
        ),
        tags=["Agent"],
    )
    async def invoke_handler(
        body: InvokeRequestBody,
        x_api_key: Optional[str] = Header(None, alias="x-api-key"),
    ):
        """Invoke the registered agent handler with a Task payload."""
        await _authenticate(x_api_key)

        # --- parse Task ---
        try:
            task = Task(**body.model_dump(), configuration=configuration)
        except Exception as exc:
            raise HTTPException(status_code=400, detail=f"Invalid Task payload: {exc}")

        logger.info(f"Handling task {task.id} via /invoke (streaming)")

        if is_streaming_handler:
            return await _handle_streaming(handler, task)
        else:
            return await _handle_regular(handler, task)

    return app


async def _handle_streaming(
    handler: Callable,
    task: Task,
):
    """Handle an async-generator handler – stream SSE lines."""
    from fastapi.responses import StreamingResponse

    def _merge_task_payload(payload: Any) -> None:
        if isinstance(payload, Task):
            updated_task = payload
        elif isinstance(payload, dict):
            updated_task = Task(**{**payload, "configuration": task.configuration})
        elif payload is not None:
            task.result = str(payload)
            return
        else:
            return

        for field, value in updated_task.__dict__.items():
            if field == "configuration":
                continue
            setattr(task, field, value)

    async def _event_generator():
        error = None
        try:
            await task.aset_status(status=AgentExecutionStatus.Executing)
            async for event in handler(task=task):
                if not isinstance(event, TaskUpdateEvent):
                    raise TypeError(
                        f"Streaming handler must yield TaskUpdateEvent instances, "
                        f"got {type(event).__name__}"
                    )
                if event.type == TaskUpdateEventType.TaskFinished:
                    _merge_task_payload(event.data)
                    continue
                yield f"data: {event.model_dump_json()}\n\n"
        except Exception as exc:
            error = str(exc)
            logger.exception(f"Streaming handler error: {exc}")
        finally:
            await _finalize_task(task, error=error)
            finished_event = TaskUpdateEvent(
                type=TaskUpdateEventType.TaskFinished,
                task_id=task.id,
                organization_id=task.organization_id,
                time=datetime.now(timezone.utc),
                data=task.model_dump_safe(exclude={"configuration"}),
            )
            yield f"data: {finished_event.model_dump_json()}\n\n"
            logger.info(f"Finished handling task {task.id} via /invoke (streaming)")

    return StreamingResponse(
        _event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


async def _handle_regular(
    handler: Callable,
    task: Task,
):
    """Handle a regular (non-generator) handler – return JSON."""
    from fastapi.responses import JSONResponse

    error = None
    try:
        await task.aset_status(status=AgentExecutionStatus.Executing)
        if iscoroutinefunction(handler):
            task = await handler(task=task)
        else:
            task = handler(task=task)
    except Exception as exc:
        error = str(exc)
        logger.exception(f"Handler error: {exc}")
    finally:
        await _finalize_task(task, error=error)
        logger.info(f"Finished handling task {task.id} via /invoke (streaming)")

    if error:
        return JSONResponse({"error": error}, status_code=500)

    return JSONResponse(
        task.model_dump_safe(exclude={"configuration"}),
        status_code=200,
    )


def run_streaming_server_in_background(
    handler: Callable,
    configuration: Optional[Configuration] = None,
    is_streaming_handler: bool = False,
    agent_id: Optional[str] = None,
) -> None:
    """
    Start the HTTP server in a daemon thread so it runs alongside the SSE listener.

    Args:
        handler: The wrapped handler function.
        configuration: SDK configuration (credentials / base URL).
        is_streaming_handler: True if the handler is an async generator.
        agent_id: The agent ID this worker serves.
    """
    try:
        import uvicorn  # noqa: F401
        import fastapi  # noqa: F401
    except ImportError:
        raise ImportError(
            "fastapi and uvicorn are required for the /invoke HTTP server. "
            "Install them with:  pip install fastapi uvicorn"
        )

    configuration = configuration or Configuration()
    agent_id = agent_id or configuration.agent_id or os.getenv("XPANDER_AGENT_ID")

    if not agent_id:
        raise ValueError(
            "XPANDER_AGENT_ID is required for the /invoke server. "
            "Set it via environment variable or Configuration.agent_id."
        )

    port = int(os.getenv("XPANDER_STREAMING_PORT", "59321"))

    def _run_server():
        import uvicorn

        app = _build_app(handler, configuration, agent_id, is_streaming_handler)
        logger.info(
            f"Starting /invoke HTTP server on port {port} (docs at http://localhost:{port}/docs)"
        )
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="warning")

    thread = threading.Thread(
        target=_run_server, daemon=True, name="xpander-invoke-server"
    )
    thread.start()
