"""FORCING TEST — a conversation's child rows live in the CONVERSATION's org.

THE LAW (``common-docs/policies/context-is-carried-never-rebuilt.md``): a child
row lives in its parent record's organization; the request context is carried,
never substituted.

Measured on production 2026-09-17: in 30 days, 211 ``chat.tool_call`` rows (742
all-time) and 3,217 ``chat.message`` rows all-time landed in an organization
that was NOT their conversation's. Both tables carry
``platform.inherit_org_from_parent``, which only fills a NULL organization — so
those rows arrived carrying an EXPLICIT wrong organization. The writer was the
one stamp point for both tables,
``matrx_ai.persistence.queue_helpers._queue_or_drop``, which stamped the AMBIENT
request's organization (the user's ACTIVE organization, or a previous request's
context leaking into a detached task) onto every child INSERT.

Nothing here is invented: the REAL conversation gate, the REAL Coordinator and
the REAL queue doors run, and the assertions read the organization off the REAL
queued ops. Only the database read at the gate's own boundary is faked — that is
the boundary, not the logic under test.
"""

from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

import pytest

from matrx_ai.db import conversation_gate as gate

CONVERSATION_ORG = "11111111-1111-4111-8111-111111111111"  # org B — the conversation's
ACTIVE_ORG = "22222222-2222-4222-8222-222222222222"  # org A — the ambient request's


class _MessageMeta:
    primary_keys = ["id"]
    foreign_keys: dict = {}
    table_name = "message"
    db_schema = "chat"


class _ToolCallMeta(_MessageMeta):
    table_name = "tool_call"


class _PackageMessage:
    _meta = _MessageMeta()


class _PackageToolCall:
    _meta = _ToolCallMeta()


@pytest.fixture(autouse=True)
def _clean(monkeypatch):
    from matrx_ai.persistence.conversation_org import reset_conversation_organizations
    from matrx_ai.persistence.registry import override_table

    reset_conversation_organizations()
    gate._known_conversation_ids.clear()
    monkeypatch.setattr(gate, "try_get_tracker", lambda: None)
    # SCOPED, never ``register_table``: that is first-writer-wins, so a stand-in
    # bound with it would own the real chat.message / chat.tool_call keys for
    # the rest of the process (main's registry-isolation guard names exactly
    # that leak). ``override_table`` restores the previous binding on exit.
    with override_table("chat.message", _PackageMessage), override_table(
        "chat.tool_call", _PackageToolCall
    ):
        yield
    reset_conversation_organizations()
    gate._known_conversation_ids.clear()


def _ambient_context(monkeypatch, organization_id: str | None) -> None:
    """Pin the AMBIENT request organization the child doors used to trust."""
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


def _queued_org(coord, row_id: str) -> str | None:
    for op in coord._session._ops:
        if op.pk_value == row_id:
            return (op.payload or {}).get("organization_id")
    raise AssertionError(f"no queued op for row {row_id}")


async def _run_turn(monkeypatch, conversation_row, *, ambient_org: str | None = ACTIVE_ORG):
    """One real turn: the gate confirms the conversation, then the real doors
    queue a message and a tool_call onto a real Coordinator."""
    from matrx_ai.persistence.coordinator import Coordinator
    from matrx_ai.persistence.queue_helpers import (
        _coordinator_cv,
        queue_message_create,
        queue_tool_call_create,
    )

    conversation_id = str(conversation_row["id"])
    user_id = str(uuid4())

    class _Conversation:
        async def filter_conversations(self, **_kwargs):
            return [SimpleNamespace(**conversation_row)] if conversation_row.get("id") else []

    monkeypatch.setattr(gate, "_cxm", lambda: SimpleNamespace(conversation=_Conversation()))
    monkeypatch.setattr(gate, "_require_persistence_actor", lambda value, _where: value)
    monkeypatch.setattr(gate, "_verify_system_anchor_owner", lambda *_a, **_kw: None)

    coord = Coordinator(request_id=str(uuid4()), conversation_id=conversation_id)
    token = _coordinator_cv.set(coord)
    try:
        monkeypatch.setattr(gate, "_get_coordinator", lambda: coord)
        monkeypatch.setattr(gate, "_get_active_lane_coordinator", lambda: coord)
        # The real gate — the continued conversation is confirmed to exist.
        await gate.ensure_conversation_exists(conversation_id, user_id)

        _ambient_context(monkeypatch, ambient_org)

        message_id = str(uuid4())
        tool_call_id = str(uuid4())
        queue_message_create(
            id=message_id,
            conversation_id=conversation_id,
            role="assistant",
            position=1,
            status="active",
            content=[{"type": "text", "text": "hi"}],
        )
        queue_tool_call_create(
            id=tool_call_id,
            conversation_id=conversation_id,
            tool_name="search",
            status="running",
        )
        return coord, message_id, tool_call_id
    finally:
        _coordinator_cv.reset(token)


