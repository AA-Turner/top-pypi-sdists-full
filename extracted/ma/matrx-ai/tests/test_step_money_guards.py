"""The money guards of a workflow AI step (2026-10-27): the pause switch and the per-call caps.

Proves, through the real step code:
* a Run Mandate step asks the host's ONE pause check (``mandate_pause_check``) before anything
  resolves or spends, and a paused mandate refuses in words;
* ``max_output_tokens`` reaches the request as the top config layer (above authored and run
  overrides) and never as a stray request field;
* ``max_call_cost_usd`` opens the per-call spend cap around the agent run, and the cap refuses a
  call estimated over it (exact request + output ceiling at catalog price) before anything is sent,
  refuses an unpriceable call, and admits one under it;
* a workflow-held mandate with a cap refuses (its calls cannot be capped from this step).
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai import _ext
from matrx_ai.config import usage_config
from matrx_ai.graph_nodes import agent_action
from matrx_ai.graph_nodes import mandate_action as ma
from matrx_ai.graph_nodes.agent_action import AgentStartInput, StepWorkflowMandate, agent_start
from matrx_ai.providers import guardrail_gate as gg


class _Paused(Exception):
    pass


def test_a_paused_mandate_step_refuses_before_anything_resolves(monkeypatch: pytest.MonkeyPatch) -> None:
    asked: list[str] = []
    resolved: list[str] = []

    async def pause_check(mandate_key: str) -> None:
        asked.append(mandate_key)
        raise _Paused("Paused until it has a decision step and a spend cap.")

    async def resolve(*_a: Any, **_k: Any) -> Any:
        resolved.append("resolved")
        raise AssertionError("a paused step must not resolve its doer")

    monkeypatch.setitem(_ext._registry, "mandate_pause_check", pause_check)
    monkeypatch.setattr(ma, "resolve_step_agent_full", resolve)
    inputs = ma.MandateStartInput.model_validate({"mandate_key": "seo.ai_visibility_question_qa"})
    with pytest.raises(_Paused, match="Paused until"):
        asyncio.run(ma._mandate_start_body(SimpleNamespace(node_id="qa", run_id="r"), inputs, None))
    assert asked == ["seo.ai_visibility_question_qa"] and resolved == []


def test_a_workflow_held_mandate_with_a_cap_refuses(monkeypatch: pytest.MonkeyPatch) -> None:
    async def resolve(*_a: Any, **_k: Any) -> Any:
        return object.__new__(StepWorkflowMandate)

    async def never(*_a: Any, **_k: Any) -> Any:
        raise AssertionError("the workflow holder must not start")

    monkeypatch.setattr(ma, "resolve_step_agent_full", resolve)
    monkeypatch.setattr(ma, "_run_workflow_held_mandate", never)
    inputs = ma.MandateStartInput.model_validate({"mandate_key": "k", "max_call_cost_usd": 0.05})
    with pytest.raises(ValueError, match="cannot cap"):
        asyncio.run(ma._mandate_start_body(SimpleNamespace(node_id="s", run_id="r"), inputs, None))


def _capture(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    captured: dict[str, Any] = {}

    class FakeAgentStartRequest:
        @classmethod
        def model_validate(cls, payload: dict[str, Any]) -> Any:
            captured["payload"] = payload
            return SimpleNamespace()

    async def fake_agent_runner(agent_id: str, request: Any, app_ctx: Any) -> str:
        captured["cap"] = gg._CALL_SPEND_CAP.get()
        return "completed"

    async def warm() -> dict[str, Any]:
        captured["warmed"] = True
        return {}

    monkeypatch.setitem(_ext._registry, "agent_runner", fake_agent_runner)
    monkeypatch.setitem(_ext._registry, "AgentStartRequest", FakeAgentStartRequest)
    monkeypatch.setattr(agent_action, "normalize_completed_result", lambda value, **_kwargs: value)
    monkeypatch.setattr(usage_config, "ensure_pricing_lookup", warm)
    return captured


def _ctx() -> Any:
    return SimpleNamespace(app=SimpleNamespace(), node_id="qa", organization_id="8fd3a0e1-0000-4000-8000-000000000001")


@pytest.mark.asyncio
async def test_step_limits_reach_the_run(monkeypatch: pytest.MonkeyPatch) -> None:
    captured = _capture(monkeypatch)
    inputs = AgentStartInput.model_validate(
        {
            "agent_id": "4185e955-0f4e-4faa-b63c-704bb876c85f",
            "config_overrides": {"temperature": 0.2, "max_output_tokens": 999},
            "runtime_config_overrides": {"max_output_tokens": 500},
            "max_output_tokens": 20000,
            "max_call_cost_usd": 0.15,
        }
    )
    assert await agent_start(_ctx(), inputs) == "completed"  # type: ignore[arg-type]
    payload = captured["payload"]
    assert payload["config_overrides"]["max_output_tokens"] == 20000
    assert payload["config_overrides"]["temperature"] == 0.2
    assert "max_call_cost_usd" not in payload and "max_output_tokens" not in payload
    cap = captured["cap"]
    assert cap is not None and cap.max_usd == 0.15 and "qa" in cap.subject
    assert captured.get("warmed") is True
    assert gg._CALL_SPEND_CAP.get() is None, "the cap never outlives the step"


@pytest.mark.asyncio
async def test_no_limits_no_cap(monkeypatch: pytest.MonkeyPatch) -> None:
    captured = _capture(monkeypatch)
    inputs = AgentStartInput.model_validate({"agent_id": "4185e955-0f4e-4faa-b63c-704bb876c85f"})
    await agent_start(_ctx(), inputs)  # type: ignore[arg-type]
    assert captured["cap"] is None and "config_overrides" not in captured["payload"]


def _price(monkeypatch: pytest.MonkeyPatch, priced: bool = True) -> None:
    # $1 per million in, $4 per million out — or no catalog price at all.
    def cost(self: Any, _lookup: Any = None, _at: Any = None) -> float | None:
        return (self.input_tokens * 1 + self.output_tokens * 4) / 1e6 if priced else None

    monkeypatch.setattr(usage_config.TokenUsage, "calculate_catalog_cost", cost)
    monkeypatch.setattr(usage_config, "_get_db_pricing_lookup", lambda: {})


def _config(out: int | None, prompt_chars: int = 40_000) -> Any:
    return SimpleNamespace(
        system_instruction="x" * prompt_chars, messages=[], tools=[], max_output_tokens=out,
        matrx_model_name="gemini-3.8-flash",
    )


def test_the_cap_refuses_a_call_estimated_over_it(monkeypatch: pytest.MonkeyPatch) -> None:
    _price(monkeypatch)
    with gg.call_spend_cap_scope(0.05, subject="Step qa"):
        with pytest.raises(gg.GuardrailStopError, match=r"over its \$0\.05 cap") as refused:
            gg.admit_call_spend_cap(None, _config(20_000))  # 80k out alone = $0.08
    assert refused.value.kind == gg.CALL_SPEND_CAP and refused.value.is_caller_refusal
    assert refused.value.observed and refused.value.observed > 0.05


def test_the_cap_admits_a_call_under_it(monkeypatch: pytest.MonkeyPatch) -> None:
    _price(monkeypatch)
    with gg.call_spend_cap_scope(0.15, subject="Step qa"):
        gg.admit_call_spend_cap(None, _config(20_000))


def test_the_cap_refuses_what_it_cannot_price(monkeypatch: pytest.MonkeyPatch) -> None:
    _price(monkeypatch)
    with gg.call_spend_cap_scope(0.15, subject="Step qa"):
        with pytest.raises(gg.GuardrailStopError, match="longest-answer limit"):
            gg.admit_call_spend_cap(None, _config(None))
        with pytest.raises(gg.GuardrailStopError, match="no request to price"):
            gg.admit_call_spend_cap(None, None)
    _price(monkeypatch, priced=False)
    with gg.call_spend_cap_scope(0.15, subject="Step qa"):
        with pytest.raises(gg.GuardrailStopError, match="no catalog price"):
            gg.admit_call_spend_cap(None, _config(1000))


def test_no_scope_and_zero_cap_check_nothing(monkeypatch: pytest.MonkeyPatch) -> None:
    _price(monkeypatch, priced=False)
    gg.admit_call_spend_cap(None, _config(None))
    with gg.call_spend_cap_scope(0, subject="Step qa"):
        gg.admit_call_spend_cap(None, _config(None))


def test_every_paid_call_is_asked(monkeypatch: pytest.MonkeyPatch) -> None:
    """The cap is asked inside ``admit_guardrails`` — the gate every paid dispatch passes."""
    _price(monkeypatch)
    with gg.call_spend_cap_scope(0.01, subject="Step qa"):
        with pytest.raises(gg.GuardrailStopError, match="cap per AI call"):
            gg.admit_guardrails(None, _config(20_000))
