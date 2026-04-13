"""Tests for AIService retry logic, timeouts, and cancel handling (#1021)."""

from __future__ import annotations

import asyncio
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from anteroom.config import AIConfig
from anteroom.services.ai_service import AIService, _is_html_error


def _make_config(**overrides: Any) -> AIConfig:
    defaults: dict[str, Any] = {
        "base_url": "http://localhost:11434/v1",
        "api_key": "test-key",
        "model": "gpt-4",
        "request_timeout": 120,
        "verify_ssl": True,
        "retry_max_attempts": 0,
        "retry_backoff_base": 0.01,
        "first_token_timeout": 60,
        "chunk_stall_timeout": 45,
    }
    defaults.update(overrides)
    return AIConfig(**defaults)


def _make_service(**config_overrides: Any) -> AIService:
    config = _make_config(**config_overrides)
    svc = AIService.__new__(AIService)
    svc.config = config
    svc._token_provider = None
    svc.client = MagicMock()
    return svc


async def _collect(gen: Any) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    async for e in gen:
        events.append(e)
    return events


class _MockChunk:
    def __init__(
        self,
        content: str | None = None,
        finish_reason: str | None = None,
        tool_calls: list[Any] | None = None,
        usage: Any = None,
    ) -> None:
        delta = MagicMock()
        delta.content = content
        delta.tool_calls = tool_calls
        choice = MagicMock()
        choice.delta = delta
        choice.finish_reason = finish_reason
        self.choices = [choice]
        self.usage = usage


class _AsyncChunkIter:
    def __init__(self, chunks: list[Any]) -> None:
        self._chunks = list(chunks)
        self._index = 0

    def __aiter__(self) -> "_AsyncChunkIter":
        return self

    async def __anext__(self) -> Any:
        if self._index >= len(self._chunks):
            raise StopAsyncIteration
        c = self._chunks[self._index]
        self._index += 1
        return c

    async def aclose(self) -> None:
        pass


# ---------------------------------------------------------------------------
# Retry with exponential backoff
# ---------------------------------------------------------------------------


class TestRetryBackoff:
    @pytest.mark.asyncio
    async def test_retry_on_timeout_then_success(self) -> None:
        from openai import APITimeoutError

        svc = _make_service(retry_max_attempts=1, retry_backoff_base=0.01, first_token_timeout=60)

        call_count = 0
        usage = MagicMock()
        usage.prompt_tokens = 10
        usage.completion_tokens = 5
        usage.total_tokens = 15

        async def fake_create(**kwargs: Any) -> Any:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise APITimeoutError(request=MagicMock())
            return _AsyncChunkIter([_MockChunk(content="hi"), _MockChunk(finish_reason="stop", usage=usage)])

        # Patch _build_client to re-apply our fake_create after client rebuild
        def patched_build() -> None:
            svc.client = MagicMock()
            svc.client.chat.completions.create = AsyncMock(side_effect=fake_create)

        svc._build_client = patched_build
        svc.client.chat.completions.create = AsyncMock(side_effect=fake_create)
        events = await _collect(svc.stream_chat([{"role": "user", "content": "hi"}]))

        retrying = [e for e in events if e["event"] == "retrying"]
        assert len(retrying) == 1
        assert retrying[0]["data"]["delay"] == pytest.approx(0.01, abs=0.001)
        assert any(e["event"] == "done" for e in events)

    @pytest.mark.asyncio
    async def test_exponential_backoff_delay(self) -> None:
        from openai import APITimeoutError

        svc = _make_service(retry_max_attempts=2, retry_backoff_base=0.01)

        def patched_build() -> None:
            svc.client = MagicMock()
            svc.client.chat.completions.create = AsyncMock(side_effect=APITimeoutError(request=MagicMock()))

        svc._build_client = patched_build
        svc.client.chat.completions.create = AsyncMock(side_effect=APITimeoutError(request=MagicMock()))
        events = await _collect(svc.stream_chat([{"role": "user", "content": "hi"}]))

        retrying = [e for e in events if e["event"] == "retrying"]
        assert len(retrying) == 2
        assert retrying[0]["data"]["delay"] == pytest.approx(0.01, abs=0.001)
        assert retrying[1]["data"]["delay"] == pytest.approx(0.02, abs=0.001)


