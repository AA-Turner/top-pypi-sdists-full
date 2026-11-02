"""A branch passes its input through, but its output is a ``branch_result``: an upstream
``__kind`` (a typed state) must never ride the passthrough. Live 2026-10-21: every agent_build
run stopped at its first gate — "violates its declared kind 'branch_result'"."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_graph.nodes.control.branch import BranchConfig, BranchExecutor, BranchInput


@pytest.mark.asyncio
async def test_a_typed_input_does_not_overwrite_the_branch_result_marker() -> None:
    emitted: list[tuple[str, dict]] = []
    ctx = SimpleNamespace(emit=lambda handle, payload: emitted.append((handle, payload)))
    inputs = BranchInput.model_validate({"__kind": "agent_build_state", "rerun_idx": 0, "contract": None})
    result = await BranchExecutor().execute(ctx, inputs, BranchConfig(predicate="inputs['contract'] is None"))
    out = result.result.model_dump(mode="json", by_alias=True)
    assert out["direction"] == "true"
    assert out.get("__kind") in (None, "branch_result"), out
    assert out["rerun_idx"] == 0  # the rest still passes through
    assert emitted and emitted[0][0] == "true"
