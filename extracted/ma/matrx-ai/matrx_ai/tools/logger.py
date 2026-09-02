from __future__ import annotations

import json
import traceback
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any
from uuid import uuid4

from matrx_connect.reservations import try_get_tracker
from matrx_utils import vcprint

from matrx_ai.db.ownership_fields import stamp_row_owner
from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolResult
from matrx_ai.utils.cache import TTLCache

# (conversation_id:call_id) -> cx_tool_call.id, populated the instant a tool call
# is logged (log_started) and read by backfill_message_id. This makes the
# message_id link ORDER-INDEPENDENT: when the result message persists, the row's
# INSERT may still be DEFERRED on the coordinator Session (invisible to a DB
# read) — but we already KNOW the row id, so the link is queued by pk and
# coalesces with the INSERT, instead of a DB read that finds nothing and silently
# drops the link. That dropped link is the EARLY race that left
# cx_tool_call.message_id NULL → the rebuild duplicate-tool_result 400. The TTL
# comfortably exceeds the 600s in-turn tool watchdog SLA so even a long-running
# tool's link survives; a genuine miss (cross-process / expired) falls back to
# the DB read, which by then succeeds because the INSERT has long committed.
_TOOL_CALL_ROW_BY_CALL_ID: TTLCache[str] = TTLCache(ttl_seconds=1800, max_size=5000)


def _call_row_key(conversation_id: Any, call_id: Any) -> str | None:
    if not conversation_id or not call_id:
        return None
    return f"{conversation_id}:{call_id}"


# Lazy access to persistence.queue_helpers — breaks the matrx_ai.persistence
# ↔ matrx_ai.tools circular import (tools/handle_tool_calls is imported via
# matrx_ai.tools, which queue_helpers transitively reaches via cx_managers).


def _cxm():
    # Lazy: resolving cxm constructs host-injected ORM managers, which requires
    # matrx_ai.configure(). Import at call time so `import matrx_ai.tools`
    # works in an unconfigured environment (config errors at CALL time, never
    # import time).
    from matrx_ai.db import cxm

    return cxm


def _get_coordinator():
    from matrx_ai.persistence.queue_helpers import get_coordinator as _gc

    return _gc()


def _queue_tool_call_create(**kwargs):
    from matrx_ai.persistence.queue_helpers import queue_tool_call_create as _q

    return _q(**kwargs)


def _queue_tool_call_update(row_id, **kwargs):
    from matrx_ai.persistence.queue_helpers import queue_tool_call_update as _q

    return _q(row_id, **kwargs)


def _should_persist_tool_call() -> bool:
    from matrx_ai.context.app_context import try_get_app_context

    ctx = try_get_app_context()
    if ctx is None:
        return True
    return bool(getattr(ctx, "store", True))


async def _capture_tool_ledger_failure(
    exc: BaseException, operation: str, **payload: Any
) -> None:
    from matrx_connect.streaming.error_capture import capture_error

    await capture_error(
        exc,
        kind="tool_ledger_persistence_failed",
        route="tool_execution_logger",
        error_type=type(exc).__name__,
        error_text=f"{operation}: {exc}",
        payload={"operation": operation, **payload},
    )


async def _ensure_tool_call_parents(
    *, conversation_id: str | None, user_request_id: str | None, user_id: str
) -> None:
    """Guarantee both FK parents for a ``tool_call`` exist.

    Direct tool paths (``/tools/test``, realtime bridge, local harnesses) can
    reach ``ToolExecutor`` without the chat/agent boundary's conversation and
    user-request gates. Without this backstop the INSERT lands in
    ``system_write_failure`` as a permanent FK orphan. Idempotent; safe to call
    on every tool-call write.
    """
    if not user_id:
        return
    from matrx_ai.db.conversation_gate import (
        ensure_conversation_exists,
        ensure_user_request_exists,
    )

    if conversation_id:
        await ensure_conversation_exists(conversation_id=conversation_id, user_id=user_id)
    if user_request_id:
        await ensure_user_request_exists(request_id=user_request_id, user_id=user_id)
    coord = _get_coordinator()
    if (
        coord is not None
        and user_request_id
        and getattr(coord, "_request_id", None) != user_request_id
    ):
        # Coordinator was minted under a prior request_id (e.g. independent
        # child fork, or a late override). Keep failure-row correlation in
        # lockstep with the stamped FK so replay/admin views aren't lying.
        coord.set_correlation(request_id=user_request_id)


_AS_CALLED_SUPPORTED: bool | None = None


def _cx_tool_call_supports_as_called() -> bool:
    """Cached check: does the host-injected ``CxToolCall`` ORM model expose
    a ``tool_name_as_called`` field? Migration 0022 added the column to the
    DB; the ORM model regenerates with migration 0023. Until then, callers
    fall back to stashing the value in ``metadata.tool_name_as_called`` so
    the trace isn't lost.
    """
    global _AS_CALLED_SUPPORTED
    if _AS_CALLED_SUPPORTED is not None:
        return _AS_CALLED_SUPPORTED
    try:
        from matrx_ai.db._registry import get_model

        model = get_model("ToolCall")
        # matrx-orm stores fields on the class. Check by attribute presence
        # — both Pydantic-style and field-list-style implementations expose
        # the attribute on the class itself.
        _AS_CALLED_SUPPORTED = hasattr(model, "tool_name_as_called")
    except Exception:
        _AS_CALLED_SUPPORTED = False
    return _AS_CALLED_SUPPORTED


