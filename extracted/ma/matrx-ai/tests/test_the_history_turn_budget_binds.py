"""🚨 THE HISTORY WINDOW'S TOKEN BOUND BINDS — whole turns, cold sends only, through the real path.

Live (2026-11-19, the test admin's staff thread 3af9e95c, live proof 6): every staff ask sent 199k-211k prompt
tokens, over the 200,000 input budget, so ``input_fit`` ran its last-resort trim on staff sends (A6: 39 thinking
blocks dropped, 38 tool blocks stubbed). The window is 40 turns with a "12,000-token" budget, but that budget only
stubs old tool results and never touches words: ask 1's 87 messages were ~500k characters, 347k of them four
earlier turns' kept turn context (``chat.message.metadata.turn_context_in_cache`` at positions 1216/1230/1238/1250,
~87k characters each) — a limit that did not limit. And its estimate never counted a kept block at all (it rides
the row's metadata, replayed at the loop stage).

The bound that binds (``history_budget.cut_oldest_turns_to_budget``, host knob
``chat.history.held_history_turn_token_budget``): after the results are stubbed, while the history — counting each
turn's replayed kept block — is still over the turn budget, the oldest whole turns are left out. It moves only when
the window's cut moves (cold cache), so a warm follow-up replays the same first message byte for byte.

The stored rows go through the real rebuild, the turn through the real resolver, the send through the real loop
stage, the request's end through the real ``persistence._refresh_cache_state``. Only the database is in memory.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from typing import Any

import pytest
from matrx_connect.context.app_context import AppContext, clear_app_context, get_app_context, set_app_context

from matrx_ai import _ext
from matrx_ai.db._registry import configure_db

configure_db(models={name: SimpleNamespace for name in ("CxMessage", "CxToolCall", "CxMedia", "Message", "ToolCall", "Media")})

from matrx_ai.agents.cache import AgentCache  # noqa: E402
from matrx_ai.agents.definition import Agent  # noqa: E402
from matrx_ai.agents.resolver import ConversationResolver  # noqa: E402
from matrx_ai.config import UnifiedConfig, context_trim, send_boundary  # noqa: E402
from matrx_ai.config.context_trim import TrimPolicy  # noqa: E402
from matrx_ai.config.history_budget import (  # noqa: E402
    HistoryWindowPolicy,
    cut_oldest_turns_to_budget,
    estimate_sent_history_tokens,
)
from matrx_ai.config.send_boundary import STAGE_LOOP, prepare_for_send  # noqa: E402
from matrx_ai.config.typed_text_last import STORED_TURN_CONTEXT_KEY  # noqa: E402
from matrx_ai.db import persistence  # noqa: E402
from matrx_ai.db.conversation_rebuild import rebuild_conversation_messages  # noqa: E402
from matrx_ai.testing.profile_factory import make_profile  # noqa: E402

CONVERSATION = "3af9e95c-0000-4000-8000-00000000b0d9"
TURNS = 30
#: The turns whose row keeps its whole turn-context block, as positions 1216/1230/1238/1250 did live.
KEPT_ON = (5, 12, 19, 26)
KEPT_CHARS = 80_000
TURN_BUDGET = 40_000  # tokens: 160k characters at the window's estimate
PROFILE = make_profile(model_name="claude-opus-5-5", wire_format="anthropic_chat")
MEMOS = ("_CACHE_STATE_MEMO", "_LAST_SEND_AT", "_HISTORY_CUT_MEMO", "_TRIM_REPLAY_MEMO", "_TRIM_REPLAY_DROPPED", "_PREFIX_BYTES_MEMO")


def _kept_block(turn: int) -> str:
    body = f"<earlier_turn_context>KEPT-BLOCK-{turn}</earlier_turn_context>\n"
    return '<turn_context source="platform">\n' + body + ("reference material " * (KEPT_CHARS // 19)) + "\n</turn_context>"


class _Thread:
    def __init__(self) -> None:
        self.messages: list[SimpleNamespace] = []
        self.cache_state: dict[str, Any] = {"est_cache_ttl_secs": 300, "last_provider": "anthropic"}
        self.go_quiet()

    def go_quiet(self) -> None:
        self.cache_state["last_response_at"] = (datetime.now(UTC) - timedelta(hours=3)).isoformat()

    def _row(self, role: str, text: str, metadata: dict[str, Any] | None = None) -> SimpleNamespace:
        n = len(self.messages)
        row = SimpleNamespace(
            id=f"00000000-0000-4000-8000-{n:012d}", role=role, position=n, created_at=None, status="active",
            content=[{"type": "text", "text": text}], metadata=metadata or {}, deleted_at=None, is_visible_to_model=True,
        )
        self.messages.append(row)
        return row

    def turn(self, i: int, question: str, answer: str) -> None:
        self._row("user", question, {STORED_TURN_CONTEXT_KEY: _kept_block(i)} if i in KEPT_ON else None)
        self._row("assistant", answer)

    def first_row_of_turn(self, i: int) -> SimpleNamespace:
        return [r for r in self.messages if r.role == "user"][i - 1]


@pytest.fixture
def thread(monkeypatch):
    db = _Thread()
    for i in range(1, TURNS + 1):
        db.turn(i, f"Plan day {i} of the trip.", f"Day {i}: " + "a long walk through the old town, " * 60)

    async def load_conversation_by_id(_cid: str) -> Any:
        return SimpleNamespace(
            id=CONVERSATION, cache_state=json.loads(json.dumps(db.cache_state)), config={},
            last_request_status="completed", system_prompt_frozen=None, created_at=None,
        )

    async def load_by_id(_cid: str) -> Any:
        return None

    async def rebuilt(_cid: str) -> list[Any]:
        return await rebuild_conversation_messages(list(db.messages), [], [])

    fake = SimpleNamespace(
        conversation=SimpleNamespace(load_conversation_by_id=load_conversation_by_id, load_by_id=load_by_id),
        get_rebuilt_conversation_messages=rebuilt,
    )
    monkeypatch.setattr("matrx_ai.db.cxm", fake, raising=False)
    monkeypatch.setattr("matrx_ai.client_host.get_conversation_store", lambda: None, raising=False)
    monkeypatch.setattr(persistence, "_cxm", lambda: fake)
    monkeypatch.setattr(persistence, "_get_live_coordinator", lambda: object())

    def write(_cid: str, **fields: Any) -> None:
        db.cache_state = json.loads(json.dumps(fields["cache_state"], default=str))

    monkeypatch.setattr(persistence, "_queue_conversation_update", write)

    async def profile(config: Any, *, conversation_id: str | None, iteration: int | None = None) -> Any:
        return PROFILE  # the catalog read: the wire is ordered (kept blocks replayed) as on the live send

    monkeypatch.setattr(send_boundary, "_send_profile", profile)

    # The staff thread's window as the host builds it from the chat.history knobs.
    async def window(*, conversation_id: str, structure_is_live: bool):
        return HistoryWindowPolicy(
            turns=40, token_budget=12_000, waits_for_cold_cache=True, keep_recent_tool_results=10,
            turn_token_budget=TURN_BUDGET,
        )

    async def no_markers(*, conversation_id: str, structure_is_live: bool):
        return False

    monkeypatch.setitem(_ext._registry, "conversation_history_window", window)
    monkeypatch.setitem(_ext._registry, "perishable_state_marker", no_markers)
    previous_resolver = context_trim.get_trim_policy_resolver()

    async def holding_policy(_organization_id: Any) -> TrimPolicy:
        return TrimPolicy(cache_gate_mode="legacy", cache_gate_min_saved_tokens=10**9)

    context_trim.set_trim_policy_resolver(holding_policy)
    for name in MEMOS:
        getattr(send_boundary, name).clear()
    AgentCache.set(
        CONVERSATION,
        Agent(config=UnifiedConfig(model="claude-opus-5-5", system_instruction="You are the person's chief of staff.", messages=[])),
    )
    token = set_app_context(AppContext(emitter=None, user_id="u", organization_id="o", conversation_id=CONVERSATION))
    yield db
    clear_app_context(token)
    context_trim.set_trim_policy_resolver(previous_resolver)
    for name in MEMOS:
        getattr(send_boundary, name).clear()
    AgentCache.clear()


def _bytes(message: Any) -> str:
    parts = [b.to_storage_dict() if hasattr(b, "to_storage_dict") else b for b in message.content]
    return json.dumps({"role": str(getattr(message.role, "value", message.role)), "content": parts}, sort_keys=True, default=str)


async def _ask(db: _Thread, n: int, question: str) -> dict[str, Any]:
    get_app_context().metadata.pop("history_cut", None)
    config = await ConversationResolver.from_conversation_id(CONVERSATION, user_input=question)
    history = list(config.messages)
    prep = await prepare_for_send(config, stage=STAGE_LOOP, conversation_id=CONVERSATION, request_id=f"req-{n}", iteration=1)
    sent = list(prep.wire_messages if prep.wire_messages is not None else config.messages)
    covered = len(sent)
    while covered and str(getattr(sent[covered - 1].role, "value", sent[covered - 1].role)) == "user":
        covered -= 1
    verdict = dict(get_app_context().metadata.get("history_cut") or {})
    db.turn(TURNS + n, question, f"Here is that plan ({n}).")
    await persistence._refresh_cache_state(
        CONVERSATION, [{"provider": "anthropic", "ai_model": "claude-opus-5-5", "raw_usage": {}}], None
    )
    return {"history": history, "wire": [_bytes(m) for m in sent], "covered": covered, "verdict": verdict}


@pytest.mark.asyncio
async def test_a_text_heavy_history_is_cut_to_the_turn_budget_at_a_turn_boundary_and_held_while_warm(thread) -> None:
    rows = [r for r in thread.messages]
    over = estimate_sent_history_tokens([SimpleNamespace(content=r.content, metadata=r.metadata, role=r.role) for r in rows])
    assert over > TURN_BUDGET * 2, over  # the case: four kept blocks put the stored history far over the budget

    cold = await _ask(thread, 1, "Thursday or Friday for Toledo?")
    verdict = cold["verdict"]
    assert verdict["action"] == "moved", verdict
    cut = verdict.get("turn_budget") or {}
    assert cut.get("turns_dropped", 0) > 0 and cut["tokens_after"] <= TURN_BUDGET, (
        f"the window read back a history over its turn budget: {verdict}"
    )
    assert estimate_sent_history_tokens(cold["history"]) <= TURN_BUDGET, estimate_sent_history_tokens(cold["history"])
    wire = "\n".join(cold["wire"])
    assert f"KEPT-BLOCK-{KEPT_ON[-1]}" in wire, "a kept turn's block is replayed on the wire (what the budget counts)"
    for turn in KEPT_ON[:-1]:
        assert f"KEPT-BLOCK-{turn}" not in wire, f"turn {turn}'s kept block is still sent"
    first = thread.cache_state["history_cut"]
    opening = next(r for r in thread.messages if r.id == first["first_id"])
    assert opening.role == "user", "the cut landed inside a turn"
    assert first["turn_token_budget"] == TURN_BUDGET

    warm = await _ask(thread, 2, "Is my calendar free on the 27th?")
    prefix = warm["verdict"]["prefix"]
    assert warm["verdict"]["action"] == "held_warm" and prefix["action"] == "held", warm["verdict"]
    assert prefix["bytes"]["first_difference"] is None, prefix
    assert warm["wire"][: cold["covered"]] == cold["wire"][: cold["covered"]]
    assert thread.cache_state["history_cut"]["first_id"] == first["first_id"]


def test_the_newest_earlier_turn_and_the_turn_in_flight_always_stay() -> None:
    """A last turn alone over the budget is kept as it is (never cut inside a turn, never emptied)."""
    big = SimpleNamespace(role="user", content=[{"type": "text", "text": "x" * 400_000}], metadata={})
    answer = SimpleNamespace(role="assistant", content=[{"type": "text", "text": "ok"}], metadata={})
    older = SimpleNamespace(role="user", content=[{"type": "text", "text": "hi"}], metadata={})
    history = [older, answer, big, answer]
    kept, report = cut_oldest_turns_to_budget(history, 1_000)
    assert kept == [big, answer] and report.turns_dropped == 1 and report.over_budget_after
    in_flight = SimpleNamespace(role="user", content=[{"type": "text", "text": "now"}], metadata={})
    kept, report = cut_oldest_turns_to_budget([older, answer, big, answer, in_flight], 1_000, protect_from=4)
    assert kept == [big, answer, in_flight], "the newest earlier turn left with the turn in flight"
