"""L48 defect 79: every stored request names the agent version that ran.

Live 2026-10-20: 5,730 of ~8,400 recent ``chat.request_snapshot`` rows had an empty
``agent_definition_version`` although their conversation named the agent (and, via the
conversation trigger, the version). The snapshot writer read ``ctx.agent_version_id`` only,
which is set for PINNED runs; a floating run (latest) carries ``agent_id`` alone, and a
continuation / child may carry neither on its context.

Census over the doors, all through the ONE writer ``_write_request_snapshot``:
  pinned version | floating agent (latest) | continuation (conversation only) |
  child fork (version cleared, agent set) | no agent at all (honest NULL).
"""

from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

import pytest

from matrx_ai.orchestrator import executor as executor_mod
from matrx_ai.orchestrator.execution_state import ExecutionState

AGENT = str(uuid4())
VERSION = str(uuid4())
LIVE_VERSION = str(uuid4())
CONV_VERSION = str(uuid4())


async def _stamped(monkeypatch: pytest.MonkeyPatch, **ctx_fields) -> object:
    queued: list[dict] = []
    monkeypatch.setattr("matrx_ai.persistence.queue_helpers.get_coordinator", lambda: object())
    monkeypatch.setattr(
        "matrx_ai.persistence.queue_helpers.queue_request_snapshot_create",
        lambda **kwargs: queued.append(kwargs) or "op",
    )

    async def fake_live_version(agent_id: str) -> str | None:
        return LIVE_VERSION if agent_id == AGENT else None

    async def fake_conv_version(conversation_id: str) -> str | None:
        return CONV_VERSION

    monkeypatch.setattr("matrx_ai.db.persistence.live_version_id_for_agent", fake_live_version)
    monkeypatch.setattr("matrx_ai.db.persistence.conversation_agent_version_id", fake_conv_version)
    ctx = SimpleNamespace(
        store=True,
        conversation_id=str(uuid4()),
        request_id=str(uuid4()),
        metadata={},
        agent_id=None,
        agent_version_id=None,
    )
    for k, v in ctx_fields.items():
        setattr(ctx, k, v)
    await executor_mod._write_request_snapshot(
        exec_ctx=ctx,
        iteration=1,
        api_response=None,
        request_payload={"messages": []},
        unified_payload=None,
        trigger_position=0,
        first_assistant_position=1,
        state_snapshot=ExecutionState().snapshot(),
        error_payload=None,
        provider="anthropic",
        model="claude-sonnet-5",
    )
    assert len(queued) == 1
    return queued[0].get("agent_definition_version")


@pytest.mark.asyncio
async def test_pinned_version_run(monkeypatch: pytest.MonkeyPatch) -> None:
    assert await _stamped(monkeypatch, agent_version_id=VERSION) == VERSION


@pytest.mark.asyncio
async def test_floating_latest_run_names_the_live_version(monkeypatch: pytest.MonkeyPatch) -> None:
    assert await _stamped(monkeypatch, agent_id=AGENT) == LIVE_VERSION


@pytest.mark.asyncio
async def test_child_fork_with_version_cleared(monkeypatch: pytest.MonkeyPatch) -> None:
    assert await _stamped(monkeypatch, agent_id=AGENT, agent_version_id=None) == LIVE_VERSION


@pytest.mark.asyncio
async def test_continuation_with_only_the_conversation(monkeypatch: pytest.MonkeyPatch) -> None:
    assert await _stamped(monkeypatch) == CONV_VERSION
