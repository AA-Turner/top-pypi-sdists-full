from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any, Literal, TypeVar, cast

import structlog

from mistralai.client import Mistral
from mistralai.client import models as mistralai_models
from mistralai.client.utils import eventstreaming
from mistralai.workflows.client import get_mistral_client as _get_mistral_client
from mistralai.workflows.core.config.config import config
from mistralai.workflows.core.rate_limiting.rate_limit import RateLimit
from mistralai.workflows.core.task import Task
from mistralai.workflows.plugins.mistralai.connectors.run_as import ConnectorRunAs, use_executor_credentials_for
from mistralai.workflows.plugins.mistralai.models import ChatStreamState, ContentChunk, ConversationStreamState

_MISTRAL_LLM_RATE_LIMIT_DEFAULT_KEY = "__MISTRAL_LLM_RATE_LIMIT_DEFAULT_KEY"
_StreamEventT = TypeVar("_StreamEventT")


def get_mistral_client(run_as: ConnectorRunAs = ConnectorRunAs.AUTO) -> Mistral:
    api_key_secret = config.worker.agent.mistral_client_api_key
    return _get_mistral_client(
        api_key=api_key_secret.get_secret_value() if api_key_secret else None,
        server=config.worker.agent.mistral_client_server,
        server_url=config.worker.agent.mistral_client_server_url,
        url_params=config.worker.agent.mistral_client_url_params,
        timeout_ms=config.worker.agent.mistral_client_timeout_ms,
        use_executor_credentials=use_executor_credentials_for(run_as),
    )


def _get_agent_llm_rate_limit() -> RateLimit | None:
    llm_rate_limit = config.worker.agent.llm_rate_limit
    if llm_rate_limit is None:
        return None
    if llm_rate_limit.key is None:
        llm_rate_limit.key = _MISTRAL_LLM_RATE_LIMIT_DEFAULT_KEY
    return llm_rate_limit


logger = structlog.get_logger(__name__)


async def _iter_stream(stream: eventstreaming.EventStreamAsync[_StreamEventT]) -> AsyncIterator[_StreamEventT]:
    async with stream:
        async for chunk in stream:
            yield chunk


# FIXME : Add cost informations - depends on agent team
async def handle_conversation_stream(
    stream: eventstreaming.EventStreamAsync[mistralai_models.ConversationEvents],
) -> mistralai_models.ConversationResponse:
    aggregated_content = ""
    tool_calls: dict[int, mistralai_models.ToolExecutionEntry] = {}
    function_calls: dict[int, mistralai_models.FunctionCallEntry] = {}
    handoffs: dict[str, mistralai_models.AgentHandoffEntry] = {}
    conversation_id: str = ""
    outputs: list[mistralai_models.ConversationResponseOutput] = []
    async with Task[ConversationStreamState](type="assistant_message", state=ConversationStreamState()) as task:
        async for chunk in _iter_stream(stream):
            if isinstance(chunk.data, mistralai_models.ResponseStartedEvent):
                conversation_id = chunk.data.conversation_id

            elif isinstance(chunk.data, mistralai_models.ResponseDoneEvent):
                outputs.append(mistralai_models.MessageOutputEntry(content=aggregated_content, type="message.output"))

            elif isinstance(chunk.data, mistralai_models.MessageOutputEvent):
                if isinstance(chunk.data.content, str):
                    aggregated_content += chunk.data.content
                    await task.set_state(ConversationStreamState(contentChunks=[ContentChunk(text=aggregated_content)]))

                elif isinstance(chunk.data.content, mistralai_models.TextChunk):
                    aggregated_content += chunk.data.content.text
                    await task.set_state(ConversationStreamState(contentChunks=[ContentChunk(text=aggregated_content)]))
            elif isinstance(chunk.data, mistralai_models.FunctionCallEvent):
                index = chunk.data.output_index or 0
                existing_function = function_calls.get(index)

                if not existing_function:
                    function_call = mistralai_models.FunctionCallEntry(
                        tool_call_id=chunk.data.tool_call_id,
                        name=chunk.data.name,
                        arguments=chunk.data.arguments or "",
                        type="function.call",
                    )
                    function_calls[index] = function_call
                else:
                    if chunk.data.id and chunk.data.id != existing_function.id:
                        existing_function.id = chunk.data.id
                    if chunk.data.name and not existing_function.name:
                        existing_function.name = chunk.data.name
                    if chunk.data.arguments:
                        previous_args = existing_function.arguments or ""
                        new_args = chunk.data.arguments
                        if isinstance(previous_args, str):
                            existing_function.arguments = previous_args + new_args
                        else:
                            existing_function.arguments = new_args

            elif isinstance(chunk.data, mistralai_models.ToolExecutionDeltaEvent):
                index = chunk.data.output_index or 0
                existing_tool = tool_calls.get(index)

                if not existing_tool:
                    if isinstance(chunk.data, mistralai_models.ToolExecutionDeltaEvent):
                        tool_call = mistralai_models.ToolExecutionEntry(
                            name=chunk.data.name,
                            arguments=chunk.data.arguments or "",
                            id=chunk.data.id,
                            type="tool.execution",
                        )

                        tool_calls[index] = tool_call

                else:
                    if chunk.data.id and chunk.data.id != existing_tool.id:
                        existing_tool.id = chunk.data.id
                    if chunk.data.name and not existing_tool.name:
                        existing_tool.name = chunk.data.name
                    if chunk.data.arguments:
                        previous_args = existing_tool.arguments
                        new_args = chunk.data.arguments
                        existing_tool.arguments = previous_args + new_args

            elif isinstance(chunk.data, mistralai_models.ToolExecutionDoneEvent):
                outputs.append(tool_calls[chunk.data.output_index or 0])
            elif isinstance(chunk.data, mistralai_models.AgentHandoffStartedEvent):
                handoff_id = chunk.data.id
                if handoff_id in handoffs:
                    logger.error(
                        "This handoff is already registered..., this should never happen... Overwriting the handoff."
                    )
                if not handoff_id:
                    logger.error("This handoff has no id ..., overwriting element with empty key.")
                handoffs[handoff_id] = mistralai_models.AgentHandoffEntry(
                    previous_agent_id=chunk.data.previous_agent_id,
                    previous_agent_name=chunk.data.previous_agent_name,
                    next_agent_id="",
                    next_agent_name="",
                    id=handoff_id,
                    type="agent.handoff",
                )
            elif isinstance(chunk.data, mistralai_models.AgentHandoffDoneEvent):
                handoff_id = chunk.data.id
                if handoff_id not in handoffs:
                    logger.error("This handoff should already be registered..., this should never happen... Passing...")
                    pass
                if not handoff_id:
                    logger.error("This handoff has no id ..., overwriting element with empty key.")

                handoffs[handoff_id].next_agent_id = chunk.data.next_agent_id
                handoffs[handoff_id].next_agent_name = chunk.data.next_agent_name
                outputs.append(handoffs[handoff_id])

    message_payload: dict[str, object] = {}

    message_payload["outputs"] = outputs + list(function_calls.values())
    message_payload["conversation_id"] = conversation_id
    message_payload["usage"] = mistralai_models.ConversationUsageInfo()  # FIXME : fill that

    return mistralai_models.ConversationResponse.model_validate(message_payload)


