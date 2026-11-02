from __future__ import annotations

import pytest
from matrx_connect.context.events import WarningPayload
from matrx_connect.context.operations import CompletionPayload
from matrx_connect.emitters import stream_emitter
from matrx_connect.emitters.stream_emitter import StreamEmitter


@pytest.mark.asyncio
async def test_routine_events_are_quiet_when_debug_is_false(monkeypatch) -> None:
    calls: list[tuple[object, str, bool | None]] = []

    def fake_vcprint(data=None, title="Unnamed Data", **kwargs) -> None:
        calls.append((data, title, kwargs.get("verbose")))

    monkeypatch.setattr(stream_emitter, "vcprint", fake_vcprint)

    emitter = StreamEmitter(debug=False)
    await emitter.send_completion(
        CompletionPayload(
            operation="sub_agent",
            operation_id="op-1",
            status="failed",
        )
    )

    assert calls == [
        (
            {"operation": "sub_agent", "operation_id": "op-1", "status": "failed"},
            "[Stream Emitter] Completion",
            False,
        )
    ]


@pytest.mark.asyncio
async def test_warning_events_still_log_when_debug_is_false(monkeypatch) -> None:
    calls: list[tuple[object, str, bool | None]] = []

    def fake_vcprint(data=None, title="Unnamed Data", **kwargs) -> None:
        calls.append((data, title, kwargs.get("verbose")))

    monkeypatch.setattr(stream_emitter, "vcprint", fake_vcprint)

    emitter = StreamEmitter(debug=False)
    await emitter.send_warning(
        WarningPayload(
            code="provider_busy",
            system_message="Provider is temporarily busy.",
        )
    )

    assert calls == [
        (
            {
                "code": "provider_busy",
                "level": "medium",
                "message": "Provider is temporarily busy.",
            },
            "[Stream Emitter] Warning",
            None,
        )
    ]


@pytest.mark.asyncio
async def test_stream_emitter_suppresses_duplicate_terminal_errors(capsys) -> None:
    emitter = StreamEmitter(debug=False)

    await emitter.send_error("first_failure", "first")
    await emitter.send_error("duplicate_failure", "duplicate")

    queued = []
    while not emitter.queue.empty():
        queued.append(emitter.queue.get_nowait())
    assert len(queued) == 1
    assert emitter._error_guard.duplicate_count == 1
    stderr = capsys.readouterr().err
    assert "DUPLICATE ERROR SUPPRESSED" in stderr
    assert "duplicate_failure" in stderr
