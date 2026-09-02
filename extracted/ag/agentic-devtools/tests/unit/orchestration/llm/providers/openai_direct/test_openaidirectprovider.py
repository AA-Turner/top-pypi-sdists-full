"""Tests for OpenAIDirectProvider."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from agentic_devtools.orchestration.llm.errors import StreamInterruptedError, StructuredOutputValidationError
from agentic_devtools.orchestration.llm.providers.openai_direct import OpenAIDirectProvider
from agentic_devtools.orchestration.llm.types import LLMMessage, ProviderType


class TestOpenAIDirectProvider:
    """Tests for OpenAIDirectProvider."""

    def _make_provider(self):
        return OpenAIDirectProvider(
            api_key="test-key",
            model="gpt-4o-mini",
            temperature=0.5,
            max_tokens=500,
        )

    def _mock_response(self, text="Response"):
        response = MagicMock()
        choice = MagicMock()
        choice.message.content = text
        response.choices = [choice]
        response.model = "gpt-4o-mini"
        usage = MagicMock()
        usage.prompt_tokens = 20
        usage.completion_tokens = 10
        usage.total_tokens = 30
        response.usage = usage
        return response

    @pytest.mark.asyncio
    async def test_complete_returns_response(self):
        provider = self._make_provider()
        mock_response = self._mock_response()

        with patch.object(provider, "_get_client") as mock_client:
            mock_client.return_value.chat.completions.create = AsyncMock(return_value=mock_response)
            result = await provider.complete([LLMMessage(role="user", content="Hello")])

        assert result.text == "Response"
        assert result.provider_type == ProviderType.OPENAI_DIRECT
        assert result.usage is not None
        assert result.usage.total_tokens == 30

    @pytest.mark.asyncio
    async def test_complete_without_usage(self):
        provider = self._make_provider()
        response = MagicMock()
        choice = MagicMock()
        choice.message.content = "Hi"
        response.choices = [choice]
        response.model = "gpt-4o-mini"
        response.usage = None

        with patch.object(provider, "_get_client") as mock_client:
            mock_client.return_value.chat.completions.create = AsyncMock(return_value=response)
            result = await provider.complete([LLMMessage(role="user", content="Hello")])

        assert result.usage is None

    def test_get_client_lazy_init(self):
        provider = self._make_provider()
        with patch("openai.AsyncOpenAI") as mock_cls:
            mock_cls.return_value = MagicMock()
            client = provider._get_client()
            assert client is mock_cls.return_value
            client2 = provider._get_client()
            assert client2 is client
            mock_cls.assert_called_once()

    @pytest.mark.asyncio
    async def test_complete_uses_retry_wrapper(self):
        provider = self._make_provider()
        mock_response = self._mock_response()

        with (
            patch.object(provider, "_get_client") as mock_client,
            patch(
                "agentic_devtools.orchestration.llm.providers.openai_direct.execute_with_retry",
                new_callable=AsyncMock,
            ) as execute_with_retry_mock,
        ):
            create_mock = AsyncMock()
            mock_client.return_value.chat.completions.create = create_mock
            execute_with_retry_mock.return_value = mock_response

            await provider.complete([LLMMessage(role="user", content="Hello")])

        execute_with_retry_mock.assert_awaited_once()
        assert execute_with_retry_mock.await_args.args[0] is create_mock

    @pytest.mark.asyncio
    async def test_stream_uses_retry_wrapper(self):
        """stream() must use execute_with_retry for the initial create() call."""
        provider = self._make_provider()

        chunk = MagicMock()
        chunk.choices = [MagicMock()]
        chunk.choices[0].delta.content = "Hi"
        chunk.choices[0].finish_reason = "stop"
        chunk.usage = None

        async def mock_stream():
            yield chunk

        with (
            patch.object(provider, "_get_client") as mock_client,
            patch(
                "agentic_devtools.orchestration.llm.providers.openai_direct.execute_with_retry",
                new_callable=AsyncMock,
            ) as execute_with_retry_mock,
        ):
            create_mock = AsyncMock()
            mock_client.return_value.chat.completions.create = create_mock
            execute_with_retry_mock.return_value = mock_stream()

            async for _ in provider.stream([LLMMessage(role="user", content="Hi")]):
                pass

        execute_with_retry_mock.assert_awaited_once()
        assert execute_with_retry_mock.await_args.args[0] is create_mock

    def test_get_client_preserves_zero_timeout(self):
        """timeout_seconds=0 is passed through as-is, not replaced by the default."""
        provider = OpenAIDirectProvider(api_key="test-key", model="gpt-4o", timeout_seconds=0)
        with patch("openai.AsyncOpenAI") as mock_cls:
            mock_cls.return_value = MagicMock()
            provider._get_client()
        assert mock_cls.call_args[1]["timeout"] == 0

    def test_build_messages_with_name(self):
        provider = self._make_provider()
        messages = [LLMMessage(role="user", content="Hello", name="bob")]
        result = provider._build_messages(messages)
        assert result == [{"role": "user", "content": "Hello", "name": "bob"}]

    @pytest.mark.asyncio
    async def test_complete_without_temperature_and_max_tokens(self):
        """When temperature and max_tokens are None, they are not included in params."""
        provider = OpenAIDirectProvider(api_key="test-key", model="gpt-4o")
        mock_response = self._mock_response()

        with patch.object(provider, "_get_client") as mock_client:
            create_mock = AsyncMock(return_value=mock_response)
            mock_client.return_value.chat.completions.create = create_mock
            await provider.complete([LLMMessage(role="user", content="Hello")])

        call_kwargs = create_mock.call_args[1]
        assert "temperature" not in call_kwargs
        assert "max_tokens" not in call_kwargs

    @pytest.mark.asyncio
    async def test_complete_omits_explicit_none_kwargs(self):
        """Explicit None kwargs must not override configured provider defaults."""
        provider = self._make_provider()
        mock_response = self._mock_response()

        with patch.object(provider, "_get_client") as mock_client:
            create_mock = AsyncMock(return_value=mock_response)
            mock_client.return_value.chat.completions.create = create_mock
            await provider.complete(
                [LLMMessage(role="user", content="Hello")],
                temperature=None,
                max_tokens=None,
            )

        call_kwargs = create_mock.call_args[1]
        assert call_kwargs["temperature"] == 0.5
        assert call_kwargs["max_tokens"] == 500

    @pytest.mark.asyncio
    async def test_stream_without_temperature_and_max_tokens(self):
        """When temperature and max_tokens are None, they are not included in stream params."""
        provider = OpenAIDirectProvider(api_key="test-key", model="gpt-4o")

        chunk = MagicMock()
        chunk.choices = [MagicMock()]
        chunk.choices[0].delta.content = "Hi"
        chunk.choices[0].finish_reason = "stop"
        chunk.usage = None

        async def mock_stream():
            yield chunk

        with patch.object(provider, "_get_client") as mock_client:
            create_mock = AsyncMock(return_value=mock_stream())
            mock_client.return_value.chat.completions.create = create_mock
            async for _ in provider.stream([LLMMessage(role="user", content="Hi")]):
                pass

        call_kwargs = create_mock.call_args[1]
        assert "temperature" not in call_kwargs
        assert "max_tokens" not in call_kwargs

    @pytest.mark.asyncio
    async def test_stream_omits_explicit_none_kwargs(self):
        """Explicit None kwargs must not override configured stream defaults."""
        provider = self._make_provider()

        chunk = MagicMock()
        chunk.choices = [MagicMock()]
        chunk.choices[0].delta.content = "Hi"
        chunk.choices[0].finish_reason = "stop"
        chunk.usage = None

        async def mock_stream():
            yield chunk

        with patch.object(provider, "_get_client") as mock_client:
            create_mock = AsyncMock(return_value=mock_stream())
            mock_client.return_value.chat.completions.create = create_mock
            async for _ in provider.stream(
                [LLMMessage(role="user", content="Hi")],
                temperature=None,
                max_tokens=None,
            ):
                pass

        call_kwargs = create_mock.call_args[1]
        assert call_kwargs["temperature"] == 0.5
        assert call_kwargs["max_tokens"] == 500

    @pytest.mark.asyncio
    async def test_stream_skips_empty_chunk(self):
        """Chunks with no choices and no usage are skipped (loop continues)."""
        provider = self._make_provider()

        empty_chunk = MagicMock()
        empty_chunk.choices = []
        empty_chunk.usage = None

        content_chunk = MagicMock()
        content_chunk.choices = [MagicMock()]
        content_chunk.choices[0].delta.content = "Hello"
        content_chunk.choices[0].finish_reason = "stop"
        content_chunk.usage = None

        async def mock_stream():
            yield empty_chunk
            yield content_chunk

        with patch.object(provider, "_get_client") as mock_client:
            mock_client.return_value.chat.completions.create = AsyncMock(return_value=mock_stream())
            chunks = []
            async for c in provider.stream([LLMMessage(role="user", content="Hi")]):
                chunks.append(c)

        assert len(chunks) == 1
        assert chunks[0].text_delta == "Hello"

    @pytest.mark.asyncio
    async def test_complete_structured_valid(self):
        provider = self._make_provider()
        mock_response = self._mock_response(text='{"name": "test"}')

        with patch.object(provider, "_get_client") as mock_client:
            mock_client.return_value.chat.completions.create = AsyncMock(return_value=mock_response)
            schema = {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}
            result = await provider.complete_structured(
                [LLMMessage(role="system", content="System"), LLMMessage(role="user", content="Get data")],
                schema=schema,
            )

        assert result.text == '{"name": "test"}'

    @pytest.mark.asyncio
    async def test_complete_structured_without_system_message(self):
        provider = self._make_provider()
        mock_response = self._mock_response(text='{"ok": true}')

        with patch.object(provider, "_get_client") as mock_client:
            mock_client.return_value.chat.completions.create = AsyncMock(return_value=mock_response)
            schema = {"type": "object", "properties": {"ok": {"type": "boolean"}}}
            result = await provider.complete_structured(
                [LLMMessage(role="user", content="Check")],
                schema=schema,
            )

        assert result.text == '{"ok": true}'

    @pytest.mark.asyncio
    async def test_complete_structured_invalid_raises(self):
        provider = self._make_provider()
        mock_response = self._mock_response(text="not json")

        with patch.object(provider, "_get_client") as mock_client:
            mock_client.return_value.chat.completions.create = AsyncMock(return_value=mock_response)
            schema = {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}

            with pytest.raises(StructuredOutputValidationError):
                await provider.complete_structured([LLMMessage(role="user", content="Get")], schema=schema)

    @pytest.mark.asyncio
    async def test_stream_yields_chunks(self):
        provider = self._make_provider()

        chunk1 = MagicMock()
        chunk1.choices = [MagicMock()]
        chunk1.choices[0].delta.content = "Hello"
        chunk1.choices[0].finish_reason = None
        chunk1.usage = None

        chunk2 = MagicMock()
        chunk2.choices = [MagicMock()]
        chunk2.choices[0].delta.content = " world"
        chunk2.choices[0].finish_reason = "stop"
        chunk2.usage = None

        async def mock_stream():
            yield chunk1
            yield chunk2

        with patch.object(provider, "_get_client") as mock_client:
            mock_client.return_value.chat.completions.create = AsyncMock(return_value=mock_stream())
            chunks = []
            async for c in provider.stream([LLMMessage(role="user", content="Hi")]):
                chunks.append(c)

        assert len(chunks) == 2
        assert chunks[0].text_delta == "Hello"
        assert chunks[1].finish_reason == "stop"

    @pytest.mark.asyncio
    async def test_stream_usage_only_chunk(self):
        provider = self._make_provider()

        final_chunk = MagicMock()
        final_chunk.choices = []
        final_chunk.usage = MagicMock()
        final_chunk.usage.prompt_tokens = 10
        final_chunk.usage.completion_tokens = 5
        final_chunk.usage.total_tokens = 15

        async def mock_stream():
            yield final_chunk

        with patch.object(provider, "_get_client") as mock_client:
            mock_client.return_value.chat.completions.create = AsyncMock(return_value=mock_stream())
            chunks = []
            async for c in provider.stream([LLMMessage(role="user", content="Hi")]):
                chunks.append(c)

        assert len(chunks) == 1
        assert chunks[0].token_usage is not None
        assert chunks[0].token_usage.total_tokens == 15

    @pytest.mark.asyncio
    async def test_stream_with_finish_and_usage(self):
        provider = self._make_provider()

        chunk = MagicMock()
        chunk.choices = [MagicMock()]
        chunk.choices[0].delta.content = "done"
        chunk.choices[0].finish_reason = "stop"
        chunk.usage = MagicMock()
        chunk.usage.prompt_tokens = 8
        chunk.usage.completion_tokens = 3
        chunk.usage.total_tokens = 11

        async def mock_stream():
            yield chunk

        with patch.object(provider, "_get_client") as mock_client:
            mock_client.return_value.chat.completions.create = AsyncMock(return_value=mock_stream())
            chunks = []
            async for c in provider.stream([LLMMessage(role="user", content="Hi")]):
                chunks.append(c)

        assert chunks[0].token_usage is not None

    @pytest.mark.asyncio
    async def test_stream_interrupted_error(self):
        provider = self._make_provider()

        chunk1 = MagicMock()
        chunk1.choices = [MagicMock()]
        chunk1.choices[0].delta.content = "partial"
        chunk1.choices[0].finish_reason = None
        chunk1.usage = None

        async def mock_stream():
            yield chunk1
            raise ConnectionError("disconnected")

        with patch.object(provider, "_get_client") as mock_client:
            mock_client.return_value.chat.completions.create = AsyncMock(return_value=mock_stream())
            with pytest.raises(StreamInterruptedError) as exc_info:
                async for _ in provider.stream([LLMMessage(role="user", content="Hi")]):
                    pass
            assert exc_info.value.chunks_received == 1

    @pytest.mark.asyncio
    async def test_stream_error_before_chunks_reraises(self):
        provider = self._make_provider()

        async def mock_stream():
            raise ConnectionError("disconnected")
            yield  # pragma: no cover

        with patch.object(provider, "_get_client") as mock_client:
            mock_client.return_value.chat.completions.create = AsyncMock(return_value=mock_stream())
            with pytest.raises(ConnectionError):
                async for _ in provider.stream([LLMMessage(role="user", content="Hi")]):
                    pass
