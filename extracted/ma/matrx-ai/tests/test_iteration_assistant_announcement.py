"""Regression for FOUND_DEFECTS 2026-06-23 (conversation bcc588b6): an
assistant message persisted with MORE tool_uses than its adjacent tool message
answers — the surplus duplicated onto later turns.

Pinned root: the executor announced (record_reserved) ONLY the loop-start
first-assistant cx_message; iteration-2+ assistant rows were fresh-INSERTed by
``persist_completed_request`` silently. The client therefore knew exactly ONE
assistant message id per run, folded the WHOLE run's assembled content (every
iteration's text + tool_calls) onto it at stream end, and — when the content
carried an <artifact> block — persisted that union through the
``cx_message_set_content`` RPC, overwriting the first assistant row with
tool_calls belonging to later rows. (The overwritten original is archived in
the row's own ``content_history`` with reason 'artifact_materialization' —
that archive is the forensic proof.)

The server-side contract pinned here:
  1. EVERY fresh assistant cx_message INSERT is announced via the reservation
     tracker (role/position metadata), so the client's multi-reservation
     per-iteration partitioning applies — it never folds a multi-iteration
     run onto one row.
  2. The announced id is registered on the reservation channel
     (``state.reserved_message_ids``), so any re-persist of that position is
     an idempotent UPDATE, never a duplicate INSERT.
  3. role='tool' rows are NOT announced (the client sources tool data from
     cx_tool_call observability; message-row stubs would pollute the
     transcript).

The DB-side layer (``cx_message_set_content`` rejecting any tool_call-graph
change) lives in migration 0151 and is validated against the live DB.
"""

from __future__ import annotations

from typing import Any
from uuid import UUID, uuid4

import pytest

from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.message_config import ToolCallContent, ToolResultContent
from matrx_ai.config.unified_config import UnifiedResponse
from matrx_ai.db.message_positions import APPEND_MESSAGE_POSITION
from matrx_ai.orchestrator.execution_state import ExecutionState
from matrx_ai.orchestrator.executor import _append_partial_response
from matrx_ai.orchestrator.requests import AIMatrixRequest, CompletedRequest

CONVERSATION_ID = "11111111-1111-1111-1111-111111111111"
USER_ID = "22222222-2222-2222-2222-222222222222"
REQUEST_ID = "33333333-3333-3333-3333-333333333333"


def _is_uuid(value: Any) -> bool:
    try:
        UUID(str(value))
        return True
    except (ValueError, TypeError):
        return False


class _StubModelManager:
    async def load_model_get_string_uuid(self, name):
        return "44444444-4444-4444-4444-444444444444"


class _StubCoordinator:
    def queue(self, *a, **k):
        return ""


class _AsyncAnything:
    def __getattr__(self, name):
        return _AsyncAnything()

    async def __call__(self, *a, **k):
        return []


class _StubEmitter:
    async def send_record_reserved(self, payload):  # pragma: no cover - shape only
        return None


class _CapturingTracker:
    def __init__(self) -> None:
        self.reserved: list[dict[str, Any]] = []
        self.activated: list[str] = []

    async def reserve(
        self,
        emitter: Any,
        db_project: str,
        table: str,
        parent_refs: dict[str, str] | None = None,
        metadata: dict[str, Any] | None = None,
        record_id: str | None = None,
    ) -> str:
        record_id = record_id or str(uuid4())
        self.reserved.append(
            {
                "table": table,
                "record_id": record_id,
                "parent_refs": parent_refs or {},
                "metadata": metadata or {},
            }
        )
        return record_id

    async def mark_active(self, emitter: Any, table: str, record_id: str) -> None:
        self.activated.append(record_id)


class _StubAppContext:
    user_id = USER_ID
    conversation_id = CONVERSATION_ID
    store = True
    emitter = _StubEmitter()


