"""Integration tests for PostgresCheckpointer, DefinitionStore, and RunStore.

Skipped automatically when MATRX_GRAPH_TEST_DB is unset. To run locally:

    export MATRX_GRAPH_TEST_DB=1
    # ensure `.env` has SUPABASE_MATRIX_* set for matrx-orm
    # ensure the 0001_wf_initial.sql migration has been applied
    uv run --package matrx-graph pytest \
        packages/matrx-graph/tests/test_postgres_checkpointer.py -v

The tests create + tear down their own definitions and runs, so they're
safe to run against a dev DB (no shared fixture state). They never touch
wf_* rows owned by other runs.
"""

from __future__ import annotations

import os
from uuid import uuid4

import pytest
from pydantic import BaseModel, ConfigDict

# Load the repo .env HERE, above the gate. The skip decision below reads
# process env, and other suites (anything importing aidream.config) load .env
# as an import side effect — so without this line the same commit skips when
# this file is collected alone and runs when it is collected second.
# Guard: scripts/check_test_gate_determinism.py
from dotenv import load_dotenv

load_dotenv()


pytestmark = [
    pytest.mark.skipif(
        not os.environ.get("MATRX_GRAPH_TEST_DB"),
        reason="Set MATRX_GRAPH_TEST_DB=1 to run PostgresCheckpointer integration tests.",
    ),
    # All tests share matrx-orm's registered asyncpg pool. Keep that pool on one
    # event loop instead of tearing its SSL transports down between test loops.
    pytest.mark.asyncio(loop_scope="session"),
]

# wf_definition / wf_run carry user_id NOT NULL (root migration 0052) with an
# auth.users FK, so test rows need a REAL user — without it every test here
# dies on NotNullViolation (this suite was silently dead from 0052 until
# 2026-06-11 because the env gate skipped it everywhere). Default: the
# platform's agent user (same row matrx-feedback attributes to). Override via
# MATRX_GRAPH_TEST_USER_ID.
TEST_USER_ID = os.environ.get("MATRX_GRAPH_TEST_USER_ID", "87a6e699-3622-4869-8843-d0867456c0dd")
TEST_ORGANIZATION_ID = os.environ.get(
    "MATRX_GRAPH_TEST_ORGANIZATION_ID", "3e790542-fdaf-40b2-8bf3-658bf94fe67f"
)


@pytest.fixture(scope="module", autouse=True)
def _bootstrap_db() -> None:
    """Register the aidream database so matrx-orm's pool can be acquired.

    HARD-FAILS via the production refusal gate if SUPABASE_MATRIX_* points
    at the production project — this suite writes real workflow.* rows
    (see tests/_db_guard.py; escape hatch MATRX_ALLOW_PROD_DB_TESTS=1).
    """
    from dotenv import load_dotenv

    load_dotenv()

    from matrx_orm import register_platform_db

    register_platform_db(
        "supabase_automation_matrix",
        package="matrx-graph tests",
        additional_schemas=["auth"],
    )

    from ._db_guard import assert_not_production_db

    assert_not_production_db("supabase_automation_matrix")

    # Registration configures the connection only. These tests bootstrap the
    # package's standalone schema, so wire Models that match that schema rather
    # than aidream's host-enriched Models.
    from matrx_graph.db import configure_standalone_db, reset_for_tests

    reset_for_tests()
    configure_standalone_db("supabase_automation_matrix")


