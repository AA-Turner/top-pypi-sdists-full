"""Chaos proof for the durable work set: kill the executor mid-drain, recover.

Closes the acknowledged gap at matrx_graph/workers/FEATURE.md ("CI does not
kill a real workflow worker mid-run and prove zero dropped/duplicated side
effects after lease recovery") for the work-set path: a REAL scheduler run
over PostgresCheckpointer + PostgresWorkSetStore is HARD-CANCELLED mid-drain
(asyncio task cancellation ripping through the TaskGroup — the in-process
equivalent of process death), then a FRESH scheduler resumes from the
durable checkpoint and the run must finish with every item's side effect
having happened EXACTLY once.

The kill point is engineered so the proof is deterministic, not
probabilistic:

- items a..e, batch_size=1 (serial waves);
- the worker BLOCKS on item "c" before performing its side effect, so at
  kill time exactly one worker is unfinished and its side effect has not
  happened;
- the queue's next wave has already CLAIMED item "d" (in_progress in
  Postgres) but its dispatch dies with the killed step — "d" is the
  claimed-by-a-dead-holder orphan only lease reclaim can save.

Recovery therefore has to come from BOTH durability layers, each proven by
an observable only that layer can produce:

- the checkpoint frontier replays worker("c")  → "c" settles at attempts=1;
- reclaim_expired rescues orphaned "d" after its lease lapses → "d"
  re-claims at attempts=2.

Zero dropped: all five side effects present. Zero duplicated: each present
exactly once. Neither is reachable if any recovery layer drops or replays
work.

Skipped when MATRX_GRAPH_TEST_DB is unset (same gate + scratch-DB bootstrap
as test_postgres_checkpointer.py; production refuses via tests/_db_guard).
"""

from __future__ import annotations

import asyncio
import os
from typing import TYPE_CHECKING, Any, ClassVar
from uuid import UUID, uuid4

import pytest
from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from matrx_graph.types.node_spec import NodeSpec

from matrx_graph.workset import (
    PostgresWorkSetStore,
    configure_work_set_store,
)

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
        reason="Set MATRX_GRAPH_TEST_DB=1 to run the work-set chaos test.",
    ),
    pytest.mark.asyncio(loop_scope="session"),
]

TEST_USER_ID = os.environ.get("MATRX_GRAPH_TEST_USER_ID", "87a6e699-3622-4869-8843-d0867456c0dd")
TEST_ORGANIZATION_ID = os.environ.get(
    "MATRX_GRAPH_TEST_ORGANIZATION_ID", "3e790542-fdaf-40b2-8bf3-658bf94fe67f"
)


@pytest.fixture(scope="module", autouse=True)
def _bootstrap_db() -> None:
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

    from matrx_graph.db import configure_standalone_db, reset_for_tests

    reset_for_tests()
    configure_standalone_db("supabase_automation_matrix")


@pytest.fixture(autouse=True)
def _postgres_work_set_store():
    configure_work_set_store(PostgresWorkSetStore())
    yield
    configure_work_set_store(None)


class _AnyIO(BaseModel):
    model_config = ConfigDict(extra="allow")


class _NoConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _ChaosWorker:
    """Side effect = append the url to ``effects``. Item "c" blocks BEFORE
    its side effect while ``block_c`` is set — the deterministic kill
    window: at cancellation, c's side effect has not happened."""

    spec: ClassVar[NodeSpec] = None  # type: ignore[assignment]  # set below

    def __init__(self) -> None:
        self.effects: list[str] = []
        self.block_c = True
        self.holding_c = asyncio.Event()
        self.release_c = asyncio.Event()

    async def execute(self, _ctx, inputs, _config):
        from matrx_graph.types.result import success

        url = inputs.model_dump(mode="json")["value"]["url"]
        if url == "c" and self.block_c:
            self.holding_c.set()
            await self.release_c.wait()  # canceled here — never released
        self.effects.append(url)
        return success(_AnyIO(url=url))


def _build_worker_spec() -> Any:
    from matrx_graph.types.handle import HandleDirection, HandleSpec
    from matrx_graph.types.node_spec import NodeSpec
    from matrx_graph.types.primitives import ActionTier, NodeCategory

    return NodeSpec(
        type="test.chaos_worker",
        category=NodeCategory.DATA,
        display_name="Chaos worker",
        description="Processes one item; blocks on 'c' pre-side-effect.",
        input_schema=_AnyIO,
        output_schema=_AnyIO,
        config_schema=_NoConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT, required=False),
        ),
        determinism=ActionTier.NON_DETERMINISTIC,
    )


def _definition(urls: list[str]):
    from matrx_graph import Definition

    return Definition.model_validate(
        {
            "entry_nodes": ["seed"],
            "nodes": [
                {
                    "id": "seed",
                    "type": "control.work_seed",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "config": {"key_template": "$item.url"},
                        "input": {"items": [{"url": u} for u in urls]},
                    },
                },
                {
                    "id": "queue",
                    "type": "control.work_queue",
                    "position": {"x": 200, "y": 0},
                    "data": {
                        "config": {
                            "target_node_id": "work",
                            "batch_size": 1,
                            "lease_seconds": 3600,
                        }
                    },
                },
                {
                    "id": "work",
                    "type": "test.chaos_worker",
                    "position": {"x": 400, "y": 0},
                    "data": {"config": {}},
                },
            ],
            "edges": [
                {"id": "e_seed_queue", "source": "seed", "target": "queue", "data": {}},
            ],
        }
    )


