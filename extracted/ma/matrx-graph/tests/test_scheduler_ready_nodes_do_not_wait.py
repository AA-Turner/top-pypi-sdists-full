"""A node whose inputs are ready never waits for an unrelated slow sibling.

The bug (podcast challenger, run d3d657a0, 2026-10-07): ``call_w6`` (audio,
6.5 min) and ``pack_w7`` ran in super-step 11. ``pack_w7`` finished in 1 ms,
which made ``call_w7`` (images) Ready — but the pure Pregel barrier held it
until EVERY invocation of step 11 finished, so images only started when the
audio was done. Nothing in the wiring connects W6 to W7; the one-hop depth
difference (a ``stringify`` on the W7 path) was enough to serialize them.

The contract pinned here (``Scheduler`` RUN-AHEAD): in a pure-dataflow graph a
node made Ready by finished work starts at once, filed under the step key the
barrier would give it — step numbers, checkpoints and replay keys are the
barrier's — and a park-and-resume never re-executes work that already ran.
"""

from __future__ import annotations

import asyncio
import time

import pytest
from typing import Any, ClassVar

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.checkpoint.protocol import NodeOutcome
from matrx_graph.executor.scheduler import RUN_AHEAD_ENABLED
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from pydantic import BaseModel, ConfigDict

from tests._fixtures import FakeEmitter, make_app_context

SLOW_S = 0.6


class _In(BaseModel):
    model_config = ConfigDict(extra="allow")

    value: str = ""


class _Out(BaseModel):
    model_config = ConfigDict(extra="forbid")

    value: str = ""


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")

    seconds: float = 0.0
    ask: bool = False


