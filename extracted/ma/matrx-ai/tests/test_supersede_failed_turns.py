"""A successful turn collapses the prior FAILED attempts out of the user's view.

While a turn keeps failing, the user sees the failures. The moment a real
response lands, ``_hide_superseded_failed_turns`` flips the prior failed rows to
is_visible_to_user=False (kept for the record; already hidden from the agent).
Net model visibility is unchanged, so no cache bust is needed.
"""

# ruff: noqa: I001 -- executor must load before persistence (see import note below).

from __future__ import annotations

from contextlib import asynccontextmanager
from types import SimpleNamespace

import pytest

# Load the orchestrator → persistence chain in the app's natural order first;
# importing persistence directly at collection trips a pre-existing
# persistence↔executor circular import.
import matrx_ai.orchestrator.executor as _executor_mod  # noqa: F401,E402
import matrx_ai.persistence as persistence_api  # noqa: E402
import matrx_ai.db._registry as _registry_mod  # noqa: E402
import matrx_ai.db.persistence as persist_mod  # noqa: E402


class _FakeMsgModel:
    def __init__(self, rows):
        self._rows = rows

    async def filter_items(self, **kw):
        return [
            r
            for r in self._rows
            if getattr(r, "status", None) == kw.get("status")
            and getattr(r, "is_visible_to_user", None) == kw.get("is_visible_to_user")
            and str(getattr(r, "conversation_id", None)) == str(kw.get("conversation_id"))
        ]


class _FakeMessageMgr:
    def __init__(self):
        self.updates: list[tuple] = []

    async def update_message(self, mid, **fields):
        self.updates.append((mid, fields))


class _FakeCxm:
    def __init__(self):
        self.message = _FakeMessageMgr()


def _rows():
    return [
        SimpleNamespace(id="f1", conversation_id="C", status="failed", is_visible_to_user=True, position=14),
        SimpleNamespace(id="f2", conversation_id="C", status="failed", is_visible_to_user=True, position=14),
        # active turn — not a failure, must be left alone.
        SimpleNamespace(id="ok", conversation_id="C", status="active", is_visible_to_user=True, position=14),
        # a failure BEYOND the success position — not superseded by this success.
        SimpleNamespace(id="future", conversation_id="C", status="failed", is_visible_to_user=True, position=20),
    ]


def _install_standalone_coordinator(monkeypatch, queued):
    current = {"coordinator": None}

    @asynccontextmanager
    async def _scope(**_kwargs):
        current["coordinator"] = object()
        try:
            yield current["coordinator"]
        finally:
            current["coordinator"] = None

    monkeypatch.setattr(
        persist_mod,
        "_get_coordinator",
        lambda: current["coordinator"],
    )
    monkeypatch.setattr(persistence_api, "standalone_coordinator", _scope)
    monkeypatch.setattr(
        persist_mod,
        "_queue_message_update",
        lambda mid, **fields: queued.append((mid, fields)),
    )


@pytest.mark.asyncio
async def test_hides_prior_failed_turns_at_or_before_position(monkeypatch):
    fake_model = _FakeMsgModel(_rows())
    fake_cxm = _FakeCxm()
    queued: list[tuple] = []
    monkeypatch.setattr(_registry_mod, "get_model", lambda name: fake_model)
    monkeypatch.setattr(persist_mod, "cxm", fake_cxm)
    _install_standalone_coordinator(monkeypatch, queued)

    hidden = await persist_mod._hide_superseded_failed_turns("C", up_to_position=14)

    assert hidden == 2
    assert {u[0] for u in queued} == {"f1", "f2"}
    assert fake_cxm.message.updates == []
    for _mid, fields in queued:
        # hidden from user AND (defensively) from model; net model visibility unchanged.
        assert fields == {"is_visible_to_user": False, "is_visible_to_model": False}


@pytest.mark.asyncio
async def test_noop_when_no_failed_turns(monkeypatch):
    rows = [SimpleNamespace(id="ok", conversation_id="C", status="active", is_visible_to_user=True, position=3)]
    fake_cxm = _FakeCxm()
    queued: list[tuple] = []
    monkeypatch.setattr(_registry_mod, "get_model", lambda name: _FakeMsgModel(rows))
    monkeypatch.setattr(persist_mod, "cxm", fake_cxm)
    _install_standalone_coordinator(monkeypatch, queued)

    hidden = await persist_mod._hide_superseded_failed_turns("C", up_to_position=99)

    assert hidden == 0
    assert fake_cxm.message.updates == []
    assert queued == []


@pytest.mark.asyncio
async def test_uses_coordinator_queue_when_in_request(monkeypatch):
    queued: list[tuple] = []
    fake_cxm = _FakeCxm()  # its update_message must NOT be called on the coord path
    monkeypatch.setattr(_registry_mod, "get_model", lambda name: _FakeMsgModel(_rows()))
    monkeypatch.setattr(persist_mod, "cxm", fake_cxm)
    monkeypatch.setattr(persist_mod, "_get_coordinator", lambda: object())
    monkeypatch.setattr(persist_mod, "_queue_message_update", lambda mid, **f: queued.append((mid, f)))

    hidden = await persist_mod._hide_superseded_failed_turns("C", up_to_position=14)

    assert hidden == 2
    assert {q[0] for q in queued} == {"f1", "f2"}
    assert fake_cxm.message.updates == []  # queued, not direct
