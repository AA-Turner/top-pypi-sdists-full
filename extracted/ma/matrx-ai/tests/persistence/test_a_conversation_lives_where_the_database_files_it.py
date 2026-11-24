"""FORCING TEST — a conversation born where the database files rows elsewhere lives THERE, and so do its children.

Live 2026-11-20 03:18Z: an administrator's trial run (aidream ``runtime/trial_run.py``) ran a Run Typed Agent step
switched into a person's organization (``data.in_organization``). The database trigger ``platform._stamp_actor``
filed the new ``chat.conversation`` in the trial's FILING organization, but matrx-ai's child-row registry remembered
the step's organization — so every ``chat.message`` / ``chat.request`` / ``chat.request_snapshot`` of the turn was
stamped with the step's organization and refused ``org_foreign_to_parent``: 44 lost writes, 11 lost turns.

The host now names that filing organization (``row_filing_organization`` seam). The REAL create guard, the REAL queue
doors and a REAL Coordinator run; the assertions read the organization off the queued ops.
"""

from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

import pytest

from matrx_ai import _ext
from matrx_ai.db import conversation_gate as gate

STEP_ORG = "33333333-3333-4333-8333-333333333333"  # the organization the step switched into
FILING_ORG = "44444444-4444-4444-8444-444444444444"  # where the database files every new row


class _MessageMeta:
    primary_keys = ["id"]
    foreign_keys: dict = {}
    table_name = "message"
    db_schema = "chat"


class _ConversationMeta(_MessageMeta):
    table_name = "conversation"


class _PackageMessage:
    _meta = _MessageMeta()


class _PackageConversation:
    _meta = _ConversationMeta()


@pytest.fixture(autouse=True)
def _clean(monkeypatch):
    from matrx_ai.persistence import queue_helpers
    from matrx_ai.persistence.conversation_org import reset_conversation_organizations
    from matrx_ai.persistence.registry import override_table

    reset_conversation_organizations()
    gate._known_conversation_ids.clear()
    monkeypatch.setattr(
        queue_helpers,
        "_resolve_app_context",
        lambda: SimpleNamespace(
            organization_id=STEP_ORG, request_id=str(uuid4()), user_id=str(uuid4()), conversation_id=None
        ),
    )
    with override_table("chat.message", _PackageMessage), override_table("chat.conversation", _PackageConversation):
        yield
    _ext._registry.pop("row_filing_organization", None)
    reset_conversation_organizations()
    gate._known_conversation_ids.clear()


def _file_rows_in(org: str | None) -> None:
    _ext._registry["row_filing_organization"] = lambda: org


def _queued_org(coord, row_id: str) -> str | None:
    for op in coord._session._ops:
        if op.pk_value == row_id:
            return (op.payload or {}).get("organization_id")
    raise AssertionError(f"no queued op for row {row_id}")


def _turn(monkeypatch) -> tuple[object, str, str, list]:
    from matrx_ai.persistence import queue_helpers
    from matrx_ai.persistence.coordinator import Coordinator
    from matrx_ai.persistence.queue_helpers import (
        _coordinator_cv,
        queue_conversation_create,
        queue_message_create,
    )

    bleeds: list = []
    monkeypatch.setattr(queue_helpers, "_capture_child_org_bleed", lambda **kw: bleeds.append(kw))
    conversation_id, message_id = str(uuid4()), str(uuid4())
    coord = Coordinator(request_id=str(uuid4()), conversation_id=conversation_id)
    token = _coordinator_cv.set(coord)
    try:
        queue_conversation_create(id=conversation_id, organization_id=STEP_ORG, created_by=str(uuid4()))
        queue_message_create(
            id=message_id,
            conversation_id=conversation_id,
            role="user",
            position=0,
            status="active",
            content=[{"type": "text", "text": "hi"}],
        )
    finally:
        _coordinator_cv.reset(token)
    return coord, conversation_id, message_id, bleeds


def test_the_create_guard_names_the_filing_organization():
    _file_rows_in(FILING_ORG)
    conversation_id = str(uuid4())
    kwargs = {"organization_id": STEP_ORG}
    gate._require_create_organization(kwargs, conversation_id)
    gate.mark_conversation_known(conversation_id, organization_id=kwargs["organization_id"])

    from matrx_ai.persistence.conversation_org import conversation_organization

    assert kwargs["organization_id"] == FILING_ORG
    assert conversation_organization(conversation_id) == FILING_ORG


def test_a_born_conversation_and_its_message_live_in_the_filing_organization(monkeypatch):
    _file_rows_in(FILING_ORG)
    coord, conversation_id, message_id, bleeds = _turn(monkeypatch)

    assert _queued_org(coord, conversation_id) == FILING_ORG
    assert _queued_org(coord, message_id) == FILING_ORG
    # The parent lives in the filing organization by design: not a bleed, nothing screamed.
    assert bleeds == []


def test_outside_a_filing_context_nothing_moves(monkeypatch):
    _file_rows_in(None)
    coord, conversation_id, message_id, _ = _turn(monkeypatch)

    assert _queued_org(coord, conversation_id) == STEP_ORG
    assert _queued_org(coord, message_id) == STEP_ORG


def test_a_reader_that_raises_files_nothing_elsewhere():
    def _broken() -> str:
        raise RuntimeError("host bug")

    _ext._registry["row_filing_organization"] = _broken
    kwargs = {"organization_id": STEP_ORG}
    gate._require_create_organization(kwargs, str(uuid4()))
    assert kwargs["organization_id"] == STEP_ORG
