"""A chain of pure steps runs back to back: no status read between two of them (L-SPEED 6c).

Live (search child 79c58b1f, durability "boundaries"): trivial transforms ran ~0.1-0.3 s apart. Inside
a chain the boundary's checkpoint is queued, not written, so no save read the run's status for the
next boundary, and every boundary paid a ``control_check`` round trip (27 reads in one child run, one
per step). Now a boundary inside a chain reads the controls only when they were last read
``CHAIN_CONTROL_POLL_SECONDS`` ago (or a step that may spend launched) under ``durability="boundaries"``:
a Stop still lands within that interval, and a chain of milliseconds-long steps costs milliseconds. The
default ``every_step`` keeps a read at every boundary (a Cancel stops at the next one).
"""

from __future__ import annotations

import time

from matrx_graph import Definition, RunStatus
from matrx_graph.executor import scheduler as scheduler_module
from tests.test_a_boundaries_run_writes_one_checkpoint_per_chain import _scheduler
from tests.test_scheduler_ready_nodes_do_not_wait import _edge, _node, _Sleeper

STEPS = 20
READ_SECONDS = 0.1  # one control read, as slow as a contended pool makes it


def _chain(n: int, seconds: float = 0.0) -> Definition:
    ids = [f"s{i}" for i in range(n)]
    return Definition.model_validate(
        {
            "nodes": [_node(i, seconds) for i in ids],
            "edges": [_edge(x, y) for x, y in zip(ids, ids[1:])],
            "entry_nodes": [ids[0]],
        }
    )


class _Controls:
    def __init__(self, status: str = "running", sleep: float = READ_SECONDS) -> None:
        self.reads = 0
        self.status = status
        self.sleep = sleep

    async def __call__(self) -> str:
        import asyncio

        self.reads += 1
        await asyncio.sleep(self.sleep)
        return self.status


async def test_a_twenty_step_pure_chain_reads_its_controls_once_not_per_step() -> None:
    controls = _Controls()
    sched, _cp = _scheduler(
        _chain(STEPS),
        _Sleeper(),
        control_check=controls,
        control_check_reads_own_row=True,
        fresh_history=True,
        durability="boundaries",
    )
    started = time.perf_counter()
    result = await sched.run(run_id="pure-chain-budget")
    elapsed = time.perf_counter() - started
    assert result.status is RunStatus.COMPLETED
    # Before: one read per boundary (19 reads, >= 1.9 s of waiting). The chain lands every
    # CHAIN_MAX_STEPS steps; the boundary after that write uses the status the save read.
    assert controls.reads <= 3, controls.reads
    # The step-overhead budget: twenty pure steps plus at most three reads, well under the
    # 19 x 100 ms the per-step read cost.
    assert elapsed < 1.0, f"20 pure steps took {elapsed:.2f}s"


async def test_a_stop_still_lands_inside_a_long_chain() -> None:
    # Six pure steps of 0.4 s: the controls are read again once a second has passed, so a Stop
    # requested from the start lands mid-chain, never after the last step.
    controls = _Controls(status="cancelling", sleep=0.0)
    sleeper = _Sleeper()
    sched, _cp = _scheduler(
        _chain(6, seconds=0.4),
        sleeper,
        control_check=controls,
        control_check_reads_own_row=True,
        fresh_history=True,
        durability="boundaries",
    )
    result = await sched.run(run_id="pure-chain-stop")
    assert result.status is RunStatus.CANCELLED
    assert len(sleeper.runs) < 6, sleeper.runs


async def test_with_no_interval_every_boundary_reads_again(monkeypatch) -> None:
    monkeypatch.setattr(scheduler_module, "CHAIN_CONTROL_POLL_SECONDS", 0.0)
    controls = _Controls(sleep=0.0)
    sched, _cp = _scheduler(
        _chain(6),
        _Sleeper(),
        control_check=controls,
        control_check_reads_own_row=True,
        fresh_history=True,
        durability="boundaries",
    )
    assert (await sched.run(run_id="pure-chain-every-read")).status is RunStatus.COMPLETED
    assert controls.reads >= 5, controls.reads


async def test_every_step_durability_still_reads_at_every_boundary() -> None:
    controls = _Controls(sleep=0.0)
    sched, _cp = _scheduler(
        _chain(6),
        _Sleeper(),
        control_check=controls,
        control_check_reads_own_row=True,
        fresh_history=True,
    )
    assert (await sched.run(run_id="pure-chain-every-step")).status is RunStatus.COMPLETED
    assert controls.reads >= 5, controls.reads


async def test_each_leg_reports_what_its_awaits_and_the_process_cost(caplog) -> None:
    # Part 2: one line per leg names the engine's awaited hooks, GC and loop-lag time, so a live
    # gap between steps can be read as CPU (lag) or I/O (hook time that is not lag).
    import logging

    sched, _cp = _scheduler(
        _chain(4), _Sleeper(), control_check=_Controls(sleep=0.0), fresh_history=True
    )
    with caplog.at_level(logging.INFO, logger="matrx_graph.executor.scheduler"):
        assert (await sched.run(run_id="pure-chain-report")).status is RunStatus.COMPLETED
    lines = [r.getMessage() for r in caplog.records if "leg overhead" in r.getMessage()]
    assert len(lines) == 1, lines
    for word in (
        "wall=",
        "emit=",
        "save_checkpoint=",
        "gc=",
        "loop_lag=",
        "pool_wait=",
        "thread_wait=",
        "thread_work=",
        "intern=hit:",
    ):
        assert word in lines[0], lines[0]


async def test_the_leg_line_level_is_the_knob(caplog) -> None:
    """L-SPEED 6e: the timing line is INFO unless the workflow.leg_overhead.warn_seconds knob is on (> 0) and the
    leg lasted at least that long — then WARNING, which reaches production logs."""
    import logging

    from matrx_graph.executor.scheduler import _leg_clock, _log_leg_overhead

    started = _leg_clock()
    long_ago = (started[0] - 5.0, *started[1:])
    with caplog.at_level(logging.INFO, logger="matrx_graph.executor.scheduler"):
        _log_leg_overhead("leg-knob-off", long_ago, {}, 0)
        _log_leg_overhead("leg-knob-on", long_ago, {}, 2)
        _log_leg_overhead("leg-knob-short", started, {}, 2)
    by_run = [(r.getMessage()[:16], r.levelno) for r in caplog.records if "leg overhead" in r.getMessage()]
    assert by_run == [
        ("[wf:leg-knob] le", logging.INFO),
        ("[wf:leg-knob] le", logging.WARNING),
        ("[wf:leg-knob] le", logging.INFO),
    ], by_run


async def test_a_thread_hop_counts_its_queue_wait_and_its_work() -> None:
    from matrx_graph.checkpoint.values import OFF_LOOP_TOTALS, run_pure_off_loop

    before = list(OFF_LOOP_TOTALS)
    big = ["x" * 64] * 5000  # past OFF_LOOP_MIN_NODES: runs in a worker thread
    assert await run_pure_off_loop(len, big) == 5000
    assert OFF_LOOP_TOTALS[1] == before[1] + 1
    assert OFF_LOOP_TOTALS[0] >= before[0] and OFF_LOOP_TOTALS[2] >= before[2]