class _Sleeper:
    """Sleeps ``config.seconds``, passes ``value`` through, and records every
    REAL execution (replays never reach ``execute``) with its wall times."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.sleeper",
        category=NodeCategory.DATA,
        display_name="Sleeper",
        description="Sleeps, then passes its input through.",
        input_schema=_In,
        output_schema=_Out,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
    )

    def __init__(self, fail_once: set[str] | None = None, vary: set[str] | None = None) -> None:
        self.fail_once = set(fail_once or ())
        # Nodes whose output carries their run count — a re-run produces a
        # DIFFERENT output, so downstream inputs change.
        self.vary = set(vary or ())
        self.runs: dict[str, int] = {}
        self.started: dict[str, float] = {}
        self.finished: dict[str, float] = {}

    async def execute(
        self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg
    ) -> NodeResult[_Out]:
        node_id = ctx.node_id
        self.runs[node_id] = self.runs.get(node_id, 0) + 1
        self.started.setdefault(node_id, time.monotonic())
        await asyncio.sleep(config.seconds)
        if config.ask:
            ctx.interrupt({"question": f"{node_id}: go on?"})
        if node_id in self.fail_once:
            self.fail_once.discard(node_id)
            raise RuntimeError(f"{node_id} failed on purpose")
        self.finished[node_id] = time.monotonic()
        suffix = str(self.runs[node_id]) if node_id in self.vary else ""
        return success(_Out(value=f"{inputs.value}>{node_id}{suffix}"))


def _node(node_id: str, seconds: float = 0.0, *, ask: bool = False) -> dict[str, Any]:
    return {
        "id": node_id,
        "type": "test.sleeper",
        "position": {"x": 0, "y": 0},
        "data": {"config": {"seconds": seconds, "ask": ask}},
    }


def _edge(src: str, tgt: str, target_field: str = "value") -> dict[str, Any]:
    return {
        "id": f"e_{src}_{tgt}",
        "source": src,
        "target": tgt,
        "data": {"kind": "data", "mappings": {target_field: "value"}},
    }


def _podcast_shape(*, channels: list[dict[str, Any]] | None = None) -> Definition:
    """The W0 shape in miniature: ``audio`` (slow) launches beside ``hop1``;
    the images path is one hop deeper (``hop1 → hop2 → images``), and
    ``compose`` joins both slow branches."""
    return Definition.model_validate(
        {
            "nodes": [
                _node("start"),
                _node("audio", SLOW_S),
                _node("hop1"),
                _node("hop2"),
                _node("images", SLOW_S),
                _node("compose"),
            ],
            "edges": [
                _edge("start", "audio"),
                _edge("start", "hop1"),
                _edge("hop1", "hop2"),
                _edge("hop2", "images"),
                _edge("audio", "compose", "audio"),
                _edge("images", "compose", "images"),
            ],
            "entry_nodes": ["start"],
            "channels": channels or [],
        }
    )


def _scheduler(
    definition: Definition,
    sleeper: _Sleeper,
    checkpointer: MemoryCheckpointer | None = None,
    **scheduler_kwargs: Any,
) -> tuple[Scheduler, MemoryCheckpointer, FakeEmitter]:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(sleeper)
    graph = compile_graph(definition, registry=registry)
    emitter = FakeEmitter()
    checkpointer = checkpointer or MemoryCheckpointer()
    scheduler = Scheduler(
        graph, checkpointer, make_app_context(emitter), registry=registry, **scheduler_kwargs
    )
    return scheduler, checkpointer, emitter


@pytest.mark.skipif(not RUN_AHEAD_ENABLED, reason="run-ahead kill switch is off")
async def test_ready_node_starts_while_unrelated_slow_sibling_runs():
    # Warm-up run, untimed: the first run in a process pays one-time costs
    # (lazy imports, a host DB pool connecting) that are not the engine's
    # scheduling and made the wall-clock bound flaky in isolation.
    warm, _wcp, _wem = _scheduler(_podcast_shape(), _Sleeper())
    assert (await warm.run(run_id="run-ahead-warmup")).status is RunStatus.COMPLETED

    sleeper = _Sleeper()
    scheduler, checkpointer, _em = _scheduler(_podcast_shape(), sleeper)

    began = time.monotonic()
    result = await scheduler.run(run_id="run-ahead")
    elapsed = time.monotonic() - began

    assert result.status is RunStatus.COMPLETED, result.error
    # images started long before audio finished — they overlap.
    assert sleeper.started["images"] < sleeper.finished["audio"] - SLOW_S / 2
    # ~max(audio, images), never ~audio + images.
    assert elapsed < SLOW_S * 1.6, f"took {elapsed:.2f}s — the slow branches ran one after another"
    assert result.last_outputs["compose"]["value"].endswith(">compose")
    assert all(count == 1 for count in sleeper.runs.values()), sleeper.runs
    # Numbering is the barrier's: start 0, {audio, hop1} 1, hop2 2, images 3,
    # compose 4 — the run-ahead launches were filed under the keys a replay
    # looks up, so a crash replay finds them instead of re-running them.
    assert result.steps_executed == 5
    for step, node_id in ((2, "hop2"), (3, "images"), (4, "compose")):
        outcome = await checkpointer.get_outcome(
            run_id="run-ahead", step=step, node_id=node_id, attempt=1
        )
        assert outcome is not None and outcome.error is None, (step, node_id)


async def test_park_mid_wave_then_resume_never_reruns_finished_work():
    sleeper = _Sleeper(fail_once={"images"})
    scheduler, checkpointer, emitter = _scheduler(_podcast_shape(), sleeper)

    parked = await scheduler.run(run_id="run-ahead-park")
    assert parked.status is RunStatus.ERRORED
    errored = [
        e for k, e in emitter.events
        if k == "data" and isinstance(e, dict) and e.get("event") == "run_errored"
    ]
    assert errored[0]["node_id"] == "images"
    step = errored[0]["step"]
    cp_id = errored[0]["checkpoint_id"]
    checkpoint = await checkpointer.load_checkpoint(cp_id)
    assert checkpoint is not None and checkpoint.step == step
    # The parked frontier names the failed node, so recovery can address it.
    assert "images" in {ni.node_id for ni in checkpoint.next_invocations}

    # The host's manual-result lever: an outcome at the failed node's key.
    await checkpointer.record_outcome(
        NodeOutcome(
            run_id="run-ahead-park", step=step, node_id="images", attempt=1,
            output={"value": "manual-images"},
        )
    )
    resumed = await scheduler.resume(run_id="run-ahead-park", checkpoint_id=cp_id)

    assert resumed.status is RunStatus.COMPLETED, resumed.error
    # The slow audio branch and the hops ran exactly once across park+resume.
    assert sleeper.runs["audio"] == 1
    assert sleeper.runs["hop1"] == 1
    assert sleeper.runs["hop2"] == 1
    assert sleeper.runs["compose"] == 1


async def test_graph_with_channels_keeps_the_super_step_barrier():
    """Channels are read from the step snapshot, so a graph that declares any
    keeps the barrier: a node never runs against a snapshot missing a write a
    same-step sibling has yet to commit."""
    sleeper = _Sleeper()
    scheduler, _cp, _em = _scheduler(
        _podcast_shape(channels=[{"name": "notes", "reducer": "append"}]), sleeper
    )
    result = await scheduler.run(run_id="barrier-kept")
    assert result.status is RunStatus.COMPLETED, result.error
    assert sleeper.started["images"] >= sleeper.finished["audio"] - 0.01


async def test_interrupt_resume_never_reruns_a_node_that_ran_ahead():
    """A slow node interrupts while a fast branch has already run ahead. The
    interrupt checkpoint must schedule that branch's successors for the step
    they ran ahead under, so resume replays them instead of running them
    again (review of 87df55e20b: ``sink`` ran twice)."""
    definition = Definition.model_validate(
        {
            "nodes": [_node("start"), _node("ask", SLOW_S, ask=True), _node("fast"), _node("sink")],
            "edges": [_edge("start", "ask"), _edge("start", "fast"), _edge("fast", "sink")],
            "entry_nodes": ["start"],
        }
    )
    sleeper = _Sleeper()
    scheduler, checkpointer, _em = _scheduler(definition, sleeper)
    parked = await scheduler.run(run_id="interrupt-ahead")
    assert parked.status is RunStatus.INTERRUPTED, parked.error
    assert parked.interrupt is not None

    resumer, _cp, _em2 = _scheduler(definition, sleeper, checkpointer)
    resumed = await resumer.resume(
        run_id="interrupt-ahead",
        checkpoint_id=parked.interrupt["checkpoint_id"],
        resume_value={"value": "yes"},
    )
    assert resumed.status is RunStatus.COMPLETED, resumed.error
    assert sleeper.runs["sink"] == 1, sleeper.runs
    assert sleeper.runs["fast"] == 1, sleeper.runs


async def test_crash_resume_from_any_checkpoint_never_reruns_finished_work():
    """A crash leaves the run at its last end-of-step checkpoint. Resuming from
    ANY of them must replay every node that already ran — the frontier runs at
    the step it was scheduled for, not at the checkpoint's own step (which
    re-ran it under a fresh key — on the plain barrier too)."""
    sleeper = _Sleeper()
    scheduler, checkpointer, _em = _scheduler(_podcast_shape(), sleeper)
    first = await scheduler.run(run_id="crash-replay")
    assert first.status is RunStatus.COMPLETED, first.error
    finished = dict(sleeper.runs)
    assert all(count == 1 for count in finished.values()), finished

    checkpoints = await checkpointer.list_checkpoints("crash-replay")
    assert len(checkpoints) >= 4
    for checkpoint in checkpoints:
        if not checkpoint.next_invocations:
            continue
        replayer, _cp, _em2 = _scheduler(_podcast_shape(), sleeper, checkpointer)
        replayed = await replayer.resume(
            run_id="crash-replay", checkpoint_id=checkpoint.checkpoint_id
        )
        assert replayed.status is RunStatus.COMPLETED, (checkpoint.step, replayed.error)
        assert sleeper.runs == finished, (checkpoint.step, sleeper.runs)


async def test_cancel_mid_step_launches_nothing_more():
    """Cancel requested while a step waits on a slow member: nothing further
    runs ahead, and the run stops at the boundary as canceled."""
    sleeper = _Sleeper()

    async def cancel_once_hop1_done() -> bool:
        return "hop1" in sleeper.finished

    scheduler, _cp, _em = _scheduler(
        _podcast_shape(), sleeper, cancel_check=cancel_once_hop1_done
    )
    began = time.monotonic()
    result = await scheduler.run(run_id="cancel-mid-step")
    elapsed = time.monotonic() - began

    assert result.status is RunStatus.CANCELLED, result.error
    assert "hop2" not in sleeper.runs and "images" not in sleeper.runs, sleeper.runs
    assert elapsed < SLOW_S * 1.6, f"cancel waited {elapsed:.2f}s"


async def test_a_broken_adoption_fails_loudly_and_leaks_no_task():
    """If a run-ahead launch's inputs ever differ from what its step schedules,
    the run fails before that step starts anything — and the mismatched
    launch is canceled, not orphaned."""
    from matrx_graph.executor.scheduler import Invocation, _StepResult

    sleeper = _Sleeper()
    scheduler, _cp, _em = _scheduler(_podcast_shape(), sleeper)
    stray = asyncio.create_task(asyncio.sleep(30))
    wrong = _StepResult(invocation=Invocation(node_id="hop1", inputs={"value": "WRONG"}), output=None)
    # Step 1 schedules [audio, hop1]; the bad launch is the SECOND, so a
    # check made inside the launch loop would already have started audio.
    scheduler._run_ahead[(1, "hop1", "", 0)] = (stray, wrong)

    result = await scheduler.run(run_id="broken-adoption")
    await asyncio.sleep(0)

    assert result.status is RunStatus.FAILED
    assert "run-ahead invariant" in (result.error or "")
    assert stray.cancelled()
    assert "audio" not in sleeper.runs, "a step member started before the check"
    assert _engine_leftovers() == []


def _engine_leftovers() -> list[asyncio.Task[Any]]:
    """Unfinished tasks the ENGINE started (scheduler coroutines and node
    executions). Process-wide tasks a host library keeps — matrx_orm's pool
    keepalive starts the first time anything touches the DB — are not the
    run's and never were what this guard is about."""
    current = asyncio.current_task()
    out = []
    for task in asyncio.all_tasks():
        if task is current or task.done():
            continue
        coro = task.get_coro()
        module = getattr(getattr(coro, "cr_code", None), "co_filename", "") or ""
        if "matrx_orm" in module:
            continue
        out.append(task)
    return out


