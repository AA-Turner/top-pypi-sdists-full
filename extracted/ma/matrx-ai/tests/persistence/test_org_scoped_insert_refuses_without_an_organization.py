"""FORCING TEST — an org-scoped INSERT with NO organization is REFUSED.

THE LAW (``common-docs/policies/context-is-carried-never-rebuilt.md``, rule 4):
below the boundary the organization is READ — off the carried context or off the
parent record — and an absent one is a refusal, never a quieter tenant.

Until 2026-09-17 ``_queue_or_drop`` left ``organization_id`` out of the payload
when neither the conversation nor the ambient context had one, and the
database's ``_stamp_org_default`` backstop filled it with the CREATOR's personal
organization. That is the same wrong-tenant defect as the measured ambient
bleed one layer down, except silent: the row exists, in a tenant nobody chose,
and every later read of the conversation it belongs to misses it.

The REAL Coordinator and the REAL queue door run; only the ambient context (the
boundary) is faked.
"""

from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

import pytest

ORG = "33333333-3333-4333-8333-333333333333"


class _MemoryMeta:
    primary_keys = ["id"]
    foreign_keys: dict = {}
    table_name = "agent_memory"
    db_schema = "chat"


class _PackageMemory:
    _meta = _MemoryMeta()


@pytest.fixture(autouse=True)
def _register():
    from matrx_ai.persistence.registry import override_table

    # SCOPED, never ``register_table`` (first-writer-wins would let this
    # stand-in own the real chat.agent_memory key for the whole process).
    with override_table("chat.agent_memory", _PackageMemory):
        yield


def _ambient(monkeypatch, organization_id: str | None) -> None:
    from matrx_ai.persistence import queue_helpers

    monkeypatch.setattr(
        queue_helpers,
        "_resolve_app_context",
        lambda: SimpleNamespace(
            organization_id=organization_id,
            request_id=str(uuid4()),
            user_id=str(uuid4()),
            conversation_id=None,
        ),
    )


def _queue(monkeypatch, organization_id: str | None):
    from matrx_ai.persistence.coordinator import Coordinator
    from matrx_ai.persistence.queue_helpers import _coordinator_cv, _queue_or_drop

    _ambient(monkeypatch, organization_id)
    coord = Coordinator(request_id=str(uuid4()), conversation_id=None)
    token = _coordinator_cv.set(coord)
    row_id = str(uuid4())
    try:
        _queue_or_drop(
            "chat.agent_memory",
            {"id": row_id, "summary": "remembered"},
            op_type="insert",
            primary_key=("id", row_id),
        )
        return coord, row_id
    finally:
        _coordinator_cv.reset(token)


def test_the_carried_organization_is_stamped_on_the_insert(monkeypatch):
    coord, row_id = _queue(monkeypatch, ORG)
    payloads = [op.payload for op in coord._session._ops if op.pk_value == row_id]
    assert payloads and payloads[0]["organization_id"] == ORG


def test_no_organization_anywhere_refuses_by_name(monkeypatch):
    with pytest.raises(ValueError) as exc:
        _queue(monkeypatch, None)
    message = str(exc.value)
    assert "chat.agent_memory" in message
    assert "org-scoped" in message
    # The remedy names where the organization comes from, and says plainly that
    # the database is never the one to guess it.
    assert "personal organization" in message
