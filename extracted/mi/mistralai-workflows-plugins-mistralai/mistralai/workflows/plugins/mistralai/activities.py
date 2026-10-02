from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import TypeVar

import httpx
import structlog
from pydantic import AliasChoices, BaseModel, Field
from temporalio.exceptions import ApplicationError

from mistralai.client import Mistral
from mistralai.client import models as mistralai_models
from mistralai.client.models import ResponseFormat
from mistralai.extra import response_format_from_pydantic_model
from mistralai.workflows.core.activity import activity
from mistralai.workflows.core.dependencies.dependency_injector import Depends
from mistralai.workflows.plugins.mistralai.connectors.run_as import ConnectorRunAs
from mistralai.workflows.plugins.mistralai.models import AgentUpdateRequest, ConversationAppendRequest
from mistralai.workflows.plugins.mistralai.utils import (
    _get_agent_llm_rate_limit,
    get_mistral_client,
    handle_chat_stream,
    handle_conversation_stream,
)

T = TypeVar("T", bound=BaseModel)
EXCLUDED_FIELDS = {"stream"}

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def _conversation_append_timeout_guard(conversation_id: str) -> AsyncIterator[None]:
    try:
        yield
    except (httpx.ReadTimeout, httpx.WriteTimeout) as e:
        logger.exception(
            "Conversation append timed out; the conversation may still be processing server-side",
            conversation_id=conversation_id,
        )
        raise ApplicationError(
            "Conversation append timed out: the Mistral API did not respond in time. "
            "The conversation may still be processing server-side.",
            non_retryable=True,
        ) from e


@activity(rate_limit=_get_agent_llm_rate_limit())
async def mistralai_create_agent(
    params: mistralai_models.CreateAgentRequest,
    run_as: ConnectorRunAs = ConnectorRunAs.AUTO,
) -> mistralai_models.Agent:
    mistral_client = get_mistral_client(run_as)
    agent = await mistral_client.beta.agents.create_async(**params.model_dump(by_alias=True, exclude=EXCLUDED_FIELDS))
    return agent


@activity(rate_limit=_get_agent_llm_rate_limit())
async def mistralai_start_conversation(
    params: mistralai_models.ConversationRequest,
    run_as: ConnectorRunAs = ConnectorRunAs.AUTO,
) -> mistralai_models.ConversationResponse:
    mistral_client = get_mistral_client(run_as)
    return await mistral_client.beta.conversations.start_async(
        **params.model_dump(by_alias=True, exclude=EXCLUDED_FIELDS)
    )


@activity(rate_limit=_get_agent_llm_rate_limit())
async def mistralai_append_conversation(
    params: ConversationAppendRequest,
    run_as: ConnectorRunAs = ConnectorRunAs.AUTO,
) -> mistralai_models.ConversationResponse:
    mistral_client = get_mistral_client(run_as)
    async with _conversation_append_timeout_guard(params.conversation_id):
        return await mistral_client.beta.conversations.append_async(
            **params.model_dump(by_alias=True, exclude=EXCLUDED_FIELDS)
        )


@activity(rate_limit=_get_agent_llm_rate_limit())
async def mistralai_update_agent(
    params: AgentUpdateRequest,
    run_as: ConnectorRunAs = ConnectorRunAs.AUTO,
) -> mistralai_models.Agent:
    mistral_client = get_mistral_client(run_as)
    return await mistral_client.beta.agents.update_async(**params.model_dump(by_alias=True, exclude=EXCLUDED_FIELDS))


@activity(rate_limit=_get_agent_llm_rate_limit())
async def mistralai_chat_complete(
    params: mistralai_models.ChatCompletionRequest,
    mistral_client: Mistral = Depends(get_mistral_client),
) -> mistralai_models.ChatCompletionResponse:
    return await mistral_client.chat.complete_async(**params.model_dump(exclude=EXCLUDED_FIELDS))


@activity(rate_limit=_get_agent_llm_rate_limit())
async def mistralai_chat_stream(
    params: mistralai_models.ChatCompletionRequest,
    mistral_client: Mistral = Depends(get_mistral_client),
) -> mistralai_models.AssistantMessage:
    stream = await mistral_client.chat.stream_async(
        **params.model_dump(by_alias=True, exclude_none=True, exclude=EXCLUDED_FIELDS)
    )
    return await handle_chat_stream(stream=stream)


