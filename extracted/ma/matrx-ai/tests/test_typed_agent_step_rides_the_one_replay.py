"""Run Typed Agent asks the ONE mandate replay hook, keyed exactly as Run Mandate and the code path key it.

Why (2026-11-10): a person's PICKED agent runs through Run Typed Agent, which had no replay or stand-in door — a
test pair whose topic has picks set bought every answer (or was refused) on the workflow side while the code side
replayed. Now the step asks ``mandate_taps.replay_answer`` after its binding: the key is the job it runs as (a named
mandate, a converted step's ``mandate_key_origin``, or its agent's own job; with no job, its agent), the fingerprint
is ``answer_fingerprint`` over the resolved agent and the variables it runs on. A host answer skips the doer; a miss
runs it and offers the real answer back. Red before: the host was never asked.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai import mandate_taps
from matrx_ai.graph_nodes import agent_produce_action as ap
from matrx_ai.graph_nodes.agent_action import StepAgent
from matrx_ai.graph_nodes.shared import AiExecutionResult

JOB = "research.structured_page_summary"
VARIABLES = {"page_content": "a page", "topic": {"name": "t"}}


def _answer(text: str) -> AiExecutionResult:
    return AiExecutionResult(conversation_id="c", request_id="r", iterations=1, final_text=text,
                             structured_output={"summary": text})


class _Host:
    def __init__(self, answer: dict[str, Any] | None = None) -> None:
        self.answer = answer
        self.looked: list[tuple[str, str, dict[str, Any]]] = []
        self.stored: list[tuple[str, str, dict[str, Any], dict[str, Any]]] = []

    async def lookup(self, door: str, key: str, _run: Any, fp: dict[str, Any]) -> dict[str, Any] | None:
        self.looked.append((door, key, fp))
        return self.answer

    async def store(self, door: str, key: str, _run: Any, fp: dict[str, Any], result: dict[str, Any]) -> None:
        self.stored.append((door, key, fp, result))


class _ReachedTheAnswer(Exception):
    """Raised by the test's stand-in for the step's own answer handling: the hook is what is under test."""

    def __init__(self, normalized: AiExecutionResult) -> None:
        self.normalized = normalized


@pytest.fixture()
def step(monkeypatch: pytest.MonkeyPatch):
    runs: list[str] = []

    async def resolve(*_a: Any, **_k: Any) -> StepAgent:
        return StepAgent(agent_id="picked-1", is_version=False, config_overrides={}, declared_output_kind=None)

    async def limit(_ctx: Any, _authored: Any) -> Any:
        return SimpleNamespace(value=10, name_on=lambda r: r)

    async def bind(_key: str, **_k: Any) -> Any:
        async def fill(variables: Any) -> Any:
            return dict(variables or {})

        return fill

    async def run(_ctx: Any, agent_id: str, _request: Any, **_kw: Any) -> tuple[Any, None]:
        runs.append(agent_id)
        return _answer("real answer"), None

    async def fmt(*_a: Any) -> dict[str, Any]:
        return {}

    def stop(_ctx: Any, normalized: AiExecutionResult) -> None:
        raise _ReachedTheAnswer(normalized)

    monkeypatch.setattr(ap, "require_agent_host", lambda _n: None)
    monkeypatch.setattr(ap, "_declared_kind", lambda *_a: "research_page_analysis")
    monkeypatch.setattr(ap, "refuse_if_mandate_paused", _noop)
    monkeypatch.setattr(ap, "resolve_step_agent_full", resolve)
    monkeypatch.setattr(ap, "_assert_declarations_agree", lambda *_a: None)
    monkeypatch.setattr(ap, "resolve_step_iteration_limit", limit)
    monkeypatch.setattr(ap, "_response_format_for", fmt)
    monkeypatch.setattr(ap, "build_agent_request", lambda *_a, **_k: SimpleNamespace(variables=dict(VARIABLES)))
    monkeypatch.setattr(ap, "job_variable_binder", bind)
    monkeypatch.setattr(ap, "run_walled_step_agent", run)
    monkeypatch.setattr(ap, "_record_spend", stop)
    yield runs
    mandate_taps.set_mandate_replay(None)


async def _noop(*_a: Any, **_k: Any) -> None:
    return None


def _go(origin: str | None = JOB) -> AiExecutionResult:
    ctx = SimpleNamespace(node_id="ask_pick", run_id="run-b")
    inputs = ap.AgentProduceInput.model_validate({"agent_id": "picked-1"})
    config = SimpleNamespace(mandate_key_origin=origin, exposed_variables=[], variable_sources={}, include_org_catalog=False)
    try:
        asyncio.run(ap._agent_produce_body(ctx, inputs, config))  # type: ignore[arg-type]
    except _ReachedTheAnswer as reached:
        return reached.normalized
    raise AssertionError("the step never reached its answer")


def _expected() -> dict[str, Any]:
    return mandate_taps.answer_fingerprint(agent_id="picked-1", is_version=False, variables=VARIABLES,
                                           user_input=None, config_overrides={})


def test_a_host_answer_skips_the_picked_agent(step: list[str]) -> None:
    host = _Host(answer=_answer("the stand-in").model_dump(mode="json"))
    mandate_taps.set_mandate_replay(host)
    got = _go()
    assert step == [], "the doer must not run when the host answers"
    assert got.final_text == "the stand-in" and got.metadata["agent_id"] == "picked-1"
    # Keyed as Run Mandate and the code path key it: the ONE door, the job, the agent and its variables.
    assert host.looked == [(mandate_taps.MANDATE_DOOR, JOB, _expected())]
    assert host.stored == []


def test_a_miss_runs_the_agent_and_offers_the_real_answer_back(step: list[str]) -> None:
    host = _Host()
    mandate_taps.set_mandate_replay(host)
    got = _go()
    assert step == ["picked-1"] and got.final_text == "real answer"
    (door, key, fp, result), = host.stored
    assert (door, key, fp) == (mandate_taps.MANDATE_DOOR, JOB, _expected())
    assert result["final_text"] == "real answer" and result["metadata"]["agent_id"] == "picked-1"


def test_a_step_with_no_job_is_keyed_on_its_agent(step: list[str]) -> None:
    host = _Host()
    mandate_taps.set_mandate_replay(host)
    _go(origin=None)
    assert host.looked[0][1] == "agent:picked-1"


def test_no_host_is_the_real_run(step: list[str]) -> None:
    assert _go().final_text == "real answer" and step == ["picked-1"]


def test_a_served_pick_hands_the_host_the_picked_agent_for_its_run_row(step: list[str], monkeypatch: pytest.MonkeyPatch) -> None:
    """Red before: a pick has no mandate run stamp, so the served answer left no request row (Idaho Update
    4bb874f0, Holders "3 on A, 0 on B"). Now the host is handed the job and the picked agent."""
    recorded: list[dict[str, Any]] = []

    async def recorder(_ctx: Any, *, mandate_key: str, stamp: dict[str, Any], answer: dict[str, Any]) -> None:
        recorded.append({"mandate_key": mandate_key, **stamp})

    from matrx_ai import _ext

    monkeypatch.setitem(_ext._registry, "mandate_step_replay_recorder", recorder)
    mandate_taps.set_mandate_replay(_Host({"conversation_id": "", "request_id": "", "iterations": 1,
                                           "final_text": "served", "structured_output": {"summary": "served"},
                                           "metadata": {"ai_test_replay": {"mode": "stand_in"}}}))
    _go()
    assert step == [], "a served answer never runs the agent"
    assert recorded == [{"mandate_key": JOB, "holder_type": "agent", "picked_agent_id": "picked-1",
                         "picked_is_version": False}]
