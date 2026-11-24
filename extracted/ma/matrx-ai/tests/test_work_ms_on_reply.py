"""WORKED FOR is recorded ONCE, by the server, on the reply row: ``chat.message.metadata.work_ms``.

"Worked for" means the time from the person's send until the answer began (CGU-09 lane C4
ruling). A client measuring between saved row timestamps read "Worked for 1s" over a 35 s turn:
the server writes the question row, the reply row and ``chat.user_request`` within about a second
at the turn's end. So the server stamps it from its own clock at the first answer text.

SUTs: ``send_once`` + ``matrx_ai.orchestrator.first_output`` (the stamp, on every model call of the
turn) and the REAL ``_finalize_and_persist`` → ``to_storage_dict`` (the reply message's metadata,
which persistence writes to ``chat.message.metadata``). Doubled: the send boundary, the provider
client (reads ``get_app_context().emitter`` at call time, like every real provider), the DB sinks.

Breaks these tests name: work_ms measured to the FIRST output (thinking, or an aside before a tool)
instead of the answer; the stamp missing from the reply row; a guessed number on a turn with no answer.
"""

from __future__ import annotations

import asyncio
import time
from types import SimpleNamespace
from typing import Any

import pytest
from matrx_connect.context.app_context import AppContext, set_app_context
from matrx_connect.emitters.stream_emitter import StreamEmitter
from matrx_connect.request_latency import arm_request_latency, clear_request_latency
from matrx_utils.source_guard import stable_source

import matrx_ai.orchestrator.executor as executor_mod
from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.tools_config import ToolCallContent
from matrx_ai.config.unified_config import UnifiedResponse
from matrx_ai.orchestrator.execution_state import ExecutionState
from matrx_ai.orchestrator.requests import AIMatrixRequest
from matrx_ai.orchestrator.send_once import send_once
from matrx_ai.orchestrator.tracking import TimingUsage

_CONVERSATION_ID = "5b0f3c8e-7d0e-4c55-9a51-1f3f0b8f6a21"
_REQUEST_ID = "0e9b6f2a-2b8c-4a8e-8a7e-6d1c4c3b2a10"
_USER_ID = "e4687a9c-acf7-469f-aa12-860eb4d948d0"


@pytest.fixture(autouse=True)
def _no_request() -> Any:
    clear_request_latency()
    yield
    clear_request_latency()


@pytest.fixture(autouse=True)
def _boundary_doubled(monkeypatch: pytest.MonkeyPatch) -> None:
    async def _prep(*_a: Any, **_k: Any) -> Any:
        return SimpleNamespace(wire_config=None)

    monkeypatch.setattr("matrx_ai.config.send_boundary.prepare_for_send", _prep)
    monkeypatch.setattr("matrx_ai.mandate_taps.observe_first_send", lambda *_a, **_k: None)


def _use(emitter: Any) -> None:
    set_app_context(
        AppContext(
            emitter=emitter,
            user_id=_USER_ID,
            request_id=_REQUEST_ID,  # type: ignore[arg-type]
            conversation_id=_CONVERSATION_ID,
            store=True,
            debug=False,
            snapshot=False,
        )
    )


def _request() -> AIMatrixRequest:
    messages = MessageList()
    messages.append_or_extend_user_text("Summarize the quarterly numbers.")
    return AIMatrixRequest(
        conversation_id=_CONVERSATION_ID,
        request_id=_REQUEST_ID,
        config=UnifiedConfig(model="gemini-test", messages=messages),
        metadata={"source": "chat"},
    )


async def _iteration(request: AIMatrixRequest, provider: Any, state: ExecutionState, *, tool_s: float = 0.0) -> None:
    """One executor iteration as the loop runs it: the TimingUsage bracket, ``send_once``, then the REAL
    ``_stamp_answer_notes`` on the call's answers — where the loop stamps them, BEFORE the mid-turn commit writes the
    row (the final persist only writes rows past ``committed_position``)."""
    timing = TimingUsage(start_time=time.time(), iteration=len(request.timing_history) + 1)
    try:
        sent = await send_once(provider, request, state=state, iteration=timing.iteration)
        executor_mod._stamp_answer_notes(
            sent.response.messages, timing.iteration, None, state=state,
            timing_history=[*request.timing_history, timing],
        )
        await asyncio.sleep(tool_s)  # tool execution inside the iteration
    finally:
        timing.end_time = time.time()
        request.add_timing(timing)


def _reply(*, tool: bool = False, text: str = "Revenue rose.") -> UnifiedResponse:
    content: list[Any] = [TextContent(text=text)] if text else []
    if tool:
        content.append(ToolCallContent(id="call_1", name="web_search", arguments={"q": "revenue"}))
    return UnifiedResponse(
        messages=[
            UnifiedMessage(role="assistant", content=content, metadata={"provider_iteration": 1})
        ],
        usage=None,
        finish_reason="tool_calls" if tool else "stop",
    )