async def handle_chat_stream(
    stream: eventstreaming.EventStreamAsync[mistralai_models.CompletionEvent],
) -> mistralai_models.AssistantMessage:
    aggregated_content = ""
    role: Literal["assistant"] | None = None
    tool_calls: dict[int, mistralai_models.ToolCall] = {}

    async with Task[ChatStreamState](type="assistant_message", state=ChatStreamState()) as task:
        async for chunk in _iter_stream(stream):
            if not chunk.data.choices:
                continue

            choice = chunk.data.choices[0]
            delta = choice.delta

            if isinstance(delta.role, str) and delta.role == "assistant":
                role = cast(Literal["assistant"], "assistant")

            delta_content = delta.content
            if isinstance(delta_content, str):
                aggregated_content += delta_content
                await task.set_state(ChatStreamState(contentChunks=[ContentChunk(text=aggregated_content)]))
            elif isinstance(delta_content, list):
                for item in delta_content:
                    if isinstance(item, mistralai_models.TextChunk):
                        aggregated_content += item.text
                    else:
                        logger.debug("Skipping non-text content chunk in stream", chunk_type=type(item).__name__)
                await task.set_state(ChatStreamState(contentChunks=[ContentChunk(text=aggregated_content)]))

            if delta.tool_calls:
                for partial in delta.tool_calls:
                    index = partial.index if partial.index is not None else 0
                    existing = tool_calls.get(index)

                    function_name = ""
                    function_arguments: str | dict[str, Any] = ""
                    if partial.function:
                        if partial.function.name:
                            function_name = partial.function.name
                        if partial.function.arguments:
                            function_arguments = partial.function.arguments

                    if existing is None:
                        tool_call = mistralai_models.ToolCall(
                            id=partial.id,
                            type=partial.type,
                            index=partial.index,
                            function=mistralai_models.FunctionCall(
                                name=function_name,
                                arguments=function_arguments,
                            )
                            if partial.function
                            else mistralai_models.FunctionCall(name=function_name, arguments=""),
                        )
                        tool_calls[index] = tool_call
                    else:
                        if partial.id and partial.id != existing.id:
                            existing.id = partial.id
                        if partial.type:
                            existing.type = partial.type
                        if partial.function:
                            if partial.function.name and not existing.function.name:
                                existing.function.name = partial.function.name
                            if partial.function.arguments:
                                previous_args = existing.function.arguments or ""
                                new_args = partial.function.arguments
                                if isinstance(previous_args, str) and isinstance(new_args, str):
                                    existing.function.arguments = previous_args + new_args
                                else:
                                    existing.function.arguments = new_args

    message_payload: dict[str, object] = {}
    if role is not None:
        message_payload["role"] = role
    if aggregated_content:
        message_payload["content"] = aggregated_content
    if tool_calls:
        message_payload["tool_calls"] = list(tool_calls.values())

    return mistralai_models.AssistantMessage.model_validate(message_payload)
