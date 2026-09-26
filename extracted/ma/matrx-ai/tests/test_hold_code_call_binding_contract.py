"""hold_code_call honors the WHOLE binding contract, and every refusal is recorded.

Found 2026-09-25 (independent review of the code-call conversion): the door
passed the site's variables straight to the Holder — a binding's
``variable_mapping`` / ``spill_variables`` / consumption map were ignored, the
post-run ``complete`` check never ran, and only a resolver exception left a
durable record. A rebind to an agent with different variable names rendered
empty variables and nothing said so.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

import matrx_ai.mandates as mandates
from matrx_ai.agents.variables import AgentVariable


class _Agent:
    def __init__(self, declared: dict[str, AgentVariable]) -> None:
        self.variable_defaults = declared
        self.name = "Fake Holder"
        self.bound: dict[str, Any] = {}
        self.config = SimpleNamespace(
            model="holder-model",
            system_instruction=None,
            resolved_system_instruction="SYSTEM",
            messages=[],
            temperature=0.2,
            max_output_tokens=900,
        )

    def apply_config_overrides(self, **_kwargs: Any) -> None:
        return None

    def with_variables(self, **variables: Any) -> _Agent:
        self.bound.update(variables)
        return self


class _Source:
    agent_id = "11111111-1111-1111-1111-111111111111"
    is_version = False

    def __init__(self, agent: _Agent) -> None:
        self._agent = agent

    async def load(self) -> _Agent:
        return self._agent


@pytest.fixture
def records(monkeypatch):
    captured: list[dict[str, Any]] = []

    async def _report(*, mandate_key, consumer, exc):
        captured.append({"mandate_key": mandate_key, "consumer": consumer, "reason": str(exc)})

    monkeypatch.setattr(mandates, "_report_resolution_failure", _report)
    return captured


def _install(monkeypatch, resolution: mandates.MandateResolution) -> None:
    async def _resolver(_key: str):
        return resolution

    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", _resolver)


async def test_variable_mapping_renames_onto_the_holders_variables(monkeypatch, records) -> None:
    agent = _Agent({"body": AgentVariable(name="body", required=True)})
    _install(
        monkeypatch,
        mandates.MandateResolution(
            source=_Source(agent),
            variable_mapping={"body": {"mapType": "offered_value", "target": "text"}},
        ),
    )

    held = await mandates.hold_code_call("x.y", consumer="t", variables={"text": "hello"})

    assert agent.bound == {"body": "hello"}
    assert held.variables == {"body": "hello"}
    assert records == []


async def test_spilled_values_reach_the_request(monkeypatch, records) -> None:
    agent = _Agent({})
    _install(
        monkeypatch,
        mandates.MandateResolution(source=_Source(agent), spill_variables=frozenset({"notes"})),
    )

    held = await mandates.hold_code_call("x.y", consumer="t", variables={"notes": "remember X"})

    assert held.spilled_text and "remember X" in held.spilled_text
    config = mandates.held_request_config(held)
    assert any("remember X" in str(m.content) for m in config.messages)


async def test_blocking_mapping_is_refused_and_recorded(monkeypatch, records) -> None:
    agent = _Agent({"body": AgentVariable(name="body", required=True)})
    _install(
        monkeypatch,
        mandates.MandateResolution(
            source=_Source(agent), variable_mapping={"body": {"mapType": "unmapped"}}
        ),
    )

    with pytest.raises(mandates.MandateResolutionUnavailable):
        await mandates.hold_code_call("x.y", consumer="t", variables={"text": "hi"})
    assert records and records[0]["mandate_key"] == "x.y"


async def test_workflow_holder_refusal_is_recorded(monkeypatch, records) -> None:
    _install(
        monkeypatch,
        mandates.MandateResolution(source=None, holder_type="workflow", workflow_id="w"),
    )

    with pytest.raises(mandates.MandateResolutionUnavailable):
        await mandates.hold_code_call("x.y", consumer="t")
    assert len(records) == 1


async def test_consumption_map_goes_through_the_host_pipeline(monkeypatch, records) -> None:
    agent = _Agent({"body": AgentVariable(name="body")})
    seen: list[dict[str, Any]] = []

    async def _materialize(supplied: dict[str, Any]) -> dict[str, Any]:
        seen.append(supplied)
        return {"body": supplied["text"].upper()}

    _install(
        monkeypatch,
        mandates.MandateResolution(
            source=_Source(agent),
            consumption_map={"body": {"source": "text"}},
            materialize=_materialize,
        ),
    )

    await mandates.hold_code_call("x.y", consumer="t", variables={"text": "hi"})

    assert seen == [{"text": "hi"}]
    assert agent.bound == {"body": "HI"}


async def test_consumption_map_without_a_pipeline_refuses(monkeypatch, records) -> None:
    _install(
        monkeypatch,
        mandates.MandateResolution(
            source=_Source(_Agent({})), consumption_map={"body": {"source": "text"}}
        ),
    )

    with pytest.raises(mandates.MandateResolutionUnavailable):
        await mandates.hold_code_call("x.y", consumer="t", variables={"text": "hi"})
    assert len(records) == 1


async def test_finish_runs_the_post_run_check(monkeypatch, records) -> None:
    completed: list[tuple] = []

    async def _complete(result, variables, user_input):
        completed.append((result.output, result.model_id, variables))

    agent = _Agent({"body": AgentVariable(name="body")})
    _install(monkeypatch, mandates.MandateResolution(source=_Source(agent), complete=_complete))

    held = await mandates.hold_code_call("x.y", consumer="t", variables={"body": "b"})
    await held.finish('{"ok": true}')

    assert completed == [('{"ok": true}', "holder-model", {"body": "b"})]
