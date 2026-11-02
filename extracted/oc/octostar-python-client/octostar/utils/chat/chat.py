import asyncio as _asyncio
import httpx
from collections.abc import AsyncIterator, Callable
from typing import Optional, List, Any, Literal, Union, Dict, TypedDict
from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
from enum import Enum
import json
import logging

from ...client import Client, get_default_client
from ..exceptions import ApiConnectionError, StopAsyncIterationWithResult
from ..commons import network_retry_strategy, TimeoutAsyncGenerator

_logger = logging.getLogger(__name__)


class EntityBase(BaseModel):
    class Config:
        extra = "allow"

    entity_type: str = "os_workspace"
    entity_id: str
    entity_label: Optional[str] = None


class SearchSetModel(BaseModel):
    entity_id: str
    entity_label: str
    query: dict


class ChatMessagePriority(Enum):
    CRITICAL = 0
    CONTEXTUAL = 1
    HISTORICAL = 2


ContextMode = Literal["limited_to_context", "context_boosted"]


class ToolName(TypedDict):
    source: str
    name: str


class ExecutionMode(str, Enum):
    """The execution mode for a chat request."""

    COMPLETION = "completion"
    """Pure pass-through: no system prompt or processing, just forwards messages to the LLM."""

    SIMPLE = "simple"
    """Basic chat with a system prompt, but no RAG retrieval or tool usage."""

    AGENTIC = "agentic"
    """Full agent: formulates a plan, retrieves context via RAG, and invokes tools as needed."""


class ChatMessage(BaseModel):
    """
    Represents a single chat message in the conversation. Class is taken from octostar-api lib.
    """

    id: str = Field(..., description="The unique ID of the message.")
    role: str = Field(
        ...,
        description="The role of the message sender. Must be 'user', 'assistant', or 'system'.",
    )
    content: Union[List[EntityBase], SearchSetModel, str, Dict[str, Any]] = Field(
        ..., description="The content of the message."
    )
    type: Optional[
        Literal[
            "text",
            "json",
            "add_entities",
            "remove_entities",
            "add_search_set",
            "remove_search_set",
        ]
    ] = Field(
        None,
        description=(
            "The type of the message. Can be 'text', 'json', 'add_entities', 'remove_entities', 'add_search_set' or 'remove_search_set."
        ),
    )
    timestamp: Optional[datetime] = Field(
        None, description="The timestamp of the message in ISO 8601 format."
    )


class ChatStreamEvent(TypedDict, total=False):
    """A single event from the streaming chat endpoint."""

    channel: str
    """The event channel: 'text', 'agentic', 'context', 'final_prompt', 'heartbeat', 'error', or 'status'."""

    content: Any
    """The event payload. For 'text' events this is the accumulated response text so far."""


def _build_request(
    prompt: str,
    *,
    chat_history: Optional[list[ChatMessage]],
    workspaces: Optional[list[EntityBase]],
    context_mode: str,
    model_name: Optional[str],
    execution_mode: ExecutionMode,
    disabled_tools: Optional[list[ToolName]],
    streaming: bool,
    client: Client,
    extra_body: Optional[dict] = None,
) -> tuple:
    """Build the endpoint URL, headers, and JSON body for the chat API.

    Returns:
        (endpoint_url, headers, body)
    """
    endpoint_url = f"{client.get_base_url_v1()}/api/v1/chat"
    headers = {
        "Content-Type": "application/json",
        # ``.token`` lives on AuthenticatedClient (the runtime type); the
        # param is annotated with the Client base for call-site flexibility.
        "Authorization": f"Bearer {client.token}",  # pyright: ignore[reportAttributeAccessIssue]
        "x-ontology": client.ontology,
    }
    ws_list = workspaces or []
    ws_dicts = [ws.model_dump() for ws in ws_list]
    for ws in ws_dicts:
        if "os_workspace" not in ws:
            ws["os_workspace"] = ws["entity_id"]
    hist = chat_history or []
    hist_dicts = [ch.model_dump() for ch in hist]
    hist_dicts = [
        {
            **m,
            "timestamp": (
                m.get("timestamp", "").strftime("%Y-%m-%d %H:%M:%S")
                if isinstance(m.get("timestamp"), datetime)
                else None
            ),
        }
        for m in hist_dicts
    ]
    body = {
        **(extra_body or {}),
        "model_name": model_name,
        "messages": hist_dicts,
        "prompt": prompt,
        "streaming": streaming,
        "execution_mode": execution_mode,
        "context_mode": context_mode,
        "api_key": "",
        "cohere_key": "",
        "open_workspaces": ws_dicts,
        "disabled_tools": disabled_tools or [],
        "deployment_url": client.get_base_url_v1(),
        **(
            {} if "prompt_overrides" in (extra_body or {}) else {"prompt_overrides": {}}
        ),
    }
    return endpoint_url, headers, body


