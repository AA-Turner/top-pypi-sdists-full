"""Tests for AzureOpenAIProvider."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from agentic_devtools.orchestration.llm.errors import StreamInterruptedError, StructuredOutputValidationError
from agentic_devtools.orchestration.llm.providers.azure_openai import AzureOpenAIProvider
from agentic_devtools.orchestration.llm.types import LLMMessage, ProviderType


class TestAzureOpenAIProvider:
    """Tests for AzureOpenAIProvider."""

    def _make_provider(self):
        return AzureOpenAIProvider(
            api_key="test-key",
            endpoint="https://test.openai.azure.com",
            model="gpt-4o",
            api_version="2024-02-01",
            temperature=0.7,
            max_tokens=1000,
        )

    def _mock_response(self, text="Hello", prompt_tokens=10, completion_tokens=5):
        response = MagicMock()
        choice = MagicMock()
        choice.message.content = text
        choice.finish_reason = "stop"
        response.choices = [choice]
        response.model = "gpt-4o"
        usage = MagicMock()
        usage.prompt_tokens = prompt_tokens
        usage.completion_tokens = completion_tokens
        usage.total_tokens = prompt_tokens + completion_tokens
        response.usage = usage
        return response

    @pytest.mark.asyncio
    async def test_complete_returns_response(self):
        provider = self._make_provider()
        mock_response = self._mock_response()

        with patch.object(provider, "_get_client") as mock_client:
            mock_client.return_value.chat.completions.create = AsyncMock(return_value=mock_response)
            result = await provider.complete([LLMMessage(role="user", content="Hello")])

        assert result.text == "Hello"
        assert result.model == "gpt-4o"
        assert result.provider_type == ProviderType.AZURE_OPENAI
        assert result.usage is not None
        assert result.usage.input_tokens == 10
        assert result.usage.output_tokens == 5
        assert result.latency_ms is not None

    @pytest.mark.asyncio
    async def test_complete_without_usage(self):
        provider = self._make_provider()
        response = MagicMock()
        choice = MagicMock()
        choice.message.content = "Hi"
        response.choices = [choice]
        response.model = "gpt-4o"
        response.usage = None

        with patch.object(provider, "_get_client") as mock_client:
            mock_client.return_value.chat.completions.create = AsyncMock(return_value=response)
            result = await provider.complete([LLMMessage(role="user", content="Hello")])

        assert result.usage is None

    @pytest.mark.asyncio
    async def test_complete_uses_retry_wrapper(self):
        provider = self._make_provider()
        mock_response = self._mock_response()

        with (
            patch.object(provider, "_get_client") as mock_client,
            patch(
                "agentic_devtools.orchestration.llm.providers.azure_openai.execute_with_retry",
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
                "agentic_devtools.orchestration.llm.providers.azure_openai.execute_with_retry",
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
        assert call_kwargs["temperature"] == 0.7
        assert call_kwargs["max_tokens"] == 1000

    @pytest.mark.asyncio
    async def test_complete_structured_validates_schema(self):
        provider = self._make_provider()
        mock_response = self._mock_response(text='{"name": "test", "value": 42}')

        with patch.object(provider, "_get_client") as mock_client:
            mock_client.return_value.chat.completions.create = AsyncMock(return_value=mock_response)
            schema = {
                "type": "object",
                "properties": {"name": {"type": "string"}, "value": {"type": "integer"}},
                "required": ["name", "value"],
            }
            result = await provider.complete_structured(
                [LLMMessage(role="system", content="You are helpful"), LLMMessage(role="user", content="Get data")],
                schema=schema,
            )

        assert result.text == '{"name": "test", "value": 42}'

    @pytest.mark.asyncio
    async def test_complete_structured_without_system_message(self):
        """When no system message exists, one is inserted."""
        provider = self._make_provider()
        mock_response = self._mock_response(text='{"result": true}')

        with patch.object(provider, "_get_client") as mock_client:
            mock_client.return_value.chat.completions.create = AsyncMock(return_value=mock_response)
            schema = {"type": "object", "properties": {"result": {"type": "boolean"}}}
            result = await provider.complete_structured(
                [LLMMessage(role="user", content="Check")],
                schema=schema,
            )

        assert result.text == '{"result": true}'

    @pytest.mark.asyncio
    async def test_complete_structured_raises_on_invalid(self):
        provider = self._make_provider()
        mock_response = self._mock_response(text="not json")

        with patch.object(provider, "_get_client") as mock_client:
            mock_client.return_value.chat.completions.create = AsyncMock(return_value=mock_response)
            schema = {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}

            with pytest.raises(StructuredOutputValidationError):
                await provider.complete_structured([LLMMessage(role="user", content="Get data")], schema=schema)

    @pytest.mark.asyncio
    async def test_stream_yields_chunks(self):
        provider = self._make_provider()

        # Create mock stream chunks
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
        assert chunks[1].text_delta == " world"
        assert chunks[1].finish_reason == "stop"

    @pytest.mark.asyncio
    async def test_stream_usage_only_chunk(self):
        """Stream that ends with a usage-only chunk (no choices)."""
        provider = self._make_provider()

        chunk1 = MagicMock()
        chunk1.choices = [MagicMock()]
        chunk1.choices[0].delta.content = "Hi"
        chunk1.choices[0].finish_reason = None
        chunk1.usage = None

        # Final usage-only chunk
        final_chunk = MagicMock()
        final_chunk.choices = []
        final_chunk.usage = MagicMock()
        final_chunk.usage.prompt_tokens = 10
        final_chunk.usage.completion_tokens = 5
        final_chunk.usage.total_tokens = 15

        async def mock_stream():
            yield chunk1
            yield final_chunk

        with patch.object(provider, "_get_client") as mock_client:
            mock_client.return_value.chat.completions.create = AsyncMock(return_value=mock_stream())
            chunks = []
            async for c in provider.stream([LLMMessage(role="user", content="Hi")]):
                chunks.append(c)

        assert len(chunks) == 2
        assert chunks[1].finish_reason == "stop"
        assert chunks[1].token_usage is not None
        assert chunks[1].token_usage.total_tokens == 15

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
        assert call_kwargs["temperature"] == 0.7
        assert call_kwargs["max_tokens"] == 1000

    @pytest.mark.asyncio
    async def test_stream_with_finish_and_usage(self):
        """Stream chunk with finish_reason and usage attached."""
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
        assert chunks[0].token_usage.total_tokens == 11

    @pytest.mark.asyncio
    async def test_stream_interrupted_error(self):
        """After receiving chunks, an error raises StreamInterruptedError."""
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
            assert "partial" in exc_info.value.partial_response

    @pytest.mark.asyncio
    async def test_stream_error_before_chunks_reraises(self):
        """Error before any chunks should re-raise the original error."""
        provider = self._make_provider()

        async def mock_stream():
            raise ConnectionError("disconnected")
            yield  # pragma: no cover

        with patch.object(provider, "_get_client") as mock_client:
            mock_client.return_value.chat.completions.create = AsyncMock(return_value=mock_stream())
            with pytest.raises(ConnectionError, match="disconnected"):
                async for _ in provider.stream([LLMMessage(role="user", content="Hi")]):
                    pass

    def test_get_client_lazy_init(self):
        """Client is lazily initialized."""
        provider = self._make_provider()
        with patch("openai.AsyncAzureOpenAI") as mock_cls:
            mock_cls.return_value = MagicMock()
            client = provider._get_client()
            assert client is mock_cls.return_value
            # Second call should use cached
            client2 = provider._get_client()
            assert client2 is client
            mock_cls.assert_called_once()

    def test_get_client_preserves_zero_timeout(self):
        """timeout_seconds=0 is passed through as-is, not replaced by the default."""
        provider = AzureOpenAIProvider(
            api_key="test-key",
            endpoint="https://test.openai.azure.com",
            model="gpt-4o",
            timeout_seconds=0,
        )
        with patch("openai.AsyncAzureOpenAI") as mock_cls:
            mock_cls.return_value = MagicMock()
            provider._get_client()
        assert mock_cls.call_args[1]["timeout"] == 0

    def test_build_messages_with_name(self):
        """Messages with name field are properly converted."""
        provider = self._make_provider()
        messages = [LLMMessage(role="user", content="Hello", name="alice")]
        result = provider._build_messages(messages)
        assert result == [{"role": "user", "content": "Hello", "name": "alice"}]

    @pytest.mark.asyncio
    async def test_complete_without_temperature_and_max_tokens(self):
        """When temperature and max_tokens are None, they are not included in params."""
        provider = AzureOpenAIProvider(
            api_key="test-key",
            endpoint="https://test.openai.azure.com",
            model="gpt-4o",
        )
        mock_response = self._mock_response()

        with patch.object(provider, "_get_client") as mock_client:
            create_mock = AsyncMock(return_value=mock_response)
            mock_client.return_value.chat.completions.create = create_mock
            await provider.complete([LLMMessage(role="user", content="Hello")])

        call_kwargs = create_mock.call_args[1]
        assert "temperature" not in call_kwargs
        assert "max_tokens" not in call_kwargs

    @pytest.mark.asyncio
    async def test_stream_without_temperature_and_max_tokens(self):
        """When temperature and max_tokens are None, they are not included in stream params."""
        provider = AzureOpenAIProvider(
            api_key="test-key",
            endpoint="https://test.openai.azure.com",
            model="gpt-4o",
        )

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