def _chain(*node_ids: str) -> Definition:
    return Definition.model_validate(
        {
            "nodes": [_node(n) for n in node_ids],
            "edges": [_edge(a, b) for a, b in zip(node_ids, node_ids[1:])],
            "entry_nodes": [node_ids[0]],
        }
    )


async def test_rerun_from_a_step_never_replays_stale_downstream_outputs():
    """"Re-run from this step" (the host's save_retry_child_checkpoint: the
    target's attempt bumped on the checkpoint that scheduled it). The target
    runs fresh with a NEW output; every downstream node is keyed exactly as
    before, so its recorded outcome sits at the same key — and must NOT
    replay, because it was produced from the old inputs."""
    from uuid import uuid4

    from matrx_graph.checkpoint.protocol import Checkpoint

    definition = _chain("a", "b", "c", "d")
    sleeper = _Sleeper(vary={"b"})
    scheduler, checkpointer, _em = _scheduler(definition, sleeper)
    first = await scheduler.run(run_id="rerun-from")
    assert first.status is RunStatus.COMPLETED, first.error
    assert first.last_outputs["d"]["value"] == ">a>b1>c>d"

    source = next(
        cp
        for cp in await checkpointer.list_checkpoints("rerun-from")
        if [ni.node_id for ni in cp.next_invocations] == ["b"]
    )
    child = Checkpoint(
        checkpoint_id=str(uuid4()),
        run_id="rerun-from",
        thread_id=source.thread_id,
        parent_checkpoint_id=source.checkpoint_id,
        step=source.step,
        channel_values=source.channel_values,
        pending_bindings=source.pending_bindings,
        next_invocations=[
            ni.model_copy(update={"attempt": ni.attempt + 1}) for ni in source.next_invocations
        ],
    )
    await checkpointer.save_checkpoint(child)
    rerunner, _cp, _em2 = _scheduler(definition, sleeper, checkpointer)
    rerun = await rerunner.resume(run_id="rerun-from", checkpoint_id=child.checkpoint_id)

    assert rerun.status is RunStatus.COMPLETED, rerun.error
    assert sleeper.runs == {"a": 1, "b": 2, "c": 2, "d": 2}, sleeper.runs
    assert rerun.last_outputs["d"]["value"] == ">a>b2>c>d"


