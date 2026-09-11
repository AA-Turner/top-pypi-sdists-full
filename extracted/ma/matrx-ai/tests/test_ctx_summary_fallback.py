"""context mode=summary must never hard-fail — and must never fall back SILENTLY.

Resolution order (ctx.py ``_ctx_get_body``):
  1. AI summary when summary_agent_id is set
  2. source-backed: precomputed descriptor.summary
  3. otherwise the first page, ANNOUNCED with fell_back_from="summary" + a note
     naming the remedy (both for inline objects and for lazy source-backed ones)

The LLM is the only external dependency: ``Agent.from_prompt`` and
``run_agent`` are replaced; ``_run_summary_agent`` (owned by ctx.py) runs for
real so its routing — content handed to the agent, stream suppression,
failure mapping — is under test.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from unittest.mock import MagicMock, patch

from matrx_ai.agents import executor as agent_executor
from matrx_ai.agents.definition import Agent
from matrx_ai.agents.executor import AgentRunResult
from matrx_ai.tools.implementations.ctx import ctx_get
from matrx_ai.tools.models import ToolContext


def _ctx() -> ToolContext:
    return ToolContext(
        call_id="call_test",
        user_id="user_test",
        conversation_id="conv_test",
        emitter=None,
    )


def _manifest(obj: Any) -> MagicMock:
    m = MagicMock()
    m.get.return_value = obj
    m.all.return_value = [obj]
    return m


def _inline_obj(key: str, content: str, summary_agent_id: str | None) -> SimpleNamespace:
    return SimpleNamespace(
        key=key,
        type=SimpleNamespace(value="text"),
        label=key.title(),
        summary_agent_id=summary_agent_id,
        descriptor=None,
        source=None,
        is_lazy_source=lambda: False,
        content_as_str=lambda: content,
    )


class _FakeSummaryAgent:
    """Stands in for the LLM agent; records what the SUT handed it."""

    def __init__(self, prompt_id: str) -> None:
        self.prompt_id = prompt_id
        self.variables: dict[str, Any] = {}

    def set_variable(self, name: str, value: Any) -> _FakeSummaryAgent:
        self.variables[name] = value
        return self


class _LLM:
    """Replaces Agent.from_prompt + run_agent. The summary it returns is a
    function of the content the SUT actually routed to the agent, so the
    expected literal is reachable only when ctx.py passes the object's body."""

    def __init__(self, *, fail_with: str | None = None, raise_on_load: Exception | None = None):
        self.fail_with = fail_with
        self.raise_on_load = raise_on_load
        self.agents: list[_FakeSummaryAgent] = []
        self.run_kwargs: list[dict[str, Any]] = []

    async def from_prompt(self, prompt_id: str, *_a: Any, **_kw: Any) -> _FakeSummaryAgent:
        if self.raise_on_load is not None:
            raise self.raise_on_load
        agent = _FakeSummaryAgent(prompt_id)
        self.agents.append(agent)
        return agent

    async def run_agent(self, agent: _FakeSummaryAgent, **kwargs: Any) -> AgentRunResult:
        self.run_kwargs.append(kwargs)
        if self.fail_with is not None:
            return AgentRunResult(success=False, error=self.fail_with)
        body = agent.variables.get("content", "")
        return AgentRunResult(success=True, output=f"{agent.prompt_id} read {len(body)} chars")


async def _get(obj: Any, args: dict[str, Any], llm: _LLM | None = None, **ext: Any) -> Any:
    def _get_ext(name: str) -> Any:
        if name == "load_manifest_from_ctx":
            return lambda _app: _manifest(obj)
        return ext[name]

    with (
        patch("matrx_ai.context.app_context.get_app_context", return_value=MagicMock(user_id="u")),
        patch("matrx_ai._ext.get_ext", side_effect=_get_ext),
        patch("matrx_ai._ext.has_ext", side_effect=lambda name: name in ext),
    ):
        if llm is None:
            return await ctx_get(args, _ctx())
        with (
            patch.object(Agent, "from_prompt", llm.from_prompt),
            patch.object(agent_executor, "run_agent", llm.run_agent),
        ):
            return await ctx_get(args, _ctx())


# --------------------------------------------------------------------------
# 2. descriptor
# --------------------------------------------------------------------------


async def test_summary_on_lazy_source_returns_descriptor() -> None:
    # Break caught: skipping the descriptor branch (falls through to materialize).
    desc = SimpleNamespace(
        summary="DOC: 12 pages · clean text · sections: Intro, Methods",
        primary_size_chars=48000,
    )
    obj = SimpleNamespace(
        key="attached_document_abc",
        type=SimpleNamespace(value="json"),
        label="Report.pdf",
        summary_agent_id=None,
        descriptor=desc,
        source=SimpleNamespace(kind="processed_document", id="pd-1"),
        is_lazy_source=lambda: True,
        content_as_str=lambda: "",
    )
    result = await _get(obj, {"key": "attached_document_abc", "mode": "summary"})

    assert result.success is True
    assert result.output.summary_kind == "descriptor"
    assert result.output.summary == "DOC: 12 pages · clean text · sections: Intro, Methods"
    assert result.output.total_chars == 48000
    assert result.output.fell_back_from is None


