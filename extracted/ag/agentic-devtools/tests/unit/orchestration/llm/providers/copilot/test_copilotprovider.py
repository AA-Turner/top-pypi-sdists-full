"""Tests for CopilotProvider."""

import asyncio
from collections.abc import AsyncIterator
from typing import Any
from unittest.mock import AsyncMock

import pytest

from agentic_devtools.orchestration.llm.errors import (
    AuthenticationError,
    ModelNotAvailableError,
    RetryExhaustedError,
    StreamInterruptedError,
    StructuredOutputValidationError,
)
from agentic_devtools.orchestration.llm.providers.copilot import (
    CopilotProvider,
    CopilotTransportChunk,
    CopilotTransportResponse,
    _StatusError,
)
from agentic_devtools.orchestration.llm.types import LLMMessage, ProviderType, TokenUsage


class FakeTransport:
    """Deterministic Copilot transport for offline tests."""

    def __init__(self, response: CopilotTransportResponse | None = None, chunks=None, error=None):
        self.response = response or CopilotTransportResponse("ok", "gemini-3.7-flash")
        self.chunks = (
            [CopilotTransportChunk("hello"), CopilotTransportChunk(finish_reason="stop")] if chunks is None else chunks
        )
        self.error = error
        self.calls: list[Any] = []
        self.closed = False

    async def preflight(self, model: str, *, timeout_seconds: int | None = None) -> set[str]:
        self.calls.append(("preflight", model, timeout_seconds))
        if self.error:
            raise self.error
        return {"gemini-3.7-flash", "alias"}

    async def complete(self, messages, **kwargs) -> CopilotTransportResponse:
        self.calls.append(("complete", messages, kwargs))
        if self.error:
            raise self.error
        return self.response

    async def stream(self, messages, **kwargs) -> AsyncIterator[CopilotTransportChunk]:
        self.calls.append(("stream", messages, kwargs))
        for chunk in self.chunks:
            if isinstance(chunk, BaseException):
                raise chunk
            yield chunk

    async def close(self) -> None:
        self.closed = True


class NoPreflightTransport:
    """Transport used to verify calls can proceed without an inventory hook."""

    async def complete(self, messages, **kwargs) -> CopilotTransportResponse:
        return CopilotTransportResponse("ok")

    async def close(self) -> None:
        return None


def _messages() -> list[LLMMessage]:
    return [LLMMessage(role="user", content="Review this")]


@pytest.mark.asyncio
async def test_complete_forwards_model_parameters_and_metadata():
    usage = TokenUsage(input_tokens=2, output_tokens=3, total_tokens=5)
    transport = FakeTransport(CopilotTransportResponse("answer", "canonical-model", usage, "stop"))
    provider = CopilotProvider("gemini-3.7-flash", temperature=0.1, max_tokens=20, transport=transport)

    result = await provider.complete(_messages(), model="alias", timeout_seconds=7, tools=["tool"])

    assert result.text == "answer"
    assert result.model == "canonical-model"
    assert result.provider_type == ProviderType.COPILOT
    assert result.usage == usage
    assert result.latency_ms is not None
    assert result.finish_reason == "stop"
    complete_call = next(c for c in transport.calls if c[0] == "complete")
    assert complete_call[2] == {
        "model": "alias",
        "temperature": 0.1,
        "max_tokens": 20,
        "timeout_seconds": 7,
        "tools": ["tool"],
    }


def test_rejects_negative_timeout_seconds():
    """Negative timeout budgets fail during provider construction."""
    with pytest.raises(ValueError, match="timeout_seconds must be non-negative"):
        CopilotProvider("gemini-3.7-flash", timeout_seconds=-1)


@pytest.mark.asyncio
async def test_rejects_negative_per_call_timeout_on_complete():
    """Negative per-call timeout override fails before the transport is called."""
    transport = FakeTransport(CopilotTransportResponse("ok"))
    provider = CopilotProvider("gemini-3.7-flash", transport=transport)

    with pytest.raises(ValueError, match="timeout_seconds must be non-negative"):
        await provider.complete(_messages(), timeout_seconds=-1)