async def test_run_one_step_on_an_interrupt_successor_runs_it():
    """"Run this one step" (select + stop_after_steps=1) on a node an
    interrupt checkpoint scheduled for the NEXT step runs that node — the
    step-mode leg starts at the selected node's step instead of holding it
    and running an empty step."""
    from uuid import uuid4

    from matrx_graph.checkpoint.protocol import Checkpoint

    definition = Definition.model_validate(
        {
            "nodes": [_node("start"), _node("ask", ask=True), _node("fast", 0.2), _node("sink")],
            "edges": [_edge("start", "ask"), _edge("start", "fast"), _edge("fast", "sink")],
            "entry_nodes": ["start"],
        }
    )
    sleeper = _Sleeper()
    scheduler, checkpointer, _em = _scheduler(definition, sleeper)
    parked = await scheduler.run(run_id="one-step")
    assert parked.status is RunStatus.INTERRUPTED, parked.error
    assert "sink" not in sleeper.runs  # ask interrupted first: nothing ran ahead
    cp = await checkpointer.load_checkpoint(parked.interrupt["checkpoint_id"])
    assert cp is not None
    assert {ni.node_id: ni.step for ni in cp.next_invocations} == {
        "ask": cp.step,
        "sink": cp.step + 1,
    }

    # The host's run-one-step leg: a child of the parked checkpoint.
    child = Checkpoint(
        checkpoint_id=str(uuid4()),
        run_id="one-step",
        thread_id=cp.thread_id,
        parent_checkpoint_id=cp.checkpoint_id,
        step=cp.step,
        channel_values=cp.channel_values,
        pending_bindings=cp.pending_bindings,
        next_invocations=list(cp.next_invocations),
    )
    await checkpointer.save_checkpoint(child)
    stepper, _cp, _em2 = _scheduler(definition, sleeper, checkpointer)
    stepped = await stepper.resume(
        run_id="one-step",
        checkpoint_id=child.checkpoint_id,
        stop_after_steps=1,
        select_node_ids={"sink"},
    )
    assert stepped.status is RunStatus.PAUSED, stepped.error
    assert sleeper.runs.get("sink") == 1, sleeper.runs
    assert sleeper.runs["ask"] == 1, sleeper.runs  # only its interrupting run
    sink_outcome = await checkpointer.get_outcome(
        run_id="one-step", step=cp.step + 1, node_id="sink", attempt=1
    )
    assert sink_outcome is not None and sink_outcome.error is None


async def test_a_broken_adoption_cancels_and_awaits_every_taken_launch():
    """Two launches taken for one step — a VALID one first, then a mismatched
    one: both are canceled and awaited before the run fails, so neither is
    left running behind a dead run."""
    from matrx_graph.executor.scheduler import Invocation, _StepResult

    # The exact inputs step 1 schedules for ``audio``, from a clean run.
    probe_sleeper = _Sleeper()
    probe, probe_cp, _em = _scheduler(_podcast_shape(), probe_sleeper)
    assert (await probe.run(run_id="adoption-probe")).status is RunStatus.COMPLETED
    step0 = next(
        cp for cp in await probe_cp.list_checkpoints("adoption-probe") if cp.step == 0
    )
    audio_inputs = next(ni.inputs for ni in step0.next_invocations if ni.node_id == "audio")

    sleeper = _Sleeper()
    scheduler, _cp, _em2 = _scheduler(_podcast_shape(), sleeper)
    valid = asyncio.create_task(asyncio.sleep(30))
    stray = asyncio.create_task(asyncio.sleep(30))
    scheduler._run_ahead[(1, "audio", "", 0)] = (
        valid,
        _StepResult(invocation=Invocation(node_id="audio", inputs=dict(audio_inputs)), output=None),
    )
    scheduler._run_ahead[(1, "hop1", "", 0)] = (
        stray,
        _StepResult(invocation=Invocation(node_id="hop1", inputs={"value": "WRONG"}), output=None),
    )

    result = await scheduler.run(run_id="broken-adoption-2")

    assert result.status is RunStatus.FAILED
    assert valid.cancelled() and stray.cancelled()
    assert _engine_leftovers() == []


