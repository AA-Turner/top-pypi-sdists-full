from __future__ import annotations

from datetime import datetime
from types import SimpleNamespace
from uuid import uuid4

import pytest

from matrx_graph.db import run_store as module


@pytest.mark.asyncio
@pytest.mark.parametrize("has_actor", [True, False])
@pytest.mark.parametrize("changed", [True, False])
async def test_reattach_payload_read_repeats_the_identity_predicates(monkeypatch, has_actor, changed):
    run_id = str(uuid4())
    actor = str(uuid4()) if has_actor else None
    org = str(uuid4())
    identity = {"created_by": actor, "organization_id": org, "deleted_at": None}
    payload = {"input": {"topic": "synthetic stored input"}}
    reads = []

    class Query:
        def __init__(self, filters):
            self.filters = filters

        def filter(self, **filters):
            return Query({**self.filters, **filters})

        async def values(self, *columns):
            reads.append((self.filters, columns))
            return [identity] if columns else ([] if changed else [payload])

    monkeypatch.setattr(module, "get_model", lambda _: SimpleNamespace(filter=lambda **kw: Query(kw)))
    monkeypatch.setattr(module, "_row_to_run_dict", lambda row: row)

    async def reattach():
        supplied_actor = actor.replace("-", "").upper() if actor is not None else None
        return await module.RunStore().load(
            run_id, resolve_inputs=False, resolve_output=False, reattach_as=(supplied_actor, org)
        )

    if changed:
        with pytest.raises(module.RunReattachRefused, match="changed while retrying"):
            await reattach()
    else:
        assert await reattach() == payload
    actor_filter = {"created_by": actor} if has_actor else {"created_by__isnull": True}
    assert reads == [
        ({"id": run_id}, ("created_by", "organization_id", "deleted_at")),
        ({"id": run_id, "organization_id": org, "deleted_at__isnull": True, **actor_filter}, ()),
    ]


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
    # Id-only RETURNING: the whole row is megabytes of jsonb (2026-11-02, workflow.run timeouts).
    assert updates.pop("returning") == module.RUN_UPDATE_RETURNS
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
            seen.setdefault("filters", filters)
            seen.setdefault("updates", updates)
            return SimpleNamespace(rows_affected=1)

        def filter(self, **_filters: object) -> SimpleNamespace:
            async def values(*_cols: str) -> list[dict[str, object]]:
                return []  # no called workflows under this run

            return SimpleNamespace(values=values)

    monkeypatch.setattr(module, "get_model", lambda name: Model())

    assert await module.RunStore().mark_cancelling(run_id) is True
    assert seen["filters"] == {
        "id": run_id,
        "status__in": ["pending", "running", "pausing"],
    }
    assert seen["updates"] == {"status": "cancelling", "returning": module.RUN_UPDATE_RETURNS}


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


def _family(monkeypatch: pytest.MonkeyPatch, root_status: str = "running"):
    """A run, its live called workflows (``metadata.subgraph_parent``, down the ``parent_run_id``
    chain), a finished one, a parked one, and a fork of the run with its own called child."""
    root, child, grandchild, done_child, parked, fork, fork_child = (str(uuid4()) for _ in range(7))
    called = {"subgraph_parent": {"run_id": "x"}}
    rows = {
        root: {"id": root, "parent_run_id": None, "status": root_status, "metadata": {}},
        child: {"id": child, "parent_run_id": root, "status": "running", "metadata": called},
        grandchild: {"id": grandchild, "parent_run_id": child, "status": "pending", "metadata": called},
        done_child: {"id": done_child, "parent_run_id": root, "status": "completed", "metadata": called},
        parked: {"id": parked, "parent_run_id": root, "status": "paused", "metadata": called},
        fork: {"id": fork, "parent_run_id": root, "status": "running", "metadata": {"_forked_from": root}},
        fork_child: {"id": fork_child, "parent_run_id": fork, "status": "running", "metadata": called},
    }

    class Model:
        async def update_where(self, filters: dict[str, object], **updates: object) -> SimpleNamespace:
            ids = [filters["id"]] if "id" in filters else list(filters["id__in"])  # type: ignore[arg-type]
            hit = 0
            for rid in ids:
                if rows[str(rid)]["status"] in filters["status__in"]:  # type: ignore[operator]
                    if "status" in updates:
                        rows[str(rid)]["status"] = updates["status"]
                    merge = updates.get("metadata")
                    if merge is not None:
                        rows[str(rid)]["metadata"] = {**rows[str(rid)]["metadata"], **merge.value}  # type: ignore[attr-defined]
                    hit += 1
            return SimpleNamespace(rows_affected=hit)

        def filter(
            self, *, parent_run_id__in: list[str], status__in: list[str], deleted_at: object,
            metadata__json_has_key: str,
        ) -> SimpleNamespace:
            async def values(*_cols: str) -> list[dict[str, object]]:
                return [
                    {"id": r["id"]}
                    for r in rows.values()
                    if r["parent_run_id"] in parent_run_id__in
                    and r["status"] in status__in
                    and metadata__json_has_key in r["metadata"]
                ]

            return SimpleNamespace(values=values)

    async def _status(_self: object, run_id: str) -> str | None:
        return rows[run_id]["status"]

    async def _merge(_self: object, run_id: str, patch: dict[str, object]) -> None:
        rows[run_id]["metadata"] = {**rows[run_id]["metadata"], **patch}

    monkeypatch.setattr(module, "get_model", lambda name: Model())
    monkeypatch.setattr(module.RunStore, "control_status", _status)
    monkeypatch.setattr(module.RunStore, "merge_metadata", _merge)
    return rows, (root, child, grandchild, done_child, parked, fork, fork_child)


