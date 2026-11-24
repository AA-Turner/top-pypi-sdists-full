"""C135 (PB-08 k=30): two helper reports taken at one boundary are ONE stored host message.

Where a report was delivered used to decide its shape: a woken turn (inbox_driver) wrote one host
message holding both `<task-notification>` blocks, the run's own boundary drain wrote one message per
row (d16: positions 8 and 9 in the same millisecond). A consumer counting messages got 1 or 2.
A person's own queued words stay one message each.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import matrx_ai.db.cx_managers as cxm_mod
from matrx_ai.tools import dynamic_drain


def _note(i: str, helper: str) -> SimpleNamespace:
    return SimpleNamespace(
        id=i,
        kind="system_message",
        source="deferred_tool",
        is_visible_to_user=False,
        content={"text": f"<task-notification>\n<task-id>{helper}</task-id>\n</task-notification>"},
        metadata={},
        enqueued_seq=1,
    )


async def _none(_c, *, request_id=None):
    return []


class _Emitter:
    def __init__(self) -> None:
        self.payloads: list[Any] = []

    async def send_injection_consumed(self, payload: Any) -> None:
        self.payloads.append(payload)


async def test_two_helper_reports_are_one_host_message(monkeypatch):
    rows = [_note("r1", "write-haiku-22c8a1"), _note("r2", "list-three-facts-cb8014")]

    async def _reports(_c, *, request_id=None):
        return rows

    monkeypatch.setattr(
        cxm_mod.cxm, "pending_injection", SimpleNamespace(claim_pending=_none, claim_reports_now=_reports)
    )
    config = SimpleNamespace(messages=[])
    emitter = _Emitter()
    ctx = SimpleNamespace(conversation_id="c", request_id="req", emitter=emitter)
    await dynamic_drain.drain_pending_injections(config, ctx)

    assert len(config.messages) == 1, "two reports must be ONE host message, not one per row"
    text = config.messages[0].content[0].text
    assert "write-haiku-22c8a1" in text and "list-three-facts-cb8014" in text
    assert text.count("<task-notification>") == 2
    assert config.messages[0].metadata["inbox_injection_ids"] == ["r1", "r2"]
    items = emitter.payloads[0].items
    assert {it.injection_id for it in items} == {"r1", "r2"}
    assert {it.position for it in items} == {0}


async def test_a_persons_words_stay_their_own_message(monkeypatch):
    person = SimpleNamespace(
        id="p1", kind="user_message", source="queue", is_visible_to_user=True,
        content={"text": "hello"}, metadata={}, enqueued_seq=1,
    )

    async def _claim(_c, *, request_id=None):
        return [_note("r1", "a-aaaaaa"), person, _note("r2", "b-bbbbbb")]

    monkeypatch.setattr(
        cxm_mod.cxm, "pending_injection", SimpleNamespace(claim_pending=_claim, claim_reports_now=_none)
    )
    config = SimpleNamespace(messages=[])
    await dynamic_drain.drain_pending_injections(config, SimpleNamespace(conversation_id="c", request_id="r", emitter=None))
    assert [m.content[0].text.startswith("<task-notification>") for m in config.messages] == [True, False, True]
