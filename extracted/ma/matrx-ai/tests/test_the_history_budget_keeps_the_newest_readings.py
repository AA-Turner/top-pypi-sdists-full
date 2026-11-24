"""🚨 THE HISTORY BUDGET NEVER BLINDS AN AGENT TO WHAT IT JUST READ — conversation bf84b149, 2026-11-13.

The Matrx Browser Agent ran 134 browser calls (user_request f2b7b064). On the next turn, 21 minutes later, the
provider cache was cold, so the history window moved and its token budget (``chat.history``
``held_history_token_budget`` = 12,000) cleared 40 tool results — call 1 through call 132 of 134, every result
over ~500 characters, the latest page and form state included (``chat.request`` of user_request afdc193f:
``history_cut.cleared_now = 40``; ``chat.conversation.cache_state.history_cut.cleared``). The prompt was ~86,000
tokens against a 1,000,000 window and a 200,000 host budget. The agent then reported "earlier tool results were
stripped out of my context". Nothing protected the newest readings, and nothing protected the turn in flight: a
browser run re-resolves on every client tool round trip, so a run that pauses past the cache TTL would have had
its OWN results cleared mid-run.

Through the REAL ``prepare_for_send`` (resolve stage) with a host window door installed in ``_ext``:

* a new turn after a browser run keeps the newest ``keep_recent_tool_results`` readings (the host's knob,
  ``chat.history.history_keep_recent_tool_results``) and still clears the older ones;
* a run resumed mid-turn on a cold cache keeps every result of the turn in flight.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest
from matrx_connect.context.app_context import (
    AppContext,
    clear_app_context,
    get_app_context,
    set_app_context,
)

from matrx_ai import _ext
from matrx_ai.config import (
    TextContent,
    ToolCallContent,
    ToolResultContent,
    UnifiedMessage,
    send_boundary,
)
from matrx_ai.config.history_budget import HistoryWindowPolicy, trim_history_to_token_budget
from matrx_ai.config.send_boundary import STAGE_RESOLVE, prepare_for_send

CONVERSATION = "c0ffee00-0000-4000-8000-0000000bf84b"
CALLS = 30
READING = 1500  # chars of one read_page result — under the context trim's tiers, so only the window acts


def _reading(i: int) -> str:
    return f"page state {i}: " + "r" * READING


def _browser_run() -> list[UnifiedMessage]:
    """One person turn answered by ``CALLS`` browser reads, then the run's final answer."""
    out = [UnifiedMessage(role="user", id="u0", position=0, content=[TextContent(text="add these DNS records")])]
    for i in range(CALLS):
        out.append(
            UnifiedMessage(
                role="assistant",
                id=f"a{i}",
                position=2 * i + 1,
                content=[ToolCallContent(id=f"call{i}", name="read_page", arguments={"filter": "interactive"})],
            )
        )
        out.append(
            UnifiedMessage(
                role="tool",
                id=f"t{i}",
                position=2 * i + 2,
                content=[
                    ToolResultContent(tool_use_id=f"call{i}", name="read_page", content=_reading(i), output_chars=READING)
                ],
            )
        )
    return out


def _results(messages: list) -> dict[str, str]:
    return {
        b.tool_use_id: b.content
        for m in messages
        for b in m.content
        if getattr(b, "type", None) == "tool_result"
    }


def _cold_state() -> dict:
    return {
        "last_response_at": (datetime.now(UTC) - timedelta(minutes=21)).isoformat(),
        "est_cache_ttl_secs": 300,
        "last_provider": "anthropic",
    }


@pytest.fixture
def door(monkeypatch):
    policy = {"value": HistoryWindowPolicy(turns=40, token_budget=3000, waits_for_cold_cache=True)}

    async def window(*, conversation_id: str, structure_is_live: bool):
        return policy["value"]

    monkeypatch.setitem(_ext._registry, "conversation_history_window", window)
    monkeypatch.setattr(send_boundary, "_CACHE_STATE_MEMO", type(send_boundary._CACHE_STATE_MEMO)())
    monkeypatch.setattr(send_boundary, "_HISTORY_CUT_MEMO", type(send_boundary._HISTORY_CUT_MEMO)())
    token = set_app_context(AppContext(emitter=None, user_id="u", organization_id="o", conversation_id=CONVERSATION))
    yield policy
    clear_app_context(token)


async def _resolve(persisted: list[UnifiedMessage], tail: list[UnifiedMessage]) -> tuple[dict[str, str], dict]:
    config = SimpleNamespace(messages=[*persisted, *tail], system_instruction=None, prompt_cache_key=None)
    await prepare_for_send(
        config,
        stage=STAGE_RESOLVE,
        conversation_id=CONVERSATION,
        cache_state=_cold_state(),
        history_len=len(persisted),
    )
    return _results(config.messages), dict(get_app_context().metadata.get("history_cut") or {})


@pytest.mark.asyncio
async def test_the_next_turn_keeps_the_newest_readings(door) -> None:
    door["value"] = HistoryWindowPolicy(
        turns=40, token_budget=3000, waits_for_cold_cache=True, keep_recent_tool_results=5
    )
    question = UnifiedMessage(role="user", content=[TextContent(text="why did that take so many reads?")])
    results, decision = await _resolve(_browser_run(), [question])

    assert decision["action"] == "moved" and decision["cleared_now"] > 0, "the budget must still clear old results"
    for i in range(CALLS - 5, CALLS):
        assert results[f"call{i}"] == _reading(i), f"call{i} — one of the newest readings — was cleared"
    assert results["call0"] != _reading(0), "the oldest reading should be cleared to honor the budget"


@pytest.mark.asyncio
async def test_a_run_resumed_mid_turn_keeps_every_result_of_the_turn(door) -> None:
    """A client tool round trip re-resolves mid-turn: the persisted history ends inside the turn in flight and
    nothing new from the person arrives. A cold cache here must never clear the run's own readings."""
    results, decision = await _resolve(_browser_run(), [])

    assert decision.get("cleared_now", 0) == 0
    for i in range(CALLS):
        assert results[f"call{i}"] == _reading(i), f"call{i} of the turn in flight was cleared"


def test_without_protection_the_budget_still_clears_oldest_first() -> None:
    """The protection narrows what may be cleared; with none the budget behaves exactly as before."""
    messages = _browser_run()
    report = trim_history_to_token_budget(messages, 100)
    assert report.blocks_cleared == CALLS
    protected = _browser_run()
    report = trim_history_to_token_budget(protected, 100, keep_recent_tool_results=3)
    assert report.blocks_cleared == CALLS - 3
    assert [r for r in _results(protected).values() if r.startswith("page state")] == [
        _reading(i) for i in range(CALLS - 3, CALLS)
    ]
