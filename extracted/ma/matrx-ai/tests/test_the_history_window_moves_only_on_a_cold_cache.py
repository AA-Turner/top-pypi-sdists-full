"""🚨 EVERY CONVERSATION GETS THE HISTORY WINDOW, AND A WARM PREFIX NEVER MOVES — adversarial 2026-10-30 A2 + B2.

Two rulings at once. Arman, D3: "Every conversation" gets the history window. His cache law: nothing except the
removal of LARGE tool outputs may change text behind the cache line. Both hold because the window is a declared
stage of the send boundary (``send_boundary._apply_history_window``) whose cut MOVES only when the provider cache
is already cold (the trim gate's own warm/cold test, ``context_trim._is_cache_likely_alive``); while warm the
recorded cut is replayed byte for byte, and every moved cut is recorded on the request.

RED before: the window ran in ``ConversationResolver._finish`` and slid one turn off the FRONT on every turn past
the limit — a 50-turn conversation's prefix changed every turn, unannounced.

Through the REAL ``prepare_for_send`` (resolve stage) with a host door installed in ``_ext``.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

from matrx_ai import _ext
from matrx_ai.config import TextContent, ToolResultContent, UnifiedMessage
from matrx_ai.config import send_boundary
from matrx_ai.config.history_budget import HistoryWindowPolicy, HistoryWindowUnavailable
from matrx_ai.config.send_boundary import HISTORY_CUT_KEY, STAGE_RESOLVE, prepare_for_send

CONVERSATION = "c0ffee00-0000-4000-8000-000000000050"
WINDOW = 10


def _turn(i: int) -> list[UnifiedMessage]:
    return [
        UnifiedMessage(role="user", id=f"u{i}", position=3 * i, content=[TextContent(text=f"question {i}")]),
        UnifiedMessage(
            role="tool",
            id=f"t{i}",
            position=3 * i + 1,
            content=[ToolResultContent(tool_use_id=f"call{i}", name="fs_read", content="x" * 40, output_chars=40)],
        ),
        UnifiedMessage(role="assistant", id=f"a{i}", position=3 * i + 2, content=[TextContent(text=f"answer {i}")]),
    ]


def _history(turns: int) -> list[UnifiedMessage]:
    return [m for i in range(1, turns + 1) for m in _turn(i)]


def _wire(messages: list) -> list[str]:
    out = []
    for m in messages:
        block = m.content[0]
        out.append(f"{m.role}:{getattr(block, 'text', None) or getattr(block, 'content', None)}")
    return out


def _state(*, warm: bool, cut: dict | None) -> dict:
    age = timedelta(seconds=10) if warm else timedelta(hours=2)
    state = {"last_response_at": (datetime.now(UTC) - age).isoformat(), "est_cache_ttl_secs": 300, "last_provider": "anthropic"}
    if cut is not None:
        state[HISTORY_CUT_KEY] = cut
    return state


@pytest.fixture
def door(monkeypatch):
    policy = {"value": HistoryWindowPolicy(turns=WINDOW, token_budget=None, waits_for_cold_cache=True)}
    calls: list = []

    async def window(*, conversation_id: str, structure_is_live: bool):
        calls.append(conversation_id)
        return policy["value"]

    monkeypatch.setitem(_ext._registry, "conversation_history_window", window)
    monkeypatch.setattr(send_boundary, "_CACHE_STATE_MEMO", type(send_boundary._CACHE_STATE_MEMO)())
    monkeypatch.setattr(send_boundary, "_HISTORY_CUT_MEMO", type(send_boundary._HISTORY_CUT_MEMO)())
    token = set_app_context(AppContext(emitter=None, user_id="u", organization_id="o", conversation_id=CONVERSATION))
    yield policy
    clear_app_context(token)


async def _send(turns: int, *, warm: bool, cut: dict | None) -> tuple[list[str], dict]:
    """One turn: ``turns`` persisted turns, then this turn's question, through the real resolve stage."""
    persisted = _history(turns)
    config = SimpleNamespace(
        messages=[*persisted, UnifiedMessage(role="user", content=[TextContent(text=f"question {turns + 1}")])],
        system_instruction=None,
        prompt_cache_key=None,
    )
    await prepare_for_send(
        config,
        stage=STAGE_RESOLVE,
        conversation_id=CONVERSATION,
        cache_state=_state(warm=warm, cut=cut),
        history_len=len(persisted),
    )
    from matrx_connect.context.app_context import get_app_context

    decision = dict(get_app_context().metadata.get("history_cut") or {})
    return _wire(config.messages), decision