# --------------------------------------------------------------------------
# 3. first-page fallback — must announce itself, with the remedy
# --------------------------------------------------------------------------


async def test_inline_summary_without_agent_falls_back_to_first_page_and_announces_it() -> None:
    # Breaks caught: dropping fell_back_from, dropping the remedy note, wrong slice.
    content = "A" * 4000 + "B" * 5000
    obj = _inline_obj("notes", content, summary_agent_id=None)
    result = await _get(obj, {"key": "notes", "mode": "summary"})

    assert result.success is True
    assert result.output.mode == "page"
    assert result.output.fell_back_from == "summary"
    assert result.output.content == "A" * 4000
    assert result.output.has_more is True
    assert result.output.next_offset == 4000
    # The announcement names the remedy (the knob that would give a real summary).
    assert result.output.note is not None
    assert "summary_agent_id" in result.output.note


async def test_lazy_source_summary_without_descriptor_falls_back_and_announces_it() -> None:
    # Breaks caught: the lazy branch's fell_back_from stamp removed, or keyed on
    # the reassigned local ``mode`` (always "page" by then) instead of the request.
    obj = SimpleNamespace(
        key="attached_document_pd-2",
        type=SimpleNamespace(value="text"),
        label="Scan.pdf",
        summary_agent_id=None,
        descriptor=None,
        source=SimpleNamespace(kind="file", id="file-2"),
        is_lazy_source=lambda: True,
        content_as_str=lambda: "",
    )
    calls: list[dict[str, Any]] = []

    async def materialize(source: Any, **kwargs: Any) -> Any:
        calls.append({"source_id": source.id, **kwargs})
        return SimpleNamespace(
            representation="clean_text",
            text="Page one of the scan.",
            offset=0,
            total_chars=90210,
            has_more=True,
            next_offset=21,
            page_range=None,
        )

    result = await _get(
        obj,
        {"key": "attached_document_pd-2", "mode": "summary"},
        materialize_context_source=materialize,
    )

    assert result.success is True
    assert calls == [
        {"source_id": "file-2", "mode": "page", "offset": 0, "chars": 4000, "user_id": "u"}
    ]
    assert result.output.content == "Page one of the scan."
    assert result.output.mode == "page"
    assert result.output.fell_back_from == "summary"
    assert result.output.note is not None and "first page" in result.output.note


# --------------------------------------------------------------------------
# 1. AI summary — routed through the real _run_summary_agent
# --------------------------------------------------------------------------


async def test_summary_agent_receives_the_object_body_and_its_output_is_the_summary() -> None:
    # Breaks caught: content not handed to the agent, wrong agent id, wrong
    # summary_kind, summary text not taken from the agent result.
    llm = _LLM()
    obj = _inline_obj("big_doc", "long content here", summary_agent_id="agent-summary-1")
    result = await _get(obj, {"key": "big_doc", "mode": "summary"}, llm)

    assert result.success is True
    assert result.output.summary_kind == "agent"
    assert result.output.summary == "agent-summary-1 read 17 chars"
    assert result.output.fell_back_from is None


async def test_summary_agent_runs_with_its_stream_suppressed() -> None:
    # Break caught: suppress_stream=False leaks the nested summary tokens into
    # the calling agent's user-facing stream.
    llm = _LLM()
    obj = _inline_obj("big_doc", "long content here", summary_agent_id="agent-summary-1")
    await _get(obj, {"key": "big_doc", "mode": "summary"}, llm)

    assert len(llm.run_kwargs) == 1
    assert llm.run_kwargs[0]["suppress_stream"] is True
    assert llm.run_kwargs[0]["source_feature"] == "context_summary"


async def test_unsuccessful_summary_agent_run_is_a_failed_tool_call() -> None:
    """Guard for the 2026-09-08 class: a failed summary-agent run must be
    ``ToolResult(success=False)`` naming the cause — never a success whose
    summary is empty or an apology string."""
    llm = _LLM(fail_with="provider overloaded (529)")
    obj = _inline_obj("big_doc", "long content here", summary_agent_id="agent-summary-1")
    result = await _get(obj, {"key": "big_doc", "mode": "summary"}, llm)

    assert result.success is False
    assert result.output is None
    assert result.error.error_type == "execution"
    assert "provider overloaded (529)" in result.error.message
    assert result.error.is_retryable is True


async def test_summary_agent_that_cannot_load_is_a_failed_tool_call() -> None:
    llm = _LLM(raise_on_load=LookupError("agent-summary-1 has no active version"))
    obj = _inline_obj("big_doc", "long content here", summary_agent_id="agent-summary-1")
    result = await _get(obj, {"key": "big_doc", "mode": "summary"}, llm)

    assert result.success is False
    assert result.output is None
    assert "agent-summary-1 has no active version" in result.error.message
    assert llm.run_kwargs == []
