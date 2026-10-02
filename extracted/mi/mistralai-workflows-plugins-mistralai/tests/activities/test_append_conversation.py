from unittest.mock import AsyncMock, patch

import httpx
import pytest
from temporalio.exceptions import ApplicationError

from mistralai.workflows.plugins.mistralai.activities import (
    mistralai_append_conversation,
    mistralai_append_conversation_stream,
)
from mistralai.workflows.plugins.mistralai.models import ConversationAppendRequest


def make_params() -> ConversationAppendRequest:
    return ConversationAppendRequest(
        conversation_id="conv-123",
        inputs="Hello",
    )


class TestMistralaiAppendConversationTimeout:
    @pytest.mark.asyncio
    async def test_timeout_exception_raises_non_retryable_application_error(self) -> None:
        params = make_params()
        with patch("mistralai.workflows.plugins.mistralai.utils._get_mistral_client") as mistral_cls:
            mock_client = AsyncMock()
            mock_client.beta.conversations.append_async.side_effect = httpx.ReadTimeout("read timeout")
            mock_client.__aenter__.return_value = mock_client
            mistral_cls.return_value = mock_client

            with patch("mistralai.workflows.plugins.mistralai.activities.logger") as mock_logger:
                with pytest.raises(ApplicationError) as exc_info:
                    await mistralai_append_conversation(params)

            assert exc_info.value.non_retryable is True
            assert "timed out" in str(exc_info.value)
            mock_logger.exception.assert_any_call(
                "Conversation append timed out; the conversation may still be processing server-side",
                conversation_id=params.conversation_id,
            )

    @pytest.mark.asyncio
    async def test_connect_timeout_propagates_for_retry(self) -> None:
        params = make_params()
        with patch("mistralai.workflows.plugins.mistralai.utils._get_mistral_client") as mistral_cls:
            mock_client = AsyncMock()
            mock_client.beta.conversations.append_async.side_effect = httpx.ConnectTimeout("connect timeout")
            mock_client.__aenter__.return_value = mock_client
            mistral_cls.return_value = mock_client

            with pytest.raises(httpx.ConnectTimeout):
                await mistralai_append_conversation(params)


class TestMistralaiAppendConversationStreamTimeout:
    @pytest.mark.asyncio
    async def test_timeout_exception_raises_non_retryable_application_error(self) -> None:
        params = make_params()
        with patch("mistralai.workflows.plugins.mistralai.utils._get_mistral_client") as mistral_cls:
            mock_client = AsyncMock()
            mock_client.beta.conversations.append_stream_async.side_effect = httpx.ReadTimeout("read timeout")
            mock_client.__aenter__.return_value = mock_client
            mistral_cls.return_value = mock_client

            with pytest.raises(ApplicationError) as exc_info:
                await mistralai_append_conversation_stream(params)

            assert exc_info.value.non_retryable is True
            assert "timed out" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_timeout_exception_during_stream_raises_non_retryable_application_error(self) -> None:
        params = make_params()
        with patch("mistralai.workflows.plugins.mistralai.utils._get_mistral_client") as mistral_cls:
            mock_client = AsyncMock()
            mock_client.beta.conversations.append_stream_async.return_value = AsyncMock()

            with patch(
                "mistralai.workflows.plugins.mistralai.activities.handle_conversation_stream",
                side_effect=httpx.ReadTimeout("read timeout during stream"),
            ):
                mock_client.__aenter__.return_value = mock_client
                mistral_cls.return_value = mock_client

                with pytest.raises(ApplicationError) as exc_info:
                    await mistralai_append_conversation_stream(params)

                assert exc_info.value.non_retryable is True
                assert "timed out" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_connect_timeout_propagates_for_retry(self) -> None:
        params = make_params()
        with patch("mistralai.workflows.plugins.mistralai.utils._get_mistral_client") as mistral_cls:
            mock_client = AsyncMock()
            mock_client.beta.conversations.append_stream_async.side_effect = httpx.ConnectTimeout("connect timeout")
            mock_client.__aenter__.return_value = mock_client
            mistral_cls.return_value = mock_client

            with pytest.raises(httpx.ConnectTimeout):
                await mistralai_append_conversation_stream(params)