async def test_definition_store_roundtrip():
    from matrx_graph import Definition, NodeDef, Position
    from matrx_graph.db import DefinitionStore
    from matrx_graph.types.variables import VariableSpec

    store = DefinitionStore()
    name = f"test-wf-{uuid4()}"
    definition = Definition(
        nodes=[
            NodeDef(
                id="n1",
                type="data.transform",
                position=Position(x=0, y=0),
                data={"config": {"expression": "inputs['x'] + 1"}},
            )
        ],
        variables=[
            VariableSpec(name="topic", description="Subject", default="physics"),
            VariableSpec(name="audience"),
        ],
    )

    created = await store.create(name=name, definition=definition, user_id=TEST_USER_ID)
    try:
        assert created.name == name
        assert created.version == 1
        assert len(created.definition.nodes) == 1

        loaded = await store.load(created.id)
        assert loaded is not None
        assert loaded.name == name
        assert loaded.definition.nodes[0].type == "data.transform"
        # Declared run variables must survive the round-trip — the store
        # silently DROPPED them before 0024_definition_variables.sql.
        assert [v.name for v in loaded.definition.variables] == ["topic", "audience"]
        assert loaded.definition.variables[0].default == "physics"

        # Save draft — `version` is the canonical ROW REVISION, not a publish
        # counter, so every content write bumps it (platform._touch_row hosted,
        # the store's explicit F("version") + 1 standalone). Publish snapshots
        # label themselves with the revision at publish time; they are not
        # numbered 1, 2, 3.
        updated_def = Definition(
            nodes=[
                NodeDef(
                    id="n1",
                    type="data.transform",
                    position=Position(x=10, y=20),
                    data={"config": {"expression": "inputs['x'] * 2"}},
                )
            ]
        )
        drafted = await store.save_draft(created.id, definition=updated_def)
        assert drafted.version == 2
        assert drafted.definition.nodes[0].position.x == 10
        assert drafted.definition.variables == []  # draft replaced them

        v1_vars = await store.load(created.id, is_version=True, version_number=1)
        assert v1_vars is not None
        assert [v.name for v in v1_vars.definition.variables] == ["topic", "audience"]

        # Publish — bumps the revision again and snapshots it under that number;
        # the original v1 snapshot is preserved untouched.
        published = await store.publish(created.id, change_note="second version")
        assert published.version == 3

        v1 = await store.load(created.id, is_version=True, version_number=1)
        assert v1 is not None
        assert v1.is_version is True
        assert v1.definition.nodes[0].position.x == 0  # original v1 snapshot preserved

        versions = await store.list_versions(created.id)
        assert len(versions) == 2
        assert [v.version_number for v in versions] == [3, 1]
    finally:
        await store.archive(created.id)


async def test_postgres_checkpointer_save_load_outcome():
    from matrx_graph import Definition
    from matrx_graph.checkpoint import PostgresCheckpointer
    from matrx_graph.checkpoint.protocol import (
        Checkpoint,
        NextInvocation,
        NodeOutcome,
        PendingBinding,
        PendingEdgeBinding,
    )
    from matrx_graph.db import DefinitionStore, RunStore
    from matrx_graph.types.send import Send

    checkpointer = PostgresCheckpointer()
    def_store = DefinitionStore()
    run_store = RunStore()

    # Definition + run must exist for wf_checkpoint FKs to hold
    definition = Definition()
    definition_row = await def_store.create(
        name=f"chk-test-{uuid4()}", definition=definition, user_id=TEST_USER_ID
    )
    run_id = await run_store.create(
        definition_id=definition_row.id,
        definition_hash="test-hash",
        inputs={"x": 1},
        user_id=TEST_USER_ID,
        organization_id=TEST_ORGANIZATION_ID,
    )

    try:
        cp = Checkpoint(
            checkpoint_id=str(uuid4()),
            run_id=run_id,
            thread_id=run_id,
            step=0,
            channel_values={"counter": 5, "log": ["a", "b"]},
            # Join accumulator (ENGINE_SPEC §3.8) — replaced the dead
            # pending_writes field; must round-trip through the JSONB column.
            pending_bindings={
                "join_node": PendingBinding(
                    firing=2,
                    edges={
                        "e_a": PendingEdgeBinding(
                            state="delivered",
                            payload={"x": "A-VAL"},
                            source_node_id="a",
                            source_step=0,
                        ),
                        "e_b": PendingEdgeBinding(
                            state="pruned",
                            source_node_id="b",
                            source_step=0,
                        ),
                    },
                )
            },
            next_invocations=[
                NextInvocation(node_id="worker", inputs={"name": "alpha"}, attempt=1)
            ],
        )
        await checkpointer.save_checkpoint(cp)

        loaded = await checkpointer.load_checkpoint(cp.checkpoint_id)
        assert loaded is not None
        assert loaded.channel_values == {"counter": 5, "log": ["a", "b"]}
        assert loaded.next_invocations[0].node_id == "worker"
        assert loaded.next_invocations[0].inputs == {"name": "alpha"}
        assert loaded.pending_bindings == cp.pending_bindings

        latest = await checkpointer.latest_checkpoint(run_id)
        assert latest is not None
        assert latest.checkpoint_id == cp.checkpoint_id

        # Outcome record — with a Send in it
        outcome = NodeOutcome(
            run_id=run_id,
            step=0,
            node_id="producer",
            attempt=1,
            output={"result": 42},
            channel_writes=[("counter", 1), ("log", "hi")],
            sends=[Send(target_node_id="worker", payload={"name": "alpha"})],
            duration_ms=123,
        )
        await checkpointer.record_outcome(outcome)

        fetched = await checkpointer.get_outcome(run_id, 0, "producer", 1)
        assert fetched is not None
        assert fetched.output == {"result": 42}
        assert len(fetched.sends) == 1
        assert fetched.sends[0].target_node_id == "worker"
        assert fetched.duration_ms == 123

        # Idempotency — re-record same key with new output should upsert
        outcome2 = NodeOutcome(
            run_id=run_id,
            step=0,
            node_id="producer",
            attempt=1,
            output={"result": 99},
            duration_ms=456,
        )
        await checkpointer.record_outcome(outcome2)
        fetched2 = await checkpointer.get_outcome(run_id, 0, "producer", 1)
        assert fetched2 is not None
        assert fetched2.output == {"result": 99}
        assert fetched2.duration_ms == 456
    finally:
        # wf_run / wf_checkpoint / wf_node_outcome cascade via ON DELETE CASCADE
        # on wf_definition. Archiving the definition keeps the DB clean.
        await def_store.archive(definition_row.id)


