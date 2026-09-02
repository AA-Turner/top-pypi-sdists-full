"""Wrapper that lets the OM Observer/Reflector call the unified AI client.

Provides the ``llm_call_fn`` the OM system needs: ``(model, messages,
temperature, max_tokens) -> str``. Bypasses ``execute_until_complete`` so
no ``cx_request`` / ``cx_user_request`` side effects are written — memory
LLM cost lives in ``cx_observational_memory_event`` only.

Fires a background task to write the event row (tokens, cost, duration)
and emits a structured ``OMEvent`` through the request emitter so the UI
can see each Observer/Reflector call.
"""
from __future__ import annotations

import asyncio
import logging
import time
import uuid
from datetime import UTC, datetime
from typing import Any, Optional

from matrx_utils import vcprint

logger = logging.getLogger(__name__)

_BG_TASKS: set[asyncio.Task[Any]] = set()


def _spawn_bg(coro: Any) -> None:
    task = asyncio.create_task(coro)
    _BG_TASKS.add(task)
    task.add_done_callback(_BG_TASKS.discard)


def _spawn_bg_shielded(coro: Any) -> None:
    """Like _spawn_bg, but the inner write survives caller cancellation.

    The OM cost record (cx_observational_memory_event) must land even when
    the request is cancelled mid-call — otherwise the tokens we just spent
    on the Observer/Reflector LLM vanish with no trace. asyncio.shield keeps
    the write running through the cancellation unwind.
    """
    async def _runner() -> None:
        try:
            await asyncio.shield(coro)
        except asyncio.CancelledError:
            pass
        except Exception:
            logger.exception("OM background write failed")

    task = asyncio.create_task(_runner())
    _BG_TASKS.add(task)
    task.add_done_callback(_BG_TASKS.discard)


def _extract_response_text(response: Any) -> str:
    """Pull assistant text out of a ``UnifiedResponse``.

    The Observer/Reflector LLM returns a single assistant message with text
    content. Concatenate all TextContent.text values defensively in case the
    provider returns multiple segments.
    """
    messages = getattr(response, "messages", None) or []
    for msg in reversed(messages):
        role = getattr(msg, "role", None)
        if role and role != "assistant":
            continue
        content = getattr(msg, "content", None) or []
        parts: list[str] = []
        for item in content:
            text_val = getattr(item, "text", None)
            if isinstance(text_val, str) and text_val:
                parts.append(text_val)
            elif isinstance(item, dict) and isinstance(item.get("text"), str):
                parts.append(item["text"])
        if parts:
            return "".join(parts)
    return ""


def _split_system_from_messages(messages: list[dict[str, Any]]) -> tuple[Optional[str], list[dict[str, Any]]]:
    """UnifiedConfig forbids system-role entries in ``messages``. Pull the
    first system message out and return it separately."""
    system_text: Optional[str] = None
    remaining: list[dict[str, Any]] = []
    for msg in messages:
        role = msg.get("role")
        if role == "system" and system_text is None:
            content = msg.get("content")
            if isinstance(content, str):
                system_text = content
            elif isinstance(content, list):
                system_text = "".join(
                    part.get("text", "") if isinstance(part, dict) else str(part)
                    for part in content
                )
            else:
                system_text = str(content or "")
        else:
            remaining.append(msg)
    return system_text, remaining


