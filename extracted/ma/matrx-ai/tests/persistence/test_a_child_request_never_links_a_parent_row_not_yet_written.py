"""A child request's parent link names a row that is in the database when the child commits.

Live 2026-11-03 (write_failure 561ff84e and siblings): a parent request's
``chat.user_request`` row was only QUEUED in its Coordinator (it lands at the
parent's turn commit), the conversation gate remembered it anyway, and
``lineage_columns`` linked a child to it. The child committed first through its
own Coordinator → ``user_request_parent_request_id_fkey``; the replay inserted the
child later as ``pending`` after its completion had already run against no row →
abandoned by the watchdog (440 open).

The rule: a remembered parent queued in ANOTHER coordinator is committed first
(``Coordinator.commit_queued_now``); when that cannot be done, no link is written
(the root still is). A row whose insert failed is never remembered as a parent.
"""

from __future__ import annotations

import asyncio
import contextlib
import weakref
from types import SimpleNamespace
from typing import Any

import pytest

import matrx_ai.persistence.coordinator as coord_mod
from matrx_ai.db import conversation_gate as gate
from matrx_ai.persistence.coordinator import Coordinator
from matrx_ai.persistence.registry import register_table

ORG = "11111111-1111-4111-8111-111111111111"
PARENT = "22222222-2222-4222-8222-222222222222"
CHILD = "44444444-4444-4444-8444-444444444444"


class _Meta:
    primary_keys = ["id"]
    foreign_keys: dict = {}
    table_name = "cx_parent_link"
    db_schema = "public"


class _Model:
    _meta = _Meta()

    def __init__(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


register_table("public.cx_parent_link", _Model)


@contextlib.asynccontextmanager
async def _fake_transaction(*args: Any, **kwargs: Any):
    yield


@pytest.fixture
def db(monkeypatch: pytest.MonkeyPatch):
    import matrx_orm.core.transaction as txn_mod

    monkeypatch.setattr(txn_mod, "transaction", _fake_transaction)
    coord_mod._inflight_commits = 0
    committed: dict[str, dict] = {}

    async def execute_tiers(tiers):
        written = 0
        for tier in tiers:
            for op in tier:
                committed[op.pk_value] = dict(op.payload)
                written += 1
        return written

    monkeypatch.setattr("matrx_orm.session.flush.execute_tiers", execute_tiers)
    monkeypatch.setattr("matrx_orm.session.session.execute_tiers", execute_tiers)
    yield committed
    coord_mod._inflight_commits = 0


@pytest.fixture
def gate_state(monkeypatch: pytest.MonkeyPatch, db: dict[str, dict]):
    """The gate reads ``chat.user_request`` from the fake database above."""

    class Requests:
        async def filter_user_requests(self, id: str) -> list[Any]:  # noqa: A002
            row = db.get(id)
            return [SimpleNamespace(**row)] if row else []

    monkeypatch.setattr(gate, "_cxm", lambda: SimpleNamespace(user_request=Requests()))
    monkeypatch.setattr(gate, "_request_org_memo", type(gate._request_org_memo)())
    monkeypatch.setattr(gate, "_request_org_scope", {})
    return db


def _child_lineage() -> Any:
    return gate.lineage_columns(
        own_request_id=CHILD, parent_request_id=PARENT, root_request_id=PARENT, organization_id=ORG
    )


@pytest.mark.asyncio
async def test_a_parent_queued_in_another_coordinator_is_committed_before_the_child_links_it(
    gate_state: dict[str, dict], monkeypatch: pytest.MonkeyPatch
) -> None:
    db = gate_state
    parent_coord = Coordinator(request_id=PARENT, conversation_id="c-parent")
    parent_coord.queue("public.cx_parent_link", {"id": PARENT, "organization_id": ORG})
    gate._remember_request_org(PARENT, ORG, weakref.ref(parent_coord))
    assert PARENT not in db  # only queued: the child must not name it yet

    child_coord = Coordinator(request_id=CHILD, conversation_id="c-child")
    monkeypatch.setattr(gate, "_get_active_lane_coordinator", lambda: child_coord)

    got = await asyncio.wait_for(_child_lineage(), 5)

    assert got == {"root_request_id": PARENT, "parent_request_id": PARENT}
    assert PARENT in db, "the child was linked to a parent row that was not written"
    # The parent's own barrier still accounts for the commit it did not fire itself.
    await asyncio.wait_for(parent_coord.check_pending(), 5)
    await asyncio.wait_for(parent_coord.finalize(reason="request_final_commit"), 5)


@pytest.mark.asyncio
async def test_a_parent_that_cannot_be_committed_is_not_linked(
    gate_state: dict[str, dict], monkeypatch: pytest.MonkeyPatch
) -> None:
    parent_coord = Coordinator(request_id=PARENT, conversation_id="c-parent")
    parent_coord.queue("public.cx_parent_link", {"id": PARENT, "organization_id": ORG})
    parent_coord._dropped_ops_count = 1  # its queue already lost a write: nothing it holds is provable
    gate._remember_request_org(PARENT, ORG, weakref.ref(parent_coord))
    monkeypatch.setattr(gate, "_get_active_lane_coordinator", lambda: None)

    assert await _child_lineage() == {"root_request_id": PARENT}


@pytest.mark.asyncio
async def test_a_parent_queued_in_the_same_coordinator_links_without_an_early_commit(
    gate_state: dict[str, dict], monkeypatch: pytest.MonkeyPatch
) -> None:
    db = gate_state
    coord = Coordinator(request_id=PARENT, conversation_id="c-one")
    coord.queue("public.cx_parent_link", {"id": PARENT, "organization_id": ORG})
    gate._remember_request_org(PARENT, ORG, weakref.ref(coord))
    monkeypatch.setattr(gate, "_get_active_lane_coordinator", lambda: coord)

    assert await _child_lineage() == {"root_request_id": PARENT, "parent_request_id": PARENT}
    assert PARENT not in db  # same session, parent first: no early commit needed


@pytest.mark.asyncio
async def test_a_failed_parent_insert_is_never_a_parent(gate_state: dict[str, dict]) -> None:
    gate._remember_request_org(PARENT, ORG)
    gate._forget_request_org(PARENT)  # what _create_user_request does when its insert failed
    assert await _child_lineage() == {"root_request_id": PARENT}
