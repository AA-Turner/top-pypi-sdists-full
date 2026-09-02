"""Regression tests for OpenAI streaming terminal-event handling.

The OpenAI Responses SDK only records its internal ``_completed_response`` for a
``response.completed`` event, so ``stream.get_final_response()`` RAISES
("Didn't receive a `response.completed` event.") for a ``response.incomplete``
terminal state — e.g. a reasoning model that streamed a full answer but hit
``max_output_tokens``. The old code let that RuntimeError bubble up as a
retryable error, which DISCARDED the already-streamed answer and retried.

``_execute_streaming`` now captures the terminal ``event.response`` directly for
``response.completed`` / ``response.incomplete`` so the answer survives with its
real finish_reason, and only falls back to the raising ``get_final_response()``
when no usable terminal event arrived (a genuine failure / mid-stream break).
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.providers.openai.openai_api import OpenAIChat


class _FakeEmitter:
    def __init__(self) -> None:
        self.chunks: list[str] = []

    async def send_chunk(self, text: str) -> None:
        self.chunks.append(text)

    async def send_error(self, **kwargs) -> None:  # pragma: no cover - not hit here
        pass


class _FakeStream:
    """Minimal async-context-manager + async-iterator mimicking the SDK stream."""

    def __init__(self, events: list, raise_on_final: bool = True) -> None:
        self._events = events
        self._raise_on_final = raise_on_final
        self.get_final_called = False

    async def __aenter__(self) -> _FakeStream:
        return self

    async def __aexit__(self, *exc) -> bool:
        return False

    async def __aiter__(self):
        for event in self._events:
            yield event

    async def get_final_response(self):
        self.get_final_called = True
        if self._raise_on_final:
            raise RuntimeError("Didn't receive a `response.completed` event.")
        return SimpleNamespace(status="completed")


def _bare_chat() -> OpenAIChat:
    # Avoid the real AsyncOpenAI/network client construction.
    chat = object.__new__(OpenAIChat)
    chat.debug = False
    chat._event_samples = {}
    chat._reasoning_started = {}
    return chat


def _install_stream(chat: OpenAIChat, stream: _FakeStream) -> None:
    chat.client = SimpleNamespace(responses=SimpleNamespace(stream=lambda **kwargs: stream))
    # Passthrough so we can assert which Response object flowed through.
    chat.to_unified_response = lambda resp, name: ("RESULT", resp.status)


@pytest.mark.asyncio
async def test_incomplete_terminal_event_is_returned_not_retried():
    incomplete_resp = SimpleNamespace(status="incomplete")
    events = [
        SimpleNamespace(type="response.created"),
        SimpleNamespace(type="response.output_text.delta", delta="hello "),
        SimpleNamespace(type="response.output_text.delta", delta="world"),
        SimpleNamespace(type="response.incomplete", response=incomplete_resp),
    ]
    stream = _FakeStream(events, raise_on_final=True)
    chat = _bare_chat()
    _install_stream(chat, stream)
    emitter = _FakeEmitter()

    result = await chat._execute_streaming({}, emitter, "gpt-5.5")

    assert result == ("RESULT", "incomplete")
    assert emitter.chunks == ["hello ", "world"]
    # We must NOT have fallen back to the raising accumulator.
    assert stream.get_final_called is False


@pytest.mark.asyncio
async def test_completed_terminal_event_is_returned():
    completed_resp = SimpleNamespace(status="completed")
    events = [
        SimpleNamespace(type="response.created"),
        SimpleNamespace(type="response.output_text.delta", delta="ok"),
        SimpleNamespace(type="response.completed", response=completed_resp),
    ]
    stream = _FakeStream(events, raise_on_final=True)
    chat = _bare_chat()
    _install_stream(chat, stream)

    result = await chat._execute_streaming({}, _FakeEmitter(), "gpt-5.5")

    assert result == ("RESULT", "completed")
    assert stream.get_final_called is False


@pytest.mark.asyncio
async def test_no_terminal_event_falls_back_and_raises():
    # A genuine mid-stream break: no completed/incomplete event ever arrives.
    events = [
        SimpleNamespace(type="response.created"),
        SimpleNamespace(type="response.output_text.delta", delta="partial"),
    ]
    stream = _FakeStream(events, raise_on_final=True)
    chat = _bare_chat()
    _install_stream(chat, stream)

    with pytest.raises(RuntimeError):
        await chat._execute_streaming({}, _FakeEmitter(), "gpt-5.5")
    assert stream.get_final_called is True
