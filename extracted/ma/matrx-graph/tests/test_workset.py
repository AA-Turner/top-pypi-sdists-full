"""Durable work sets (matrx_graph.workset) — incremental work discovery.

Proves the headline capability of the dynamic-topology task: a run whose
TOTAL work is unknown at start. A seeder discovers wave 1; workers processing
wave 1 discover MORE items (control.work_seed mid-run); the queue keeps
claiming until the set drains, then fires `done` exactly once with the final
tally. Also covers dedup, the settle hook (engine marks items at
outcome-record time), failure settling, and store semantics.
"""

from __future__ import annotations

from typing import ClassVar
from uuid import uuid4

import pytest
from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    MemoryWorkSetStore,
    NodeRegistry,
    RunStatus,
    Scheduler,
    WorkItemSeed,
    compile_graph,
    configure_work_set_store,
    register_builtin_nodes,
)
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success
from matrx_graph.workset import canonical_key_for, get_work_set_store
from pydantic import BaseModel, ConfigDict

from tests._fixtures import FakeEmitter, make_app_context


@pytest.fixture(autouse=True)
def _fresh_store():
    configure_work_set_store(MemoryWorkSetStore())
    yield
    configure_work_set_store(None)


class _AnyIO(BaseModel):
    model_config = ConfigDict(extra="allow")


class _NoConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _CrawlWorker:
    """Processes one 'page'; pages may declare children discovered mid-run.

    ``pages`` maps url -> list of child urls. Processing a page appends its
    children to the SAME work set via the store (equivalent to a downstream
    control.work_seed, but inline so the test graph stays two nodes).
    """

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.crawl_worker",
        category=NodeCategory.DATA,
        display_name="Crawl worker",
        description="Processes one item; may discover children.",
        input_schema=_AnyIO,
        output_schema=_AnyIO,
        config_schema=_NoConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT, required=False),
        ),
        determinism=ActionTier.NON_DETERMINISTIC,
    )

    def __init__(
        self,
        pages: dict[str, list[str]],
        fail_urls: set[str] | None = None,
    ) -> None:
        self.pages = pages
        self.fail_urls = fail_urls or set()
        self.processed: list[str] = []

    async def execute(
        self, ctx: NodeExecutionContext, inputs: _AnyIO, _config: _NoConfig
    ) -> NodeResult[_AnyIO]:
        url = inputs.model_dump(mode="json")["value"]["url"]
        self.processed.append(url)
        if url in self.fail_urls:
            return failure("crawl_failed", f"failed to crawl {url}")
        children = self.pages.get(url, [])
        if children:
            store = get_work_set_store()
            await store.append(
                ctx.run_id,
                "default",
                [WorkItemSeed(canonical_key=child, payload={"url": child}) for child in children],
                discovered_by=ctx.node_id,
            )
        return success(_AnyIO(url=url))


