"""The merge-field producer sees the RUN's organization on a brand-new conversation.

THE DEFECT (clone + live, 2026-09-30). On turn one the conversation's row is still queued, so
``resolve_full_context`` answers a ``context`` map with NO ``organization_id``. The host filled
the run's organization in AFTER ``build_agent_context`` returned (active_selection, "KD-1") —
but the merge-field producer runs INSIDE it, so every first turn was refused ("scope names no
organization"), fell back to the direct tier split, cost ~8 s and wrote a
``context_resolver_failed`` row (15 on live in 24 h).

RED on the old engine: the producer received ``{}`` as its scope (``organization_id`` absent).
GREEN: ``build_agent_context(organization_id=...)`` carries it into the scope first.
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

from matrx_ai.context_engine import build_agent_context, configure_context_resolver

RUN_ORG = "f980f202-0e4e-4e39-8411-facae6fab50e"


@pytest.fixture
def first_turn_rpc(monkeypatch):
    """The RPC's real first-turn answer: no organization in its context map."""

    async def fake_call_function(*_args: Any, **_kwargs: Any) -> dict[str, Any]:
        return {"variables": {}, "context": {}, "scope_labels": {}, "cell_values": {}}

    monkeypatch.setattr("matrx_ai.context_engine._resolve_context_database", lambda: "test")
    monkeypatch.setattr("matrx_orm.call_function", fake_call_function)
    monkeypatch.setattr("matrx_ai.context_engine._path_chooser", None)


@pytest.fixture
def producer_sees():
    seen: list[dict[str, Any]] = []

    async def producer(**kwargs: Any) -> dict[str, dict[str, Any]]:
        seen.append(dict(kwargs["scope"]))
        return {"direct": {}, "tool_accessible": {}, "searchable": {}}

    configure_context_resolver(producer)
    yield seen
    configure_context_resolver(None)


def _build(**kw: Any):
    return asyncio.run(
        build_agent_context(
            "87a6e699-3622-4869-8843-d0867456c0dd",
            "conversation",
            "00000000-0000-4000-8000-000000000001",
            entity_is_new=True,
            use_cache=False,
            **kw,
        )
    )


def test_the_producer_receives_the_run_organization_on_turn_one(first_turn_rpc, producer_sees):
    ctx = _build(organization_id=RUN_ORG)
    assert producer_sees == [{"organization_id": RUN_ORG}]
    assert ctx.scope.get("organization_id") == RUN_ORG


def test_no_organization_is_invented_when_the_run_carries_none(first_turn_rpc, producer_sees):
    _build()
    assert producer_sees == [{}]  # nothing filled: the producer names the gap itself


def test_an_organization_the_resolver_named_is_never_replaced(monkeypatch, producer_sees):
    async def named(*_a: Any, **_k: Any) -> dict[str, Any]:
        return {"variables": {}, "context": {"organization_id": "the-entitys-org"},
                "scope_labels": {}, "cell_values": {}}

    monkeypatch.setattr("matrx_ai.context_engine._resolve_context_database", lambda: "test")
    monkeypatch.setattr("matrx_orm.call_function", named)
    monkeypatch.setattr("matrx_ai.context_engine._path_chooser", None)
    _build(organization_id=RUN_ORG)
    assert producer_sees == [{"organization_id": "the-entitys-org"}]
