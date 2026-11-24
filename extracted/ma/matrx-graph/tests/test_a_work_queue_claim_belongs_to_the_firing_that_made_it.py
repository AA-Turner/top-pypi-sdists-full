"""A work-queue claim belongs to the queue FIRING that made it.

Review findings on 076b1961 (the draining-queue fix, 2026-10-31):

1. A CONDITIONAL edge off a draining queue was pruned on every non-final wave
   (its predicate read ``done: false``) — the same early release of the join
   behind ``done`` that the handle fix closed, one branch earlier.
2. ``release_wave_claims`` matched (run, set, wave >= N) and ignored WHO
   claimed: a second queue on the same set name, a second delivery into the
   queue's ``in`` (wave restarts at 0) or a queue inside a fan-out freed a
   live firing's in-flight claims and ran those items twice. A release now
   frees only the claims of the firing being re-executed (its stable firing
   identity rides the claim holder).
3. Every release burned an attempt: a run resumed by a deploy every 30 minutes
   walked its items into dead-letter. A release gives the attempt back.
4. Released claims were logged as "reclaimed expired lease(s)".
5. ``complete``/``fail`` accepted a result from a worker whose claim had been
   released — a stale worker could overwrite the live re-claim's outcome. The
   claim token (the claiming firing's dispatch id) must match.
"""

from __future__ import annotations

import logging
from collections import Counter
from uuid import uuid4

import pytest

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    MemoryWorkSetStore,
    RunStatus,
    Scheduler,
    compile_graph,
    configure_work_set_store,
)
from matrx_graph.workset import WorkItemSeed, work_claim_holder
from tests._fixtures import FakeEmitter, make_app_context
from tests.test_a_draining_queue_never_releases_its_done_early import (
    ITEMS,
    _assert_joined_once_after_drain,
    _definition,
    _edge,
    _Join,
    _node,
    _registry,
    _Worker,
)


@pytest.fixture(autouse=True)
def _fresh_store():
    configure_work_set_store(MemoryWorkSetStore())
    yield
    configure_work_set_store(None)


async def _run(definition: Definition, worker: _Worker, join: _Join) -> None:
    registry = _registry(worker, join)
    scheduler = Scheduler(
        compile_graph(definition, registry=registry),
        MemoryCheckpointer(),
        make_app_context(FakeEmitter()),
        registry=registry,
    )
    result = await scheduler.run(run_id=str(uuid4()), max_steps=200)
    assert result.status is RunStatus.COMPLETED, result.error


# 1 ---------------------------------------------------------------------------


async def test_a_conditional_edge_off_a_draining_queue_waits_for_the_drain():
    raw = _definition().model_dump(mode="json", by_alias=True)
    for edge in raw["edges"]:
        if edge["id"] == "e_drain_wait":
            edge["data"] = {**edge["data"], "kind": "conditional", "condition": "inputs['done']"}
    worker = _Worker()
    join = _Join(worker)
    await _run(Definition.model_validate(raw), worker, join)
    _assert_joined_once_after_drain(join)


# 2 ---------------------------------------------------------------------------


async def test_two_queues_on_one_set_never_free_each_others_claims():
    worker = _Worker()
    join = _Join(worker)
    definition = Definition.model_validate(
        {
            "nodes": [
                _node("go", "test.dq_echo", inp={"handed_on": "from-go"}),
                _node(
                    "seed",
                    "control.work_seed",
                    {"key_template": "$item.key"},
                    {"items": [{"key": k} for k in ITEMS]},
                ),
                _node(
                    "drain_a", "control.work_queue", {"target_node_id": "ingest", "batch_size": 2}
                ),
                _node(
                    "drain_b", "control.work_queue", {"target_node_id": "ingest", "batch_size": 2}
                ),
                {
                    **_node("ingest", "test.dq_worker"),
                    "data": {"config": {}, "on_item_failure": "hole"},
                },
            ],
            "edges": [
                _edge("e_go_seed", "go", "seed", "control"),
                _edge("e_seed_a", "seed", "drain_a", "control"),
                _edge("e_seed_b", "seed", "drain_b", "control"),
            ],
            "entry_nodes": ["go"],
        }
    )
    await _run(definition, worker, join)
    twice = {k: n for k, n in Counter(worker.done).items() if n > 1}
    assert not twice, f"one queue freed the other's live claims — items ran twice: {twice}"
    assert sorted(worker.done) == sorted(ITEMS)


