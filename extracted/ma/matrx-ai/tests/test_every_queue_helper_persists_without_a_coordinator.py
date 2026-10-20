"""No queue_* helper ever drops a write (defect 66, class fix).

A send with no visible write coordinator (every programmatic door: /try, mandate_call, run_mandate, the
workflow step) used to have its queued write DROPPED with a console "DATA LOSS" line: the conversation
kept no frozen wire swaps, so the stored snapshot could never be restored "as sent". Every queue_*
helper funnels through ``_queue_or_drop``; with no coordinator it must hand the write to the
coordinator-less writer, and that writer must record its own failure.
"""

from __future__ import annotations

import inspect
import uuid
from types import SimpleNamespace
from typing import Any

import pytest

import matrx_ai.persistence.queue_helpers as qh

CONV = str(uuid.uuid4())
USER_REQUEST = str(uuid.uuid4())
ORG = str(uuid.uuid4())

#: One minimal call per public queue_* helper. A new helper must be added here (census test below).
CALLS: dict[str, Any] = {
    "queue_conversation_create": lambda f: f(id=CONV, created_by=ORG, organization_id=ORG),
    "queue_conversation_metadata_patch": lambda f: f(CONV, {"k": "v"}),
    "queue_conversation_update": lambda f: f(CONV, title="t"),
    "queue_user_request_create": lambda f: f(id=USER_REQUEST, organization_id=ORG),
    "queue_user_request_update": lambda f: f(USER_REQUEST, status="x"),
    "queue_message_create": lambda f: f(id=str(uuid.uuid4()), conversation_id=CONV, content=[]),
    "queue_message_update": lambda f: f(str(uuid.uuid4()), status="x"),
    "queue_request_create": lambda f: f(id=str(uuid.uuid4()), user_request_id=USER_REQUEST, conversation_id=CONV),
    "queue_request_update": lambda f: f(str(uuid.uuid4()), status="x"),
    "queue_tool_call_create": lambda f: f(id=str(uuid.uuid4()), conversation_id=CONV),
    "queue_tool_call_update": lambda f: f(str(uuid.uuid4()), status="x"),
    "queue_request_snapshot_create": lambda f: f(id=str(uuid.uuid4()), user_request_id=USER_REQUEST, conversation_id=CONV),
    "queue_tool_trace_create": lambda f: f(id=str(uuid.uuid4()), conversation_id=CONV),
    "queue_om_memory_create": lambda f: f(id=str(uuid.uuid4()), conversation_id=CONV),
    "queue_om_memory_update": lambda f: f(str(uuid.uuid4()), status="x"),
    "queue_om_event_create": lambda f: f(id=str(uuid.uuid4()), conversation_id=CONV),
    "queue_agent_memory_create": lambda f: f(id=str(uuid.uuid4())),
    "queue_agent_memory_update": lambda f: f(str(uuid.uuid4()), status="x"),
    "queue_agent_memory_delete": lambda f: f(str(uuid.uuid4())),
}


def _public_helpers() -> list[str]:
    return sorted(n for n, o in vars(qh).items() if n.startswith("queue_") and inspect.isfunction(o) and o.__module__ == qh.__name__)


def test_every_queue_helper_is_covered_here() -> None:
    assert _public_helpers() == sorted(CALLS), "add the new queue_* helper to CALLS"


@pytest.mark.parametrize("name", sorted(CALLS))
async def test_a_queue_helper_with_no_coordinator_persists_its_write(name: str, monkeypatch: pytest.MonkeyPatch) -> None:
    ctx = SimpleNamespace(
        organization_id=ORG, user_id=ORG, request_id=USER_REQUEST, conversation_id=CONV, store=True, metadata={}
    )
    monkeypatch.setattr(qh, "get_coordinator", lambda: None)
    monkeypatch.setattr(qh, "_resolve_app_context", lambda: ctx)
    monkeypatch.setattr(qh, "conversation_organization", lambda _cid: ORG)
    written: list[tuple[str, str]] = []
    scheduled: list[Any] = []

    async def _writer(table: str, payload: dict[str, Any], *, op_type: str, **_: Any) -> None:
        written.append((table, op_type))

    monkeypatch.setattr(qh, "_persist_without_coordinator", _writer)
    monkeypatch.setattr(qh, "detached_task", lambda coro, **_: scheduled.append(coro))
    CALLS[name](getattr(qh, name))
    for coro in scheduled:
        await coro
    assert len(written) == 1, f"{name}: the write was dropped with no coordinator ({written})"


