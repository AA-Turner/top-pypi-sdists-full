"""🚨 THE NEXT SEND STARTS FROM THE CUT THIS ONE USED — on any server task, through the real path.

Live (2026-11-19, the test admin's staff thread 3af9e95c, three server tasks; ``platform.ai_request_latency
.server_task_id``): ask 1 (task b75f…, cold) moved the history cut and wrote it into ``cache_state``. Ask 5a
(task bc32…, cold) moved it again and wrote the new cut. Ask 5b (task b75f…, warm) correctly HELD the new cut it
read from the row — then ``persistence._refresh_cache_state`` wrote back ``remembered_history_cut``: task b75f's
memo, still ask 1's cut from 14 minutes earlier (a held send never touched it). Ask 6 (task 3610…, warm) started
from that old cut: ``prefix bytes differ from the previous request at message 0``, 118,419 tokens written again
on a warm cache, and ``cache_state.history_cut.at`` still read ask 1's 17:48:56 afterwards.

Two independent layers, each proven alone here: (1) a held send makes the cut it used this process's cut
(``send_boundary._remember_the_held_cut``); (2) persistence never writes a cut decided earlier than the one the
row holds (``send_boundary.history_cut_to_persist``). The stored rows go through the real rebuild, the turn
through the real resolver, the send through the real loop stage, the request's end through the real
``persistence._refresh_cache_state``; each server task keeps its own process memos. Only the database reads and
writes are in-memory doubles.
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
from matrx_ai.config.history_budget import HistoryWindowPolicy  # noqa: E402
from matrx_ai.config.send_boundary import STAGE_LOOP, prepare_for_send  # noqa: E402
from matrx_ai.db import persistence  # noqa: E402
from matrx_ai.db.conversation_rebuild import rebuild_conversation_messages  # noqa: E402

CONVERSATION = "3af9e95c-0000-4000-8000-0000000c0ffe"
#: Every per-conversation memo a server task keeps in its own process.
PROCESS_MEMOS = (
    "_CACHE_STATE_MEMO", "_LAST_SEND_AT", "_HISTORY_CUT_MEMO", "_TRIM_REPLAY_MEMO", "_TRIM_REPLAY_DROPPED",
    "_PREFIX_BYTES_MEMO", "_WIRE_TEXT_CUTS", "_REPLAYED_CONTEXT_DROPPED", "_WIRE_TEXT_STUBS", "_LAST_BREAKDOWN",
)


class _Thread:
    def __init__(self) -> None:
        self.messages: list[SimpleNamespace] = []
        self.cache_state: dict[str, Any] = {}
        self.go_quiet()

    def go_quiet(self) -> None:
        """Hours pass: the provider cache is cold on the next ask."""
        self.cache_state["last_response_at"] = (datetime.now(UTC) - timedelta(hours=3)).isoformat()
        self.cache_state.setdefault("est_cache_ttl_secs", 300)
        self.cache_state.setdefault("last_provider", "anthropic")

    def answered(self, question: str, answer: str) -> None:
        for role, text in (("user", question), ("assistant", answer)):
            n = len(self.messages)
            self.messages.append(
                SimpleNamespace(
                    id=f"00000000-0000-4000-8000-{n:012d}", role=role, position=n, created_at=None, status="active",
                    content=[{"type": "text", "text": text}], metadata={}, deleted_at=None, is_visible_to_model=True,
                )
            )


class _Tasks:
    """Server tasks: each keeps its own process memos; only ``cache_state`` (the row) is shared."""

    def __init__(self) -> None:
        self.saved: dict[str, dict[str, Any]] = {}
        self.current: str | None = None

    def on(self, task: str) -> None:
        if self.current is not None:
            self.saved[self.current] = {n: dict(getattr(send_boundary, n)) for n in PROCESS_MEMOS}
        for name in PROCESS_MEMOS:
            memo = getattr(send_boundary, name)
            memo.clear()
            memo.update(self.saved.get(task, {}).get(name, {}))
        self.current = task


@pytest.fixture
def thread(monkeypatch):
    db = _Thread()
    for i in range(1, 7):
        db.answered(f"Plan day {i} of the Andalusia trip.", f"Day {i}: the cathedral, then tapas ({i}).")

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

    async def window(*, conversation_id: str, structure_is_live: bool):
        return HistoryWindowPolicy(turns=3, token_budget=400_000, waits_for_cold_cache=True)

    async def no_markers(*, conversation_id: str, structure_is_live: bool):
        return False

    monkeypatch.setitem(_ext._registry, "conversation_history_window", window)
    monkeypatch.setitem(_ext._registry, "perishable_state_marker", no_markers)
    previous_resolver = context_trim.get_trim_policy_resolver()

    async def holding_policy(_organization_id: Any) -> TrimPolicy:
        return TrimPolicy(cache_gate_mode="legacy", cache_gate_min_saved_tokens=10**9)

    context_trim.set_trim_policy_resolver(holding_policy)
    for name in PROCESS_MEMOS:
        getattr(send_boundary, name).clear()
    AgentCache.set(
        CONVERSATION,
        Agent(config=UnifiedConfig(model="claude-opus-5-5", system_instruction="You are the person's chief of staff.", messages=[])),
    )
    token = set_app_context(AppContext(emitter=None, user_id="u", organization_id="o", conversation_id=CONVERSATION))
    yield db
    clear_app_context(token)
    context_trim.set_trim_policy_resolver(previous_resolver)
    for name in PROCESS_MEMOS:
        getattr(send_boundary, name).clear()
    AgentCache.clear()


def _bytes(message: Any) -> str:
    parts = [b.to_storage_dict() if hasattr(b, "to_storage_dict") else b for b in message.content]
    return json.dumps({"role": str(getattr(message.role, "value", message.role)), "content": parts}, sort_keys=True, default=str)


async def _ask(db: _Thread, n: int, question: str) -> tuple[list[str], dict[str, Any], int]:
    get_app_context().metadata.pop("history_cut", None)
    config = await ConversationResolver.from_conversation_id(CONVERSATION, user_input=question)
    prep = await prepare_for_send(config, stage=STAGE_LOOP, conversation_id=CONVERSATION, request_id=f"req-{n}", iteration=1)
    sent = list(prep.wire_messages if prep.wire_messages is not None else config.messages)
    covered = len(sent)
    while covered and str(getattr(sent[covered - 1].role, "value", sent[covered - 1].role)) == "user":
        covered -= 1
    verdict = dict(get_app_context().metadata.get("history_cut") or {})
    db.answered(question, f"Here is that plan ({n}).")
    await persistence._refresh_cache_state(
        CONVERSATION, [{"provider": "anthropic", "ai_model": "claude-opus-5-5", "raw_usage": {}}], None
    )
    return [_bytes(m) for m in sent], verdict, covered


@pytest.mark.asyncio
@pytest.mark.parametrize("layers", ["both", "held_send_remembers_its_cut_only", "newest_cut_wins_only"])
async def test_a_warm_send_on_a_third_task_starts_from_the_cut_the_last_send_used(thread, monkeypatch, layers) -> None:
    if layers == "held_send_remembers_its_cut_only":
        monkeypatch.setattr(send_boundary, "history_cut_to_persist", lambda cid, existing: send_boundary.remembered_history_cut(cid))
    if layers == "newest_cut_wins_only":
        monkeypatch.setattr(send_boundary, "_remember_the_held_cut", lambda cid, cut: None)
    tasks = _Tasks()

    tasks.on("b75f")
    _, ask1, _ = await _ask(thread, 1, "Plan a day in Seville.")
    assert ask1["action"] == "moved", ask1
    old_cut = dict(thread.cache_state["history_cut"])

    tasks.on("bc32")
    _, ask2, _ = await _ask(thread, 2, "And Granada?")
    assert ask2["action"] == "held_warm", ask2

    thread.go_quiet()
    tasks.on("bc32")
    _, ask5a, _ = await _ask(thread, 3, "Thursday or Friday for Toledo?")
    assert ask5a["action"] == "moved", ask5a
    new_cut = dict(thread.cache_state["history_cut"])
    assert new_cut["first_id"] != old_cut["first_id"], (old_cut, new_cut)  # the case: the cold send moved the cut

    tasks.on("b75f")  # the task that decided the OLD cut serves the next warm ask
    held, ask5b, covered = await _ask(thread, 4, "Is my calendar free on the 27th?")
    assert ask5b["action"] == "held_warm" and ask5b["prefix"]["action"] == "held", ask5b
    assert thread.cache_state["history_cut"]["first_id"] == new_cut["first_id"], (
        "the warm send held the new cut, but its request's end wrote back an older cut this task decided earlier: "
        f"{thread.cache_state['history_cut']} (the send used {new_cut})"
    )

    tasks.on("3610")
    nxt, ask6, _ = await _ask(thread, 5, "Am I free Monday afternoon?")
    prefix = ask6["prefix"]
    assert prefix["action"] == "held" and prefix["bytes"]["first_difference"] is None, prefix
    for index in range(covered):
        assert held[index] == nxt[index], f"message {index} moved on a warm send:\n{held[index][:200]}\n{nxt[index][:200]}"
