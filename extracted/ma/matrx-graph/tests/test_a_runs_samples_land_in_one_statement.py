"""A run's step samples land in ONE statement (L-SPEED 6k).

``adopt_live_outputs`` wrote each step's ``last_live_output`` slot with its own upsert: a research run
with 71 steps made 71 single-row writes to ``workflow.node_data_slot`` on the shared pool. The guard:
however many steps a run has, adoption sends one bulk write and no single-row write; a step whose result
is over the slot cap is still left out of it.
"""

from __future__ import annotations

from typing import Any
from uuid import uuid4

import pytest

from matrx_graph.db import NodeDataSlotStore

from .test_a_large_step_result_reaches_only_when_whole import _wire, bulk_calls_by_run


def _outcome(run_id: str, node_id: str, output: Any) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "node_id": node_id,
        "step": 0,
        "attempt": 1,
        "error": None,
        "source": "executor",
        "output": output,
        "emissions": {},
        "output_kind": None,
    }


@pytest.mark.asyncio
async def test_seventy_one_steps_are_one_write(monkeypatch: pytest.MonkeyPatch) -> None:
    run_id = str(uuid4())
    outcomes = [_outcome(run_id, f"step{i}", {"n": i}) for i in range(71)]
    outcomes.append(_outcome(run_id, "huge", {"blob": "x" * (300 * 1024)}))  # over the slot cap
    slots = _wire(monkeypatch, run_id, outcomes, stored={})

    import matrx_orm.operations.conflict_writes as conflict_writes

    singles: list[str] = []
    real_single = conflict_writes.upsert_with_conflict

    async def _single(model: Any, data: dict[str, Any], **kw: Any) -> Any:
        singles.append(data["node_id"])
        return await real_single(model, data, **kw)

    monkeypatch.setattr(conflict_writes, "upsert_with_conflict", _single)

    adopted = await NodeDataSlotStore().adopt_live_outputs(
        run_id=run_id, definition_id=str(uuid4()), user_id=str(uuid4())
    )

    assert adopted == 71
    assert singles == [], f"{len(singles)} single-row slot writes; adoption must send one statement"
    assert bulk_calls_by_run[run_id] == [71]
    assert slots[("step70", "last_live_output")]["value"] == {"n": 70}
    assert ("huge", "last_live_output") not in slots


@pytest.mark.asyncio
async def test_a_run_with_nothing_to_adopt_writes_nothing(monkeypatch: pytest.MonkeyPatch) -> None:
    run_id = str(uuid4())
    _wire(monkeypatch, run_id, [], stored={})
    assert (
        await NodeDataSlotStore().adopt_live_outputs(
            run_id=run_id, definition_id=str(uuid4()), user_id=str(uuid4())
        )
        == 0
    )
    assert run_id not in bulk_calls_by_run


@pytest.mark.asyncio
async def test_a_step_whose_result_is_json_null_still_lands(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    run_id = str(uuid4())
    slots = _wire(
        monkeypatch,
        run_id,
        [_outcome(run_id, "a", {"n": 1}), _outcome(run_id, "nothing", None)],
        stored={},
    )
    adopted = await NodeDataSlotStore().adopt_live_outputs(
        run_id=run_id, definition_id=str(uuid4()), user_id=str(uuid4())
    )
    assert adopted == 2
    assert bulk_calls_by_run[run_id] == [1]
    assert slots[("nothing", "last_live_output")]["value"] is None