async def test_run_ahead_polls_for_a_stop_at_most_once_a_second():
    """Each poll is a status read; a burst of completions inside one step
    polls once, not once per completion."""
    calls = 0

    async def never_cancel() -> bool:
        nonlocal calls
        calls += 1
        return False

    hops = [f"hop{i}" for i in range(1, 9)]
    definition = Definition.model_validate(
        {
            "nodes": [_node("start"), _node("slow", SLOW_S), *(_node(h) for h in hops)],
            "edges": [
                _edge("start", "slow"),
                _edge("start", hops[0]),
                *(_edge(a, b) for a, b in zip(hops, hops[1:])),
            ],
            "entry_nodes": ["start"],
        }
    )
    sleeper = _Sleeper()
    scheduler, _cp, _em = _scheduler(definition, sleeper, cancel_check=never_cancel)
    result = await scheduler.run(run_id="poll-throttle")
    assert result.status is RunStatus.COMPLETED, result.error
    # Every hop ran ahead while ``slow`` held step 1.
    assert sleeper.started["hop8"] < sleeper.finished["slow"]
    # One boundary poll per step, plus at most one throttled in-step poll.
    assert calls <= result.steps_executed + 1, (calls, result.steps_executed)


class _JsonRoundTripCheckpointer(MemoryCheckpointer):
    """Stores outcomes and checkpoints the way Postgres does: as JSON."""

    async def record_outcome(self, outcome: NodeOutcome) -> None:
        import json

        await super().record_outcome(
            NodeOutcome.model_validate(json.loads(json.dumps(outcome.model_dump(mode="json"))))
        )

    async def save_checkpoint(self, checkpoint: Any) -> None:
        import json

        from matrx_graph.checkpoint.protocol import Checkpoint

        await super().save_checkpoint(
            Checkpoint.model_validate(json.loads(json.dumps(checkpoint.model_dump(mode="json"))))
        )


async def test_resume_from_every_checkpoint_never_repays_a_finished_node():
    """Resume must replay, never re-pay. A replayed outcome routes its RECORDED
    settled dump — ``__kind`` stamp included — so every downstream node sees
    exactly the inputs it ran with. Replay used to rebuild the output through
    the node's model: for a closed legacy model (data.parse_json,
    subgraph.call, ...) that stripped ``__kind``, the downstream node's inputs
    no longer matched its recorded ones, and it ran AGAIN on every resume — a
    podcast child's multi-minute audio, re-bought."""
    import json

    from matrx_graph.nodes.subgraph.call import set_subgraph_resolver

    child_calls = 0

    async def child_run(_ctx: Any, _config: Any, inputs: Any) -> dict[str, Any]:
        nonlocal child_calls
        child_calls += 1
        return {"run_id": "child-1", "last_outputs": {"out": {"value": "rendered"}}}

    text = json.dumps({"value": "brief", "f": 0.1, "big": 1e20, "at": "2026-10-07T10:00:00Z"})
    definition = Definition.model_validate(
        {
            "nodes": [
                {"id": "x", "type": "data.transform", "position": {"x": 0, "y": 0},
                 "data": {"config": {"expression": "{'text': " + repr(text) + "}"}}},
                {"id": "parse", "type": "data.parse_json", "position": {"x": 0, "y": 0},
                 "data": {"config": {}}},
                {"id": "call", "type": "subgraph.call", "position": {"x": 0, "y": 0},
                 "data": {"config": {"definition_id": "child-def"}}},
                _node("b"),
                _node("c"),
            ],
            "edges": [
                {"id": "e_x_parse", "source": "x", "target": "parse",
                 "data": {"kind": "data", "mappings": {"text": "text"}}},
                {"id": "e_parse_call", "source": "parse", "target": "call"},
                {"id": "e_call_b", "source": "call", "target": "b"},
                _edge("b", "c"),
            ],
            "entry_nodes": ["x"],
        }
    )
    set_subgraph_resolver(child_run)
    try:
        sleeper = _Sleeper()
        checkpointer = _JsonRoundTripCheckpointer()
        scheduler, _cp, _em = _scheduler(definition, sleeper, checkpointer)
        first = await scheduler.run(run_id="no-repay")
        assert first.status is RunStatus.COMPLETED, first.error
        assert child_calls == 1 and sleeper.runs == {"b": 1, "c": 1}

        checkpoints = [
            cp for cp in await checkpointer.list_checkpoints("no-repay") if cp.next_invocations
        ]
        assert len(checkpoints) >= 4
        for _round in range(2):  # a resume must not poison the next baseline
            for checkpoint in checkpoints:
                replayer, _cp2, _em2 = _scheduler(definition, sleeper, checkpointer)
                replayed = await replayer.resume(
                    run_id="no-repay", checkpoint_id=checkpoint.checkpoint_id
                )
                assert replayed.status is RunStatus.COMPLETED, (checkpoint.step, replayed.error)
                assert child_calls == 1, f"child re-run resuming from step {checkpoint.step}"
                assert sleeper.runs == {"b": 1, "c": 1}, (checkpoint.step, sleeper.runs)
    finally:
        set_subgraph_resolver(None)