@pytest.mark.asyncio
async def test_rejects_negative_per_call_timeout_on_stream():
    """Negative per-call timeout override fails before the transport is called."""
    transport = FakeTransport(CopilotTransportResponse("ok"))
    provider = CopilotProvider("gemini-3.7-flash", transport=transport)

    with pytest.raises(ValueError, match="timeout_seconds must be non-negative"):
        async for _ in provider.stream(_messages(), timeout_seconds=-1):
            pass


@pytest.mark.asyncio
async def test_structured_output_validates_json():
    transport = FakeTransport(CopilotTransportResponse('{"ok": true}'))
    provider = CopilotProvider("gemini-3.7-flash", transport=transport)
    schema = {"type": "object", "required": ["ok"], "properties": {"ok": {"type": "boolean"}}}

    result = await provider.complete_structured(_messages(), schema)

    assert result.text == '{"ok": true}'
    complete_call = next(c for c in transport.calls if c[0] == "complete")
    assert "conforming to this schema" in complete_call[1][0].content


@pytest.mark.asyncio
async def test_structured_output_rejects_invalid_response():
    provider = CopilotProvider("gemini-3.7-flash", transport=FakeTransport(CopilotTransportResponse("{}")))

    with pytest.raises(StructuredOutputValidationError):
        await provider.complete_structured(
            _messages(),
            {"type": "object", "required": ["ok"], "properties": {"ok": {"type": "boolean"}}},
        )


@pytest.mark.asyncio
async def test_stream_preserves_deltas_and_finish_reason():
    usage = TokenUsage(input_tokens=1, output_tokens=2, total_tokens=3)
    transport = FakeTransport(
        chunks=[CopilotTransportChunk("a"), CopilotTransportChunk("b", "stop", usage, "gemini-3.7-flash")],
    )
    provider = CopilotProvider("gemini-3.7-flash", transport=transport)

    chunks = [chunk async for chunk in provider.stream(_messages())]

    assert [chunk.text_delta for chunk in chunks] == ["a", "b"]
    assert chunks[1].finish_reason == "stop"
    assert chunks[1].token_usage == usage
    assert chunks[1].model == "gemini-3.7-flash"


@pytest.mark.asyncio
async def test_stream_interruption_reports_partial_response():
    transport = FakeTransport(chunks=[CopilotTransportChunk("partial"), RuntimeError("offline")])
    provider = CopilotProvider("gemini-3.7-flash", transport=transport)

    with pytest.raises(StreamInterruptedError, match="interrupted") as exc_info:
        [chunk async for chunk in provider.stream(_messages())]

    assert exc_info.value.partial_response == "partial"
    assert exc_info.value.chunks_received == 1
    assert transport.closed


@pytest.mark.asyncio
async def test_preflight_maps_authentication_and_model_errors():
    provider = CopilotProvider(
        "gemini-3.7-flash",
        transport=FakeTransport(error=AuthenticationError("sign in", provider_type="copilot")),
    )

    with pytest.raises(AuthenticationError):
        await provider.preflight()

    provider = CopilotProvider("unknown", transport=FakeTransport())
    with pytest.raises(ModelNotAvailableError, match="unknown"):
        await provider.preflight()


@pytest.mark.asyncio
async def test_preflight_with_explicit_model_does_not_validate_unused_provider_default():
    provider = CopilotProvider("unused-default", transport=FakeTransport())
    await provider.preflight(["gemini-3.7-flash"])


@pytest.mark.asyncio
async def test_preflight_ignores_blank_and_non_string_requested_models():
    provider = CopilotProvider("gemini-3.7-flash", transport=FakeTransport())
    await provider.preflight(["  ", 42, "gemini-3.7-flash"])  # type: ignore[list-item]


@pytest.mark.asyncio
async def test_preflight_forwards_provider_timeout_to_transport():
    transport = FakeTransport()
    provider = CopilotProvider("gemini-3.7-flash", timeout_seconds=30, transport=transport)
    await provider.preflight()
    assert any(call[0] == "preflight" and call[2] == 30 for call in transport.calls)


@pytest.mark.asyncio
async def test_close_closes_transport():
    transport = FakeTransport()
    provider = CopilotProvider("gemini-3.7-flash", transport=transport)

    await provider.close()

    assert transport.closed


@pytest.mark.asyncio
async def test_close_without_transport_is_safe():
    await CopilotProvider("model").close()


