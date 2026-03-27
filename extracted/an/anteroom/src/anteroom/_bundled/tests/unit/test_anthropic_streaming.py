"""Tests for AnthropicService streaming, retry, and error handling (#1021).

Covers the biggest coverage gap (~20%) in anthropic_provider.py:
stream_chat() timeouts, retries, cancel-awareness, error classification,
complete_with_usage(), and token refresh flows.
"""

from __future__ import annotations

import asyncio
import gc
import sys
from types import ModuleType
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from anteroom.config import AIConfig

# Create a mock anthropic module so tests work without the optional dependency.
# The service itself guards with HAS_ANTHROPIC; tests patch it to True.
if "anthropic" not in sys.modules:
    _mock_anthropic = ModuleType("anthropic")

    class _StubError(Exception):
        """Stub exception that accepts arbitrary kwargs like the real SDK."""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            self.status_code = kwargs.get("status_code", 0)
            self.response = kwargs.get("response", None)
            self.request = kwargs.get("request", None)
            self.message = kwargs.get("message", "")
            self.body = kwargs.get("body", None)
            super().__init__(self.message or str(args))

    for _exc_name in (
        "APIConnectionError",
        "APIStatusError",
        "APITimeoutError",
        "AuthenticationError",
        "BadRequestError",
        "RateLimitError",
    ):
        setattr(_mock_anthropic, _exc_name, type(_exc_name, (_StubError,), {}))
    setattr(_mock_anthropic, "Anthropic", MagicMock)
    sys.modules["anthropic"] = _mock_anthropic


def _make_config(**overrides: Any) -> AIConfig:
    defaults: dict[str, Any] = {
        "base_url": "https://api.anthropic.com",
        "api_key": "test-key",
        "model": "claude-sonnet-4-20250514",
        "provider": "anthropic",
        "max_output_tokens": 4096,
        "request_timeout": 120,
        "retry_max_attempts": 0,
        "retry_backoff_base": 1.0,
        "chunk_stall_timeout": 45,
    }
    defaults.update(overrides)
    return AIConfig(**defaults)


class _AsyncEventIterator:
    """Async iterator that yields events from a list."""

    def __init__(self, events: list[Any]) -> None:
        self._events = list(events)
        self._index = 0

    def __aiter__(self) -> "_AsyncEventIterator":
        return self

    async def __anext__(self) -> Any:
        if self._index >= len(self._events):
            raise StopAsyncIteration
        event = self._events[self._index]
        self._index += 1
        return event


def _make_mock_stream_context(events: list[Any]) -> MagicMock:
    event_iter = _AsyncEventIterator(events)
    mock_ctx = MagicMock()
    mock_ctx.__aenter__ = AsyncMock(return_value=event_iter)
    mock_ctx.__aexit__ = AsyncMock(return_value=False)
    return mock_ctx


def _make_service(**config_overrides: Any) -> Any:
    with (
        patch("anteroom.services.anthropic_provider.anthropic"),
        patch("anteroom.services.anthropic_provider.HAS_ANTHROPIC", True),
    ):
        config = _make_config(**config_overrides)
        from anteroom.services.anthropic_provider import AnthropicService

        svc = AnthropicService(config)
    return svc


async def _collect(gen: Any) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    async for event in gen:
        events.append(event)
    return events


def _text_event(text: str = "Hello") -> MagicMock:
    e = MagicMock()
    e.type = "content_block_delta"
    e.delta = MagicMock()
    e.delta.type = "text_delta"
    e.delta.text = text
    return e


def _msg_start(input_tokens: int = 100) -> MagicMock:
    e = MagicMock()
    e.type = "message_start"
    e.message = MagicMock()
    e.message.usage = MagicMock()
    e.message.usage.input_tokens = input_tokens
    return e


def _msg_delta(stop_reason: str = "end_turn", output_tokens: int = 50) -> MagicMock:
    e = MagicMock()
    e.type = "message_delta"
    e.delta = MagicMock()
    e.delta.stop_reason = stop_reason
    e.usage = MagicMock()
    e.usage.output_tokens = output_tokens
    return e


