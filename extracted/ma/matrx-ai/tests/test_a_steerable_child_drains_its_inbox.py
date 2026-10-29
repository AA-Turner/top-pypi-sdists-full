"""A helper its host launched as steerable reads messages sent to it mid-run.

An internal (subagent) conversation drains no inbox — under a fan-out of dozens
of children the per-step UPDATE was pure overhead. The agent harness's
``send_message`` steers a RUNNING background helper by writing into that
helper's own inbox, so exactly the helpers launched with the
``STEERABLE_CHILD_KEY`` marker drain it; every other subagent stays skipped.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from matrx_connect.context.app_context import AppContext

from matrx_ai.agents.conversation_type import STEERABLE_CHILD_KEY
from matrx_ai.db import cxm
from matrx_ai.tools import dynamic_drain

HELPER_CONVERSATION = "7a1c2f4e-1d5b-4c3a-9e8f-2b6d4a1c0e9f"
STEER = "[Message from the agent that started you]\nSkip the 2019 filings; only 2024+."


class _Emitter:
    def __init__(self) -> None:
        self.consumed: list[Any] = []

    async def send_injection_consumed(self, payload: Any) -> None:
        self.consumed.append(payload)


def _spy(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    claims: list[str] = []
    row = SimpleNamespace(
        id="0d2e8f1a-3b4c-4d5e-8f6a-7b8c9d0e1f2a",
        kind="user_message",
        content={"text": STEER},
        is_visible_to_user=True,
        enqueued_seq=1,
        metadata={},
    )

    async def claim_pending(conversation_id: str, *, request_id: str | None = None):
        claims.append(conversation_id)
        return [row]

    async def claim_next_turn_end(conversation_id: str, *, request_id: str | None = None):
        return []

    monkeypatch.setattr(cxm.pending_injection, "claim_pending", claim_pending)
    monkeypatch.setattr(cxm.pending_injection, "claim_next_turn_end", claim_next_turn_end)
    async def _no_reports(_cid, *, request_id=None):
        return []

    monkeypatch.setattr(cxm.pending_injection, "claim_reports_now", _no_reports)
    return claims


def _helper_ctx(emitter: _Emitter, *, steerable: bool) -> AppContext:
    return AppContext(
        emitter=emitter,
        user_id="11111111-1111-4111-8111-111111111111",
        organization_id="2c1d4319-bf0d-40bc-8ca1-657f4063d080",
        conversation_id=HELPER_CONVERSATION,
        request_id="b1c2d3e4-f5a6-4b7c-8d9e-0f1a2b3c4d5e",
        store=True,
        is_internal_agent=True,
        conversation_type="subagent",
        metadata={STEERABLE_CHILD_KEY: True} if steerable else {},
    )


@pytest.mark.asyncio
async def test_a_steerable_helper_reads_the_message_at_its_next_step(monkeypatch) -> None:
    claims = _spy(monkeypatch)
    emitter = _Emitter()
    config = SimpleNamespace(messages=[])

    await dynamic_drain.drain_pending_injections(config, _helper_ctx(emitter, steerable=True))

    assert claims == [HELPER_CONVERSATION]
    assert [m.content[0].text for m in config.messages] == [STEER]


@pytest.mark.asyncio
async def test_an_ordinary_subagent_still_skips_the_inbox(monkeypatch) -> None:
    claims = _spy(monkeypatch)
    config = SimpleNamespace(messages=[])

    await dynamic_drain.drain_pending_injections(config, _helper_ctx(_Emitter(), steerable=False))

    assert claims == [], "a non-steerable internal run paid the inbox UPDATE"
    assert config.messages == []
