"""🚨 THE STALE MARKERS NEVER REWRITE A WARM PREFIX — the cache law, adversarial 2026-10-30 follow-up to B2.

Arman's cache law: nothing but the removal of LARGE tool outputs may change text behind the cache line. The stale
markers (``config/perishable_state.py``) prefix an earlier turn's workspace reading — and an earlier answer that
states a date — with ``[STALE — …]``. On a mandate-held thread every turn makes the LAST turn "earlier", so the
markers rewrote text the provider had just cached: the prefix changed on every warm turn.

RED before: turn N+1 on a warm cache marked turn N's ``fs_read`` result and its dated answer, so the message list
sent on turn N was no longer a prefix of the one sent on turn N+1.

GREEN now: the markers move on the SAME cold-cache decision as the history window. While warm, exactly the blocks
marked on the last cold turn are re-marked (byte for byte); a cold cache marks every earlier reading and records
the new set on the cut (``cx_conversation.cache_state.history_cut.stale``) and on the request
(``cx_request.metadata.history_cut.stale_markers``).

Through the REAL ``prepare_for_send`` (resolve stage) with both host doors installed in ``_ext``.
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
from matrx_ai.config import TextContent, ToolResultContent, UnifiedMessage, send_boundary
from matrx_ai.config.history_budget import HistoryWindowPolicy
from matrx_ai.config.perishable_state import STALE_MARKER
from matrx_ai.config.send_boundary import HISTORY_CUT_KEY, STAGE_RESOLVE, prepare_for_send

CONVERSATION = "c0ffee00-0000-4000-8000-000000000051"
WINDOW = 40


def _turn(i: int) -> list[UnifiedMessage]:
    at = (datetime(2026, 10, 1, tzinfo=UTC) + timedelta(minutes=i)).isoformat()
    return [
        UnifiedMessage(role="user", id=f"u{i}", position=3 * i, content=[TextContent(text=f"what is in my workspace {i}")]),
        UnifiedMessage(
            role="tool",
            id=f"t{i}",
            position=3 * i + 1,
            timestamp=at,
            content=[ToolResultContent(tool_use_id=f"call{i}", name="fs_read", content=f"file {i}", output_chars=6)],
        ),
        UnifiedMessage(
            role="assistant",
            id=f"a{i}",
            position=3 * i + 2,
            timestamp=at,
            content=[TextContent(text=f"On Friday October 2 your workspace held file {i}.")],
        ),
    ]


def _wire(messages: list) -> list[str]:
    out = []
    for m in messages:
        block = m.content[0]
        out.append(f"{m.role}:{getattr(block, 'text', None) or getattr(block, 'content', None)}")
    return out


def _state(*, warm: bool, cut: dict | None) -> dict:
    age = timedelta(seconds=10) if warm else timedelta(hours=2)
    state = {
        "last_response_at": (datetime.now(UTC) - age).isoformat(),
        "est_cache_ttl_secs": 300,
        "last_provider": "anthropic",
    }
    if cut is not None:
        state[HISTORY_CUT_KEY] = cut
    return state


@pytest.fixture
def doors(monkeypatch):
    async def window(*, conversation_id: str, structure_is_live: bool):
        return HistoryWindowPolicy(turns=WINDOW, token_budget=None, waits_for_cold_cache=True)

    async def markers(*, conversation_id: str, structure_is_live: bool):
        return structure_is_live

    monkeypatch.setitem(_ext._registry, "conversation_history_window", window)
    monkeypatch.setitem(_ext._registry, "perishable_state_marker", markers)
    monkeypatch.setattr(send_boundary, "_CACHE_STATE_MEMO", type(send_boundary._CACHE_STATE_MEMO)())
    monkeypatch.setattr(send_boundary, "_HISTORY_CUT_MEMO", type(send_boundary._HISTORY_CUT_MEMO)())
    token = set_app_context(AppContext(emitter=None, user_id="u", organization_id="o", conversation_id=CONVERSATION))
    yield
    clear_app_context(token)


async def _send(turns: int, *, warm: bool, cut: dict | None) -> tuple[list[str], dict]:
    """The last send of one turn on a mandate-held thread: ``turns`` persisted turns, then this turn's question
    and the reading its tool just returned (this turn's truth, never marked) — all of it what the provider caches."""
    persisted = [m for i in range(1, turns + 1) for m in _turn(i)]
    current = _turn(turns + 1)[:2]
    config = SimpleNamespace(
        messages=[*persisted, *current],
        system_instruction=None,
        prompt_cache_key=None,
        responder_mandate_key="personal_staff.chief",
    )
    get_app_context().metadata.pop("history_cut", None)
    await prepare_for_send(
        config,
        stage=STAGE_RESOLVE,
        conversation_id=CONVERSATION,
        cache_state=_state(warm=warm, cut=cut),
        history_len=len(persisted),
    )
    return _wire(config.messages), dict(get_app_context().metadata.get("history_cut") or {})


def _persisted_cut() -> dict | None:
    return send_boundary.remembered_history_cut(CONVERSATION)


@pytest.mark.asyncio
async def test_a_warm_mandate_held_thread_keeps_an_identical_prefix(doors) -> None:
    # Turn 6 arrives on a cold cache: every earlier reading and dated answer is marked (a recorded break).
    sent, decision = await _send(5, warm=False, cut=None)
    assert sum(STALE_MARKER in line for line in sent) == 10, sent
    assert decision["stale_markers"]["action"] == "moved" and decision["stale_markers"]["cache_break"] is True
    cut = _persisted_cut()
    assert cut and len(cut["stale"]) == 10

    # Turns 7..15 arrive while warm: what was sent last turn is never rewritten.
    previous = sent
    for turns in range(6, 15):
        sent, decision = await _send(turns, warm=True, cut=cut)
        assert sent[: len(previous)] == previous, (
            f"turn {turns + 1}: a stale marker rewrote text behind the cache line while the cache was warm"
        )
        assert decision["stale_markers"]["action"] == "held_warm"
        assert decision["stale_markers"]["cache_break"] is False
        previous = sent
    # The readings from the warm turns were never marked; the cold-turn ones still are, byte for byte.
    assert "tool:file 14" in sent and f"{STALE_MARKER}" in sent[1]


@pytest.mark.asyncio
async def test_a_cold_cache_marks_every_earlier_reading_again(doors) -> None:
    await _send(5, warm=False, cut=None)
    cut = _persisted_cut()
    await _send(10, warm=True, cut=cut)
    sent, decision = await _send(10, warm=False, cut=_persisted_cut())
    assert sum(STALE_MARKER in line for line in sent) == 20
    assert decision["stale_markers"]["action"] == "moved" and decision["stale_markers"]["cache_break"] is True
    assert len(_persisted_cut()["stale"]) == 20
