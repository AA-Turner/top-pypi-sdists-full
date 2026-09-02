"""Post-prep transform contract (PODCAST_PIPELINE.md §6/§7).

``_apply_post_prep`` is a SOFT stage: NONE passes through untouched; every
option runs its mandated agent; ANY failure — agent error, resolver exception,
or a degenerate too-short "success" — returns a failed StageResult so the
pipeline keeps the original content. Nothing here may ever kill a run.
"""

from __future__ import annotations

import asyncio

import matrx_ai.agent_runners.podcast_generator as pg
from matrx_ai.agent_runners.podcast_generator import (
    PostPrepOption,
    _apply_post_prep,
)


class _FakeResult:
    def __init__(self, *, success: bool, output: str = "", error: str | None = None):
        self.success = success
        self.output = output
        self.error = error
        self.usage = None
        self.usage_aggregated = None
        self.parsed = None


def _run(coro):
    return asyncio.new_event_loop().run_until_complete(coro)


def test_none_is_pure_pass_through():
    result = _run(_apply_post_prep("original content", PostPrepOption.NONE, language="English"))
    assert result.success is True
    assert result.output == "original content"


def test_each_option_runs_its_own_mandated_agent(monkeypatch):
    seen: list[tuple[str, dict]] = []

    async def fake_run_mandated(agent_cls, **kwargs):
        seen.append((agent_cls.mandate_key, kwargs["inputs"].model_dump()))
        return _FakeResult(success=True, output="x" * 3000)

    monkeypatch.setattr(pg, "_run_mandated", fake_run_mandated)
    content = "y" * 3000
    for option, mandate_key in [
        (PostPrepOption.TRANSLATION, "podcast.post_prep_translation"),
        (PostPrepOption.SUMMARIZATION, "podcast.post_prep_summarization"),
        (PostPrepOption.EXPANSION, "podcast.post_prep_expansion"),
        (PostPrepOption.FACT_CHECKING, "podcast.post_prep_fact_checking"),
    ]:
        result = _run(_apply_post_prep(content, option, language="Spanish"))
        assert result.success is True, option
        assert seen[-1][0] == mandate_key
    # Translation receives the run's language as its target.
    translation_inputs = seen[0][1]
    assert translation_inputs["target_language"] == "Spanish"
    assert translation_inputs["content"] == content


def test_agent_failure_is_soft(monkeypatch):
    async def fake_run_mandated(agent_cls, **kwargs):
        return _FakeResult(success=False, error="provider exploded")

    monkeypatch.setattr(pg, "_run_mandated", fake_run_mandated)
    result = _run(
        _apply_post_prep("z" * 3000, PostPrepOption.SUMMARIZATION, language="English")
    )
    assert result.success is False
    assert "provider exploded" in (result.error or "")


def test_resolver_exception_is_soft(monkeypatch):
    async def fake_run_mandated(agent_cls, **kwargs):
        raise RuntimeError("mandate resolution broke")

    monkeypatch.setattr(pg, "_run_mandated", fake_run_mandated)
    result = _run(
        _apply_post_prep("z" * 3000, PostPrepOption.EXPANSION, language="English")
    )
    assert result.success is False
    assert "mandate resolution broke" in (result.error or "")


def test_degenerate_short_output_is_rejected(monkeypatch):
    async def fake_run_mandated(agent_cls, **kwargs):
        return _FakeResult(success=True, output="tiny")

    monkeypatch.setattr(pg, "_run_mandated", fake_run_mandated)
    result = _run(
        _apply_post_prep("z" * 3000, PostPrepOption.TRANSLATION, language="French")
    )
    assert result.success is False
    assert "too little content" in (result.error or "")


def test_short_input_keeps_scaled_floor(monkeypatch):
    # A legitimately short full_content body (GATE-1-exempt) must not have its
    # transform rejected by the absolute floor — the floor scales to input/2.
    async def fake_run_mandated(agent_cls, **kwargs):
        return _FakeResult(success=True, output="w" * 300)

    monkeypatch.setattr(pg, "_run_mandated", fake_run_mandated)
    result = _run(
        _apply_post_prep("z" * 400, PostPrepOption.TRANSLATION, language="German")
    )
    assert result.success is True
    assert result.output == "w" * 300
