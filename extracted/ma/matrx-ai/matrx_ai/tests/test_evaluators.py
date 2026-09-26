"""Unit tests for :class:`matrx_ai.evaluators.AIJudge` — schema, error paths, no real API calls."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from matrx_ai.evaluators import AIJudge, JudgeError, JudgeVerdict


def test_verdict_round_trip():
    v = JudgeVerdict(
        verdict="pass",
        confidence=0.9,
        reasoning="Output meets the rubric.",
        evidence=["matched X", "matched Y"],
    )
    dumped = v.model_dump()
    assert dumped["verdict"] == "pass"
    assert dumped["evidence"] == ["matched X", "matched Y"]
    assert dumped["failure_modes"] == []


def test_verdict_rejects_extra_fields():
    with pytest.raises(ValidationError):
        JudgeVerdict(
            verdict="pass",
            confidence=0.5,
            reasoning="r",
            extra_field="nope",  # type: ignore[call-arg]
        )


def test_verdict_rejects_invalid_verdict_literal():
    with pytest.raises(ValidationError):
        JudgeVerdict(verdict="maybe", confidence=0.5, reasoning="r")  # type: ignore[arg-type]


def test_verdict_confidence_bounds():
    with pytest.raises(ValidationError):
        JudgeVerdict(verdict="pass", confidence=1.5, reasoning="r")
    with pytest.raises(ValidationError):
        JudgeVerdict(verdict="pass", confidence=-0.1, reasoning="r")


def test_verdict_requires_non_empty_reasoning():
    with pytest.raises(ValidationError):
        JudgeVerdict(verdict="pass", confidence=0.5, reasoning="")


def _held(**overrides):
    from matrx_ai.mandates import HeldCall

    base = dict(
        mandate_key="proof_runs.judge",
        model="holder-model",
        system="HOLDER SYSTEM",
        temperature=None,
        max_output_tokens=4096,
        turns=[{"role": "user", "content": "## Rubric\nbe correct"}],
        config=type("Cfg", (), {"internal_web_search": True})(),
        metadata={"mandate_key": "proof_runs.judge", "mandate_holder": {"agent_id": "a"}},
    )
    base.update(overrides)
    return HeldCall(**base)


async def test_judge_runs_on_its_mandate_holder_not_a_code_default(monkeypatch):
    """RED on the pre-2026-09-25 code (hard-coded claude-opus-4-7 + inline prompt);
    GREEN when the model, prompt, turns and web access all come from the Holder."""
    captured: dict = {}
    held_calls: list = []

    async def fake_hold(key, **kwargs):
        held_calls.append((key, kwargs))
        return _held()

    async def fake_structured(**kwargs):
        captured.update(kwargs)
        return JudgeVerdict(verdict="pass", confidence=0.9, reasoning="Meets the rubric.")

    monkeypatch.setattr("matrx_ai.evaluators.ai_judge.hold_code_call", fake_hold)
    monkeypatch.setattr("matrx_ai.graph_nodes._strict_json.llm_messages_to_pydantic", fake_structured)

    verdict = await AIJudge().judge("be correct", {"answer": 42})

    assert verdict.verdict == "pass"
    assert held_calls[0][0] == "proof_runs.judge"
    assert held_calls[0][1]["variables"]["rubric"] == "be correct"
    assert captured["model"] == "holder-model"
    assert captured["system"] == "HOLDER SYSTEM"
    assert captured["messages"] == [{"role": "user", "content": "## Rubric\nbe correct"}]
    assert captured["internal_web_search"] is True
    assert captured["metadata"]["mandate_key"] == "proof_runs.judge"
    assert captured["system_run"] is True
    assert captured["store"] is True
    assert captured["output_cls"] is JudgeVerdict


async def test_explicit_model_and_web_access_are_run_scope_overrides(monkeypatch):
    captured: dict = {}

    async def fake_hold(key, **kwargs):
        return _held()

    async def fake_structured(**kwargs):
        captured.update(kwargs)
        return JudgeVerdict(verdict="fail", confidence=0.4, reasoning="Missing X.")

    monkeypatch.setattr("matrx_ai.evaluators.ai_judge.hold_code_call", fake_hold)
    monkeypatch.setattr("matrx_ai.graph_nodes._strict_json.llm_messages_to_pydantic", fake_structured)

    await AIJudge(model="run-model", web_access=False).judge("r", "o")

    assert captured["model"] == "run-model"
    assert captured["internal_web_search"] is False


async def test_web_access_reaches_the_holders_instructions_and_ceiling_is_the_holders(monkeypatch):
    """The Holder's rule 6 reads {{web_search}}; a caller that turns web off must
    say so to the Holder, not just to the provider. With no explicit ceiling the
    Holder's max output tokens apply (review items 6 + 7, 2026-09-25)."""
    captured: dict = {}
    held_calls: list = []

    async def fake_hold(key, **kwargs):
        held_calls.append(kwargs)
        return _held(max_output_tokens=1234)

    async def fake_structured(**kwargs):
        captured.update(kwargs)
        return JudgeVerdict(verdict="pass", confidence=0.9, reasoning="ok")

    monkeypatch.setattr("matrx_ai.evaluators.ai_judge.hold_code_call", fake_hold)
    monkeypatch.setattr("matrx_ai.graph_nodes._strict_json.llm_messages_to_pydantic", fake_structured)

    await AIJudge(web_access=False).judge("r", "o")
    assert held_calls[0]["variables"]["web_search"] == "not allowed"
    assert captured["max_tokens"] == 1234

    await AIJudge(max_tokens=900).judge("r", "o")
    assert "web_search" not in held_calls[1]["variables"]
    assert captured["max_tokens"] == 900


async def test_judge_refuses_when_its_mandate_cannot_resolve(monkeypatch):
    from matrx_ai.mandates import MandateResolutionUnavailable

    async def fake_hold(key, **kwargs):
        raise MandateResolutionUnavailable(key, "AIJudge", "no resolver")

    monkeypatch.setattr("matrx_ai.evaluators.ai_judge.hold_code_call", fake_hold)
    with pytest.raises(JudgeError, match="could not resolve its mandate"):
        await AIJudge().judge(rubric="r", actual_output="o")


def test_judge_max_iterations_overrideable():
    judge = AIJudge(max_iterations=10)
    assert judge.max_iterations == 10