def _persisted_cut() -> dict | None:
    """What persistence writes into ``cache_state`` after the turn (``persistence._refresh_cache_state``)."""
    return send_boundary.remembered_history_cut(CONVERSATION)


@pytest.mark.asyncio
async def test_a_warm_fifty_turn_conversation_keeps_an_identical_prefix(door) -> None:
    # Turn 31 arrives on a cold cache: the window cuts to the last 10 turns (a recorded break).
    sent, decision = await _send(30, warm=False, cut=None)
    assert decision["action"] == "moved" and decision["cache_break"] is True
    assert sent[0] == "user:question 21"
    cut = _persisted_cut()
    assert cut and cut["first_id"] == "u21"

    # Turns 32..50 arrive while the cache is warm: the cut never moves, every send extends the last one.
    previous = sent
    for turns in range(31, 50):
        sent, decision = await _send(turns, warm=True, cut=cut)
        assert decision["action"] == "held_warm" and decision["cache_break"] is False
        assert sent[: len(previous)] == previous, f"turn {turns + 1}: the cached prefix changed while warm"
        previous = sent
    assert sent[0] == "user:question 21", "the warm cut drifted"


@pytest.mark.asyncio
async def test_a_cold_conversation_gets_the_window(door) -> None:
    sent, _ = await _send(30, warm=False, cut=None)
    cut = _persisted_cut()
    sent, _ = await _send(45, warm=True, cut=cut)
    assert sent[0] == "user:question 21" and len(sent) == 3 * 25 + 1

    # The person comes back after the cache expired: the cut moves to the last 10 turns, recorded as a break.
    sent, decision = await _send(45, warm=False, cut=cut)
    assert sent[0] == "user:question 36"
    assert len(sent) == 3 * WINDOW + 1
    assert decision["action"] == "moved" and decision["cache_break"] is True
    assert decision["reason"] == "the provider cache is cold"
    assert _persisted_cut()["first_id"] == "u36"


@pytest.mark.asyncio
async def test_the_cold_cache_gate_is_a_knob(door) -> None:
    """Off: the cut moves whenever it must, even warm — still recorded as a cache break."""
    door["value"] = HistoryWindowPolicy(turns=WINDOW, waits_for_cold_cache=False)
    sent, _ = await _send(30, warm=False, cut=None)
    sent, decision = await _send(31, warm=True, cut=_persisted_cut())
    assert sent[0] == "user:question 22"
    assert decision["action"] == "moved" and decision["cache_break"] is True


@pytest.mark.asyncio
async def test_a_warm_replay_clears_the_same_tool_results(door) -> None:
    """The token budget's clearing is part of the cut: replayed while warm, so the prefix is rebuilt exactly."""
    door["value"] = HistoryWindowPolicy(turns=WINDOW, token_budget=60, waits_for_cold_cache=True)
    first, _ = await _send(12, warm=False, cut=None)
    cut = _persisted_cut()
    assert cut["cleared"], "the budget cleared nothing"
    again, decision = await _send(13, warm=True, cut=cut)
    assert decision["action"] == "held_warm"
    assert again[: len(first)] == first


@pytest.mark.asyncio
async def test_a_window_the_host_cannot_decide_fails_the_turn(monkeypatch, door) -> None:
    async def broken(**_k):
        raise RuntimeError("platform.feature_knob is unreachable")

    monkeypatch.setitem(_ext._registry, "conversation_history_window", broken)
    with pytest.raises(HistoryWindowUnavailable, match="unreachable"):
        await _send(30, warm=False, cut=None)


def test_the_window_is_a_send_boundary_stage_not_a_resolver_step() -> None:
    from matrx_utils.source_guard import stable_source

    from matrx_ai.agents.resolver import ConversationResolver

    assert "get_conversation_history_window" not in stable_source(ConversationResolver._finish)
    assert "_apply_history_window" in stable_source(prepare_for_send)
