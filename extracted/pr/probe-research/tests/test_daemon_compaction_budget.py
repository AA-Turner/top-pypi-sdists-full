"""Compaction by token budget, with room to grow (2026-10-06).

Compaction used to keep "the last 20 messages" and stop just under the size. In
conversation mode one message can be a whole bite of the session, so the kept
tail alone was over the size: a long session compacted on nearly every bite
("compacted the conversation: 22 messages -> 22" once a minute on 2026-10-05),
and each compaction rewrote the history, so the provider re-cached ~1M tokens
at the write price every time. Now it runs past the size, comes down to
COMPACT_TO of it, and keeps the newest KEEP_SHARE whole.

The model is Pydantic AI's FunctionModel reporting the harness's own token
estimate as its usage, so the provider-anchored estimate and the heuristic agree.
"""

from __future__ import annotations

import asyncio
import json

import httpx
import pytest

pytest.importorskip("pydantic_ai")
pytest.importorskip("pydantic_ai_harness")

from pydantic_ai import Agent  # noqa: E402
from pydantic_ai.messages import (  # noqa: E402
    ModelRequest,
    ModelResponse,
    TextPart,
    ToolCallPart,
    ToolReturnPart,
    UserPromptPart,
)
from pydantic_ai.models.function import AgentInfo, FunctionModel  # noqa: E402
from pydantic_ai.usage import RequestUsage  # noqa: E402
from pydantic_ai_harness.compaction import estimate_token_count  # noqa: E402

from probe.daemon import agent as agent_mod  # noqa: E402
from probe.daemon import model as model_mod  # noqa: E402
from probe.daemon import usage  # noqa: E402

SIZE = 10_000
SUMMARY = "SUMMARY: earlier turns."


