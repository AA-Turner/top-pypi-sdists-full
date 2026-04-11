"""Tests for LiteLLMService provider."""

from __future__ import annotations

import asyncio
import sys
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from anteroom.config import AIConfig
from anteroom.services.token_provider import TokenProvider

# Create mock exception hierarchy matching litellm's real exceptions.
# These must exist before importing litellm_provider so the typed except blocks work.


class _MockLiteLLMAPIError(Exception):
    pass


class _MockAuthError(_MockLiteLLMAPIError):
    pass


class _MockRateLimitError(_MockLiteLLMAPIError):
    pass


class _MockContextError(_MockLiteLLMAPIError):
    pass


class _MockBadRequestError(_MockLiteLLMAPIError):
    pass


class _MockConnectionError(_MockLiteLLMAPIError):
    pass


class _MockTimeoutError(_MockLiteLLMAPIError):
    pass


class _MockServiceUnavailableError(_MockLiteLLMAPIError):
    pass


class _MockInternalServerError(_MockLiteLLMAPIError):
    pass


class _MockBadGatewayError(_MockLiteLLMAPIError):
    pass


# Inject a mock litellm module before importing litellm_provider,
# so that the try/except import succeeds and `litellm` is bound as a module attribute.
_mock_litellm_module = MagicMock()

# Wire up mock exceptions module. The litellm_provider module imports these
# at module init time and uses them in the `_LITELLM_TRANSIENT` tuple, so
# each attribute MUST be a real class that inherits from BaseException — a
# bare MagicMock would break `except _LITELLM_TRANSIENT` with
# "TypeError: catching classes that do not inherit from BaseException".
_mock_exceptions = MagicMock()
_mock_exceptions.AuthenticationError = _MockAuthError
_mock_exceptions.RateLimitError = _MockRateLimitError
_mock_exceptions.ContextWindowExceededError = _MockContextError
_mock_exceptions.BadRequestError = _MockBadRequestError
_mock_exceptions.APIConnectionError = _MockConnectionError
_mock_exceptions.APIError = _MockLiteLLMAPIError
_mock_exceptions.Timeout = _MockTimeoutError
_mock_exceptions.ServiceUnavailableError = _MockServiceUnavailableError
_mock_exceptions.InternalServerError = _MockInternalServerError
_mock_exceptions.BadGatewayError = _MockBadGatewayError
_mock_litellm_module.exceptions = _mock_exceptions

sys.modules.setdefault("litellm", _mock_litellm_module)
sys.modules.setdefault("litellm.exceptions", _mock_exceptions)

from anteroom.services.litellm_provider import LiteLLMService  # noqa: E402


def _make_config(**overrides: object) -> AIConfig:
    defaults: dict[str, object] = {
        "base_url": "https://openrouter.ai/api/v1",
        "api_key": "sk-or-test-key",
        "model": "openrouter/openai/gpt-4o",
        "provider": "litellm",
        "request_timeout": 120,
        "retry_max_attempts": 0,
    }
    defaults.update(overrides)
    return AIConfig(**defaults)


class _AsyncChunkIterator:
    """Helper that creates a proper async iterator from a list of chunks."""

    def __init__(self, chunks: list[Any]) -> None:
        self._chunks = list(chunks)
        self._index = 0

    def __aiter__(self) -> "_AsyncChunkIterator":
        return self

    async def __anext__(self) -> Any:
        if self._index >= len(self._chunks):
            raise StopAsyncIteration
        chunk = self._chunks[self._index]
        self._index += 1
        return chunk


def _make_service(config: AIConfig | None = None) -> LiteLLMService:
    """Build a LiteLLMService bypassing __init__."""
    svc = LiteLLMService.__new__(LiteLLMService)
    svc.config = config or _make_config()
    svc._token_provider = None
    return svc


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


class TestLiteLLMServiceConstruction:
    def test_raises_without_litellm(self) -> None:
        with patch("anteroom.services.litellm_provider.HAS_LITELLM", False):
            with pytest.raises(ImportError, match="litellm"):
                LiteLLMService(_make_config())

    def test_constructs_with_litellm(self) -> None:
        with patch("anteroom.services.litellm_provider.HAS_LITELLM", True):
            svc = LiteLLMService(_make_config())
            assert svc.config.provider == "litellm"

    def test_egress_blocked_raises(self) -> None:
        with (
            patch("anteroom.services.litellm_provider.HAS_LITELLM", True),
            patch("anteroom.services.litellm_provider.check_egress_allowed", return_value=False),
        ):
            with pytest.raises(ValueError, match="Egress blocked"):
                LiteLLMService(_make_config())


# ---------------------------------------------------------------------------
# Factory routing
# ---------------------------------------------------------------------------


class TestCreateAiServiceFactoryLiteLLM:
    def test_litellm_provider_selected(self) -> None:
        with patch("anteroom.services.litellm_provider.HAS_LITELLM", True):
            from anteroom.services.ai_service import create_ai_service

            config = _make_config(provider="litellm")
            svc = create_ai_service(config)
            assert isinstance(svc, LiteLLMService)

    def test_openai_still_default(self) -> None:
        from anteroom.services.ai_service import AIService, create_ai_service

        config = _make_config(provider="openai", base_url="http://localhost:11434/v1")
        with patch("anteroom.services.ai_service.AsyncOpenAI"):
            svc = create_ai_service(config)
        assert isinstance(svc, AIService)


