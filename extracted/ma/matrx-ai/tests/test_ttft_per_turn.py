"""Time-to-first-token is stamped at the provider seam and persisted on EVERY turn.

SUTs: ``send_once`` (the one step every model call crosses) with
``matrx_ai.orchestrator.first_output`` (the stamp, measured from the first
iteration's start — the origin ``total_duration`` uses), and the REAL ``_finalize_and_persist`` →
``build_request_summary`` / ``to_storage_dict`` (``chat.user_request.metadata.
ttft_ms`` and ``timing_stats.first_token_seconds``). Doubled: the send
boundary (``prepare_for_send`` — prompt shaping, DB-backed), the provider
client (it behaves like every real provider: reads ``get_app_context().
emitter`` at call time and streams through it), and the DB sinks.

One test per route class, because the defect this guards was a stamp that
lived on ONE emitter: on 2026-10-05 production recorded ttft_ms on 27/27
agent-route chat turns and on 0 of every other kind — agent-less chat,
ai-results, agent-builder, agent-runner, mandates, batch, the MCP agent
service.

Breaks these tests name:
* the stamp moves back onto an emitter type (a run with a different emitter,
  or none, records nothing);
* a non-streaming / tool-call-only provider reply stops counting as output;
* TTFT and total duration drift onto different clocks (ttft_ms > total_duration_ms
  on 2026-10-06, row e3b39db0: 24842 vs 9254 — TTFT counted pre-execution setup);
* finalize stops carrying the number, or overwrites other metadata keys.
"""

from __future__ import annotations

import asyncio
import time
from types import SimpleNamespace
from typing import Any

import pytest
from matrx_connect.context.app_context import AppContext, set_app_context
from matrx_connect.emitters.console_emitter import ConsoleEmitter
from matrx_connect.emitters.stream_emitter import StreamEmitter
from matrx_connect.request_latency import arm_request_latency, clear_request_latency

import matrx_ai.orchestrator.executor as executor_mod
from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.unified_config import UnifiedResponse
from matrx_ai.orchestrator.execution_state import ExecutionState
from matrx_ai.orchestrator.first_output import turn_ttft_ms
from matrx_ai.orchestrator.requests import AIMatrixRequest
from matrx_ai.orchestrator.send_once import send_once
from matrx_ai.orchestrator.tracking import TimingUsage

_CONVERSATION_ID = "5b0f3c8e-7d0e-4c55-9a51-1f3f0b8f6a21"
_REQUEST_ID = "0e9b6f2a-2b8c-4a8e-8a7e-6d1c4c3b2a10"
_USER_ID = "e4687a9c-acf7-469f-aa12-860eb4d948d0"
_DELAY_S = 0.05


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
            emitter=emitter,  # type: ignore[arg-type]
            user_id=_USER_ID,
            request_id=_REQUEST_ID,
            conversation_id=_CONVERSATION_ID,
            store=True,
            debug=False,
            snapshot=False,
        )
    )


def _request() -> AIMatrixRequest:
    messages = MessageList()
    messages.append_or_extend_user_text("Summarise the quarterly numbers.")
    return AIMatrixRequest(
        conversation_id=_CONVERSATION_ID,
        request_id=_REQUEST_ID,
        config=UnifiedConfig(model="gemini-test", messages=messages),
        metadata={"source": "chat", "client_trace": "keep-me"},
    )


def _response() -> UnifiedResponse:
    return UnifiedResponse(
        messages=[UnifiedMessage(role="assistant", content=[TextContent(text="Revenue rose.")])],
        usage=None,
        finish_reason="stop",
    )


class _Provider:
    """Behaves like a real provider: reads the context emitter at call time."""

    def __init__(self, *, wait_s: float = 0.0, stream: list[tuple[str, str]] | None = None):
        self.wait_s = wait_s
        self.stream = stream or []

    async def execute(self, _request: Any) -> UnifiedResponse:
        from matrx_connect.context.app_context import get_app_context

        emitter = get_app_context().emitter
        await asyncio.sleep(self.wait_s)
        for kind, text in self.stream:
            if emitter is None:
                continue
            if kind == "r":
                await emitter.send_reasoning_chunk(text)
            else:
                await emitter.send_chunk(text)
            await asyncio.sleep(0.02)
        return _response()


async def _iteration(
    request: AIMatrixRequest, provider: Any, state: ExecutionState, *, tool_s: float = 0.0
) -> None:
    """One executor iteration: the same TimingUsage bracket the loop uses."""
    timing = TimingUsage(start_time=time.time(), iteration=len(request.timing_history) + 1)
    try:
        await send_once(provider, request, state=state, iteration=timing.iteration)
        await asyncio.sleep(tool_s)  # tool execution inside the iteration
    finally:
        timing.end_time = time.time()
        request.add_timing(timing)


