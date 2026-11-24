"""A helper is saved when it starts (CGU-M3 P-014 / P-022, lead ruling 2026-11-04).

A child run owns its own Coordinator, and its first commit came only at its
first turn barrier — after its first model call. A one-turn helper therefore
wrote its conversation row at the END, and the person saw no sidebar row and
no running dot while it worked.

Two layers, each proven here:
1. the gate writes a helper's row born RUNNING (``last_request_status`` =
   ``pending``, ``last_request_id`` = the helper's request), which the sidebar
   draws as the running dot;
2. the executor FIRES that row (with the reserved message rows) through the
   helper's own Coordinator before the first model call — the same
   fire-and-verify path; the first barrier's ``check_pending`` verifies it.

A top-level chat is untouched by both: it has its own start claim and its
first barrier already follows the reservations.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from uuid import uuid4

import pytest

import matrx_ai.orchestrator.executor as executor_mod
from matrx_ai.config import MessageList, UnifiedConfig
from matrx_ai.db import conversation_gate as gate
from matrx_ai.orchestrator.requests import AIMatrixRequest

PARENT = "6b7d1d36-6d0b-4c6e-9a5e-2f4c8f0d1a11"
HELPER_REQUEST = "7c1e2f3a-4b5c-4d6e-8f70-81a2b3c4d5e6"


# ── layer 1: the gate ────────────────────────────────────────────────────────


def _wire_gate(monkeypatch) -> list[dict]:
    queued: list[dict] = []

    class _Coordinator:
        def set_correlation(self, **_kw):
            return None

        async def finalize(self, *, reason):
            return None

    async def _verified(parent, _child):
        return parent

    monkeypatch.setattr(gate, "try_get_tracker", lambda: None)
    monkeypatch.setattr(gate, "_get_coordinator", lambda: _Coordinator())
    monkeypatch.setattr(gate, "_get_active_lane_coordinator", lambda: _Coordinator())
    monkeypatch.setattr(
        gate,
        "_cxm",
        lambda: SimpleNamespace(conversation=SimpleNamespace(filter_conversations=_none)),
    )
    monkeypatch.setattr(gate, "_queue_conversation_create", lambda **kw: queued.append(kw))
    monkeypatch.setattr(
        gate,
        "stamp_org_id",
        lambda row, _org: row.setdefault("organization_id", "55555555-5555-4555-8555-555555555555"),
    )
    monkeypatch.setattr(gate, "resolve_parent_conversation_lineage", _verified)
    gate._known_conversation_ids.clear()
    return queued


async def _none(**_kw):
    return []


async def _ensure(monkeypatch, *, parent: str | None) -> dict:
    from matrx_connect import AppContext
    from matrx_connect.context.app_context import clear_app_context, set_app_context
    from matrx_connect.emitters.console_emitter import ConsoleEmitter

    queued = _wire_gate(monkeypatch)
    ctx = AppContext(
        emitter=ConsoleEmitter("t", accumulate=False),
        conversation_type="subagent" if parent else "chat",
        is_internal_agent=bool(parent),
        parent_conversation_id=parent,
        request_id=HELPER_REQUEST,
    )
    token = set_app_context(ctx)
    try:
        await gate.ensure_conversation_exists(
            str(uuid4()), str(uuid4()), parent_conversation_id=parent
        )
    finally:
        clear_app_context(token)
    return queued[0]


@pytest.mark.asyncio
async def test_a_helpers_row_is_born_running(monkeypatch):
    row = await _ensure(monkeypatch, parent=PARENT)
    assert row.get("last_request_status") == gate.CONVERSATION_START_CLAIM_STATUS, (
        "a helper's conversation row was written with no running status — the sidebar "
        "shows no dot while it works (P-014)"
    )
    assert row.get("last_request_id") == HELPER_REQUEST


@pytest.mark.asyncio
async def test_a_row_with_no_parent_carries_no_claim_from_this_door(monkeypatch):
    row = await _ensure(monkeypatch, parent=None)
    assert "last_request_status" not in row


# ── layer 2: the executor fires the helper's rows before the first model call ─


class _Emitter:
    async def send_info(self, *a, **k):
        return None

    async def send_phase(self, *a, **k):
        return None

    async def send_data(self, *a, **k):
        return None

    async def send_chunk(self, *a, **k):
        return None

    async def send_end(self, *a, **k):
        return None

    async def fatal_error(self, *a, **k):
        return None

    def reset_turn_text(self):
        return None

    def get_turn_text(self):
        return ""


class _Tracker:
    async def reserve(self, *a, **k):
        return None

    async def mark_active(self, *a, **k):
        return None

    def register_existing(self, *a, **k):
        return None


class _RecordingCoordinator:
    def __init__(self, log: list[str]) -> None:
        self.log = log

    def queue(self, *a, **k):
        return ""

    async def acquire_commit_slot(self, *a, **k):
        return None

    def commit_async(self, *, reason: str = "turn_commit"):
        self.log.append(f"commit:{reason}")

    async def check_pending(self, *a, **k):
        return None

    async def finalize(self, *a, **k):
        return None

    async def drain_and_confirm(self, *a, **k):
        return []

    async def seal(self, *a, **k):
        return None


class _Stop(Exception):
    pass


async def _run(monkeypatch, *, parent: str | None) -> list[str]:
    log: list[str] = []
    coord = _RecordingCoordinator(log)

    class _Ctx:
        conversation_id = "11111111-1111-4111-8111-111111111111"
        user_id = "22222222-2222-4222-8222-222222222222"
        parent_conversation_id = parent
        request_id = HELPER_REQUEST
        store = True
        debug = False
        snapshot = False
        metadata: dict[str, Any] = {}
        emitter = _Emitter()

    import matrx_ai.persistence.queue_helpers as qh

    monkeypatch.setattr(qh, "queue_message_create", lambda **kw: "msg-id")
    monkeypatch.setattr(qh, "get_coordinator", lambda: coord)

    async def _noop(*a, **k):
        return None

    monkeypatch.setattr(executor_mod, "ensure_conversation_exists", _noop)
    monkeypatch.setattr(executor_mod, "ensure_user_request_exists", _noop)
    monkeypatch.setattr(executor_mod, "get_tracker", lambda: _Tracker())
    monkeypatch.setattr(executor_mod, "get_app_context", lambda: _Ctx())

    messages = MessageList()
    messages.append_or_extend_user_text("Find the three cheapest flights to Lisbon.")
    req = AIMatrixRequest(
        conversation_id=_Ctx.conversation_id,
        config=UnifiedConfig(model="claude-haiku-4-5", messages=messages),
        request_id=_Ctx.request_id,
    )

    class _Client:
        async def execute(self, *a, **k):
            log.append("model_call")
            raise _Stop()

    from matrx_ai.orchestrator.execution_state import ExecutionState

    with pytest.raises(BaseException):
        await executor_mod._execute_until_complete_inner(
            exec_ctx=_Ctx(),
            state=ExecutionState(),
            initial_request=req,
            client=_Client(),
            max_iterations=1,
            max_retries_per_iteration=0,
        )
    return log


@pytest.mark.asyncio
async def test_a_helpers_rows_are_fired_before_its_first_model_call(monkeypatch):
    log = await _run(monkeypatch, parent=PARENT)
    assert "commit:child_run_start_commit" in log, (
        f"a helper's rows waited for its first turn barrier (after the model call): {log}"
    )
    assert "model_call" in log
    assert log.index("commit:child_run_start_commit") < log.index("model_call")


@pytest.mark.asyncio
async def test_a_top_level_chat_takes_no_extra_commit(monkeypatch):
    log = await _run(monkeypatch, parent=None)
    assert "commit:child_run_start_commit" not in log
