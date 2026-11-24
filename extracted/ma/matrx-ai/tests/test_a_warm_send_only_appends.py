"""🚨 A WARM SEND ONLY APPENDS — the message prefix the provider cached is rebuilt byte for byte.

Live (2026-11-19, the test admin's staff thread 3af9e95c, Anthropic): asks a few minutes apart alternated cold /
warm, and EVERY warm ask read only the 46,062 system + tools tokens and re-wrote ~55k of history. The two sends'
snapshots differed from message 30 on:

* the cold send's context trim (``_gated_trim``, gate rule ``cold_cache``) cleared two old ``fs_list`` results.
  Its rewrites lived in memory only; the warm send's trim was held (``cache_protect``), so a result the cold send
  had cleared came back IN FULL (message 42, ~18k);
* the stale markers ran BEFORE the trim: on the cold send the trim replaced a marked block whole (the marker went
  with it — and a window-cleared stub carrying a marker was not recognised as cleared, so it was cleared AGAIN); on
  the warm send nothing cleared it after the marker, so the stub went out with ``[STALE …]`` on top (message 30).

GREEN now: every trim rewrite is recorded (``cache_state.trim_replay``) and replayed on every later send before the
markers run — a deterministic function of persisted state, never of whether THIS send happened to trim; a cleared
stub is never marked. The guard below fails on the old code (the warm wire differs from the cold one) and passes
on the new. Its second case: a send the trim is genuinely forced to rewrite is recorded as a MOVED prefix, never
silently (``history_cut.prefix`` → ``cx_request.metadata`` and the latency row's ``cache_outcome``).

Through the REAL ``prepare_for_send`` (resolve stage) with the staff thread's two host doors installed.
"""

from __future__ import annotations

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
from matrx_ai.config import (
    TextContent,
    ToolCallContent,
    ToolResultContent,
    UnifiedMessage,
    send_boundary,
)
from matrx_ai.config.context_trim import TrimPolicy
from matrx_ai.config.history_budget import HistoryWindowPolicy
from matrx_ai.config.send_boundary import HISTORY_CUT_KEY, STAGE_RESOLVE, prepare_for_send

CONVERSATION = "c0ffee00-0000-4000-8000-0000000000a7"
RESULT_CHARS = 9_000


