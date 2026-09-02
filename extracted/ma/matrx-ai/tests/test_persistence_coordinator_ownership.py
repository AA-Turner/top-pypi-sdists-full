"""Conversation persistence never writes through an unowned ORM Session."""

from __future__ import annotations

import ast
from contextlib import asynccontextmanager
from pathlib import Path
from types import SimpleNamespace

import pytest

import matrx_ai.client_host as client_host
import matrx_ai.db.persistence as persistence
import matrx_ai.persistence as persistence_api


class _PersistenceReached(RuntimeError):
    pass


@pytest.mark.asyncio
async def test_background_persist_enters_standalone_coordinator(monkeypatch) -> None:
    current = {"coordinator": None}
    scopes: list[dict[str, str | None]] = []

    @asynccontextmanager
    async def _standalone(**kwargs):
        scopes.append(kwargs)
        current["coordinator"] = object()
        try:
            yield current["coordinator"]
        finally:
            current["coordinator"] = None

    class _Completed:
        request = SimpleNamespace(
            request_id="11111111-1111-1111-1111-111111111111",
            conversation_id="22222222-2222-2222-2222-222222222222",
        )

        @staticmethod
        def to_storage_dict():
            raise _PersistenceReached

    monkeypatch.setattr(client_host, "get_conversation_store", lambda: None)
    monkeypatch.setattr(
        persistence,
        "_get_coordinator",
        lambda: current["coordinator"],
    )
    monkeypatch.setattr(persistence_api, "standalone_coordinator", _standalone)

    with pytest.raises(_PersistenceReached):
        await persistence.persist_completed_request(_Completed())

    assert scopes == [
        {
            "reason": "persist_completed_request",
            "request_id": "11111111-1111-1111-1111-111111111111",
            "conversation_id": "22222222-2222-2222-2222-222222222222",
        }
    ]


@pytest.mark.asyncio
async def test_terminal_inherited_lane_enters_standalone_before_owner_probe(monkeypatch) -> None:
    current = {"coordinator": None}
    scopes: list[dict[str, str | None]] = []

    @asynccontextmanager
    async def _standalone(**kwargs):
        scopes.append(kwargs)
        current["coordinator"] = object()
        try:
            yield current["coordinator"]
        finally:
            current["coordinator"] = None

    class _Completed:
        request = SimpleNamespace(
            request_id="11111111-1111-1111-1111-111111111111",
            conversation_id="22222222-2222-2222-2222-222222222222",
        )

        @staticmethod
        def to_storage_dict():
            raise _PersistenceReached

    owner_probes: list[object | None] = []

    def _owner():
        owner_probes.append(current["coordinator"])
        if current["coordinator"] is None:
            pytest.fail("terminal inherited lane must be isolated before owner probe")
        return current["coordinator"]

    monkeypatch.setattr(client_host, "get_conversation_store", lambda: None)
    monkeypatch.setattr(
        persistence,
        "get_current_lane",
        lambda: SimpleNamespace(phase="closed"),
    )
    monkeypatch.setattr(persistence, "_get_coordinator", _owner)
    monkeypatch.setattr(persistence_api, "standalone_coordinator", _standalone)

    with pytest.raises(_PersistenceReached):
        await persistence.persist_completed_request(_Completed())

    assert len(owner_probes) == 1
    assert owner_probes[0] is not None
    assert scopes == [
        {
            "reason": "persist_completed_request",
            "request_id": "11111111-1111-1111-1111-111111111111",
            "conversation_id": "22222222-2222-2222-2222-222222222222",
        }
    ]


def test_persistence_module_has_no_bare_session_write_fallback() -> None:
    tree = ast.parse(Path(persistence.__file__).read_text())
    bare_session_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "Session"
    ]
    assert bare_session_calls == []
