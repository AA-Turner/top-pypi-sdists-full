"""Stage tracking for durable stages and orchestrator tasks.

Reports lifecycle events (started / completed / failed) to the Chronos backend,
which persists them and handles Slack notifications server-side.

This replaces the client-side Slack notification approach in ``slack.py``.
"""

from __future__ import annotations

import asyncio
import contextvars
import json
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

import httpx

from plato.chronos.api.stages import report_stage as _report_stage_api
from plato.chronos.models import ReportStageRequest, StageType, Status5

logger = logging.getLogger(__name__)


@dataclass
class StageTrackingContext:
    """Holds stage tracking configuration for the current session."""

    base_url: str
    api_key: str | None
    session_id: str


# When set, @durable and ParallelAgentOrchestrator report stage events.
_stage_tracking_ctx: contextvars.ContextVar[StageTrackingContext | None] = contextvars.ContextVar(
    "_stage_tracking_ctx", default=None
)

# Tracks the public_id of the currently executing durable stage.
# Read by ParallelAgentOrchestrator._run_task to set parent context.
# Inherited by asyncio.create_task, so orchestrator tasks see their parent.
_current_stage_public_id: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "_current_stage_public_id", default=None
)


def enable_stage_tracking(
    session_id: str,
    base_url: str | None = None,
    api_key: str | None = None,
) -> contextvars.Token[StageTrackingContext | None]:
    """Enable stage tracking for the current context.

    Args:
        session_id: Chronos session public ID.
        base_url: Chronos base URL. Defaults to CHRONOS_URL env var.
        api_key: Chronos API key. Defaults to PLATO_API_KEY env var.
    """
    if api_key is None:
        api_key = os.environ.get("PLATO_API_KEY")
    if base_url is None:
        base_url = os.environ.get("CHRONOS_URL", "https://chronos.plato.so")
    ctx = StageTrackingContext(
        base_url=base_url,
        api_key=api_key,
        session_id=session_id,
    )
    return _stage_tracking_ctx.set(ctx)


def disable_stage_tracking(
    token: contextvars.Token[StageTrackingContext | None],
) -> None:
    """Disable stage tracking by resetting the context var."""
    _stage_tracking_ctx.reset(token)


async def report_stage(
    *,
    stage_name: str,
    stage_type: Literal["durable", "orchestrator_task"],
    status: Literal["started", "completed", "failed"],
    started_at: datetime,
    output_type: str | None = None,
    completed_at: datetime | None = None,
    elapsed_seconds: float | None = None,
    base_path: str | None = None,
    args_snapshot: dict[str, Any] | None = None,
    parent_stage_public_id: str | None = None,
    error_message: str | None = None,
    metadata: dict[str, Any] | None = None,
    trace_id: str | None = None,
    span_id: str | None = None,
) -> str | None:
    """Report a stage lifecycle event to Chronos. Returns the stage public_id.

    No-op if stage tracking is not enabled. All errors are caught and logged —
    stage tracking never blocks the pipeline.
    """
    ctx = _stage_tracking_ctx.get()
    if ctx is None:
        return None

    try:
        body = ReportStageRequest(
            session_public_id=ctx.session_id,
            stage_name=stage_name,
            stage_type=StageType(stage_type),
            status=Status5(status),
            started_at=started_at,
            output_type=output_type,
            completed_at=completed_at,
            elapsed_seconds=elapsed_seconds,
            base_path=base_path,
            args_snapshot=args_snapshot,
            parent_stage_public_id=parent_stage_public_id,
            error_message=error_message[:2000] if error_message else None,
            metadata=metadata,
            trace_id=trace_id,
            span_id=span_id,
        )

        async with httpx.AsyncClient(
            base_url=ctx.base_url,
            timeout=5.0,
        ) as client:
            resp = await _report_stage_api.asyncio(client, body=body, x_api_key=ctx.api_key)
            return resp.public_id
    except Exception:
        logger.warning("Failed to report stage %s (%s)", stage_name, status, exc_info=True)
        return None


def report_stage_sync(
    *,
    stage_name: str,
    stage_type: Literal["durable", "orchestrator_task"],
    status: Literal["started", "completed", "failed"],
    started_at: datetime,
    output_type: str | None = None,
    completed_at: datetime | None = None,
    elapsed_seconds: float | None = None,
    base_path: str | None = None,
    args_snapshot: dict[str, Any] | None = None,
    parent_stage_public_id: str | None = None,
    error_message: str | None = None,
    metadata: dict[str, Any] | None = None,
    trace_id: str | None = None,
    span_id: str | None = None,
) -> None:
    """Sync version of report_stage. Fire-and-forget."""
    coro = report_stage(
        stage_name=stage_name,
        stage_type=stage_type,
        status=status,
        started_at=started_at,
        output_type=output_type,
        completed_at=completed_at,
        elapsed_seconds=elapsed_seconds,
        base_path=base_path,
        args_snapshot=args_snapshot,
        parent_stage_public_id=parent_stage_public_id,
        error_message=error_message,
        metadata=metadata,
        trace_id=trace_id,
        span_id=span_id,
    )
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(coro)
    except RuntimeError:
        try:
            asyncio.run(asyncio.wait_for(coro, timeout=5.0))
        except Exception:
            logger.warning("Failed to report stage %s (%s) sync", stage_name, status, exc_info=True)


def serialize_args(args: dict[str, Any]) -> dict[str, Any]:
    """Serialize function args to a JSON-safe dict.

    Converts Path objects to strings, drops non-serializable values.
    """
    safe: dict[str, Any] = {}
    for key, value in args.items():
        try:
            if isinstance(value, Path):
                safe[key] = str(value)
            elif isinstance(value, (str, int, float, bool, type(None))):
                safe[key] = value
            elif isinstance(value, (list, tuple, dict)):
                # Round-trip through JSON to ensure the value is fully serializable
                safe[key] = json.loads(json.dumps(value))
            else:
                # Complex objects — store type name only
                safe[key] = f"<{type(value).__name__}>"
        except (TypeError, ValueError, OverflowError):
            safe[key] = f"<{type(value).__name__}>"
    return safe
