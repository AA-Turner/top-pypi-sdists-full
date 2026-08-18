"""Mistral completion adapter — CompletionModel implementation.

Thin wrapper that maps CompletionRequest to Mistral SDK types,
calls the streaming API, and maps chunks to CompletionChunk.
"""

import os
from collections.abc import AsyncIterator, Mapping
from typing import TYPE_CHECKING, Any

import structlog
from pydantic import TypeAdapter

from mistralai.vibe.sdk.observability.otel.instrumentation import (
    configure_mistral_client_telemetry,
)
from mistralai.vibe.sdk.providers.completion import utils
from mistralai.vibe.sdk.providers.completion.messages import Message
from mistralai.vibe.sdk.providers.completion.port import CompletionModel
from mistralai.vibe.sdk.providers.completion.types import (
    CompletionChunk,
    CompletionRequest,
    ToolCallDelta,
)
from mistralai.vibe.sdk.providers.completion.usage import TokenUsage

if TYPE_CHECKING:
    from mistralai.client import Mistral

logger = structlog.get_logger()
_MISTRAL_USAGE_NESTED_ALIASES = {
    "cached_tokens": ("prompt_tokens_details", "cached_tokens"),
    "reasoning_tokens": ("completion_tokens_details", "reasoning_tokens"),
}


def _dump_messages_for_mistral(messages: list[Message]) -> list[dict[str, Any]]:
    dumped = [message.model_dump(exclude_none=True) for message in messages]
    for message in dumped:
        content = message.get("content")
        if not isinstance(content, list):
            continue
        for part in content:
            if not isinstance(part, dict) or part.get("type") != "image_url":
                continue
            image_url = part.get("image_url")
            if isinstance(image_url, dict) and isinstance(image_url.get("url"), str):
                part["image_url"] = image_url["url"]
    return dumped


def _get_mistral_status_code(exc: BaseException) -> int | None:
    """Return the HTTP status code for a Mistral SDK error, if present."""
    try:
        from mistralai.client.errors.sdkerror import SDKError
    except Exception:
        return None

    if not isinstance(exc, SDKError):
        return None

    return exc.raw_response.status_code


def _is_retryable_mistral_exception(exc: BaseException) -> bool:
    """Return whether an LLM call failure looks transient and safe to retry."""
    if utils.is_retryable_httpx_error(exc):
        return True

    status_code = _get_mistral_status_code(exc)
    return status_code is not None and status_code in utils.RETRYABLE_STATUS_CODES


def _extract_deltas(content: object) -> tuple[str | None, str | None]:
    """Extract visible text and thinking text from a Mistral delta content field.

    The Mistral SDK's DeltaMessage.content can be:
    - str: plain text delta (common in streaming)
    - list[ContentChunk]: list of typed chunks (TextChunk, ThinkChunk, etc.)

    We split visible answer text from thinking/reasoning text so reasoning
    does not get flattened into user-visible assistant content.
    """
    if isinstance(content, str):
        return (content, None)
    if isinstance(content, list):
        content_parts: list[str] = []
        thinking_parts: list[str] = []
        for chunk in content:
            chunk_type = getattr(chunk, "type", None)
            if chunk_type == "thinking" or hasattr(chunk, "thinking"):
                thinking_content = getattr(chunk, "thinking", None)
                if thinking_content:
                    for inner in thinking_content:
                        if isinstance(inner, str):
                            thinking_parts.append(inner)
                        elif hasattr(inner, "text") and isinstance(inner.text, str):
                            thinking_parts.append(inner.text)
            elif hasattr(chunk, "text") and isinstance(chunk.text, str):
                content_parts.append(chunk.text)
        content_delta = "".join(content_parts) if content_parts else None
        thinking_delta = "".join(thinking_parts) if thinking_parts else None
        return (content_delta, thinking_delta)
    return (None, None)