# ---------------------------------------------------------------------------
# _build_kwargs
# ---------------------------------------------------------------------------


class TestBuildKwargs:
    def test_basic_kwargs(self) -> None:
        svc = _make_service()
        kwargs = svc._build_kwargs([{"role": "user", "content": "hi"}])
        assert kwargs["model"] == "openrouter/openai/gpt-4o"
        assert kwargs["api_key"] == "sk-or-test-key"
        assert kwargs["stream"] is False

    def test_stream_kwargs(self) -> None:
        svc = _make_service()
        kwargs = svc._build_kwargs([{"role": "user", "content": "hi"}], stream=True)
        assert kwargs["stream"] is True
        assert kwargs["stream_options"] == {"include_usage": True}

    def test_openrouter_headers_injected(self) -> None:
        svc = _make_service()
        kwargs = svc._build_kwargs([{"role": "user", "content": "hi"}])
        assert kwargs["extra_headers"]["HTTP-Referer"] == "https://anteroom.ai"
        assert kwargs["extra_headers"]["X-Title"] == "Anteroom"

    def test_no_openrouter_headers_for_other_models(self) -> None:
        svc = _make_service(_make_config(model="gpt-4o", base_url="https://api.openai.com/v1"))
        kwargs = svc._build_kwargs([{"role": "user", "content": "hi"}])
        assert "extra_headers" not in kwargs

    def test_tools_passed(self) -> None:
        svc = _make_service()
        tools = [{"type": "function", "function": {"name": "test"}}]
        kwargs = svc._build_kwargs([{"role": "user", "content": "hi"}], tools=tools)
        assert kwargs["tools"] == tools

    def test_temperature_passed(self) -> None:
        svc = _make_service(_make_config(temperature=0.5))
        kwargs = svc._build_kwargs([{"role": "user", "content": "hi"}])
        assert kwargs["temperature"] == 0.5

    def test_base_url_as_api_base(self) -> None:
        svc = _make_service()
        kwargs = svc._build_kwargs([{"role": "user", "content": "hi"}])
        assert kwargs["api_base"] == "https://openrouter.ai/api/v1"

    def test_top_p_passed(self) -> None:
        svc = _make_service(_make_config(top_p=0.9))
        kwargs = svc._build_kwargs([{"role": "user", "content": "hi"}])
        assert kwargs["top_p"] == 0.9

    def test_seed_passed(self) -> None:
        svc = _make_service(_make_config(seed=42))
        kwargs = svc._build_kwargs([{"role": "user", "content": "hi"}])
        assert kwargs["seed"] == 42

    def test_max_completion_tokens_passed(self) -> None:
        svc = _make_service()
        kwargs = svc._build_kwargs([{"role": "user", "content": "hi"}], max_completion_tokens=100)
        assert kwargs["max_completion_tokens"] == 100

    def test_openrouter_headers_via_base_url(self) -> None:
        svc = _make_service(_make_config(model="gpt-4o", base_url="https://openrouter.ai/api/v1"))
        kwargs = svc._build_kwargs([{"role": "user", "content": "hi"}])
        assert kwargs["extra_headers"]["HTTP-Referer"] == "https://anteroom.ai"

    def test_api_key_omitted_when_empty(self) -> None:
        """Bedrock/Vertex: omitting api_key lets LiteLLM use provider-native auth."""
        svc = _make_service(_make_config(api_key="", model="bedrock/anthropic.claude-3-sonnet", base_url=""))
        kwargs = svc._build_kwargs([{"role": "user", "content": "hi"}])
        assert "api_key" not in kwargs

    def test_api_key_included_when_set(self) -> None:
        svc = _make_service()
        kwargs = svc._build_kwargs([{"role": "user", "content": "hi"}])
        assert kwargs["api_key"] == "sk-or-test-key"


# ---------------------------------------------------------------------------
# Streaming
# ---------------------------------------------------------------------------