async def test_end_to_end_scheduler_with_postgres_checkpointer():
    """Run a small graph end-to-end with PostgresCheckpointer and verify:
    - run completes
    - checkpoints are written
    - recorded outcomes round-trip
    - listing matches the step count
    """
    from matrx_connect.context.app_context import AppContext
    from matrx_graph import (
        Definition,
        NodeDef,
        Position,
        RunStatus,
        Scheduler,
        compile_graph,
        register_builtin_nodes,
    )
    from matrx_graph.checkpoint import PostgresCheckpointer
    from matrx_graph.db import DefinitionStore, RunStore

    register_builtin_nodes(overwrite=True)

    definition = Definition(
        nodes=[
            NodeDef(
                id="double",
                type="data.transform",
                position=Position(x=0, y=0),
                data={"config": {"expression": "inputs['value'] * 2"}},
            ),
            NodeDef(
                id="plus5",
                type="data.transform",
                position=Position(x=200, y=0),
                data={"config": {"expression": "inputs['result'] + 5"}},
            ),
        ],
        edges=[{"id": "e1", "source": "double", "target": "plus5"}],
    )

    def_store = DefinitionStore()
    run_store = RunStore()
    checkpointer = PostgresCheckpointer()

    def_row = await def_store.create(
        name=f"Weekly client recap {uuid4().hex[:6]}", definition=definition, user_id=TEST_USER_ID
    )
    try:
        graph = compile_graph(def_row.definition)
        run_id = await run_store.create(
            definition_id=def_row.id,
            definition_hash=graph.definition_hash,
            inputs={"value": 10},
            user_id=TEST_USER_ID,
            organization_id=TEST_ORGANIZATION_ID,
        )

        class _NoopEmitter:
            async def send_chunk(self, _): ...
            async def send_reasoning_chunk(self, _): ...
            async def send_phase(self, _): ...
            async def send_data(self, _): ...
            async def send_init(self, _): ...
            async def send_completion(self, _): ...
            async def send_error(self, *a, **k): ...
            async def send_tool_event(self, _): ...
            async def send_end(self): ...

        class _AppShim(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)

        # Use the real AppContext — lightweight for test
        app = AppContext(
            emitter=_NoopEmitter(),
            user_id="test-user",
            is_authenticated=True,
            conversation_id=run_id,
            request_id=run_id,
        )

        scheduler = Scheduler(graph, checkpointer, app)
        result = await scheduler.run(run_id=run_id, inputs={"value": 10})

        assert result.status is RunStatus.COMPLETED
        # 10 * 2 + 5 = 25
        assert result.last_outputs["plus5"]["result"] == 25

        checkpoints = await checkpointer.list_checkpoints(run_id)
        assert len(checkpoints) >= 2  # at least one per super-step

        # Outcomes were recorded for both nodes
        out_double = await checkpointer.get_outcome(run_id, 0, "double", 1)
        assert out_double is not None
        assert out_double.output["result"] == 20

        out_plus5 = await checkpointer.get_outcome(run_id, 1, "plus5", 1)
        assert out_plus5 is not None
        assert out_plus5.output["result"] == 25
    finally:
        await def_store.archive(def_row.id)


# ---------------------------------------------------------------------------
# Guarded status transitions (audit P1-1/2/3/4 — BS-2)
# ---------------------------------------------------------------------------


