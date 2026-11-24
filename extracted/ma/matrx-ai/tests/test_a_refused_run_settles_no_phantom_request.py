"""Forcing-function: a run refused before its request row exists is RECORDED as a failed request.

Live 2026-10-30..11-02: refused runs (protected account, required input missing, workflow
tracking open failed, platform-tenant refusal) queued ``status='failed'`` UPDATEs and
``chat.request`` children for a ``chat.user_request`` that was never written — "UPDATE
matched no row" and ``cx_request_user_request_id_fkey`` lost writes. Ruling 2026-11-02: the
refused run CREATES its row with status ``failed`` and the refusal, stamped with the
organization its context carries — never the refused platform tenant, never a chosen one.
A recorded request still settles by UPDATE; a row queued into a DEAD coordinator whose
address the live one reuses is not trusted as queued."""

from __future__ import annotations

import gc
from contextlib import asynccontextmanager, contextmanager
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from matrx_ai.db import conversation_gate as gate

ORG = "77777777-7777-4777-8777-777777777777"
SYSTEM_ORG = "00000000-0000-4000-8000-000000000001"


class _Requests:
    model = object()

    def __init__(self, rows: dict[str, object]):
        self.rows = rows
        self.updates: list[tuple[str, dict]] = []
        self.creates: list[dict] = []

    async def filter_user_requests(self, **kwargs):
        row = self.rows.get(kwargs["id"])
        return [row] if row is not None else []

    async def update_user_request(self, rid, **kwargs):
        self.updates.append((rid, kwargs))

    async def create_user_request(self, **kwargs):
        self.creates.append(kwargs)


class _Coordinator:
    """Weak-referenceable, like the real Coordinator (``__weakref__`` slot)."""


@pytest.fixture
def wired(monkeypatch):
    import matrx_orm

    import matrx_ai.context.app_context as context
    from matrx_ai.context.app_context import AppContext

    queued_updates: list[tuple[str, dict]] = []
    queued_creates: list[dict] = []
    state = {
        "coord": None,
        "requests": _Requests({}),
        "ctx": AppContext(emitter=None, user_id=str(uuid4()), organization_id=ORG),
    }

    @asynccontextmanager
    async def session():
        yield

    @contextmanager
    def allow_direct(*_a, **_k):
        yield

    monkeypatch.setattr(context, "try_get_app_context", lambda: state["ctx"])
    monkeypatch.setattr(gate, "try_get_tracker", lambda: None)
    monkeypatch.setattr(gate, "resolve_parent_conversation_lineage", AsyncMock(return_value=None))
    monkeypatch.setattr(gate, "_get_active_lane_coordinator", lambda: state["coord"])
    monkeypatch.setattr(gate, "_cxm", lambda: SimpleNamespace(user_request=state["requests"]))
    monkeypatch.setattr(gate, "_queue_user_request_update", lambda rid, **kw: queued_updates.append((rid, kw)))
    monkeypatch.setattr(gate, "_queue_user_request_create", lambda **kw: queued_creates.append(kw))
    monkeypatch.setattr(matrx_orm, "Session", session)
    monkeypatch.setattr(matrx_orm, "allow_direct_coordinator_write", allow_direct)
    import matrx_ai.client_host as client_host

    monkeypatch.setattr(client_host, "get_conversation_store", lambda: None)
    gate._ensured_request_ids.clear()
    yield state, queued_updates, queued_creates
    gate._ensured_request_ids.clear()


def _created(state, queued_creates, in_lane):
    return queued_creates if in_lane else state["requests"].creates


@pytest.mark.asyncio
@pytest.mark.parametrize("in_lane", [True, False])
async def test_a_refused_run_is_recorded_as_a_failed_request(wired, in_lane):
    state, queued_updates, queued_creates = wired
    state["coord"] = _Coordinator() if in_lane else None
    request_id = str(uuid4())
    refusal = "protected_account_run_refused: Not run"

    await gate.update_user_request_status(request_id, "failed", error=refusal)

    created = _created(state, queued_creates, in_lane)
    assert len(created) == 1, "the refused run must CREATE its request row"
    row = created[0]
    assert (row["status"], row["error"], row["organization_id"]) == ("failed", refusal, ORG)
    assert row.get("completed_at") is not None
    # No UPDATE that would match nothing.
    assert queued_updates == [] and state["requests"].updates == []


