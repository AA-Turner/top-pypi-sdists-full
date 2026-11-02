"""error_capture injection hook — verifies the universal capture wiring.

The streaming layer calls capture_error() on crash/cancel. When the host
injects a capture coroutine it must be invoked with the right kind +
fields; when nothing is injected it must be a silent no-op; and a failing
capture must never escalate.
"""

from __future__ import annotations

import asyncio

import pytest

from matrx_connect.streaming import error_capture
from matrx_connect.streaming.primitives import text_chunks_to_sse


@pytest.fixture(autouse=True)
def _reset_capture():
    error_capture.configure_error_capture(None)
    yield
    error_capture.configure_error_capture(None)


@pytest.mark.asyncio
async def test_no_op_when_unconfigured():
    # Must not raise when no capture fn is injected.
    await error_capture.capture_error(RuntimeError("x"), kind="stream_crash")
    assert error_capture.is_error_capture_configured() is False


@pytest.mark.asyncio
async def test_invokes_injected_fn_with_kind_and_fields():
    seen = {}

    async def fake(exc, *, kind, **fields):
        seen["exc"] = exc
        seen["kind"] = kind
        seen["fields"] = fields

    error_capture.configure_error_capture(fake, allow_in_tests=True)
    assert error_capture.is_error_capture_configured() is True

    err = ValueError("boom")
    await error_capture.capture_error(
        err, kind="stream_cancelled", request_id="r1", user_id="u1",
        route="TestFlow", context={"debug_label": "TestFlow"},
    )

    assert seen["exc"] is err
    assert seen["kind"] == "stream_cancelled"
    assert seen["fields"]["request_id"] == "r1"
    assert seen["fields"]["user_id"] == "u1"
    assert seen["fields"]["route"] == "TestFlow"


@pytest.mark.asyncio
async def test_failing_capture_never_escalates():
    async def boom(exc, *, kind, **fields):
        raise RuntimeError("capture backend down")

    error_capture.configure_error_capture(boom, allow_in_tests=True)
    # Must swallow the capture failure — the caller is usually already on an
    # error/cancel path and must not be derailed.
    await error_capture.capture_error(KeyError("orig"), kind="stream_crash")


@pytest.mark.asyncio
async def test_capture_survives_outer_cancellation():
    """capture_error shields its write so an in-flight cancellation can't
    interrupt it mid-flight."""
    completed = {}

    async def slow_capture(exc, *, kind, **fields):
        await asyncio.sleep(0.02)
        completed["done"] = True

    error_capture.configure_error_capture(slow_capture, allow_in_tests=True)
    await error_capture.capture_error(asyncio.CancelledError(), kind="stream_cancelled")
    assert completed.get("done") is True


@pytest.mark.asyncio
async def test_default_capture_policy_blocks_test_process_writes(monkeypatch, caplog):
    seen = []

    async def would_write(exc, *, kind, **fields):
        seen.append((exc, kind, fields))

    monkeypatch.setenv("PYTEST_CURRENT_TEST", "synthetic::failure (call)")
    error_capture.configure_error_capture(would_write)

    await error_capture.capture_error(
        RuntimeError("synthetic failure"),
        kind="agent_run_stage_failed",
    )

    assert seen == []
    assert "system_error_capture_blocked_in_test" in caplog.text


@pytest.mark.asyncio
async def test_legacy_sse_adapter_durably_captures_source_crash():
    seen = []

    async def fake(exc, *, kind, **fields):
        seen.append((exc, kind, fields))

    async def source():
        yield "first"
        raise RuntimeError("source exploded")

    error_capture.configure_error_capture(fake, allow_in_tests=True)
    events = [event async for event in text_chunks_to_sse(source())]

    assert events[-1]["event"] == "error"
    assert seen[0][1] == "stream_crash"
    assert seen[0][2]["route"] == "text_chunks_to_sse"


@pytest.mark.asyncio
async def test_legacy_sse_adapter_captures_and_reraises_cancellation():
    seen = []

    async def fake(exc, *, kind, **fields):
        seen.append((exc, kind, fields))

    async def source():
        if False:
            yield "never"
        raise asyncio.CancelledError()

    error_capture.configure_error_capture(fake, allow_in_tests=True)
    with pytest.raises(asyncio.CancelledError):
        _ = [event async for event in text_chunks_to_sse(source())]

    assert seen[0][1] == "stream_cancelled"