@pytest.mark.asyncio
async def test_a_graceful_stop_lets_a_called_workflow_already_working_finish(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """G1 ruling (2026-11-01, plan § B1): a graceful Stop stops THIS run only. A called workflow
    already working for one of its steps finishes its whole chain, saves included — before, the
    cancel cascaded and cut it off at its next step, so the save at its end never ran."""
    rows, (root, child, grandchild, *_rest) = _family(monkeypatch)
    assert await module.RunStore().mark_cancelling(root) is True
    assert rows[root]["status"] == "cancelling"
    assert rows[child]["status"] == "running" and rows[grandchild]["status"] == "pending"
    assert "_hard_stop" not in rows[root]["metadata"]


@pytest.mark.asyncio
@pytest.mark.parametrize(("root_status", "why"), [("running", "stop_now"), ("cancelling", "second_stop")])
async def test_a_hard_stop_reaches_every_live_called_workflow_and_says_so(
    monkeypatch: pytest.MonkeyPatch, root_status: str, why: str,
) -> None:
    """"Stop now", or a second Stop on a run already stopping, is HARD: the run and each LIVE called
    workflow under it go to cancelling, every one stamped ``metadata._hard_stop`` (the run's end status
    names it). A fork / re-run of the run also carries ``parent_run_id`` and is a run of its own: never
    cancelled with its source (review of 118310e66)."""
    rows, (root, child, grandchild, done_child, parked, fork, fork_child) = _family(monkeypatch, root_status)

    assert await module.RunStore().mark_cancelling(root, hard=True, why=why) is True
    assert {rid: r["status"] for rid, r in rows.items()} == {
        root: "cancelling",
        child: "cancelling",
        grandchild: "cancelling",
        done_child: "completed",
        parked: "paused",
        fork: "running",
        fork_child: "running",
    }
    assert rows[root]["metadata"]["_hard_stop"]["why"] == why
    for rid in (child, grandchild):
        assert rows[rid]["metadata"]["_hard_stop"]["by"] == root, rid
    assert "_hard_stop" not in rows[fork_child]["metadata"]


@pytest.mark.asyncio
async def test_a_hard_stop_on_a_run_that_ended_does_nothing(monkeypatch: pytest.MonkeyPatch) -> None:
    rows, (root, child, *_rest) = _family(monkeypatch, "completed")
    assert await module.RunStore().mark_cancelling(root, hard=True) is False
    assert rows[child]["status"] == "running" and "_hard_stop" not in rows[root]["metadata"]


@pytest.mark.asyncio
async def test_a_failed_cascade_never_fails_the_cancel(monkeypatch: pytest.MonkeyPatch) -> None:
    class Model:
        async def update_where(self, filters: dict[str, object], **updates: object) -> SimpleNamespace:
            return SimpleNamespace(rows_affected=1)

        def filter(self, **_filters: object) -> SimpleNamespace:
            async def values(*_cols: str) -> list[dict[str, object]]:
                raise ConnectionError("database went away")

            return SimpleNamespace(values=values)

    async def _merge(_self: object, _run_id: str, _patch: dict[str, object]) -> None:
        return None

    monkeypatch.setattr(module, "get_model", lambda name: Model())
    monkeypatch.setattr(module.RunStore, "merge_metadata", _merge)
    assert await module.RunStore().mark_cancelling(str(uuid4()), hard=True) is True