class ToolExecutionLogger:
    """Two-phase logging to the ``cx_tool_call`` table via the ORM manager.

    Phase 1 — ``log_started()``:
        INSERT a row with ``status='running'`` the moment execution begins.

    Phase 2 — ``log_completed()`` / ``log_error()``:
        UPDATE that row with output, cost, events, and final status.

    Both phases are fire-and-forget — failures are logged but never block
    the execution pipeline.
    """

    def row_id_for_call(self, ctx: ToolContext) -> str:
        try:
            key = _call_row_key(ctx.conversation_id, ctx.call_id)
        except Exception:
            return ""
        return _TOOL_CALL_ROW_BY_CALL_ID.get(key or "") or ""

    # ------------------------------------------------------------------
    # Phase 1: log_started (INSERT)
    # ------------------------------------------------------------------

    async def log_started(
        self,
        ctx: ToolContext,
        tool_def: ToolDefinition,
        arguments: dict[str, Any],
        *,
        exposed_name: str | None = None,
        authorization_metadata: dict[str, Any] | None = None,
    ) -> str:
        row_id = str(uuid4())
        now = datetime.now(UTC)

        safe_arguments = self._truncate_arguments(arguments)

        # ``tool_name`` always stores the canonical identity (the registry
        # row's name). ``tool_name_as_called`` (added by migration 0022)
        # stores the exposed name the model actually used — bundle alias
        # if a bundle was loaded, canonical otherwise. Defaults to
        # canonical when ``exposed_name`` isn't passed (call sites that
        # haven't been updated yet).
        as_called = exposed_name if exposed_name is not None else tool_def.name

        data: dict[str, Any] = {
            "id": row_id,
            "conversation_id": ctx.conversation_id,
            "user_request_id": ctx.request_id if ctx.request_id else None,
            "tool_name": tool_def.name,
            "tool_type": tool_def.tool_type.value,
            "call_id": ctx.call_id,
            "status": "running",
            # The DB column defaults success=true; a row that is only just
            # STARTING has not succeeded. Stamp it false at INSERT so a row stuck
            # at 'running' (e.g. a lost completion write) never masquerades as a
            # success. The completion path (log_completed) flips it to true.
            "success": False,
            "is_error": False,
            "arguments": safe_arguments,
            "iteration": ctx.iteration,
            "cost_usd": Decimal("0"),
            "started_at": now.isoformat(),
            "completed_at": now.isoformat(),
            "created_at": now.isoformat(),
            "metadata": {},
        }
        if authorization_metadata:
            data["metadata"] = {
                **data["metadata"],
                "execution_authorization": authorization_metadata,
            }
        if ctx.message_id:
            data["message_id"] = ctx.message_id

        stamp_row_owner(data, ctx.user_id)

        if not _should_persist_tool_call():
            return ""

        # Register call_id -> row_id the instant the row is born so a later
        # backfill_message_id resolves the pk from memory (no DB read) even while
        # this INSERT is still deferred — the EARLY-arrival fix.
        _row_key = _call_row_key(ctx.conversation_id, ctx.call_id)
        if _row_key:
            _TOOL_CALL_ROW_BY_CALL_ID.set(_row_key, row_id)

        # ``tool_name_as_called`` was added by migration 0022 but the ORM
        # model regen lands with 0023. Set it conditionally — when the
        # generated CxToolCall model exposes it as a field we'll use it;
        # until then, log it under metadata so the trace isn't lost.
        if _cx_tool_call_supports_as_called():
            data["tool_name_as_called"] = as_called
        elif as_called != tool_def.name:
            data["metadata"] = {**data["metadata"], "tool_name_as_called": as_called}

        # Provenance: record where the call originated when the caller stamped a
        # ``tool_origin`` on the request AppContext (e.g. the realtime voice
        # bridge sets "realtime_bridge"). Generic — any entry point can mark its
        # origin and it lands in the existing cx_tool_call.metadata column, so a
        # bridge-originated call is identifiable but otherwise a normal tool call.
        try:
            from matrx_ai.context.app_context import try_get_app_context

            _origin_ctx = try_get_app_context()
            _origin = (_origin_ctx.metadata or {}).get("tool_origin") if _origin_ctx else None
            if _origin:
                data["metadata"] = {**data["metadata"], "tool_origin": _origin}
        except Exception:
            pass

        # Client host: delegate the INSERT to the ConversationStore (matrx-local
        # SQLite) — no cxm, no coordinator. 0.1.26 ConversationHandler semantics:
        # return the row_id on success, "" on failure, never raise.
        from matrx_ai.client_host import get_conversation_store

        store = get_conversation_store()
        if store is not None:
            try:
                await store.log_tool_call_start(row_id, data)
                return row_id
            except Exception as exc:
                vcprint(
                    f"ConversationStore.log_tool_call_start failed: {exc}\n"
                    f"{traceback.format_exc()}",
                    "[ToolLogger] client-host INSERT failed",
                    color="red",
                )
                return ""

        try:
            await _ensure_tool_call_parents(
                conversation_id=ctx.conversation_id,
                user_request_id=data.get("user_request_id"),
                user_id=ctx.user_id,
            )
            # Route through the WriteCoordinator: queue the INSERT (fire-and-
            # forget; lands at end-of-stream flush) and announce the row to
            # the client via the reservation tracker. The cx_tool_call lifecycle
            # is now: queue INSERT → log_completed queues UPDATE → coalescer
            # merges into a single INSERT with terminal status. The 0-stuck-
            # row guarantee for this table that we had via shield+finally is
            # preserved structurally — the lane finalizer ALWAYS flushes.
            if _get_coordinator() is not None:
                _queue_tool_call_create(**data)
            else:
                # Boot-time / out-of-request: this table is Coordinator-owned.
                # A bare Session has transaction mechanics but no ownership
                # authority, so it emits CoordinatorWriteViolation even when
                # the write lands. Give the complete one-shot its canonical
                # owner and synchronously prove durability on scope exit.
                from matrx_ai.persistence import standalone_coordinator

                async with standalone_coordinator(
                    reason="tool_ledger_insert_started",
                    request_id=ctx.request_id or None,
                    user_id=ctx.user_id or None,
                    conversation_id=ctx.conversation_id or None,
                ):
                    _queue_tool_call_create(**data)

            try:
                from matrx_ai.context.app_context import try_get_app_context

                app_ctx = try_get_app_context()
                tracker = try_get_tracker()
                if tracker and app_ctx and app_ctx.emitter:
                    await tracker.reserve(
                        emitter=app_ctx.emitter,
                        db_project="matrx",
                        table="tool_call",
                        parent_refs={
                            "conversation_id": ctx.conversation_id,
                            "call_id": ctx.call_id,
                            "user_request_id": ctx.request_id or "",
                        },
                        metadata={
                            "tool_name": tool_def.name,
                            "call_id": ctx.call_id,
                            "iteration": ctx.iteration,
                        },
                        record_id=row_id,
                    )
            except Exception as exc:
                await _capture_tool_ledger_failure(
                    exc,
                    "emit_tool_reservation",
                    tool_name=tool_def.name,
                    call_id=ctx.call_id,
                    row_id=row_id,
                )

            return row_id
        except Exception as exc:
            vcprint(
                f"Failed to INSERT cx_tool_call (started): {exc}\n{traceback.format_exc()}",
                "[ToolLogger] INSERT cx_tool_call failed",
                color="red",
            )
            await _capture_tool_ledger_failure(
                exc,
                "insert_started",
                tool_name=tool_def.name,
                call_id=ctx.call_id,
                conversation_id=ctx.conversation_id,
                row_id=row_id,
            )
            return ""

    # ------------------------------------------------------------------
    # Synchronous metadata preparation (must run before create_task)
    # ------------------------------------------------------------------

    def prepare_metadata(self, result: ToolResult) -> None:
        """Compute output_chars and output_preview synchronously and stamp them
        onto *result* in-place.

        This MUST be called before ``asyncio.create_task(log_completed(...))``
        so that the values are available on the in-memory ToolResult object
        for the persistence layer to read — without a DB round-trip.

        ``log_completed`` checks whether the fields are already populated and
        skips recomputation when they are.
        """
        # Tool adapters may return terminal/binary-derived text containing NUL.
        # Normalize it at the producer boundary so the in-memory ToolResult that
        # feeds provider messages and request snapshots is PostgreSQL-safe.  The
        # Coordinator sanitizer remains an independent persistence backstop.
        from matrx_ai.persistence.postgres_text import sanitize_postgres_text

        sanitized_output = sanitize_postgres_text(result.output, path="tool_result.output")
        if sanitized_output.replacements:
            result.output = sanitized_output.value

        sanitized_preview = sanitize_postgres_text(
            result.output_preview,
            path="tool_result.output_preview",
        )
        if sanitized_preview.replacements:
            result.output_preview = sanitized_preview.value

        if result.output_chars:
            return  # already prepared (e.g. tool set them manually)

        _, output_type, output_chars = self._serialize_output(result.output)
        result.output_chars = output_chars

        if result.output_preview is None:
            result.output_preview = self._synthesize_preview(
                result.output, output_type, output_chars
            )

    # ------------------------------------------------------------------
    # Phase 0: log_rejected (single terminal INSERT)
    #
    # For calls rejected BEFORE dispatch — not_allowed / not_found /
    # invalid_arguments / no_viable_executor / guardrail-pre. These paths
    # never reach log_started(), so without this they leave NO cx_tool_call
    # row at all: the failure is invisible in the tools table and the
    # cx_message tool_result pointer block has nothing to join to. This
    # records the FULL attempt (input + error) in one terminal INSERT so the
    # invariant "every tool call — success or failure — is fully recorded"
    # holds structurally for the entire pre-dispatch surface.
    # ------------------------------------------------------------------

    async def log_rejected(
        self,
        ctx: ToolContext,
        *,
        tool_name: str,
        arguments: dict[str, Any],
        result: ToolResult,
        tool_type: str = "local",
        canonical_name: str | None = None,
    ) -> str:
        row_id = str(uuid4())
        now = datetime.now(UTC)
        canonical = canonical_name or tool_name
        err = result.error

        started = datetime.fromtimestamp(result.started_at, tz=UTC) if result.started_at else now
        completed = (
            datetime.fromtimestamp(result.completed_at, tz=UTC) if result.completed_at else now
        )
        duration_ms = result.duration_ms or int(
            max(0.0, completed.timestamp() - started.timestamp()) * 1000
        )

        data: dict[str, Any] = {
            "id": row_id,
            "conversation_id": ctx.conversation_id,
            "user_request_id": ctx.request_id if ctx.request_id else None,
            "tool_name": canonical,
            "tool_type": tool_type,
            "call_id": ctx.call_id,
            "status": "error",
            "arguments": self._truncate_arguments(arguments or {}),
            "success": False,
            "is_error": True,
            "error_type": err.error_type if err else "rejected",
            "error_message": (err.message if err else "Tool call rejected before dispatch."),
            "output": None,
            "output_type": "text",
            "output_chars": 0,
            "duration_ms": duration_ms,
            "iteration": ctx.iteration,
            "cost_usd": Decimal("0"),
            "started_at": started.isoformat(),
            "completed_at": completed.isoformat(),
            "created_at": now.isoformat(),
            "metadata": {},
        }
        if ctx.message_id:
            data["message_id"] = ctx.message_id

        stamp_row_owner(data, ctx.user_id)

        if not _should_persist_tool_call():
            return ""

        # Preserve the exposed-name trace the same way log_started does.
        if canonical != tool_name:
            if _cx_tool_call_supports_as_called():
                data["tool_name_as_called"] = tool_name
            else:
                data["metadata"] = {"tool_name_as_called": tool_name}

        # Client host: a rejected call is a single TERMINAL insert — route it
        # through the store's log_tool_call_start (the data carries
        # status='error' + the rejection details).
        from matrx_ai.client_host import get_conversation_store

        store = get_conversation_store()
        if store is not None:
            try:
                await store.log_tool_call_start(row_id, data)
                return row_id
            except Exception as exc:
                vcprint(
                    f"ConversationStore.log_tool_call_start (rejected) failed: {exc}\n"
                    f"{traceback.format_exc()}",
                    "[ToolLogger] client-host INSERT (rejected) failed",
                    color="red",
                )
                return ""

        try:
            await _ensure_tool_call_parents(
                conversation_id=ctx.conversation_id,
                user_request_id=data.get("user_request_id"),
                user_id=ctx.user_id,
            )
            if _get_coordinator() is not None:
                _queue_tool_call_create(**data)
            else:
                from matrx_ai.persistence import standalone_coordinator

                async with standalone_coordinator(
                    reason="tool_ledger_insert_rejected",
                    request_id=ctx.request_id or None,
                    user_id=ctx.user_id or None,
                    conversation_id=ctx.conversation_id or None,
                ):
                    _queue_tool_call_create(**data)
            return row_id
        except Exception as exc:
            vcprint(
                f"Failed to INSERT cx_tool_call (rejected): {exc}\n{traceback.format_exc()}",
                "[ToolLogger] INSERT cx_tool_call (rejected) failed",
                color="red",
            )
            await _capture_tool_ledger_failure(
                exc,
                "insert_rejected",
                tool_name=canonical,
                call_id=ctx.call_id,
                conversation_id=ctx.conversation_id,
                row_id=row_id,
            )
            return ""

    # ------------------------------------------------------------------
    # Phase 2a: log_completed (UPDATE)
    # ------------------------------------------------------------------

    async def log_completed(
        self,
        row_id: str,
        result: ToolResult,
        execution_events: list[dict[str, Any]] | None = None,
        *,
        coordinator: Any = None,
    ) -> None:
        output_str, output_type, output_chars = self._serialize_output(result.output)

        # Use whatever is already on result (prepare_metadata sets this synchronously
        # in the executor before create_task fires); fall back to recompute here for
        # any call path that skipped prepare_metadata.
        output_preview = result.output_preview
        if output_preview is None:
            output_preview = self._synthesize_preview(result.output, output_type, output_chars)

        # Keep in-memory object consistent.
        result.output_chars = output_chars
        result.output_preview = output_preview

        input_tokens, output_tokens, cost_usd = self._aggregate_usage(result)
        total_tokens = input_tokens + output_tokens

        update_data: dict[str, Any] = {
            "status": "completed",
            "success": True,
            "is_error": False,
            "output": output_str,
            "output_type": output_type,
            "output_chars": output_chars,
            "output_preview": output_preview,
            "duration_ms": result.duration_ms,
            "completed_at": datetime.fromtimestamp(result.completed_at, tz=UTC).isoformat()
            if result.completed_at
            else datetime.now(UTC).isoformat(),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "cost_usd": cost_usd,
            "retry_count": result.retry_count,
            "execution_events": execution_events or [],
            "persist_key": result.persist_key if result.should_persist_output else None,
        }

        # Value-store linkage (Pattern 2 grooming): stamp the groom handle when
        # the result's content lives in / was served from the value store.
        # model_stub_at is NOT stamped here — auto_stub is applied at
        # CONSUMPTION time (the orchestrator's turn-directive drain, after the
        # next provider response), never at completion: a rebuild in the
        # completion→send window (delegation suspend + resume) would otherwise
        # stub content the model never saw.
        if result.value_ref_key:
            update_data["value_ref_key"] = result.value_ref_key

        await self._update_row(row_id, update_data, coordinator=coordinator)

    # ------------------------------------------------------------------
    # Phase 2b: log_error (UPDATE)
    # ------------------------------------------------------------------

    async def log_error(
        self,
        row_id: str,
        result: ToolResult,
        execution_events: list[dict[str, Any]] | None = None,
        *,
        coordinator: Any = None,
    ) -> None:
        # Ensure output_chars / output_preview are consistent on error results too
        # (prepare_metadata should already have run in executor.py, but guard here).
        if not result.output_chars and result.output is not None:
            _, output_type, output_chars = self._serialize_output(result.output)
            result.output_chars = output_chars
            if result.output_preview is None:
                result.output_preview = self._synthesize_preview(
                    result.output, output_type, output_chars
                )

        input_tokens, output_tokens, cost_usd = self._aggregate_usage(result)
        total_tokens = input_tokens + output_tokens

        update_data: dict[str, Any] = {
            "status": "error",
            "success": False,
            "is_error": True,
            "error_type": result.error.error_type if result.error else "unknown",
            "error_message": result.error.message if result.error else "Unknown error",
            "duration_ms": result.duration_ms,
            "completed_at": datetime.fromtimestamp(result.completed_at, tz=UTC).isoformat()
            if result.completed_at
            else datetime.now(UTC).isoformat(),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "cost_usd": cost_usd,
            "retry_count": result.retry_count,
            "execution_events": execution_events or [],
        }

        await self._update_row(row_id, update_data, coordinator=coordinator)

    # ------------------------------------------------------------------
    # Phase 1b: log_delegated (UPDATE) — transition 'running' → 'delegated'.
    # Called when the tool is handed off to the client for execution. After
    # this lands, the row is the durable source of truth for "awaiting client
    # POST" and survives SSE disconnects / server restarts.
    # ------------------------------------------------------------------

    async def log_delegated(
        self,
        row_id: str,
        *,
        expires_at: datetime,
        allow_desktop_target: bool = True,
    ) -> None:
        update_data: dict[str, Any] = {
            "status": "delegated",
            "is_client_delegated": True,
            "expires_at": expires_at.isoformat(),
        }
        # Pin this suspend to its runtime-spine execution (the WAITING_INPUT root the
        # resume must re-attach to). Without it, a conversation with TWO concurrent
        # suspended turns resumes against the NEWEST root — mis-attributing the other
        # turn's continuation (cost/status the cx_user_request → spine cutover can't
        # tolerate). Best-effort: NULL when the turn runs untracked (v1) or the
        # detached spine open hasn't landed yet — the resume then falls back to
        # newest-root.
        execution_id = self._runtime_execution_id()
        if execution_id:
            update_data["runtime_execution_id"] = str(execution_id)
        # Desktop-instance targeting applies ONLY to tools the matrx-local
        # desktop executes. Stamping it on browser-executed delegated tools
        # (war_room_*, widget_*, ui-first) makes the browser's own
        # /tool_results POST fail the submission-binding check (the FE sends
        # no instance_id) → 404 not_found → wedged turn, while the desktop
        # claims calls it can't execute.
        if allow_desktop_target:
            target_instance_id = self._desktop_target_instance_id()
            if target_instance_id:
                update_data["target_instance_id"] = target_instance_id
        await self._update_row(row_id, update_data)

    @staticmethod
    def _runtime_execution_id() -> str | None:
        from matrx_ai.context.app_context import try_get_app_context

        ctx = try_get_app_context()
        if ctx is None:
            return None
        try:
            metadata = ctx.metadata
            if not isinstance(metadata, dict):
                return None
            # The ROOT key, never the nesting key: "runtime_execution_id" is the
            # current nesting parent and is legitimately RE-STAMPED mid-turn (a
            # workflow launched from chat points it at the workflow execution so
            # agent nodes nest under it) — pinning that here would give the resume
            # an id it can never match. "runtime_root_execution_id" is stamped once
            # per request by the conversation open/resume and never overwritten.
            return metadata.get("runtime_root_execution_id")
        except Exception:  # noqa: BLE001 — tracking id is best-effort, never break the ledger
            return None

    @staticmethod
    def _desktop_target_instance_id() -> str | None:
        from matrx_ai.context.app_context import try_get_app_context

        ctx = try_get_app_context()
        if ctx is None:
            return None
        try:
            metadata = ctx.metadata
            if not isinstance(metadata, dict):
                return None
            direct = metadata.get("desktop_target_instance_id")
            if isinstance(direct, str) and direct.strip():
                return direct.strip()
            canonical = metadata.get("client_capabilities_payloads")
            if isinstance(canonical, dict):
                payload = canonical.get("desktop-native")
                if isinstance(payload, dict):
                    for key in ("target_instance_id", "selected_target_instance_id", "instance_id"):
                        raw = payload.get(key)
                        if isinstance(raw, str) and raw.strip():
                            return raw.strip()
        except Exception:  # noqa: BLE001 — targeting is best-effort; NULL preserves legacy routing
            return None
        return None

    # ------------------------------------------------------------------
    # Phase 2c: log_abandoned (UPDATE) — row was left in 'running' because the
    # caller (SSE task, client-delegated wait) was cancelled or the server
    # process died before the normal completion path ran.
    # ------------------------------------------------------------------

    async def log_abandoned(
        self,
        row_id: str,
        *,
        reason: str = "client_disconnected",
        error_message: str | None = None,
        execution_events: list[dict[str, Any]] | None = None,
        coordinator: Any = None,
    ) -> None:
        now = datetime.now(UTC).isoformat()
        update_data: dict[str, Any] = {
            "status": "error",
            "success": False,
            "is_error": True,
            "error_type": reason,
            "error_message": error_message
            or "Tool call was abandoned before a result was recorded.",
            "completed_at": now,
            "execution_events": execution_events or [],
        }
        await self._update_row(row_id, update_data, coordinator=coordinator)

    async def abandon_stale_running_rows(
        self,
        *,
        older_than_seconds: float,
        limit: int = 500,
    ) -> int:
        """Find cx_tool_call rows still in 'running' older than the cutoff and
        mark them as 'error' with error_type='abandoned'.

        Intended to be called from a periodic background sweep so orphan rows
        from crashed processes / dropped SSE connections do not accumulate.

        Returns the number of rows updated.
        """
        # Client stores own their local lifecycle, and an unconfigured package
        # has no server cx_ backend to sweep. This direct-call guard is the
        # backstop behind ToolLifecycleManager's scheduler-level readiness gate.
        from matrx_ai.db.cx_managers import server_maintenance_available

        if not server_maintenance_available():
            return 0

        from datetime import timedelta

        cutoff = datetime.now(UTC) - timedelta(seconds=older_than_seconds)
        try:
            stale = await _cxm().tool_call.filter_items(
                status="running",
                is_client_delegated=False,
                started_at__lt=cutoff,
            )
        except Exception as exc:
            # Diagnostic ORM exceptions (DatabaseConnectError etc.) carry their
            # full readable banner in __str__ — printing traceback.format_exc()
            # on top embeds the banner a second time. Only attach a traceback
            # for unclassified errors. The sweep is a background cleanup that
            # will retry in 5 minutes; one short line is plenty.
            if getattr(exc, "is_diagnostic", False):
                vcprint(
                    f"Failed to query stale cx_tool_call rows (sweep will retry): {exc}",
                    "[ToolLogger] abandon_stale_running_rows query failed",
                    color="red",
                )
            else:
                vcprint(
                    f"Failed to query stale cx_tool_call rows: {exc}\n{traceback.format_exc()}",
                    "[ToolLogger] abandon_stale_running_rows query failed",
                    color="red",
                )
            await _capture_tool_ledger_failure(
                exc, "query_stale_rows", older_than_seconds=older_than_seconds
            )
            return 0

        if not stale:
            return 0

        updated = 0
        for item in stale[:limit]:
            try:
                row_id = str(item.id)
                await self.log_abandoned(
                    row_id,
                    reason="abandoned",
                    error_message=(
                        "Tool call left in 'running' state longer than "
                        f"{older_than_seconds:.0f}s with no completion — "
                        "marked abandoned by sweep."
                    ),
                )
                updated += 1
            except Exception as exc:
                # Same diagnostic-vs-unknown split as above. The per-row update
                # path is in a loop, so noise here multiplies fast on a network
                # blip — keep the diagnostic branch one line.
                if getattr(exc, "is_diagnostic", False):
                    vcprint(
                        f"Failed to mark cx_tool_call {getattr(item, 'id', '?')} abandoned: {exc}",
                        "[ToolLogger] abandon_stale_running_rows update failed",
                        color="red",
                    )
                else:
                    vcprint(
                        f"Failed to mark cx_tool_call {getattr(item, 'id', '?')} abandoned: {exc}\n{traceback.format_exc()}",
                        "[ToolLogger] abandon_stale_running_rows update failed",
                        color="red",
                    )

        if updated:
            vcprint(
                f"Marked {updated} stale cx_tool_call row(s) as abandoned "
                f"(older than {older_than_seconds:.0f}s).",
                "[ToolLogger] Stale sweep",
                color="cyan",
            )
        return updated

    async def expire_delegated_calls(
        self,
        *,
        limit: int = 500,
    ) -> int:
        """Sweep cx_tool_call rows where the client-delegated wait has run out.

        A row is expired when ``is_client_delegated=true AND status='delegated'
        AND expires_at < now()``. Each such row is flipped to
        ``status='error'``, ``error_type='client_tool_timeout'``,
        ``resolution_source='timeout_sweep'``.

        IMPORTANT — this is a far-future ABANDONMENT backstop, NOT a user answer
        deadline. ``expires_at`` defaults to now +
        ``DELEGATED_CALL_ABANDON_AFTER_SECONDS`` (30 days; per-tool override via
        ``tools.max_client_wait_seconds``) precisely so a user may take seconds,
        hours, or weeks to answer while the conversation stays cleanly resumable
        (status='delegated' / user_request 'paused'). A row only reaches this
        sweep if the conversation was genuinely abandoned. Even then a late
        genuine client answer is NOT lost: ``submit_tool_results`` SUPERSEDES a
        ``timeout_sweep`` row (re-resolves it with the real output and resumes),
        so this terminal state is a recoverable placeholder, never a dead end.

        There is a narrow race with an incoming POST /tool_results: the sweep
        may update a row that was just resolved. We re-verify status='delegated'
        immediately before the UPDATE (below) to close it; at a 30-day default
        the window is effectively nonexistent anyway.

        Returns the number of rows expired.
        """
        # Client stores own their local lifecycle, and an unconfigured package
        # has no server cx_ backend to sweep. This direct-call guard is the
        # backstop behind ToolLifecycleManager's scheduler-level readiness gate.
        from matrx_ai.db.cx_managers import server_maintenance_available

        if not server_maintenance_available():
            return 0

        now = datetime.now(UTC)
        try:
            expired_rows = await _cxm().tool_call.filter_items(
                is_client_delegated=True,
                status="delegated",
                expires_at__lt=now,
            )
        except Exception as exc:
            vcprint(
                f"Failed to query expired cx_tool_call rows: {exc}\n{traceback.format_exc()}",
                "[ToolLogger] expire_delegated_calls query failed",
                color="red",
            )
            await _capture_tool_ledger_failure(exc, "query_expired_delegated_rows")
            return 0

        if not expired_rows:
            return 0

        now_iso = now.isoformat()
        updated = 0
        for row in expired_rows[:limit]:
            row_id = str(row.id)
            try:
                # Re-verify status='delegated' before writing — guard against the
                # narrow race where POST /tool_results resolved this row between
                # our SELECT and this UPDATE (Bug 9-C fix).
                current = await _cxm().tool_call.filter_items(id=row.id, status="delegated")
                if not current:
                    continue

                await self._update_row(
                    row_id,
                    {
                        "status": "error",
                        "success": False,
                        "is_error": True,
                        "error_type": "client_tool_timeout",
                        "error_message": (
                            "Client did not respond within "
                            "max_client_wait_seconds — marked expired by sweep."
                        ),
                        "completed_at": now_iso,
                        "resolved_at": now_iso,
                        "resolution_source": "timeout_sweep",
                    },
                )
                updated += 1
            except Exception as exc:
                vcprint(
                    f"Failed to expire cx_tool_call {row_id}: {exc}",
                    "[ToolLogger] expire_delegated_calls update failed",
                    color="red",
                )

        if updated:
            vcprint(
                f"Expired {updated} delegated cx_tool_call row(s).",
                "[ToolLogger] Delegated-call expiry sweep",
                color="cyan",
            )
        return updated

    # ------------------------------------------------------------------
    # Link message_id after persistence creates the cx_message row
    # ------------------------------------------------------------------

    async def link_message(self, row_id: str, message_id: str) -> None:
        await self._update_row(row_id, {"message_id": message_id})

    # ------------------------------------------------------------------
    # Backfill message_id by call_id + conversation_id
    # ------------------------------------------------------------------

    async def backfill_message_id(
        self,
        call_id: str,
        conversation_id: str,
        message_id: str,
    ) -> None:
        # Client host: message-id backfill is a cx_message linking concern —
        # the host store owns its local storage schema and any linking (0.1.26
        # parity: no-op).
        from matrx_ai.client_host import get_conversation_store

        if get_conversation_store() is not None:
            return

        try:
            coord = _get_coordinator()

            def _link(row_id: str) -> None:
                # Queue the link by pk onto the SAME coordinator Session as the
                # cx_message write so the FK lands in one commit (and coalesces
                # with the row's still-deferred INSERT) — never an immediate DB
                # write while the parent row is deferred.
                if coord is not None:
                    coord.queue(
                        "chat.tool_call",
                        {"id": row_id, "message_id": message_id},
                        op_type="update",
                        primary_key=("id", row_id),
                    )
                else:
                    return None  # out-of-request: handled by the awaited path below

            # FAST PATH — resolve the row id from the in-process registry that
            # log_started populated. This is ORDER-INDEPENDENT: the row's INSERT
            # may still be DEFERRED (invisible to a DB read), but we already know
            # its id, so the link survives the early race that previously left
            # message_id NULL.
            cached_row_id = _TOOL_CALL_ROW_BY_CALL_ID.get(
                _call_row_key(conversation_id, call_id) or ""
            )
            if cached_row_id:
                if coord is not None:
                    _link(cached_row_id)
                else:
                    await self._durable_link_update(cached_row_id, message_id, conversation_id)
                return

            # SLOW PATH — cache miss (cross-process, or expired after a very long
            # tool whose INSERT has by now committed). Read the DB.
            matches = await _cxm().tool_call.filter_items(
                call_id=call_id,
                conversation_id=conversation_id,
            )
            if not matches:
                # Neither the in-process registry NOR the committed DB knows this
                # call_id. The row was genuinely never registered — that is now an
                # anomaly worth shouting about (the early race is handled by the
                # cache above), never a silent drop.
                vcprint(
                    f"[ToolLogger] backfill_message_id found NO cx_tool_call row "
                    f"for call_id={call_id} conversation_id={conversation_id} in "
                    f"EITHER the in-process registry or the DB — message_id link "
                    f"could not be made. This should be impossible once log_started "
                    f"has run; investigate the tool-call INSERT path.",
                    color="red",
                )
                return
            for item in matches:
                row_id = str(item.id)
                if coord is not None:
                    _link(row_id)
                    continue
                await self._durable_link_update(row_id, message_id, conversation_id)
        except Exception as exc:
            vcprint(
                f"Failed to backfill message_id for call_id={call_id}: {exc}\n{traceback.format_exc()}",
                "[ToolLogger] backfill_message_id failed",
                color="red",
            )
            await _capture_tool_ledger_failure(
                exc,
                "backfill_message_id",
                call_id=call_id,
                conversation_id=conversation_id,
                message_id=message_id,
            )

    async def _durable_link_update(
        self, row_id: str, message_id: str, conversation_id: str | None
    ) -> None:
        """Out-of-request (no-coordinator) message_id link. The immediate write
        has no fire-and-verify net, so on failure we DON'T swallow it — we
        capture a REPLAYABLE update op to system_write_failure (pk=id) so the
        auto-replay loop re-applies the link. Without this a failed link leaves
        cx_tool_call.message_id NULL and the tool result silently vanishes from
        the reconstructed message (KD-3)."""
        try:
            await _cxm().tool_call.update_item_fields(row_id, message_id=message_id)
        except Exception as exc:
            try:
                from matrx_orm.session.fallback import record_failures
                from matrx_orm.session.op import make_update

                from matrx_ai.persistence.registry import get_model

                op = make_update(
                    get_model("chat.tool_call"),
                    str(row_id),
                    {"message_id": message_id},
                )
                await record_failures([op], exc, conversation_id=conversation_id)
                vcprint(
                    f"[ToolLogger] message_id link for cx_tool_call.id={row_id} failed "
                    f"immediately — captured to system_write_failure for replay "
                    f"({type(exc).__name__}: {exc})",
                    color="yellow",
                )
            except Exception as capture_exc:
                vcprint(
                    f"[ToolLogger] message_id link for cx_tool_call.id={row_id} failed "
                    f"AND could not be captured: {type(capture_exc).__name__}: "
                    f"{capture_exc}",
                    color="red",
                )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _update_row(
        self, row_id: str, data: dict[str, Any], *, coordinator: Any = None
    ) -> None:
        if not row_id:
            return

        # Client host: delegate the UPDATE to the ConversationStore.
        from matrx_ai.client_host import get_conversation_store

        store = get_conversation_store()
        if store is not None:
            try:
                await store.log_tool_call_update(row_id, data)
            except Exception as exc:
                vcprint(
                    f"ConversationStore.log_tool_call_update failed for {row_id}: {exc}\n"
                    f"{traceback.format_exc()}",
                    "[ToolLogger] client-host UPDATE failed",
                    color="red",
                )
            return

        try:
            # Route through the WriteCoordinator when inside a request scope so
            # the UPDATE coalesces with the row's INSERT and lands in the single
            # transactional barrier flush.
            #
            # CRITICAL: the completion writes (log_completed / log_error) are
            # fired from a detached_task, which runs in a FRESH contextvars
            # Context — so the coordinator ContextVar is invisible there and
            # ``_get_coordinator()`` returns None. If we then took the direct
            # ``update_item_fields`` path, that immediate UPDATE would race the
            # row's still-deferred INSERT, match 0 rows, and be silently lost —
            # leaving the row stuck 'running' until the watchdog repainted it
            # 'error' (the systematic status='error'+success=true bug). The
            # caller therefore captures the coordinator in the LIVE request
            # context and passes it in; we prefer it over the (absent) ambient
            # one so the UPDATE is queued onto the same Session as the INSERT
            # and ordered after it. Queuing is synchronous + in-memory (no DB
            # connection), so it does NOT reintroduce the asyncpg-connection
            # race the detached_task exists to avoid.
            coord = coordinator if coordinator is not None else _get_coordinator()
            if coord is not None:
                coord.queue(
                    "chat.tool_call",
                    {"id": row_id, **data},
                    op_type="update",
                    primary_key=("id", row_id),
                )
                return
            # True out-of-request callers only (background sweepers). The tool
            # ledger is Coordinator-owned; a bare Session is not ownership.
            # Queue the update into a standalone owner so the normal commit,
            # replay, and structured-capture boundary applies.
            from matrx_ai.persistence import standalone_coordinator

            async with standalone_coordinator(reason="tool_ledger_update") as standalone:
                standalone.queue(
                    "chat.tool_call",
                    {"id": row_id, **data},
                    op_type="update",
                    primary_key=("id", row_id),
                )
        except Exception as exc:
            vcprint(
                f"Failed to UPDATE cx_tool_call {row_id}: {exc}\n{traceback.format_exc()}",
                "[ToolLogger] UPDATE cx_tool_call failed",
                color="red",
            )
            await _capture_tool_ledger_failure(
                exc,
                "update_tool_call",
                row_id=row_id,
                data_keys=sorted(data.keys()),
            )

    _MAX_ARG_STRING_CHARS = 10_000

    @staticmethod
    def _truncate_arguments(arguments: dict[str, Any]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        limit = ToolExecutionLogger._MAX_ARG_STRING_CHARS
        for key, value in arguments.items():
            if isinstance(value, str) and len(value) > limit:
                result[key] = value[:limit] + f"…[truncated {len(value):,} chars]"
            else:
                result[key] = value
        return result

    _MAX_OUTPUT_CHARS = 100_000
    # Hard cap for output_preview — keeps the cx_message pointer block tiny.
    _MAX_PREVIEW_CHARS = 500
    _MAX_PREVIEW_KEYS = 20

    @staticmethod
    def _serialize_output(output: Any) -> tuple[str | None, str, int]:
        """Serialize tool output to a string for DB storage.

        Returns (serialized_string, output_type, char_count).
        char_count reflects the *pre-truncation* length so the UI can show
        the true size even when the stored value was truncated.
        """
        if output is None:
            return None, "text", 0
        if isinstance(output, str):
            serialized, output_type = output, "text"
        elif isinstance(output, dict | list):
            serialized, output_type = json.dumps(output, default=str), "json"
        else:
            serialized, output_type = str(output), "text"

        char_count = len(serialized)

        if char_count > ToolExecutionLogger._MAX_OUTPUT_CHARS:
            truncated = serialized[: ToolExecutionLogger._MAX_OUTPUT_CHARS]
            suffix = f"\n\n[TRUNCATED — {char_count:,} chars total, showing first {ToolExecutionLogger._MAX_OUTPUT_CHARS:,}]"
            serialized = truncated + suffix

        return serialized, output_type, char_count

    @staticmethod
    def _synthesize_preview(output: Any, output_type: str, char_count: int) -> dict[str, Any]:
        """Build a lightweight preview dict when the tool doesn't supply one.

        Rules:
        - None / empty → {"chars": 0}
        - Small JSON dict (≤ _MAX_PREVIEW_KEYS keys AND ≤ _MAX_PREVIEW_CHARS when
          re-serialized): return the dict directly — it IS the preview.
        - Large JSON dict: return {"keys": [...first 20 keys...], "chars": N}
        - JSON list: return {"count": N, "chars": N}
        - Text: return {"chars": N}

        The goal is for the preview to never exceed ~500 chars of serialized JSON
        so it stays genuinely lightweight inside cx_message.content.
        """
        if output is None or char_count == 0:
            return {"chars": 0}

        max_keys = ToolExecutionLogger._MAX_PREVIEW_KEYS
        max_chars = ToolExecutionLogger._MAX_PREVIEW_CHARS

        if output_type == "json":
            if isinstance(output, dict):
                if len(output) <= max_keys:
                    candidate = {str(k): v for k, v in output.items()}
                    try:
                        if len(json.dumps(candidate, default=str)) <= max_chars:
                            return candidate
                    except Exception:
                        pass
                # Too large — return key names only
                keys = list(output.keys())[:max_keys]
                return {"keys": [str(k) for k in keys], "chars": char_count}

            if isinstance(output, list):
                return {"count": len(output), "chars": char_count}

        # text / other
        return {"chars": char_count}

    @staticmethod
    def _aggregate_usage(result: ToolResult) -> tuple[int, int, Decimal]:
        input_tokens = 0
        output_tokens = 0
        cost_usd = 0.0

        if result.usage:
            input_tokens = result.usage.get("input_tokens", 0)
            output_tokens = result.usage.get("output_tokens", 0)
            cost_usd = result.usage.get("cost_usd", 0.0)

        for child in result.child_usages:
            if isinstance(child, dict):
                input_tokens += child.get("input_tokens", 0)
                output_tokens += child.get("output_tokens", 0)
                cost_usd += child.get("cost_usd", 0.0)
            else:
                input_tokens += getattr(child, "input_tokens", 0)
                output_tokens += getattr(child, "output_tokens", 0)
                child_cost = child.calculate_cost()
                cost_usd += child_cost if child_cost is not None else 0.0

        return input_tokens, output_tokens, Decimal(str(cost_usd))
