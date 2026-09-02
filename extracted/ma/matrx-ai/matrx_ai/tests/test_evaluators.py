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


async def test_judge_raises_when_no_api_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    judge = AIJudge(api_key=None)
    with pytest.raises(JudgeError, match="ANTHROPIC_API_KEY"):
        await judge.judge(rubric="r", actual_output="o")


def test_judge_default_model_is_opus():
    judge = AIJudge()
    assert judge.model.startswith("claude-opus")


def test_judge_web_access_default_true():
    judge = AIJudge()
    assert judge.web_access is True


def test_judge_max_iterations_overrideable():
    judge = AIJudge(max_iterations=10)
    assert judge.max_iterations == 10


async def test_judge_routes_web_search_and_cost_capture_through_funnel(monkeypatch):
    captured = {}

    async def fake_structured(**kwargs):
        captured.update(kwargs)
        return JudgeVerdict(
            verdict="pass",
            confidence=0.9,
            reasoning="Meets the rubric.",
        )

    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setattr(
        "matrx_ai.evaluators.ai_judge.llm_messages_to_pydantic",
        fake_structured,
    )

    verdict = await AIJudge(web_access=True).judge("be correct", {"answer": 42})

    assert verdict.verdict == "pass"
    assert captured["internal_web_search"] is True
    assert captured["system_run"] is True
    assert captured["store"] is True
    assert captured["output_cls"] is JudgeVerdict