class _Report:
    """Echo terminal node — records the done-handle payload."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.report",
        category=NodeCategory.DATA,
        display_name="Report",
        description="Echoes inputs.",
        input_schema=_AnyIO,
        output_schema=_AnyIO,
        config_schema=_NoConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT, required=False),
        ),
        determinism=ActionTier.PURE,
    )

    async def execute(
        self, _ctx: NodeExecutionContext, inputs: _AnyIO, _config: _NoConfig
    ) -> NodeResult[_AnyIO]:
        return success(_AnyIO(**inputs.model_dump(mode="json")))


def _crawl_definition(seed_urls: list[str]) -> Definition:
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "seed",
                    "type": "control.work_seed",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "config": {"key_template": "$item.url"},
                        "input": {"items": [{"url": u} for u in seed_urls]},
                    },
                },
                {
                    "id": "queue",
                    "type": "control.work_queue",
                    "position": {"x": 200, "y": 0},
                    "data": {"config": {"target_node_id": "crawl", "batch_size": 2}},
                },
                {
                    "id": "crawl",
                    "type": "test.crawl_worker",
                    "position": {"x": 400, "y": 0},
                    "data": {"config": {}, "on_item_failure": "hole"},
                },
                {
                    "id": "report",
                    "type": "test.report",
                    "position": {"x": 600, "y": 0},
                    "data": {"config": {}},
                },
            ],
            "edges": [
                {
                    "id": "e_seed_queue",
                    "source": "seed",
                    "target": "queue",
                    "data": {},
                },
                {
                    "id": "e_queue_done",
                    "source": "queue",
                    "sourceHandle": "done",
                    "target": "report",
                    "data": {"mappings": {"value": "$FULL_PAYLOAD"}},
                },
            ],
            "entry_nodes": ["seed"],
        }
    )


def _registry(worker: _CrawlWorker) -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    reg.register(worker, overwrite=True)
    reg.register(_Report(), overwrite=True)
    return reg


def _scheduler(definition: Definition, registry: NodeRegistry) -> Scheduler:
    return Scheduler(
        compile_graph(definition, registry=registry),
        MemoryCheckpointer(),
        make_app_context(FakeEmitter()),
        registry=registry,
    )


# ---------------------------------------------------------------------------
# The headline: total unknown at start, waves discovered while processing
# ---------------------------------------------------------------------------


async def test_wave_discovery_drains_multi_level_tree():
    # a -> a1, a2 ; a1 -> a1x — three waves deep, 5 total from 2 seeds.
    worker = _CrawlWorker(pages={"a": ["a1", "a2"], "a1": ["a1x"], "b": []})
    definition = _crawl_definition(["a", "b"])
    scheduler = _scheduler(definition, _registry(worker))
    result = await scheduler.run(run_id=str(uuid4()))
    assert result.status is RunStatus.COMPLETED, result.error
    assert sorted(worker.processed)[:5] == ["a", "a1", "a1x", "a2", "b"]
    # Every discovered item settled succeeded.
    store = get_work_set_store()
    # report ran once, from the done handle, with the final tally. A
    # Send-driven firing delivers in the §4.4 aggregated-dispatch shape
    # (items list, one entry for the queue's final firing).
    done_payload = result.last_outputs.get("report")
    assert done_payload is not None
    [done_item] = done_payload["items"]
    assert done_item["status"] == "succeeded"
    # The done handle fires ONLY when the queue has drained: its payload is the final tally.
    assert done_item["value"]["value"] == {"discovered": 5, "succeeded": 5, "failed": 0}
    counts = await store.counts(result.run_id, "default")
    assert counts.pending == 0
    assert counts.in_progress == 0
    assert counts.succeeded == 5
    assert counts.discovered == 5


async def test_dedup_rediscovery_is_noop():
    # Both seeds point at the same child — it must process exactly once.
    worker = _CrawlWorker(pages={"a": ["shared"], "b": ["shared"]})
    definition = _crawl_definition(["a", "b"])
    scheduler = _scheduler(definition, _registry(worker))
    result = await scheduler.run(run_id=str(uuid4()))
    assert result.status is RunStatus.COMPLETED, result.error
    assert worker.processed.count("shared") == 1
    counts = await get_work_set_store().counts(result.run_id, "default")
    assert counts.discovered == 3


async def test_failed_item_settles_failed_and_run_completes_with_hole():
    worker = _CrawlWorker(pages={"a": [], "b": []}, fail_urls={"b"})
    definition = _crawl_definition(["a", "b"])
    scheduler = _scheduler(definition, _registry(worker))
    result = await scheduler.run(run_id=str(uuid4()))
    # crawl has on_item_failure='hole' — the failed item becomes a hole, the
    # queue drains (failed counts as settled), and the run completes.
    assert result.status is RunStatus.COMPLETED, result.error
    counts = await get_work_set_store().counts(result.run_id, "default")
    assert counts.succeeded == 1
    assert counts.failed == 1
    assert counts.drained


# ---------------------------------------------------------------------------
# Store semantics
# ---------------------------------------------------------------------------


async def test_memory_store_claim_lease_and_reclaim():
    store = MemoryWorkSetStore()
    run_id = str(uuid4())
    await store.append(
        run_id,
        "default",
        [WorkItemSeed(canonical_key="k1", payload={"n": 1}, max_attempts=2)],
    )
    claims = await store.claim(run_id, "default", limit=10, holder="h", lease_seconds=-1, wave=1)
    assert len(claims) == 1
    # Lease already expired (negative) — reclaim returns it to pending.
    assert await store.reclaim_expired(run_id, "default") == 1
    counts = await store.counts(run_id, "default")
    assert counts.pending == 1
    # Second claim + expiry exhausts max_attempts=2 → dead_letter.
    await store.claim(run_id, "default", limit=10, holder="h", lease_seconds=-1, wave=2)
    assert await store.reclaim_expired(run_id, "default") == 1
    counts = await store.counts(run_id, "default")
    assert counts.dead_letter == 1
    assert counts.drained


async def test_settle_idempotent():
    store = MemoryWorkSetStore()
    run_id = str(uuid4())
    await store.append(run_id, "default", [WorkItemSeed(canonical_key="k")])
    [claim] = await store.claim(run_id, "default", limit=1, holder="h", lease_seconds=60, wave=1)
    assert await store.complete(claim.id, run_id=run_id) is True
    assert await store.complete(claim.id, run_id=run_id) is False
    assert await store.fail(claim.id, run_id=run_id) is False


def test_canonical_key_stable():
    assert canonical_key_for({"b": 1, "a": 2}) == canonical_key_for({"a": 2, "b": 1})
    assert canonical_key_for("x") != canonical_key_for("y")