async def test_the_coordinator_less_writer_records_its_own_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """If even the standalone write fails, a recorded error row is filed, never just a console line."""
    import contextlib

    import matrx_connect.streaming.error_capture as ec

    captured: list[dict[str, Any]] = []

    async def _capture(exc: BaseException, **kw: Any) -> None:
        captured.append(kw)

    @contextlib.asynccontextmanager
    async def _broken(**_: Any):
        raise RuntimeError("database unreachable")
        yield  # pragma: no cover

    monkeypatch.setattr(ec, "capture_error", _capture)
    monkeypatch.setattr(qh, "standalone_coordinator", _broken)
    monkeypatch.setattr(qh, "_resolve_app_context", lambda: None)
    await qh._persist_without_coordinator(
        "chat.message", {"id": "m1"}, op_type="update", primary_key=("id", "m1"), depends_on=()
    )
    assert [c["kind"] for c in captured] == ["write_without_coordinator_failed"]


# ── no event loop (a worker thread, a script): the write still lands or its failure is recorded ──


def _call_from_a_thread_with_no_loop(monkeypatch: pytest.MonkeyPatch, writer: Any, spill: Any) -> str:
    import threading

    ctx = SimpleNamespace(organization_id=ORG, user_id=ORG, request_id=USER_REQUEST, conversation_id=CONV, store=True, metadata={})
    monkeypatch.setattr(qh, "get_coordinator", lambda: None)
    monkeypatch.setattr(qh, "_resolve_app_context", lambda: ctx)
    monkeypatch.setattr(qh, "conversation_organization", lambda _cid: ORG)
    monkeypatch.setattr(qh, "_persist_without_coordinator", writer)
    monkeypatch.setattr(qh, "_spill_write_failure", spill)
    out: list[str] = []
    t = threading.Thread(target=lambda: out.append(qh.queue_conversation_metadata_patch(CONV, {"k": "v"})))
    t.start()
    t.join(10)
    assert out, "the call from a thread with no loop never returned"
    return out[0]


def test_a_queue_call_from_a_thread_with_no_loop_persists_the_write(monkeypatch: pytest.MonkeyPatch) -> None:
    written: list[str] = []

    async def _writer(table: str, payload: dict[str, Any], *, op_type: str, **_: Any) -> bool:
        written.append(table)
        return True

    got = _call_from_a_thread_with_no_loop(monkeypatch, _writer, lambda *a, **k: pytest.fail("spilled"))
    assert written == ["chat.conversation"], "the write was not made before the call returned"
    assert got == "written-without-coordinator"


def test_a_failed_write_from_a_thread_with_no_loop_is_spilled_for_replay(monkeypatch: pytest.MonkeyPatch) -> None:
    spilled: list[str] = []

    async def _writer(table: str, payload: dict[str, Any], *, op_type: str, **_: Any) -> bool:
        return False

    def _spill(table: str, payload: dict[str, Any], **kw: Any) -> bool:
        spilled.append(table)
        return True

    got = _call_from_a_thread_with_no_loop(monkeypatch, _writer, _spill)
    assert spilled == ["chat.conversation"] and got == "spilled-without-coordinator"


def test_the_real_spill_writes_a_replayable_failure_row(monkeypatch: pytest.MonkeyPatch, tmp_path: Any) -> None:
    import json

    monkeypatch.setenv("MATRX_SPILL_DIR", str(tmp_path))
    monkeypatch.setattr(qh, "_resolve_app_context", lambda: None)
    from db.models.chat import (
        Conversation,  # the real model (this package's conftest stubs the registry)
    )

    monkeypatch.setattr(qh, "get_model", lambda _t: Conversation)
    ok = qh._spill_write_failure(
        "chat.conversation", {"metadata": {"k": "v"}}, op_type="update", primary_key=("id", CONV), error="boom"
    )
    files = list(tmp_path.glob("*.json"))
    assert ok and len(files) == 1, "nothing was spilled"
    row = json.loads(files[0].read_text())
    assert row["table_target"] == "chat.conversation" and row["op_type"] == "update" and "boom" in row["error_text"]
