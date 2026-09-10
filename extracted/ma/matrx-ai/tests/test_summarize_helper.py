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


def test_summarize_agent_is_mandated_without_a_hardcoded_source():
    """A mandate_key + a hardcoded source is refused by NamedAgent; that refusal
    turned EVERY web summarize=true call into a "[Summarization failed: …]"
    shell (2026-09-08, Google sync run). The class must define cleanly."""
    agent = _summarize_helper.SummarizeContentAgent
    assert agent.mandate_key == "tools.summarize_content"
    assert getattr(agent, "source", None) is None
    agent._check_definition()  # raises TypeError on the BOTH-declared antipattern


@pytest.mark.asyncio
async def test_web_read_reports_summarize_failure_as_tool_failure(monkeypatch):
    """A failed summarization is a failed tool call, never a success whose text
    is an apology — the model must see is_error and the remedy."""
    from matrx_ai.tools.implementations import web as web_mod
    from matrx_ai.tools.models import ToolContext

    async def fake_summarize(content, instructions, ctx):
        return "[Summarization failed: mandate refused]", []

    monkeypatch.setattr(_summarize_helper, "summarize_content", fake_summarize)

    import matrx_scraper.features.read_page as read_page

    async def fake_read(url):
        # Big enough that the small-page skip does not apply.
        return {"status": "success", "result": "Gemini pricing: $0.75 in / $3.75 out\n" * 200}

    monkeypatch.setattr(read_page, "read_page_mcp_quick", fake_read)

    ctx = ToolContext(conversation_id="c1", call_id="call-1", emitter=None)
    result = await web_mod.web_read(
        {
            "urls": ["https://ai.google.dev/gemini-api/docs/pricing"],
            "summarize": True,
            "instructions": "Report prices",
        },
        ctx,
    )
    assert result.success is False
    assert result.error is not None
    assert "Summarization failed" in result.error.message
    assert "summarize=false" in (result.error.suggested_action or "")


@pytest.mark.asyncio
async def test_web_read_summarizes_the_full_page_not_the_window(monkeypatch):
    """The summarizer used to get the offset/chars window, so summarize=true
    could never spare a paging call (2026-09-09 experiment: 87% of a 69K
    pricing page never reached it). It must see the whole page."""
    from matrx_ai.tools.implementations import web as web_mod
    from matrx_ai.tools.models import ToolContext

    seen: dict[str, str] = {}

    async def fake_summarize(content, instructions, ctx):
        seen["content"] = content
        return "PRICE $0.15 cached", []

    monkeypatch.setattr(_summarize_helper, "summarize_content", fake_summarize)
    import matrx_scraper.features.read_page as read_page

    page = "A" * 6_000 + " UNIQUE-TAIL-FACT " + "B" * 6_000  # well past a 4K window

    async def fake_read(url):
        return {"status": "success", "result": page}

    monkeypatch.setattr(read_page, "read_page_mcp_quick", fake_read)
    ctx = ToolContext(conversation_id="c1", call_id="call-2", emitter=None)
    result = await web_mod.web_read(
        {
            "urls": ["https://example.com/x"],
            "summarize": True,
            "instructions": "prices",
            "chars": 4000,
        },
        ctx,
    )
    assert result.success is True
    assert "UNIQUE-TAIL-FACT" in seen["content"]
    assert len(seen["content"]) > 12_000


@pytest.mark.asyncio
async def test_web_read_skips_summarizing_a_small_page(monkeypatch):
    from matrx_ai.tools.implementations import web as web_mod
    from matrx_ai.tools.models import ToolContext

    called = {"n": 0}

    async def fake_summarize(content, instructions, ctx):
        called["n"] += 1
        return "should not run", []

    monkeypatch.setattr(_summarize_helper, "summarize_content", fake_summarize)
    import matrx_scraper.features.read_page as read_page

    async def fake_read(url):
        return {"status": "success", "result": "tiny page: price $1"}

    monkeypatch.setattr(read_page, "read_page_mcp_quick", fake_read)
    ctx = ToolContext(conversation_id="c1", call_id="call-3", emitter=None)
    result = await web_mod.web_read(
        {"urls": ["https://example.com/y"], "summarize": True, "instructions": "prices"}, ctx
    )
    assert result.success is True and called["n"] == 0
    assert "raw instead of summarizing" in str(result.output)