def _tool_block_start(tool_id: str = "tool_1", name: str = "read_file") -> MagicMock:
    e = MagicMock()
    e.type = "content_block_start"
    e.content_block = MagicMock()
    e.content_block.type = "tool_use"
    e.content_block.id = tool_id
    e.content_block.name = name
    return e


def _json_delta(partial: str) -> MagicMock:
    e = MagicMock()
    e.type = "content_block_delta"
    e.delta = MagicMock()
    e.delta.type = "input_json_delta"
    e.delta.partial_json = partial
    return e


# ---------------------------------------------------------------------------
# Streaming: successful paths
# ---------------------------------------------------------------------------


class TestStreamChatSuccess:
    @pytest.mark.asyncio
    async def test_text_stream_yields_phase_token_done(self) -> None:
        svc = _make_service()
        events_list = [_text_event("Hi"), _msg_delta("end_turn", 5)]
        svc.client.messages.stream = MagicMock(return_value=_make_mock_stream_context(events_list))

        events = await _collect(svc.stream_chat([{"role": "user", "content": "Hi"}]))
        types = [e["event"] for e in events]
        assert "phase" in types
        assert "token" in types
        assert "done" in types

    @pytest.mark.asyncio
    async def test_tool_use_yields_tool_call_event(self) -> None:
        svc = _make_service()
        events_list = [
            _tool_block_start("t1", "bash"),
            _json_delta('{"cmd": "ls"}'),
            _msg_delta("tool_use", 10),
        ]
        svc.client.messages.stream = MagicMock(return_value=_make_mock_stream_context(events_list))

        events = await _collect(
            svc.stream_chat(
                [{"role": "user", "content": "list"}],
                tools=[{"type": "function", "function": {"name": "bash", "description": "", "parameters": {}}}],
            )
        )
        tc_events = [e for e in events if e["event"] == "tool_call"]
        assert len(tc_events) == 1
        assert tc_events[0]["data"]["function_name"] == "bash"
        assert tc_events[0]["data"]["arguments"] == {"cmd": "ls"}

    @pytest.mark.asyncio
    async def test_tool_args_accumulation_across_chunks(self) -> None:
        svc = _make_service()
        events_list = [
            _tool_block_start("t1", "grep"),
            _json_delta('{"patt'),
            _json_delta('ern": "foo"}'),
            _msg_delta("tool_use", 10),
        ]
        svc.client.messages.stream = MagicMock(return_value=_make_mock_stream_context(events_list))

        events = await _collect(svc.stream_chat([{"role": "user", "content": "search"}]))
        tc = [e for e in events if e["event"] == "tool_call"]
        assert len(tc) == 1
        assert tc[0]["data"]["arguments"] == {"pattern": "foo"}

    @pytest.mark.asyncio
    async def test_tool_call_args_delta_events_emitted(self) -> None:
        svc = _make_service()
        events_list = [
            _tool_block_start("t1", "read_file"),
            _json_delta('{"path":'),
            _json_delta(' "/tmp"}'),
            _msg_delta("tool_use", 5),
        ]
        svc.client.messages.stream = MagicMock(return_value=_make_mock_stream_context(events_list))

        events = await _collect(svc.stream_chat([{"role": "user", "content": "read"}]))
        deltas = [e for e in events if e["event"] == "tool_call_args_delta"]
        assert len(deltas) == 2
        assert deltas[0]["data"]["tool_name"] == "read_file"

    @pytest.mark.asyncio
    async def test_usage_with_message_start_and_delta(self) -> None:
        svc = _make_service()
        events_list = [_msg_start(200), _text_event("ok"), _msg_delta("end_turn", 30)]
        svc.client.messages.stream = MagicMock(return_value=_make_mock_stream_context(events_list))

        events = await _collect(svc.stream_chat([{"role": "user", "content": "hi"}]))
        usage = [e for e in events if e["event"] == "usage"]
        assert len(usage) == 1
        assert usage[0]["data"]["prompt_tokens"] == 200
        assert usage[0]["data"]["completion_tokens"] == 30
        assert usage[0]["data"]["total_tokens"] == 230

    @pytest.mark.asyncio
    async def test_usage_emitted_on_tool_use_stop(self) -> None:
        svc = _make_service()
        events_list = [
            _msg_start(50),
            _tool_block_start("t1", "bash"),
            _json_delta("{}"),
            _msg_delta("tool_use", 10),
        ]
        svc.client.messages.stream = MagicMock(return_value=_make_mock_stream_context(events_list))

        events = await _collect(svc.stream_chat([{"role": "user", "content": "run"}]))
        usage = [e for e in events if e["event"] == "usage"]
        assert len(usage) == 1

    @pytest.mark.asyncio
    async def test_stream_ends_without_stop_reason_yields_done(self) -> None:
        svc = _make_service()
        svc.client.messages.stream = MagicMock(return_value=_make_mock_stream_context([_text_event("partial")]))

        events = await _collect(svc.stream_chat([{"role": "user", "content": "hi"}]))
        assert any(e["event"] == "done" for e in events)

    @pytest.mark.asyncio
    async def test_multiple_tool_calls_in_order(self) -> None:
        svc = _make_service()
        events_list = [
            _tool_block_start("t1", "read_file"),
            _json_delta('{"path": "/a"}'),
            _tool_block_start("t2", "grep"),
            _json_delta('{"pattern": "x"}'),
            _msg_delta("tool_use", 20),
        ]
        svc.client.messages.stream = MagicMock(return_value=_make_mock_stream_context(events_list))

        events = await _collect(svc.stream_chat([{"role": "user", "content": "do both"}]))
        tc = [e for e in events if e["event"] == "tool_call"]
        assert len(tc) == 2
        assert tc[0]["data"]["function_name"] == "read_file"
        assert tc[1]["data"]["function_name"] == "grep"


