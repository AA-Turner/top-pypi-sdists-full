"""A token-limit truncation is flagged, captured, and persisted as truncated.

SUTs: ``_execute_until_complete_inner`` (the provider-response branch: finish
reason classification → structured capture → partial-turn append → finalize
with ``status="truncated"``) and ``_capture_truncated_response`` (the bounded
``system_error`` row). Doubles replace only what the loop CALLS: the provider
client (returns a recorded-shape ``UnifiedResponse``), the DB gates, the
durable persistence sink (``_finalize_and_persist`` — we read the metadata the
loop hands it), the DB-backed turn-boundary inbox drain, and ``capture_error``
(the system_error writer).

Breaks these tests name:
* truncation treated as a clean completion (classifier, enum, or branch) —
  the partial answer is persisted as if whole and no alarm row lands;
* the loop skips the capture call — the counter the alarm reads never moves;
* the finalize metadata stops saying ``truncated`` — persistence records a
  cut-off answer as completed;
* the capture row's kind drifts from the literal the consumer counts by, or
  loses the request/user/conversation identity, or starts retaining content.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

import matrx_ai.orchestrator.executor as executor_mod
from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.finish_reason import FinishReason
from matrx_ai.config.unified_config import UnifiedResponse
from matrx_ai.config.usage_config import TokenUsage
from matrx_ai.orchestrator.execution_state import ExecutionState
from matrx_ai.orchestrator.requests import AIMatrixRequest

# The literal the consumer (aidream snapshot_retention capture health / the
# system_error alarm) counts rows by. Never import it from the SUT: a drifted
# constant would then agree with itself while every alarm goes dark.
_TRUNCATED_KIND = "provider_response_truncated"

_CONVERSATION_ID = "33c2198e-e068-463d-831e-995f78a794ab"
_REQUEST_ID = "79e68e55-e1d8-4de5-b15f-585587d57b02"
_USER_ID = "e4687a9c-acf7-469f-aa12-860eb4d948d0"
_PARTIAL_TEXT = "Here are the first three steps of the migration: 1. Snapshot the"


class _RecordingEmitter:
    def __init__(self) -> None:
        self.warnings: list[Any] = []

    async def send_warning(self, payload: Any, *a: Any, **k: Any) -> None:
        self.warnings.append(payload)

    def reset_turn_text(self) -> None:
        return None

    def get_turn_text(self) -> str:
        return ""

    def __getattr__(self, name: str) -> Any:
        async def _noop(*a: Any, **k: Any) -> None:
            return None

        return _noop


class _StubTracker:
    async def reserve(self, *a: Any, **k: Any) -> None:
        return None

    async def mark_active(self, *a: Any, **k: Any) -> None:
        return None

    def register_existing(self, *a: Any, **k: Any) -> None:
        return None


def _app_context(emitter: _RecordingEmitter) -> AppContext:
    return AppContext(
        emitter=emitter,  # type: ignore[arg-type]
        user_id=_USER_ID,
        request_id=_REQUEST_ID,
        conversation_id=_CONVERSATION_ID,
        store=True,
        debug=False,
        snapshot=False,
    )


class _OneResponseClient:
    def __init__(self, response: UnifiedResponse) -> None:
        self.response = response
        self.calls = 0

    async def execute(self, *a: Any, **k: Any) -> UnifiedResponse:
        self.calls += 1
        return self.response


def _usage() -> TokenUsage:
    return TokenUsage(
        input_tokens=1200,
        output_tokens=321,
        matrx_model_name="gemini-test",
        provider_model_name="gemini-test",
        api="google",
    )


def _provider_response(finish_reason: str, usage: TokenUsage | None) -> UnifiedResponse:
    return UnifiedResponse(
        messages=[
            UnifiedMessage(role="assistant", content=[TextContent(text=_PARTIAL_TEXT)])
        ],
        usage=usage,
        finish_reason=finish_reason,
    )


def _request() -> AIMatrixRequest:
    messages = MessageList()
    messages.append_or_extend_user_text("Write the full migration runbook.")
    return AIMatrixRequest(
        conversation_id=_CONVERSATION_ID,
        request_id=_REQUEST_ID,
        config=UnifiedConfig(model="gemini-test", messages=messages, max_output_tokens=321),
    )


async def _run_one_turn(
    monkeypatch: pytest.MonkeyPatch,
    finish_reason: str,
    *,
    usage: TokenUsage | None = None,
    with_usage: bool = True,
) -> dict[str, Any]:
    captured: list[dict[str, Any]] = []
    finalized: list[dict[str, Any]] = []
    emitter = _RecordingEmitter()

    async def capture_error(exc: BaseException, **kwargs: Any) -> None:
        captured.append({"exc": exc, **kwargs})

    async def finalize(**kwargs: Any) -> str:
        finalized.append(kwargs)
        return "completed-request"

    async def _noop_async(*a: Any, **k: Any) -> None:
        return None

    monkeypatch.setattr("matrx_connect.streaming.error_capture.capture_error", capture_error)
    monkeypatch.setattr(executor_mod, "_finalize_and_persist", finalize)
    monkeypatch.setattr(executor_mod, "ensure_conversation_exists", _noop_async)
    monkeypatch.setattr(executor_mod, "ensure_user_request_exists", _noop_async)
    monkeypatch.setattr(executor_mod, "get_tracker", lambda: _StubTracker())

    async def _empty_turn_boundary_inbox(config: Any, app_ctx: Any) -> Any:
        return app_ctx  # DB-backed inbox (cx_pending_injection): nothing pending

    monkeypatch.setattr(
        "matrx_ai.tools.dynamic_drain.drain_pending", _empty_turn_boundary_inbox
    )
    ctx = _app_context(emitter)
    monkeypatch.setattr(executor_mod, "get_app_context", lambda: ctx)

    client = _OneResponseClient(
        _provider_response(finish_reason, (usage or _usage()) if with_usage else None)
    )
    token = set_app_context(ctx)
    try:
        result = await executor_mod._execute_until_complete_inner(
            exec_ctx=ctx,
            state=ExecutionState(),
            initial_request=_request(),
            client=client,
            max_iterations=1,
            max_retries_per_iteration=0,
        )
    finally:
        clear_app_context(token)
    return {
        "result": result,
        "client": client,
        "captured": captured,
        "finalized": finalized,
        "warnings": emitter.warnings,
    }


# Each provider's native token-limit signal, normalized through the real enum
# mappers the provider translators use.
_TRUNCATION_SIGNALS = [
    pytest.param(str(FinishReason.from_anthropic("max_tokens")), id="anthropic-max_tokens"),
    pytest.param(str(FinishReason.from_google("FinishReason.MAX_TOKENS")), id="google-MAX_TOKENS"),
    pytest.param("max_tokens", id="unified-string"),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("finish_reason", _TRUNCATION_SIGNALS)
async def test_truncated_turn_is_finalized_as_truncated_not_completed(
    monkeypatch: pytest.MonkeyPatch, finish_reason: str
) -> None:
    run = await _run_one_turn(monkeypatch, finish_reason)

    assert run["client"].calls == 1
    assert len(run["finalized"]) == 1, "the truncated turn must finalize exactly once"
    final = run["finalized"][0]
    assert final["metadata"] == {
        "status": "truncated",
        "finish_reason": "max_tokens",
        "error": (
            "Response truncated: model hit the output token limit "
            "(model=gemini-test, max_output_tokens=321)"
        ),
        "error_type": "truncated_response",
    }
    # The partial text the user already saw is appended so persistence keeps it.
    last = final["current_request"].config.messages[-1]
    assert last.role == "assistant"
    assert [block.text for block in last.content] == [_PARTIAL_TEXT]
    assert run["result"] == "completed-request"


@pytest.mark.asyncio
@pytest.mark.parametrize("finish_reason", _TRUNCATION_SIGNALS)
async def test_truncated_turn_lands_one_structured_capture_row(
    monkeypatch: pytest.MonkeyPatch, finish_reason: str
) -> None:
    run = await _run_one_turn(monkeypatch, finish_reason)

    truncations = [row for row in run["captured"] if row["kind"] == _TRUNCATED_KIND]
    assert len(truncations) == 1, (
        f"expected exactly one {_TRUNCATED_KIND} row, got kinds "
        f"{[row['kind'] for row in run['captured']]}"
    )
    assert [w.code for w in run["warnings"]] == ["truncated_response"]


@pytest.mark.asyncio
async def test_clean_stop_is_not_flagged_truncated(monkeypatch: pytest.MonkeyPatch) -> None:
    """Control: the same harness with a clean finish never takes the branch."""
    run = await _run_one_turn(monkeypatch, "stop")

    assert [row for row in run["captured"] if row["kind"] == _TRUNCATED_KIND] == []
    assert all(
        (f.get("metadata") or {}).get("status") != "truncated" for f in run["finalized"]
    )
    assert all(getattr(w, "code", None) != "truncated_response" for w in run["warnings"])


@pytest.mark.asyncio
async def test_capture_row_is_bounded_identified_and_content_free(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: list[dict[str, Any]] = []

    async def capture_error(exc: BaseException, **kwargs: Any) -> None:
        captured.append({"exc": exc, **kwargs})

    monkeypatch.setattr("matrx_connect.streaming.error_capture.capture_error", capture_error)

    await executor_mod._capture_truncated_response(
        exec_ctx=SimpleNamespace(user_id=_USER_ID),
        current_request=_request(),
        iteration=4,
    )

    assert len(captured) == 1
    row = captured[0]
    assert isinstance(row["exc"], RuntimeError)
    assert str(row["exc"]) == "Model 'gemini-test' reached its output token limit"
    assert {k: v for k, v in row.items() if k != "exc"} == {
        "kind": _TRUNCATED_KIND,
        "request_id": _REQUEST_ID,
        "user_id": _USER_ID,
        "conversation_id": _CONVERSATION_ID,
        "route": "orchestrator/provider_response",
        "error_type": "truncated_response",
        "payload": {"model": "gemini-test", "max_output_tokens": 321, "iteration": 4},
    }


@pytest.mark.asyncio
async def test_usage_less_response_on_a_run_without_snapshots_is_captured_not_crashed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Defect found 2026-09-10 by this suite: the missing-usage capture read
    ``snap_provider``, which is only bound when request snapshots are enabled.
    A provider response without usage on a ``snapshot=False`` / ``store=False``
    run raised UnboundLocalError and the turn finalized as a matrx internal
    error — the answer the user already saw was recorded as ``failed`` and the
    missing-usage alarm row never landed."""
    run = await _run_one_turn(monkeypatch, "max_tokens", with_usage=False)

    assert [row["kind"] for row in run["captured"]] == [
        "provider_usage_missing",
        _TRUNCATED_KIND,
    ]
    assert run["captured"][0]["payload"] == {
        "provider": "unknown",
        "model": "gemini-test",
        "iteration": 1,
    }
    assert [f["metadata"]["status"] for f in run["finalized"]] == ["truncated"]