class MistralCompletion(CompletionModel):
    """Mistral API adapter implementing CompletionModel.

    Thin wrapper that maps CompletionRequest to Mistral SDK types,
    calls the streaming API, and maps chunks to CompletionChunk.
    """

    def __init__(
        self,
        api_key: str | None,
        model: str = "mistral-small-latest",
        http_headers: Mapping[str, str] | None = None,
        prompt_cache_key: str | None = None,
        server_url: str | None = None,
        reasoning_effort: str | None = None,
    ) -> None:
        """Initialize the adapter.

        Client construction is deferred to first use to avoid blocking
        the Temporal workflow deterministic thread with SSL context loading
        during task reconstruction.

        Args:
            api_key: Mistral API key.
            model: Model name to use.
            reasoning_effort: Optional reasoning-effort, omitted when None.
        """
        self._api_key = api_key
        self._http_headers = dict(http_headers) if http_headers is not None else None
        self._prompt_cache_key = prompt_cache_key
        self._server_url = server_url
        self._client: Mistral | None = None
        self._model = model
        self.reasoning_effort = reasoning_effort

    @property
    def model(self) -> str:
        return self._model

    @property
    def client(self) -> "Mistral":
        """Lazy-initialize the Mistral client on first access."""
        if self._client is None:
            from mistralai.client import Mistral

            client = configure_mistral_client_telemetry(
                Mistral(api_key=self._api_key, server_url=self._server_url)
            )
            self._client = client
        assert self._client is not None
        return self._client

    @classmethod
    def from_env(
        cls,
        model: str = "mistral-small-latest",
        http_headers: Mapping[str, str] | None = None,
        prompt_cache_key: str | None = None,
        server_url: str | None = None,
    ) -> "MistralCompletion":
        """Construct from environment variables.

        Uses MISTRAL_CLIENT_API_KEY if set (needed when MISTRAL_API_KEY is the
        Workflows API stack key), otherwise falls back to MISTRAL_API_KEY.
        """
        api_key = os.environ.get("MISTRAL_CLIENT_API_KEY") or os.environ["MISTRAL_API_KEY"]
        return cls(
            api_key=api_key,
            model=model,
            http_headers=http_headers,
            prompt_cache_key=prompt_cache_key,
            server_url=server_url,
        )

    async def _open_stream(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None,
        metadata: dict[str, Any] | None,
    ) -> Any:
        """Open the Mistral streaming response with bounded retry."""
        from mistralai.client import models as mistral_models

        sdk_messages = TypeAdapter(
            list[mistral_models.ChatCompletionStreamRequestMessage],
        ).validate_python(messages)
        sdk_tools = (
            TypeAdapter(list[mistral_models.ChatCompletionStreamRequestTool]).validate_python(tools)
            if tools
            else None
        )
        # Only the initial request that opens the stream is retried; once bytes
        # are flowing, retrying would risk duplicating already emitted chunks.
        async for attempt in utils.build_stream_open_retrying(
            retry=_is_retryable_mistral_exception,
            log_event="mistral_stream_retry",
            status_of=_get_mistral_status_code,
        ):
            with attempt:
                kwargs: dict[str, Any] = {
                    "model": self.model,
                    "messages": sdk_messages,
                    "tools": sdk_tools if sdk_tools else None,
                    "parallel_tool_calls": True if tools else None,
                    "prompt_cache_key": self._prompt_cache_key,
                    "http_headers": self._http_headers,
                    "metadata": metadata,
                }
                if self.reasoning_effort is not None:
                    kwargs["reasoning_effort"] = self.reasoning_effort
                return await self.client.chat.stream_async(**kwargs)

        msg = "stream retry loop exited without returning or raising"
        raise RuntimeError(msg)

    async def complete(self, request: CompletionRequest) -> AsyncIterator[CompletionChunk]:
        """Stream the completion using Mistral API."""
        messages = _dump_messages_for_mistral(request.messages)
        tools = [tool.model_dump() for tool in request.tools] if request.tools else None

        logger.debug("mistral_stream_start", model=self.model, n_messages=len(messages))

        stream = await self._open_stream(
            messages=messages,
            tools=tools,
            metadata=request.metadata,
        )

        chunk_count = 0
        content_chunk_count = 0
        thinking_chunk_count = 0
        tool_chunk_count = 0

        async for event in stream:
            chunk_data = event.data
            usage = TokenUsage.from_attribute_usage(
                getattr(chunk_data, "usage", None),
                nested_aliases=_MISTRAL_USAGE_NESTED_ALIASES,
            )
            if not chunk_data.choices:
                if usage is not None:
                    yield CompletionChunk(usage=usage)
                continue
            choice = chunk_data.choices[0]
            delta = choice.delta
            chunk_count += 1

            content_delta = None
            thinking_delta = None
            tool_call_deltas = None

            if delta.content:
                content_delta, thinking_delta = _extract_deltas(delta.content)
                if content_delta:
                    content_chunk_count += 1
                if thinking_delta:
                    thinking_chunk_count += 1
                logger.debug(
                    "mistral_content_delta",
                    chunk_n=chunk_count,
                    content_type=type(delta.content).__name__,
                    delta_len=len(content_delta) if content_delta else 0,
                    delta_preview=content_delta[:40] if content_delta else None,
                    thinking_delta_len=len(thinking_delta) if thinking_delta else 0,
                    thinking_delta_preview=thinking_delta[:40] if thinking_delta else None,
                )

            if delta.tool_calls:
                tool_chunk_count += 1
                tool_call_deltas = []
                for tc in delta.tool_calls:
                    tool_call_deltas.append(
                        ToolCallDelta(
                            index=tc.index or 0,
                            id=tc.id if tc.id and tc.id != "null" else None,
                            function_name=(
                                tc.function.name if tc.function and tc.function.name else None
                            ),
                            arguments_delta=(
                                tc.function.arguments
                                if tc.function
                                and tc.function.arguments
                                and isinstance(tc.function.arguments, str)
                                else None
                            ),
                        )
                    )

            yield CompletionChunk(
                content_delta=content_delta,
                thinking_delta=thinking_delta,
                tool_call_deltas=tool_call_deltas,
                finish_reason=choice.finish_reason,
                usage=usage,
            )

        logger.debug(
            "mistral_stream_end",
            total_chunks=chunk_count,
            content_chunks=content_chunk_count,
            thinking_chunks=thinking_chunk_count,
            tool_chunks=tool_chunk_count,
        )
