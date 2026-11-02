"""``add_member``'s membership upsert must run inside a named actor.

Live defect, 2026-09-19 (aidream ``VERIFICATION.md`` §16, same class as
``docproc.processed_documents``): ``rag.data_store_members`` carries an AFTER
INSERT/UPDATE trigger (``sync_data_store_member_association``) that writes
``platform.associations`` as a side effect of this very upsert. Neither
``add_member`` nor ``DataStoreMembers.upsert`` is instrumented for that,
because ``data_store_members`` itself carries no actor requirement — only the
downstream ``platform.associations`` row does, and a table's own trigger is
invisible to matrx-orm's ``write_needs_named_actor`` check. Wrapping the upsert
in ``matrx_orm.actor_named_for_write`` closes it: nothing declared here is a
per-call-site string — the fallback name comes from the calling module via the
seam's own registry (``matrx_orm.write_actor.writing_system``).

No real database: this fakes the two seams the fix touches
(``get_db_model``, ``actor_named_for_write``) and asserts the upsert happens
INSIDE the named-actor block, which is what determines whether the trigger's
INSERT sees a declared ``app.actor_system`` GUC.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any

import pytest
import matrx_rag.data_stores as data_stores_mod


class _FakeDataStores:
    """No library-store branch exercised here — ``kind`` is a plain store."""

    async def get_or_none(
        self, *, id: str, deleted_at__isnull: bool
    ) -> Any:  # noqa: A002 - matches the real signature
        assert deleted_at__isnull is True
        return type("Store", (), {"id": id, "kind": "default", "organization_id": "org-1"})()


class _FakeDataStoreMembers:
    def __init__(self) -> None:
        self.upsert_calls: list[dict[str, Any]] = []

    async def upsert(self, data: dict[str, Any], *, on_conflict: list[str], update_fields: list[str]) -> None:
        self.upsert_calls.append(data)


@pytest.fixture
def fakes(monkeypatch: pytest.MonkeyPatch) -> tuple[_FakeDataStores, _FakeDataStoreMembers, list[str]]:
    stores = _FakeDataStores()
    members = _FakeDataStoreMembers()
    events: list[str] = []

    def _fake_get_db_model(name: str, schema: str | None = None) -> Any:
        if name == "DataStores":
            return stores
        if name == "DataStoreMembers":
            return members
        raise AssertionError(f"unexpected get_db_model({name!r})")

    @asynccontextmanager
    async def _fake_actor_named_for_write(database: str):
        events.append(f"enter:{database}")
        yield
        events.append("exit")

    monkeypatch.setattr(data_stores_mod, "get_db_model", _fake_get_db_model)
    monkeypatch.setattr("matrx_orm.actor_named_for_write", _fake_actor_named_for_write)
    return stores, members, events


@pytest.mark.asyncio
async def test_add_member_upsert_runs_inside_the_named_actor_block(fakes) -> None:
    _stores, members, events = fakes

    await data_stores_mod.add_member(
        store_id="store-1",
        source_kind="cld_file",
        source_id="file-1",
        added_by="user-1",
    )

    assert members.upsert_calls, "the membership row must still be written"
    assert events[0].startswith("enter:"), (
        "the upsert must run inside actor_named_for_write, or the trigger that "
        "cascades into platform.associations sees no declared actor"
    )
    assert events[-1] == "exit"