# ---------------------------------------------------------------------------
# Cancel handling
# ---------------------------------------------------------------------------


class TestStreamChatCancel:
    @pytest.mark.asyncio
    async def test_cancel_before_stream_returns_empty(self) -> None:
        svc = _make_service()
        cancel = asyncio.Event()
        cancel.set()

        events = await _collect(svc.stream_chat([{"role": "user", "content": "hi"}], cancel_event=cancel))
        assert events == []

    @pytest.mark.asyncio
    async def test_cancel_during_connect_returns_early(self) -> None:
        svc = _make_service(request_timeout=5)
        cancel = asyncio.Event()

        async def slow_enter() -> Any:
            cancel.set()
            await asyncio.sleep(10)
            return _AsyncEventIterator([])

        mock_ctx = MagicMock()
        mock_ctx.__aenter__ = AsyncMock(side_effect=slow_enter)
        mock_ctx.__aexit__ = AsyncMock(return_value=False)
        svc.client.messages.stream = MagicMock(return_value=mock_ctx)

        events = await _collect(svc.stream_chat([{"role": "user", "content": "hi"}], cancel_event=cancel))
        types = [e["event"] for e in events]
        assert "error" not in types

    @pytest.mark.asyncio
    async def test_cancel_during_iteration(self) -> None:
        svc = _make_service(chunk_stall_timeout=5)
        cancel = asyncio.Event()

        class _CancellingIterator:
            def __init__(self) -> None:
                self._count = 0

            def __aiter__(self) -> "_CancellingIterator":
                return self

            async def __anext__(self) -> Any:
                self._count += 1
                if self._count == 1:
                    return _text_event("hi")
                # Set cancel and then block so the cancel event wins the race
                cancel.set()
                await asyncio.sleep(10)
                raise StopAsyncIteration

        mock_ctx = MagicMock()
        mock_ctx.__aenter__ = AsyncMock(return_value=_CancellingIterator())
        mock_ctx.__aexit__ = AsyncMock(return_value=False)
        svc.client.messages.stream = MagicMock(return_value=mock_ctx)

        events = await _collect(svc.stream_chat([{"role": "user", "content": "hi"}], cancel_event=cancel))
        # Should have gotten at least the first token before cancel
        assert any(e["event"] == "token" for e in events)
        # Should NOT have an error since we cancelled cleanly
        assert not any(e["event"] == "error" for e in events)

    @pytest.mark.asyncio
    async def test_cancel_during_iteration_suppresses_late_task_exception(self) -> None:
        svc = _make_service(chunk_stall_timeout=5)
        cancel = asyncio.Event()
        loop = asyncio.get_running_loop()
        previous_handler = loop.get_exception_handler()
        loop_errors: list[dict[str, object]] = []

        class _LateExplodingIterator:
            def __init__(self) -> None:
                self._count = 0

            def __aiter__(self) -> "_LateExplodingIterator":
                return self

            async def __anext__(self) -> Any:
                self._count += 1
                if self._count == 1:
                    return _text_event("hi")
                try:
                    await asyncio.sleep(10)
                except asyncio.CancelledError as exc:
                    raise RuntimeError("late anthropic stream boom") from exc
                raise StopAsyncIteration

        mock_ctx = MagicMock()
        mock_ctx.__aenter__ = AsyncMock(return_value=_LateExplodingIterator())
        mock_ctx.__aexit__ = AsyncMock(return_value=False)
        svc.client.messages.stream = MagicMock(return_value=mock_ctx)

        loop.set_exception_handler(lambda _loop, context: loop_errors.append(context))
        try:

            async def _trip_cancel() -> None:
                await asyncio.sleep(0.05)
                cancel.set()

            trip_task = asyncio.create_task(_trip_cancel())
            events = await _collect(svc.stream_chat([{"role": "user", "content": "hi"}], cancel_event=cancel))
            await asyncio.wait_for(trip_task, timeout=1.0)
            await asyncio.sleep(0.05)
            gc.collect()
            await asyncio.sleep(0.05)
        finally:
            loop.set_exception_handler(previous_handler)

        assert any(e["event"] == "token" for e in events)
        assert not any(e["event"] == "error" for e in events)
        assert loop_errors == []