class _Provider:
    def __init__(
        self,
        response: UnifiedResponse,
        *,
        wait_s: float = 0.0,
        stream: list[tuple[str, str]] | None = None,
    ):
        self.response, self.wait_s, self.stream = response, wait_s, stream or []

    async def execute(self, _request: Any) -> UnifiedResponse:
        from matrx_connect.context.app_context import get_app_context

        emitter = get_app_context().emitter
        await asyncio.sleep(self.wait_s)
        for kind, text in self.stream:
            await asyncio.sleep(0.03)
            if kind == "r":
                await emitter.send_reasoning_chunk(text)
            else:
                await emitter.send_chunk(text)
        return self.response


async def _turn(
    request: AIMatrixRequest, state: ExecutionState, *calls: tuple[_Provider, float]
) -> None:
    for provider, tool_s in calls:
        await _iteration(request, provider, state, tool_s=tool_s)
        for message in provider.response.messages:
            request.config.messages.append(message)


async def _finalize(
    monkeypatch: pytest.MonkeyPatch, state: ExecutionState, request: AIMatrixRequest, *, pre: int
) -> Any:
    captured: dict[str, Any] = {}

    async def _record(completed: Any, **_k: Any) -> dict[str, Any]:
        captured["completed"] = completed
        return {}

    async def _noop(*_a: Any, **_k: Any) -> None:
        return None

    async def _not_shifted(*_a: Any, **_k: Any) -> bool:
        return False

    monkeypatch.setattr(executor_mod, "persist_completed_request", _record)
    monkeypatch.setattr(executor_mod, "_scream_if_history_shifted", _not_shifted)
    monkeypatch.setattr(executor_mod, "_apply_turn_directives", _noop)
    monkeypatch.setattr("matrx_ai.config.usage_config.ensure_pricing_lookup", _noop)
    monkeypatch.setattr("matrx_ai.persistence.queue_helpers.get_coordinator", lambda: None)
    await executor_mod._finalize_and_persist(
        request,
        1,
        _reply(),
        {"finish_reason": "stop"},
        0,
        pre,
        conversation_id=request.conversation_id,
        state=state,
    )
    return captured["completed"]


def _reply_meta(completed: Any) -> dict[str, Any]:
    rows = completed.to_storage_dict()["messages"]
    replies = [r for r in rows if r["role"] == "assistant"]
    return replies[-1].get("metadata") or {}


