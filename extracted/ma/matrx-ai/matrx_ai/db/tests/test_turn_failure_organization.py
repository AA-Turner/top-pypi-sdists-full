"""``persist_stream_turn_failure`` must never write a null organization.

Shape 2.7, 2026-09-20: ``chat.message.organization_id`` is NOT NULL, but the
``fields`` dict this seam builds for the dead-turn row never carried one — a
sibling of the ``chat.agent_run`` bug fixed the same night in
``matrx_ai.agent_runners._checkpoint``. This is the OUT-OF-LANE crash branch:
the request that verified an organization may be long gone by the time a
stream task's crash is caught, so the only source trusted here is the PARENT
conversation row itself — see
``matrx_ai.db.turn_failure._organization_for_failed_turn``.

Both writers this module can use — the in-lane ``_queue_message_create`` and
the out-of-lane ``_direct_write_failed_message`` — share the SAME ``fields``
dict, so fixing it once at the build site covers both; these tests exercise
both branches to prove that.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

import matrx_ai.db.turn_failure as turn_failure_module
from matrx_ai.db import cxm


class _FakeConversationManager:
    def __init__(self, organization_id: str | None) -> None:
        self._organization_id = organization_id

    async def filter_items(self, **_kw: Any):
        if self._organization_id is None:
            return []
        return [SimpleNamespace(organization_id=self._organization_id)]


@pytest.mark.asyncio
async def test_in_lane_write_stamps_organization_from_parent_conversation(monkeypatch):
    """In-lane branch (a lane coordinator is active): the queued create must
    carry the PARENT conversation's organization_id."""
    monkeypatch.setattr(cxm, "conversation", _FakeConversationManager("org-parent"))
    monkeypatch.setattr(turn_failure_module, "_active_lane_coordinator", lambda: object())

    queued: dict[str, Any] = {}

    def fake_queue(**kwargs: Any) -> str:
        queued.update(kwargs)
        return "queued"

    monkeypatch.setattr(turn_failure_module, "_queue_message_create", fake_queue)

    wrote = await turn_failure_module.persist_stream_turn_failure(
        conversation_id="conv-1",
        request_id=None,
        user_id="user-1",
        error_type="stream_crash",
        message="boom",
        user_message="Something went wrong.",
        route="chat",
    )

    assert wrote is True
    assert queued["organization_id"] == "org-parent"
    assert queued["conversation_id"] == "conv-1"


@pytest.mark.asyncio
async def test_out_of_lane_write_stamps_organization_from_parent_conversation(monkeypatch):
    """Out-of-lane branch (no active lane coordinator, `_direct_write_failed_message`):
    the fields handed to it must carry the PARENT conversation's organization_id."""
    monkeypatch.setattr(cxm, "conversation", _FakeConversationManager("org-parent"))
    monkeypatch.setattr(turn_failure_module, "_active_lane_coordinator", lambda: None)

    captured: dict[str, Any] = {}

    async def fake_direct_write(fields: dict[str, Any], _conversation_id: str) -> bool:
        captured.update(fields)
        return True

    monkeypatch.setattr(turn_failure_module, "_direct_write_failed_message", fake_direct_write)

    wrote = await turn_failure_module.persist_stream_turn_failure(
        conversation_id="conv-2",
        request_id=None,
        user_id="user-1",
        error_type="stream_crash",
        message="boom",
        user_message="Something went wrong.",
        route="chat",
    )

    assert wrote is True
    assert captured["organization_id"] == "org-parent"


@pytest.mark.asyncio
async def test_no_organization_on_the_parent_refuses_without_a_write(monkeypatch):
    """The conversation row can't be read (or carries no organization) → NO
    write is attempted on either branch, and the seam still never raises."""
    monkeypatch.setattr(cxm, "conversation", _FakeConversationManager(None))
    monkeypatch.setattr(turn_failure_module, "_active_lane_coordinator", lambda: object())

    queued: dict[str, Any] = {}

    def fake_queue(**kwargs: Any) -> str:
        queued.update(kwargs)
        return "queued"

    monkeypatch.setattr(turn_failure_module, "_queue_message_create", fake_queue)

    wrote = await turn_failure_module.persist_stream_turn_failure(
        conversation_id="conv-orgless",
        request_id=None,
        user_id="user-1",
        error_type="stream_crash",
        message="boom",
        user_message="Something went wrong.",
        route="chat",
    )

    assert wrote is False
    assert queued == {}