# ---------------------------------------------------------------------------
# Timeout handling
# ---------------------------------------------------------------------------


class TestStreamChatTimeouts:
    @pytest.mark.asyncio
    async def test_connect_timeout_retries_then_errors(self) -> None:
        from anthropic import APITimeoutError as RealTimeoutError

        svc = _make_service(request_timeout=0.1, retry_max_attempts=1, retry_backoff_base=0.01)

        mock_ctx = MagicMock()
        mock_ctx.__aenter__ = AsyncMock(side_effect=RealTimeoutError.__new__(RealTimeoutError))
        mock_ctx.__aexit__ = AsyncMock(return_value=False)

        with patch.object(type(svc), "_build_client", lambda self: None):
            svc.client.messages.stream = MagicMock(return_value=mock_ctx)
            events = await _collect(svc.stream_chat([{"role": "user", "content": "hi"}]))

        error_events = [e for e in events if e["event"] == "error"]
        assert len(error_events) == 1
        assert error_events[0]["data"]["code"] == "timeout"

    @pytest.mark.asyncio
    async def test_chunk_stall_yields_error(self) -> None:
        svc = _make_service(chunk_stall_timeout=0.1)

        class _StallingIterator:
            def __init__(self) -> None:
                self._yielded = False

            def __aiter__(self) -> "_StallingIterator":
                return self

            async def __anext__(self) -> Any:
                if not self._yielded:
                    self._yielded = True
                    return _text_event("start")
                await asyncio.sleep(10)
                raise StopAsyncIteration

        mock_ctx = MagicMock()
        mock_ctx.__aenter__ = AsyncMock(return_value=_StallingIterator())
        mock_ctx.__aexit__ = AsyncMock(return_value=False)
        svc.client.messages.stream = MagicMock(return_value=mock_ctx)

        events = await _collect(svc.stream_chat([{"role": "user", "content": "hi"}]))
        error_events = [e for e in events if e["event"] == "error"]
        assert len(error_events) == 1
        assert error_events[0]["data"]["code"] == "stream_stall"
        assert error_events[0]["data"]["retryable"] is True


# ---------------------------------------------------------------------------
# Retry with backoff
# ---------------------------------------------------------------------------