@activity(rate_limit=_get_agent_llm_rate_limit())
async def mistralai_start_conversation_stream(
    params: mistralai_models.ConversationRequest, run_as: ConnectorRunAs = ConnectorRunAs.AUTO
) -> mistralai_models.ConversationResponse:
    mistral_client = get_mistral_client(run_as)
    stream = await mistral_client.beta.conversations.start_stream_async(
        **params.model_dump(by_alias=True, exclude_none=True, exclude=EXCLUDED_FIELDS)
    )
    return await handle_conversation_stream(stream=stream)


@activity(rate_limit=_get_agent_llm_rate_limit())
async def mistralai_append_conversation_stream(
    params: ConversationAppendRequest, run_as: ConnectorRunAs = ConnectorRunAs.AUTO
) -> mistralai_models.ConversationResponse:
    mistral_client = get_mistral_client(run_as)
    async with _conversation_append_timeout_guard(params.conversation_id):
        stream = await mistral_client.beta.conversations.append_stream_async(
            **params.model_dump(by_alias=True, exclude_none=True, exclude=EXCLUDED_FIELDS)
        )
        return await handle_conversation_stream(stream=stream)


@activity(rate_limit=_get_agent_llm_rate_limit())
async def mistralai_chat_parse(
    params: mistralai_models.ChatCompletionRequest,
    response_format: ResponseFormat,
    mistral_client: Mistral = Depends(get_mistral_client),
) -> mistralai_models.ChatCompletionResponse:
    """
    Chat completion with structured output parsing.

    This activity performs chat completion with structured output parsing.
    We use complete_async because Temporal doesn't support serializing Type[PydanticModel].

    Args:
        params: Chat completion request parameters
        response_format: Output response format
        mistral_client: Mistral client

    Returns:
        ChatCompletionResponse with parsed output in choices[0].message.content (as JSON string)
    """
    params_with_format = params.model_copy(update={"response_format": response_format})
    return await mistral_client.chat.complete_async(
        **params_with_format.model_dump(by_alias=True, exclude=EXCLUDED_FIELDS)
    )


async def chat_parse_to_model(
    model_class: type[T],
    request: mistralai_models.ChatCompletionRequest,
) -> T:
    """
    Parse chat completion response into a Pydantic model.

    Wraps mistralai_chat_parse activity with schema conversion and response validation.
    """
    response_format = ResponseFormat.model_validate(response_format_from_pydantic_model(model_class))
    response = await mistralai_chat_parse(request, response_format)

    if not response.choices or not response.choices[0].message or not response.choices[0].message.content:
        raise ValueError("No parsed response from Mistral")

    return model_class.model_validate_json(str(response.choices[0].message.content))


class MistralEmbeddingsParams(mistralai_models.EmbeddingRequest):
    # without this, the current `mistralai.EmbeddingRequest` doesn't keep the
    # `input` and `inputs` fields during model_dump(). This fixes it.
    # TODO(WFL-451): remove this once the `mistralai` SDK is updated.
    inputs: mistralai_models.EmbeddingRequestInputs = Field(validation_alias=AliasChoices("inputs", "input"))


@activity(rate_limit=_get_agent_llm_rate_limit())
async def mistralai_embeddings(
    params: MistralEmbeddingsParams,
    mistral_client: Mistral = Depends(get_mistral_client),
) -> mistralai_models.EmbeddingResponse:
    return await mistral_client.embeddings.create_async(**params.model_dump(by_alias=True, exclude=EXCLUDED_FIELDS))


@activity(rate_limit=_get_agent_llm_rate_limit())
async def mistralai_ocr(
    params: mistralai_models.OCRRequest,
    mistral_client: Mistral = Depends(get_mistral_client),
) -> mistralai_models.OCRResponse:
    return await mistral_client.ocr.process_async(**params.model_dump(by_alias=True, exclude=EXCLUDED_FIELDS))
