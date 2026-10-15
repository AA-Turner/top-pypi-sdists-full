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


def _small_exchanges(n: int) -> list:
    """`n` exchanges of a few tokens each: 2n messages, far under SIZE."""
    out: list = []
    for i in range(n):
        out.append(ModelRequest(parts=[UserPromptPart(f"b{i} ok")]))
        out.append(ModelResponse(parts=[TextPart(f"r{i}")], usage=RequestUsage(input_tokens=(i + 1) * 4, output_tokens=1)))
    return out


def _wire(messages: list) -> int:
    """The chat messages `messages` really become on the OpenAI-compatible model
    route (Pydantic AI's own mapping), which is what the server's cap counts."""
    from pydantic_ai.models import ModelRequestParameters
    from pydantic_ai.models.openai import OpenAIChatModel
    from pydantic_ai.providers.openai import OpenAIProvider

    model = OpenAIChatModel("x", provider=OpenAIProvider(api_key="x"))
    return len(asyncio.run(model._map_messages(messages, ModelRequestParameters())))


def test_a_history_of_many_small_messages_compacts_by_count():
    """strand-ai 2026-10-11: 2,003 small messages at 245K tokens, under the 250K
    size, and the model route refused the call (at most 2,000). Past
    COMPACT_MESSAGES the history is summarized whatever its size, the tail
    keeps at most KEEP_MESSAGES, and the next bites do not compact again."""
    history = _small_exchanges(agent_mod.COMPACT_MESSAGES // 2 + 50)
    assert estimate_token_count(history) < SIZE * agent_mod.COMPACT_TO, "under the token target: only the count trips"
    state, seen = _state(), Seen()
    after = _run(seen, state, "next", history)
    assert state.compactions == 1 and seen.summaries == 1
    sent = seen.main[-1]
    assert _wire(sent) <= agent_mod.KEEP_MESSAGES + 3, _wire(sent)
    assert SUMMARY in str(sent) and "b0 ok" not in str(sent)
    assert f"b{len(history) // 2 - 1} ok" in str(sent), "the newest exchange is kept whole"
    for n in range(5):
        after = _run(seen, state, f"more{n}", after)
    assert state.compactions == 1, f"{state.compactions} compactions: the kept tail tripped the count again"


def test_more_messages_than_the_model_route_takes_never_go_out():
    """Whatever the history, no request leaves with more chat messages than the
    server's 2,000; the count compaction runs before that, with room."""
    history = _small_exchanges(1_200)
    state, seen = _state(), Seen()
    _run(seen, state, "next", history)
    assert max(_wire(m) for m in seen.main) <= agent_mod.COMPACT_MESSAGES


def test_parallel_tool_rounds_are_counted_as_the_route_counts_them():
    """Each tool result is its own chat message on the route: 500 rounds of three
    parallel reads are 1,001 Pydantic AI messages but 2,001 on the wire. The
    count is the wire's, so this compacts; counting Pydantic AI's messages would
    send all 2,001 and get the 400."""
    history: list = [ModelRequest(parts=[UserPromptPart("bite")])]
    for r in range(500):
        history.append(ModelResponse(parts=[ToolCallPart("read", {"path": f"{r}-{i}"}, tool_call_id=f"c{r}-{i}")
                                            for i in range(3)], usage=RequestUsage(input_tokens=(r + 1) * 8)))
        history.append(ModelRequest(parts=[ToolReturnPart("read", "ok", tool_call_id=f"c{r}-{i}") for i in range(3)]))
    assert len(history) < agent_mod.COMPACT_MESSAGES < _wire(history)
    assert agent_mod.wire_messages(history) == _wire(history)
    state, seen = _state(), Seen()
    _run(seen, state, "next", history)
    assert state.compactions == 1
    sent = seen.main[-1]
    assert agent_mod.wire_messages(sent) == _wire(sent) <= agent_mod.KEEP_MESSAGES + 3, _wire(sent)


def test_past_the_size_and_the_count_a_cleared_history_is_still_summarized():
    """Tool output puts 2,000 messages over the size, and clearing old tool
    results alone reaches the token target; the count must still be summarized
    away (the writer's shape: it runs `shell`)."""
    size, history = 120_000, []
    for i in range(500):
        history.append(ModelRequest(parts=[UserPromptPart(f"a{i}")]))
        history.append(ModelResponse(parts=[ToolCallPart("shell", {"command": f"ls {i}"}, tool_call_id=f"c{i}")],
                                     usage=RequestUsage(input_tokens=(i + 1) * 260, output_tokens=1)))
        history.append(ModelRequest(parts=[ToolReturnPart("shell", _words(260, f"o{i}"), tool_call_id=f"c{i}")]))
        history.append(ModelResponse(parts=[TextPart(f"s{i}")],
                                     usage=RequestUsage(input_tokens=(i + 1) * 262, output_tokens=1)))
    state, seen = _state(size), Seen()
    _run(seen, state, "next", history)
    assert max(_wire(m) for m in seen.main) <= agent_mod.COMPACT_MESSAGES
    assert seen.summaries == 1 and state.compactions == 1


def test_the_count_stays_under_the_servers_message_cap():
    """COMPACT_MESSAGES is the client's half of the server's MAX_CHAT_MESSAGES
    (the model route's 400). Read from the server's source when this is the
    monorepo (the public agent mirror has no server)."""
    import re
    from pathlib import Path

    router = Path(__file__).resolve().parents[2] / "app" / "companion" / "chat_router.py"
    if not router.is_file():
        pytest.skip("no server source beside the agent")
    cap = int(re.search(r"^MAX_CHAT_MESSAGES = ([\d_]+)", router.read_text(), re.M).group(1).replace("_", ""))
    assert agent_mod.COMPACT_MESSAGES + 100 <= cap
    assert agent_mod.KEEP_MESSAGES * 2 <= agent_mod.COMPACT_MESSAGES, "room between compactions"


def test_many_messages_with_a_tail_heavier_than_the_kept_share_cut_by_tokens():
    """More messages than KEEP_MESSAGES whose newest KEEP_MESSAGES outweigh the
    kept share: the token cut wins and keeps fewer."""
    history = [m for i in range(300) for m in _exchange(i, 50)]
    assert len(history) > agent_mod.KEEP_MESSAGES
    assert estimate_token_count(history[-agent_mod.KEEP_MESSAGES:]) > SIZE * agent_mod.KEEP_SHARE
    state, seen = _state(), Seen()
    _run(seen, state, "next", history)
    sent = seen.main[-1]
    assert state.compactions == 1
    assert len(sent) < agent_mod.KEEP_MESSAGES
    assert estimate_token_count(sent) <= SIZE * agent_mod.COMPACT_TO


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



def test_the_writer_compacts_at_250k_and_the_reader_starts_fresh_at_120k_by_default():
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


# ---------------------------------------------------------------------------
# The tail compaction leaves: tool results whose calls were summarized away.
# ---------------------------------------------------------------------------


def test_a_tail_opening_with_retries_for_summarized_calls_still_has_a_user_turn_first():
    """The harness's cut pairs a call with its ToolReturnPart but not with a
    RetryPromptPart, so it can land right after a round whose calls all failed
    validation. Those retries answer nothing that is left: they are dropped and
    EARLIER_TURNS goes before the model's next message, so what goes out is
    system, user, assistant -- never the model's tool call straight after the
    system messages (Gemini refuses that)."""
    from pydantic_ai.messages import RetryPromptPart, SystemPromptPart

    summary = ModelRequest(parts=[SystemPromptPart("SUMMARY")])
    retries = ModelRequest(parts=[RetryPromptPart("bad args", tool_name="read", tool_call_id=f"gone{i}")
                                  for i in range(2)])
    call = ModelResponse(parts=[ToolCallPart("read", {"path": "x"}, tool_call_id="c1")])
    result = ModelRequest(parts=[ToolReturnPart("read", "ok", tool_call_id="c1")])
    fixed = agent_mod.user_turn_first([summary, retries, call, result])
    assert fixed[0] is summary and fixed[2:] == [call, result]
    assert fixed[1].parts[0].content == agent_mod.EARLIER_TURNS

    from pydantic_ai.models import ModelRequestParameters
    from pydantic_ai.models.openai import OpenAIChatModel
    from pydantic_ai.providers.openai import OpenAIProvider

    sent = asyncio.run(OpenAIChatModel("x", provider=OpenAIProvider(api_key="x"))
                       ._map_messages(fixed, ModelRequestParameters()))
    assert [m["role"] for m in sent] == ["system", "user", "assistant", "tool"]


def test_a_tail_of_nothing_but_orphaned_results_still_ends_in_a_user_turn():
    from pydantic_ai.messages import RetryPromptPart, SystemPromptPart

    summary = ModelRequest(parts=[SystemPromptPart("SUMMARY")])
    retries = ModelRequest(parts=[RetryPromptPart("truncated JSON", tool_name="shell", tool_call_id="gone")])
    fixed = agent_mod.user_turn_first([summary, retries])
    assert fixed[0] is summary and len(fixed) == 2
    assert fixed[1].parts[0].content == agent_mod.EARLIER_TURNS


def test_a_history_that_needs_no_fixing_is_returned_as_it_is():
    from pydantic_ai.messages import SystemPromptPart

    history = [ModelRequest(parts=[SystemPromptPart("S")]), ModelRequest(parts=[UserPromptPart("hi")]),
               ModelResponse(parts=[TextPart("ok")])]
    assert agent_mod.user_turn_first(history) is history