class TestStreamChatRetry:
    @pytest.mark.asyncio
    async def test_max_retries_exhausted_yields_error(self) -> None:
        from anthropic import APITimeoutError as RealTimeoutError

        svc = _make_service(retry_max_attempts=1, retry_backoff_base=0.01)

        mock_ctx = MagicMock()
        mock_ctx.__aenter__ = AsyncMock(side_effect=RealTimeoutError.__new__(RealTimeoutError))
        mock_ctx.__aexit__ = AsyncMock(return_value=False)

        with patch.object(type(svc), "_build_client", lambda self: None):
            svc.client.messages.stream = MagicMock(return_value=mock_ctx)
            events = await _collect(svc.stream_chat([{"role": "user", "content": "hi"}]))

        error = [e for e in events if e["event"] == "error"]
        assert len(error) == 1
        assert "attempts" in error[0]["data"]["message"]


# ---------------------------------------------------------------------------
# Error classification
# ---------------------------------------------------------------------------


class TestStreamChatErrors:
    @pytest.mark.asyncio
    async def test_auth_error_yields_auth_failed(self) -> None:
        import httpx
        from anthropic import AuthenticationError as RealAuthError

        svc = _make_service()
        exc = RealAuthError(
            message="invalid key",
            response=httpx.Response(401, request=httpx.Request("POST", "https://test")),
            body=None,
        )
        mock_ctx = MagicMock()
        mock_ctx.__aenter__ = AsyncMock(side_effect=exc)
        mock_ctx.__aexit__ = AsyncMock(return_value=False)
        svc.client.messages.stream = MagicMock(return_value=mock_ctx)

        events = await _collect(svc.stream_chat([{"role": "user", "content": "hi"}]))
        err = [e for e in events if e["event"] == "error"]
        assert len(err) == 1
        assert err[0]["data"]["code"] == "auth_failed"
        assert err[0]["data"]["retryable"] is False

    @pytest.mark.asyncio
    async def test_auth_error_with_token_refresh(self) -> None:
        import httpx
        from anthropic import AuthenticationError as RealAuthError

        with (
            patch("anteroom.services.anthropic_provider.anthropic"),
            patch("anteroom.services.anthropic_provider.HAS_ANTHROPIC", True),
        ):
            config = _make_config()
            from anteroom.services.anthropic_provider import AnthropicService

            mock_tp = MagicMock()
            mock_tp.get_token.return_value = "old-key"
            svc = AnthropicService(config, token_provider=mock_tp)

        exc = RealAuthError(
            message="invalid",
            response=httpx.Response(401, request=httpx.Request("POST", "https://test")),
            body=None,
        )

        call_count = 0

        def side_effect(**kwargs: Any) -> MagicMock:
            nonlocal call_count
            call_count += 1
            if call_count <= 1:
                m = MagicMock()
                m.__aenter__ = AsyncMock(side_effect=exc)
                m.__aexit__ = AsyncMock(return_value=False)
                return m
            return _make_mock_stream_context([_text_event("ok"), _msg_delta("end_turn", 1)])

        with patch.object(type(svc), "_build_client", lambda self: None):
            svc.client.messages.stream = MagicMock(side_effect=side_effect)
            events = await _collect(svc.stream_chat([{"role": "user", "content": "hi"}]))

        assert any(e["event"] == "done" for e in events)

    @pytest.mark.asyncio
    async def test_rate_limit_yields_rate_limit_event(self) -> None:
        import httpx
        from anthropic import RateLimitError as RealRateLimitError

        svc = _make_service()
        exc = RealRateLimitError(
            message="rate limited",
            response=httpx.Response(429, request=httpx.Request("POST", "https://test")),
            body=None,
        )
        mock_ctx = MagicMock()
        mock_ctx.__aenter__ = AsyncMock(side_effect=exc)
        mock_ctx.__aexit__ = AsyncMock(return_value=False)
        svc.client.messages.stream = MagicMock(return_value=mock_ctx)

        events = await _collect(svc.stream_chat([{"role": "user", "content": "hi"}]))
        err = [e for e in events if e["event"] == "error"]
        assert len(err) == 1
        assert err[0]["data"]["code"] == "rate_limit"
        assert err[0]["data"]["retryable"] is True

    @pytest.mark.asyncio
    async def test_rate_limit_cancelled_returns_empty(self) -> None:
        import httpx
        from anthropic import RateLimitError as RealRateLimitError

        svc = _make_service()
        cancel = asyncio.Event()
        cancel.set()
        exc = RealRateLimitError(
            message="rate limited",
            response=httpx.Response(429, request=httpx.Request("POST", "https://test")),
            body=None,
        )
        mock_ctx = MagicMock()
        mock_ctx.__aenter__ = AsyncMock(side_effect=exc)
        mock_ctx.__aexit__ = AsyncMock(return_value=False)
        svc.client.messages.stream = MagicMock(return_value=mock_ctx)

        events = await _collect(svc.stream_chat([{"role": "user", "content": "hi"}], cancel_event=cancel))
        assert not any(e["event"] == "error" for e in events)

    @pytest.mark.asyncio
    async def test_4xx_non_retryable_yields_api_error(self) -> None:
        import httpx
        from anthropic import APIStatusError as RealStatusError

        svc = _make_service()
        exc = RealStatusError(
            message="not found",
            response=httpx.Response(404, request=httpx.Request("POST", "https://test")),
            body=None,
        )
        mock_ctx = MagicMock()
        mock_ctx.__aenter__ = AsyncMock(side_effect=exc)
        mock_ctx.__aexit__ = AsyncMock(return_value=False)
        svc.client.messages.stream = MagicMock(return_value=mock_ctx)

        events = await _collect(svc.stream_chat([{"role": "user", "content": "hi"}]))
        err = [e for e in events if e["event"] == "error"]
        assert len(err) == 1
        assert err[0]["data"]["code"] == "api_error"
        assert err[0]["data"]["retryable"] is False

    @pytest.mark.asyncio
    async def test_connection_error_retries(self) -> None:
        from anthropic import APIConnectionError as RealConnError

        svc = _make_service(retry_max_attempts=1, retry_backoff_base=0.01)

        call_count = 0

        def side_effect(**kwargs: Any) -> MagicMock:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                m = MagicMock()
                m.__aenter__ = AsyncMock(side_effect=RealConnError(request=MagicMock()))
                m.__aexit__ = AsyncMock(return_value=False)
                return m
            return _make_mock_stream_context([_text_event("ok"), _msg_delta("end_turn", 1)])

        with patch.object(type(svc), "_build_client", lambda self: None):
            svc.client.messages.stream = MagicMock(side_effect=side_effect)
            events = await _collect(svc.stream_chat([{"role": "user", "content": "hi"}]))

        assert any(e["event"] == "retrying" for e in events)
        assert any(e["event"] == "done" for e in events)

    @pytest.mark.asyncio
    async def test_generic_exception_yields_internal_error(self) -> None:
        svc = _make_service()
        mock_ctx = MagicMock()
        mock_ctx.__aenter__ = AsyncMock(side_effect=RuntimeError("crash"))
        mock_ctx.__aexit__ = AsyncMock(return_value=False)
        svc.client.messages.stream = MagicMock(return_value=mock_ctx)

        events = await _collect(svc.stream_chat([{"role": "user", "content": "hi"}]))
        err = [e for e in events if e["event"] == "error"]
        assert len(err) == 1
        assert err[0]["data"]["retryable"] is False

    @pytest.mark.asyncio
    async def test_bad_tool_json_parsed_as_empty(self) -> None:
        svc = _make_service()
        events_list = [
            _tool_block_start("t1", "bash"),
            _json_delta("not valid json"),
            _msg_delta("tool_use", 5),
        ]
        svc.client.messages.stream = MagicMock(return_value=_make_mock_stream_context(events_list))

        events = await _collect(svc.stream_chat([{"role": "user", "content": "run"}]))
        tc = [e for e in events if e["event"] == "tool_call"]
        assert len(tc) == 1
        assert tc[0]["data"]["arguments"] == {}


