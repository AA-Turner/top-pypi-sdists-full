"""A bulk member add defers the store's reachability refresh; the flush settles it.

Live 2026-11-15: the platform catalog sync filed hundreds of library docs into one
14k-member store. Every ``add_member`` fired the association trigger, which re-derived
the WHOLE store's reachability under its advisory lock, so the upserts ran past the 5 s
lock timeout and the 10 s statement timeout — 30 ``db_statement_canceled`` rows on
``rag.data_store_members`` in 11 minutes. ``defer_reachability=True`` sets migration
1381's transaction-local switch in the SAME transaction as the upsert, and
``flush_deferred_reachability`` settles the pending containers afterwards.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any

import pytest

import matrx_rag.data_stores as data_stores_mod
from matrx_orm.exceptions import LockContentionError


class _Stores:
    async def get_or_none(self, *, id: str, deleted_at__isnull: bool) -> Any:  # noqa: A002
        return type("Store", (), {"id": id, "kind": "default", "organization_id": "org-1"})()


@pytest.fixture
def seams(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    events: list[str] = []

    class _Members:
        async def upsert(self, data: dict[str, Any], *, on_conflict: list[str], update_fields: list[str]) -> None:
            events.append("upsert")

    def _model(name: str, schema: str | None = None) -> Any:
        return _Stores() if name == "DataStores" else _Members()

    @asynccontextmanager
    async def _transaction(*, database: str):
        events.append("begin")
        yield
        events.append("commit")

    async def _set_local_gucs(gucs: dict[str, str], *, connection: Any = None) -> None:
        events.extend(f"guc:{k}={v}" for k, v in gucs.items())

    @asynccontextmanager
    async def _actor(database: str):
        yield

    monkeypatch.setattr(data_stores_mod, "get_db_model", _model)
    monkeypatch.setattr("matrx_orm.core.transaction.transaction", _transaction)
    monkeypatch.setattr("matrx_orm.core.transaction.set_local_gucs", _set_local_gucs)
    monkeypatch.setattr("matrx_orm.actor_named_for_write", _actor)
    return events


async def _add(defer: bool) -> None:
    await data_stores_mod.add_member(
        store_id="s", source_kind="library_doc", source_id="d", added_by="u", defer_reachability=defer
    )


@pytest.mark.asyncio
async def test_a_deferred_add_sets_the_switch_in_the_upserts_transaction(seams: list[str]) -> None:
    await _add(True)
    assert seams == ["begin", "guc:platform.reachability_defer=on", "upsert", "commit"]


@pytest.mark.asyncio
async def test_an_ordinary_add_refreshes_inline(seams: list[str]) -> None:
    await _add(False)
    assert seams == ["upsert"], "a normal add never defers: a new member must convey access at once"


@pytest.mark.asyncio
async def test_the_flush_runs_until_drained_and_rides_out_a_lock_collision(monkeypatch: pytest.MonkeyPatch) -> None:
    answers: list[Any] = [5, LockContentionError("collision"), 5, 2]
    calls: list[tuple[str, str, int]] = []

    async def _call_function(database: str, schema: str, function: str, *args: Any, **_: Any) -> Any:
        calls.append((schema, function, args[0]))
        answer = answers.pop(0)
        if isinstance(answer, Exception):
            raise answer
        return answer

    async def _no_sleep(_: float) -> None:
        return None

    monkeypatch.setattr("matrx_orm.call_function", _call_function)
    monkeypatch.setattr("asyncio.sleep", _no_sleep)

    assert await data_stores_mod.flush_deferred_reachability() == 12
    assert all(c[:2] == ("platform", "reachability_flush") for c in calls)
    assert len(calls) == 4 and not answers
