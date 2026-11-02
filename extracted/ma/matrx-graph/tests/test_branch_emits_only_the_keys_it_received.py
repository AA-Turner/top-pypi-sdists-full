"""A branch routes its input on, unchanged: it never adds its own ``value`` default to what it emits.

Live 2026-10-22 (agent_build run faaf147b): a build ending without a kept agent crashed at "Tell the
door" because ``stop_gate`` (control.branch) emitted the build's state plus ``value: None``, and the
strict state (``AgentBuildState``, extra=forbid) refused the extra key. A ``value`` the caller did
send still travels; the predicate still sees ``inputs['value']`` either way."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_graph.nodes.control.branch import BranchConfig, BranchExecutor, BranchInput


async def _run(payload: dict, predicate: str) -> tuple[list[tuple[str, dict]], dict]:
    emitted: list[tuple[str, dict]] = []
    ctx = SimpleNamespace(emit=lambda handle, p: emitted.append((handle, p)))
    result = await BranchExecutor().execute(ctx, BranchInput.model_validate(payload), BranchConfig(predicate=predicate))
    return emitted, result.result.model_dump(mode="json")


@pytest.mark.asyncio
async def test_a_state_without_value_is_emitted_without_value() -> None:
    emitted, _ = await _run({"saved_agent_id": None, "has_person": False, "verdict": "fail"},
                            "inputs['saved_agent_id'] is not None and inputs['has_person']")
    assert emitted == [("false", {"saved_agent_id": None, "has_person": False, "verdict": "fail"})]


@pytest.mark.asyncio
async def test_a_sent_value_still_travels_and_the_predicate_still_sees_value() -> None:
    emitted, out = await _run({"value": 3}, "inputs['value'] > 0")
    assert emitted == [("true", {"value": 3})]
    assert out["value"] == 3 and out["direction"] == "true"
    emitted, _ = await _run({"x": 1}, "inputs['value'] is None")  # unset value reads as None in the predicate
    assert emitted == [("true", {"x": 1})]


@pytest.mark.asyncio
@pytest.mark.parametrize(("handle", "should_pass"), [("true", True), ("false", False)])
async def test_emitted_payload_keeps_upstream_markers_and_result_has_branch_marker(handle: str, should_pass: bool) -> None:
    payload = {"__kind": "source_state", "nested": {"__kind": "nested_state"}, "pass": should_pass}
    original = {**payload, "nested": dict(payload["nested"])}
    emitted, result = await _run(payload, "inputs['pass']")

    assert emitted == [(handle, original)]
    assert result["__kind"] == "branch_result"
    assert result["nested"] == {"__kind": "nested_state"}
    assert result["direction"] == handle
    assert payload == original


@pytest.mark.asyncio
async def test_branch_result_direction_overrides_an_input_direction() -> None:
    emitted, result = await _run({"direction": "upstream", "x": 1}, "inputs['x'] > 0")
    assert emitted == [("true", {"direction": "upstream", "x": 1})]
    assert result["direction"] == "true"
