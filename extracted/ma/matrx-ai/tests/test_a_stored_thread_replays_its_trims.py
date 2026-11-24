"""🚨 A STORED THREAD REPLAYS ITS TRIMS, AND THE HELD/MOVED VERDICT IS THE BYTES' — through the real path.

Live (2026-11-19, the test admin's staff thread 3af9e95c, Anthropic, a build carrying the trim replay): ask 1 (cold)
cleared two old ``fs_list`` results; ask 2, 118 s later and warm, recorded its prefix ``held`` — yet it read only
the 46,062 system + tools tokens from the cache. ``chat.request_snapshot`` of the two sends differs at message 36:
590 bytes (the cleared stub) on ask 1, 18,139 (the whole result, under a ``[STALE …]`` marker) on ask 2. The server
said why at 15:06:44: ``trim replay: 2 recorded key(s) name more than one block in this history and are not
replayed``. A tool result rebuilt from the database carries ``tool_use_id`` AND ``call_id``, equal; the replay's
repeated-id guard counted one block twice, called every recorded key ambiguous, dropped it from the record — and
``cache_state.trim_replay`` was written back empty. The earlier guard passed because its hand-built results carried
``tool_use_id`` only and its persistence was rebuilt by hand.

This guard runs the REAL pieces end to end: the stored rows go through the real rebuild
(``rebuild_conversation_messages``), the turn through the real resolver (``ConversationResolver.from_conversation_id``
on a process-cache hit → ``_finish`` → ``prepare_for_send`` resolve stage, reading the conversation row), the send
through the real loop stage, and the request's end through the real ``persistence._refresh_cache_state`` writing the
row the next ask reads. Only the database reads/writes are in-memory doubles.

Second layer: the verdict compares the bytes. A send whose messages differ from the previous send's inside the part
that send's cache line covered is MOVED ("prefix bytes differ … at message N"), whatever the shaping steps believed.
"""

from __future__ import annotations

import asyncio
import json
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from typing import Any

import pytest
from matrx_connect.context.app_context import (
    AppContext,
    clear_app_context,
    get_app_context,
    set_app_context,
)

from matrx_ai import _ext
from matrx_ai.db._registry import configure_db

# The rebuild resolves its row models from the registry at import time; it only uses them as type references.
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

CONVERSATION = "3af9e95c-0000-4000-8000-00000000c0de"
LISTING_CHARS = 18_000
EARLY_TURNS = 12


