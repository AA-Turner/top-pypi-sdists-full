"""An out-of-credit refusal delivered as a FLAT Responses ``error`` event is
classified as billing — and the adapter does not announce it first.

The OpenAI SDK raises ``APIError`` itself only for a NESTED ``{"error": {...}}``
stream body. The flat Responses event (``{type: "error", code, message}``) is
handed to ``_handle_event``, and the stream then fails with "Didn't receive a
`response.completed` event" — no code, no message.

Breaks named:
* the provider's words are dropped on the flat path → the refusal is a
  retryable ``unknown_error`` again (the 2026-10-01 incident class);
* the adapter sends "An error occurred during streaming." for a billing
  refusal the orchestrator owns (and may still reroute past).
Control: a non-billing stream error is still sent to the person.

SUT: ``OpenAIChat._execute_streaming`` / ``_handle_event``. Doubles: the SDK
stream (yields the recorded event, then raises like the SDK does) and the
emitter.
"""

from __future__ import annotations

from typing import Any

import pytest
from openai.types.responses import ResponseErrorEvent

from matrx_ai.providers.errors import classify_provider_error
from matrx_ai.providers.openai.openai_api import OpenAIChat

_NO_CREDITS = (
    "You have no credits remaining. Add credits to continue using the API at "
    "https://platform.openai.com/settings/organization/billing/."
)


class _Emitter:
    def __init__(self) -> None:
        self.errors: list[dict[str, Any]] = []

    async def send_error(self, **kwargs: Any) -> None:
        self.errors.append(kwargs)

    def __getattr__(self, name: str) -> Any:
        async def _noop(*a: Any, **k: Any) -> None:
            return None

        return _noop


class _SdkStream:
    """Yields the recorded events, then fails the way the SDK does with no
    ``response.completed``."""

    def __init__(self, events: list[Any]) -> None:
        self.events = events

    async def __aenter__(self) -> _SdkStream:
        return self

    async def __aexit__(self, *exc: Any) -> None:
        return None

    def __aiter__(self) -> Any:
        async def _gen() -> Any:
            for event in self.events:
                yield event

        return _gen()

    async def get_final_response(self) -> Any:
        raise RuntimeError("Didn't receive a `response.completed` event.")


def _flat_error(code: str, message: str) -> ResponseErrorEvent:
    return ResponseErrorEvent(type="error", code=code, message=message, param=None, sequence_number=3)


async def _stream(monkeypatch: pytest.MonkeyPatch, event: Any) -> tuple[BaseException, _Emitter]:
    class _Responses:
        def stream(self, **kwargs: Any) -> _SdkStream:
            return _SdkStream([event])

    class _Client:
        responses = _Responses()

    monkeypatch.setattr(OpenAIChat, "client", _Client())
    emitter = _Emitter()
    with pytest.raises(Exception) as raised:
        await OpenAIChat()._execute_streaming({"model": "gpt-5.4-nano", "input": []}, emitter, "gpt-5.4-nano")
    return raised.value, emitter


@pytest.mark.asyncio
async def test_a_flat_out_of_credit_event_classifies_as_billing(monkeypatch) -> None:
    exc, _ = await _stream(monkeypatch, _flat_error("insufficient_quota", _NO_CREDITS))
    result = classify_provider_error("openai", exc)  # type: ignore[arg-type]
    assert result.error_type == "billing_error"
    assert result.is_retryable is False


@pytest.mark.asyncio
async def test_a_flat_server_error_event_keeps_its_words(monkeypatch) -> None:
    exc, _ = await _stream(
        monkeypatch,
        _flat_error("server_error", "The server had an error while processing your request."),
    )
    assert "The server had an error while processing your request." in str(exc)
    assert classify_provider_error("openai", exc).error_type != "billing_error"  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_a_billing_stream_event_is_left_to_the_orchestrator(monkeypatch) -> None:
    _, emitter = await _stream(monkeypatch, _flat_error("insufficient_quota", _NO_CREDITS))
    assert emitter.errors == []


@pytest.mark.asyncio
async def test_a_non_billing_stream_event_is_still_sent(monkeypatch) -> None:
    _, emitter = await _stream(
        monkeypatch,
        _flat_error("server_error", "The server had an error while processing your request."),
    )
    assert [(e["error_type"], e["message"]) for e in emitter.errors] == [
        ("streaming_error", "server_error The server had an error while processing your request.")
    ]