def test_constructor_rejects_invalid_arguments():
    with pytest.raises(ValueError, match="non-empty"):
        CopilotProvider(" ")
    with pytest.raises(ValueError, match="either"):
        CopilotProvider("model", transport=FakeTransport(), transport_factory=FakeTransport)


def test_transport_is_lazily_created():
    transport = FakeTransport()
    provider = CopilotProvider("model", transport_factory=lambda: transport)
    assert provider._get_transport() is transport


def test_default_transport_is_lazily_created(monkeypatch):
    transport = FakeTransport()
    monkeypatch.setattr(
        "agentic_devtools.orchestration.llm.providers.copilot.CopilotSDKTransport",
        lambda: transport,
    )
    provider = CopilotProvider("model")
    assert provider._get_transport() is transport


@pytest.mark.asyncio
async def test_complete_maps_authentication_failure():
    provider = CopilotProvider(
        "gemini-3.7-flash",
        transport=FakeTransport(error=AuthenticationError("auth", provider_type="copilot")),
    )
    with pytest.raises(AuthenticationError):
        await provider.complete(_messages())


@pytest.mark.asyncio
async def test_preflight_handles_cancellation_generic_errors_and_empty_inventory():
    class CancelTransport(FakeTransport):
        async def preflight(self, model, *, timeout_seconds=None):
            raise asyncio.CancelledError

    with pytest.raises(asyncio.CancelledError):
        await CopilotProvider("model", transport=CancelTransport()).preflight()

    with pytest.raises(_StatusError):
        await CopilotProvider("model", transport=FakeTransport(error=_StatusError("bad", 418))).preflight()

    class EmptyTransport(FakeTransport):
        async def preflight(self, model, *, timeout_seconds=None):
            return None

    provider = CopilotProvider("model", transport=EmptyTransport())
    await provider.preflight()
    with pytest.raises(ModelNotAvailableError):
        provider._validate_model("")


@pytest.mark.asyncio
async def test_complete_handles_cancellation_and_status_errors():
    class CancelTransport(FakeTransport):
        async def complete(self, messages, **kwargs):
            raise asyncio.CancelledError

    cancelled = CopilotProvider("model", transport=CancelTransport())
    cancelled._known_models = {"model"}
    with pytest.raises(asyncio.CancelledError):
        await cancelled.complete(_messages())
    assert cancelled._transport.closed

    provider = CopilotProvider("model", transport=FakeTransport(error=_StatusError("bad", 418)))
    provider._known_models = {"model"}
    with pytest.raises(_StatusError):
        await provider.complete(_messages())


@pytest.mark.asyncio
async def test_stream_supports_empty_stream_and_cancellation():
    provider = CopilotProvider("gemini-3.7-flash", transport=FakeTransport(chunks=[]))
    assert [chunk async for chunk in provider.stream(_messages())] == []

    cancelled = CopilotProvider("gemini-3.7-flash", transport=FakeTransport(chunks=[asyncio.CancelledError()]))
    with pytest.raises(asyncio.CancelledError):
        [chunk async for chunk in cancelled.stream(_messages())]
    assert cancelled._transport.closed


@pytest.mark.asyncio
async def test_stream_maps_failure_before_first_chunk():
    transport = FakeTransport(chunks=[RuntimeError("offline")])
    provider = CopilotProvider("gemini-3.7-flash", transport=transport)
    with pytest.raises(RuntimeError, match="offline"):
        [chunk async for chunk in provider.stream(_messages())]
    assert transport.closed


@pytest.mark.asyncio
async def test_stream_retries_with_stable_request_kwargs():
    class RetryingTransport(FakeTransport):
        def __init__(self) -> None:
            super().__init__()
            self.attempts = 0

        async def stream(self, messages, **kwargs) -> AsyncIterator[CopilotTransportChunk]:
            self.calls.append(("stream", messages, kwargs))
            self.attempts += 1
            if self.attempts == 1:
                raise _StatusError("retry", 503)
            yield CopilotTransportChunk("ok")

    transport = RetryingTransport()
    provider = CopilotProvider("gemini-3.7-flash", transport=transport)
    provider._known_models = {"gemini-3.7-flash"}

    chunks = [
        chunk
        async for chunk in provider.stream(
            _messages(),
            temperature=0.2,
            max_tokens=64,
            timeout_seconds=9,
        )
    ]

    assert [chunk.text_delta for chunk in chunks] == ["ok"]
    assert len(transport.calls) == 2
    first_kwargs = transport.calls[0][2]
    second_kwargs = transport.calls[1][2]
    assert first_kwargs == second_kwargs
    assert first_kwargs == {
        "model": "gemini-3.7-flash",
        "temperature": 0.2,
        "max_tokens": 64,
        "timeout_seconds": 9,
    }