class MemoryLLMAdapter:
    """Adapter exposing ``.call(model, messages, temperature, max_tokens)``.

    Construct once per turn with a closed-over ``ctx`` and ``conversation_id``
    so every event row carries the right user/request/conversation.

    The ``event_type_hint`` lets the caller mark whether a given invocation
    is an Observer or Reflector call. Defaults to ``observer`` because that's
    the far more common path; the ReflectorRunner wraps its calls through
    ``call_as`` to override.
    """

    def __init__(self, ctx: Any, conversation_id: str, memory_record_id: Optional[str] = None) -> None:
        self.ctx = ctx
        self.conversation_id = conversation_id
        self.memory_record_id = memory_record_id
        self._default_event_type = "observer"

    def bind_record(self, memory_record_id: str) -> None:
        """Set the memory_record_id after the record is materialized — the
        adapter is built before we know the DB id, so this lets the factory
        wire the id back in once it's known."""
        self.memory_record_id = memory_record_id

    async def __call__(self, model: str, messages: list[dict[str, Any]], temperature: float, max_tokens: int) -> str:
        return await self._invoke(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            event_type=self._default_event_type,
        )

    async def call_as(
        self,
        event_type: str,
        model: str,
        messages: list[dict[str, Any]],
        temperature: float,
        max_tokens: int,
    ) -> str:
        return await self._invoke(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            event_type=event_type,
        )

    async def _invoke(
        self,
        model: str,
        messages: list[dict[str, Any]],
        temperature: float,
        max_tokens: int,
        event_type: str,
    ) -> str:
        # Deferred imports avoid pulling the full provider stack at module load
        # time (important because the memory package must remain usable even
        # when matrx_ai hasn't been configured yet, e.g. in unit tests).
        from matrx_ai.config import UnifiedConfig
        from matrx_ai.orchestrator.requests import AIMatrixRequest
        from matrx_ai.providers.unified_client import UnifiedAIClient

        system_text, body_messages = _split_system_from_messages(messages)

        config = UnifiedConfig(
            model=model,
            messages=body_messages,
            system_instruction=system_text,
            stream=False,
            temperature=temperature,
            max_output_tokens=max_tokens,
            store=False,
        )
        request = AIMatrixRequest(
            conversation_id=self.conversation_id,
            config=config,
            debug=False,
            request_id=str(uuid.uuid4()),
        )

        client = _get_client()
        started_at = datetime.now(UTC)
        t0 = time.time()
        error_text: Optional[str] = None
        text_out = ""
        usage = None
        cost: float = 0.0
        input_tokens = 0
        output_tokens = 0

        try:
            response = await client.execute(request)
            text_out = _extract_response_text(response)
            usage = getattr(response, "usage", None)
            if usage is not None:
                input_tokens = int(getattr(usage, "input_tokens", 0) or 0) + int(
                    getattr(usage, "cached_input_tokens", 0) or 0
                )
                output_tokens = int(getattr(usage, "output_tokens", 0) or 0)
                try:
                    calculated = usage.calculate_cost()
                    cost = float(calculated or 0.0)
                except Exception as exc:
                    logger.debug("OM cost calculation failed: %s", exc)
        except asyncio.CancelledError:
            # Client disconnect / shutdown during the paid OM call. CancelledError
            # does NOT inherit from Exception, so without this branch it would
            # skip the error bookkeeping below and the spend would be recorded
            # as a phantom success (or not at all). Mark it, let the finally
            # write the cost row (shielded), then re-raise.
            error_text = "cancelled mid-stream (client disconnect or shutdown)"
            logger.warning("[OM:llm_adapter] LLM call cancelled mid-stream")
            raise
        except Exception as exc:
            error_text = f"{type(exc).__name__}: {exc}"
            logger.warning("[OM:llm_adapter] LLM call failed: %s", error_text)
        finally:
            duration_ms = int((time.time() - t0) * 1000)
            completed_at = datetime.now(UTC)
            # Shielded: the cost record must survive a cancellation unwind.
            _spawn_bg_shielded(
                _write_event(
                    ctx=self.ctx,
                    conversation_id=self.conversation_id,
                    memory_record_id=self.memory_record_id,
                    event_type=event_type if error_text is None else "error",
                    model=model,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    cost=cost,
                    duration_ms=duration_ms,
                    triggered_at=started_at,
                    completed_at=completed_at,
                    success=error_text is None,
                    error=error_text,
                    trigger_reason=event_type,
                )
            )
            _spawn_bg(
                _emit_event(
                    ctx=self.ctx,
                    conversation_id=self.conversation_id,
                    success=error_text is None,
                    event_type=event_type,
                    model=model,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    cost=cost,
                    duration_ms=duration_ms,
                    error=error_text,
                )
            )

        if error_text is not None:
            # Propagate so OM's internal error handling converts this to a log
            # entry without blowing up the main conversation turn.
            raise RuntimeError(error_text)
        return text_out