class TestLiteLLMStreamChat:
    @pytest.mark.asyncio
    async def test_stream_text_tokens(self) -> None:
        svc = _make_service()
        chunk = MagicMock()
        chunk.choices = [MagicMock()]
        chunk.choices[0].delta.content = "Hello"
        chunk.choices[0].delta.tool_calls = None
        chunk.choices[0].finish_reason = None
        chunk.usage = None

        done_chunk = MagicMock()
        done_chunk.choices = [MagicMock()]
        done_chunk.choices[0].delta.content = None
        done_chunk.choices[0].delta.tool_calls = None
        done_chunk.choices[0].finish_reason = "stop"
        done_chunk.usage = None

        mock_litellm = MagicMock()
        mock_litellm.acompletion = AsyncMock(return_value=_AsyncChunkIterator([chunk, done_chunk]))

        with patch("anteroom.services.litellm_provider.litellm", mock_litellm):
            events: list[dict[str, Any]] = []
            async for event in svc.stream_chat([{"role": "user", "content": "hi"}]):
                events.append(event)

        event_types = [e["event"] for e in events]
        assert "token" in event_types
        assert "done" in event_types

    @pytest.mark.asyncio
    async def test_stream_tool_call(self) -> None:
        svc = _make_service()
        tool_chunk = MagicMock()
        tool_chunk.choices = [MagicMock()]
        tool_chunk.choices[0].delta.content = None
        tc = MagicMock()
        tc.index = 0
        tc.id = "call_123"
        tc.function.name = "read_file"
        tc.function.arguments = '{"path": "/tmp/f"}'
        tool_chunk.choices[0].delta.tool_calls = [tc]
        tool_chunk.choices[0].finish_reason = None
        tool_chunk.usage = None

        done_chunk = MagicMock()
        done_chunk.choices = [MagicMock()]
        done_chunk.choices[0].delta.content = None
        done_chunk.choices[0].delta.tool_calls = None
        done_chunk.choices[0].finish_reason = "tool_calls"
        done_chunk.usage = None

        mock_litellm = MagicMock()
        mock_litellm.acompletion = AsyncMock(return_value=_AsyncChunkIterator([tool_chunk, done_chunk]))

        with patch("anteroom.services.litellm_provider.litellm", mock_litellm):
            events: list[dict[str, Any]] = []
            async for event in svc.stream_chat([{"role": "user", "content": "read file"}]):
                events.append(event)

        tool_events = [e for e in events if e["event"] == "tool_call"]
        assert len(tool_events) >= 1
        assert tool_events[0]["data"]["function_name"] == "read_file"

    @pytest.mark.asyncio
    async def test_stream_with_usage(self) -> None:
        svc = _make_service()
        chunk = MagicMock()
        chunk.choices = [MagicMock()]
        chunk.choices[0].delta.content = "Hi"
        chunk.choices[0].delta.tool_calls = None
        chunk.choices[0].finish_reason = None
        chunk.usage = None

        done_chunk = MagicMock()
        done_chunk.choices = [MagicMock()]
        done_chunk.choices[0].delta.content = None
        done_chunk.choices[0].delta.tool_calls = None
        done_chunk.choices[0].finish_reason = "stop"
        usage = MagicMock()
        usage.prompt_tokens = 10
        usage.completion_tokens = 5
        usage.total_tokens = 15
        done_chunk.usage = usage

        mock_litellm = MagicMock()
        mock_litellm.acompletion = AsyncMock(return_value=_AsyncChunkIterator([chunk, done_chunk]))

        with patch("anteroom.services.litellm_provider.litellm", mock_litellm):
            events: list[dict[str, Any]] = []
            async for event in svc.stream_chat([{"role": "user", "content": "hi"}]):
                events.append(event)

        usage_events = [e for e in events if e["event"] == "usage"]
        assert len(usage_events) == 1
        assert usage_events[0]["data"]["prompt_tokens"] == 10


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------