async def test_legacy_replay_salvage_never_forwards_the_keys_it_dropped():
    """A recorded outcome in a node's OLD shape is replayed with unknown keys
    stripped (LEGACY-REPLAY). Routing must carry the salvaged output — never
    the raw recorded dump, or downstream nodes receive the very keys the
    salvage dropped."""
    definition = Definition.model_validate(
        {
            "nodes": [_node("a"), _node("b"), _node("c")],
            "edges": [
                {"id": "e_a_b", "source": "a", "target": "b"},
                {"id": "e_b_c", "source": "b", "target": "c"},
            ],
            "entry_nodes": ["a"],
        }
    )
    sleeper = _Sleeper()
    scheduler, checkpointer, _em = _scheduler(definition, sleeper)
    first = await scheduler.run(run_id="legacy-salvage")
    assert first.status is RunStatus.COMPLETED, first.error

    b_step = next(
        cp.step + 1
        for cp in await checkpointer.list_checkpoints("legacy-salvage")
        if [ni.node_id for ni in cp.next_invocations] == ["b"]
    )
    recorded = await checkpointer.get_outcome(
        run_id="legacy-salvage", step=b_step, node_id="b", attempt=1
    )
    assert recorded is not None and recorded.inputs is not None
    # The pre-migration shape: a field b's output model no longer declares.
    await checkpointer.record_outcome(
        recorded.model_copy(
            update={"output": {**recorded.output, "removed_legacy_flag": True}}
        )
    )
    source = next(
        cp
        for cp in await checkpointer.list_checkpoints("legacy-salvage")
        if [ni.node_id for ni in cp.next_invocations] == ["b"]
    )
    replayer, _cp, _em2 = _scheduler(definition, sleeper, checkpointer)
    resumed = await replayer.resume(run_id="legacy-salvage", checkpoint_id=source.checkpoint_id)

    assert resumed.status is RunStatus.COMPLETED, resumed.error
    assert sleeper.runs["b"] == 1  # salvaged, not re-run
    assert "removed_legacy_flag" not in resumed.last_outputs["b"]
    c_outcome = await checkpointer.get_outcome(
        run_id="legacy-salvage", step=b_step + 1, node_id="c", attempt=1
    )
    assert c_outcome is not None and c_outcome.inputs is not None
    assert "removed_legacy_flag" not in c_outcome.inputs, c_outcome.inputs
    assert sleeper.runs["c"] == 1, "c's inputs changed — the dropped key leaked"


def _join_shape() -> Definition:
    """The Smart Add identify shape in miniature (run 363ea8bb, 2026-10-14): ``probe`` starts the round;
    ``shots`` (slow, the homepage pictures), ``page`` and ``web`` run in the same super-step; ``first``
    JOINS page + web (a capture point) and ``facts`` follows it. Nothing reads ``shots`` — yet the point
    waited 25 s for it, because a join was only ever run ahead on ONE finished result at a time."""
    return Definition.model_validate(
        {
            "nodes": [
                _node("probe"),
                _node("shots", SLOW_S),
                _node("page"),
                _node("web"),
                _node("first"),
                _node("facts"),
            ],
            "edges": [
                _edge("probe", "shots"),
                _edge("probe", "page"),
                _edge("probe", "web"),
                _edge("page", "first", "value"),
                _edge("web", "first", "web"),
                _edge("first", "facts"),
            ],
            "entry_nodes": ["probe"],
            "channels": [],
        }
    )


@pytest.mark.skipif(not RUN_AHEAD_ENABLED, reason="run-ahead kill switch is off")
async def test_a_join_whose_inputs_all_finished_starts_while_an_unrelated_sibling_runs():
    sleeper = _Sleeper()
    scheduler, checkpointer, _em = _scheduler(_join_shape(), sleeper)

    result = await scheduler.run(run_id="run-ahead-join")

    assert result.status is RunStatus.COMPLETED, result.error
    # The join and the step after it both ran while the slow sibling was still working.
    assert sleeper.finished["first"] < sleeper.finished["shots"] - SLOW_S / 2, "the join waited for the barrier"
    assert sleeper.finished["facts"] < sleeper.finished["shots"] - SLOW_S / 2, "facts waited for the barrier"
    assert all(count == 1 for count in sleeper.runs.values()), sleeper.runs
    # The barrier's numbering: probe 0, {shots, page, web} 1, first 2, facts 3.
    assert result.steps_executed == 4
    for step, node_id in ((2, "first"), (3, "facts")):
        outcome = await checkpointer.get_outcome(run_id="run-ahead-join", step=step, node_id=node_id, attempt=1)
        assert outcome is not None and outcome.error is None, (step, node_id)