async def test_a_release_frees_only_the_claims_of_its_own_firing():
    store = MemoryWorkSetStore()
    run = str(uuid4())
    await store.append(run, "s", [WorkItemSeed(canonical_key=k) for k in ITEMS])
    mine = await store.claim(
        run, "s", limit=2, holder=work_claim_holder("fire-A", "t1"), lease_seconds=600, wave=1
    )
    theirs = await store.claim(
        run, "s", limit=2, holder=work_claim_holder("fire-B", "t2"), lease_seconds=600, wave=1
    )
    # Same set, same wave, a different firing (another queue, a fan-out
    # sibling, a second delivery): never mine to release.
    released = await store.release_firing_claims(run, "s", "fire-A")
    assert released == len(mine)
    counts = await store.counts(run, "s")
    assert counts.in_progress == len(theirs), counts
    for claim in theirs:
        assert await store.complete(claim.id, run_id=run, claim_token="t2")


# 3 ---------------------------------------------------------------------------


async def test_a_release_gives_the_attempt_back():
    store = MemoryWorkSetStore()
    run = str(uuid4())
    await store.append(run, "s", [WorkItemSeed(canonical_key="only", max_attempts=2)])
    for deploy in range(10):  # a long run, resumed by a deploy every 30 minutes
        [claim] = await store.claim(
            run,
            "s",
            limit=1,
            holder=work_claim_holder("fire", f"t{deploy}"),
            lease_seconds=600,
            wave=1,
        )
        assert claim.attempts == 1, f"release #{deploy} kept the attempt: {claim.attempts}"
        assert await store.release_firing_claims(run, "s", "fire") == 1
    counts = await store.counts(run, "s")
    assert counts.pending == 1 and counts.dead_letter == 0, counts


# 4 ---------------------------------------------------------------------------


async def test_a_released_claim_is_not_logged_as_an_expired_lease(caplog):
    # Drive the kill/resume scenario of the guard file: the resumed wave
    # releases the claims its dead execution made.
    from tests.test_a_draining_queue_never_releases_its_done_early import (
        test_a_kill_mid_drain_resumes_and_finishes_the_drain,
    )

    with caplog.at_level(logging.INFO, logger="matrx_graph.nodes.control.work_queue"):
        await test_a_kill_mid_drain_resumes_and_finishes_the_drain()
    messages = [r.getMessage() for r in caplog.records]
    assert not any("expired" in m for m in messages), messages
    assert any("released" in m and "interrupted execution" in m for m in messages), messages


# 5 ---------------------------------------------------------------------------


async def test_a_worker_whose_claim_was_released_cannot_settle_the_item():
    store = MemoryWorkSetStore()
    run = str(uuid4())
    await store.append(run, "s", [WorkItemSeed(canonical_key="only")])
    [stale] = await store.claim(
        run, "s", limit=1, holder=work_claim_holder("fire", "dead"), lease_seconds=600, wave=1
    )
    await store.release_firing_claims(run, "s", "fire")
    # Released and still pending: the stale worker may not settle it.
    assert not await store.complete(stale.id, run_id=run, claim_token="dead")
    [live] = await store.claim(
        run, "s", limit=1, holder=work_claim_holder("fire", "live"), lease_seconds=600, wave=1
    )
    assert live.id == stale.id
    # Re-claimed by the live execution: the stale worker still may not.
    assert not await store.complete(stale.id, run_id=run, claim_token="dead")
    assert not await store.fail(stale.id, run_id=run, claim_token="dead", error={"code": "late"})
    assert (await store.counts(run, "s")).in_progress == 1
    assert await store.complete(live.id, run_id=run, claim_token="live")
    assert (await store.counts(run, "s")).succeeded == 1