class TestLiteLLMStreamErrors:
    @pytest.mark.asyncio
    async def test_auth_error(self) -> None:
        svc = _make_service()
        mock_litellm = MagicMock()
        mock_litellm.acompletion = AsyncMock(side_effect=_MockAuthError("invalid api key"))

        with patch("anteroom.services.litellm_provider.litellm", mock_litellm):
            events: list[dict[str, Any]] = []
            async for event in svc.stream_chat([{"role": "user", "content": "hi"}]):
                events.append(event)

        error_events = [e for e in events if e["event"] == "error"]
        assert len(error_events) == 1
        assert error_events[0]["data"]["code"] == "auth_failed"

    @pytest.mark.asyncio
    async def test_rate_limit_error(self) -> None:
        svc = _make_service()
        mock_litellm = MagicMock()
        mock_litellm.acompletion = AsyncMock(side_effect=_MockRateLimitError("Rate limit exceeded"))

        with patch("anteroom.services.litellm_provider.litellm", mock_litellm):
            events: list[dict[str, Any]] = []
            async for event in svc.stream_chat([{"role": "user", "content": "hi"}]):
                events.append(event)

        error_events = [e for e in events if e["event"] == "error"]
        assert len(error_events) == 1
        assert error_events[0]["data"]["code"] == "rate_limit"

    @pytest.mark.asyncio
    async def test_context_length_error(self) -> None:
        svc = _make_service()
        mock_litellm = MagicMock()
        mock_litellm.acompletion = AsyncMock(side_effect=_MockContextError("context length exceeded"))

        with patch("anteroom.services.litellm_provider.litellm", mock_litellm):
            events: list[dict[str, Any]] = []
            async for event in svc.stream_chat([{"role": "user", "content": "hi"}]):
                events.append(event)

        error_events = [e for e in events if e["event"] == "error"]
        assert len(error_events) == 1
        assert error_events[0]["data"]["code"] == "context_length_exceeded"

    @pytest.mark.asyncio
    async def test_transient_error_retries(self) -> None:
        # (#1343) Transient = typed LiteLLM classes only. Bare Exception is
        # now fail-fast; see test_unknown_exception_fails_fast below.
        svc = _make_service(_make_config(retry_max_attempts=1))
        mock_litellm = MagicMock()
        mock_litellm.acompletion = AsyncMock(side_effect=_MockConnectionError("Connection reset"))

        with patch("anteroom.services.litellm_provider.litellm", mock_litellm):
            events: list[dict[str, Any]] = []
            async for event in svc.stream_chat([{"role": "user", "content": "hi"}]):
                events.append(event)

        retry_events = [e for e in events if e["event"] == "retrying"]
        assert len(retry_events) >= 1
        # (#1343) retrying events now carry exception_type for observability.
        assert retry_events[0]["data"]["exception_type"] == "_MockConnectionError"
        error_events = [e for e in events if e["event"] == "error"]
        assert len(error_events) == 1
        assert error_events[0]["data"]["retryable"] is True
        # (#1343) error events now carry provider + model.
        assert error_events[0]["data"]["provider"] == "litellm"
        assert error_events[0]["data"]["model"] == "openrouter/openai/gpt-4o"

    @pytest.mark.asyncio
    async def test_transient_error_refreshes_api_key_each_attempt(self) -> None:
        """Regression: kwargs must be rebuilt each retry so api_key reflects token refresh."""
        svc = _make_service(_make_config(retry_max_attempts=1))
        mock_tp = MagicMock(spec=TokenProvider)
        call_count = 0

        def rotating_token() -> str:
            nonlocal call_count
            call_count += 1
            return f"key-{call_count}"

        mock_tp.get_token = MagicMock(side_effect=rotating_token)
        svc._token_provider = mock_tp

        captured_keys: list[str] = []

        async def capture_and_fail(**kwargs: Any) -> Any:
            captured_keys.append(kwargs["api_key"])
            # (#1343) Use a typed transient class so this exercises the
            # retry path; bare Exception would now fail fast.
            raise _MockConnectionError("transient failure")

        mock_litellm = MagicMock()
        mock_litellm.acompletion = AsyncMock(side_effect=capture_and_fail)

        with patch("anteroom.services.litellm_provider.litellm", mock_litellm):
            events: list[dict[str, Any]] = []
            async for event in svc.stream_chat([{"role": "user", "content": "hi"}]):
                events.append(event)

        # Two attempts (1 initial + 1 retry), each should get a fresh key
        assert len(captured_keys) == 2
        assert captured_keys[0] != captured_keys[1]

    @pytest.mark.asyncio
    async def test_bad_request_error_surfaces_sanitized_message(self) -> None:
        svc = _make_service()
        mock_litellm = MagicMock()
        mock_litellm.acompletion = AsyncMock(
            side_effect=_MockBadRequestError("The model was unable to complete inference due to an internal error")
        )

        with patch("anteroom.services.litellm_provider.litellm", mock_litellm):
            events: list[dict[str, Any]] = []
            async for event in svc.stream_chat([{"role": "user", "content": "hi"}]):
                events.append(event)

        error_events = [e for e in events if e["event"] == "error"]
        assert len(error_events) == 1
        assert error_events[0]["data"]["code"] == "bad_request"
        assert error_events[0]["data"]["retryable"] is False
        assert "unable to complete inference" in error_events[0]["data"]["message"]

    @pytest.mark.asyncio
    async def test_bad_request_too_many_tools(self) -> None:
        svc = _make_service()
        mock_litellm = MagicMock()
        mock_litellm.acompletion = AsyncMock(side_effect=_MockBadRequestError("too many tool definitions provided"))

        with patch("anteroom.services.litellm_provider.litellm", mock_litellm):
            events: list[dict[str, Any]] = []
            async for event in svc.stream_chat([{"role": "user", "content": "hi"}]):
                events.append(event)

        error_events = [e for e in events if e["event"] == "error"]
        assert len(error_events) == 1
        assert error_events[0]["data"]["code"] == "too_many_tools"
        assert error_events[0]["data"]["retryable"] is False


# ---------------------------------------------------------------------------
# (#1343) Typed transient retry path + tightened catch-all regression tests
# ---------------------------------------------------------------------------


