"""The writer compacts a conversation the provider measured over its window
(daemon cost round 4, T1/T5; synthetic, shaped like strand-ai's 2026-10-12
writer at 252,709 prompt tokens: one ~250K-char opening bite, ~120 shell rounds,
a final_result per run; chars/4 alone reads it UNDER 250K).

T1 found the prod no-op was not a compaction bug: one worker had run CLI 0.219.0
since 10-09, whose window was 950K and ignored the server's header. These pin
both halves: the current window compacts this history, and a 950K window sends
it unchanged -- the shape the model route's prompt ceiling now refuses.
"""

from __future__ import annotations

import asyncio

import pytest

pytest.importorskip("pydantic_ai")
pytest.importorskip("pydantic_ai_harness")

from pydantic_ai import RunContext  # noqa: E402
from pydantic_ai.messages import (  # noqa: E402
    ModelRequest,
    ModelResponse,
    TextPart,
    ToolCallPart,
    ToolReturnPart,
    UserPromptPart,
)
from pydantic_ai.models import ModelRequestContext, ModelRequestParameters  # noqa: E402
from pydantic_ai.models.function import AgentInfo, FunctionModel  # noqa: E402
from pydantic_ai.usage import RequestUsage, RunUsage, UsageLimits  # noqa: E402
from pydantic_ai_harness.compaction import estimate_context_tokens, estimate_token_count  # noqa: E402

from probe.daemon import agent as agent_mod  # noqa: E402

ANCHOR = 252_709  # the provider's prompt_tokens on the last answer (run 591 round 1)
OLD_WINDOW = 950_000  # CONTEXT_TOKENS before 0.223.0


def _text(chars: int, tag: str) -> str:
    unit = f"{tag} lorem ipsum "
    return (unit * (chars // len(unit) + 1))[:chars]


def _history() -> list:
    """Opening bite, then 60 runs of (shell, shell, final_result); the pending
    request is the last run's shell result, so the gate reads the anchor."""
    msgs: list = [ModelRequest(parts=[UserPromptPart(_text(250_000, "opening"))], instructions=_text(31_000, "job"))]
    call = 0
    prompt_tokens = 90_000
    for run in range(60):
        if run:
            msgs.append(ModelRequest(parts=[ToolReturnPart("final_result", "Final result processed.", f"c{call}"),
                                            UserPromptPart(_text(5_000, f"bite{run}"))], instructions=_text(31_000, "job")))
        for _ in range(2):
            call += 1
            prompt_tokens += 1_350
            msgs.append(ModelResponse(parts=[ToolCallPart("shell", '{"command": "probe note append"}', f"c{call}")],
                                      usage=RequestUsage(input_tokens=prompt_tokens, output_tokens=60),
                                      model_name="gpt-6.1-sol"))
            msgs.append(ModelRequest(parts=[ToolReturnPart("shell", _text(1_200, "out"), f"c{call}")],
                                     instructions=_text(31_000, "job")))
        call += 1
        msgs.append(ModelResponse(parts=[ToolCallPart("final_result", '{"summary": "noted"}', f"c{call}")],
                                  usage=RequestUsage(input_tokens=prompt_tokens, output_tokens=50),
                                  model_name="gpt-6.1-sol"))
    msgs.pop()  # the last run is mid-way: its shell result is the pending request
    msgs[-2].usage = RequestUsage(input_tokens=ANCHOR, output_tokens=59)
    return msgs


def _before_request(state: agent_mod.RunState, messages: list):
    summaries: list[int] = []

    def summarizer(msgs, info: AgentInfo) -> ModelResponse:
        summaries.append(len(msgs))
        return ModelResponse(parts=[TextPart("SYNTHETIC SUMMARY")])

    model = FunctionModel(summarizer, model_name="gpt-6.1-sol")
    ctx = RunContext(deps=None, model=model, usage=RunUsage(), usage_limits=UsageLimits(request_limit=None))
    rc = ModelRequestContext(model=model, messages=list(messages), model_settings=None,
                             model_request_parameters=ModelRequestParameters())
    out = asyncio.run(agent_mod.counted_compaction(state).before_model_request(ctx, rc))
    return out.messages, summaries


def test_the_history_is_over_the_window_by_the_anchor_but_not_by_the_heuristic():
    history = _history()
    assert estimate_context_tokens(history) > 250_000
    assert estimate_token_count(history) < 250_000  # chars/4 alone would not have gated


def test_main_compacts_it():
    history = _history()
    state = agent_mod.RunState(conversation=True)
    after, summaries = _before_request(state, history)
    assert state.compactions == 1 and summaries
    assert len(after) < len(history)


def test_the_pre_0_223_window_sends_it_unchanged():
    history = _history()
    state = agent_mod.RunState(conversation=True, context_tokens=OLD_WINDOW)
    after, summaries = _before_request(state, history)
    assert state.compactions == 0 and not summaries
    assert len(after) == len(history) and all(a is b for a, b in zip(after, history))
