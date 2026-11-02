from __future__ import annotations

from datetime import datetime
from types import SimpleNamespace
from uuid import uuid4

import pytest

from matrx_graph.db import run_store as module


@pytest.mark.asyncio
@pytest.mark.parametrize(("rows_affected", "started"), [(1, True), (0, False)])
async def test_mark_running_never_matches_control_states(
    monkeypatch: pytest.MonkeyPatch,
    rows_affected: int,
    started: bool,
) -> None:
    run_id = str(uuid4())
    seen: dict[str, object] = {}

    class Model:
        async def update_where(
            self, filters: dict[str, object], **updates: object
        ) -> SimpleNamespace:
            seen["filters"] = filters
            seen["updates"] = updates
            return SimpleNamespace(rows_affected=rows_affected)

    monkeypatch.setattr(module, "get_model", lambda name: Model())

    result = await module.RunStore().mark_running(run_id)

    assert result is started
    assert seen["filters"] == {
        "id": run_id,
        "status__in": ["pending", "running"],
    }
    updates = dict(seen["updates"])
    claim = updates.pop("metadata")
    assert updates == {"status": "running"}
    # The claim is a liveness signal in the SAME statement (run f30299d0).
    assert isinstance(claim, module.JsonbMerge)
    assert set(claim.value) == {module.RUN_CLAIM_METADATA_KEY}


