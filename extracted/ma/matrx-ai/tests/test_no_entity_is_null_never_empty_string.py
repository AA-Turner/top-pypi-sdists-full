"""A context resolution with no entity binds NULL, never "" (live regression 2026-10-19).

``context.resolve_full_context(p_entity_id uuid, ...)``: the mandate Holder-input route resolves
scope-bound variables before any conversation exists and passed ``entity_id=""``, which the
database refused with ``invalid input syntax for type uuid: ""`` on every mandate door whose
Holder binds a scope value. NULL is the honest "no entity" and still resolves the selection.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai import context_engine


@pytest.mark.asyncio
async def test_an_empty_entity_id_reaches_the_database_as_null(monkeypatch: pytest.MonkeyPatch) -> None:
    sent: list[tuple[Any, ...]] = []

    async def fake_call_function(_db: Any, _schema: str, name: str, *args: Any, **_kw: Any) -> dict:
        sent.append((name, *args))
        return {}

    import matrx_orm

    monkeypatch.setattr(matrx_orm, "call_function", fake_call_function)
    monkeypatch.setattr(context_engine, "_resolve_context_database", lambda: "db")

    try:
        await context_engine.build_agent_context(
            user_id="87a6e699-3622-4869-8843-d0867456c0dd",
            entity_type="conversation",
            entity_id="",
            scope_ids=["9a4e5ff6-833a-4b6d-986b-26eaf3893e28"],
            organization_id="884d1ce8-7b49-4fba-a2f3-0f7dd7c83d4f",
            use_cache=False,
        )
    except Exception:
        pass  # only the bound arguments matter here; shaping an empty answer may raise
    calls = [c for c in sent if c[0] == "resolve_full_context"]
    assert calls, "resolve_full_context was never called"
    assert calls[0][3] is None, f"entity_id bound as {calls[0][3]!r}, must be None (SQL NULL)"