# ---------------------------------------------------------------------------
# validate_connection() errors
# ---------------------------------------------------------------------------


class TestValidateConnectionErrors:
    @pytest.mark.asyncio
    async def test_timeout_returns_false(self) -> None:
        from anthropic import APITimeoutError as RealTimeoutError

        svc = _make_service()
        svc.client.messages.create = AsyncMock(side_effect=RealTimeoutError.__new__(RealTimeoutError))

        with patch.object(type(svc), "_build_client", lambda self: None):
            ok, msg, models = await svc.validate_connection()
        assert ok is False
        assert "timed out" in msg.lower()

    @pytest.mark.asyncio
    async def test_connection_error_returns_false(self) -> None:
        from anthropic import APIConnectionError as RealConnError

        svc = _make_service()
        svc.client.messages.create = AsyncMock(side_effect=RealConnError(request=MagicMock()))

        with patch.object(type(svc), "_build_client", lambda self: None):
            ok, msg, models = await svc.validate_connection()
        assert ok is False
        assert "connect" in msg.lower()

    @pytest.mark.asyncio
    async def test_auth_error_with_refresh(self) -> None:
        import httpx
        from anthropic import AuthenticationError as RealAuthError

        with (
            patch("anteroom.services.anthropic_provider.anthropic"),
            patch("anteroom.services.anthropic_provider.HAS_ANTHROPIC", True),
        ):
            config = _make_config()
            from anteroom.services.anthropic_provider import AnthropicService

            mock_tp = MagicMock()
            mock_tp.get_token.return_value = "key"
            svc = AnthropicService(config, token_provider=mock_tp)

        exc = RealAuthError(
            message="bad key",
            response=httpx.Response(401, request=httpx.Request("POST", "https://test")),
            body=None,
        )

        call_count = 0

        async def fake_create(**kwargs: Any) -> MagicMock:
            nonlocal call_count
            call_count += 1
            if call_count <= 1:
                raise exc
            resp = MagicMock()
            resp.content = [MagicMock(text="hi")]
            return resp

        with patch.object(type(svc), "_build_client", lambda self: None):
            svc.client.messages.create = fake_create
            ok, msg, models = await svc.validate_connection()

        assert ok is True


