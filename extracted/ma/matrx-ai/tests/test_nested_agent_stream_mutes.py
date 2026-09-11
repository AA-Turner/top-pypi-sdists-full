"""Runtime proof that tool-scope nested agent runs are muted.

THE CLASS: an agent run started while a parent agent is streaming to a user
inherits the parent's emitter, so unless it is explicitly muted every one of its
tokens is delivered to that user as if the parent had said it. Proven live
2026-09-08 — ~860K characters of the agent factory's partial JSON envelope
poured into a Creator's Plan Room as chat text.

``scripts/check_nested_agent_streams.py`` is the static layer. This is the
independent second one: it CALLS each helper for real, with the runner replaced
by a spy, and asserts the kwarg that actually reaches ``run_agent``. A static
guard cannot see a kwarg computed at runtime; this can.
"""

from __future__ import annotations

from typing import Any

import pytest


class _Spy:
    """Stands in for run_mandated / run_agent and records the kwargs it got."""

    def __init__(self, output: str = "ok") -> None:
        self.calls: list[dict[str, Any]] = []
        self.output = output

    async def __call__(self, *args: Any, **kwargs: Any) -> Any:
        self.calls.append(kwargs)
        return _Result(self.output)

    @property
    def last(self) -> dict[str, Any]:
        assert self.calls, "the helper never started an agent run"
        return self.calls[-1]


class _Result:
    def __init__(self, output: str) -> None:
        self.success = True
        self.output = output
        self.parsed = None
        self.parse_error = None
        self.error = None
        self.error_kind = None
        self.usage: dict[str, Any] = {}
        self.usage_history: list[Any] = []
        self.metadata: dict[str, Any] = {}


@pytest.mark.asyncio
async def test_web_read_summarizer_is_muted(monkeypatch: pytest.MonkeyPatch) -> None:
    """`web_read(summarize=true)` must not narrate its summary at the user."""
    from matrx_ai.tools.implementations import _summarize_helper as mod

    spy = _Spy("a summary")
    monkeypatch.setattr(mod, "run_mandated", spy)

    text, _usage = await mod.summarize_content("body text", "instructions", ctx=None)

    assert text == "a summary"
    assert spy.last.get("suppress_stream") is True


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "fn_name", ["scrape_research_condenser_agent_1", "scrape_research_condenser_agent_2"]
)
async def test_research_condensers_are_muted(monkeypatch: pytest.MonkeyPatch, fn_name: str) -> None:
    """`research_web`'s condensers must not dump their blob on the caller's wire."""
    from matrx_ai.agent_runners import research as mod

    spy = _Spy("condensed")
    monkeypatch.setattr(mod, "run_mandated", spy)
    monkeypatch.setattr(mod, "_stamp_web_research_source", lambda: None)

    result = await getattr(mod, fn_name)(
        instructions="i", scraped_content="c", queries="q", search_results="s", ctx=None
    )

    assert result.success
    assert spy.last.get("suppress_stream") is True


@pytest.mark.asyncio
async def test_pdf_content_cleaner_is_muted(monkeypatch: pytest.MonkeyPatch) -> None:
    """The cleaned PDF is machine-parsed — it is never the user's reading copy."""
    from matrx_ai.agent_runners import content_cleaner as mod

    spy = _Spy("cleaned")
    monkeypatch.setattr(mod, "run_mandated", spy)
    monkeypatch.setattr(mod, "stamp_source_context", lambda **_kw: None)

    result = await mod.clean_pdf_extracted_content("raw pdf text")

    assert result.success
    assert spy.last.get("suppress_stream") is True


@pytest.mark.asyncio
async def test_ctx_get_summary_agent_is_muted(monkeypatch: pytest.MonkeyPatch) -> None:
    """`ctx_get(mode="summary")` returns its summary in the ToolResult, not the wire."""
    import matrx_ai.agents.executor as executor_mod
    from matrx_ai.agents.definition import Agent
    from matrx_ai.tools.implementations import ctx as mod

    spy = _Spy("the summary")
    monkeypatch.setattr(executor_mod, "run_agent", spy)

    class _FakeAgent:
        def set_variable(self, *_a: Any, **_kw: Any) -> None:
            return None

    async def _from_prompt(_agent_id: str) -> Any:
        return _FakeAgent()

    monkeypatch.setattr(Agent, "from_prompt", staticmethod(_from_prompt))

    summary, error = await mod._run_summary_agent("agent-id", "content", ctx=None)

    assert error is None and summary == "the summary"
    assert spy.last.get("suppress_stream") is True