class _Thread:
    """The staff thread as the database holds it: message rows, tool-call rows, the conversation row."""

    def __init__(self) -> None:
        self.messages: list[SimpleNamespace] = []
        self.tool_calls: list[SimpleNamespace] = []
        self.cache_state: dict[str, Any] = {
            "last_response_at": (datetime.now(UTC) - timedelta(hours=3)).isoformat(),
            "est_cache_ttl_secs": 300,
            "last_provider": "anthropic",
        }

    def _row(self, role: str, content: list[dict[str, Any]]) -> SimpleNamespace:
        n = len(self.messages)
        row = SimpleNamespace(
            id=f"00000000-0000-4000-8000-{n:012d}", role=role, position=n, content=content, created_at=None,
            status="active", metadata={}, deleted_at=None, is_visible_to_model=True,
        )
        self.messages.append(row)
        return row

    def listing_turn(self, i: int) -> None:
        call = f"toolu_01{i:06d}fsList"
        self._row("user", [{"type": "text", "text": f"what is in my workspace? ({i})"}])
        self._row("assistant", [{"type": "tool_call", "call_id": call, "name": "fs_list", "arguments": {"path": "/home/agent"}}])
        # Exactly what persistence stores: a pointer block; the rebuild hydrates it from the tool-call row.
        tool = self._row("tool", [{"type": "tool_result", "call_id": call, "tool_use_id": call, "name": "fs_list", "output_chars": 0}])
        listing = "\n".join(f"/home/agent/file-{i}-{n:05d}.txt" for n in range(LISTING_CHARS // 30))[:LISTING_CHARS]
        self.tool_calls.append(
            SimpleNamespace(
                id=f"tc-{i}", call_id=call, message_id=tool.id, tool_name="fs_list", output=listing, is_error=False,
                status="completed", output_chars=len(listing), output_preview=None, error_type=None, error_message=None,
                deleted_at=None, metadata={}, model_stub_at=None,
            )
        )
        self._row("assistant", [{"type": "text", "text": f"Folders: cloud-files, projects ({i})."}])

    def answered(self, question: str, answer: str) -> None:
        self._row("user", [{"type": "text", "text": question}])
        self._row("assistant", [{"type": "text", "text": answer}])


@pytest.fixture
def thread(monkeypatch):
    db = _Thread()
    for i in range(1, EARLY_TURNS + 1):
        db.listing_turn(i)

    async def load_conversation_by_id(_cid: str) -> Any:
        return SimpleNamespace(
            id=CONVERSATION, cache_state=dict(db.cache_state), config={}, last_request_status="completed",
            system_prompt_frozen=None, created_at=None,
        )

    async def load_by_id(_cid: str) -> Any:
        return None  # not mandate-held: the process-cache path

    async def rebuilt(_cid: str) -> list[Any]:
        return await rebuild_conversation_messages(list(db.messages), list(db.tool_calls), [])

    fake = SimpleNamespace(
        conversation=SimpleNamespace(load_conversation_by_id=load_conversation_by_id, load_by_id=load_by_id),
        get_rebuilt_conversation_messages=rebuilt,
    )
    monkeypatch.setattr("matrx_ai.db.cxm", fake, raising=False)
    monkeypatch.setattr("matrx_ai.client_host.get_conversation_store", lambda: None, raising=False)
    # Persistence's real ``_refresh_cache_state``; only its read and its queued UPDATE are the in-memory row.
    monkeypatch.setattr(persistence, "_cxm", lambda: fake)
    monkeypatch.setattr(persistence, "_get_live_coordinator", lambda: object())

    def write(_cid: str, **fields: Any) -> None:
        db.cache_state = json.loads(json.dumps(fields["cache_state"], default=str))  # a jsonb round trip

    monkeypatch.setattr(persistence, "_queue_conversation_update", write)

    # The staff thread's host doors: its history window (40 turns, a budget this short thread stays under, so the
    # trim clears and the window does not, as live), its stale markers, and a trim policy the warm cache holds (the
    # live payback gate said "hold" on every warm ask).
    async def window(*, conversation_id: str, structure_is_live: bool):
        return HistoryWindowPolicy(turns=40, token_budget=400_000, waits_for_cold_cache=True, keep_recent_tool_results=3)

    async def markers(*, conversation_id: str, structure_is_live: bool):
        return True

    monkeypatch.setitem(_ext._registry, "conversation_history_window", window)
    monkeypatch.setitem(_ext._registry, "perishable_state_marker", markers)
    previous_resolver = context_trim.get_trim_policy_resolver()

    async def holding_policy(_organization_id: Any) -> TrimPolicy:
        return TrimPolicy(cache_gate_mode="legacy", cache_gate_min_saved_tokens=10**9)

    context_trim.set_trim_policy_resolver(holding_policy)
    _forget_this_process()
    AgentCache.set(
        CONVERSATION,
        Agent(config=UnifiedConfig(model="claude-opus-5-5", system_instruction="You are the person's chief of staff.", messages=[])),
    )
    token = set_app_context(AppContext(emitter=None, user_id="u", organization_id="o", conversation_id=CONVERSATION))
    yield db
    clear_app_context(token)
    context_trim.set_trim_policy_resolver(previous_resolver)
    _forget_this_process()
    AgentCache.clear()


def _forget_this_process() -> None:
    """The next ask lands on another server task: only what persistence wrote into ``cache_state`` carries over."""
    for memo in ("_CACHE_STATE_MEMO", "_HISTORY_CUT_MEMO", "_TRIM_REPLAY_MEMO", "_TRIM_REPLAY_DROPPED", "_PREFIX_BYTES_MEMO"):
        getattr(send_boundary, memo, {}).clear()


def _bytes(message: Any) -> str:
    """What the provider is sent for one message (cache marks are not part of a message)."""
    parts = [b.to_storage_dict() if hasattr(b, "to_storage_dict") else b for b in message.content]
    return json.dumps({"role": str(getattr(message.role, "value", message.role)), "content": parts}, sort_keys=True, default=str)


async def _ask(db: _Thread, n: int, question: str) -> tuple[list[str], dict[str, Any], int]:
    """One staff ask: resolve (real resolver), one send (real loop stage), the request's end (real persistence)."""
    get_app_context().metadata.pop("history_cut", None)
    config = await ConversationResolver.from_conversation_id(CONVERSATION, user_input=question)
    prep = await prepare_for_send(config, stage=STAGE_LOOP, conversation_id=CONVERSATION, request_id=f"req-{n}", iteration=1)
    sent = list(prep.wire_messages if prep.wire_messages is not None else config.messages)
    wire = [_bytes(m) for m in sent]
    covered = len(sent)
    while covered and str(getattr(sent[covered - 1].role, "value", sent[covered - 1].role)) == "user":
        covered -= 1  # the newest person turn rides after the rolling cache mark
    verdict = dict(get_app_context().metadata.get("history_cut") or {})
    db.answered(question, f"Here is the plan ({n}).")
    await persistence._refresh_cache_state(
        CONVERSATION, [{"provider": "anthropic", "ai_model": "claude-opus-5-5", "raw_usage": {}}], None
    )
    return wire, verdict, covered


@pytest.mark.asyncio
@pytest.mark.parametrize("next_ask_on", ["same_task", "another_task"])
async def test_a_warm_ask_on_a_stored_thread_resends_the_cold_asks_messages_byte_for_byte(thread, next_ask_on) -> None:
    cold, cold_verdict, covered = await _ask(thread, 1, "Plan a three-day trip to Lisbon.")
    assert cold_verdict["prefix"]["trim"]["rewritten_now"] >= 1, cold_verdict  # the case: the cold send's trim cleared
    record = thread.cache_state.get("trim_replay") or {}
    assert record.get("results"), f"the cold send's trim rewrites never reached the row: {thread.cache_state}"
    if next_ask_on == "another_task":
        _forget_this_process()

    warm, warm_verdict, _ = await _ask(thread, 2, "Plan a two-day trip to Porto.")
    for index in range(covered):
        assert cold[index] == warm[index], (
            f"message {index} changed between the cold ask and its warm follow-up, inside the cached prefix — the "
            f"provider writes the history again from here.\ncold: {cold[index][:300]}\nwarm: {warm[index][:300]}"
        )
    prefix = warm_verdict["prefix"]
    assert prefix["action"] == "held", prefix
    assert prefix["bytes"]["first_difference"] is None and prefix["bytes"]["compared"] == covered, prefix
    assert (thread.cache_state.get("trim_replay") or {}).get("results") == record["results"], thread.cache_state


@pytest.mark.asyncio
async def test_a_send_whose_bytes_moved_is_never_recorded_as_held(thread, monkeypatch) -> None:
    """The live defect's shape — the replay silently made nothing — must read MOVED, naming the message."""
    cold, _, covered = await _ask(thread, 1, "Plan a three-day trip to Lisbon.")
    monkeypatch.setattr(
        context_trim, "replay_trim_rewrites", lambda messages, record, policy=None: {"results": 0, "arguments": 0, "present": dict(record or {})}
    )
    warm, verdict, _ = await _ask(thread, 2, "Plan a two-day trip to Porto.")
    first = next(i for i in range(covered) if cold[i] != warm[i])
    prefix = verdict["prefix"]
    assert prefix["action"] == "moved" and prefix["cache_break"] is True, prefix
    assert prefix["bytes"]["first_difference"] == first, prefix
    assert any(r.startswith("prefix bytes differ from the previous request at message") for r in prefix["reasons"]), prefix


def test_one_rebuilt_result_is_one_block_to_the_replay() -> None:
    """The minimal shape: a result carrying ``tool_use_id`` and ``call_id``, equal, is replayed (it was 'ambiguous')."""
    from matrx_ai.config import ToolCallContent, UnifiedMessage

    async def rebuilt() -> list[Any]:
        db = _Thread()
        db.listing_turn(1)
        return await rebuild_conversation_messages(db.messages, db.tool_calls, [])

    messages = asyncio.run(rebuilt())
    block = messages[2].content[0]
    assert block.tool_use_id == block.call_id  # what the rebuild produces
    assert isinstance(messages[1].content[0], ToolCallContent) and isinstance(messages[0], UnifiedMessage)
    out = context_trim.replay_trim_rewrites(messages, {"results": [block.tool_use_id]})
    assert out["results"] == 1 and out["present"]["results"] == [block.tool_use_id], out