async def _make_run(def_store, run_store):
    from matrx_graph import Definition

    def_row = await def_store.create(
        name=f"transition-test-{uuid4()}",
        definition=Definition(),
        user_id=TEST_USER_ID,
    )
    run_id = await run_store.create(
        definition_id=def_row.id,
        definition_hash="t",
        inputs={},
        user_id=TEST_USER_ID,
        organization_id=TEST_ORGANIZATION_ID,
    )
    return def_row, run_id


async def test_claim_for_resume_exactly_one_winner():
    """THE double-recovery guard: two concurrent claims on one parked run —
    exactly one wins, the loser must 409 (audit P1-1)."""
    import asyncio

    from matrx_graph.db import DefinitionStore, RunStore

    def_store, run_store = DefinitionStore(), RunStore()
    def_row, run_id = await _make_run(def_store, run_store)
    try:
        await run_store.mark_errored(run_id, error={"message": "boom"})

        results = await asyncio.gather(
            run_store.claim_for_resume(run_id),
            run_store.claim_for_resume(run_id),
        )
        assert sorted(results) == [False, True]

        run = await run_store.load(run_id)
        assert run is not None and run["status"] == "running"
    finally:
        await def_store.archive(def_row.id)


async def test_transition_rejects_wrong_from_status():
    from matrx_graph.db import DefinitionStore, RunStore

    def_store, run_store = DefinitionStore(), RunStore()
    def_row, run_id = await _make_run(def_store, run_store)
    try:
        # run is 'running' — claiming as if paused must fail.
        assert (
            await run_store.transition(run_id, from_statuses=("paused",), to_status="running")
            is False
        )
    finally:
        await def_store.archive(def_row.id)


async def test_terminal_status_is_immutable():
    """completed/failed/cancelled never overwrite each other (P1-4)."""
    from matrx_graph.db import DefinitionStore, RunStore

    def_store, run_store = DefinitionStore(), RunStore()
    def_row, run_id = await _make_run(def_store, run_store)
    try:
        assert await run_store.mark_completed(run_id, output={"ok": True}, steps_executed=3)
        # A racing cancel/fail must be rejected...
        assert not await run_store.mark_cancelled(run_id, steps_executed=3)
        assert not await run_store.mark_failed(run_id, error={"message": "late failure"})
        run = await run_store.load(run_id)
        assert run is not None
        assert run["status"] == "completed"
        assert run["output"] == {"ok": True}
        # ...while an idempotent same-status rewrite still applies.
        assert await run_store.mark_completed(run_id, output={"ok": True}, steps_executed=3)
    finally:
        await def_store.archive(def_row.id)


async def test_recovery_counter_atomic_cap():
    """Concurrent bumps cannot overshoot max_recovery_retries (P1-3)."""
    import asyncio

    from matrx_graph.db import DefinitionStore, RunStore
    from matrx_graph.db.pool import acquire

    def_store, run_store = DefinitionStore(), RunStore()
    def_row, run_id = await _make_run(def_store, run_store)
    try:
        from uuid import UUID

        async with acquire() as conn:
            await conn.execute(
                "UPDATE workflow.run SET max_recovery_retries = 3 WHERE id = $1",
                UUID(run_id),
            )

        results = await asyncio.gather(*[run_store.bump_recovery_counter(run_id) for _ in range(6)])
        allowed = [r for r in results if r["allowed"]]
        denied = [r for r in results if not r["allowed"]]
        assert len(allowed) == 3
        assert len(denied) == 3
        assert max(r["count"] for r in allowed) == 3  # never past the cap
    finally:
        await def_store.archive(def_row.id)


async def test_event_store_concurrent_seq_assignment():
    """BS-3 (audit P1-5): per-run seq is unique, dense, and commit-ordered
    even under CONCURRENT inserts — the CTE serializes on the wf_run row
    lock. The after_seq cursor returns exactly the tail."""
    import asyncio

    from matrx_graph.db import DefinitionStore, EventStore, RunStore

    def_store, run_store = DefinitionStore(), RunStore()
    events = EventStore()
    def_row, run_id = await _make_run(def_store, run_store)
    try:
        seqs = await asyncio.gather(
            *[
                events.insert_event(
                    run_id,
                    event_type="node_started",
                    payload={"event": "node_started", "i": i},
                    node_id=f"n{i}",
                    step=0,
                    attempt=1,
                )
                for i in range(8)
            ]
        )
        assert sorted(seqs) == list(range(1, 9))  # dense, unique, 1-based

        tail = await events.list_events(run_id, after_seq=5)
        assert [r["seq"] for r in tail] == [6, 7, 8]

        # The previously-constraint-killed event types now land (0019).
        seq = await events.insert_event(
            run_id,
            event_type="run_errored",
            payload={"event": "run_errored"},
        )
        assert seq == 9
    finally:
        await def_store.archive(def_row.id)