async def _finalize(
    monkeypatch: pytest.MonkeyPatch, state: ExecutionState, request: AIMatrixRequest
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
        _response(),
        {"finish_reason": "stop"},
        0,
        len(request.config.messages),
        conversation_id=_CONVERSATION_ID,
        state=state,
    )
    return captured["completed"]


def _assert_persisted(completed: Any, at_least_ms: int) -> int:
    ttft_ms = completed.metadata["ttft_ms"]
    assert isinstance(ttft_ms, int) and ttft_ms >= at_least_ms
    # ONE origin: ttft can never exceed the turn's total duration.
    summary = completed.build_request_summary()
    assert ttft_ms <= summary["total_duration_ms"], (ttft_ms, summary["total_duration_ms"])
    assert completed.timing_stats["first_token_seconds"] == pytest.approx(ttft_ms / 1000)
    meta = completed.to_storage_dict()["user_request"]["metadata"]
    assert meta["ttft_ms"] == ttft_ms
    assert meta["client_trace"] == "keep-me"  # merged, never overwritten
    return ttft_ms


# ---------------------------------------------------------------------------
# One per route class
# ---------------------------------------------------------------------------


async def test_agentless_v2_chat_streaming_text(monkeypatch: pytest.MonkeyPatch) -> None:
    arm_request_latency(path="/ai/chat")
    _use(StreamEmitter())
    await asyncio.sleep(_DELAY_S)  # route prep BEFORE the execution: not counted
    state, request = ExecutionState(), _request()
    await _iteration(request, _Provider(wait_s=0.03, stream=[("c", "Rev"), ("c", "enue")]), state)
    ttft = _assert_persisted(await _finalize(monkeypatch, state, request), at_least_ms=30)
    assert ttft < _DELAY_S * 1000 + 30  # the pre-execution setup is excluded


async def test_reasoning_delta_counts_as_first_output(monkeypatch: pytest.MonkeyPatch) -> None:
    _use(StreamEmitter())
    state, request = ExecutionState(), _request()
    await _iteration(request, _Provider(stream=[("r", "Thinking"), ("c", "Answer")]), state)
    ttft = turn_ttft_ms(state, request.timing_history)
    assert ttft is not None and ttft < 15  # before the 20ms gap to the text
    completed = await _finalize(monkeypatch, state, request)
    assert completed.metadata["ttft_ms"] == ttft


async def test_manual_builder_non_streaming_provider_stamps_at_receipt(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    arm_request_latency(path="/ai/manual")
    _use(ConsoleEmitter("builder", accumulate=False))
    state, request = ExecutionState(), _request()
    await _iteration(request, _Provider(wait_s=_DELAY_S), state)  # nothing streamed
    _assert_persisted(
        await _finalize(monkeypatch, state, request), at_least_ms=int(_DELAY_S * 1000)
    )


async def test_no_emitter_mandate_run(monkeypatch: pytest.MonkeyPatch) -> None:
    """A mandate / batch / MCP run: no HTTP request armed, no emitter at all."""
    _use(None)
    state, request = ExecutionState(), _request()
    await _iteration(request, _Provider(wait_s=_DELAY_S, stream=[("c", "no emitter")]), state)
    _assert_persisted(
        await _finalize(monkeypatch, state, request), at_least_ms=int(_DELAY_S * 1000)
    )


async def test_tool_call_first_turn(monkeypatch: pytest.MonkeyPatch) -> None:
    arm_request_latency(path="/ai/agents/a1")
    _use(StreamEmitter())
    state, request = ExecutionState(), _request()
    await _iteration(request, _Provider(wait_s=_DELAY_S), state, tool_s=0.03)  # tool call only
    first = state.ttft_first_output_at
    await _iteration(request, _Provider(stream=[("c", "Answer after the tool")]), state)
    assert state.ttft_first_output_at == first  # the turn's FIRST output stands
    _assert_persisted(
        await _finalize(monkeypatch, state, request), at_least_ms=int(_DELAY_S * 1000)
    )


# ---------------------------------------------------------------------------
# Edges
# ---------------------------------------------------------------------------


async def test_failed_call_records_nothing(monkeypatch: pytest.MonkeyPatch) -> None:
    class _Failing:
        async def execute(self, _r: Any) -> Any:
            raise RuntimeError("provider down")

    _use(StreamEmitter())
    state, request = ExecutionState(), _request()
    with pytest.raises(RuntimeError):
        await _iteration(request, _Failing(), state)
    completed = await _finalize(monkeypatch, state, request)
    assert "ttft_ms" not in completed.metadata
    assert "first_token_seconds" not in completed.timing_stats


async def test_the_watcher_is_removed_after_the_call() -> None:
    from matrx_connect.context.app_context import get_app_context

    emitter = StreamEmitter()
    _use(emitter)
    await _iteration(_request(), _Provider(stream=[("c", "x")]), ExecutionState())
    assert get_app_context().emitter is emitter
