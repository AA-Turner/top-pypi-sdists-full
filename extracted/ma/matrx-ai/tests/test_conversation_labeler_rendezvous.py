"""Regression: the conversation labeler must never race the conversation
INSERT.

The historical bug: the labeler was scheduled BEFORE the end-of-request flush
committed the cx_conversation row, polled a pending-aware ``exists()`` that saw
the still-QUEUED row, then issued a direct UPDATE that hit zero committed rows
("No rows were updated for Conversation ...").

The fix routes the labeler through the process Rendezvous: it holds the work
until the ORM's commit signal announces the row. These tests prove the work is
withheld until announcement and then fires exactly once — in BOTH arrival
orders — which is the whole class of failure.
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from matrx_utils import rendezvous

import matrx_ai.agents.services.conversation_labeler as labeler


def _install_stubs(monkeypatch, ran: list[str]):
    async def _recorder(**kwargs):
        ran.append(kwargs["conversation_id"])

    monkeypatch.setattr(labeler, "_run_labeling", _recorder)


async def test_labeler_waits_for_commit_then_fires(monkeypatch):
    """Consumer-first: scheduled before the row commits → held, then fired on
    announce. This is the exact production ordering."""
    ran: list[str] = []
    _install_stubs(monkeypatch, ran)
    cid = "11111111-0000-0000-0000-000000000001"

    labeler.schedule_conversation_labeling(cid, "user-1", messages=[{"role": "user", "content": "hi"}])

    # Held — NOT run yet. This is precisely what the old code got wrong.
    assert rendezvous.pending_count("Conversation", cid) == 1
    assert ran == []

    rendezvous.announce("Conversation", cid)  # end-of-request flush commits
    await rendezvous.drain()

    assert ran == [cid]
    assert rendezvous.pending_count("Conversation", cid) == 0
    await rendezvous.aclose()


async def test_labeler_fires_immediately_if_already_committed(monkeypatch):
    """Producer-first: conversation already committed → labeler runs at once."""
    ran: list[str] = []
    _install_stubs(monkeypatch, ran)
    cid = "22222222-0000-0000-0000-000000000002"

    rendezvous.announce("Conversation", cid)  # already on disk
    labeler.schedule_conversation_labeling(cid, "user-1", messages=[{"role": "user", "content": "hi"}])
    await rendezvous.drain()

    assert ran == [cid]
    await rendezvous.aclose()


async def test_duplicate_schedules_coalesce_to_one_run(monkeypatch):
    """Two messages from the same user must not spawn two racing labelers."""
    ran: list[str] = []
    _install_stubs(monkeypatch, ran)
    cid = "33333333-0000-0000-0000-000000000003"

    labeler.schedule_conversation_labeling(cid, "u", messages=[{"role": "user", "content": "a"}])
    labeler.schedule_conversation_labeling(cid, "u", messages=[{"role": "user", "content": "b"}])
    assert rendezvous.pending_count("Conversation", cid) == 1

    rendezvous.announce("Conversation", cid)
    await rendezvous.drain()

    assert ran == [cid]  # fired exactly once
    await rendezvous.aclose()


async def test_missing_ids_do_not_register(monkeypatch):
    ran: list[str] = []
    _install_stubs(monkeypatch, ran)
    labeler.schedule_conversation_labeling("", "u", messages=[{"role": "user", "content": "a"}])
    labeler.schedule_conversation_labeling("cid", "u", messages=[])
    assert rendezvous.pending_count("Conversation", "") == 0
    assert rendezvous.pending_count("Conversation", "cid") == 0


async def test_label_update_uses_standalone_coordinator(monkeypatch):
    queued: list[tuple[str, dict, str, tuple[str, str]]] = []
    scope_args: list[dict[str, str]] = []

    class _Coordinator:
        def queue(self, table, payload, *, op_type, primary_key):
            queued.append((table, payload, op_type, primary_key))
            return "op-1"

    @asynccontextmanager
    async def _scope(**kwargs):
        scope_args.append(kwargs)
        yield _Coordinator()

    monkeypatch.setattr(labeler, "standalone_coordinator", _scope)

    await labeler._update_conversation_labels(
        "conversation-1",
        "user-1",
        {"title": "Coordinator owned"},
    )

    assert scope_args == [
        {
            "reason": "conversation_label",
            "user_id": "user-1",
            "conversation_id": "conversation-1",
        }
    ]
    assert queued == [
        (
            "chat.conversation",
            {"title": "Coordinator owned"},
            "update",
            ("id", "conversation-1"),
        )
    ]