@pytest.mark.asyncio
async def test_stream_falls_back_to_request_model_when_chunk_model_missing():
    transport = FakeTransport(
        chunks=[
            CopilotTransportChunk(text_delta="hello"),
            CopilotTransportChunk(finish_reason="stop"),
        ]
    )
    provider = CopilotProvider("gemini-3.7-flash", transport=transport)
    provider._known_models = {"gemini-3.7-flash"}

    chunks = [chunk async for chunk in provider.stream(_messages())]

    assert [chunk.model for chunk in chunks] == ["gemini-3.7-flash", "gemini-3.7-flash"]


@pytest.mark.asyncio
async def test_preflight_maps_retry_exhaustion_to_inventory_error():
    provider = CopilotProvider(
        "gemini-3.7-flash",
        transport=FakeTransport(
            error=RetryExhaustedError(
                "All 5 retry attempts exhausted",
                attempts=5,
                total_wait_seconds=1.0,
                last_status_code=503,
            )
        ),
    )

    with pytest.raises(_StatusError, match="model inventory is unavailable") as exc_info:
        await provider.preflight()

    assert exc_info.value.status_code == 503


@pytest.mark.asyncio
async def test_complete_preserves_retry_exhaustion():
    provider = CopilotProvider(
        "gemini-3.7-flash",
        transport=FakeTransport(
            error=RetryExhaustedError(
                "All 5 retry attempts exhausted",
                attempts=5,
                total_wait_seconds=1.0,
                last_status_code=503,
            )
        ),
    )
    provider._known_models = {"gemini-3.7-flash"}

    with pytest.raises(RetryExhaustedError, match="All 5 retry attempts exhausted") as exc_info:
        await provider.complete(_messages())

    assert exc_info.value.attempts == 5
    assert exc_info.value.last_status_code == 503


@pytest.mark.asyncio
async def test_stream_preserves_retry_exhaustion():
    provider = CopilotProvider(
        "gemini-3.7-flash",
        transport=FakeTransport(
            chunks=[
                RetryExhaustedError(
                    "All 5 retry attempts exhausted",
                    attempts=5,
                    total_wait_seconds=1.0,
                    last_status_code=503,
                )
            ]
        ),
    )
    provider._known_models = {"gemini-3.7-flash"}

    with pytest.raises(RetryExhaustedError, match="All 5 retry attempts exhausted") as exc_info:
        [chunk async for chunk in provider.stream(_messages())]

    assert exc_info.value.attempts == 5
    assert exc_info.value.last_status_code == 503
    assert provider._transport.closed


@pytest.mark.asyncio
async def test_stream_accepts_awaitable_stream_result():
    transport = FakeTransport()
    stream = transport.stream(_messages(), model="model")
    transport.stream = AsyncMock(return_value=stream)
    provider = CopilotProvider("model", transport=transport)
    provider._known_models = {"model"}

    chunks = [chunk async for chunk in provider.stream(_messages())]

    assert chunks[0].text_delta == "hello"


@pytest.mark.asyncio
async def test_provider_without_preflight_hook_can_complete():
    provider = CopilotProvider("model", transport=NoPreflightTransport())

    result = await provider.complete(_messages())

    assert result.text == "ok"


@pytest.mark.asyncio
async def test_structured_output_augments_existing_system_message():
    provider = CopilotProvider("gemini-3.7-flash", transport=FakeTransport(CopilotTransportResponse("{}")))
    await provider.complete_structured(
        [LLMMessage(role="system", content="Instructions"), *_messages()],
        {"type": "object"},
    )
    complete_call = next(c for c in provider._get_transport().calls if c[0] == "complete")
    assert "Instructions" in complete_call[1][0].content
