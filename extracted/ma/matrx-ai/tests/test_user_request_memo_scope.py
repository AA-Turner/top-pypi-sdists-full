"""Forcing-function: the ensure_user_request_exists memo must be COORDINATOR-SCOPED.

The 2026-07-13 blank-title podcast class: the podcast pipeline fans out the
script and metadata sub-agents concurrently (asyncio.create_task). Each becomes
a forked child agent with its OWN WriteCoordinator, but both SHARE the parent
request_id. The process-global "ensured" memo was a bare exists-flag set the
instant the FIRST sub-agent QUEUED (not committed) the parent cx_user_request
into its own Session. The sibling then hit the memo and SKIPPED queuing the
parent into ITS Session — so it flushed a cx_request whose user_request_id had
no parent row → asyncpg ForeignKeyViolationError cx_request_user_request_id_fkey
(non-fatal, but the metadata stage never committed → empty episode title).

Gut check: if the memo ignores scope, `test_sibling_coordinator_does_not_hit`
fails — coordinator B would skip its own ensure and re-orphan the cx_request.
"""

from __future__ import annotations

from uuid import uuid4

import pytest

from matrx_ai.db import conversation_gate as gate


@pytest.fixture(autouse=True)
def _clean_memo_and_no_store(monkeypatch):
    gate._ensured_request_ids.clear()

    async def _no_store(request_id, user_id):
        return False  # aidream server: no ConversationStore → real gate path

    monkeypatch.setattr(gate, "_store_pending_user_request", _no_store)

    # No parent row exists on DB read → every non-hit falls through to create.
    class _FakeUR:
        async def filter_user_requests(self, id):  # noqa: A002 - mirrors real kwarg
            return []

    monkeypatch.setattr(gate, "_cxm", lambda: type("M", (), {"user_request": _FakeUR()})())
    monkeypatch.setattr(gate, "try_get_tracker", lambda: None)
    yield
    gate._ensured_request_ids.clear()


def _spy_creates(monkeypatch):
    creates: list[str] = []

    async def _spy(*, request_id, user_id):
        creates.append(request_id)

    monkeypatch.setattr(gate, "_create_user_request", _spy)
    return creates


@pytest.mark.asyncio
async def test_sibling_coordinator_does_not_hit(monkeypatch):
    """Two concurrent children (distinct coordinators) sharing one request_id
    must EACH queue the parent into their own Session — the memo entry one wrote
    is not trusted by the other."""
    creates = _spy_creates(monkeypatch)
    rid, uid = str(uuid4()), str(uuid4())

    coord_a, coord_b = object(), object()
    current = {"c": coord_a}
    monkeypatch.setattr(gate, "_get_coordinator", lambda: current["c"])

    # Child A ensures under coordinator A → queues its own parent INSERT.
    await gate.ensure_user_request_exists(rid, uid)
    # Sibling B ensures the SAME request_id under coordinator B → must NOT hit
    # A's memo entry; it queues its OWN parent INSERT (FK-safe in B's Session).
    current["c"] = coord_b
    await gate.ensure_user_request_exists(rid, uid)

    assert creates == [rid, rid], (
        "sibling coordinator skipped queuing the parent cx_user_request — "
        "cx_request would orphan (cx_request_user_request_id_fkey)"
    )


@pytest.mark.asyncio
async def test_same_coordinator_hits_memo(monkeypatch):
    """Re-ensure on the SAME coordinator is a memo hit — no redundant create
    (the hot-path optimization the memo exists for is preserved)."""
    creates = _spy_creates(monkeypatch)
    rid, uid = str(uuid4()), str(uuid4())

    coord = object()
    monkeypatch.setattr(gate, "_get_coordinator", lambda: coord)

    await gate.ensure_user_request_exists(rid, uid)
    await gate.ensure_user_request_exists(rid, uid)

    assert creates == [rid], "same-coordinator re-ensure must not re-create"


@pytest.mark.asyncio
async def test_durable_entry_trusted_by_any_scope(monkeypatch):
    """A row ensured OUT of request (no coordinator → committed durably) is
    trusted by any later coordinator — the boundary-prep → executor fast path."""
    creates = _spy_creates(monkeypatch)
    rid, uid = str(uuid4()), str(uuid4())

    current = {"c": None}  # no coordinator → durable
    monkeypatch.setattr(gate, "_get_coordinator", lambda: current["c"])

    await gate.ensure_user_request_exists(rid, uid)  # durable create
    current["c"] = object()  # now inside some request coordinator
    await gate.ensure_user_request_exists(rid, uid)  # must hit the durable memo

    assert creates == [rid], "durable memo entry must be trusted by a later coordinator"