def _build_two_iteration_completed() -> CompletedRequest:
    """The bcc588b6 shape, minimized: user(0) → assistant+tool_use(1) →
    tool(2) → final assistant(3). Position 1 is the loop-start reservation;
    positions 2 and 3 are fresh INSERTs at persist time."""
    messages = [
        UnifiedMessage(role="user", content=[TextContent(text="do the thing")]),
        UnifiedMessage(
            role="assistant",
            metadata={"provider_iteration": 1},
            content=[
                TextContent(text="working on it"),
                ToolCallContent(id="toolu_a", name="context_patch", arguments={"k": "v"}),
            ],
        ),
        UnifiedMessage(
            role="tool",
            content=[ToolResultContent(tool_use_id="toolu_a", content="patched")],
        ),
        UnifiedMessage(
            role="assistant",
            content=[TextContent(text="done")],
            metadata={"provider_iteration": 2},
        ),
    ]
    cfg = UnifiedConfig(model="claude-test", messages=MessageList(_messages=messages))
    req = AIMatrixRequest(
        conversation_id=CONVERSATION_ID,
        config=cfg,
        request_id=REQUEST_ID,
    )
    return CompletedRequest(
        request=req,
        iterations=2,
        final_response=UnifiedResponse(messages=[messages[-1]]),
        trigger_message_position=0,
        result_start_position=1,
        result_end_position=3,
    )


def test_partial_assistant_response_keeps_iteration_attribution():
    config = UnifiedConfig(
        model="claude-test",
        messages=MessageList(
            _messages=[UnifiedMessage(role="user", content=[TextContent(text="go")])]
        ),
    )
    request = AIMatrixRequest(
        conversation_id=CONVERSATION_ID,
        config=config,
        request_id=REQUEST_ID,
    )
    partial = UnifiedResponse(
        messages=[
            UnifiedMessage(role="assistant", content=[TextContent(text="partial")])
        ]
    )
    state = ExecutionState()
    state.iteration = 4

    updated = _append_partial_response(request, partial, state)

    assert updated.config.messages[-1].metadata["provider_iteration"] == 4


@pytest.fixture()
def persist_harness(monkeypatch):
    import matrx_ai.context.app_context as app_ctx_mod
    import matrx_ai.db.persistence as persistence_mod

    monkeypatch.setattr(app_ctx_mod, "get_app_context", lambda: _StubAppContext())
    monkeypatch.setattr(app_ctx_mod, "try_get_app_context", lambda: _StubAppContext())

    creates: list[dict[str, Any]] = []
    updates: list[tuple[str, dict[str, Any]]] = []
    request_creates: list[dict[str, Any]] = []
    tracker = _CapturingTracker()

    monkeypatch.setattr(persistence_mod, "ai_model_manager_instance", _StubModelManager())
    monkeypatch.setattr(persistence_mod, "_get_coordinator", lambda: _StubCoordinator())
    monkeypatch.setattr(
        persistence_mod, "_queue_message_create", lambda **kw: creates.append(kw) or ""
    )
    monkeypatch.setattr(
        persistence_mod, "_queue_message_update", lambda mid, **kw: updates.append((mid, kw)) or ""
    )
    monkeypatch.setattr(persistence_mod, "_queue_conversation_update", lambda cid, **kw: "")
    monkeypatch.setattr(
        persistence_mod,
        "_queue_request_create",
        lambda **kw: request_creates.append(kw) or "",
    )
    monkeypatch.setattr(persistence_mod, "_queue_user_request_update", lambda rid, **kw: "")

    async def _no_hide(*a, **k):
        return 0

    async def _no_backfill(*a, **k):
        return []

    async def _no_op(*a, **k):
        return None

    monkeypatch.setattr(persistence_mod, "_hide_superseded_failed_turns", _no_hide)
    monkeypatch.setattr(persistence_mod, "_backfill_tool_message", _no_backfill)
    monkeypatch.setattr(persistence_mod, "_refresh_cache_state", _no_op)
    monkeypatch.setattr(persistence_mod, "_emit_context_state", _no_op)
    monkeypatch.setattr(persistence_mod, "cxm", _AsyncAnything())
    monkeypatch.setattr(persistence_mod, "try_get_tracker", lambda: tracker)

    return persistence_mod, creates, updates, request_creates, tracker