# ---------------------------------------------------------------------------
# wf_job lease lifecycle — renewal, orphan reaper, dead-letter (audit P1-14)
# ---------------------------------------------------------------------------


async def _backdate_claim(job_id: str, *, attempt: int, seconds_expired: int = 600):
    """Simulate a worker that claimed the job and then died: claimed_at set,
    lease (visible_at) already expired. Never uses claim_one — that would
    steal real queued jobs from the shared dev DB."""
    from uuid import UUID

    from matrx_graph.db.pool import acquire

    async with acquire() as conn:
        await conn.execute(
            """
            UPDATE workflow.job
            SET claimed_at = now() - interval '1 hour',
                claimed_by = 'test-dead-worker',
                visible_at = now() - make_interval(secs => $2),
                attempt = $3
            WHERE id = $1
            """,
            UUID(job_id),
            float(seconds_expired),
            attempt,
        )


async def _load_job(job_id: str):
    from uuid import UUID

    from matrx_graph.db.pool import acquire

    async with acquire() as conn:
        return await conn.fetchrow("SELECT * FROM workflow.job WHERE id = $1", UUID(job_id))


async def _delete_job(job_id: str):
    from uuid import UUID

    from matrx_graph.db.pool import acquire

    async with acquire() as conn:
        await conn.execute("DELETE FROM workflow.job WHERE id = $1", UUID(job_id))


async def test_lease_reaper_requeues_dead_worker_job():
    """A worker death mid-job must NOT orphan the wf_job row forever: the
    reaper nulls the dead claim so claim_one can requeue it."""
    import json as _json

    from matrx_graph.db import DefinitionStore, RunStore
    from matrx_graph.workers.queue import enqueue, reap_expired_leases, renew_lease

    def_store, run_store = DefinitionStore(), RunStore()
    def_row, run_id = await _make_run(def_store, run_store)
    job_id = await enqueue(run_id=run_id, kind="start")
    try:
        # Attempts remaining → requeued.
        await _backdate_claim(job_id, attempt=1)
        await reap_expired_leases(grace_seconds=120)
        row = await _load_job(job_id)
        assert row["claimed_at"] is None and row["claimed_by"] is None
        err = row["last_error"]
        err = _json.loads(err) if isinstance(err, str) else err
        assert err["type"] == "lease_expired"

        # renew_lease on an unclaimed row reports lost ownership.
        assert await renew_lease(job_id) is False

        # A live lease (visible_at in the future) is never touched.
        await _backdate_claim(job_id, attempt=1, seconds_expired=-600)
        await reap_expired_leases(grace_seconds=120)
        row = await _load_job(job_id)
        assert row["claimed_at"] is not None  # still owned

        # And renewal keeps pushing the lease forward while claimed.
        assert await renew_lease(job_id) is True
    finally:
        await _delete_job(job_id)
        await def_store.archive(def_row.id)


async def test_lease_reaper_dead_letters_exhausted_job():
    """Dead worker + no attempts left → dead-letter (far-future visible_at),
    never silently requeued."""
    from datetime import UTC, datetime, timedelta

    from matrx_graph.db import DefinitionStore, RunStore
    from matrx_graph.workers.queue import enqueue, fail, reap_expired_leases

    def_store, run_store = DefinitionStore(), RunStore()
    def_row, run_id = await _make_run(def_store, run_store)
    job_id = await enqueue(run_id=run_id, kind="start")
    try:
        await _backdate_claim(job_id, attempt=3)  # max_attempts default = 3
        await reap_expired_leases(grace_seconds=120)
        row = await _load_job(job_id)
        assert row["claimed_at"] is None
        assert row["visible_at"] > datetime.now(UTC) + timedelta(days=365 * 50)

        # fail() at exhausted attempts must ALSO dead-letter (the old code
        # left visible_at at the lease deadline → infinite retry loop).
        await _backdate_claim(job_id, attempt=3)
        await fail(job_id, error={"type": "Boom", "message": "x"})
        row = await _load_job(job_id)
        assert row["claimed_at"] is None
        assert row["visible_at"] > datetime.now(UTC) + timedelta(days=365 * 50)
    finally:
        await _delete_job(job_id)
        await def_store.archive(def_row.id)