# ── Partial routing never resolves an edge differently from the barrier ──────
#
# Reviewer probe (2026-10-14, on 819c9cffc7 and on the original 2026-10-07
# run-ahead): ``mA`` is a ``control.map`` over an EMPTY list and ``mB`` a slow
# dispatcher that Sends two items to the same target ``T``. Routed alone, ``mA``
# triggered the empty-map rule ("no dispatch in this run targets T" — but mB had
# not registered its dispatch yet), pruned T's subtree, and launched the join
# ``K`` without the gather's values. The barrier then routed both, T ran, and K
# ran AGAIN at a later step with the right inputs. Two runs of K, the first on
# wrong inputs, under different keys — and the run said COMPLETED.


class _SendIn(BaseModel):
    model_config = ConfigDict(extra="allow")


class _SendOut(BaseModel):
    model_config = ConfigDict(extra="forbid")

    n: int = 0


class _SendCfg(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _SlowSender:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.slow_sender",
        category=NodeCategory.CONTROL,
        display_name="Slow sender",
        description="Sleeps, then sends two items to T.",
        input_schema=_SendIn,
        output_schema=_SendOut,
        config_schema=_SendCfg,
        launches_nodes=True,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT, required=False),
        ),
        determinism=ActionTier.PURE,
    )

    async def execute(
        self, ctx: NodeExecutionContext, inputs: _SendIn, config: _SendCfg
    ) -> NodeResult[_SendOut]:
        await asyncio.sleep(SLOW_S)
        ctx.send("T", {"value": "x"})
        ctx.send("T", {"value": "y"})
        return success(_SendOut(n=2))


def _empty_map_beside_a_dispatcher(*, dispatchers_from: str) -> Definition:
    """``dispatchers_from='start'``: mA and mB run in the SAME step as ``page``
    (the case 819c9cffc7 introduced). ``'page'``: they run a step AFTER ``page``
    (the case the original single-result run-ahead already had)."""
    return Definition.model_validate(
        {
            "nodes": [
                _node("start"),
                _node("page"),
                {
                    "id": "mA",
                    "type": "control.map",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"target_node_id": "T"}, "input": {"items": []}},
                },
                {"id": "mB", "type": "test.slow_sender", "position": {"x": 0, "y": 0}, "data": {"config": {}}},
                _node("T"),
                _node("K"),
                {"id": "G", "type": "control.gather", "position": {"x": 0, "y": 0}, "data": {"config": {}}},
            ],
            "edges": [
                _edge("start", "page"),
                {"id": "e_a", "source": dispatchers_from, "target": "mA",
                 "data": {"kind": "data", "mappings": {"seed": "value"}}},
                {"id": "e_b", "source": dispatchers_from, "target": "mB",
                 "data": {"kind": "data", "mappings": {"seed": "value"}}},
                _edge("page", "K"),
                {"id": "e_t_g", "source": "T", "target": "G", "data": {"mappings": {"value": "value"}}},
                {"id": "e_g_k", "source": "G", "target": "K",
                 "data": {"kind": "data", "mappings": {"tvals": "values"}}},
            ],
            "entry_nodes": ["start"],
        }
    )


def _dispatcher_scheduler(
    definition: Definition, sleeper: _Sleeper
) -> tuple[Scheduler, MemoryCheckpointer]:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(sleeper, overwrite=True)
    registry.register(_SlowSender(), overwrite=True)
    graph = compile_graph(definition, registry=registry)
    checkpointer = MemoryCheckpointer()
    return Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry), checkpointer


def _outcomes_of(checkpointer: MemoryCheckpointer, run_id: str, node_id: str) -> list[NodeOutcome]:
    return [o for k, o in sorted(checkpointer._outcomes.items()) if k[0] == run_id and k[2] == node_id]


@pytest.mark.skipif(not RUN_AHEAD_ENABLED, reason="run-ahead kill switch is off")
@pytest.mark.parametrize("dispatchers_from", ["start", "page"], ids=["same-step", "earlier-step"])
async def test_an_empty_map_beside_a_running_dispatcher_never_launches_the_join_early(dispatchers_from: str):
    sleeper = _Sleeper()
    scheduler, checkpointer = _dispatcher_scheduler(
        _empty_map_beside_a_dispatcher(dispatchers_from=dispatchers_from), sleeper
    )
    run_id = f"empty-map-{dispatchers_from}"

    result = await scheduler.run(run_id=run_id)

    assert result.status is RunStatus.COMPLETED, result.error
    assert sleeper.runs["K"] == 1, f"the join ran {sleeper.runs['K']} times"
    k_outcomes = _outcomes_of(checkpointer, run_id, "K")
    assert len(k_outcomes) == 1, [o.step for o in k_outcomes]
    assert k_outcomes[0].inputs["tvals"] == ["x>T", "y>T"], k_outcomes[0].inputs