# ---------------------------------------------------------------------------
# complete_with_usage()
# ---------------------------------------------------------------------------


class TestCompleteWithUsage:
    @pytest.mark.asyncio
    async def test_returns_text_and_usage(self) -> None:
        svc = _make_service()
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="summary")]
        mock_response.usage = MagicMock()
        mock_response.usage.input_tokens = 100
        mock_response.usage.output_tokens = 50
        svc.client.messages.create = AsyncMock(return_value=mock_response)

        text, usage = await svc.complete_with_usage(
            [{"role": "user", "content": "summarize"}],
            max_completion_tokens=500,
        )
        assert text == "summary"
        assert usage["prompt_tokens"] == 100
        assert usage["completion_tokens"] == 50
        assert usage["total_tokens"] == 150

    @pytest.mark.asyncio
    async def test_with_system_prompt(self) -> None:
        svc = _make_service()
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="ok")]
        mock_response.usage = MagicMock()
        mock_response.usage.input_tokens = 10
        mock_response.usage.output_tokens = 5
        svc.client.messages.create = AsyncMock(return_value=mock_response)

        text, usage = await svc.complete_with_usage(
            [{"role": "system", "content": "be brief"}, {"role": "user", "content": "hi"}],
        )
        assert text == "ok"
        call_kwargs = svc.client.messages.create.call_args[1]
        assert "system" in call_kwargs

    @pytest.mark.asyncio
    async def test_with_temperature(self) -> None:
        svc = _make_service()
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="creative")]
        mock_response.usage = MagicMock()
        mock_response.usage.input_tokens = 10
        mock_response.usage.output_tokens = 5
        svc.client.messages.create = AsyncMock(return_value=mock_response)

        await svc.complete_with_usage(
            [{"role": "user", "content": "hi"}],
            temperature=0.9,
        )
        call_kwargs = svc.client.messages.create.call_args[1]
        assert call_kwargs["temperature"] == 0.9

    @pytest.mark.asyncio
    async def test_empty_response_returns_none(self) -> None:
        svc = _make_service()
        mock_response = MagicMock()
        mock_response.content = []
        mock_response.usage = MagicMock()
        mock_response.usage.input_tokens = 10
        mock_response.usage.output_tokens = 0
        svc.client.messages.create = AsyncMock(return_value=mock_response)

        text, usage = await svc.complete_with_usage([{"role": "user", "content": "hi"}])
        assert text is None

    @pytest.mark.asyncio
    async def test_auth_error_with_refresh_retries(self) -> None:
        import httpx
        from anthropic import AuthenticationError as RealAuthError

        with (
            patch("anteroom.services.anthropic_provider.anthropic"),
            patch("anteroom.services.anthropic_provider.HAS_ANTHROPIC", True),
        ):
            config = _make_config()
            from anteroom.services.anthropic_provider import AnthropicService

            mock_tp = MagicMock()
            mock_tp.get_token.return_value = "key"
            svc = AnthropicService(config, token_provider=mock_tp)

        exc = RealAuthError(
            message="bad",
            response=httpx.Response(401, request=httpx.Request("POST", "https://test")),
            body=None,
        )

        call_count = 0

        async def fake_create(**kwargs: Any) -> MagicMock:
            nonlocal call_count
            call_count += 1
            if call_count <= 1:
                raise exc
            resp = MagicMock()
            resp.content = [MagicMock(text="ok")]
            resp.usage = MagicMock()
            resp.usage.input_tokens = 10
            resp.usage.output_tokens = 5
            return resp

        with patch.object(type(svc), "_build_client", lambda self: None):
            svc.client.messages.create = fake_create
            text, usage = await svc.complete_with_usage([{"role": "user", "content": "hi"}])

        assert text == "ok"

    @pytest.mark.asyncio
    async def test_auth_error_no_refresh_raises(self) -> None:
        import httpx
        from anthropic import AuthenticationError as RealAuthError

        svc = _make_service()
        exc = RealAuthError(
            message="bad key",
            response=httpx.Response(401, request=httpx.Request("POST", "https://test")),
            body=None,
        )
        svc.client.messages.create = AsyncMock(side_effect=exc)

        with pytest.raises(type(exc)):
            await svc.complete_with_usage([{"role": "user", "content": "hi"}])


