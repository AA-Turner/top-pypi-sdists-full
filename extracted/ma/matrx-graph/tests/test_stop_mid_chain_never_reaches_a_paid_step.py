"""Stop pressed in the middle of a pure chain: the paid (or side-effect) step after it NEVER runs (review 6h, M4).

Under ``durability="boundaries"`` the pure steps of a chain defer their checkpoint and outcomes, and Stop is read
at a boundary. The review proved by probe that a checkpoint is queued only when the NEXT step is itself
chain-eligible, so the boundary before a paid or side-effect step always reads Stop — but no test ran it (the
chain tests were pure chains only). Five 50 ms pure steps, then an IDEMPOTENT tool that may spend / a SIDE_EFFECT
step; Stop is pressed 80 ms in; both durabilities, both control-check modes. Red with the paid tool made
chain-eligible (``step_reruns_safely`` -> True): it runs after Stop.
"""

from __future__ import annotations

import time

import pytest

from matrx_graph import Definition, RunStatus
from tests.test_a_boundaries_run_writes_one_checkpoint_per_chain import _scheduler
from tests.test_scheduler_ready_nodes_do_not_wait import _edge, _node, _Sleeper


def _definition(last_type: str, steps: int = 5, seconds: float = 0.05) -> Definition:
    ids = [f"s{i}" for i in range(steps)]
    last = _node("last")
    last["type"] = last_type
    chain = [*ids, "last"]
    return Definition.model_validate(
        {
            "nodes": [_node(i, seconds) for i in ids] + [last],
            "edges": [_edge(a, b) for a, b in zip(chain, chain[1:], strict=False)],
            "entry_nodes": [ids[0]],
        }
    )


class _StopAfter:
    """The run's control row: ``cancelling`` from ``after`` seconds into the run."""

    def __init__(self, after: float) -> None:
        self.t0 = time.monotonic()
        self.after = after

    async def __call__(self) -> str:
        return "cancelling" if time.monotonic() - self.t0 >= self.after else "running"


@pytest.mark.parametrize("last_type", ["test.paid_tool", "test.side_effect"])
@pytest.mark.parametrize("durability", ["boundaries", None])
@pytest.mark.parametrize("own_row", [True, False])
async def test_stop_mid_chain_never_reaches_the_paid_step(last_type: str, durability: str | None, own_row: bool) -> None:
    sleeper = _Sleeper()
    kwargs: dict = {"control_check": _StopAfter(0.08), "control_check_reads_own_row": own_row, "fresh_history": True}
    if durability:
        kwargs["durability"] = durability
    sched, _cp = _scheduler(_definition(last_type), sleeper, **kwargs)
    result = await sched.run(run_id=f"stop-{last_type}-{durability}-{own_row}")
    last_runs = getattr(sched.registry.get(last_type), "runs", [])
    assert result.status is RunStatus.CANCELLED, result.status
    assert len(sleeper.runs) >= 1, "Stop must land mid-chain (some pure steps ran)"
    assert not last_runs, f"{last_type} ran after Stop was pressed ({len(sleeper.runs)} pure steps ran first)"