_CLIENT_SINGLETON: Any | None = None


def _get_client() -> Any:
    """Lazy single-instance client. The full UnifiedAIClient wires up every
    provider adapter on construction so we only want one per process."""
    global _CLIENT_SINGLETON
    if _CLIENT_SINGLETON is None:
        from matrx_ai.providers.unified_client import UnifiedAIClient

        _CLIENT_SINGLETON = UnifiedAIClient()
    return _CLIENT_SINGLETON


async def _write_event(
    ctx: Any,
    conversation_id: str,
    memory_record_id: Optional[str],
    event_type: str,
    model: Optional[str],
    input_tokens: int,
    output_tokens: int,
    cost: float,
    duration_ms: int,
    triggered_at: datetime,
    completed_at: datetime,
    success: bool,
    error: Optional[str],
    trigger_reason: Optional[str],
) -> None:
    """Persist one OM cost/event row through a WriteCoordinator.

    Spawned via ``_spawn_bg_shielded`` after the LLM call — the request
    coordinator is often already gone, so this opens a short-lived
    ``standalone_coordinator`` and queues the insert. Never opens a bare
    ``Session()`` (coordinator-owned table).
    """
    try:
        from matrx_ai.persistence import queue_om_event_create, standalone_coordinator

        event_id = str(uuid.uuid4())
        fields = {
            "memory_record_id": memory_record_id,
            "conversation_id": conversation_id,
            "created_by": str(getattr(ctx, "user_id", "") or ""),
            "user_request_id": str(getattr(ctx, "request_id", "") or "") or None,
            "event_type": event_type,
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost": cost,
            "duration_ms": duration_ms,
            "triggered_at": triggered_at,
            "completed_at": completed_at,
            "success": success,
            "error": error,
            "trigger_reason": trigger_reason,
            "metadata": {},
            "created_at": datetime.now(UTC),
        }
        async with standalone_coordinator(
            reason="om_event_write",
            request_id=str(getattr(ctx, "request_id", "") or "") or None,
            user_id=str(getattr(ctx, "user_id", "") or "") or None,
            conversation_id=conversation_id or None,
        ):
            queue_om_event_create(id=event_id, **fields)
    except Exception as exc:
        logger.warning("OM event write failed: %s", exc)


async def _emit_event(
    ctx: Any,
    conversation_id: str,
    success: bool,
    event_type: str,
    model: Optional[str] = None,
    input_tokens: int = 0,
    output_tokens: int = 0,
    cost: float = 0.0,
    duration_ms: Optional[int] = None,
    error: Optional[str] = None,
) -> None:
    """Emit a typed ``DataPayload`` through the request emitter.

    Maps the internal event_type to the matching
    ``matrx_connect.context.data_types`` subclass so the frontend's
    generated ``TypedDataPayload`` union sees these as first-class events
    (not ``UntypedDataPayload``). Silently drops when the emitter is closed
    (background tasks after SSE end) — the DB event row is authoritative.
    """
    try:
        from matrx_connect.context.data_types import (
            MemoryErrorData,
            MemoryObserverCompletedData,
            MemoryReflectorCompletedData,
        )

        emitter = getattr(ctx, "emitter", None)
        if emitter is None:
            return

        if not success:
            payload = MemoryErrorData(
                conversation_id=conversation_id,
                phase=event_type,
                error=error or "",
                model=model,
            )
        elif event_type in ("reflector", "reflector_buffer"):
            payload = MemoryReflectorCompletedData(
                conversation_id=conversation_id,
                model=model,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost=cost,
                duration_ms=duration_ms,
            )
        else:
            payload = MemoryObserverCompletedData(
                conversation_id=conversation_id,
                model=model,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost=cost,
                duration_ms=duration_ms,
            )
        await emitter.send_data(payload.model_dump())
    except Exception as exc:
        logger.debug("OM event emit failed (non-fatal): %s", exc)
