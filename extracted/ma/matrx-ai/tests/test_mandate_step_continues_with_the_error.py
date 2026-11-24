"""Run Mandate ``continue_on_failure``: a refused or failed agent turn finishes the step with the error in hand.

Why (2026-11-10): code that records a failure ("failed" row with its reason, then the next page) could not be
replaced by a workflow — a refused analyst failed the step, the run stopped there, and nothing was saved. With the
flag on, the step succeeds with no answer, ``metadata.failed`` true and the reason in ``metadata.error``; the next
step saves it. Off (the default) nothing changes: the step fails. A carried failure is never recorded as a replay
answer, and a step that is wired wrong still raises.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any

import pytest
from matrx_graph.types.result import failure

from matrx_ai import mandate_taps
from matrx_ai.graph_nodes import agent_action as aa
from matrx_ai.graph_nodes import mandate_action as ma
from matrx_ai.graph_nodes.agent_action import StepAgent

REFUSAL = "Refused: this account runs only the catalog's test models; gemini-3.8-flash is not one."
USAGE = {"models": {}, "cost_usd": 0.0, "input_tokens": 0, "output_tokens": 0, "total_tokens": 0}


class _Host:
    def __init__(self) -> None:
        self.stored: list[Any] = []

    async def lookup(self, *_a: Any) -> None:
        return None

    async def store(self, *a: Any) -> None:
        self.stored.append(a)


@pytest.fixture()
def host(monkeypatch: pytest.MonkeyPatch):
    async def resolve(*_a: Any, **_k: Any) -> StepAgent:
        async def materialize(_supplied: dict[str, Any]) -> dict[str, Any]:
            return {"page_content": "a page"}

        return StepAgent(agent_id="agent-1", is_version=True, config_overrides={}, declared_output_kind=None,
                         materialize=materialize, consumption_map={"page_content": [{"target": "page_content"}]})

    async def limit(_ctx: Any, _authored: Any) -> Any:
        return SimpleNamespace(value=10, name_on=lambda r: r)

    async def run(*_a: Any, **_k: Any) -> Any:
        return SimpleNamespace(refused=True)  # a CompletedRequest whose turn failed

    def normalize(_completed: Any, *, step_config: Any = None) -> Any:
        return failure("ai_turn_failed", REFUSAL, technical="AI turn ended with status failed",
                       details={"status": "failed", "refusal_code": "automation_guardrail", "usage": USAGE,
                                "conversation_id": "conv-1", "request_id": "req-1"})

    monkeypatch.setattr(ma, "resolve_step_agent_full", resolve)
    monkeypatch.setattr(ma, "resolve_step_iteration_limit", limit)
    monkeypatch.setattr(ma, "build_agent_request", lambda *a, **k: {"req": True})
    monkeypatch.setattr(aa, "run_step_agent", run)
    monkeypatch.setattr(ma, "normalize_completed_result", normalize)
    h = _Host()
    mandate_taps.set_mandate_replay(h)
    yield h
    mandate_taps.set_mandate_replay(None)


def _go(**extra: Any) -> Any:
    ctx = SimpleNamespace(node_id="ask", run_id="run-1")
    inputs = ma.MandateStartInput.model_validate(
        {"mandate_key": "research.structured_page_summary", "provision_values": {"page": "x"}, **extra})
    return asyncio.run(ma._mandate_start_body(ctx, inputs, None))


def test_off_by_default_the_step_fails(host: _Host) -> None:
    out = _go()
    assert out.status == "error" and out.error.code == "ai_turn_failed" and out.error.message == REFUSAL


def test_on_the_step_finishes_with_the_error_and_no_answer(host: _Host) -> None:
    out = _go(continue_on_failure=True)
    assert out.status == "success"
    r = out.result
    assert r.structured_output is None and r.final_text == "" and r.finish_reason == "failed"
    assert r.metadata["failed"] is True and r.metadata["error"] == REFUSAL
    assert r.metadata["error_code"] == "ai_turn_failed"
    assert r.metadata["error_details"]["refusal_code"] == "automation_guardrail"
    assert r.metadata["agent_id"] == "agent-1", "the failed row still names who was asked"
    assert r.usage.total_tokens == 0 and (r.conversation_id, r.request_id) == ("conv-1", "req-1")
    assert host.stored == [], "a carried failure is never recorded as an answer to replay"


def test_only_a_failed_turn_is_carried() -> None:
    wired_wrong = failure("mandate_unresolved", "no holder")
    assert ma.failed_turn_as_answer(wired_wrong, node_id="ask", mandate_key="k") is wired_wrong
    fine = ma.success(ma.AiExecutionResult(conversation_id="c", request_id="r", iterations=1, final_text="hi"))
    assert ma.failed_turn_as_answer(fine, node_id="ask", mandate_key="k") is fine


def _refused(code: str) -> Any:
    from matrx_ai.mandates import MandateRefused

    async def resolve(*_a: Any, **_k: Any) -> Any:
        raise MandateRefused("research.source_triage_decision", code=code, sentence=f"refused ({code})")

    return resolve


def _go_recorded(monkeypatch: pytest.MonkeyPatch, code: str, **extra: Any) -> Any:
    monkeypatch.setattr(ma, "resolve_step_agent_full", _refused(code))
    monkeypatch.setattr(ma, "refuse_if_mandate_paused", lambda _k: asyncio.sleep(0))
    ctx = SimpleNamespace(node_id="judge", run_id="run-1")
    inputs = ma.MandateStartInput.model_validate({"mandate_key": "research.source_triage_decision", **extra})
    return asyncio.run(ma._mandate_start_recorded(ctx, inputs, None))


def test_a_job_nobody_holds_is_carried_when_the_step_continues(host: _Host, monkeypatch: pytest.MonkeyPatch) -> None:
    """Gaps round 3: the triage judge's no-Holder refusal errored the whole triage run (B read 2 pages, A 8)."""
    out = _go_recorded(monkeypatch, "unfulfilled", continue_on_failure=True)
    assert out.status == "success"
    r = out.result
    assert r.structured_output is None and r.finish_reason == "failed"
    assert r.metadata["failed"] is True and r.metadata["error_code"] == "mandate_unfulfilled"
    assert r.metadata["error"] == "refused (unfulfilled)"
    assert host.stored == []


def test_a_job_nobody_holds_still_fails_the_step_by_default(host: _Host, monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_ai.mandates import MandateRefused

    with pytest.raises(MandateRefused):
        _go_recorded(monkeypatch, "unfulfilled")


def test_any_other_refusal_still_fails_the_step(host: _Host, monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_ai.mandates import MandateRefused

    with pytest.raises(MandateRefused):
        _go_recorded(monkeypatch, "inputs", continue_on_failure=True)