def _words(tokens: int, tag: str) -> str:
    """About `tokens` tokens by the harness's 4-characters-per-token estimate."""
    unit = f"{tag} "
    return unit * (tokens * 4 // len(unit))


class Seen:
    """The model: answers a summary request with SUMMARY, anything else with
    text; keeps every main request's messages."""

    def __init__(self) -> None:
        self.main: list[list] = []
        self.summaries = 0

    def __call__(self, messages, info: AgentInfo) -> ModelResponse:
        tokens = estimate_token_count(messages)
        if _is_summary(messages):
            self.summaries += 1
            return ModelResponse(parts=[TextPart(SUMMARY)], usage=RequestUsage(input_tokens=tokens, output_tokens=5))
        self.main.append(list(messages))
        return ModelResponse(parts=[TextPart("noted")], usage=RequestUsage(input_tokens=tokens, output_tokens=1))


def _is_summary(messages) -> bool:
    last = messages[-1]
    return any(isinstance(p, UserPromptPart) and "<messages>" in str(p.content) for p in last.parts)


def _state(size: int = SIZE) -> agent_mod.RunState:
    return agent_mod.RunState(conversation=True, context_tokens=size)


def _run(seen: Seen, state: agent_mod.RunState, prompt: str, history: list) -> list:
    agent = Agent(FunctionModel(seen), capabilities=[agent_mod.counted_compaction(state)])
    result = asyncio.run(agent.run(prompt, message_history=history))
    return result.all_messages()


def _exchange(i: int, tokens: int) -> list:
    return [ModelRequest(parts=[UserPromptPart(_words(tokens, f"bite{i}"))]),
            ModelResponse(parts=[TextPart(f"ok {i}")], usage=RequestUsage(input_tokens=(i + 1) * tokens, output_tokens=1))]


def test_one_compaction_brings_the_context_to_half_and_the_next_bites_do_not_compact():
    """Twelve 1,500-token bites (18K) past a 10K size: one compaction, down to
    at most half the size, and the next bite neither compacts nor touches the
    history the provider has cached."""
    history = [m for i in range(12) for m in _exchange(i, 1_500)]
    state, seen = _state(), Seen()
    after_first = _run(seen, state, _words(200, "new1"), history)
    assert state.compactions == 1 and seen.summaries == 1
    sent = seen.main[-1]
    assert estimate_token_count(sent) <= SIZE * agent_mod.COMPACT_TO
    assert SUMMARY in json.dumps([str(getattr(p, "content", "")) for m in sent for p in m.parts])
    assert "bite0" not in str(sent), "the oldest bites were summarized away"
    assert "bite11" in str(sent), "the newest bite is kept whole"

    after_second = _run(seen, state, _words(1_500, "new2"), after_first)
    assert state.compactions == 1, "a 1,500-token bite after compacting to half does not compact again"
    second = seen.main[-1]
    assert [str(m) for m in second[: len(sent)]] == [str(m) for m in sent], "the cached prefix is unchanged"
    _run(seen, state, _words(1_500, "new3"), after_second)
    assert state.compactions == 1


def test_the_old_thrash_shape_compacts_once_not_every_bite():
    """The 2026-10-05 shape: 30 big bites, each one 10% of the size. Keeping a
    message count kept more than the size and compacted on every bite."""
    history = [m for i in range(30) for m in _exchange(i, 1_000)]
    state, seen = _state(), Seen()
    messages = history
    for n in range(4):
        messages = _run(seen, state, _words(600, f"more{n}"), messages)
    assert state.compactions == 1, f"{state.compactions} compactions over 4 bites"


def test_a_tool_call_and_its_result_stay_together():
    """The cut never leaves a tool result without its call, or a call without its
    result (Anthropic refuses either)."""
    history: list = []
    for i in range(10):
        history.append(ModelRequest(parts=[UserPromptPart(_words(300, f"ask{i}"))]))
        history.append(ModelResponse(parts=[ToolCallPart("shell", {"command": f"ls {i}"}, tool_call_id=f"c{i}")],
                                     usage=RequestUsage(input_tokens=(i + 1) * 1_500, output_tokens=1)))
        history.append(ModelRequest(parts=[ToolReturnPart("shell", _words(1_200, f"out{i}"), tool_call_id=f"c{i}")]))
        history.append(ModelResponse(parts=[TextPart(f"seen {i}")],
                                     usage=RequestUsage(input_tokens=(i + 1) * 1_500 + 1_200, output_tokens=1)))
    state, seen = _state(), Seen()
    _run(seen, state, "next", history)
    assert state.compactions == 1
    sent = seen.main[-1]
    calls = {p.tool_call_id for m in sent if isinstance(m, ModelResponse) for p in m.parts
             if isinstance(p, ToolCallPart)}
    returns = {p.tool_call_id for m in sent if isinstance(m, ModelRequest) for p in m.parts
               if isinstance(p, ToolReturnPart)}
    assert calls == returns and calls, (calls, returns)


def test_a_newest_message_bigger_than_the_kept_share_is_kept_alone():
    """One bite bigger than the kept share (2,500 tokens here): it stays, whole
    and alone, the rest is summarized, and the run ends (no loop)."""
    history = [m for i in range(6) for m in _exchange(i, 1_000)]
    giant = _words(6_000, "giant")
    state, seen = _state(), Seen()
    after = _run(seen, state, giant, history)
    assert state.compactions == 1 and seen.summaries == 1
    sent = seen.main[-1]
    assert giant in str(sent) and "bite5" not in str(sent)
    _run(seen, state, "small follow-up", after)
    assert state.compactions == 1, "summary + the giant bite + a small one fit the size"


def test_under_the_size_nothing_is_rewritten():
    history = [m for i in range(4) for m in _exchange(i, 1_000)]
    state, seen = _state(), Seen()
    _run(seen, state, "hello", history)
    assert state.compactions == 0 and seen.summaries == 0
    assert [str(m) for m in seen.main[-1][: len(history)]] == [str(m) for m in history]


# ---------------------------------------------------------------------------
# Cache writes priced as writes.
# ---------------------------------------------------------------------------


def test_sonnet_5_and_cache_writes_are_priced():
    assert usage.cost("claude-sonnet-5", input_tokens=1_000_000) == pytest.approx(2.0)
    assert usage.cost("claude-sonnet-5", input_tokens=1_000_000, cache_write_tokens=1_000_000) == pytest.approx(2.5)
    assert usage.cost("claude-sonnet-5", input_tokens=1_000_000, cache_read_tokens=1_000_000,
                      output_tokens=1_000_000) == pytest.approx(10.2)
    assert usage.cost("claude-opus-5-5", input_tokens=1_000_000, cache_read_tokens=100_000,
                      cache_write_tokens=800_000) == pytest.approx(0.1 * 0.20 + 0.8 * 5.0 + 0.1 * 4.0)


def _served(usage_body: dict):
    """One answer from the daemon's own model (`model.build`) against a fake
    `/v1/companion/chat/completions` returning `usage_body`."""

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path.endswith("/v1/companion/chat/completions")
        return httpx.Response(200, json={
            "id": "chatcmpl-1", "object": "chat.completion", "created": 1, "model": "claude-opus-5-5",
            "choices": [{"index": 0, "message": {"role": "assistant", "content": "ok"}, "finish_reason": "stop"}],
            "usage": usage_body})

    async def go():
        client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
        old, model_mod._HTTP_CLIENT = model_mod._HTTP_CLIENT, client
        try:
            model = model_mod.build(model_mod.Endpoint("http://probe.test", "k"))
            result = await Agent(model).run("hi")
            return result.all_messages()[-1]
        finally:
            model_mod._HTTP_CLIENT = old
            await client.aclose()

    return asyncio.run(go())


def test_a_server_that_reports_cache_writes_gets_them_priced_as_writes():
    """The route reports Anthropic's cache writes as
    `prompt_tokens_details.cache_write_tokens`; Pydantic AI reads that name into
    `cache_write_tokens`, priced at $5/MTok on Opus 5.5, not as $4 input."""
    response = _served({"prompt_tokens": 1_000_000, "completion_tokens": 0, "total_tokens": 1_000_000,
                        "prompt_tokens_details": {"cached_tokens": 200_000, "cache_write_tokens": 800_000}})
    assert response.usage.cache_write_tokens == 800_000 and response.usage.cache_read_tokens == 200_000
    assert usage.response_cost(response) == pytest.approx(0.8 * 5.0 + 0.2 * 0.20)


def test_an_older_server_without_the_field_prices_as_before():
    response = _served({"prompt_tokens": 1_000_000, "completion_tokens": 0, "total_tokens": 1_000_000,
                        "prompt_tokens_details": {"cached_tokens": 200_000}})
    assert response.usage.cache_write_tokens == 0
    assert usage.response_cost(response) == pytest.approx(0.8 * 4.0 + 0.2 * 0.20)


@pytest.mark.parametrize("size", [0, -5])
def test_a_size_of_zero_or_below_is_refused_so_the_worker_runs_as_bites(monkeypatch, size):
    """`PROBE_DAEMON_CONTEXT_TOKENS=0` must not compact before every request: it
    is refused, and the worker's probe falls back to bites."""
    from probe.daemon import agent as agent_mod
    from probe.daemon import worker as worker_mod

    monkeypatch.setattr(agent_mod, "CONTEXT_TOKENS", size)
    with pytest.raises(ValueError):
        agent_mod.counted_compaction(agent_mod.RunState(conversation=True))
    assert worker_mod._compaction_available() is False



def test_the_writer_compacts_at_250k_and_the_reader_at_120k_by_default():
    """The writer's size is 250K (Richard, 2026-10-07; it was 950K): every round
    re-reads the whole context. Read in a fresh interpreter with the overrides
    unset, so a test that patched the module cannot pass it."""
    import os
    import subprocess
    import sys

    env = {k: v for k, v in os.environ.items()
           if k not in ("PROBE_DAEMON_CONTEXT_TOKENS", "PROBE_READER_CONTEXT_TOKENS")}
    out = subprocess.run([sys.executable, "-c", "from probe.daemon import agent as a; "
                          "print(a.CONTEXT_TOKENS, a.READ_CONTEXT_TOKENS)"],
                         env=env, capture_output=True, text=True, check=True).stdout.split()
    assert out == ["250000", "120000"]