def _parse_response(message, response_validation):
    if response_validation == "json" or (
        isinstance(response_validation, type)
        and issubclass(response_validation, BaseModel)
    ):
        message = message.strip()
        if message.startswith("```json"):
            message = message[7:]
        if message.startswith("```"):
            message = message[3:]
        if message.endswith("```"):
            message = message[:-3]
        try:
            message = json.loads(message)
        except json.JSONDecodeError as e:
            raise ValueError(f"Response is not valid JSON: {e}\nContent: {message}")
        if response_validation == "json":
            return message
        elif isinstance(response_validation, type) and issubclass(
            response_validation, BaseModel
        ):
            try:
                return response_validation.model_validate(message)
            except ValidationError as e:
                raise ValueError(
                    f"Response does not match schema {response_validation.__name__}: {e}\nContent: {message}"
                )
        else:
            return message
    else:
        return message


def sync(
    prompt: str,
    chat_history: Optional[list[ChatMessage]] = None,
    workspaces: Optional[list[EntityBase]] = None,
    context_mode: Literal["limited_to_context", "context_boosted"] = "context_boosted",
    model_name: Optional[str] = None,
    timeout: Optional[float] = 300.0,
    retries: int = 2,
    disabled_tools: Optional[list[ToolName]] = None,
    execution_mode: ExecutionMode = ExecutionMode.COMPLETION,
    response_validation: Union[None, Literal["json"], type[BaseModel]] = None,
    client: Optional[Client] = None,
    **kwargs,
) -> Union[str, dict, list, BaseModel]:
    """
    # Make a request for the AI chat endpoint.

    ## Arguments
    - `prompt`: The user prompt to send to the chatbot.
    - `chat_history`: The list of messages that precede the user prompt.
    - `workspaces`: The list of workspaces the chatbot is able to see.
    - `context_mode`: The filtering mode for entities retrieved by the chatbot using RAG. Can be set to:
        * 'context_boosted': The context provided in the chat history is boosted in the RAG results,
            but results from the whole knowledge base can be retrieved;
        * 'limited_to_context': Only context provided in the chat history can be retrieved and used via RAG.
    - `timeout`: The timeout for the connection to the search engine. Can be set to "None" for no enforced timeout.
    - `retries`: The number of connection retries. Note that each retry may cost additional tokens.
    - `disabled_tools`: A list of tools that the LLM is banned from using for this invocation.
    - `execution_mode`: The mode with which the LLM will answer. Defaults to
        'completion'. Only 'completion' is supported — 'simple' and 'agentic'
        are deprecated and rejected by the backend with HTTP 400:
        * 'completion': Pure pass-through — no system prompt or processing, just forwards messages to the LLM;
    - `response_validation`: Whether the response should follow a given pattern. Possible values are:
        * None: No validation on the response;
        * 'json': Response is validated to be a JSON;
        * type[BaseModel]: Response is validated against the given pydantic model class;
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.
    - `**kwargs`: Additional keyword arguments are merged into the request body.
        Explicit parameters above take precedence over kwargs.

    ## Returns
    The chatbot response, as plain text.

    ## Raises
    - `ApiConnectionError`: If the query was unsuccessful.
    """
    if not client:
        client = get_default_client()
    endpoint_url, headers, body = _build_request(
        prompt,
        chat_history=chat_history,
        workspaces=workspaces,
        context_mode=context_mode,
        model_name=model_name,
        execution_mode=execution_mode,
        disabled_tools=disabled_tools,
        streaming=False,
        client=client,
        extra_body=kwargs,
    )
    response = None
    try:
        for attempt in network_retry_strategy(retries=retries):
            with attempt:
                with httpx.Client() as httpx_client:
                    response = httpx_client.post(
                        endpoint_url, json=body, headers=headers, timeout=timeout
                    )
                    response.raise_for_status()
                try:
                    chatbot_response = response.json()["response"]["content"]
                except Exception as e:
                    raise ConnectionError(
                        f"Unparsable response format {response.content} with exception {e}"
                    )
                try:
                    chatbot_response = _parse_response(
                        chatbot_response, response_validation
                    )
                except Exception as e:
                    raise ConnectionError(
                        f"Validation failed for {chatbot_response} with exception {e}"
                    )
    except Exception:
        raise ApiConnectionError("chat", response, client)
    return chatbot_response