@pytest.mark.skipif(not RUN_AHEAD_ENABLED, reason="run-ahead kill switch is off")
async def test_without_the_partial_routing_deferral_the_barrier_guard_fails_the_run(monkeypatch):
    """The second line of defense, proven on the reviewer's exact case: with
    the partial-routing deferral switched off, the early join is an ORPHAN at
    the barrier (filed under a step the barrier does not schedule it at) — a
    different key than its real firing, which the adoption check alone never
    compared. The run must fail loudly, never complete with K run twice."""
    from matrx_graph.executor import scheduler as scheduler_module

    monkeypatch.setattr(
        scheduler_module.Scheduler,
        "_partial_routing",
        property(lambda self: False, lambda self, value: None),
        raising=False,
    )
    sleeper = _Sleeper()
    scheduler, _cp = _dispatcher_scheduler(_empty_map_beside_a_dispatcher(dispatchers_from="start"), sleeper)

    result = await scheduler.run(run_id="empty-map-unguarded")

    assert result.status is RunStatus.FAILED, (result.status, sleeper.runs)
    assert "run-ahead invariant" in (result.error or ""), result.error
    # Since an empty For Each fires its gather (42f83d9cd5), G is an early join
    # too, and whichever orphan the barrier meets first is the one it names.
    assert "'G'" in (result.error or "") or "'K'" in (result.error or ""), result.error
    assert sleeper.runs.get("K", 0) <= 1, sleeper.runs
    assert _engine_leftovers() == []


async def test_an_orphan_run_ahead_launch_fails_the_run_at_the_barrier():
    """A launch filed under a step the barrier does not schedule its node at."""
    from matrx_graph.executor.scheduler import Invocation, _StepResult

    sleeper = _Sleeper()
    scheduler, _cp, _em = _scheduler(_podcast_shape(), sleeper)
    stray = asyncio.create_task(asyncio.sleep(30))
    # compose is scheduled at step 4 — never at step 1.
    scheduler._run_ahead[(1, "compose", "", 0)] = (
        stray,
        _StepResult(invocation=Invocation(node_id="compose", inputs={}), output=None),
    )

    result = await scheduler.run(run_id="orphan-launch")

    assert result.status is RunStatus.FAILED
    assert "does not schedule it there" in (result.error or ""), result.error
    assert stray.cancelled()
    assert "audio" not in sleeper.runs, "step 1 started before the barrier check"
    assert _engine_leftovers() == []


async def test_a_node_scheduled_while_launched_under_another_step_fails_the_run():
    """A launch filed under a LATER step for a node the barrier schedules now
    would run the node twice under two keys."""
    from matrx_graph.executor.scheduler import Invocation, _StepResult

    sleeper = _Sleeper()
    scheduler, _cp, _em = _scheduler(_podcast_shape(), sleeper)
    stray = asyncio.create_task(asyncio.sleep(30))
    # hop1 is scheduled at step 1; this launch claims step 3.
    scheduler._run_ahead[(3, "hop1", "", 0)] = (
        stray,
        _StepResult(invocation=Invocation(node_id="hop1", inputs={}), output=None),
    )

    result = await scheduler.run(run_id="double-launch")

    assert result.status is RunStatus.FAILED
    assert "would run twice" in (result.error or ""), result.error
    assert stray.cancelled()
    assert _engine_leftovers() == []


@pytest.mark.skipif(not RUN_AHEAD_ENABLED, reason="run-ahead kill switch is off")
async def test_a_crash_while_the_join_ran_ahead_resumes_without_rerunning_it():
    """The Smart Add join shape, killed mid-step: the join (``first``) and the
    node after it (``facts``) already ran ahead while ``shots`` was still
    working, then the process died. The resume (from the last end-of-step
    checkpoint — the only thing a crash leaves) replays both from their
    recorded outcomes, re-runs only the cut-off ``shots``, and completes."""
    sleeper = _Sleeper()
    scheduler, checkpointer, _em = _scheduler(_join_shape(), sleeper)

    run = asyncio.create_task(scheduler.run(run_id="join-crash"))
    for _ in range(200):
        if "facts" in sleeper.finished:
            break
        await asyncio.sleep(0.01)
    assert "facts" in sleeper.finished and "shots" not in sleeper.finished, sleeper.finished
    run.cancel()  # the process dies mid-step
    with pytest.raises(asyncio.CancelledError):
        await run
    assert _engine_leftovers() == []

    checkpoints = await checkpointer.list_checkpoints("join-crash")
    last = max(checkpoints, key=lambda c: c.step)
    assert {ni.node_id for ni in last.next_invocations} == {"shots", "page", "web"}

    resumer, _cp, _em2 = _scheduler(_join_shape(), sleeper, checkpointer)
    resumed = await resumer.resume(run_id="join-crash", checkpoint_id=last.checkpoint_id)

    assert resumed.status is RunStatus.COMPLETED, resumed.error
    assert sleeper.runs["shots"] == 2, "the cut-off slow sibling runs again"
    for node_id in ("probe", "page", "web", "first", "facts"):
        assert sleeper.runs[node_id] == 1, (node_id, sleeper.runs)
    first = await checkpointer.get_outcome(run_id="join-crash", step=2, node_id="first", attempt=1)
    assert first is not None and first.inputs is not None
    assert first.inputs["value"].endswith(">page") and first.inputs["web"].endswith(">web"), first.inputs
    assert resumed.last_outputs["facts"]["value"].endswith(">facts")