@pytest.mark.asyncio
async def test_children_of_a_continued_conversation_take_its_organization(monkeypatch):
    """The 211-row bug: the conversation lives in org B, the request is running
    under the user's ACTIVE org A, and the child rows must still land in B."""
    conversation_id = str(uuid4())
    coord, message_id, tool_call_id = await _run_turn(
        monkeypatch,
        {"id": conversation_id, "organization_id": CONVERSATION_ORG},
    )

    assert _queued_org(coord, message_id) == CONVERSATION_ORG
    assert _queued_org(coord, tool_call_id) == CONVERSATION_ORG


@pytest.mark.asyncio
async def test_an_explicit_wrong_organization_is_corrected_too(monkeypatch):
    """A caller that hands the door an organization of its own does not get to
    move a child row out of its conversation."""
    from matrx_ai.persistence.conversation_org import remember_conversation_organization
    from matrx_ai.persistence.coordinator import Coordinator
    from matrx_ai.persistence.queue_helpers import _coordinator_cv, queue_tool_call_create

    conversation_id = str(uuid4())
    remember_conversation_organization(conversation_id, CONVERSATION_ORG)
    _ambient_context(monkeypatch, ACTIVE_ORG)

    coord = Coordinator(request_id=str(uuid4()))
    token = _coordinator_cv.set(coord)
    try:
        row_id = str(uuid4())
        queue_tool_call_create(
            id=row_id,
            conversation_id=conversation_id,
            tool_name="search",
            status="running",
            organization_id=ACTIVE_ORG,
        )
        assert _queued_org(coord, row_id) == CONVERSATION_ORG
    finally:
        _coordinator_cv.reset(token)


@pytest.mark.asyncio
async def test_the_correction_is_captured_not_silent(monkeypatch):
    """Nothing fails silently: a corrected row announces the writer that tried
    to put it in the wrong organization."""
    from matrx_ai.persistence import queue_helpers
    from matrx_ai.persistence.conversation_org import remember_conversation_organization
    from matrx_ai.persistence.coordinator import Coordinator

    captured: list[dict] = []
    monkeypatch.setattr(
        queue_helpers,
        "_capture_child_org_bleed",
        lambda **kw: captured.append(kw),
    )

    conversation_id = str(uuid4())
    remember_conversation_organization(conversation_id, CONVERSATION_ORG)
    _ambient_context(monkeypatch, ACTIVE_ORG)

    coord = Coordinator(request_id=str(uuid4()))
    token = queue_helpers._coordinator_cv.set(coord)
    try:
        queue_helpers.queue_message_create(
            id=str(uuid4()),
            conversation_id=conversation_id,
            role="assistant",
            position=0,
            status="active",
            content=[],
        )
    finally:
        queue_helpers._coordinator_cv.reset(token)

    assert len(captured) == 1
    assert captured[0]["declared"] == ACTIVE_ORG
    assert captured[0]["parent_org"] == CONVERSATION_ORG
    assert captured[0]["from_payload"] is False


@pytest.mark.asyncio
async def test_a_matching_organization_is_never_announced(monkeypatch):
    """No scream when the ambient organization already agrees with the row's
    parent — the capture must mean something."""
    from matrx_ai.persistence import queue_helpers
    from matrx_ai.persistence.conversation_org import remember_conversation_organization
    from matrx_ai.persistence.coordinator import Coordinator

    captured: list[dict] = []
    monkeypatch.setattr(
        queue_helpers, "_capture_child_org_bleed", lambda **kw: captured.append(kw)
    )

    conversation_id = str(uuid4())
    remember_conversation_organization(conversation_id, CONVERSATION_ORG)
    _ambient_context(monkeypatch, CONVERSATION_ORG)

    coord = Coordinator(request_id=str(uuid4()))
    token = queue_helpers._coordinator_cv.set(coord)
    try:
        row_id = str(uuid4())
        queue_helpers.queue_message_create(
            id=row_id,
            conversation_id=conversation_id,
            role="user",
            position=0,
            status="active",
            content=[],
        )
        assert _queued_org(coord, row_id) == CONVERSATION_ORG
    finally:
        queue_helpers._coordinator_cv.reset(token)

    assert captured == []


@pytest.mark.asyncio
async def test_an_unknown_conversation_still_takes_the_ambient_organization(monkeypatch):
    """A conversation this process has never read keeps the previous behaviour —
    the fallback degrades to ambient + the DB backstop, never to a guess."""
    from matrx_ai.persistence import queue_helpers
    from matrx_ai.persistence.coordinator import Coordinator

    _ambient_context(monkeypatch, ACTIVE_ORG)
    coord = Coordinator(request_id=str(uuid4()))
    token = queue_helpers._coordinator_cv.set(coord)
    try:
        row_id = str(uuid4())
        queue_helpers.queue_tool_call_create(
            id=row_id,
            conversation_id=str(uuid4()),
            tool_name="search",
            status="running",
        )
        assert _queued_org(coord, row_id) == ACTIVE_ORG
    finally:
        queue_helpers._coordinator_cv.reset(token)