async def asyncio(
    prompt: str,
    chat_history: Optional[list[ChatMessage]] = None,
    workspaces: Optional[list[EntityBase]] = None,
    context_mode: Literal["limited_to_context", "context_boosted"] = "context_boosted",
    model_name: Optional[str] = None,
    timeout: Optional[float] = 300.0,
    retries: int = 2,
    disabled_tools: Optional[list[ToolName]] = None,
    execution_mode: ExecutionMode = ExecutionMode.COMPLETION,
    response_validation: Union[None, Literal["json"], type[BaseModel]] = None,
    client: Optional[Client] = None,
    **kwargs,
) -> Union[str, dict, list, BaseModel]:
    """
    # Make asynchronously a request for the AI chat endpoint.

    ## Arguments
    - `prompt`: The user prompt to send to the chatbot.
    - `chat_history`: The list of messages that precede the user prompt.
    - `workspaces`: The list of workspaces the chatbot is able to see.
    - `context_mode`: The filtering mode for entities retrieved by the chatbot using RAG. Can be set to:
        * 'context_boosted': The context provided in the chat history is boosted in the RAG results,
            but results from the whole knowledge base can be retrieved;
        * 'limited_to_context': Only context provided in the chat history can be retrieved and used via RAG.
    - `timeout`: The timeout for the connection to the search engine. Can be set to "None" for no enforced timeout.
    - `retries`: The number of connection retries. Note that each retry may cost additional tokens.
    - `disabled_tools`: A list of tools that the LLM is banned from using for this invocation.
    - `execution_mode`: The mode with which the LLM will answer. Defaults to
        'completion'. Only 'completion' is supported — 'simple' and 'agentic'
        are deprecated and rejected by the backend with HTTP 400:
        * 'completion': Pure pass-through — no system prompt or processing, just forwards messages to the LLM;
    - `response_validation`: Whether the response should follow a given pattern. Possible values are:
        * None: No validation on the response, response is in plain text;
        * 'json': Response is validated to be a JSON, and returned as a dict;
        * type[BaseModel]: Response is validated against the given pydantic model class, and returned as an instance of that class;
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.
    - `**kwargs`: Additional keyword arguments are merged into the request body.
        Explicit parameters above take precedence over kwargs.

    ## Returns
    The chatbot response, parsed or as plain text.

    ## Raises
    - `ApiConnectionError`: If the query was unsuccessful.
    """
    if not client:
        client = get_default_client()
    endpoint_url, headers, body = _build_request(
        prompt,
        chat_history=chat_history,
        workspaces=workspaces,
        context_mode=context_mode,
        model_name=model_name,
        execution_mode=execution_mode,
        disabled_tools=disabled_tools,
        streaming=False,
        client=client,
        extra_body=kwargs,
    )
    response = None
    try:
        for attempt in network_retry_strategy(retries=retries):
            with attempt:
                async with httpx.AsyncClient() as httpx_client:
                    response = await httpx_client.post(
                        endpoint_url, json=body, headers=headers, timeout=timeout
                    )
                    response.raise_for_status()
                try:
                    chatbot_response = response.json()["response"]["content"]
                except Exception as e:
                    raise ConnectionError(
                        f"Unparsable response format {response.content} with exception {e}"
                    )
                try:
                    chatbot_response = _parse_response(
                        chatbot_response, response_validation
                    )
                except Exception as e:
                    raise ConnectionError(
                        f"Validation failed for {chatbot_response} with exception {e}"
                    )
    except Exception:
        raise ApiConnectionError("chat", response, client)
    return chatbot_response


