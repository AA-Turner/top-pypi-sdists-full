from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.tools.implementations import _summarize_helper


@pytest.mark.asyncio
async def test_summarize_content_runs_declared_variables_through_its_mandate(monkeypatch):
    captured: dict[str, object] = {}

    async def fake_run_mandated(agent_cls, **kwargs):
        captured["agent_cls"] = agent_cls
        captured.update(kwargs)
        return SimpleNamespace(success=True, output="summary", usage_history=["usage"])

    monkeypatch.setattr(_summarize_helper, "run_mandated", fake_run_mandated)

    output, usage = await _summarize_helper.summarize_content(
        "x" * 100_001,
        "Keep the facts.",
        ctx=None,
        model_id="test-model",
    )

    inputs = captured["inputs"]
    assert captured["agent_cls"] is _summarize_helper.SummarizeContentAgent
    assert inputs.instructions == "Keep the facts."
    assert inputs.content == "x" * 100_000
    assert captured["config_overrides"] == {"model": "test-model"}
    assert output == "summary"
    assert usage == ["usage"]


@pytest.mark.asyncio
async def test_summarize_content_preserves_result_failure_contract(monkeypatch):
    async def fake_run_mandated(*args, **kwargs):
        return SimpleNamespace(success=False, error="provider down", usage_history=["usage"])

    monkeypatch.setattr(_summarize_helper, "run_mandated", fake_run_mandated)

    output, usage = await _summarize_helper.summarize_content("content", "instructions", None)

    assert output == "[Summarization failed: provider down]"
    assert usage == ["usage"]


@pytest.mark.asyncio
async def test_summarize_content_never_raises(monkeypatch):
    async def fake_run_mandated(*args, **kwargs):
        raise RuntimeError("boom")

    monkeypatch.setattr(_summarize_helper, "run_mandated", fake_run_mandated)

    output, usage = await _summarize_helper.summarize_content("content", "instructions", None)

    assert output == "[Summarization failed: boom]"
    assert usage == []