class TestLiteLLMTypedTransientRetries:
    """Regression coverage for the explicit LiteLLM transient retry path.

    Before #1343, LiteLLM timeout / connection / service-unavailable
    failures rode the generic `except Exception` catch-all for retries.
    After #1343, they have typed handlers that retry, and the catch-all
    is tightened to fail-fast `provider_error`. These tests lock the
    new typed path in place so a future regression that drops one of
    the typed classes is caught immediately.
    """

    @pytest.mark.asyncio
    async def test_stream_chat_retries_on_litellm_connection_error(self) -> None:
        svc = _make_service(_make_config(retry_max_attempts=1))
        mock_litellm = MagicMock()
        # First attempt fails with a typed transient; second succeeds.
        done_chunk = MagicMock()
        done_chunk.choices = [MagicMock()]
        done_chunk.choices[0].delta.content = "ok"
        done_chunk.choices[0].delta.tool_calls = None
        done_chunk.choices[0].finish_reason = "stop"
        done_chunk.usage = None

        call_count = 0

        async def flaky(**kwargs: Any) -> Any:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise _MockConnectionError("network blip")
            return _AsyncChunkIterator([done_chunk])

        mock_litellm.acompletion = AsyncMock(side_effect=flaky)

        with patch("anteroom.services.litellm_provider.litellm", mock_litellm):
            events: list[dict[str, Any]] = []
            async for event in svc.stream_chat([{"role": "user", "content": "hi"}]):
                events.append(event)

        retry_events = [e for e in events if e["event"] == "retrying"]
        assert len(retry_events) == 1
        assert retry_events[0]["data"]["exception_type"] == "_MockConnectionError"
        error_events = [e for e in events if e["event"] == "error"]
        assert len(error_events) == 0  # second attempt succeeded
        done_events = [e for e in events if e["event"] == "done"]
        assert len(done_events) == 1

    @pytest.mark.asyncio
    async def test_stream_chat_retries_on_litellm_timeout_error(self) -> None:
        svc = _make_service(_make_config(retry_max_attempts=1))
        done_chunk = MagicMock()
        done_chunk.choices = [MagicMock()]
        done_chunk.choices[0].delta.content = "ok"
        done_chunk.choices[0].delta.tool_calls = None
        done_chunk.choices[0].finish_reason = "stop"
        done_chunk.usage = None

        call_count = 0

        async def flaky(**kwargs: Any) -> Any:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise _MockTimeoutError("request timed out")
            return _AsyncChunkIterator([done_chunk])

        mock_litellm = MagicMock()
        mock_litellm.acompletion = AsyncMock(side_effect=flaky)

        with patch("anteroom.services.litellm_provider.litellm", mock_litellm):
            events: list[dict[str, Any]] = []
            async for event in svc.stream_chat([{"role": "user", "content": "hi"}]):
                events.append(event)

        retry_events = [e for e in events if e["event"] == "retrying"]
        assert len(retry_events) == 1
        assert retry_events[0]["data"]["exception_type"] == "_MockTimeoutError"

    @pytest.mark.asyncio
    async def test_stream_chat_retries_on_litellm_service_unavailable(self) -> None:
        svc = _make_service(_make_config(retry_max_attempts=1))
        done_chunk = MagicMock()
        done_chunk.choices = [MagicMock()]
        done_chunk.choices[0].delta.content = "ok"
        done_chunk.choices[0].delta.tool_calls = None
        done_chunk.choices[0].finish_reason = "stop"
        done_chunk.usage = None

        call_count = 0

        async def flaky(**kwargs: Any) -> Any:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise _MockServiceUnavailableError("503")
            return _AsyncChunkIterator([done_chunk])

        mock_litellm = MagicMock()
        mock_litellm.acompletion = AsyncMock(side_effect=flaky)

        with patch("anteroom.services.litellm_provider.litellm", mock_litellm):
            events: list[dict[str, Any]] = []
            async for event in svc.stream_chat([{"role": "user", "content": "hi"}]):
                events.append(event)

        retry_events = [e for e in events if e["event"] == "retrying"]
        assert len(retry_events) == 1
        assert retry_events[0]["data"]["exception_type"] == "_MockServiceUnavailableError"

    @pytest.mark.asyncio
    async def test_stream_chat_retries_on_litellm_internal_server_error(self) -> None:
        svc = _make_service(_make_config(retry_max_attempts=1))
        done_chunk = MagicMock()
        done_chunk.choices = [MagicMock()]
        done_chunk.choices[0].delta.content = "ok"
        done_chunk.choices[0].delta.tool_calls = None
        done_chunk.choices[0].finish_reason = "stop"
        done_chunk.usage = None

        call_count = 0

        async def flaky(**kwargs: Any) -> Any:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise _MockInternalServerError("500")
            return _AsyncChunkIterator([done_chunk])

        mock_litellm = MagicMock()
        mock_litellm.acompletion = AsyncMock(side_effect=flaky)

        with patch("anteroom.services.litellm_provider.litellm", mock_litellm):
            events: list[dict[str, Any]] = []
            async for event in svc.stream_chat([{"role": "user", "content": "hi"}]):
                events.append(event)

        retry_events = [e for e in events if e["event"] == "retrying"]
        assert len(retry_events) == 1
        assert retry_events[0]["data"]["exception_type"] == "_MockInternalServerError"

    @pytest.mark.asyncio
    async def test_stream_chat_emits_timeout_error_event_after_transient_retries_exhausted(
        self,
    ) -> None:
        """When all typed-transient retries are exhausted, emit a single
        error event with code=timeout/connection_error and provider/model."""
        svc = _make_service(_make_config(retry_max_attempts=1))
        mock_litellm = MagicMock()
        mock_litellm.acompletion = AsyncMock(side_effect=_MockTimeoutError("persistent timeout"))

        with patch("anteroom.services.litellm_provider.litellm", mock_litellm):
            events: list[dict[str, Any]] = []
            async for event in svc.stream_chat([{"role": "user", "content": "hi"}]):
                events.append(event)

        error_events = [e for e in events if e["event"] == "error"]
        assert len(error_events) == 1
        err = error_events[0]["data"]
        assert err["code"] == "timeout"
        assert err["retryable"] is True
        assert err["provider"] == "litellm"
        assert err["model"] == "openrouter/openai/gpt-4o"
        assert "_MockTimeoutError" in err["message"]

    @pytest.mark.asyncio
    async def test_stream_chat_emits_provider_error_for_unknown_exception(self) -> None:
        """Tightened catch-all: bare Exception (not a typed transient) now
        emits code=provider_error with retryable=False and is NOT retried.

        This is the test that proves the catch-all tightening landed —
        any regression that reverts the typed transient handlers would
        cause this exception to fall through to the old retry path and
        this test would fail with a retry event."""
        svc = _make_service(_make_config(retry_max_attempts=1))
        mock_litellm = MagicMock()
        mock_litellm.acompletion = AsyncMock(
            side_effect=Exception("toolConfig must be defined when using tool calling with bedrock")
        )

        with patch("anteroom.services.litellm_provider.litellm", mock_litellm):
            events: list[dict[str, Any]] = []
            async for event in svc.stream_chat([{"role": "user", "content": "hi"}]):
                events.append(event)

        # Exactly one call (no retry) — catch-all is fail-fast now.
        assert mock_litellm.acompletion.call_count == 1
        retry_events = [e for e in events if e["event"] == "retrying"]
        assert len(retry_events) == 0
        error_events = [e for e in events if e["event"] == "error"]
        assert len(error_events) == 1
        err = error_events[0]["data"]
        assert err["code"] == "provider_error"
        assert err["retryable"] is False
        assert err["provider"] == "litellm"
        assert err["model"] == "openrouter/openai/gpt-4o"
        assert "toolConfig" in err["message"]


