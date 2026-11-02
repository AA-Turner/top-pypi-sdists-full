"""A caller refusal raised inside a stream reaches the client as ITS code.

The refusal under test is the guest AI allowance (matrx-ai raises it at the
paid-call seam with ``is_caller_refusal = True`` and a classified
``error_info``). matrx-connect does not import matrx-ai, so the exception is
modeled here by its two attributes — exactly what the crash handler reads.

Breaks named:
* the stream error event carries a generic ``<label>_error`` instead of
  ``guest_ai_allowance_used`` → the frontend cannot show the sign-up prompt;
* the numbers (allowance / used) are dropped from the event;
* an expected refusal is filed as a ``stream_crash`` system_error.
"""

from __future__ import annotations

import json
import types
from typing import Any

import pytest

from matrx_connect.emitters.stream_emitter import StreamEmitter
from matrx_connect.streaming import response as response_mod
from matrx_connect.streaming.response import create_streaming_response


class _Refusal(Exception):
    is_caller_refusal = True

    def __init__(self) -> None:
        self.error_info = types.SimpleNamespace(
            error_type="guest_ai_allowance_used",
            message="You've used your free AI tries. Create a free account to keep going.",
            user_message="You've used your free AI tries. Create a free account to keep going.",
            details={"allowance": 3, "used": 3},
        )
        super().__init__(self.error_info.message)


def _ctx(emitter: Any) -> Any:
    return types.SimpleNamespace(
        request_id="req-refusal-1",
        user_id="user-1",
        conversation_id=None,
        source_app="test",
        agent_id=None,
        emitter=emitter,
    )


async def _drain(response: Any) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    async for chunk in response.body_iterator:
        text = chunk.decode() if isinstance(chunk, bytes) else chunk
        for line in text.splitlines():
            if line.strip():
                events.append(json.loads(line))
    return events


@pytest.mark.asyncio
async def test_refusal_reaches_the_wire_with_its_code_and_numbers(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: list[str] = []

    async def _capture(exc: BaseException, *, kind: str, **_: Any) -> None:
        captured.append(kind)

    monkeypatch.setattr(response_mod, "capture_error", _capture)

    async def refused_task(emitter: Any) -> None:
        raise _Refusal()

    emitter = StreamEmitter(heartbeat_interval=600)
    events = await _drain(
        create_streaming_response(_ctx(emitter), refused_task, debug_label="chat")
    )

    errors = [e for e in events if e.get("event") == "error"]
    assert errors, f"no error event: {[e.get('event') for e in events]}"
    data = errors[-1]["data"]
    assert data["error_type"] == "guest_ai_allowance_used"
    assert data["user_message"].startswith("You've used your free AI tries.")
    assert data["details"]["allowance"] == 3
    assert data["details"]["used"] == 3
    ends = [e for e in events if e.get("event") == "end"]
    assert ends and ends[-1]["data"]["reason"] != "complete"
    assert "stream_crash" not in captured, "an expected refusal was filed as a crash"


class _PrepRefusal(_Refusal):
    http_status = 403


@pytest.mark.asyncio
async def test_a_refusal_during_prep_is_an_http_outcome_not_a_stream() -> None:
    """Prep refused (nothing streamed, no turn): the host's handler answers 403."""
    from matrx_connect.streaming.response import create_prepared_streaming_response

    async def _prepare() -> tuple[Any, ...]:
        raise _PrepRefusal()

    async def _never(*_: Any) -> None:  # pragma: no cover - must not run
        raise AssertionError("the run started after prep refused")

    emitter = StreamEmitter(heartbeat_interval=600)
    ctx = _ctx(emitter)
    ctx.agent_id = None
    with pytest.raises(_PrepRefusal):
        await create_prepared_streaming_response(ctx, _prepare, _never, debug_label="chat")
