"""``ai.mandate.start`` asks the host's test-mode answer source (``mandate_taps.MandateReplay``) once,
after the binding, and only a host answer skips the real run.

Proves: no host installed → the real run, nothing asked; a host miss → the real run, and the real result
is offered back with the SAME fingerprint; a host hit → the doer never runs and the step returns the
host's answer; a host that raises is a miss (the real run follows), never a failed step.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai import mandate_taps
from matrx_ai.graph_nodes import mandate_action as ma
from matrx_ai.graph_nodes.agent_action import StepAgent
from matrx_ai.graph_nodes.shared import AiExecutionResult


def _result(text: str) -> AiExecutionResult:
    return AiExecutionResult(conversation_id="c", request_id="r", iterations=1, final_text=text)


class _Host:
    def __init__(self, answer: dict[str, Any] | None = None, boom: bool = False) -> None:
        self.answer, self.boom = answer, boom
        self.looked: list[tuple[str, str, Any, dict[str, Any]]] = []
        self.stored: list[tuple[dict[str, Any], dict[str, Any]]] = []

    async def lookup(self, door: str, key: str, run_id: Any, fp: dict[str, Any]) -> dict[str, Any] | None:
        self.looked.append((door, key, run_id, fp))
        if self.boom:
            raise RuntimeError("seam down")
        return self.answer

    async def store(self, door: str, key: str, run_id: Any, fp: dict[str, Any], result: dict[str, Any]) -> None:
        self.stored.append((fp, result))


@pytest.fixture()
def step(monkeypatch: pytest.MonkeyPatch):
    runs: list[Any] = []

    async def resolve(*_a: Any, **_k: Any) -> StepAgent:
        # A Run Mandate step hands its state over and the binding picks (cd3a048b87): the doer's
        # ``facts`` arrive through the mandate's map, never fed by name.
        async def materialize(supplied: dict[str, Any]) -> dict[str, Any]:
            return {"facts": supplied["facts"]}

        return StepAgent(agent_id="agent-1", is_version=False, config_overrides={"m": 1}, declared_output_kind=None,
                         materialize=materialize, consumption_map={"facts": [{"target": "facts"}]})

    async def limit(_ctx: Any, _authored: Any) -> Any:
        return SimpleNamespace(value=10, name_on=lambda r: r)

    async def run(_ctx: Any, agent_id: str, request: Any, mandate_key: str, **_kw: Any) -> AiExecutionResult:
        runs.append(agent_id)
        return _result("real answer")

    monkeypatch.setattr(ma, "resolve_step_agent_full", resolve)
    monkeypatch.setattr(ma, "resolve_step_iteration_limit", limit)
    monkeypatch.setattr(ma, "build_agent_request", lambda *a, **k: {"req": True})
    monkeypatch.setattr(ma, "run_step_agent", run)
    yield runs
    mandate_taps.set_mandate_replay(None)


def _go() -> Any:
    ctx = SimpleNamespace(node_id="we_think", run_id="run-9")
    inputs = ma.MandateStartInput.model_validate({"mandate_key": "brand_intake.we_think", "provision_values": {"facts": "x"}})
    return asyncio.run(ma._mandate_start_body(ctx, inputs, None)).result


def test_no_host_is_the_real_run(step) -> None:
    assert _go().final_text == "real answer" and step == ["agent-1"]


def test_a_miss_runs_for_real_and_offers_the_result_back(step) -> None:
    host = _Host()
    mandate_taps.set_mandate_replay(host)
    assert _go().final_text == "real answer" and step == ["agent-1"]
    (door, key, run_id, fp), = host.looked
    assert (door, key, run_id) == ("workflow_step", "brand_intake.we_think", "run-9")
    assert fp["agent_id"] == "agent-1" and fp["config_overrides"] == {"m": 1} and fp["inputs"]["facts"] == "x"
    (stored_fp, stored), = host.stored
    assert stored_fp == fp and stored["final_text"] == "real answer"


def test_a_hit_never_runs_the_doer(step) -> None:
    host = _Host(answer={**_result("saved answer").model_dump(), "metadata": {"ai_test_replay": {"mode": "replay"}}})
    mandate_taps.set_mandate_replay(host)
    out = _go()
    assert out.final_text == "saved answer" and out.metadata["ai_test_replay"]["mode"] == "replay"
    assert step == [], "a replayed step must not call the agent" and not host.stored


def test_a_broken_host_is_a_miss_not_a_failure(step) -> None:
    mandate_taps.set_mandate_replay(_Host(boom=True))
    assert _go().final_text == "real answer" and step == ["agent-1"]