# ---------------------------------------------------------------------------
# First-token timeout
# ---------------------------------------------------------------------------


class TestFirstTokenTimeout:
    @pytest.mark.asyncio
    async def test_first_token_timeout_yields_error(self) -> None:
        svc = _make_service(first_token_timeout=0.05, request_timeout=0.05)

        class _SlowStream:
            def __aiter__(self) -> "_SlowStream":
                return self

            async def __anext__(self) -> Any:
                await asyncio.sleep(10)
                raise StopAsyncIteration

            async def close(self) -> None:
                pass

        svc.client.chat.completions.create = AsyncMock(return_value=_SlowStream())
        events = await _collect(svc.stream_chat([{"role": "user", "content": "hi"}]))

        error = [e for e in events if e["event"] == "error"]
        assert len(error) == 1
        assert error[0]["data"]["code"] == "timeout"


# ---------------------------------------------------------------------------
# Cancel at various phases
# ---------------------------------------------------------------------------


class TestCancelAtPhases:
    @pytest.mark.asyncio
    async def test_cancel_before_create(self) -> None:
        svc = _make_service()
        cancel = asyncio.Event()
        cancel.set()

        events = await _collect(svc.stream_chat([{"role": "user", "content": "hi"}], cancel_event=cancel))
        assert events == []

    @pytest.mark.asyncio
    async def test_cancel_during_create(self) -> None:
        svc = _make_service()
        cancel = asyncio.Event()

        async def slow_create(**kwargs: Any) -> Any:
            cancel.set()
            await asyncio.sleep(10)

        svc.client.chat.completions.create = AsyncMock(side_effect=slow_create)
        events = await _collect(svc.stream_chat([{"role": "user", "content": "hi"}], cancel_event=cancel))
        assert not any(e["event"] == "error" for e in events)

    @pytest.mark.asyncio
    async def test_cancel_during_retry_backoff(self) -> None:
        from openai import APITimeoutError

        svc = _make_service(retry_max_attempts=2, retry_backoff_base=100)
        cancel = asyncio.Event()

        svc.client.chat.completions.create = AsyncMock(side_effect=APITimeoutError(request=MagicMock()))

        async def set_cancel_soon() -> None:
            await asyncio.sleep(0.05)
            cancel.set()

        task = asyncio.create_task(set_cancel_soon())
        events = await _collect(svc.stream_chat([{"role": "user", "content": "hi"}], cancel_event=cancel))
        await task

        assert not any(e["event"] == "error" for e in events)


# ---------------------------------------------------------------------------
# Token refresh on 401
# ---------------------------------------------------------------------------


class TestTokenRefresh:
    @pytest.mark.asyncio
    async def test_auth_error_triggers_refresh(self) -> None:
        from openai import AuthenticationError

        config = _make_config()
        mock_tp = MagicMock()
        mock_tp.get_token.return_value = "old-key"

        with patch("openai.AsyncOpenAI"):
            svc = AIService(config, token_provider=mock_tp)

        usage = MagicMock()
        usage.prompt_tokens = 10
        usage.completion_tokens = 5
        usage.total_tokens = 15
        call_count = 0

        async def fake_create(**kwargs: Any) -> Any:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise AuthenticationError(
                    message="invalid key",
                    response=httpx.Response(401, request=httpx.Request("POST", "http://test")),
                    body=None,
                )
            return _AsyncChunkIter([_MockChunk(content="ok"), _MockChunk(finish_reason="stop", usage=usage)])

        def patched_build() -> None:
            svc.client = MagicMock()
            svc.client.chat.completions.create = AsyncMock(side_effect=fake_create)

        svc._build_client = patched_build
        svc.client.chat.completions.create = AsyncMock(side_effect=fake_create)
        events = await _collect(svc.stream_chat([{"role": "user", "content": "hi"}]))
        assert any(e["event"] == "done" for e in events)


# ---------------------------------------------------------------------------
# Tool argument delta accumulation
# ---------------------------------------------------------------------------