def _turn(i: int) -> list[UnifiedMessage]:
    """One staff-thread turn: the person asks, the agent lists the workspace, reads the result, answers."""
    at = int((datetime(2026, 11, 19, 8, tzinfo=UTC) + timedelta(minutes=10 * i)).timestamp())
    listing = "\n".join(f"always-on-marker-{i}-{n:04d}.txt" for n in range(RESULT_CHARS // 30))[:RESULT_CHARS]
    return [
        UnifiedMessage(role="user", id=f"u{i}", position=4 * i, content=[TextContent(text=f"what is in my workspace? ({i})")]),
        UnifiedMessage(
            role="assistant",
            id=f"c{i}",
            position=4 * i + 1,
            timestamp=at,
            content=[ToolCallContent(id=f"call{i}", name="fs_list", arguments={"path": "/home/agent"})],
        ),
        UnifiedMessage(
            role="tool",
            id=f"t{i}",
            position=4 * i + 2,
            timestamp=at,
            content=[
                ToolResultContent(tool_use_id=f"call{i}", name="fs_list", content=listing, output_chars=len(listing))
            ],
        ),
        UnifiedMessage(
            role="assistant",
            id=f"a{i}",
            position=4 * i + 3,
            timestamp=at,
            content=[TextContent(text=f"Folders: cloud-files, projects. Plus {80 + i} marker files.")],
        ),
    ]


def _block(block: Any) -> dict[str, Any]:
    return {
        key: getattr(block, key)
        for key in ("type", "text", "id", "tool_use_id", "name", "arguments", "content")
        if getattr(block, key, None) not in (None, "")
    }


def _wire(messages: list[UnifiedMessage]) -> list[str]:
    """What the provider is sent for each message, as bytes."""
    return [
        json.dumps({"role": m.role, "content": [_block(b) for b in m.content]}, sort_keys=True, default=str)
        for m in messages
    ]


def _state(*, age: timedelta, previous: dict[str, Any] | None = None) -> dict[str, Any]:
    """``cx_conversation.cache_state`` as persistence writes it after a turn (``_refresh_cache_state``): the row's
    existing state, the fresh cache facts, then what this process remembered."""
    state: dict[str, Any] = {
        **(previous or {}),
        "last_response_at": (datetime.now(UTC) - age).isoformat(),
        "est_cache_ttl_secs": 300,
        "last_provider": "anthropic",
    }
    cut = send_boundary.remembered_history_cut(CONVERSATION)
    if cut is not None:
        state[HISTORY_CUT_KEY] = cut
    extras = getattr(send_boundary, "persisted_prefix_state", None)  # absent before the fix
    if extras is not None:
        state.update(extras(CONVERSATION))
    return state


@pytest.fixture
def staff_thread(monkeypatch):
    async def window(*, conversation_id: str, structure_is_live: bool):
        # The staff thread's window: 40 turns, a token budget the oldest readings overflow, newest kept.
        return HistoryWindowPolicy(turns=40, token_budget=14_000, waits_for_cold_cache=True, keep_recent_tool_results=3)

    async def markers(*, conversation_id: str, structure_is_live: bool):
        return True

    monkeypatch.setitem(_ext._registry, "conversation_history_window", window)
    monkeypatch.setitem(_ext._registry, "perishable_state_marker", markers)
    for memo in ("_CACHE_STATE_MEMO", "_HISTORY_CUT_MEMO", "_TRIM_REPLAY_MEMO"):
        if hasattr(send_boundary, memo):
            monkeypatch.setattr(send_boundary, memo, type(getattr(send_boundary, memo))())
    token = set_app_context(AppContext(emitter=None, user_id="u", organization_id="o", conversation_id=CONVERSATION))
    yield
    clear_app_context(token)


def _forget_this_process() -> None:
    """The next ask lands on another server task: only what persistence wrote into ``cache_state`` carries over."""
    send_boundary._CACHE_STATE_MEMO.clear()
    send_boundary._HISTORY_CUT_MEMO.clear()
    if hasattr(send_boundary, "_TRIM_REPLAY_MEMO"):
        send_boundary._TRIM_REPLAY_MEMO.clear()


async def _ask(turns: int, *, state: dict[str, Any], policy: TrimPolicy) -> tuple[list[str], dict[str, Any]]:
    """One ask: ``turns`` persisted turns reloaded fresh from the database (pristine), then the new question."""
    persisted = [m for i in range(1, turns + 1) for m in _turn(i)]
    config = SimpleNamespace(
        messages=[*persisted, _turn(turns + 1)[0]],
        system_instruction=None,
        prompt_cache_key=None,
        responder_mandate_key="personal_staff.chief",
    )
    get_app_context().metadata.pop("history_cut", None)
    await prepare_for_send(
        config,
        stage=STAGE_RESOLVE,
        conversation_id=CONVERSATION,
        cache_state=state,
        history_len=len(persisted),
        policy=policy,
    )
    return _wire(config.messages), dict(get_app_context().metadata.get("history_cut") or {})


def _holding_policy() -> TrimPolicy:
    # A warm cache holds the trim (the live thread's payback gate said "hold" on every warm ask).
    return TrimPolicy(cache_gate_mode="legacy", cache_gate_min_saved_tokens=10**9)


@pytest.mark.asyncio
@pytest.mark.parametrize("next_ask_on", ["same_task", "another_task"])
async def test_a_warm_follow_up_rebuilds_the_cold_sends_messages_byte_for_byte(staff_thread, next_ask_on) -> None:
    policy = _holding_policy()
    # Ask 1 arrives after a long gap: cold. The window clears the oldest readings, the trim clears more.
    cold, cold_cut = await _ask(8, state=_state(age=timedelta(hours=3)), policy=policy)
    assert any("[tool result cleared]" in line for line in cold), "the fixture must make the cold send clear results"
    persisted = _state(age=timedelta(minutes=2, seconds=30), previous=_state(age=timedelta(hours=3)))  # ask 1 done
    if next_ask_on == "another_task":
        _forget_this_process()

    # Ask 2, a few minutes later, while the cache is warm: the first ask's turn is now persisted history.
    warm, warm_cut = await _ask(9, state=persisted, policy=policy)
    for index, (was, now) in enumerate(zip(cold, warm[: len(cold)], strict=True)):
        assert was == now, (
            f"message {index} changed between a cold send and its warm follow-up — the warm send re-writes the cached "
            f"prefix from here on.\ncold: {was[:300]}\nwarm: {now[:300]}"
        )
    assert len(warm) > len(cold)
    assert warm_cut["prefix"]["action"] == "held", warm_cut

    # Ask 3, warm again: still only appends.
    persisted = _state(age=timedelta(minutes=1), previous=persisted)
    if next_ask_on == "another_task":
        _forget_this_process()
    third, _ = await _ask(10, state=persisted, policy=policy)
    assert third[: len(warm)] == warm


@pytest.mark.asyncio
async def test_a_send_the_trim_is_forced_to_rewrite_is_recorded_as_moved(staff_thread) -> None:
    holding = _holding_policy()
    _, cold_cut = await _ask(8, state=_state(age=timedelta(hours=3)), policy=holding)
    assert cold_cut["prefix"]["action"] == "moved" and cold_cut["prefix"]["cache_break"] is True
    assert "the provider cache is cold" in " ".join(cold_cut["prefix"]["reasons"])

    # Warm, but nothing holds the trim (a zero floor — the same as a payback "take" or a forced-near-limit send):
    # turn 6's reading has aged into the trim's tier, so this send really rewrites history behind the last mark.
    taking = TrimPolicy(cache_gate_mode="legacy", cache_gate_min_saved_tokens=0)
    _, warm_cut = await _ask(9, state=_state(age=timedelta(minutes=2)), policy=taking)
    prefix = warm_cut["prefix"]
    assert prefix["action"] == "moved" and prefix["cache_break"] is True, prefix
    assert any(reason.startswith("context trim") for reason in prefix["reasons"]), prefix
    assert prefix["trim"]["rewritten_now"] >= 1


def test_a_result_cleared_after_its_arguments_were_trimmed_replays_the_same_bytes() -> None:
    """The stub's ``refetch`` reads the call's arguments as the pass that cleared it saw them. A call's 9,000-char
    arguments reach tier 1 (12 positions back) on an early send; its 5,000-char result only reaches tier 2 (24 back)
    sends later, and its stub then reads the TRIMMED arguments. A replay on the pristine history writes the same bytes."""
    from copy import deepcopy

    from matrx_ai.config.context_trim import (
        replay_trim_rewrites,
        trim_messages_context,
        trim_rewrite_record,
    )

    def history(turns: int) -> list[UnifiedMessage]:
        out: list[UnifiedMessage] = []
        for i in range(1, turns + 1):
            out += [
                UnifiedMessage(role="user", position=4 * i, content=[TextContent(text=f"q{i}")]),
                UnifiedMessage(
                    role="assistant",
                    position=4 * i + 1,
                    content=[ToolCallContent(id=f"k{i}", name="sql", arguments={"action": "query", "sql": "s" * 9_000})],
                ),
                UnifiedMessage(
                    role="tool",
                    position=4 * i + 2,
                    content=[ToolResultContent(tool_use_id=f"k{i}", name="sql", content="r" * 5_000, output_chars=5_000)],
                ),
                UnifiedMessage(role="assistant", position=4 * i + 3, content=[TextContent(text=f"a{i}")]),
            ]
        return out

    policy = TrimPolicy()
    record: dict[str, Any] | None = None
    sent = None
    for turns in range(2, 12):  # one send per turn; each starts from the pristine history plus the record
        live = history(turns)
        replay_trim_rewrites(live, record, policy)
        report = trim_messages_context(live, policy=policy, cache_state=None)
        record = trim_rewrite_record(report, record)
        sent = live
    assert record and record["results_after_arguments"], record  # the case this test exists for

    replayed = history(11)
    replay_trim_rewrites(replayed, record, policy)
    assert _wire(replayed) == _wire(sent)
    assert _wire(deepcopy(replayed)) == _wire(sent)


def test_a_recorded_id_that_names_two_results_clears_neither() -> None:
    """Tool-call ids repeat on some wires; a replay must never clear a result the trim did not choose."""
    from matrx_ai.config import TextContent, ToolCallContent, ToolResultContent, UnifiedMessage
    from matrx_ai.config.context_trim import replay_trim_rewrites

    def turn(i: int, cid: str) -> list[UnifiedMessage]:
        return [
            UnifiedMessage(role="user", position=4 * i, content=[TextContent(text=f"q{i}")]),
            UnifiedMessage(role="assistant", position=4 * i + 1,
                           content=[ToolCallContent(id=cid, name="fs_read", arguments={"path": f"/f{i}"})]),
            UnifiedMessage(role="tool", position=4 * i + 2,
                           content=[ToolResultContent(tool_use_id=cid, name="fs_read", content=f"BODY{i} " * 800,
                                                      output_chars=4800)]),
        ]

    msgs = turn(1, "call_0") + turn(2, "call_0")
    out = replay_trim_rewrites(msgs, {"results": ["call_0"]})
    bodies = [str(m.content[0].content) for m in msgs if m.role == "tool"]
    assert out["results"] == 0
    assert bodies[0].startswith("BODY1") and bodies[1].startswith("BODY2")
    assert out["present"]["results"] == []  # the ambiguous key leaves the record

    unique = turn(1, "call_a") + turn(2, "call_b")
    out = replay_trim_rewrites(unique, {"results": ["call_a"]})
    assert out["results"] == 1
    assert str(unique[5].content[0].content).startswith("BODY2")


# --------------------------------------------------------------------------- #
# Review of the replay (2026-11-19): four should-fix findings, each a guard    #
# --------------------------------------------------------------------------- #


def test_two_server_tasks_writing_one_conversation_keep_each_others_clears(monkeypatch) -> None:
    """Two requests on one conversation, on two server tasks: each holds only its own clears in memory. The row's
    ``cache_state.trim_replay`` must end as the UNION — a replacement made the second write erase the first's, and
    the result it had cleared came back whole on the next send (the original bug)."""
    import asyncio

    from matrx_ai.db import persistence

    row: dict[str, Any] = {"cache_state": {send_boundary.TRIM_REPLAY_KEY: {"results": ["call1"]}}}

    class _Conversation:
        async def load_conversation_by_id(self, _cid: str) -> Any:
            return SimpleNamespace(cache_state=dict(row["cache_state"]))

    def _write(_cid: str, **fields: Any) -> None:
        row["cache_state"] = fields["cache_state"]

    monkeypatch.setattr(persistence, "_cxm", lambda: SimpleNamespace(conversation=_Conversation()))
    monkeypatch.setattr(persistence, "_get_live_coordinator", lambda: object())
    monkeypatch.setattr(persistence, "_queue_conversation_update", _write)
    monkeypatch.setattr(send_boundary, "take_context_breakdown", lambda _cid: None)
    rows = [{"provider": "anthropic", "ai_model": "m"}]

    def _task(clears: list[str]) -> dict[str, Any]:
        """One server task's memory after its send: the record it read (``call1``) plus what its own trim cleared."""
        return {"results": ["call1", *clears], "results_after_arguments": [], "arguments": []}

    monkeypatch.setattr(send_boundary, "_TRIM_REPLAY_MEMO", type(send_boundary._TRIM_REPLAY_MEMO)())
    task_a, task_b = _task(["call2"]), _task(["call3"])
    send_boundary._TRIM_REPLAY_MEMO[CONVERSATION] = task_a
    asyncio.run(persistence._refresh_cache_state(CONVERSATION, rows, None))  # task A finishes first
    send_boundary._TRIM_REPLAY_MEMO[CONVERSATION] = task_b  # task B: another process, its own memory
    asyncio.run(persistence._refresh_cache_state(CONVERSATION, rows, None))

    record = row["cache_state"][send_boundary.TRIM_REPLAY_KEY]
    assert set(record["results"]) == {"call1", "call2", "call3"}, record
    assert len(record["results"]) == len(set(record["results"]))


def test_the_record_holds_each_key_once_and_never_outlives_its_block() -> None:
    """Ordered-unique, never a list that duplicates (the record is rewritten into ``cache_state`` every request and
    reaches the client); and a path that records but never replays (loop stage, the wire fit) prunes the record to
    the blocks present when it records — it cannot grow without limit."""
    from matrx_ai.config.context_trim import TrimReport, trim_rewrite_record

    report = TrimReport(rewritten_blocks=[{"tool_use_id": "k2"}, {"tool_use_id": "k2"}, {"block": "tool_call", "call_id": "k3"}, {"block": "tool_call", "call_id": "k3"}])
    record = trim_rewrite_record(report, {"results": ["k1", "k1"], "arguments": ["k0", "k0"]})
    for name, keys in record.items():
        assert len(keys) == len(set(keys)), (name, keys)
    assert record["results"] == ["k1", "k2"] and record["arguments"] == ["k0", "k3"]
    merged = send_boundary._merged_trim_record({"results": ["a", "b", "a"]}, {"results": ["b", "c"]})
    assert merged["results"] == ["a", "b", "c"]

    send_boundary._TRIM_REPLAY_MEMO.pop(CONVERSATION, None)
    send_boundary._TRIM_REPLAY_DROPPED.pop(CONVERSATION, None)
    try:
        for i in range(1, 30):  # a long loop: each round's trim clears one result; the window keeps three turns
            live = [m for j in range(max(1, i - 2), i + 1) for m in _turn(j)]
            send_boundary._remember_trim_rewrites(CONVERSATION, TrimReport(rewritten_blocks=[{"tool_use_id": f"call{i}"}]), live)
        kept = send_boundary.remembered_trim_replay(CONVERSATION)
        assert kept["results"] == ["call27", "call28", "call29"], kept
        # And persistence's merge subtracts what this process let go: an old row never brings it back.
        old_row = {send_boundary.TRIM_REPLAY_KEY: {"results": ["call1", "call2"]}}
        written = send_boundary.persisted_prefix_state(CONVERSATION, old_row)[send_boundary.TRIM_REPLAY_KEY]
        assert written["results"] == ["call27", "call28", "call29"], written
    finally:
        send_boundary._TRIM_REPLAY_MEMO.pop(CONVERSATION, None)
        send_boundary._TRIM_REPLAY_DROPPED.pop(CONVERSATION, None)


@pytest.mark.asyncio
async def test_a_send_at_270_of_300_seconds_holds_the_prefix(staff_thread) -> None:
    """THE ONE warm/cold test: the payback gate calls a cache cold only at age >= the full TTL; the window and the
    stale markers used ``0.8 x TTL`` — so at 270 s of a 300 s cache the window moved its cut (and the markers) on a
    cache that was still live, and the whole history was written again."""
    payback = TrimPolicy(cache_gate_mode="payback", cache_gate_min_saved_tokens=10**9)  # unpriced → floor holds
    cold, _ = await _ask(8, state=_state(age=timedelta(hours=3)), policy=payback)
    persisted = _state(age=timedelta(seconds=270), previous=_state(age=timedelta(hours=3)))
    warm, cut = await _ask(9, state=persisted, policy=payback)
    assert cut["prefix"]["cache"] == "warm", cut["prefix"]
    assert cut["prefix"]["action"] == "held", cut["prefix"]
    assert warm[: len(cold)] == cold


def _forced_case(monkeypatch, windows: dict[str, int]) -> tuple[Any, Any]:
    """A thread whose first send ran on a small-window model and was forced to clear results to fit."""
    from matrx_ai.config import context_preflight

    monkeypatch.setattr(context_preflight, "_declared_window", lambda ref: windows.get(ref))
    monkeypatch.setattr(send_boundary, "model_cache_prices", lambda *a, **k: None)
    for memo in ("_TRIM_REPLAY_MEMO", "_TRIM_REPLAY_DROPPED", "_CACHE_STATE_MEMO"):
        if hasattr(send_boundary, memo):  # ``_TRIM_REPLAY_DROPPED`` is absent before the fix
            monkeypatch.setattr(send_boundary, memo, type(getattr(send_boundary, memo))())

    def config(model: str, turns: int = 6) -> Any:
        return SimpleNamespace(messages=[m for i in range(1, turns + 1) for m in _turn(i)], model=model)

    small = config("small")
    forced = TrimPolicy(tier_1_min_positions_back=2, tier_1_min_output_chars=400, tier_2_min_positions_back=2, tier_2_min_output_chars=400)
    import inspect

    takes_config = len(inspect.signature(send_boundary._forced_trim_for).parameters) > 1  # one arg before the fix
    make = send_boundary._forced_trim_for(CONVERSATION, small) if takes_config else send_boundary._forced_trim_for(CONVERSATION)
    report = make(small.messages, forced)
    assert report.blocks_rewritten >= 1
    return config, report


def _cleared(config: Any) -> int:
    return sum(
        1 for m in config.messages for b in m.content if isinstance(getattr(b, "content", None), str) and "[tool result cleared]" in b.content
    )


@pytest.mark.parametrize(
    "model, age, replayed",
    [
        ("large", timedelta(hours=3), False),  # the window grew, the cache is cold: restored, honestly cold
        ("large", timedelta(minutes=2), True),  # grew, but warm: replayed — the warm send only appends
        ("small", timedelta(hours=3), True),  # cold, but the same limit still binds: replayed
    ],
)
def test_a_forced_clear_lives_only_while_its_limit_binds_or_the_cache_is_warm(monkeypatch, model, age, replayed) -> None:
    config_for, report = _forced_case(monkeypatch, {"small": 16_000, "large": 1_000_000})
    persisted = {
        "last_response_at": (datetime.now(UTC) - age).isoformat(),
        "est_cache_ttl_secs": 300,
        **send_boundary.persisted_prefix_state(CONVERSATION),
    }
    send_boundary._TRIM_REPLAY_MEMO.clear()  # the next send lands on another task
    nxt = config_for(model)
    prep = send_boundary.SendPrep(stage=STAGE_RESOLVE)
    send_boundary._replay_trims(prep, nxt, conversation_id=CONVERSATION, cache_state=persisted, policy=TrimPolicy())
    assert (_cleared(nxt) >= report.blocks_rewritten) if replayed else (_cleared(nxt) == 0), _cleared(nxt)
    forced = persisted[send_boundary.TRIM_REPLAY_KEY].get(send_boundary.FORCED_KEY) or {}
    assert forced.get("limit_tokens") == 16_000, "a forced clear is recorded with the limit it was made under"
    if not replayed:
        assert prep.trim_replay["forced_dropped"] >= 1
        # Dropped clears leave the record: the next WARM send must not clear them again behind the cache line.
        later = send_boundary.persisted_prefix_state(CONVERSATION, persisted)[send_boundary.TRIM_REPLAY_KEY]
        assert send_boundary.FORCED_KEY not in later and not later["results"], later