async def test_work_ms_runs_from_send_to_the_answers_first_text(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    arm_request_latency(path="/ai/chat")
    sent = time.time()
    _use(StreamEmitter())
    await asyncio.sleep(0.05)  # server prep before the model: the person is waiting, it counts
    state, request = ExecutionState(), _request()
    provider = _Provider(
        _reply(),
        wait_s=0.02,
        stream=[("r", "Thinking"), ("r", " more"), ("c", "Rev"), ("c", "enue")],
    )
    await _turn(request, state, (provider, 0.0))
    completed = await _finalize(monkeypatch, state, request, pre=1)
    work_ms = _reply_meta(completed)["work_ms"]
    # Thinking (~0.08 s) is work; prep (0.05 s) is waiting the person sees: both inside, nothing past the answer's start.
    elapsed_to_text_ms = (state.answer_began_at - sent) * 1000
    assert abs(work_ms - elapsed_to_text_ms) <= 5, (work_ms, elapsed_to_text_ms)
    assert work_ms >= 50 + 20 + 3 * 30 - 5
    assert work_ms < completed.build_request_summary()["total_duration_ms"] + 60
    # The whole turn ran longer than the work: the answer streamed after it began.
    ttft = completed.metadata["ttft_ms"]
    assert work_ms > ttft


async def test_an_aside_before_a_tool_is_work_not_the_answer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    arm_request_latency(path="/ai/chat")
    sent = time.time()
    _use(StreamEmitter())
    state, request = ExecutionState(), _request()
    first = _Provider(
        _reply(tool=True, text="Let me look that up."), stream=[("c", "Let me look that up.")]
    )
    second = _Provider(_reply(), wait_s=0.04, stream=[("c", "Revenue rose.")])
    await _turn(request, state, (first, 0.1), (second, 0.0))
    completed = await _finalize(monkeypatch, state, request, pre=1)
    work_ms = _reply_meta(completed)["work_ms"]
    # The aside streamed at ~30 ms; the answer at ~30 + 100 (tool) + 40 + 30 ms.
    assert work_ms >= 190, work_ms
    assert abs(work_ms - (state.answer_began_at - sent) * 1000) <= 5


async def test_a_non_streaming_reply_began_when_it_arrived(monkeypatch: pytest.MonkeyPatch) -> None:
    _use(StreamEmitter())  # no request clock: the origin is the first model call's start
    state, request = ExecutionState(), _request()
    await _turn(request, state, (_Provider(_reply(), wait_s=0.06), 0.0))
    completed = await _finalize(monkeypatch, state, request, pre=1)
    assert 60 <= _reply_meta(completed)["work_ms"] < 200


async def test_a_turn_with_no_answer_text_records_no_number(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    arm_request_latency(path="/ai/chat")
    _use(StreamEmitter())
    state, request = ExecutionState(), _request()
    await _turn(request, state, (_Provider(_reply(tool=True, text=""), wait_s=0.02), 0.0))
    completed = await _finalize(monkeypatch, state, request, pre=1)
    assert "work_ms" not in _reply_meta(completed)
    clear_request_latency()


def test_the_loop_stamps_each_call_before_its_row_is_committed() -> None:
    """The loop's own call hands the stamper the turn's state: a reply row is committed mid-turn, and the final persist
    writes only rows past ``committed_position`` — a stamp taken at finalize never reached chat.message (live 2026-11-09,
    conversation 974ebd49: provider_iteration on the reply, no work_ms)."""

    source = stable_source(executor_mod)
    loop_calls = [c for c in source.split("_stamp_answer_notes(")[1:] if c.lstrip().startswith("api_response.messages")]
    assert loop_calls, "the loop stamps each provider call's answers"
    assert all("state=state" in call.split(")")[0] for call in loop_calls), "with the turn's state (answer_began_at)"


# ── WORKED FOR ACROSS STREAMS ─────────────────────────────────────────────────────────────────────
# A turn that calls a device tool (the browser agent's clicks) ends its stream and resumes as a NEW
# request on the SAME user request, once per step. Measured from the resume's arrival, "Worked for"
# was the last stream alone: conversation bf84b149 / user request f2b7b064 (2026-11-13), a 100-call,
# ~12-minute browser turn stored work_ms 10886 and read "Worked for 11s" after a reload. The origin of
# a continued turn is the person's send; the device's time is work; the person's answering time is not.


class _TurnClockReader:
    """``cxm.user_request.turn_clock`` doubled: the saved user request and its person-ask spans."""

    def __init__(self, sent: float, waits: list[tuple[float, float | None]]) -> None:
        from datetime import UTC, datetime

        self._dt = lambda t: datetime.fromtimestamp(t, UTC)
        self.sent, self.waits, self.asked_for = sent, waits, None

    async def turn_clock(self, user_request_id: str, *, person_ask_tools: frozenset[str]) -> Any:
        self.asked_for = (user_request_id, person_ask_tools)
        return self._dt(self.sent), [(self._dt(s), self._dt(e) if e is not None else None) for s, e in self.waits]


def _saved_turn(monkeypatch: pytest.MonkeyPatch, reader: _TurnClockReader) -> None:
    monkeypatch.setattr(
        "matrx_ai.db.cx_managers.cxm", SimpleNamespace(user_request=reader), raising=False
    )


async def test_a_resumed_turn_works_from_the_persons_send_not_the_resume(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_ai.orchestrator.first_output import load_turn_clock

    sent = time.time() - 600.0  # the person sent 10 minutes ago; device steps ran since
    reader = _TurnClockReader(sent, [])
    _saved_turn(monkeypatch, reader)
    arm_request_latency(path="/ai/chat")  # THIS request: the last resume, arriving now
    _use(StreamEmitter())
    state, request = ExecutionState(), _request()
    await load_turn_clock(state, _REQUEST_ID)
    await _turn(request, state, (_Provider(_reply(), wait_s=0.02, stream=[("c", "Done.")]), 0.0))
    completed = await _finalize(monkeypatch, state, request, pre=1)
    work_ms = _reply_meta(completed)["work_ms"]
    assert reader.asked_for is not None and reader.asked_for[0] == _REQUEST_ID
    assert abs(work_ms - (state.answer_began_at - sent) * 1000) <= 5, work_ms
    assert work_ms >= 600_000, f"measured from the resume, not the send: {work_ms} ms"


async def test_the_persons_answering_time_is_not_work(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_ai.orchestrator.first_output import load_turn_clock

    now = time.time()
    sent = now - 900.0
    # The agent asked at -800 s; the person answered at -200 s (600 s waiting on them). A device
    # step's gap between streams (not an ask) stays inside the work.
    reader = _TurnClockReader(sent, [(now - 800.0, now - 200.0)])
    _saved_turn(monkeypatch, reader)
    arm_request_latency(path="/ai/chat")
    _use(StreamEmitter())
    state, request = ExecutionState(), _request()
    await load_turn_clock(state, _REQUEST_ID)
    await _turn(request, state, (_Provider(_reply(), stream=[("c", "Done.")]), 0.0))
    completed = await _finalize(monkeypatch, state, request, pre=1)
    work_ms = _reply_meta(completed)["work_ms"]
    expected_ms = (state.answer_began_at - sent - 600.0) * 1000
    assert abs(work_ms - expected_ms) <= 5, (work_ms, expected_ms)


async def test_a_fresh_send_keeps_its_own_arrival(monkeypatch: pytest.MonkeyPatch) -> None:
    """A user request created AFTER the arrival (the normal fresh send) never moves the origin later."""
    from matrx_ai.orchestrator.first_output import load_turn_clock

    arm_request_latency(path="/ai/chat")
    arrived = time.time()
    _saved_turn(monkeypatch, _TurnClockReader(arrived + 0.03, []))
    _use(StreamEmitter())
    await asyncio.sleep(0.05)
    state, request = ExecutionState(), _request()
    await load_turn_clock(state, _REQUEST_ID)
    await _turn(request, state, (_Provider(_reply(), stream=[("c", "Done.")]), 0.0))
    completed = await _finalize(monkeypatch, state, request, pre=1)
    assert abs(_reply_meta(completed)["work_ms"] - (state.answer_began_at - arrived) * 1000) <= 5


def test_only_a_continued_turn_reads_the_turn_clock() -> None:
    """The executor reads the saved send for a run whose trigger is a SAVED row (a rebuilt tool result
    after a device step or an answered ask, a saved user row on a reconnect), never for a fresh send."""
    fresh = UnifiedMessage(role="user", content=[TextContent(text="Go.")])
    saved_user = UnifiedMessage(role="user", content=[TextContent(text="Go.")], id="0e9b6f2a-0000-4a8e-8a7e-6d1c4c3b2a10")
    tool_result = UnifiedMessage(role="tool", content=[TextContent(text="clicked")])
    assert executor_mod._is_new_person_message(fresh) is True
    assert executor_mod._is_new_person_message(saved_user) is False
    assert executor_mod._is_new_person_message(tool_result) is False
    source = stable_source(executor_mod)
    assert "if not _is_new_person_message(state.trigger_message):" in source
    assert "state.turn_clock_request_id = str(_request_id)" in source


# ── THE EXTENSION'S `user` TOOL WAITS ON THE PERSON ───────────────────────────────────────────────
# The Browser Agent asks through the extension's `user` tool (tool.definition `user`, executor
# chrome-extension). The server's person-ask list lacked it, so a resumed turn's stored work_ms
# counted the person's answer time while the live clock (tool-cards PERSON_ASK_TOOLS) removed it.


def test_the_extensions_user_tool_is_a_person_ask() -> None:
    from matrx_ai.config.tool_result_guard import PERSON_ASK_TOOLS

    assert "user" in PERSON_ASK_TOOLS


# ── THE TURN CLOCK IS READ LAZILY, ONCE ───────────────────────────────────────────────────────────
# A browser turn is one stream per device step (~100 streams). Reading the saved send and the ask spans
# at every resume cost two DB reads before the first token of each stream; only the stream that stamps
# the answer needs them.


async def test_a_resume_that_only_calls_a_tool_reads_no_turn_clock(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_ai.orchestrator.first_output import ensure_turn_clock

    reader = _TurnClockReader(time.time() - 60.0, [])
    _saved_turn(monkeypatch, reader)
    state = ExecutionState()
    state.turn_clock_request_id = _REQUEST_ID
    await ensure_turn_clock(state)  # no answer began: a device step, not the reply
    assert reader.asked_for is None
    state.answer_began_at = time.time()
    await ensure_turn_clock(state)
    assert reader.asked_for is not None and reader.asked_for[0] == _REQUEST_ID
    reader.asked_for = None
    await ensure_turn_clock(state)  # a second answering call in the same run reads nothing more
    assert reader.asked_for is None
    assert state.turn_sent_at is not None


def test_the_executor_reads_the_turn_clock_only_before_it_stamps() -> None:
    source = stable_source(executor_mod)
    assert "await load_turn_clock(state, str(_request_id))" not in source, "no read before the first token"
    assert "state.turn_clock_request_id = str(_request_id)" in source
    stamp_at = source.index("_stamp_answer_notes(\n                    api_response.messages")
    assert "await ensure_turn_clock(state)" in source[stamp_at - 600 : stamp_at]
