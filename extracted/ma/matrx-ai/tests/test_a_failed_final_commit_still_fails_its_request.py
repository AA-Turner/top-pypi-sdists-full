"""Forcing-function: a request whose final commit fails is NEVER left 'pending'.

Live 2026-11-04 (confidential turns, user requests 62e0d24e / 864c580e): the closing
``chat.user_request`` UPDATE rode the final-commit batch, ``chat.refuse_sealed_content``
refused it, the Coordinator went ERRORED, and every write queued afterwards (the error
path's ``failed`` status included) was captured as ``queue_in_phase_errored`` — never
written. The request sat 'pending' until the lifecycle watchdog abandoned it.

Two halves:
  * ``settle_user_request_failed_after_barrier`` writes the terminal status on its OWN
    fresh write (never through the errored Coordinator), through the sealed funnel, and
    falls back to the status alone when the error text is refused;
  * ``_finalize_and_persist`` calls it when the final commit fails.

Gut check: remove the call from the executor's except branch, or route the write through
the coordinator, and these fail.
"""

from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

import pytest
from matrx_utils.source_guard import stable_source

from matrx_ai.db import conversation_gate as gate


class _FakeUserRequestManager:
    def __init__(self, refuse_error_column: bool = False):
        self.refuse_error_column = refuse_error_column
        self.updates: list[tuple[str, dict]] = []
        self.model = object()

    async def update_user_request(self, request_id, **kwargs):
        if self.refuse_error_column and "error" in kwargs:
            raise RuntimeError("23514 confidential conversation: error may not be stored")
        self.updates.append((request_id, kwargs))


@pytest.fixture
def harness(monkeypatch):
    import contextlib

    import matrx_orm

    manager = _FakeUserRequestManager()
    monkeypatch.setattr(gate, "_cxm", lambda: SimpleNamespace(user_request=manager))
    monkeypatch.setattr("matrx_ai.client_host.get_conversation_store", lambda: None)

    @contextlib.contextmanager
    def _allow(*args, **kwargs):
        yield

    @contextlib.asynccontextmanager
    async def _session(*args, **kwargs):
        yield

    monkeypatch.setattr(matrx_orm, "allow_direct_coordinator_write", _allow)
    monkeypatch.setattr(matrx_orm, "Session", _session)

    # An ERRORED coordinator is live in scope: anything queued through it is captured,
    # never written. The settle must not go there.
    def _no_queue(*args, **kwargs):
        raise AssertionError("the failed status was queued onto the errored Coordinator")

    monkeypatch.setattr(gate, "_queue_user_request_update", _no_queue)
    monkeypatch.setattr(gate, "_get_active_lane_coordinator", lambda: object())

    ctx = SimpleNamespace(sealed_conversation_id=None, sealed_keeps_content=False)
    monkeypatch.setattr("matrx_ai.context.app_context.try_get_app_context", lambda: ctx)
    return SimpleNamespace(manager=manager, ctx=ctx)


@pytest.mark.asyncio
async def test_failed_final_commit_marks_the_request_failed_on_its_own_write(harness):
    rid = str(uuid4())
    assert await gate.settle_user_request_failed_after_barrier(rid, "final save failed") is True
    assert len(harness.manager.updates) == 1
    written_id, payload = harness.manager.updates[0]
    assert written_id == rid
    assert payload["status"] == "failed"
    assert payload["error"] == "final save failed"
    assert payload["completed_at"] is not None
    assert "metadata" not in payload, "the settle must never re-send the refused metadata"


@pytest.mark.asyncio
async def test_a_sealed_request_gets_its_status_without_error_text(harness):
    harness.ctx.sealed_conversation_id = str(uuid4())
    rid = str(uuid4())
    assert await gate.settle_user_request_failed_after_barrier(rid, "final save failed") is True
    _, payload = harness.manager.updates[0]
    assert payload["status"] == "failed"
    assert "error" not in payload, "chat.refuse_sealed_content refuses any error text on a sealed row"


@pytest.mark.asyncio
async def test_a_refused_error_text_still_lands_the_status(harness):
    harness.manager.refuse_error_column = True
    rid = str(uuid4())
    assert await gate.settle_user_request_failed_after_barrier(rid, "boom") is True
    assert [p["status"] for _, p in harness.manager.updates] == ["failed"]


def test_the_final_commit_failure_path_settles_the_request():
    from matrx_ai.orchestrator import executor

    src = stable_source(executor._finalize_and_persist)
    final = src.find('finalize(reason="request_final_commit")')
    handler = src.find("except Exception as _history_exc:", final)
    settle = src.find("settle_user_request_failed_after_barrier(", handler)
    reraise = src.find("raise", settle)
    assert final != -1 and handler != -1
    assert settle != -1, (
        "a failed final commit must mark its chat.user_request 'failed' by its own write — "
        "otherwise it stays 'pending' until the lifecycle watchdog"
    )
    assert settle < reraise, "settle before the failure propagates"
