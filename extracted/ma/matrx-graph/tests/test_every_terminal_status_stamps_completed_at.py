"""Every RunStore path that writes a terminal status stamps completed_at (review 2026-10-19).

Fails when: a mark_* method writes status completed/failed/errored/cancelled without completed_at —
mark_errored did, and 786 of 789 errored runs had no end time, so the chat never showed them as failed.
The methods are discovered, not listed: a new terminal writer is checked the day it is added.
"""

from __future__ import annotations

import inspect
from types import SimpleNamespace
from typing import Any
from uuid import uuid4

import pytest

from matrx_graph.db import run_store as module

TERMINAL = {"completed", "failed", "errored", "cancelled"}


def _args_for(method: Any) -> dict[str, Any]:
    kwargs: dict[str, Any] = {}
    for name, param in inspect.signature(method).parameters.items():
        if name in {"self", "run_id"} or param.default is not inspect.Parameter.empty:
            continue
        kwargs[name] = {"error": {"message": "x"}, "output": {}, "steps_executed": 0}.get(name, None)
    return kwargs


def _mark_methods() -> list[str]:
    return [n for n, m in inspect.getmembers(module.RunStore, inspect.iscoroutinefunction) if n.startswith("mark_")]


@pytest.mark.asyncio
@pytest.mark.parametrize("name", _mark_methods())
async def test_terminal_writer_stamps_completed_at(monkeypatch: pytest.MonkeyPatch, name: str) -> None:
    writes: list[dict[str, Any]] = []

    class Model:
        async def update_where(self, filters: dict[str, Any], **updates: Any) -> SimpleNamespace:
            writes.append(updates)
            return SimpleNamespace(rows_affected=1)

    async def no_announce(*_a: Any, **_k: Any) -> None:
        return None

    monkeypatch.setattr(module, "get_model", lambda _name: Model())
    monkeypatch.setattr(module, "_announce_settled", no_announce)
    store = module.RunStore()
    method = getattr(store, name)
    await method(str(uuid4()), **_args_for(method))
    for updates in writes:
        status = updates.get("status")
        status = getattr(status, "value", status)
        if status in TERMINAL:
            assert updates.get("completed_at") is not None, f"{name} writes status={status} without completed_at"


@pytest.mark.asyncio
@pytest.mark.parametrize("to_status", sorted(TERMINAL))
async def test_transition_to_a_terminal_status_stamps_completed_at(monkeypatch: pytest.MonkeyPatch, to_status: str) -> None:
    """transition() gives runs up as failed/cancelled (wf_cancel_reconciliation, held_step_resume)."""
    writes: list[dict[str, Any]] = []

    class Model:
        async def update_where(self, filters: dict[str, Any], **updates: Any) -> SimpleNamespace:
            writes.append(updates)
            return SimpleNamespace(rows_affected=1)

    monkeypatch.setattr(module, "get_model", lambda _name: Model())
    await module.RunStore().transition(str(uuid4()), from_statuses=("running",), to_status=to_status)
    assert writes and writes[0].get("completed_at") is not None


def test_the_guard_sees_every_terminal_writer() -> None:
    assert {"mark_completed", "mark_failed", "mark_errored", "mark_cancelled", "mark_parked_cancelled"} <= set(_mark_methods())
