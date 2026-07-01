from unittest.mock import AsyncMock, patch

import pytest
from mistralai.client.models import (
    AssistantMessage,
    ChatCompletionChoice,
    ChatCompletionRequest,
    ChatCompletionResponse,
    ResponseFormat,
    UsageInfo,
    UserMessage,
)
from mistralai.extra import response_format_from_pydantic_model
from pydantic import BaseModel

from mistralai.workflows.plugins.mistralai.activities import mistralai_chat_parse


class ResponseModel(BaseModel):
    greeting: str


mock_response = ChatCompletionResponse(
    id="chatcmpl-123",
    object="chat.completion",
    created=1625000000,
    model="mistral-small",
    choices=[
        ChatCompletionChoice(
            index=0,
            message=AssistantMessage(content='{"greeting": "Hello! How can I help you?"}'),
            finish_reason="stop",
        )
    ],
    usage=UsageInfo(prompt_tokens=10, completion_tokens=5, total_tokens=15),
)

params = ChatCompletionRequest(
    model="mistral-small",
    messages=[UserMessage(content="Hello!")],
)


class TestMistralChatParse:
    @pytest.mark.asyncio
    async def test_mistral_chat_parse(self) -> None:
        with patch("mistralai.workflows.plugins.mistralai.utils._get_mistral_client") as mistral_cls:
            mock_mistral_instance = AsyncMock()
            mock_mistral_instance.chat.complete_async.return_value = mock_response
            mock_mistral_instance.__aenter__.return_value = mock_mistral_instance
            mistral_cls.return_value = mock_mistral_instance

            response_format = ResponseFormat(**response_format_from_pydantic_model(ResponseModel))
            result = await mistralai_chat_parse(params, response_format)

            assert (
                result is not None
                and result.choices is not None
                and result.choices[0].message is not None
                and result.choices[0].message.content is not None
            )
            parsed_response = ResponseModel.model_validate_json(result.choices[0].message.content)
            expected_response = ResponseModel(greeting="Hello! How can I help you?")
            assert parsed_response.model_dump() == expected_response.model_dump()
            mock_mistral_instance.chat.complete_async.assert_called_once()