# ---------------------------------------------------------------------------
# Extra system prompt
# ---------------------------------------------------------------------------


class TestLiteLLMExtraSystemPrompt:
    @pytest.mark.asyncio
    async def test_extra_system_prompt_prepended(self) -> None:
        svc = _make_service()
        done_chunk = MagicMock()
        done_chunk.choices = [MagicMock()]
        done_chunk.choices[0].delta.content = "ok"
        done_chunk.choices[0].delta.tool_calls = None
        done_chunk.choices[0].finish_reason = "stop"
        done_chunk.usage = None

        async def capture_call(**kwargs: Any) -> Any:
            capture_call.messages = kwargs["messages"]
            return _AsyncChunkIterator([done_chunk])

        mock_litellm = MagicMock()
        mock_litellm.acompletion = AsyncMock(side_effect=capture_call)

        with patch("anteroom.services.litellm_provider.litellm", mock_litellm):
            events: list[dict[str, Any]] = []
            async for event in svc.stream_chat(
                [{"role": "user", "content": "hi"}],
                extra_system_prompt="Extra context here",
            ):
                events.append(event)

        system_msg = capture_call.messages[0]
        assert system_msg["role"] == "system"
        assert system_msg["content"].startswith("Extra context here\n\n")


# ---------------------------------------------------------------------------
# Generate title
# ---------------------------------------------------------------------------


class TestLiteLLMGenerateTitle:
    @pytest.mark.asyncio
    async def test_returns_title(self) -> None:
        svc = _make_service()
        mock_resp = MagicMock()
        mock_resp.choices = [MagicMock()]
        mock_resp.choices[0].message.content = "A good title"

        mock_litellm = MagicMock()
        mock_litellm.acompletion = AsyncMock(return_value=mock_resp)

        with patch("anteroom.services.litellm_provider.litellm", mock_litellm):
            title = await svc.generate_title("hello")
        assert title == "A good title"

    @pytest.mark.asyncio
    async def test_returns_fallback_on_error(self) -> None:
        svc = _make_service()
        mock_litellm = MagicMock()
        mock_litellm.acompletion = AsyncMock(side_effect=Exception("API error"))

        with patch("anteroom.services.litellm_provider.litellm", mock_litellm):
            title = await svc.generate_title("hello")
        assert title == "New Conversation"


# ---------------------------------------------------------------------------
# Validate connection
# ---------------------------------------------------------------------------


class TestLiteLLMValidateConnection:
    @pytest.mark.asyncio
    async def test_success(self) -> None:
        svc = _make_service()
        mock_resp = MagicMock()
        mock_resp.choices = [MagicMock()]
        mock_resp.choices[0].message.content = "Hi"

        mock_litellm = MagicMock()
        mock_litellm.acompletion = AsyncMock(return_value=mock_resp)

        with patch("anteroom.services.litellm_provider.litellm", mock_litellm):
            ok, msg, models = await svc.validate_connection()
        assert ok is True
        assert "openrouter/openai/gpt-4o" in models

    @pytest.mark.asyncio
    async def test_failure(self) -> None:
        svc = _make_service()
        mock_litellm = MagicMock()
        mock_litellm.acompletion = AsyncMock(side_effect=Exception("Connection refused"))

        with patch("anteroom.services.litellm_provider.litellm", mock_litellm):
            ok, msg, models = await svc.validate_connection()
        assert ok is False
        assert models == []


# ---------------------------------------------------------------------------
# Complete
# ---------------------------------------------------------------------------


class TestLiteLLMComplete:
    @pytest.mark.asyncio
    async def test_returns_text(self) -> None:
        svc = _make_service()
        mock_resp = MagicMock()
        mock_resp.choices = [MagicMock()]
        mock_resp.choices[0].message.content = "The answer is 42"

        mock_litellm = MagicMock()
        mock_litellm.acompletion = AsyncMock(return_value=mock_resp)

        with patch("anteroom.services.litellm_provider.litellm", mock_litellm):
            result = await svc.complete([{"role": "user", "content": "question"}])
        assert result == "The answer is 42"

    @pytest.mark.asyncio
    async def test_returns_none_on_error(self) -> None:
        svc = _make_service()
        mock_litellm = MagicMock()
        mock_litellm.acompletion = AsyncMock(side_effect=Exception("fail"))

        with patch("anteroom.services.litellm_provider.litellm", mock_litellm):
            result = await svc.complete([{"role": "user", "content": "question"}])
        assert result is None


# ---------------------------------------------------------------------------
# Inheritance check — LiteLLMService has the AIService interface
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Token provider
# ---------------------------------------------------------------------------