async def _item_rows(run_id: str) -> dict[str, dict[str, Any]]:
    from matrx_graph.db._registry import get_model

    rows = await (
        get_model("WfWorkItem")
        .filter(run_id=run_id, set_name="default")
        .values("canonical_key", "state", "attempts", "lease_expires_at")
    )
    return {row["canonical_key"]: row for row in rows}


async def _expire_lease(run_id: str, canonical_key: str) -> None:
    """Simulate the orphaned item's lease lapsing (wall-clock fast-forward —
    the queue's own lease_seconds floor is 30s; the reclaim SQL under test
    still does all its real work against the real row)."""
    from matrx_graph.db.pool import acquire

    async with acquire() as conn:
        await conn.execute(
            """
            UPDATE workflow.work_item
            SET lease_expires_at = now() - interval '1 hour'
            WHERE run_id = $1 AND set_name = 'default' AND canonical_key = $2
            """,
            UUID(run_id),
            canonical_key,
        )


async def test_hard_kill_mid_drain_recovers_to_exactly_once_side_effects():
    from matrx_graph import (
        NodeRegistry,
        RunStatus,
        Scheduler,
        compile_graph,
        register_builtin_nodes,
    )
    from matrx_graph.checkpoint import PostgresCheckpointer
    from matrx_graph.db import DefinitionStore, RunStore

    from tests._fixtures import FakeEmitter, make_app_context

    worker = _ChaosWorker()
    type(worker).spec = _build_worker_spec()
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(worker, overwrite=True)

    urls = ["a", "b", "c", "d", "e"]
    definition = _definition(urls)
    graph = compile_graph(definition, registry=registry)

    def_store = DefinitionStore()
    run_store = RunStore()
    checkpointer = PostgresCheckpointer()

    def_row = await def_store.create(
        name=f"chaos-test-{uuid4()}", definition=definition, user_id=TEST_USER_ID
    )
    try:
        run_id = await run_store.create(
            definition_id=def_row.id,
            definition_hash=graph.definition_hash,
            inputs={},
            user_id=TEST_USER_ID,
            organization_id=TEST_ORGANIZATION_ID,
        )

        # ------------------------------------------------------------------
        # Phase 1 — run until the kill window, then HARD-KILL.
        # ------------------------------------------------------------------
        scheduler = Scheduler(
            graph, checkpointer, make_app_context(FakeEmitter()), registry=registry
        )
        run_task = asyncio.create_task(scheduler.run(run_id=run_id, max_steps=200))

        await asyncio.wait_for(worker.holding_c.wait(), timeout=30)
        # "c" is claimed and EXECUTING (side effect not yet performed). Give
        # the concurrently-firing queue wave a moment to claim "d" so the
        # kill also strands a claimed-but-never-dispatched orphan.
        for _ in range(200):
            rows = await _item_rows(run_id)
            if rows.get("d", {}).get("state") == "in_progress":
                break
            await asyncio.sleep(0.05)

        run_task.cancel()  # the kill — rips through the step TaskGroup
        with pytest.raises(asyncio.CancelledError):
            await run_task

        # The durable frontier survived the death, IN POSTGRES:
        rows = await _item_rows(run_id)
        assert rows["a"]["state"] == "succeeded"
        assert rows["b"]["state"] == "succeeded"
        assert rows["c"]["state"] == "in_progress"  # died holding it
        assert worker.effects == ["a", "b"]  # c's side effect never happened

        killed_in_progress = {k for k, r in rows.items() if r["state"] == "in_progress"}
        assert "c" in killed_in_progress
        # The kill MUST also strand a claimed-but-never-dispatched orphan —
        # otherwise the lease-reclaim layer below is never exercised and
        # this test proves less than it claims. If this fires, the kill
        # window closed before the next queue wave claimed "d".
        assert "d" in killed_in_progress, (
            f"no orphaned claim at kill time (in_progress={killed_in_progress}); "
            "the lease-recovery layer was not exercised"
        )

        latest = await checkpointer.latest_checkpoint(run_id)
        assert latest is not None

        # ------------------------------------------------------------------
        # Phase 2 — lease recovery + fresh-scheduler resume.
        # ------------------------------------------------------------------
        worker.block_c = False  # the replayed "c" runs to completion
        # Every item the dead executor still held lapses EXCEPT "c": "c" is
        # recovered by the checkpoint frontier replay (its lease is live),
        # the others only by reclaim_expired. Both layers must fire.
        for key in killed_in_progress - {"c"}:
            await _expire_lease(run_id, key)

        fresh = Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry)
        resumed = await fresh.resume(
            run_id=run_id, checkpoint_id=latest.checkpoint_id, max_steps=200
        )

        assert resumed.status is RunStatus.COMPLETED, resumed.error

        # THE chaos guarantee — zero dropped, zero duplicated side effects:
        assert sorted(worker.effects) == sorted(urls), (
            f"dropped or duplicated side effects after recovery: {worker.effects}"
        )
        assert len(worker.effects) == len(set(worker.effects))

        rows = await _item_rows(run_id)
        assert {k: r["state"] for k, r in rows.items()} == dict.fromkeys(urls, "succeeded")
        # "c" settled via the checkpoint-frontier replay of its original
        # claim — one claim, one attempt.
        assert rows["c"]["attempts"] == 1
        # Every lease-lapsed orphan needed a SECOND claim — the observable
        # only reclaim_expired (in_progress → pending → re-claim) produces.
        for key in killed_in_progress - {"c"}:
            assert rows[key]["attempts"] == 2, f"{key} was not lease-reclaimed"

        counts_probe = PostgresWorkSetStore()
        counts = await counts_probe.counts(run_id, "default")
        assert counts.succeeded == len(urls)
        assert counts.drained
    finally:
        await def_store.archive(def_row.id)
