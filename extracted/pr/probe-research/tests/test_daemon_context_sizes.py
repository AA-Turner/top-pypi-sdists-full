"""The server can lower the daemon's context sizes (~/plans/daemon-cost-round3,
task 16, Richard 2026-10-07: "server-pushed cap"): every chat answer carries
`x-probe-context-tokens` (writer) and `x-probe-read-context-tokens` (reader); a
client takes the lower of its own size and the server's from its next request."""

from __future__ import annotations

import pytest

pytest.importorskip("pydantic_ai")  # the daemon extra: absent on the SDK-only CI shard

from probe.daemon import agent as agent_mod  # noqa: E402
from probe.daemon import model as model_mod  # noqa: E402


@pytest.fixture(autouse=True)
def _fresh(monkeypatch):
    monkeypatch.setattr(model_mod, "_SERVER_CONTEXT_TOKENS", {})


def test_before_any_answer_the_clients_own_sizes_stand():
    assert agent_mod.writer_context_tokens() == agent_mod.CONTEXT_TOKENS
    assert agent_mod.read_context_tokens() == agent_mod.READ_CONTEXT_TOKENS


def test_a_lower_server_size_wins_and_a_higher_one_does_not(monkeypatch):
    monkeypatch.setattr(agent_mod, "CONTEXT_TOKENS", 250_000)
    monkeypatch.setattr(agent_mod, "READ_CONTEXT_TOKENS", 120_000)
    model_mod.remember_context_sizes({"x-probe-context-tokens": "200000", "x-probe-read-context-tokens": "500000"})
    assert agent_mod.writer_context_tokens() == 200_000
    assert agent_mod.read_context_tokens() == 120_000, "a server size only lowers"


@pytest.mark.parametrize("raw", ["", "lots", "1000", "99999", "-5", None])
def test_a_missing_malformed_or_tiny_server_size_is_ignored(raw):
    model_mod.remember_context_sizes({"x-probe-context-tokens": "180000"})
    model_mod.remember_context_sizes({} if raw is None else {"x-probe-context-tokens": raw})
    assert model_mod.server_context_tokens(model_mod.LANE_WRITE) == 180_000, "the last good value stays"


def test_the_writers_compaction_uses_the_lowered_size(monkeypatch):
    monkeypatch.setattr(agent_mod, "CONTEXT_TOKENS", 250_000)
    model_mod.remember_context_sizes({"x-probe-context-tokens": "100000"})
    pytest.importorskip("pydantic_ai_harness")
    compaction = agent_mod.counted_compaction(agent_mod.RunState(conversation=True))
    assert compaction.target_tokens == int(100_000 * agent_mod.COMPACT_TO)


def test_only_chat_answers_carry_sizes():
    """The response hook reads sizes from chat answers only (the same path check
    as the served-model header)."""
    import asyncio

    class _Req:
        class url:  # noqa: N801
            path = "/v1/companion/traces"

    class _Resp:
        request = _Req
        headers = {"x-probe-context-tokens": "100000"}

    asyncio.run(model_mod._remember_served_model(_Resp))
    assert model_mod.server_context_tokens(model_mod.LANE_WRITE) is None
    _Req.url.path = "/v1/companion/chat/completions"
    asyncio.run(model_mod._remember_served_model(_Resp))
    assert model_mod.server_context_tokens(model_mod.LANE_WRITE) == 100_000