async def streaming(
    prompt: str,
    chat_history: Optional[list[ChatMessage]] = None,
    workspaces: Optional[list[EntityBase]] = None,
    context_mode: Literal["limited_to_context", "context_boosted"] = "context_boosted",
    model_name: Optional[str] = None,
    timeout: Optional[float] = 300.0,
    disabled_tools: Optional[list[ToolName]] = None,
    execution_mode: ExecutionMode = ExecutionMode.COMPLETION,
    fail_condition: Optional[Callable[[List[ChatStreamEvent]], bool]] = None,
    end_condition: Optional[Callable[[List[ChatStreamEvent]], bool]] = None,
    client: Optional[Client] = None,
    **kwargs,
) -> AsyncIterator[Union[ChatStreamEvent, str]]:
    """
    # Stream a request to the AI chat endpoint.

    Opens a streaming HTTP connection and yields parsed events as they arrive.
    Each event is a `ChatStreamEvent` dict with a `channel` key indicating the
    event type and a `content` key with the payload.

    Catch `StopAsyncIterationWithResult` to get the final accumulated text
    response after the stream ends::

        try:
            async for event in chat.streaming(prompt="Hello"):
                print(event)          # process events in real-time
        except StopAsyncIterationWithResult as r:
            final_text = r.value      # the full response text

    ## Arguments
    - `prompt`: The user prompt to send to the chatbot.
    - `chat_history`: The list of messages that precede the user prompt.
    - `workspaces`: The list of workspaces the chatbot is able to see.
    - `context_mode`: The filtering mode for entities retrieved by the chatbot using RAG. Can be set to:
        * 'context_boosted': The context provided in the chat history is boosted in the RAG results,
            but results from the whole knowledge base can be retrieved;
        * 'limited_to_context': Only context provided in the chat history can be retrieved and used via RAG.
    - `timeout`: The timeout for the connection to the search engine. Can be set to "None" for no enforced timeout.
    - `disabled_tools`: A list of tools that the LLM is banned from using for this invocation.
    - `execution_mode`: The mode with which the LLM will answer. Defaults to
        'completion'. Only 'completion' is supported — 'simple' and 'agentic'
        are deprecated and rejected by the backend with HTTP 400:
        * 'completion': Pure pass-through — no system prompt or processing, just forwards messages to the LLM;
    - `fail_condition`: Custom condition to determine when the stream should be considered
        failed. Receives the list of ChatStreamEvent dicts collected so far and returns
        True to trigger an ApiConnectionError. If None, defaults to failing on events
        with channel ``'error'``.
    - `end_condition`: Custom condition to determine when the stream should stop early.
        Receives the list of ChatStreamEvent dicts collected so far and returns True to
        end the stream. If None, defaults to streaming until completion (or timeout).
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.
    - `**kwargs`: Additional keyword arguments are merged into the request body.
        Explicit parameters above take precedence over kwargs.

    ## Yields
    `ChatStreamEvent` dicts. Common channels:
    - `'text'`: Accumulated generated text so far.
    - `'agentic'`: Tool-call or agent status updates.
    - `'context'`: RAG context entities retrieved.
    - `'final_prompt'`: The full prompt sent to the LLM.
    - `'heartbeat'`: Keep-alive pings (can be ignored).
    - `'error'`: Error messages from the server.

    ## Raises
    - `StopAsyncIterationWithResult`: When the stream ends normally. `value` holds
        the final accumulated text response (``str``).
    - `ApiConnectionError`: If the connection or initial response failed, or the
        fail_condition returned True.
    """
    if fail_condition is None:
        fail_condition = lambda events: any(e.get("channel") == "error" for e in events)
    if end_condition is None:
        end_condition = lambda _events: False

    if not client:
        client = get_default_client()
    endpoint_url, headers, body = _build_request(
        prompt,
        chat_history=chat_history,
        workspaces=workspaces,
        context_mode=context_mode,
        model_name=model_name,
        execution_mode=execution_mode,
        disabled_tools=disabled_tools,
        streaming=True,
        client=client,
        extra_body=kwargs,
    )

    async def _parse_lines(resp: httpx.Response) -> AsyncIterator[ChatStreamEvent]:
        async for line in resp.aiter_lines():
            if not line.strip():
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                _logger.warning("chat streaming: unparsable line: %s", line[:200])

    collected_events: List[ChatStreamEvent] = []
    accumulated_text = ""
    try:
        async with httpx.AsyncClient() as httpx_client:
            async with httpx_client.stream(
                "POST", endpoint_url, json=body, headers=headers, timeout=timeout
            ) as response:
                if response.status_code != 200:
                    await response.aread()
                    raise ConnectionError(
                        f"chat streaming: HTTP {response.status_code}: {response.text[:500]}"
                    )

                event_stream = _parse_lines(response)
                if timeout is not None:
                    event_stream = TimeoutAsyncGenerator(event_stream, timeout)

                try:
                    async for event in event_stream:
                        collected_events.append(event)

                        if event.get("channel") == "text":
                            accumulated_text += event.get("content", "")

                        if fail_condition(collected_events):
                            raise ConnectionError(
                                "chat streaming: fail_condition triggered"
                            )
                        if end_condition(collected_events):
                            break

                        yield event
                except _asyncio.TimeoutError:
                    _logger.warning(
                        "chat streaming: timed out after %s seconds", timeout
                    )
    except (ConnectionError, httpx.HTTPStatusError) as e:
        raise ApiConnectionError("chat streaming", None, client) from e
    raise StopAsyncIterationWithResult(value=accumulated_text)
