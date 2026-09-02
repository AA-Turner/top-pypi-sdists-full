"""
CX_ Persistence Service — Writes CompletedRequest data to the database.

This is the single point of truth for persisting AI execution results.
It lives in the core AI layer (not in API routes) so that ANY execution path
(unified chat, agent, internal calls, agent-to-agent) triggers persistence.

The cx_conversation row is guaranteed to exist before this module runs —
it is created by ``ensure_conversation_exists()`` at the start of
``execute_until_complete()`` in ``ai.executor``.  This module only
**updates** the conversation; it never creates one.

Usage:
    from matrx_ai.db import persist_completed_request

    completed = await execute_until_complete(...)
    await persist_completed_request(completed)
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any
from uuid import UUID

# persistence.queue_helpers is lazy-imported by helpers below to break the
# matrx_ai.persistence ↔ matrx_ai.db circular import.
from matrx_connect.lane import get_current_lane
from matrx_connect.reservations import try_get_tracker
from matrx_utils import vcprint

# IMPORT SAFETY — ai_model_manager and cxm both resolve host-injected DB
# models/bases when their impl modules load, which raises DBNotConfiguredError
# in a CLIENT host. Both are resolved lazily at CALL time via the helpers
# below (config errors at CALL time, never import time).
from matrx_ai.db.message_parts import validate_message_content
from matrx_ai.db.message_positions import APPEND_MESSAGE_POSITION

# Import-order safety: ``matrx_ai.orchestrator.__init__`` imports executor,
# which imports THIS module — so importing anything under matrx_ai.orchestrator
# at module scope here is circular when persistence is the entry module (e.g. a
# client host importing matrx_ai.db.persistence directly). Keep these
# TYPE_CHECKING-only and resolve the runtime symbols lazily.
if TYPE_CHECKING:
    from matrx_ai.orchestrator.execution_state import ExecutionState
    from matrx_ai.orchestrator.requests import CompletedRequest


def _cx_error_text(error: Any) -> str:
    """Serialize structured execution errors for cx_user_request.error TEXT.

    ``CompletedRequest`` intentionally keeps a structured error for the runtime
    spine, but the retiring cx column is TEXT.  Passing the dict straight into
    matrx-orm masks the real provider/validation failure with a secondary
    ``Input should be a valid string`` persistence error.
    """

    if isinstance(error, str):
        return error
    return json.dumps(error, sort_keys=True, separators=(",", ":"), default=str)


def try_get_execution_state():
    from matrx_ai.orchestrator.execution_state import (
        try_get_execution_state as _tges,
    )

    return _tges()


# Reserved message-metadata keys that have earned typed cx_message columns.
# apply_context_objects stamps model_context/tools_on_call onto the user
# message's metadata; the handoff exit stamps agent_id / is_visible_to_user on
# its synthetic rows. The persist path LIFTS them out into their columns so the
# per-turn call record is first-class and cx_message.metadata stays lean.
# ⚠️ These are GLOBALLY RESERVED metadata keys — every message writer's metadata
# passes through this lift. Keep in sync with the CxMessage model columns and
# docs/cx_chat/CX_MESSAGE_CALL_RECORD.md.
PROMOTED_MESSAGE_COLUMNS: tuple[str, ...] = (
    "model_context",
    "tools_on_call",
    "agent_id",
    "is_visible_to_user",
    # Interrupt tail-hiding stamps this at the executor's cancel boundary so a
    # freshly-INSERTed abandoned-tail message lands already hidden from the
    # model (previously only post-hoc UPDATEs — compaction, grooming — set it).
    "is_visible_to_model",
)


def _valid_promoted(key: str, value: Any) -> bool:
    """Typed-column guards — a malformed promoted value must SCREAM and stay in
    metadata rather than abort the whole message INSERT (agent_id is an FK)."""
    if key == "agent_id":
        try:
            from uuid import UUID

            UUID(str(value))
            return True
        except (ValueError, TypeError):
            return False
    if key in ("is_visible_to_user", "is_visible_to_model"):
        return isinstance(value, bool)
    return True


def lift_promoted_message_columns(
    metadata: dict[str, Any] | None,
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    """Split the reserved per-turn call-record keys out of a message's metadata
    into their typed cx_message columns.

    Returns ``(clean_metadata_or_None, promoted_fields)``. Copies before mutating
    so the caller's original metadata dict is never touched. Used by BOTH write
    sites for the user message — the end-of-turn persist loop here and the
    mid-loop delegate-suspend flush in ``executor.py`` — so a delegated-tool turn
    records the call too.
    """
    if not metadata:
        return metadata, {}
    clean = dict(metadata)
    promoted: dict[str, Any] = {}
    for key in PROMOTED_MESSAGE_COLUMNS:
        if key in clean:
            value = clean[key]
            if not _valid_promoted(key, value):
                vcprint(
                    f"[CX PERSISTENCE] promoted metadata key {key!r} carries a "
                    f"malformed value ({value!r}) — left in metadata, column not "
                    "stamped (a bad agent_id FK would abort the INSERT)",
                    color="red",
                )
                continue
            promoted[key] = clean.pop(key)
    return (clean or None), promoted


def _safe_content_repr(value: Any, *, max_len: int = 600) -> str:
    """Compact, binary-safe repr for log lines.

    Raw provider payloads can embed large binary blobs (e.g. Google's
    ``thought_signature`` bytes), which previously produced ~50-page log
    entries. Collapse bytes to a short ``<N bytes>`` marker and truncate the
    final string so a validation failure never floods the logs.
    """

    def _scrub(v: Any) -> Any:
        if isinstance(v, bytes | bytearray):
            return f"<{len(v)} bytes>"
        if isinstance(v, dict):
            return {k: _scrub(val) for k, val in v.items()}
        if isinstance(v, list | tuple):
            return [_scrub(item) for item in v]
        return v

    text = repr(_scrub(value))
    if len(text) > max_len:
        return f"{text[:max_len]}… (truncated, {len(text)} chars)"
    return text


# Test-override seams: several suites monkeypatch these module attributes
# (``persistence_mod.cxm`` / ``persistence_mod.ai_model_manager_instance``).
# They default to None and the lazy accessors below prefer them when set —
# the REAL objects are resolved at call time (never import time) because both
# construct host-injected ORM managers that require matrx_ai.configure().
cxm: Any | None = None
ai_model_manager_instance: Any | None = None


def _cxm():
    if cxm is not None:
        return cxm
    from matrx_ai.db.cx_managers import cxm as _real

    return _real


def _model_manager():
    if ai_model_manager_instance is not None:
        return ai_model_manager_instance
    from matrx_ai.db.ai_models.ai_model_manager import (
        ai_model_manager_instance as _real,
    )

    return _real


def _get_coordinator():
    from matrx_ai.persistence.queue_helpers import get_coordinator as _gc

    return _gc()


def _queue_conversation_update(conv_id, **kwargs):
    from matrx_ai.persistence.queue_helpers import queue_conversation_update as _q

    return _q(conv_id, **kwargs)


def _queue_message_create(**kwargs):
    from matrx_ai.persistence.queue_helpers import queue_message_create as _q

    return _q(**kwargs)


def _queue_message_update(msg_id, **kwargs):
    from matrx_ai.persistence.queue_helpers import queue_message_update as _q

    return _q(msg_id, **kwargs)


async def _hide_superseded_failed_turns(conversation_id: str, up_to_position: int) -> int:
    """A successful turn supersedes the FAILED attempts before it.

    While a turn keeps failing, the user SHOULD see the failures. The moment a
    real response lands, those prior attempts are clutter — so collapse them out
    of the USER's view (``is_visible_to_user=False``) while KEEPING the rows for
    the record. They are already ``is_visible_to_model=False`` (the agent never
    saw them and still won't — we set it again here defensively). Net model
    visibility is unchanged (false→false), so NO cache bust is needed.

    Platform rule, not a one-off: a conversation's tail run of failed attempts
    collapses the instant a real response lands at or after them. Earlier
    failures were already hidden by the success that followed THEM, so this only
    ever touches the current run. Best-effort — it must NEVER break the
    successful turn it follows.
    """
    if _get_coordinator() is None:
        from matrx_ai.persistence import standalone_coordinator

        async with standalone_coordinator(
            reason="hide_superseded_failed_turns",
            conversation_id=conversation_id,
        ):
            return await _hide_superseded_failed_turns(conversation_id, up_to_position)

    from matrx_ai.db._registry import get_model

    cx_message_model = get_model("Message")
    rows = await cx_message_model.filter_items(
        conversation_id=conversation_id,
        status="failed",
        is_visible_to_user=True,
    )
    hidden = 0
    for r in rows:
        try:
            if int(getattr(r, "position", 0) or 0) > up_to_position:
                continue
        except (TypeError, ValueError):
            pass
        mid = str(r.id)
        fields = {"is_visible_to_user": False, "is_visible_to_model": False}
        _queue_message_update(mid, **fields)
        hidden += 1
    return hidden


def _queue_request_create(**kwargs):
    from matrx_ai.persistence.queue_helpers import queue_request_create as _q

    return _q(**kwargs)


def _queue_user_request_update(req_id, **kwargs):
    from matrx_ai.persistence.queue_helpers import queue_user_request_update as _q

    return _q(req_id, **kwargs)


def _build_cx_request_error(ur_data: dict[str, Any]) -> dict[str, Any]:
    """Structured error for cx_request.error from the failed request's data.

    Parses a provider status code out of the message (e.g. 'Error code: 400')
    so failed requests are filterable by code; the full structured error and
    the exact wire payload live in the linked cx_request_snapshot.
    """
    import re as _re

    msg = ur_data.get("error") or ""
    payload: dict[str, Any] = {"message": str(msg)}
    m = _re.search(r"Error code:\s*(\d{3})", str(msg))
    if m:
        payload["status_code"] = int(m.group(1))
    fr = ur_data.get("finish_reason")
    if fr:
        payload["finish_reason"] = str(fr)
    return payload


def _is_valid_uuid(value: str | None) -> bool:
    if not value:
        return False
    try:
        UUID(value)
        return True
    except (ValueError, AttributeError):
        return False


def _compute_message_sizes(content: Any) -> tuple[int, int]:
    """Return (content_chars, tool_results_chars) for a message's content blocks.

    ``content_chars`` is the JSON-stringified length of the stored content —
    the size of what actually lives in cx_message.content (pointer blocks for
    tool messages are tiny; text blocks for user/assistant messages carry the
    real text). It reflects what the row physically holds.

    ``tool_results_chars`` is the sum of ``output_chars`` across every
    tool_result block found in ``content``. For tool messages this is the
    "logical" cost — what the model will actually see when the translator
    expands pointer blocks back into full tool output. For non-tool messages
    it's 0.

    Defensive against non-list and non-dict content shapes — returns (0, 0)
    rather than raising, since this metric is observational and must never
    block a write.
    """
    import json as _json

    try:
        content_chars = len(_json.dumps(content, default=str))
    except (TypeError, ValueError):
        content_chars = 0

    tool_results_chars = 0
    if isinstance(content, list):
        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get("type") != "tool_result":
                continue
            try:
                tool_results_chars += int(block.get("output_chars", 0) or 0)
            except (TypeError, ValueError):
                continue

    return content_chars, tool_results_chars


async def _backfill_tool_message(
    msg: dict[str, Any],
    message_id: str,
    conversation_id: str,
) -> list[dict[str, Any]]:
    """Set message_id on every matching cx_tool_call row and build pointer blocks.

    For each ToolResultContent item in the message we:
      1. Set cx_tool_call.message_id = message_id  (backfill via logger)
      2. Read output_chars + output_preview from the in-memory ToolResultContent
         object (stamped synchronously by ToolExecutionLogger.prepare_metadata()
         in executor.py before the fire-and-forget DB task fires)
      3. Return a list of ToolResultPart pointer-block dicts to write into
         cx_message.content so the message is no longer an empty anchor.

    NOTE: msg["content"] holds the original ToolResultContent objects from the
    execution pipeline. The [] written to the DB earlier is msg_content (a local
    variable), not msg["content"], so this read is safe.

    Returns the list of pointer blocks (may be empty on failure — callers
    treat this as fire-and-forget and fall back to an empty content array).
    """
    from matrx_ai.tools.handle_tool_calls import get_executor

    original_content = msg.get("content", [])
    if not isinstance(original_content, list):
        return []

    executor = get_executor()
    tool_logger = executor.execution_logger
    pointer_blocks: list[dict[str, Any]] = []

    for item in original_content:
        call_id: str | None = None
        tool_name: str = ""
        output_chars: int = 0
        output_preview: dict[str, Any] | None = None
        is_error: bool = False

        if isinstance(item, dict):
            call_id = item.get("call_id") or item.get("tool_use_id")
            tool_name = item.get("name", "")
            output_chars = int(item.get("output_chars", 0) or 0)
            output_preview = item.get("output_preview")
            is_error = bool(item.get("is_error", False))
        elif hasattr(item, "call_id"):
            call_id = getattr(item, "call_id", None) or getattr(item, "tool_use_id", None)
            tool_name = getattr(item, "name", "") or getattr(item, "tool_name", "")
            output_chars = int(getattr(item, "output_chars", 0) or 0)
            output_preview = getattr(item, "output_preview", None)
            is_error = bool(getattr(item, "is_error", False))

        if not call_id:
            continue

        # Backfill message_id on the cx_tool_call row (fire-and-forget)
        try:
            await tool_logger.backfill_message_id(call_id, conversation_id, message_id)
        except Exception:
            pass

        # Build the pointer block from in-memory data (no DB round-trip needed)
        block: dict[str, Any] = {
            "type": "tool_result",
            "call_id": call_id,
            "tool_use_id": call_id,
            "name": tool_name,
            "is_error": is_error,
            "output_chars": output_chars,
        }
        if output_preview is not None:
            block["output_preview"] = output_preview

        pointer_blocks.append(block)

    return pointer_blocks


async def persist_completed_request(
    completed: CompletedRequest,
    conversation_id: str | None = None,
    debug: bool = False,
    state: ExecutionState | None = None,
    *,
    since_position: int | None = None,
    since_iteration: int | None = None,
    is_final: bool = True,
    _terminal_lane_isolated: bool = False,
) -> dict[str, Any]:
    """Persist a CompletedRequest to the cx_ database tables.

    The cx_conversation row is guaranteed to exist (created by the
    conversation gate at request entry time).  This function:
        1. Update cx_conversation with all data from the completed config
        2. Write new cx_message rows (only messages produced by this execution)
        3. Create cx_user_request (parent)
        4. Create cx_request rows (one per iteration)

    Args:
        completed: A CompletedRequest instance from execute_until_complete()
        conversation_id: Optional existing conversation UUID. Falls back to
                         completed.request.conversation_id.

    Returns:
        Dict with created record IDs:
            {
                "conversation_id": str,
                "user_request_id": str,
                "message_ids": list[str],
                "request_ids": list[str],
            }

    Client host: when a ConversationStore is configured (matrx-local), the
    ENTIRE persist is delegated wholesale to the store — 0.1.26
    ConversationHandler semantics. The store receives the CompletedRequest and
    owns messages/requests/status; nothing below (cxm, coordinator, model
    lookup) runs. May be called more than once per request (mid-run flush +
    final) — the store owns upsert semantics.
    """
    from matrx_ai.client_host import get_conversation_store

    _store = get_conversation_store()
    if _store is not None:
        try:
            return await _store.persist_completed_request(
                completed, conversation_id=conversation_id
            )
        except Exception as exc:
            vcprint(
                f"[CX PERSISTENCE] ConversationStore.persist_completed_request failed: {exc}",
                color="red",
            )
            return {
                "conversation_id": conversation_id or "",
                "user_request_id": "",
                "message_ids": [],
                "request_ids": [],
            }

    # Every server-host write is Coordinator-owned. RequestLane callers already
    # have one; background/non-streaming callers get an isolated Coordinator
    # whose exit is a synchronous durability barrier. The former bare-Session
    # fallback bypassed ownership for Conversation and Message and produced the
    # CoordinatorWriteViolation reported on 2026-08-17.
    lane = get_current_lane()
    inherited_terminal_lane = (
        not _terminal_lane_isolated
        and lane is not None
        and getattr(lane, "phase", None) != "active"
    )
    if inherited_terminal_lane or _get_coordinator() is None:
        from matrx_ai.persistence import standalone_coordinator

        resolved_conversation_id = conversation_id or getattr(
            completed.request, "conversation_id", None
        )
        resolved_request_id = getattr(completed.request, "request_id", None)
        async with standalone_coordinator(
            reason="persist_completed_request",
            request_id=str(resolved_request_id) if resolved_request_id else None,
            conversation_id=(
                str(resolved_conversation_id) if resolved_conversation_id else None
            ),
        ):
            return await persist_completed_request(
                completed,
                conversation_id=conversation_id,
                debug=debug,
                state=state,
                since_position=since_position,
                since_iteration=since_iteration,
                is_final=is_final,
                _terminal_lane_isolated=True,
            )

    # vcprint(
    #     completed,
    #     "[CX PERSISTENCE PERSIST COMPLETED REQUEST] Before to storage dict",
    #     color="green",
    # )

    storage = completed.to_storage_dict()
    model_manager = _model_manager()
    if model_manager is None:
        raise ValueError("Model manager is not initialized")

    if debug:
        vcprint(
            storage,
            "[CX PERSISTENCE PERSIST COMPLETED REQUEST] After to storage dict",
            color="blue",
        )

    conv_data = storage["conversation"]
    msg_list = storage["messages"]
    ur_data = storage["user_request"]
    req_list = storage["requests"]

    # vcprint(conv_data, "[CX Persistence] Conv Data", color="pink")

    ai_model_name = conv_data.get("ai_model")
    # vcprint(ai_model_name, "[CX Persistence] AI Model Name", color="pink")

    primary_ai_model_id = await model_manager.load_model_get_string_uuid(ai_model_name)
    # vcprint(primary_ai_model_id, "[CX Persistence] Primary AI Model ID", color="pink")

    user_id = conv_data.get("created_by") or conv_data.get("user_id")

    result: dict[str, Any] = {
        "conversation_id": None,
        "user_request_id": None,
        "message_ids": [],
        "request_ids": [],
    }

    if not _is_valid_uuid(user_id):
        vcprint(
            f"[CX PERSISTENCE PERSIST COMPLETED REQUEST] REJECTED — non-UUID user_id: {user_id!r}. "
            f"Cannot persist data without a valid user identity.",
            color="red",
        )
        return result

    try:
        # Resolve tracker and emitter early — needed throughout all sections
        from matrx_ai.context.app_context import try_get_app_context

        _ctx = try_get_app_context()
        tracker = try_get_tracker()
        emitter = _ctx.emitter if _ctx else None

        # Persistence intent (set by execute_ai_request, identical to the API's
        # skip_persistence). store=False → ephemeral: write NOTHING (no
        # cx_conversation / cx_user_request / cx_message / cx_request). When
        # there is no context (e.g. a direct unit test) we default to persisting.
        _should_persist = _ctx is None or _ctx.store

        # System-run mode (run_agent(system_run=True)): an internal machine
        # call whose transcript is throwaway. Persist ONLY the cost spine —
        # section 3 (cx_request cost rows) + section 4 (cx_user_request
        # rollup); the gate already wrote the minimal cx_conversation FK
        # anchor. Sections 1 (conversation config backfill) and 2 (cx_message
        # rows) are skipped, as are cache-state refresh and the context-state
        # event. A paid call NEVER loses its cost record — that is the whole
        # difference from store=False. (2026-07-07 starvation root cause:
        # ~40 concurrent internal derive calls each ran the full machinery.)
        _system_run = bool(_ctx is not None and getattr(_ctx, "system_run", False))
        _execution_kind = getattr(_ctx, "execution_kind", None) if _ctx is not None else None
        _execution_id = getattr(_ctx, "execution_id", None) if _ctx is not None else None
        if (_execution_kind is None) != (_execution_id is None):
            raise ValueError(
                "persist_completed_request: execution_kind and execution_id must be set together"
            )

        # Reserved IDs live on the executor's owned ExecutionState — never on
        # AppContext.metadata. Prefer the state object the caller threaded in
        # explicitly; fall back to the ContextVar so out-of-band callers still
        # work. Returns empty dicts when no execution is active (no harm — the
        # persistence path will then create new IDs via the DB sequence).
        _exec_state = state or try_get_execution_state()
        reserved_msg_ids: dict[int, str] = (
            dict(_exec_state.reserved_message_ids) if _exec_state else {}
        )
        reserved_req_ids: dict[int, str] = (
            dict(_exec_state.reserved_request_ids) if _exec_state else {}
        )
        # cx_message.id of messages that already existed before this execution
        # (loaded from the DB — e.g. a retry reloads the conversation). Persist
        # must NOT re-INSERT these; doing so duplicated the user message on retry.
        pre_existing_ids: set[str] = (
            set(getattr(_exec_state, "pre_existing_message_ids", set()) or set())
            if _exec_state
            else set()
        )

        # ============================================================
        # 1. CONVERSATION — update existing (created by conversation gate)
        #
        # The gate creates a minimal row (just id + created_by + status).
        # This update backfills ALL real data from the completed
        # UnifiedConfig via to_storage_dict().  Every field that
        # to_storage_dict() puts into conv_data MUST be written here.
        # ============================================================
        db_conversation_id = conversation_id or completed.request.conversation_id

        # Defense-in-depth (2026-06-12): a non-empty but NON-UUID
        # conversation_id (the classic offender is "" — an AppContext whose
        # conversation_id was never set) cannot be written to the UUID
        # cx_message.conversation_id / cx_request.conversation_id columns.
        # Left unguarded it surfaces deep inside the commit barrier as the
        # cryptic `invalid input syntax for type uuid: ""` and parks the
        # whole request (this is exactly what killed Study Pack workflow
        # runs). user_id is already valid here (guarded above), so an
        # invalid conversation_id is a CALLER bug — a request established
        # without a conversation. Fail loud and specific instead of cryptic.
        if db_conversation_id and not _is_valid_uuid(db_conversation_id):
            raise ValueError(
                "persist_completed_request: conversation_id is set but not a "
                f"valid UUID: {db_conversation_id!r} (user_id={user_id!r}, "
                f"request_id={completed.request.request_id!r}). A caller "
                "established an AI request without a valid conversation — set "
                "conversation_id on the AppContext before the LLM call. "
                "(Workflow nodes: the scheduler installs the run's context; "
                "see matrx_graph scheduler _run_one + workflow detached ctx.)"
            )

        if _system_run and db_conversation_id and _is_valid_uuid(db_conversation_id):
            # Cost-only mode: the gate's minimal row is the FK anchor; skip the
            # (large) config/system_instruction backfill UPDATE entirely.
            result["conversation_id"] = db_conversation_id
        elif _should_persist and db_conversation_id and _is_valid_uuid(db_conversation_id):
            update_kwargs: dict[str, Any] = {
                "id": db_conversation_id,
                "last_model_id": primary_ai_model_id,
                "message_count": conv_data["message_count"],
                "config": conv_data.get("config", {}),
            }

            # The system prompt is a write-once conversation prefix.  The first
            # completed turn creates it; later turns may update config/history,
            # but never replace the provider-cache prefix.
            existing_system_instruction = None
            try:
                existing_conversation = await _cxm().conversation.load_conversation_by_id(
                    db_conversation_id
                )
                existing_system_instruction = getattr(
                    existing_conversation, "system_instruction", None
                )
            except Exception as exc:  # noqa: BLE001 - gate INSERT may still be queued
                vcprint(
                    f"[CX PERSISTENCE] system-prompt freeze lookup deferred for "
                    f"{db_conversation_id}: {type(exc).__name__}: {exc}",
                    color="yellow",
                )
            # ``persist_completed_request`` can be reached more than once in a
            # turn (for example completion plus a detached finalizer) before
            # the coordinator flushes. The DB read cannot see the first queued
            # write, so it is not a sufficient ownership check. Marking the
            # request config frozen immediately makes this process-local state
            # authoritative until that write is durable and prevents a second
            # immutable-column UPDATE from aborting the whole transaction.
            if (
                not completed.request.config.system_prompt_frozen
                and not existing_system_instruction
                and conv_data.get("system_instruction") is not None
            ):
                update_kwargs["system_instruction"] = conv_data["system_instruction"]
            update_kwargs["config"] = {
                **update_kwargs["config"],
                "system_prompt_frozen": True,
            }
            completed.request.config.system_prompt_frozen = True
            if conv_data.get("metadata") is not None:
                update_kwargs["metadata"] = conv_data["metadata"]
            if conv_data.get("parent_conversation_id") and _is_valid_uuid(
                conv_data["parent_conversation_id"]
            ):
                # This UPDATE coalesces with the gate's queued INSERT into a
                # single INSERT, so re-stamping an absent parent here would
                # reintroduce the FK violation the gate just avoided. Verify
                # existence through the same gate helper before stamping.
                from matrx_ai.db.conversation_gate import (
                    resolve_parent_conversation_lineage,
                )

                verified_parent = await resolve_parent_conversation_lineage(
                    conv_data["parent_conversation_id"],
                    db_conversation_id,
                )
                if verified_parent:
                    update_kwargs["parent_conversation_id"] = verified_parent

            # Record the most recent turn's OUTCOME on the conversation (lifecycle
            # `status` stays active|archived — this is the separate last-turn
            # rollup). Lets a recovery/retry system find conversations whose last
            # turn FAILED and which request to retry, straight off the row.
            _last_req_id = ur_data.get("request_id") or completed.request.request_id
            if _last_req_id and _is_valid_uuid(_last_req_id):
                update_kwargs["last_request_id"] = _last_req_id
            update_kwargs["last_request_status"] = ur_data.get("status") or "completed"

            # Route through the coordinator so this UPDATE coalesces with
            # the gate's queued INSERT (if this is a new conversation) into
            # a single INSERT carrying both sets of fields. For existing
            # conversations the coordinator emits a plain UPDATE.
            conv_update_fields = {k: v for k, v in update_kwargs.items() if k != "id"}
            _queue_conversation_update(db_conversation_id, **conv_update_fields)
            result["conversation_id"] = db_conversation_id

            if tracker and emitter:
                try:
                    await tracker.mark_active(emitter, "conversation", db_conversation_id)
                except Exception:
                    pass
        else:
            vcprint(
                f"[CX PERSISTENCE PERSIST COMPLETED REQUEST] No valid conversation_id to update: {db_conversation_id!r}",
                color="yellow",
            )

        # ============================================================
        # 2. MESSAGES — write trigger message + messages produced by this execution
        #    Skipped entirely for ephemeral conversations (store=False).
        # ============================================================
        _should_persist_messages = (_ctx is None or _ctx.store) and not _system_run
        assistant_message_ids_by_iteration: dict[int, str] = {}

        if _should_persist_messages:
            trigger_pos = completed.trigger_message_position
            start_pos = completed.result_start_position
            end_pos = completed.result_end_position

            if start_pos is not None and end_pos is not None:
                write_from = trigger_pos if trigger_pos is not None else start_pos
                # Per-turn commit barrier: only write rows ABOVE the high-water
                # mark a prior turn's finalize() already committed. Prevents a
                # rolled Session from re-INSERTing an already-committed row.
                if since_position is not None:
                    write_from = max(write_from, since_position + 1)
                new_messages = [m for m in msg_list if write_from <= m["position"] <= end_pos]
            else:
                new_messages = msg_list
                if since_position is not None:
                    new_messages = [m for m in new_messages if m["position"] > since_position]

            for msg in new_messages:
                role_val = msg["role"]
                role_val = role_val.value if hasattr(role_val, "value") else role_val
                # Always persist with "active" — the in-memory status from the
                # config may be "pending" if the message was loaded from a prior
                # failed run; we want to mark it active now.
                status_val = "active"

                raw_content = msg["content"]
                is_tool_message = role_val == "tool"
                position = msg["position"]

                # Already-persisted message (loaded from the DB before this
                # execution — e.g. a retry reloads the conversation's messages).
                # Skip the INSERT so we don't duplicate it; it already exists.
                _existing_id = msg.get("id")
                if _existing_id and _existing_id in pre_existing_ids:
                    result["message_ids"].append(_existing_id)
                    continue

                if is_tool_message:
                    msg_content = []
                else:
                    try:
                        msg_content = validate_message_content(raw_content)
                    except ValueError as validation_err:
                        vcprint(
                            f"[CX PERSISTENCE] Message content validation failed "
                            f"(position={position}, role={role_val}): {validation_err}. "
                            f"raw_content={_safe_content_repr(raw_content)}",
                            color="red",
                        )
                        msg_content = raw_content

                reserved_id = reserved_msg_ids.get(position) or reserved_msg_ids.get(str(position))

                # LAYER-2 GUARD (2026-07-02): a message carrying an in-memory id
                # that is neither a pre-existing cx_message.id nor this
                # position's reservation is an id NOBODY will honor — persistence
                # keys rows off the reservation channel only. This is exactly how
                # an Anthropic "msg_*" response id ended up as a cx_message UUID
                # PK and 500'd the turn (the translators are fixed — layer 1 —
                # but any future path that stamps UnifiedMessage.id outside the
                # reservation channel must SCREAM here, never slip through).
                if _existing_id and _existing_id != reserved_id:
                    vcprint(
                        f"[CX PERSISTENCE] ⛔ UNRESERVED MESSAGE ID DISCARDED — "
                        f"position={position} role={role_val} carries in-memory "
                        f"id={_existing_id!r} that is neither pre-existing nor "
                        f"reserved (reserved_id={reserved_id!r}, "
                        f"conversation={db_conversation_id}). UnifiedMessage.id "
                        f"must be cx_message.id assigned via the reservation "
                        f"channel (executor reservation / handoff registration) "
                        f"— fix the caller that stamped it. Minting a fresh "
                        f"UUID for the row.",
                        color="red",
                    )
                    _existing_id = None

                vcprint(
                    f"[CX PERSISTENCE] Persisting logical_position={position} role={role_val} "
                    f"reserved_id={reserved_id} content_len={len(msg_content) if isinstance(msg_content, list) else '?'}",
                    color="cyan",
                )

                # Per-message size capture (Phase 1b). content_chars is the
                # row's stored size; tool_results_chars is 0 here because tool
                # messages get their pointer blocks (and the real size rollup)
                # written below in the is_tool_message branch.
                content_chars, tool_results_chars = _compute_message_sizes(msg_content)

                # Message-level metadata (cx_message.metadata). Reserved keys that
                # earned typed columns (model_context / tools_on_call, stamped on
                # the user message by apply_context_objects) are LIFTED out into
                # their columns so the row carries the per-turn call record
                # first-class and metadata stays lean.
                _clean_meta, _promoted = lift_promoted_message_columns(msg.get("metadata"))
                _meta_kwargs = {"metadata": _clean_meta} if _clean_meta else {}

                msg_id: str = ""
                # persist_completed_request establishes a request or standalone
                # Coordinator before reaching this loop, so queue helpers cannot
                # drop these writes for lack of an owner.
                _msg_fields: dict[str, Any] = {
                    "role": role_val,
                    "status": status_val,
                    "content": msg_content,
                    "content_chars": content_chars,
                    "tool_results_chars": tool_results_chars,
                    # Explicit owner stamp — service-role / background writes have
                    # no JWT so _stamp_actor cannot derive created_by automatically.
                    # user_id is validated as a UUID earlier in this function.
                    "created_by": user_id or None,
                    **_meta_kwargs,
                    **_promoted,
                }
                from uuid import uuid4 as _uuid4

                try:
                    if reserved_id:
                        # Streaming path: coalesce with the executor's
                        # reservation INSERT into a single INSERT carrying both
                        # the reservation's status='pending' and this UPDATE's
                        # content/status.
                        _queue_message_update(reserved_id, **_msg_fields)
                        msg_id = reserved_id

                        if tracker and emitter:
                            try:
                                await tracker.mark_active(emitter, "message", msg_id)
                            except Exception:
                                pass
                    else:
                        # No reservation existed (tool messages, iteration-2+
                        # assistant rows) — fresh INSERT with a freshly minted
                        # UUID. NEVER trust msg["id"] here: the only sanctioned
                        # id channels are reserved_msg_ids (handled above) and
                        # pre_existing_ids (skipped earlier). A deliberately
                        # pre-announced row (handoff synthetic) registers into
                        # state.reserved_message_ids like everything else.
                        msg_id = str(_uuid4())
                        _queue_message_create(
                            id=msg_id,
                            conversation_id=db_conversation_id,
                            position=APPEND_MESSAGE_POSITION,
                            **_msg_fields,
                        )
                        if role_val == "assistant":
                            # ANNOUNCE every fresh assistant row (2026-07-07 root
                            # fix for the "surplus tool_uses duplicated onto the
                            # FIRST assistant message" corruption, conversation
                            # bcc588b6). The executor announces ONLY the loop-start
                            # first-assistant reservation; iteration-2+ assistant
                            # rows were INSERTed here silently, so the client knew
                            # exactly ONE assistant cx_message id per run and — at
                            # stream end — folded the WHOLE run's assembled content
                            # (all iterations' text + tool_calls) onto that single
                            # id, then persisted it via the cx_message_set_content
                            # RPC (artifact materialization). Announcing each row
                            # activates the client's multi-reservation per-
                            # iteration partitioning, so each turn's content lands
                            # on its own row. Registering the id on the reservation
                            # channel ALSO makes any re-persist of this position an
                            # UPDATE (idempotent), never a duplicate INSERT.
                            if _exec_state is not None:
                                _exec_state.reserved_message_ids[position] = msg_id
                                reserved_msg_ids[position] = msg_id
                            if tracker and emitter:
                                try:
                                    await tracker.reserve(
                                        emitter=emitter,
                                        db_project="matrx",
                                        table="message",
                                        parent_refs={
                                            "conversation_id": db_conversation_id or "",
                                            "user_request_id": ur_data.get("request_id")
                                            or completed.request.request_id
                                            or "",
                                        },
                                        metadata={
                                            "role": "assistant",
                                            "position": position,
                                            "position_kind": "logical_index",
                                            "source": "iteration_persist",
                                        },
                                        record_id=msg_id,
                                    )
                                    await tracker.mark_active(emitter, "message", msg_id)
                                except Exception as _announce_exc:
                                    vcprint(
                                        f"[CX PERSISTENCE] Failed to announce iteration "
                                        f"assistant row {msg_id} (position={position}): "
                                        f"{_announce_exc}. The row is still durable; the "
                                        f"client just won't have its anchor this stream.",
                                        color="yellow",
                                    )
                    vcprint(
                        f"[CX PERSISTENCE] Queued msg_id={msg_id} logical_position={position} ok",
                        color="green",
                    )
                except Exception as msg_err:
                    vcprint(
                        f"[CX PERSISTENCE] FAILED to queue message position={position} "
                        f"role={role_val} reserved_id={reserved_id}: {msg_err}. "
                        f"Re-raising — a lost message blows up the barrier, never "
                        f"silently skipped. (Persistence contract — CLAUDE.md.)",
                        color="red",
                    )
                    # A message we cannot queue is a lost write. Do NOT continue
                    # past it — propagate so the commit barrier stops the run.
                    raise

                result["message_ids"].append(msg_id)
                if role_val == "assistant":
                    provider_iteration = (msg.get("metadata") or {}).get("provider_iteration")
                    if isinstance(provider_iteration, int):
                        assistant_message_ids_by_iteration.setdefault(provider_iteration, msg_id)

                if is_tool_message:
                    # Build pointer blocks AND backfill message_id on cx_tool_call rows.
                    # The pointer blocks become the real content of this message so the
                    # frontend can render tool result metadata without loading cx_tool_call.
                    try:
                        pointer_blocks = await _backfill_tool_message(
                            msg, msg_id, db_conversation_id
                        )
                    except Exception as backfill_err:
                        vcprint(
                            f"[CX PERSISTENCE PERSIST COMPLETED REQUEST] cx_tool_call backfill error: {backfill_err}",
                            color="yellow",
                        )
                        pointer_blocks = []

                    if pointer_blocks:
                        try:
                            validated_blocks = validate_message_content(pointer_blocks)
                            # Recompute sizes now that the pointer blocks are
                            # the real content — tool_results_chars rolls up
                            # the per-call output_chars from the pointers.
                            ptr_content_chars, ptr_tool_chars = _compute_message_sizes(
                                validated_blocks
                            )
                            # Coalesces with the row's earlier INSERT/UPDATE
                            # ops in the coordinator — final flush writes
                            # ONE INSERT with the merged content.
                            _queue_message_update(
                                msg_id,
                                content=validated_blocks,
                                content_chars=ptr_content_chars,
                                tool_results_chars=ptr_tool_chars,
                            )
                        except Exception as content_err:
                            vcprint(
                                f"[CX PERSISTENCE PERSIST COMPLETED REQUEST] tool pointer block update error: {content_err}",
                                color="yellow",
                            )

            # On a FAILED request, eagerly close any reserved message placeholder
            # that never became a real message (e.g. the assistant placeholder for
            # a turn that errored before producing output) → 'failed'. Without this
            # it dangles at 'pending' until the watchdog sweeps it to 'abandoned'
            # (300s) and fires a false stuck-row alert. 'failed' (errored eagerly)
            # is a DISTINCT state from 'abandoned' (watchdog-swept on timeout) — we
            # never conflate them. SAFE check: only positions absent from the actual
            # message list are unfilled — prior committed turns ARE in msg_list, so
            # their reservations are never touched. See
            # docs/persistence/STATUS_AND_ERROR_FIELDS.md.
            if ur_data.get("status") == "failed" and reserved_msg_ids:
                _live_positions = {int(m["position"]) for m in msg_list}
                for _pos, _mid in reserved_msg_ids.items():
                    try:
                        _pos_int = int(_pos)
                    except (TypeError, ValueError):
                        continue
                    if not _mid or _pos_int in _live_positions:
                        continue
                    # Hide the failed turn from the AGENT (is_visible_to_model=
                    # False — the designed primitive, same as compaction) while
                    # keeping it for the USER (is_visible_to_user stays true) as a
                    # normal error message in history. The error text is the
                    # message content so the FE renders it like any other turn.
                    _err_raw = ur_data.get("error")
                    _err_text = _err_raw or "This response failed to generate."
                    # Structured error column (presence => failed). Replaces the old
                    # metadata.{failed,error} smuggling. Pass a dict straight through
                    # (already-structured upstream error); wrap a bare string.
                    _err_struct = (
                        _err_raw
                        if isinstance(_err_raw, dict)
                        else {"type": "turn_failed", "message": str(_err_text)}
                    )
                    _fail_fields: dict[str, Any] = {
                        "status": "failed",
                        "is_visible_to_model": False,
                        "content": [{"type": "text", "text": str(_err_text)}],
                        "error": _err_struct,
                    }
                    try:
                        _queue_message_update(_mid, **_fail_fields)
                        vcprint(
                            f"[CX PERSISTENCE] Closed unfilled reserved message "
                            f"{_mid} (position={_pos_int}) → 'failed', hidden from "
                            f"agent (is_visible_to_model=False), error in content.",
                            color="yellow",
                        )
                    except Exception as _close_err:
                        vcprint(
                            f"[CX PERSISTENCE] Failed to close reserved message "
                            f"{_mid} on failed request (ignored): {_close_err}",
                            color="yellow",
                        )

            # A SUCCESSFUL final turn supersedes the prior FAILED attempts at this
            # turn — collapse them out of the USER's view (rows KEPT for the
            # record; already hidden from the agent). Best-effort; never fatal.
            if is_final and ur_data.get("status") != "failed" and db_conversation_id:
                try:
                    _up_to = max((int(m["position"]) for m in msg_list), default=0)
                    _hidden = await _hide_superseded_failed_turns(db_conversation_id, _up_to)
                    if _hidden:
                        vcprint(
                            f"[CX PERSISTENCE] Superseded {_hidden} prior failed "
                            f"turn(s) → hidden from user (kept for the record).",
                            color="green",
                        )
                except Exception as _sup_err:
                    vcprint(
                        f"[CX PERSISTENCE] hide-superseded-failures skipped "
                        f"(non-fatal): {_sup_err}",
                        color="yellow",
                    )

        now = datetime.now(UTC)
        user_request_id = ur_data.get("request_id") or completed.request.request_id
        result["user_request_id"] = user_request_id

        # ── HEARTBEAT — refresh last_activity_at EVERY turn (not just is_final),
        # in the SAME flush as this turn's messages. The lifecycle watchdog ages
        # off last_activity_at, so an ACTIVE long request (turns committing) is
        # never falsely marked 'abandoned' (the 2026-05-23 false-abandon fix);
        # only a request idle past the SLA crosses it.
        if (
            _should_persist
            and user_request_id
            and _is_valid_uuid(user_request_id)
            and _get_coordinator() is not None
        ):
            _queue_user_request_update(user_request_id, last_activity_at=now)

        # ============================================================
        # 3. REQUEST ROWS — one per iteration (written FIRST so the
        #    aggregate in step 4 can read them back from the DB)
        # ============================================================
        for req in req_list if _should_persist else []:
            iteration_num = req.get("iteration", 1)
            # Per-turn barrier: skip cx_request cost rows already committed by a
            # prior turn's finalize() (a rolled Session can't re-INSERT them).
            if since_iteration is not None and int(iteration_num) <= since_iteration:
                continue
            iter_ai_model_id = await model_manager.load_model_get_string_uuid(req.get("ai_model"))

            # RECORD THE FAILED REQUEST (May 2026 — supersedes the old skip).
            # cx_request.ai_model_id is NOT NULL. When the provider rejects
            # BEFORE a model resolves from the RESPONSE (e.g. Anthropic 400 on
            # request shape), ``req.ai_model`` is None — but the INTENDED model
            # IS known from the request config (``primary_ai_model_id``, resolved
            # from conv_data above). The failed API call is the single most
            # valuable row to keep, so we DO NOT skip it: fall back to the config
            # model and record status='failed' + error. This also materializes
            # the cx_request id we already reserved + streamed to the client (no
            # phantom id) and links the cx_request_snapshot to it.
            _resolved_from_response = bool(iter_ai_model_id)
            _request_failed = ur_data.get("status") == "failed"
            if not iter_ai_model_id:
                iter_ai_model_id = primary_ai_model_id
                if not iter_ai_model_id:
                    # Even the config model is unknown — only NOW is skipping
                    # justified (the NOT NULL column truly can't be satisfied).
                    vcprint(
                        f"[CX PERSISTENCE] Skipping cx_request INSERT for "
                        f"iteration {iteration_num}: ai_model_id unresolvable "
                        f"from response ({req.get('ai_model')!r}) AND config. "
                        f"cx_user_request status='failed' still captures the error.",
                        color="yellow",
                    )
                    continue
            reserved_req_id = reserved_req_ids.get(iteration_num) or reserved_req_ids.get(
                str(iteration_num)
            )

            request_metadata = dict(req.get("metadata", {}))
            if "response_message_id" not in request_metadata:
                response_message_id = assistant_message_ids_by_iteration.get(int(iteration_num))
                if response_message_id:
                    request_metadata["response_message_id"] = response_message_id

            req_create_data: dict[str, Any] = {
                "user_request_id": user_request_id,
                "conversation_id": db_conversation_id,
                "execution_kind": _execution_kind,
                "execution_id": _execution_id,
                "ai_model_id": iter_ai_model_id,
                "provider": req.get("provider"),
                "iteration": iteration_num,
                "input_tokens": req.get("input_tokens"),
                "output_tokens": req.get("output_tokens"),
                "cached_tokens": req.get("cached_tokens"),
                "total_tokens": req.get("total_tokens"),
                "cost": req.get("cost"),
                "api_duration_ms": req.get("api_duration_ms"),
                "tool_duration_ms": req.get("tool_duration_ms"),
                "total_duration_ms": req.get("total_duration_ms"),
                "tool_calls_count": req.get("tool_calls_count", 0),
                "tool_calls_details": req.get("tool_calls_details"),
                "finish_reason": req.get("finish_reason"),
                "response_id": req.get("response_id"),
                "metadata": request_metadata,
                # Phase 1c: verbatim provider usage. NULL when the provider's
                # response was missing usage entirely (rare; tracked anyway).
                "raw_usage": req.get("raw_usage"),
                # Phase 1d: trim audit, attached to the LAST iteration in the
                # set below after this loop builds the rows. Default None now.
                "trim_summary": req.get("trim_summary"),
            }

            # Mark THIS iteration failed when it's the attempt that failed: the
            # request failed AND no model resolved from a response (i.e. the
            # provider rejected before producing usage). Prior SUCCESSFUL
            # iterations resolved from their response and keep the default
            # 'completed'. The structured error (with parsed status_code for
            # reporting) goes here; the exact payload is in cx_request_snapshot.
            if _request_failed and not _resolved_from_response:
                req_create_data["status"] = "failed"
                req_create_data["error"] = _build_cx_request_error(ur_data)
                # finish_reason as a glanceable, column-level failure signal
                # (no jsonb parsing needed to spot a failed call).
                if not req_create_data.get("finish_reason"):
                    req_create_data["finish_reason"] = "error"

            # Generate id client-side if not pre-reserved so the queue helper
            # has a stable pk. The coalescer absorbs any duplicate INSERTs
            # for the same row, so the prior MatrxIntegrityError-absorbing
            # branch is no longer needed — duplicates become a single op.
            if reserved_req_id:
                req_id = reserved_req_id
            else:
                from uuid import uuid4 as _uuid4

                req_id = str(_uuid4())
            req_create_data["id"] = req_id

            # Pop the FK fields out and pass them explicitly so the queue helper
            # can declare the cx_user_request + cx_conversation dependencies.
            req_payload = dict(req_create_data)
            req_payload.pop("id", None)
            req_payload.pop("user_request_id", None)
            req_payload.pop("conversation_id", None)
            _queue_request_create(
                id=req_id,
                user_request_id=user_request_id,
                conversation_id=db_conversation_id,
                **req_payload,
            )
            result["request_ids"].append(req_id)

            if tracker and emitter and reserved_req_id:
                try:
                    await tracker.mark_active(emitter, "request", req_id)
                except Exception:
                    pass

        # ============================================================
        # 4. USER REQUEST — aggregate UPDATE from ALL cx_request rows
        #
        # We read every cx_request row under this user_request_id
        # (including the ones just written above) and compute true
        # totals.  This is always correct regardless of how many
        # execute_ai_request() calls share a single cx_user_request
        # (batch jobs, workflows, multi-step agents).  Each call to
        # persist_completed_request() re-derives the aggregate from
        # ground truth so no execution's data is ever lost.
        # ============================================================
        # Section 4 (cx_user_request rollup) + Phase 2/3 (cache_state +
        # context-state event) are REQUEST-level concerns. On a per-turn
        # barrier (is_final=False) we skip them: the per-iteration cx_request
        # rows above already carry each turn's cost, so nothing is lost, and
        # the rollup is derived once on the final commit (and on cancel via
        # the shield-persist path) — always recomputable from those rows.
        if _should_persist and is_final and user_request_id and _is_valid_uuid(user_request_id):
            # Compute aggregate IN-MEMORY from req_list. Previously this
            # read every cx_request row under user_request_id from the DB —
            # which no longer works because the rows are queued in the
            # coordinator (not yet flushed). Each persist_completed_request
            # call covers one execute_until_complete invocation, and each
            # invocation produces a unique request_id (== user_request_id).
            # Multi-call workflows on the same user_request_id are not the
            # supported pattern — when they happen, the second call's
            # aggregate will reflect only that call's req_list, and the
            # coordinator's UPDATE coalesces in last-write-wins fashion.
            agg_input = agg_output = agg_cached = agg_total_tokens = 0
            agg_cost = 0.0
            agg_cost_unknown = False
            agg_api_ms = agg_tool_ms = agg_total_ms = 0
            agg_tool_calls = 0
            agg_iterations = 0
            for r in req_list:
                agg_input += int(r.get("input_tokens") or 0)
                agg_output += int(r.get("output_tokens") or 0)
                agg_cached += int(r.get("cached_tokens") or 0)
                agg_total_tokens += int(r.get("total_tokens") or 0)
                if r.get("cost") is None:
                    agg_cost_unknown = True
                else:
                    agg_cost += float(r["cost"])
                agg_api_ms += int(r.get("api_duration_ms") or 0)
                agg_tool_ms += int(r.get("tool_duration_ms") or 0)
                agg_total_ms += int(r.get("total_duration_ms") or 0)
                agg_tool_calls += int(r.get("tool_calls_count") or 0)
                agg_iterations += 1

            # Prior usage_by_model: when running outside the coordinator,
            # read existing metadata for the row. When running through the
            # coordinator, the row hasn't been flushed yet — accept that
            # multi-call cumulative usage_by_model is rebuilt fresh from
            # this call's contribution only.
            prior_by_model: dict[str, Any] = {}
            if _get_coordinator() is None:
                existing_ur_rows = await _cxm().user_request.filter_user_requests(
                    id=user_request_id
                )
                if existing_ur_rows:
                    prior_meta = getattr(existing_ur_rows[0], "metadata", {}) or {}
                    prior_by_model = prior_meta.get("usage_by_model", {})

            # Start from prior state, then add this execution's contributions.
            merged_by_model: dict[str, Any] = dict(prior_by_model)
            if completed.total_usage.by_model:
                from dataclasses import asdict

                for model_name, usage_obj in completed.total_usage.by_model.items():
                    new_vals = asdict(usage_obj)
                    if model_name in merged_by_model:
                        existing_vals = merged_by_model[model_name]
                        merged_by_model[model_name] = {
                            "api": new_vals.get("api") or existing_vals.get("api"),
                            "cost": round(
                                float(existing_vals.get("cost", 0))
                                + float(new_vals.get("cost", 0)),
                                8,
                            ),
                            "input_tokens": existing_vals.get("input_tokens", 0)
                            + new_vals.get("input_tokens", 0),
                            "output_tokens": existing_vals.get("output_tokens", 0)
                            + new_vals.get("output_tokens", 0),
                            "total_tokens": existing_vals.get("total_tokens", 0)
                            + new_vals.get("total_tokens", 0),
                            "cached_input_tokens": existing_vals.get("cached_input_tokens", 0)
                            + new_vals.get("cached_input_tokens", 0),
                            "request_count": existing_vals.get("request_count", 0)
                            + new_vals.get("request_count", 0),
                        }
                    else:
                        merged_by_model[model_name] = new_vals

            # Build metadata for the user request row.
            request_metadata: dict[str, Any] = dict(ur_data.get("metadata", {}))
            if agg_cost_unknown:
                request_metadata["cost_reconciliation"] = "incomplete_child_costs"
                request_metadata["known_cost_subtotal"] = round(agg_cost, 6)
            if completed.metadata.get("response_id"):
                request_metadata["response_id"] = completed.metadata["response_id"]
            if merged_by_model:
                request_metadata["usage_by_model"] = merged_by_model

            ur_update_data: dict[str, Any] = {
                "total_input_tokens": agg_input,
                "total_output_tokens": agg_output,
                "total_cached_tokens": agg_cached,
                "total_tokens": agg_total_tokens,
                "total_cost": None if agg_cost_unknown else round(agg_cost, 6),
                "api_duration_ms": agg_api_ms,
                "tool_duration_ms": agg_tool_ms,
                "total_duration_ms": agg_total_ms,
                "iterations": agg_iterations,
                "total_tool_calls": agg_tool_calls,
                "status": ur_data.get("status", "completed"),
                "completed_at": now,
                "metadata": request_metadata,
            }

            if ur_data.get("finish_reason"):
                ur_update_data["finish_reason"] = ur_data["finish_reason"]
            if ur_data.get("error"):
                ur_update_data["error"] = _cx_error_text(ur_data["error"])

            # Queue the aggregate UPDATE. This is THE write whose loss caused
            # the 261-stuck-cx_user_request-rows leak. Coalescing with the
            # gate's INSERT (when this is the first call for this row) lands
            # one atomic INSERT carrying both pending fields and the
            # completed aggregate. Cancellation can no longer split this.
            _queue_user_request_update(user_request_id, **ur_update_data)

            if tracker and emitter:
                # Emit the ACTUAL terminal status — never hardcode 'completed'.
                # On a failed request the row was written status='failed' (see
                # to_storage_dict); emitting 'completed' here told the FE the
                # opposite and also set the tracked status so fail_all_pending
                # skipped it. The emitted event must match the persisted value.
                try:
                    if ur_update_data["status"] == "failed":
                        # metadata.reason='terminal_status' distinguishes a real
                        # persisted-failed record from a reservation ROLLBACK
                        # (fail_all_pending stamps reason='rollback') so the FE
                        # can treat the two differently. Carry the structured
                        # error when the row has one — it's already in hand.
                        _fail_meta: dict[str, Any] = {"reason": "terminal_status"}
                        if ur_update_data.get("error"):
                            _fail_meta["error"] = ur_update_data["error"]
                        await tracker.mark_failed(
                            emitter, "user_request", user_request_id, metadata=_fail_meta
                        )
                    else:
                        await tracker.mark_completed(emitter, "user_request", user_request_id)
                except Exception:
                    pass

            # ============================================================
            # Phase 2: refresh cx_conversation.cache_state so the next
            # turn's trim can apply the cache-aware gate. Best-effort —
            # never blocks the response.
            # ============================================================
            if (
                _should_persist
                and not _system_run
                and db_conversation_id
                and _is_valid_uuid(db_conversation_id)
            ):
                try:
                    await _refresh_cache_state(
                        conversation_id=db_conversation_id,
                        req_rows=req_list,
                        trim_summary=req_list[0].get("trim_summary")
                        if req_rows_available(req_list)
                        else None,
                    )
                except Exception as cs_err:
                    vcprint(
                        f"[CX PERSISTENCE] cache_state refresh failed (ignored): {cs_err}",
                        color="yellow",
                    )

            # Phase 3: emit context-state event so the FE Model Context tab
            # updates live without polling. Best-effort.
            #
            # Skip for sub-agent conversations: their cx_conversation row is
            # queued in the child's WriteCoordinator and only flushes on
            # child_agent_context exit (see queue_helpers._child_coordinator_scope).
            # _emit_context_state would read DB → DoesNotExist → exception →
            # yellow warning in logs. Sub-agent context-state is internal
            # scratch — the parent's context-state event covers what the
            # user-facing UI needs to render. ``parent_conversation_id`` is
            # the canonical "this is a sub-agent" marker (set by
            # AppContext.fork_for_child_agent).
            _is_sub_agent = bool(_ctx is not None and getattr(_ctx, "parent_conversation_id", None))
            if emitter and db_conversation_id and not _is_sub_agent and not _system_run:
                try:
                    await _emit_context_state(
                        emitter=emitter,
                        conversation_id=db_conversation_id,
                        agg_input=agg_input,
                        agg_output=agg_output,
                        agg_cached=agg_cached,
                        trim_summary=req_list[0].get("trim_summary")
                        if req_rows_available(req_list)
                        else None,
                    )
                except Exception as ev_err:
                    vcprint(
                        f"[CX PERSISTENCE] context-state event emit failed (ignored): {ev_err}",
                        color="yellow",
                    )
        elif is_final:
            vcprint(
                f"[CX PERSISTENCE PERSIST COMPLETED REQUEST] No valid request_id "
                f"for legacy cx_user_request rollup (runtime.global_request): "
                f"{user_request_id!r}",
                color="yellow",
            )

        # Empty delta is normal on the final barrier after a per-turn commit
        # already wrote the rows (since_position / since_iteration advanced).
        # Logging "0 messages, 0 request iterations" looks like a second save
        # and drowns the real one — skip the banner when nothing new was queued.
        n_messages = len(result["message_ids"])
        n_requests = len(result["request_ids"])
        if n_messages or n_requests:
            from matrx_ai.db.request_tracking_log import (
                format_request_tracking_lines,
                resolve_runtime_root_execution_id,
            )

            tracking = "\n".join(
                format_request_tracking_lines(
                    request_id=user_request_id,
                    conversation_id=db_conversation_id,
                    runtime_root_execution_id=resolve_runtime_root_execution_id(_ctx),
                )
            )
            vcprint(
                f"[CX PERSISTENCE PERSIST COMPLETED REQUEST] Saved Conversation:\n"
                f"{tracking}\n"
                f" - {n_messages} messages,\n"
                f" - {n_requests} request iterations "
                f"(legacy cx_request · retiring with cx_user_request)",
                color="green",
            )

        return result

    except Exception as e:
        vcprint(
            f"[CX PERSISTENCE PERSIST COMPLETED REQUEST] Error persisting request: {e}. "
            f"NOT swallowing — re-raising so the commit barrier blows up (data first). "
            f"A pre-queue failure here (e.g. model lookup) would otherwise advance the "
            f"high-water-mark past rows that were never queued = silent loss. "
            f"(Persistence contract — CLAUDE.md.)",
            color="red",
        )
        import traceback

        traceback.print_exc()
        # Do NOT swallow. The orchestrator's degrade path flushes whatever WAS
        # queued before this failure, and this raise stops the run loudly so a
        # partial persist can never masquerade as success.
        raise


async def apply_authoritative_user_request_rollup(user_request_id: str) -> None:
    """Overwrite cx_user_request numeric totals with the authoritative SUM over
    every committed cx_request row sharing ``user_request_id``.

    One user click = one cx_user_request = the total cost of everything it
    triggered (the parent's turns AND every sub-agent's turns, which all carry
    the same inherited user_request_id). The per-turn in-memory rollup in
    ``persist_completed_request`` only ever saw its OWN call's rows and wrote
    last-write-wins through the coordinator — so a parent finalizing after its
    sub-agents CLOBBERED their totals. This SUM, run once after the owner's
    final coordinator commit (when every row is durable), is idempotent and
    order-independent — recomputing the same total from ground truth structurally
    kills that clobber.

    Overwrites ONLY the numeric aggregates; status / completed_at / error /
    metadata.usage_by_model stay as the in-memory rollup wrote them.

    Loud-but-non-fatal: a failure leaves the in-memory value (a lower bound) and
    the per-row cx_request ground truth intact — both recomputable. Never raise:
    the response and per-row costs are already safe; turning a finished request
    into a failure here would lose the response.
    """
    if not _is_valid_uuid(user_request_id):
        return

    # Client host: totals live in the host store (persist_completed_request
    # delegated the whole turn write); there are no cx_request rows to SUM
    # and _cxm() would raise DBNotConfiguredError.
    from matrx_ai.client_host import get_conversation_store

    if get_conversation_store() is not None:
        return

    try:
        rollup = await _cxm().request.sum_costs_by_user_request(user_request_id)
    except Exception as exc:
        vcprint(
            f"[CX PERSISTENCE ROLLUP] SUM over cx_request for user_request "
            f"{user_request_id} failed ({type(exc).__name__}: {exc}); leaving the "
            f"per-turn rollup value in place. cx_request rows remain the ground "
            f"truth — the total is recomputable.",
            color="red",
        )
        return

    if rollup.request_count == 0:
        # No committed rows yet — should not happen post-finalize. Don't zero out
        # a row the in-memory path may have populated.
        return

    update_data: dict[str, Any] = {
        "total_input_tokens": rollup.input_tokens,
        "total_output_tokens": rollup.output_tokens,
        "total_cached_tokens": rollup.cached_tokens,
        "total_tokens": rollup.total_tokens,
        "total_cost": round(float(rollup.total_cost), 6),
        "api_duration_ms": rollup.api_duration_ms,
        "tool_duration_ms": rollup.tool_duration_ms,
        "total_duration_ms": rollup.total_duration_ms,
        "iterations": rollup.request_count,
        "total_tool_calls": rollup.total_tool_calls,
    }

    try:
        if _get_coordinator() is not None:
            _queue_user_request_update(user_request_id, **update_data)
        else:
            from matrx_ai.persistence import standalone_coordinator

            async with standalone_coordinator(
                reason="authoritative_user_request_rollup",
                request_id=user_request_id,
            ):
                _queue_user_request_update(user_request_id, **update_data)
    except Exception as exc:
        vcprint(
            f"[CX PERSISTENCE ROLLUP] authoritative UPDATE of cx_user_request "
            f"{user_request_id} failed ({type(exc).__name__}: {exc}); the per-turn "
            f"rollup value stands. cx_request rows remain the ground truth.",
            color="red",
        )


# --------------------------------------------------------------------------- #
# Phase 2 / Phase 3 helpers — cache_state refresh + streaming events          #
# --------------------------------------------------------------------------- #


def req_rows_available(req_list: list[dict[str, Any]]) -> bool:
    return bool(req_list) and isinstance(req_list[0], dict)


_DEFAULT_CACHE_TTLS_SECS: dict[str, int] = {
    "anthropic": 300,
    "openai": 300,
    "google": 300,
    "groq": 300,
    "xai": 300,
    "cerebras": 300,
    "together": 300,
    "fireworks": 300,
    "cohere": 300,
}


async def _refresh_cache_state(
    conversation_id: str,
    req_rows: list[dict[str, Any]],
    trim_summary: dict[str, Any] | None,
) -> None:
    """Update ``cx_conversation.cache_state`` after a completed request.

    Records the last response timestamp, provider, and estimated cache TTL
    so the next turn's trim_messages_context can decide whether the prompt
    cache is still alive (and worth protecting).

    ``cumulative_trimmable_chars`` and ``last_trim_at`` track the gate's
    history — when the gate fires (eligible_but_skipped_reason='cache_protect')
    we accumulate the est savings into a running tally; when a real trim
    runs, we reset to 0 and record the freed amount.
    """
    if not req_rows:
        return
    last_req = req_rows[-1]
    # ``cx_request.provider`` stores TokenUsage.api, the vendor tag
    # ("openai" / "groq" / "anthropic"). Renamed from the misnomer ``api_class``
    # in migration ai_035 (see /Users/armanisadeghi/code/common-docs/systems/agents/ai-models/DECISIONS.md).
    vendor_tag = (last_req.get("provider") or "").lower()
    provider_hint = _provider_from_vendor_tag(vendor_tag)

    # Pull existing state to preserve cumulative tally.
    try:
        existing = await _cxm().conversation.load_conversation_by_id(conversation_id)
        existing_state = dict(getattr(existing, "cache_state", None) or {})
    except Exception:
        existing_state = {}

    now_iso = datetime.now(UTC).isoformat()

    new_state: dict[str, Any] = {
        **existing_state,
        "last_response_at": now_iso,
        "last_provider": provider_hint,
        "last_model": last_req.get("ai_model") or "",
        "est_cache_ttl_secs": _DEFAULT_CACHE_TTLS_SECS.get(provider_hint, 300),
    }

    # Track cache-read tokens on the most recent iteration's raw_usage. Useful
    # for the FE gauge ("cache hit" indicator) and for future calibration.
    raw_usage = last_req.get("raw_usage") or {}
    cache_read = (
        raw_usage.get("cache_read_input_tokens")
        or raw_usage.get("cached_tokens")
        or (raw_usage.get("input_tokens_details", {}) or {}).get("cached_tokens")
        or raw_usage.get("cached_content_token_count")
        or 0
    )
    new_state["last_cache_read_tokens"] = int(cache_read or 0)

    # Trim accounting:
    if trim_summary:
        if trim_summary.get("blocks_rewritten", 0) > 0:
            # A trim actually ran — reset cumulative tally.
            new_state["cumulative_trimmable_chars"] = 0
            new_state["last_trim_at"] = now_iso
            new_state["last_trim_freed_chars"] = int(trim_summary.get("freed_chars", 0) or 0)
        elif trim_summary.get("eligible_but_skipped_reason") == "cache_protect":
            # Trim was eligible but skipped to protect cache — accumulate.
            gate = (trim_summary.get("policy") or {}).get("cache_gate") or {}
            est_tokens = int(gate.get("est_savings_tokens", 0) or 0)
            est_chars = int(est_tokens * 4)  # rough chars conversion for UI
            prior = int(existing_state.get("cumulative_trimmable_chars", 0) or 0)
            new_state["cumulative_trimmable_chars"] = prior + est_chars

    # Cache state update — coalesces with the prior cx_conversation UPDATE
    # at flush time. Keep the existing DB read above so prior turns'
    # cumulative_trimmable_chars are preserved across requests (each
    # request has its own coordinator; reads see last-flush state).
    # This updater runs after the completed request has been assembled.  A
    # delayed completion can inherit a RequestLane whose finalizer phase has
    # already ended; probing get_coordinator() there would manufacture a
    # terminal request coordinator and report persistence_after_lane_drain.
    # This write already has an explicit background-owner path, so terminal
    # inherited lanes must use it directly.
    lane = get_current_lane()
    lane_is_terminal = lane is not None and getattr(lane, "phase", None) != "active"
    if not lane_is_terminal and _get_coordinator() is not None:
        _queue_conversation_update(conversation_id, cache_state=new_state)
        return
    try:
        from matrx_ai.persistence import standalone_coordinator

        async with standalone_coordinator(
            reason="refresh_conversation_cache_state",
            conversation_id=conversation_id,
        ):
            _queue_conversation_update(conversation_id, cache_state=new_state)
    except Exception as upd_err:
        vcprint(
            f"[CX PERSISTENCE] cache_state UPDATE failed: {upd_err}",
            color="yellow",
        )


def _provider_from_vendor_tag(vendor_tag: str) -> str:
    """Normalize the usage vendor tag ('openai', 'gemini', 'groq', …) to a provider slug."""
    if not vendor_tag:
        return ""
    parts = vendor_tag.split("_")
    head = parts[0].lower()
    if head in {"anthropic"}:
        return "anthropic"
    if head in {"openai", "responses"}:
        return "openai"
    if head in {"google", "gemini"}:
        return "google"
    return head


async def _emit_context_state(
    emitter: Any,
    conversation_id: str,
    agg_input: int,
    agg_output: int,
    agg_cached: int,
    trim_summary: dict[str, Any] | None,
) -> None:
    """Emit context_state (+ context_trimmed when applicable) stream events.

    Phase 3. The FE listens for these in stream-parser → process-stream and
    routes them into context-state.slice for the Model Context tab. Best-effort.
    Payload schemas live in matrx_connect.context.events.
    """
    try:
        # Re-fetch the conversation to grab the freshly-written cache_state.
        # Cheap because the row was just touched above.
        #
        # Pending-aware: this best-effort telemetry read can race the
        # Coordinator's async fire-and-verify commit — the row is queued but not
        # yet visible to a committed read. A raced miss is NOT an error: skip
        # this turn quietly (the next turn's context_state carries current
        # state; the FE also gets the row via the record-update path). Matching
        # on the class NAME avoids a module-top matrx_orm import (boundary rule).
        try:
            conv = await _cxm().conversation.load_conversation_by_id(conversation_id)
        except Exception as read_exc:  # noqa: BLE001
            if type(read_exc).__name__ == "DoesNotExist":
                return
            raise
        cache_state = dict(getattr(conv, "cache_state", None) or {})

        # Pull rolled-up size metrics from the visible messages.
        messages = await _cxm().message.load_messages_by_conversation_id(conversation_id)
        visible_msgs = [
            m
            for m in messages
            if getattr(m, "is_visible_to_model", True)
            and getattr(m, "position", 0) >= 0
            and getattr(m, "deleted_at", None) is None
        ]
        total_chars = sum(
            (getattr(m, "content_chars", 0) or 0) + (getattr(m, "tool_results_chars", 0) or 0)
            for m in visible_msgs
        )

        # Use the typed emitter methods — they validate against the registered
        # payload class via build_event under the hood. The persist function
        # is wrapped in try/except so a malformed payload can't break the run.
        from matrx_connect.context.events import (
            ContextStatePayload,
            ContextTrimmedPayload,
        )

        now_iso = datetime.now(UTC).isoformat()
        state_payload = ContextStatePayload(
            conversation_id=conversation_id,
            last_request_input_tokens=int(agg_input or 0),
            last_request_cached_tokens=int(agg_cached or 0),
            last_request_output_tokens=int(agg_output or 0),
            total_chars_visible_to_model=int(total_chars),
            message_count_visible=len(visible_msgs),
            cache_state=cache_state,
            measured_at=now_iso,
        )
        await emitter.send_context_state(state_payload)

        # When a trim actually ran (or was eligible-but-skipped), emit a
        # second event with the audit detail.
        if trim_summary and (
            trim_summary.get("blocks_rewritten", 0) > 0
            or trim_summary.get("eligible_but_skipped_reason")
        ):
            trim_payload = ContextTrimmedPayload(
                conversation_id=conversation_id,
                trim_summary=trim_summary,
                measured_at=now_iso,
            )
            await emitter.send_context_trimmed(trim_payload)
    except Exception as exc:
        vcprint(
            f"[CX PERSISTENCE] _emit_context_state error: {exc}",
            color="yellow",
        )
