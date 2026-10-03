"""Time-to-first-token is measured by the server and persisted with every turn.

SUTs: ``StreamEmitter`` (the stamp: the FIRST text or reasoning chunk handed to
the wire, measured from the request start the auth middleware armed),
``_turn_ttft_ms`` + ``_finalize_and_persist`` (attribution to THIS execution's
user turn) and ``CompletedRequest.build_request_summary`` /
``to_storage_dict`` (the ``chat.user_request.metadata.ttft_ms`` the persistence
layer writes). Only the DB sinks are doubled: ``persist_completed_request`` is
replaced by a recorder so the test reads exactly the CompletedRequest the
finalize would persist.

Breaks these tests name:
* the emitter stops stamping (or re-stamps on a later chunk) — TTFT disappears
  or measures the last token instead of the first;
* an empty reasoning frame or a control-token-only chunk counts as output;
* the finalize stops carrying the number into metadata / timing_stats, or
  overwrites the caller's own request metadata keys while adding it;
* a run that never emitted output still records a TTFT;
* a later execution on the same stream (or a child agent sharing it) claims
  output an earlier execution emitted.
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest
from matrx_connect.context.app_context import AppContext, set_app_context
from matrx_connect.emitters.stream_emitter import StreamEmitter
from matrx_connect.request_latency import arm_request_latency, clear_request_latency

import matrx_ai.orchestrator.executor as executor_mod
from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.unified_config import UnifiedResponse
from matrx_ai.orchestrator.execution_state import ExecutionState
from matrx_ai.orchestrator.requests import AIMatrixRequest

_CONVERSATION_ID = "5b0f3c8e-7d0e-4c55-9a51-1f3f0b8f6a21"
_REQUEST_ID = "0e9b6f2a-2b8c-4a8e-8a7e-6d1c4c3b2a10"
_USER_ID = "e4687a9c-acf7-469f-aa12-860eb4d948d0"
_DELAY_S = 0.05


@pytest.fixture(autouse=True)
def _armed_request() -> Any:
    arm_request_latency(path="/conversations/turn")
    yield
    clear_request_latency()


def _use(ctx: AppContext) -> None:
    # Each async test runs in its own copied Context, so the AppContext set
    # here dies with the test — no token reset (it would be cross-Context).
    set_app_context(ctx)


def _ctx(emitter: StreamEmitter, *, parent_conversation_id: str | None = None) -> AppContext:
    return AppContext(
        emitter=emitter,  # type: ignore[arg-type]
        user_id=_USER_ID,
        request_id=_REQUEST_ID,
        conversation_id=_CONVERSATION_ID,
        parent_conversation_id=parent_conversation_id,
        store=True,
        debug=False,
        snapshot=False,
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


async def _finalize(monkeypatch: pytest.MonkeyPatch, state: ExecutionState) -> Any:
    """Run the real _finalize_and_persist with only the DB sinks doubled."""
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
    request = _request()
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


# ---------------------------------------------------------------------------
# The stamp
# ---------------------------------------------------------------------------


async def test_first_text_chunk_stamps_ttft_once() -> None:
    emitter = StreamEmitter()
    assert emitter.time_to_first_output_s() is None
    await asyncio.sleep(_DELAY_S)
    await emitter.send_chunk("Hello")
    first = emitter.first_output_at
    ttft = emitter.time_to_first_output_s()
    assert ttft is not None and _DELAY_S <= ttft < 2.0

    await asyncio.sleep(0.02)
    await emitter.send_chunk(" world")
    assert emitter.first_output_at == first  # the FIRST token, never the latest


async def test_reasoning_chunk_counts_as_first_output() -> None:
    emitter = StreamEmitter()
    await emitter.send_reasoning_chunk("")  # an empty frame is not output
    assert emitter.first_output_at is None
    await asyncio.sleep(_DELAY_S)
    await emitter.send_reasoning_chunk("Considering the question")
    reasoning_at = emitter.first_output_at
    assert reasoning_at is not None
    await emitter.send_chunk("Answer")
    assert emitter.first_output_at == reasoning_at


async def test_no_output_means_no_ttft() -> None:
    emitter = StreamEmitter()
    await emitter.send_chunk("")
    assert emitter.first_output_at is None
    assert emitter.time_to_first_output_s() is None


async def test_unarmed_stream_has_no_ttft() -> None:
    clear_request_latency()
    emitter = StreamEmitter()
    await emitter.send_chunk("internal run")
    assert emitter.first_output_at is not None
    assert emitter.time_to_first_output_s() is None


# ---------------------------------------------------------------------------
# Attribution + persistence
# ---------------------------------------------------------------------------


async def test_finalize_persists_ttft_ms_and_timing_stats(monkeypatch: pytest.MonkeyPatch) -> None:
    emitter = StreamEmitter()
    _use(_ctx(emitter))
    state = ExecutionState()
    await asyncio.sleep(_DELAY_S)
    await emitter.send_chunk("Revenue rose.")
    expected_ms = int(round(emitter.time_to_first_output_s() * 1000))  # type: ignore[operator]

    completed = await _finalize(monkeypatch, state)

    assert completed.metadata["ttft_ms"] == expected_ms
    assert expected_ms >= int(_DELAY_S * 1000)
    assert completed.timing_stats["first_token_seconds"] == pytest.approx(expected_ms / 1000)

    summary_meta = completed.build_request_summary()["metadata"]
    assert summary_meta["ttft_ms"] == expected_ms
    # Merge, never overwrite: the caller's own request metadata survives.
    assert summary_meta["source"] == "chat"
    assert summary_meta["client_trace"] == "keep-me"
    assert isinstance(summary_meta["ttft_ms"], int)

    # The row the persistence layer writes (chat.user_request.metadata).
    storage_meta = completed.to_storage_dict()["user_request"]["metadata"]
    assert storage_meta["ttft_ms"] == expected_ms
    assert storage_meta["client_trace"] == "keep-me"


async def test_no_output_writes_nothing(monkeypatch: pytest.MonkeyPatch) -> None:
    emitter = StreamEmitter()
    _use(_ctx(emitter))
    completed = await _finalize(monkeypatch, ExecutionState())
    assert "ttft_ms" not in completed.metadata
    assert "first_token_seconds" not in completed.timing_stats
    assert "ttft_ms" not in completed.build_request_summary()["metadata"]


async def test_later_execution_never_claims_earlier_output(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    emitter = StreamEmitter()
    _use(_ctx(emitter))
    await emitter.send_chunk("first execution's answer")
    await asyncio.sleep(0.002)
    later_state = ExecutionState()  # began after the stream's first output
    completed = await _finalize(monkeypatch, later_state)
    assert "ttft_ms" not in completed.metadata


async def test_child_agent_sharing_the_stream_records_nothing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    emitter = StreamEmitter()
    _use(_ctx(emitter, parent_conversation_id="9a3c1f7e-1111-4c55-9a51-1f3f0b8f6a21"))
    state = ExecutionState()
    await emitter.send_chunk("child text")
    completed = await _finalize(monkeypatch, state)
    assert "ttft_ms" not in completed.metadata


async def test_completion_timing_stats_carry_first_token_seconds(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_connect.context.operations import TimingStatsResult

    emitter = StreamEmitter()
    _use(_ctx(emitter))
    state = ExecutionState()
    await emitter.send_chunk("Revenue rose.")
    completed = await _finalize(monkeypatch, state)
    typed = TimingStatsResult(
        **{k: v for k, v in completed.timing_stats.items() if k in TimingStatsResult.model_fields}
    )
    assert typed.first_token_seconds == pytest.approx(completed.metadata["ttft_ms"] / 1000)
