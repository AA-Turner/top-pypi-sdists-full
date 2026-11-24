"""Forcing-function: cx_request rows are queued only under a recorded cx_user_request.

Live 2026-10-30..11-02: protected-account refusals queued chat.request rows whose parent
INSERT ``ensure_user_request_exists`` had swallowed; every one burned five retries on
cx_request_user_request_id_fkey. "ensure returned" is not "the parent exists"."""

from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

import pytest

from matrx_ai.db import conversation_gate as gate
from matrx_ai.db import persistence


@pytest.fixture
def gate_wiring(monkeypatch):
    import matrx_ai.client_host as client_host

    rows: dict[str, object] = {}

    class _Requests:
        async def filter_user_requests(self, **kwargs):
            return [rows[kwargs["id"]]] if kwargs["id"] in rows else []

    monkeypatch.setattr(client_host, "get_conversation_store", lambda: None)
    monkeypatch.setattr(gate, "_cxm", lambda: SimpleNamespace(user_request=_Requests()))
    gate._ensured_request_ids.clear()
    yield rows, monkeypatch
    gate._ensured_request_ids.clear()


@pytest.mark.asyncio
async def test_a_swallowed_parent_insert_skips_the_children(gate_wiring):
    _rows, monkeypatch = gate_wiring

    async def ensure_that_swallows(request_id, user_id, **_kw):
        return None  # the gate logged its failure and returned, as it does

    monkeypatch.setattr(gate, "ensure_user_request_exists", ensure_that_swallows)
    ok = await persistence._request_rows_have_a_parent(str(uuid4()), SimpleNamespace(user_id=str(uuid4())))
    assert ok is False


@pytest.mark.asyncio
async def test_a_refused_parent_skips_the_children(gate_wiring):
    _rows, monkeypatch = gate_wiring

    async def ensure_that_refuses(request_id, user_id, **_kw):
        raise RuntimeError("protected_account_run_refused")

    monkeypatch.setattr(gate, "ensure_user_request_exists", ensure_that_refuses)
    ok = await persistence._request_rows_have_a_parent(str(uuid4()), SimpleNamespace(user_id=str(uuid4())))
    assert ok is False


@pytest.mark.asyncio
async def test_an_ensured_parent_keeps_the_children(gate_wiring):
    _rows, monkeypatch = gate_wiring

    async def ensure_that_queues(request_id, user_id, **_kw):
        gate._remember_ensured(request_id, gate._coord_scope_key())

    monkeypatch.setattr(gate, "ensure_user_request_exists", ensure_that_queues)
    ok = await persistence._request_rows_have_a_parent(str(uuid4()), SimpleNamespace(user_id=str(uuid4())))
    assert ok is True


@pytest.mark.asyncio
async def test_a_parent_from_another_process_keeps_the_children_without_a_user(gate_wiring):
    rows, _monkeypatch = gate_wiring
    request_id = str(uuid4())
    rows[request_id] = object()
    assert await persistence._request_rows_have_a_parent(request_id, None) is True
    assert await persistence._request_rows_have_a_parent(str(uuid4()), None) is False
