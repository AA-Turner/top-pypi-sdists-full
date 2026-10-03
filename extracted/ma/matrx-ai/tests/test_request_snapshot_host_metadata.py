"""Forcing-function: host-staged metadata reaches the turn's FIRST request snapshot, once.

aidream stages what the ``context`` tool returns for every on-request value of a turn on
``AppContext.metadata[REQUEST_SNAPSHOT_METADATA_KEY]``. That text is, by definition, not in the
provider request — so unless the snapshot keeps it, the sent-turn context viewer can never return
it (410 ``not_retained``; common-docs context-delivery RULES.md §5b). One copy per turn: later
tool-round iterations never repeat it.
"""

from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

import pytest

from matrx_ai.orchestrator import executor as executor_mod
from matrx_ai.orchestrator.execution_state import ExecutionState
from matrx_ai.orchestrator.snapshot_metadata import (
    REQUEST_SNAPSHOT_METADATA_KEY,
    snapshot_metadata_for,
)

KEPT = {"context_on_request": {"lease_terms": "Tenant pays water; landlord pays sewer."}}


async def _write(monkeypatch: pytest.MonkeyPatch, iteration: int, metadata: dict) -> list[dict]:
    queued: list[dict] = []
    monkeypatch.setattr("matrx_ai.persistence.queue_helpers.get_coordinator", lambda: object())
    monkeypatch.setattr(
        "matrx_ai.persistence.queue_helpers.queue_request_snapshot_create",
        lambda **kwargs: queued.append(kwargs) or "op",
    )
    exec_ctx = SimpleNamespace(
        store=True, conversation_id=str(uuid4()), request_id=str(uuid4()), metadata=metadata
    )
    await executor_mod._write_request_snapshot(
        exec_ctx=exec_ctx,
        iteration=iteration,
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
    return queued


@pytest.mark.asyncio
async def test_the_first_snapshot_keeps_the_hosts_metadata(monkeypatch: pytest.MonkeyPatch) -> None:
    queued = await _write(monkeypatch, 1, {REQUEST_SNAPSHOT_METADATA_KEY: KEPT})
    assert len(queued) == 1
    assert queued[0].get("metadata") == KEPT, (
        "the host's on-request texts never reached chat.request_snapshot.metadata — the viewer "
        "can then only answer 410 for every on-request value of a sent turn"
    )


@pytest.mark.asyncio
async def test_a_tool_round_iteration_does_not_repeat_it(monkeypatch: pytest.MonkeyPatch) -> None:
    queued = await _write(monkeypatch, 2, {REQUEST_SNAPSHOT_METADATA_KEY: KEPT})
    assert "metadata" not in queued[0]


@pytest.mark.asyncio
async def test_nothing_staged_writes_no_metadata(monkeypatch: pytest.MonkeyPatch) -> None:
    queued = await _write(monkeypatch, 1, {})
    assert "metadata" not in queued[0]


def test_snapshot_metadata_for_reads_only_a_dict_on_iteration_one() -> None:
    ctx = SimpleNamespace(metadata={REQUEST_SNAPSHOT_METADATA_KEY: KEPT})
    assert snapshot_metadata_for(ctx, 1) == KEPT
    assert snapshot_metadata_for(ctx, 2) is None
    assert snapshot_metadata_for(SimpleNamespace(metadata={REQUEST_SNAPSHOT_METADATA_KEY: "x"}), 1) is None
    assert snapshot_metadata_for(SimpleNamespace(), 1) is None
