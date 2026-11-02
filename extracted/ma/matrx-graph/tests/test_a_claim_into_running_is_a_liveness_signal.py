"""Every move into ``running`` stamps a liveness signal in the SAME statement.

Live 2026-10-25, workflow run f30299d0 (knowledge buckets,
``batch.wait_for_units``): parked 11:40:38, a person resumed it 11:52:27 — the
claim flipped the row to 'running' while its only liveness signal was the
11:40:38 heartbeat, and the lifecycle watchdog (900s stale window) stamped it
``run_stranded`` at 11:55:53. A park longer than the stale window minus the time
the claimed leg needs to write its first heartbeat is judged dead the moment it
is claimed. The fix is in the claim itself — every lane that claims (sleep wake,
person's resume, retry, held step, recovery) inherits it.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from uuid import uuid4

import pytest

from matrx_graph.db import run_store as module


def _capture(monkeypatch: pytest.MonkeyPatch) -> dict[str, object]:
    seen: dict[str, object] = {}

    class Model:
        async def update_where(self, filters: dict[str, object], **updates: object) -> SimpleNamespace:
            seen["filters"] = filters
            seen["updates"] = updates
            return SimpleNamespace(rows_affected=1)

    monkeypatch.setattr(module, "get_model", lambda name: Model())
    return seen


def _claimed_at(updates: dict[str, object]) -> datetime:
    merge = updates.get("metadata")
    assert isinstance(merge, module.JsonbMerge), (
        "a claim into 'running' must stamp metadata in the same UPDATE as the "
        "status — otherwise the watchdog judges the claimed run by its park-time heartbeat"
    )
    # Its own top-level key: the shallow merge must never clobber _heartbeat/_recovery.
    assert set(merge.value) == {module.RUN_CLAIM_METADATA_KEY}
    return datetime.fromisoformat(merge.value[module.RUN_CLAIM_METADATA_KEY]["at"])


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "from_statuses", [("interrupted",), ("errored",), ("paused",), ("awaiting_input",), ("failed",)]
)
async def test_claim_for_resume_stamps_liveness_with_the_status(
    monkeypatch: pytest.MonkeyPatch, from_statuses: tuple[str, ...]
) -> None:
    seen = _capture(monkeypatch)
    assert await module.RunStore().claim_for_resume(str(uuid4()), from_statuses=from_statuses)
    updates = seen["updates"]
    assert updates["status"] == "running"
    at = _claimed_at(updates)
    assert datetime.now(UTC) - at < timedelta(seconds=5)


@pytest.mark.asyncio
async def test_recovery_transition_into_running_stamps_liveness(monkeypatch: pytest.MonkeyPatch) -> None:
    seen = _capture(monkeypatch)
    await module.RunStore().transition(
        str(uuid4()), from_statuses=("failed",), to_status="running", clear_error=True
    )
    _claimed_at(seen["updates"])
    assert seen["updates"]["error"] is None


@pytest.mark.asyncio
async def test_mark_running_stamps_liveness(monkeypatch: pytest.MonkeyPatch) -> None:
    seen = _capture(monkeypatch)
    await module.RunStore().mark_running(str(uuid4()))
    _claimed_at(seen["updates"])


@pytest.mark.asyncio
async def test_a_move_out_of_running_stamps_no_claim(monkeypatch: pytest.MonkeyPatch) -> None:
    seen = _capture(monkeypatch)
    await module.RunStore().transition(str(uuid4()), from_statuses=("failed",), to_status="interrupted")
    assert "metadata" not in seen["updates"]