@pytest.mark.asyncio
@pytest.mark.parametrize("in_lane", [True, False])
async def test_a_platform_tenant_refusal_writes_nothing(wired, monkeypatch, in_lane):
    """The refused org is never the row's org, and nothing chooses another one."""
    from matrx_connect.context.provenance import ATTESTED_ORIGIN_CLASSES
    from matrx_orm.session import fallback

    state, queued_updates, queued_creates = wired
    state["coord"] = _Coordinator() if in_lane else None
    state["ctx"] = SimpleNamespace(
        user_id=str(uuid4()),
        organization_id=fallback.SYSTEM_ORGANIZATION_ID,
        origin_class=next(iter(ATTESTED_ORIGIN_CLASSES)),
        request_id="r",
    )
    monkeypatch.setattr(gate, "_stamp_origin", lambda *a, **k: None)
    monkeypatch.setattr(gate, "_stamp_attribution", lambda *a, **k: None)
    monkeypatch.setattr(gate, "_stamp_agent_refs", lambda *a, **k: None)
    monkeypatch.setattr(gate, "_stamp_launch_binding", lambda *a, **k: None)
    monkeypatch.setattr(gate, "_run_identity_metadata", lambda *_a: {})
    monkeypatch.setattr(gate, "_stamp_lineage", AsyncMock(return_value=None))

    await gate.update_user_request_status(str(uuid4()), "failed", error="platform_tenant_not_for_people")

    assert _created(state, queued_creates, in_lane) == []
    assert queued_updates == [] and state["requests"].updates == []


@pytest.mark.asyncio
async def test_no_carried_organization_writes_nothing(wired):
    state, queued_updates, queued_creates = wired
    state["coord"] = _Coordinator()
    state["ctx"] = SimpleNamespace(user_id=str(uuid4()), organization_id=None)

    await gate.update_user_request_status(str(uuid4()), "failed", error="x")

    assert queued_creates == [] and queued_updates == []


@pytest.mark.asyncio
@pytest.mark.parametrize("in_lane", [True, False])
async def test_a_recorded_request_still_settles(wired, in_lane):
    state, queued_updates, queued_creates = wired
    state["coord"] = _Coordinator() if in_lane else None
    request_id = str(uuid4())
    state["requests"].rows[request_id] = object()

    await gate.update_user_request_status(request_id, "failed", error="boom")

    written = queued_updates if in_lane else state["requests"].updates
    assert written == [(request_id, {"status": "failed", "error": "boom"})]
    assert _created(state, queued_creates, in_lane) == []


@pytest.mark.asyncio
async def test_a_request_queued_this_turn_settles_without_a_read(wired):
    """The INSERT is only queued (not yet in the database): the memo answers, the UPDATE coalesces."""
    state, queued_updates, _queued_creates = wired
    state["coord"] = _Coordinator()
    request_id = str(uuid4())
    gate._remember_ensured(request_id, gate._coord_scope_key())

    async def no_read(**_kw):
        raise AssertionError("a queued request must not be re-read")

    state["requests"].filter_user_requests = no_read
    await gate.update_user_request_status(request_id, "failed")

    assert queued_updates == [(request_id, {"status": "failed"})]


@pytest.mark.asyncio
async def test_a_row_queued_into_a_dead_coordinator_is_not_trusted(wired):
    """``id(coord)`` memo keys were reused by the next coordinator after GC: the row queued
    into the dead one never landed, yet read as queued into the live one."""
    state, queued_updates, queued_creates = wired
    dead = _Coordinator()
    state["coord"] = dead
    request_id = str(uuid4())
    gate._remember_ensured(request_id, gate._coord_scope_key())
    state["coord"] = None
    del dead
    gc.collect()
    state["coord"] = _Coordinator()  # may well land at the dead one's address

    await gate.update_user_request_status(request_id, "failed", error="refused")

    assert [row["status"] for row in queued_creates] == ["failed"]
    assert queued_updates == []
