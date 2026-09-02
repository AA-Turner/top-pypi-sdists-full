"""Forcing-function: a snapshot must record WHICH provider produced it.

``UnifiedResponse.metadata`` carries no ``provider`` key, so the writer's
"read it off the response" fallback always landed on the literal string
``"unknown"`` for every SUCCESS-path row. That was invisible while capture was
per-request opt-in (2 rows/day); the moment capture went always-on (D-33) it
would have been a corrupt ``provider`` column on *every* snapshot — and the
provider is not decoration, it is which SDK a replay has to re-issue against.

The fix keeps ONE source of truth: each provider's ``execute()`` already passes
its own literal name into ``capture_request_payload`` at the exact seam where
the payload is captured, so the name is stashed beside the payload and popped
with it. These tests pin both halves of that seam.
"""

from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

import pytest

from matrx_ai.orchestrator import executor as executor_mod
from matrx_ai.orchestrator.execution_state import (
    ExecutionState,
    clear_execution_state,
    set_execution_state,
)
from matrx_ai.providers.snapshot import capture_request_payload


def test_capture_stamps_provider_beside_the_payload() -> None:
    state = ExecutionState()
    token = set_execution_state(state)
    try:
        capture_request_payload({"messages": []}, provider="anthropic")
    finally:
        clear_execution_state(token)

    assert state.snapshot_payload == {"messages": []}
    assert state.snapshot_provider == "anthropic", (
        "the provider must be stamped by the same call that captures the payload "
        "— two separate sources for one fact is how they drift"
    )


def test_capture_without_a_provider_leaves_the_stamp_alone() -> None:
    # A caller that passes no provider must not blank a previously-stamped one;
    # the executor pops the pair, so an unstamped capture is not a reset event.
    state = ExecutionState()
    state.snapshot_provider = "openai"
    token = set_execution_state(state)
    try:
        capture_request_payload({"messages": []})
    finally:
        clear_execution_state(token)

    assert state.snapshot_provider == "openai"


@pytest.mark.asyncio
async def test_writer_records_the_stamped_provider(monkeypatch) -> None:
    queued: list[dict] = []
    monkeypatch.setattr(
        "matrx_ai.persistence.queue_helpers.get_coordinator", lambda: object()
    )
    monkeypatch.setattr(
        "matrx_ai.persistence.queue_helpers.queue_request_snapshot_create",
        lambda **kwargs: queued.append(kwargs) or "op",
    )

    exec_ctx = SimpleNamespace(store=True, conversation_id=str(uuid4()), request_id=str(uuid4()))

    await executor_mod._write_request_snapshot(
        exec_ctx=exec_ctx,
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
    assert queued[0]["provider"] == "anthropic", (
        f"snapshot recorded provider={queued[0]['provider']!r} — a snapshot that "
        "cannot say which provider made the call is not a replayable input"
    )
    assert queued[0]["model"] == "claude-sonnet-5", (
        f"snapshot recorded model={queued[0]['model']!r} — same failure mode as "
        "provider: UnifiedResponse.metadata has no bare 'model' key either, so "
        "the success path wrote NULL until the executor passed it explicitly"
    )