class TestToolArgsDelta:
    @pytest.mark.asyncio
    async def test_args_accumulate_across_chunks(self) -> None:
        svc = _make_service()

        tc1 = MagicMock()
        tc1.index = 0
        tc1.id = "call_1"
        tc1.function = MagicMock()
        tc1.function.name = "read_file"
        tc1.function.arguments = '{"pa'

        tc2 = MagicMock()
        tc2.index = 0
        tc2.id = None
        tc2.function = MagicMock()
        tc2.function.name = None
        tc2.function.arguments = 'th": "/tmp"}'

        chunk1 = MagicMock()
        chunk1.choices = [MagicMock()]
        chunk1.choices[0].delta = MagicMock()
        chunk1.choices[0].delta.content = None
        chunk1.choices[0].delta.tool_calls = [tc1]
        chunk1.choices[0].finish_reason = None
        chunk1.usage = None

        chunk2 = MagicMock()
        chunk2.choices = [MagicMock()]
        chunk2.choices[0].delta = MagicMock()
        chunk2.choices[0].delta.content = None
        chunk2.choices[0].delta.tool_calls = [tc2]
        chunk2.choices[0].finish_reason = None
        chunk2.usage = None

        chunk3 = MagicMock()
        chunk3.choices = [MagicMock()]
        chunk3.choices[0].delta = MagicMock()
        chunk3.choices[0].delta.content = None
        chunk3.choices[0].delta.tool_calls = None
        chunk3.choices[0].finish_reason = "tool_calls"
        chunk3.usage = None

        svc.client.chat.completions.create = AsyncMock(return_value=_AsyncChunkIter([chunk1, chunk2, chunk3]))
        events = await _collect(svc.stream_chat([{"role": "user", "content": "hi"}]))

        tc_events = [e for e in events if e["event"] == "tool_call"]
        assert len(tc_events) == 1
        assert tc_events[0]["data"]["arguments"] == {"path": "/tmp"}

        delta_events = [e for e in events if e["event"] == "tool_call_args_delta"]
        assert len(delta_events) == 2


# ---------------------------------------------------------------------------
# HTML error detection
# ---------------------------------------------------------------------------


class TestHtmlErrorDetection:
    def test_html_doctype(self) -> None:
        exc = Exception("<!DOCTYPE html><html>error page</html>")
        assert _is_html_error(exc) is True

    def test_html_tag(self) -> None:
        exc = Exception("<html>Something went wrong</html>")
        assert _is_html_error(exc) is True

    def test_json_error(self) -> None:
        exc = Exception('{"error": "something failed"}')
        assert _is_html_error(exc) is False

    @pytest.mark.asyncio
    async def test_html_error_yields_specific_message(self) -> None:
        svc = _make_service()
        svc.client.chat.completions.create = AsyncMock(
            side_effect=Exception("<!doctype html><html>Gateway Error</html>")
        )

        events = await _collect(svc.stream_chat([{"role": "user", "content": "hi"}]))
        err = [e for e in events if e["event"] == "error"]
        assert len(err) == 1
        assert err[0]["data"]["code"] == "html_response"
        assert "HTML" in err[0]["data"]["message"]


# ---------------------------------------------------------------------------
# Server error (5xx) with retry
# ---------------------------------------------------------------------------


class TestServerErrorRetry:
    @pytest.mark.asyncio
    async def test_500_retries_and_exhausts(self) -> None:
        from openai import APIStatusError

        svc = _make_service(retry_max_attempts=1, retry_backoff_base=0.01)
        resp = httpx.Response(500, request=httpx.Request("POST", "http://test"))
        exc = APIStatusError(message="server error", response=resp, body=None)

        def patched_build() -> None:
            svc.client = MagicMock()
            svc.client.chat.completions.create = AsyncMock(side_effect=exc)

        svc._build_client = patched_build
        svc.client.chat.completions.create = AsyncMock(side_effect=exc)
        events = await _collect(svc.stream_chat([{"role": "user", "content": "hi"}]))

        retrying = [e for e in events if e["event"] == "retrying"]
        assert len(retrying) == 1
        error = [e for e in events if e["event"] == "error"]
        assert len(error) == 1
        assert error[0]["data"]["retryable"] is True