class TestLiteLLMTokenProvider:
    def test_resolve_api_key_from_token_provider(self) -> None:
        svc = _make_service()
        mock_tp = MagicMock(spec=TokenProvider)
        mock_tp.get_token.return_value = "refreshed-key"
        svc._token_provider = mock_tp
        assert svc._resolve_api_key() == "refreshed-key"
        mock_tp.get_token.assert_called_once()

    def test_resolve_api_key_fallback_to_config(self) -> None:
        svc = _make_service()
        assert svc._resolve_api_key() == "sk-or-test-key"

    def test_try_refresh_token_success(self) -> None:
        svc = _make_service()
        mock_tp = MagicMock(spec=TokenProvider)
        svc._token_provider = mock_tp
        assert svc._try_refresh_token() is True
        mock_tp.refresh.assert_called_once()

    def test_try_refresh_token_no_provider(self) -> None:
        svc = _make_service()
        assert svc._try_refresh_token() is False

    def test_try_refresh_token_failure(self) -> None:
        from anteroom.services.token_provider import TokenProviderError

        svc = _make_service()
        mock_tp = MagicMock(spec=TokenProvider)
        mock_tp.refresh.side_effect = TokenProviderError("fail")
        svc._token_provider = mock_tp
        assert svc._try_refresh_token() is False

    @pytest.mark.asyncio
    async def test_auth_error_with_successful_refresh(self) -> None:
        svc = _make_service()
        mock_tp = MagicMock(spec=TokenProvider)
        svc._token_provider = mock_tp

        call_count = 0

        async def mock_acompletion(**kwargs: Any) -> Any:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise _MockAuthError("invalid api key")
            # Second call succeeds with a simple done stream
            done_chunk = MagicMock()
            done_chunk.choices = [MagicMock()]
            done_chunk.choices[0].delta.content = "ok"
            done_chunk.choices[0].delta.tool_calls = None
            done_chunk.choices[0].finish_reason = "stop"
            done_chunk.usage = None
            return _AsyncChunkIterator([done_chunk])

        mock_litellm = MagicMock()
        mock_litellm.acompletion = AsyncMock(side_effect=mock_acompletion)

        with patch("anteroom.services.litellm_provider.litellm", mock_litellm):
            events: list[dict[str, Any]] = []
            async for event in svc.stream_chat([{"role": "user", "content": "hi"}]):
                events.append(event)

        event_types = [e["event"] for e in events]
        assert "token" in event_types or "done" in event_types
        mock_tp.refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_auth_retry_guard_prevents_infinite_recursion(self) -> None:
        """After one refresh, a second 401 should yield error, not recurse."""
        svc = _make_service()
        mock_tp = MagicMock(spec=TokenProvider)
        svc._token_provider = mock_tp

        mock_litellm = MagicMock()
        mock_litellm.acompletion = AsyncMock(side_effect=_MockAuthError("invalid api key"))

        with patch("anteroom.services.litellm_provider.litellm", mock_litellm):
            events: list[dict[str, Any]] = []
            async for event in svc.stream_chat([{"role": "user", "content": "hi"}]):
                events.append(event)

        error_events = [e for e in events if e["event"] == "error"]
        assert len(error_events) == 1
        assert error_events[0]["data"]["code"] == "auth_failed"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestLiteLLMEdgeCases:
    @pytest.mark.asyncio
    async def test_validate_connection_no_choices(self) -> None:
        svc = _make_service()
        mock_resp = MagicMock()
        mock_resp.choices = []

        mock_litellm = MagicMock()
        mock_litellm.acompletion = AsyncMock(return_value=mock_resp)

        with patch("anteroom.services.litellm_provider.litellm", mock_litellm):
            ok, msg, models = await svc.validate_connection()
        assert ok is False

    @pytest.mark.asyncio
    async def test_complete_no_choices(self) -> None:
        svc = _make_service()
        mock_resp = MagicMock()
        mock_resp.choices = []

        mock_litellm = MagicMock()
        mock_litellm.acompletion = AsyncMock(return_value=mock_resp)

        with patch("anteroom.services.litellm_provider.litellm", mock_litellm):
            result = await svc.complete([{"role": "user", "content": "hi"}])
        assert result is None

    @pytest.mark.asyncio
    async def test_stream_cancelled_mid_stream(self) -> None:
        svc = _make_service()
        cancel_event = asyncio.Event()

        chunk = MagicMock()
        chunk.choices = [MagicMock()]
        chunk.choices[0].delta.content = "Hello"
        chunk.choices[0].delta.tool_calls = None
        chunk.choices[0].finish_reason = None
        chunk.usage = None

        # Set cancel after first chunk is yielded
        async def cancelling_stream(**kwargs: Any) -> Any:
            return _AsyncChunkIterator([chunk, chunk, chunk])

        mock_litellm = MagicMock()
        mock_litellm.acompletion = AsyncMock(side_effect=cancelling_stream)

        with patch("anteroom.services.litellm_provider.litellm", mock_litellm):
            events: list[dict[str, Any]] = []
            async for event in svc.stream_chat([{"role": "user", "content": "hi"}], cancel_event=cancel_event):
                events.append(event)
                if event.get("event") == "token":
                    cancel_event.set()

        # Should have stopped after cancel, not consumed all chunks
        token_events = [e for e in events if e["event"] == "token"]
        assert len(token_events) <= 2  # at most 1-2 before cancel detected


# ---------------------------------------------------------------------------
# Inheritance check — LiteLLMService has the AIService interface
# ---------------------------------------------------------------------------


class TestLiteLLMInterface:
    def test_instance_has_required_methods(self) -> None:
        svc = _make_service()
        assert hasattr(svc, "stream_chat")
        assert hasattr(svc, "generate_title")
        assert hasattr(svc, "complete")
        assert hasattr(svc, "validate_connection")


# ---------------------------------------------------------------------------
# Pre-flight validation tests (#1344)
# ---------------------------------------------------------------------------