# ---------------------------------------------------------------------------
# Egress and token provider
# ---------------------------------------------------------------------------


class TestEgressAndTokenProvider:
    def test_egress_blocked_raises(self) -> None:
        with (
            patch("anteroom.services.anthropic_provider.anthropic"),
            patch("anteroom.services.anthropic_provider.HAS_ANTHROPIC", True),
            patch("anteroom.services.anthropic_provider.check_egress_allowed", return_value=False),
        ):
            config = _make_config(allowed_domains=["safe.example.com"])
            from anteroom.services.anthropic_provider import AnthropicService

            with pytest.raises(ValueError, match="Egress blocked"):
                AnthropicService(config)

    def test_token_provider_used_for_api_key(self) -> None:
        with (
            patch("anteroom.services.anthropic_provider.anthropic"),
            patch("anteroom.services.anthropic_provider.HAS_ANTHROPIC", True),
        ):
            config = _make_config()
            from anteroom.services.anthropic_provider import AnthropicService

            mock_tp = MagicMock()
            mock_tp.get_token.return_value = "dynamic-key"
            svc = AnthropicService(config, token_provider=mock_tp)
            assert svc._resolve_api_key() == "dynamic-key"

    def test_try_refresh_with_provider_success(self) -> None:
        with (
            patch("anteroom.services.anthropic_provider.anthropic"),
            patch("anteroom.services.anthropic_provider.HAS_ANTHROPIC", True),
        ):
            config = _make_config()
            from anteroom.services.anthropic_provider import AnthropicService

            mock_tp = MagicMock()
            mock_tp.get_token.return_value = "key"
            svc = AnthropicService(config, token_provider=mock_tp)
            assert svc._try_refresh_token() is True

    def test_try_refresh_with_provider_failure(self) -> None:
        from anteroom.services.token_provider import TokenProviderError

        with (
            patch("anteroom.services.anthropic_provider.anthropic"),
            patch("anteroom.services.anthropic_provider.HAS_ANTHROPIC", True),
        ):
            config = _make_config()
            from anteroom.services.anthropic_provider import AnthropicService

            mock_tp = MagicMock()
            mock_tp.get_token.return_value = "key"
            mock_tp.refresh.side_effect = TokenProviderError("fail")
            svc = AnthropicService(config, token_provider=mock_tp)
            assert svc._try_refresh_token() is False