@pytest.mark.asyncio
async def test_fresh_assistant_rows_are_announced_and_registered(persist_harness):
    persistence_mod, creates, updates, request_creates, tracker = persist_harness
    completed = _build_two_iteration_completed()

    state = ExecutionState()
    # Loop-start reservations: user trigger (0) and FIRST assistant (1) only —
    # exactly the live contract. Positions 2 (tool) and 3 (iteration-2
    # assistant) are unreserved.
    state.reserved_message_ids = {0: str(uuid4()), 1: str(uuid4())}

    await persistence_mod.persist_completed_request(
        completed, conversation_id=CONVERSATION_ID, state=state
    )

    # The iteration-2 assistant fresh INSERT was ANNOUNCED with its position...
    assistant_announcements = [
        r
        for r in tracker.reserved
        if r["table"] == "message" and r["metadata"].get("role") == "assistant"
    ]
    assert len(assistant_announcements) == 1, (
        "every fresh assistant cx_message INSERT must be announced — the client "
        "otherwise folds the whole run's content onto the single loop-start "
        "reservation (the bcc588b6 corruption)"
    )
    announcement = assistant_announcements[0]
    assert announcement["metadata"]["position"] == 3
    assert announcement["metadata"]["position_kind"] == "logical_index"
    assert announcement["parent_refs"]["conversation_id"] == CONVERSATION_ID
    assert _is_uuid(announcement["record_id"])
    assert announcement["record_id"] in tracker.activated

    # ...its id matches the queued INSERT...
    inserted_assistant_ids = {kw["id"] for kw in creates if kw.get("role") == "assistant"}
    assert announcement["record_id"] in inserted_assistant_ids
    assert all(row["position"] == APPEND_MESSAGE_POSITION for row in creates)

    # Updates target a row that already received its physical coordinate from
    # the INSERT trigger. A logical list index must never overwrite it.
    assert all("position" not in fields for _mid, fields in updates)

    # ...and it is registered on the reservation channel for idempotency.
    assert state.reserved_message_ids.get(3) == announcement["record_id"]

    assert [row["metadata"]["response_message_id"] for row in request_creates] == [
        state.reserved_message_ids[1],
        state.reserved_message_ids[3],
    ]


@pytest.mark.asyncio
async def test_request_cost_links_by_iteration_not_assistant_row_order(persist_harness):
    persistence_mod, _creates, _updates, request_creates, _tracker = persist_harness
    completed = _build_two_iteration_completed()
    synthetic = UnifiedMessage(
        role="assistant",
        content=[TextContent(text="handoff summary")],
        metadata={"source": "handoff"},
    )
    completed.request.config.messages._messages.insert(3, synthetic)
    completed.result_end_position = 4
    state = ExecutionState()
    state.reserved_message_ids = {0: str(uuid4()), 1: str(uuid4())}

    await persistence_mod.persist_completed_request(
        completed, conversation_id=CONVERSATION_ID, state=state
    )

    assert request_creates[0]["metadata"]["response_message_id"] == state.reserved_message_ids[1]
    assert request_creates[1]["metadata"]["response_message_id"] == state.reserved_message_ids[4]


@pytest.mark.asyncio
async def test_repersist_of_announced_position_updates_not_reinserts(persist_harness):
    """A retry / final pass that re-covers the same position must UPDATE the
    already-announced row, never INSERT a second one (idempotent-per-position)."""
    persistence_mod, creates, updates, _request_creates, tracker = persist_harness
    completed = _build_two_iteration_completed()

    state = ExecutionState()
    state.reserved_message_ids = {0: str(uuid4()), 1: str(uuid4())}

    await persistence_mod.persist_completed_request(
        completed, conversation_id=CONVERSATION_ID, state=state
    )
    announced_id = state.reserved_message_ids[3]
    inserts_after_first = [kw for kw in creates if kw.get("id") == announced_id]
    assert len(inserts_after_first) == 1

    # Second pass over the same window (e.g. a stateless final persist).
    await persistence_mod.persist_completed_request(
        completed, conversation_id=CONVERSATION_ID, state=state
    )

    inserts_after_second = [kw for kw in creates if kw.get("id") == announced_id]
    assert len(inserts_after_second) == 1, (
        "re-persisting an announced position must not INSERT a duplicate row"
    )
    assert announced_id in {mid for mid, _ in updates}, (
        "the re-persist must ride the UPDATE path against the announced id"
    )


@pytest.mark.asyncio
async def test_tool_rows_are_not_announced(persist_harness):
    persistence_mod, creates, updates, _request_creates, tracker = persist_harness
    completed = _build_two_iteration_completed()

    state = ExecutionState()
    state.reserved_message_ids = {0: str(uuid4()), 1: str(uuid4())}

    await persistence_mod.persist_completed_request(
        completed, conversation_id=CONVERSATION_ID, state=state
    )

    tool_announcements = [
        r for r in tracker.reserved if r["metadata"].get("role") == "tool"
    ]
    assert not tool_announcements, (
        "role='tool' cx_message rows must not be announced — the client reads "
        "tool data from cx_tool_call observability, and message-row stubs "
        "pollute the transcript"
    )