@pytest.mark.asyncio
async def test_mark_cancelling_supersedes_pause_before_park(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    run_id = str(uuid4())
    seen: dict[str, object] = {}

    class Model:
        async def update_where(
            self, filters: dict[str, object], **updates: object
        ) -> SimpleNamespace:
            seen["filters"] = filters
            seen["updates"] = updates
            return SimpleNamespace(rows_affected=1)

    monkeypatch.setattr(module, "get_model", lambda name: Model())

    assert await module.RunStore().mark_cancelling(run_id) is True
    assert seen["filters"] == {
        "id": run_id,
        "status__in": ["pending", "running", "pausing"],
    }
    assert seen["updates"] == {"status": "cancelling"}


@pytest.mark.asyncio
async def test_parked_cancel_is_a_guarded_terminal_transition(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    run_id = str(uuid4())
    seen: dict[str, object] = {}

    class Model:
        async def update_where(
            self, filters: dict[str, object], **updates: object
        ) -> SimpleNamespace:
            seen["filters"] = filters
            seen["updates"] = updates
            return SimpleNamespace(rows_affected=1)

    monkeypatch.setattr(module, "get_model", lambda name: Model())

    assert await module.RunStore().mark_parked_cancelled(run_id) is True
    assert seen["filters"] == {
        "id": run_id,
        "status__in": ["paused", "interrupted", "errored", "awaiting_input"],
    }
    updates = seen["updates"]
    assert isinstance(updates, dict)
    assert updates["status"] == "cancelled"
    assert updates["completed_at"] is not None


@pytest.mark.asyncio
@pytest.mark.parametrize(("rows_affected", "retired"), [(1, True), (0, False)])
async def test_soft_delete_refuses_live_runs_and_discards_only_retired_queue_residue(
    monkeypatch: pytest.MonkeyPatch,
    rows_affected: int,
    retired: bool,
) -> None:
    run_id = str(uuid4())
    seen: dict[str, object] = {}
    discarded: list[str] = []

    class Model:
        async def update_where(
            self, filters: dict[str, object], **updates: object
        ) -> SimpleNamespace:
            seen["filters"] = filters
            seen["updates"] = updates
            return SimpleNamespace(rows_affected=rows_affected)

    async def fake_discard(supplied_run_id: str) -> int:
        discarded.append(supplied_run_id)
        return 1

    monkeypatch.setattr(module, "get_model", lambda name: Model())
    monkeypatch.setattr("matrx_graph.workers.queue.discard_for_run", fake_discard)

    assert await module.RunStore().soft_delete(run_id) is retired
    assert seen["filters"] == {
        "id": run_id,
        "deleted_at__isnull": True,
        "status__in": ["completed", "failed", "cancelled", "errored"],
    }
    updates = seen["updates"]
    assert isinstance(updates, dict) and updates["deleted_at"] is not None
    assert discarded == ([run_id] if retired else [])


# ── W62: a resumed/completed run never keeps its death certificate ──────────
# Live 2026-09-13 (Watson Parenting Adviser): the lifecycle watchdog force-
# failed three in-flight runs at a deploy, wf_cancel_reconciliation resumed
# them, and two of them (d611933b, f748a361) went on to COMPLETE with real
# output — while `workflow.run.error` still carried the watchdog's
# `run_stranded` blob. The row said "completed" and "we dropped this run" at
# the same time. Both halves of the seam are asserted below with the VERBATIM
# production error payload.
_PRODUCTION_STRANDED_ERROR = {
    "cause": "run_stranded",
    "source": "lifecycle_sweeper",
    "message": (
        "This run was dropped by our system before it could finish — "
        "nothing you did caused it."
    ),
    "technical": (
        "Watchdog force-failed run (stale-heartbeat): run was heartbeating "
        "but went silent — last liveness signal at 2026-09-13 06:12:43"
    ),
}


def _capturing_model(seen: dict[str, object], rows_affected: int = 1):
    class Model:
        async def update_where(
            self, filters: dict[str, object], **updates: object
        ) -> SimpleNamespace:
            seen["filters"] = filters
            seen["updates"] = updates
            return SimpleNamespace(rows_affected=rows_affected)

    return Model()


@pytest.mark.asyncio
async def test_resume_into_running_clears_the_stranded_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A run coming back to life sheds the error that explained its death."""
    seen: dict[str, object] = {}
    monkeypatch.setattr(module, "get_model", lambda name: _capturing_model(seen))

    assert (
        await module.RunStore().transition(
            str(uuid4()), from_statuses=("failed",), to_status="running"
        )
        is True
    )
    updates = seen["updates"]
    assert updates["status"] == "running"
    assert "error" in updates, (
        "resume must clear workflow.run.error — the watchdog's run_stranded "
        f"blob otherwise outlives the resume: {_PRODUCTION_STRANDED_ERROR}"
    )
    assert updates["error"] is None


@pytest.mark.asyncio
async def test_transition_to_a_terminal_status_leaves_error_untouched(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Clearing is scoped to coming ALIVE; a terminal move must not erase why."""
    seen: dict[str, object] = {}
    monkeypatch.setattr(module, "get_model", lambda name: _capturing_model(seen))

    await module.RunStore().transition(
        str(uuid4()), from_statuses=("running",), to_status="cancelled"
    )
    updates = seen["updates"]
    assert updates["status"] == "cancelled"
    assert isinstance(updates["completed_at"], datetime)
    assert updates["completed_at"].tzinfo is not None
    assert "error" not in updates


@pytest.mark.asyncio
async def test_completed_run_never_carries_an_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """mark_completed is the last gate: a completed row cannot say it failed."""
    seen: dict[str, object] = {}
    monkeypatch.setattr(module, "get_model", lambda name: _capturing_model(seen))

    assert (
        await module.RunStore().mark_completed(
            str(uuid4()), output={"deliver": {"letter": "…"}}, steps_executed=9
        )
        is True
    )
    updates = seen["updates"]
    assert updates["status"] == "completed"
    assert "error" in updates and updates["error"] is None, (
        "a COMPLETED run published real output; it must not also carry "
        f"{_PRODUCTION_STRANDED_ERROR['message']!r}"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("status_name", ["INTERRUPTED", "PAUSED", "ERRORED"])
async def test_every_resumable_park_keeps_the_legs_outputs(
    monkeypatch: pytest.MonkeyPatch, status_name: str
) -> None:
    """A resume restarts ``last_outputs`` empty and mark_completed only merges
    what the last leg produced — so EVERY resumable park (interrupt, pause,
    error) must persist the partial outputs, or a node that finished before
    the park (a mandate's deliverable) is lost from the completed row."""
    from matrx_graph.types.run import RunStatus

    seen: dict[str, object] = {}

    class Model:
        async def update_where(
            self, filters: dict[str, object], **updates: object
        ) -> SimpleNamespace:
            seen["updates"] = updates
            return SimpleNamespace(rows_affected=1)

    monkeypatch.setattr(module, "get_model", lambda name: Model())
    async def _no_wake(*_a: object, **_k: object) -> None:
        return None

    monkeypatch.setattr("matrx_graph.workers.sleep_wake.schedule_sleep_wake", _no_wake)

    await module.RunStore().apply_result(
        str(uuid4()),
        status=getattr(RunStatus, status_name),
        steps_executed=2,
        output={"emit_quiz": {"quiz": 1}},
        interrupt={"node_id": "ask", "payload": {}, "checkpoint_id": str(uuid4())},
        error="boom",
        last_checkpoint_id=None,
    )

    merge = seen["updates"]["output"]  # type: ignore[index]
    assert "emit_quiz" in repr(getattr(merge, "__dict__", merge))


@pytest.mark.asyncio
@pytest.mark.parametrize("empty", [{}, {"message": ""}, {"message": None}])
async def test_a_failed_run_always_records_a_reason(
    monkeypatch: pytest.MonkeyPatch, empty: dict[str, object]
) -> None:
    seen: dict[str, object] = {}

    class Model:
        async def update_where(
            self, filters: dict[str, object], **updates: object
        ) -> SimpleNamespace:
            seen.update(updates)
            return SimpleNamespace(rows_affected=1)

    monkeypatch.setattr(module, "get_model", lambda name: Model())
    await module.RunStore().mark_failed(str(uuid4()), error=empty)
    assert seen["status"] == "failed"
    assert seen["error"], "a failed run was written with no reason"
    assert "no reason recorded" in str(seen["error"])