class TestPreflightValidation:
    @pytest.mark.asyncio
    async def test_stream_chat_rejects_assistant_first_anthropic_route(self) -> None:
        """stream_chat yields request_invalid for Anthropic routes with assistant-first."""
        svc = _make_service(_make_config(model="anthropic/claude-sonnet-4-20250514"))
        messages = [{"role": "assistant", "content": "oops"}]
        events: list[dict[str, Any]] = []
        async for event in svc.stream_chat(messages):
            events.append(event)

        error_events = [e for e in events if e["event"] == "error"]
        assert len(error_events) == 1
        assert error_events[0]["data"]["code"] == "request_invalid"
        assert error_events[0]["data"]["retryable"] is False
        assert error_events[0]["data"]["provider"] == "litellm"
        assert "role='assistant'" in error_events[0]["data"]["message"]
        # SDK must not have been called
        _mock_litellm_module.acompletion.assert_not_called()

    @pytest.mark.asyncio
    async def test_stream_chat_rejects_assistant_first_bedrock_route(self) -> None:
        """stream_chat yields request_invalid for Bedrock routes with assistant-first."""
        svc = _make_service(_make_config(model="bedrock/anthropic.claude-v2"))
        messages = [{"role": "assistant", "content": "oops"}]
        events: list[dict[str, Any]] = []
        async for event in svc.stream_chat(messages):
            events.append(event)

        error_events = [e for e in events if e["event"] == "error"]
        assert len(error_events) == 1
        assert error_events[0]["data"]["code"] == "request_invalid"

    @pytest.mark.asyncio
    async def test_stream_chat_does_not_validate_openai_route(self) -> None:
        """OpenAI routes accept any message ordering — no first-message validation."""
        svc = _make_service(_make_config(model="openai/gpt-4o"))

        # Set up mock to return a valid stream
        chunk = MagicMock()
        chunk.usage = None
        chunk.choices = [MagicMock()]
        chunk.choices[0].delta = MagicMock()
        chunk.choices[0].delta.content = "Hi"
        chunk.choices[0].delta.tool_calls = None
        chunk.choices[0].finish_reason = "stop"
        _mock_litellm_module.acompletion = AsyncMock(return_value=_AsyncChunkIterator([chunk]))

        messages = [{"role": "assistant", "content": "I go first"}]
        events: list[dict[str, Any]] = []
        async for event in svc.stream_chat(messages):
            events.append(event)

        # Should NOT have a request_invalid error
        assert not any(e["event"] == "error" and e["data"].get("code") == "request_invalid" for e in events)

    @pytest.mark.asyncio
    async def test_stream_chat_rejects_bedrock_tools_without_confirmation(self) -> None:
        """Bedrock + tools + unconfirmed triggers bedrock_tool_route rule."""
        svc = _make_service(_make_config(model="bedrock/anthropic.claude-v2", litellm_bedrock_tools_confirmed=False))
        messages = [{"role": "user", "content": "Hi"}]
        tools = [{"type": "function", "function": {"name": "test", "parameters": {}}}]
        events: list[dict[str, Any]] = []
        async for event in svc.stream_chat(messages, tools=tools):
            events.append(event)

        error_events = [e for e in events if e["event"] == "error"]
        assert len(error_events) == 1
        assert error_events[0]["data"]["code"] == "request_invalid"
        assert "litellm_bedrock_tools_confirmed" in error_events[0]["data"]["message"]

    @pytest.mark.asyncio
    async def test_stream_chat_allows_bedrock_tools_when_confirmed(self) -> None:
        """Bedrock + tools + confirmed=True passes validation."""
        svc = _make_service(_make_config(model="bedrock/anthropic.claude-v2", litellm_bedrock_tools_confirmed=True))

        chunk = MagicMock()
        chunk.usage = None
        chunk.choices = [MagicMock()]
        chunk.choices[0].delta = MagicMock()
        chunk.choices[0].delta.content = "Hi"
        chunk.choices[0].delta.tool_calls = None
        chunk.choices[0].finish_reason = "stop"
        _mock_litellm_module.acompletion = AsyncMock(return_value=_AsyncChunkIterator([chunk]))

        messages = [{"role": "user", "content": "Hi"}]
        tools = [{"type": "function", "function": {"name": "test", "parameters": {}}}]
        events: list[dict[str, Any]] = []
        async for event in svc.stream_chat(messages, tools=tools):
            events.append(event)

        assert not any(e["event"] == "error" and e["data"].get("code") == "request_invalid" for e in events)

    @pytest.mark.asyncio
    async def test_complete_validates_anthropic_route(self) -> None:
        """complete() with Anthropic route raises on assistant-first."""
        svc = _make_service(_make_config(model="anthropic/claude-sonnet-4-20250514"))
        messages = [{"role": "assistant", "content": "oops"}]
        # complete() catches Exception and returns None
        result = await svc.complete(messages)
        assert result is None

    @pytest.mark.asyncio
    async def test_complete_with_usage_validates_anthropic_route(self) -> None:
        """complete_with_usage() with Anthropic route raises on assistant-first."""
        svc = _make_service(_make_config(model="anthropic/claude-sonnet-4-20250514"))
        messages = [{"role": "assistant", "content": "oops"}]
        # complete_with_usage catches Exception and re-raises
        with pytest.raises(Exception):
            await svc.complete_with_usage(messages)
