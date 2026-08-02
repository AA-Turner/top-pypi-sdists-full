"""OpenAI Completion-like API adapter - CompletionModel implementation.

Thin wrapper that maps CompletionRequest to OpenAI Completion-like payloads,
opens an SSE stream, and maps chunks to CompletionChunk.
"""

import json
import os
from collections.abc import AsyncIterator
from typing import Any

import httpx
import structlog

from mistralai.vibe.sdk.providers.completion import utils
from mistralai.vibe.sdk.providers.completion.port import CompletionModel
from mistralai.vibe.sdk.providers.completion.types import (
    CompletionChunk,
    CompletionRequest,
    ToolCallDelta,
)
from mistralai.vibe.sdk.providers.completion.usage import TokenUsage

logger = structlog.get_logger()
_DEFAULT_OPENAI_BASE_URL = "https://api.openai.com/v1"
_OPENAI_USAGE_NESTED_ALIASES = {
    "cached_tokens": ("prompt_tokens_details", "cached_tokens"),
    "reasoning_tokens": ("completion_tokens_details", "reasoning_tokens"),
}


class OpenAIAPIError(utils.StreamHTTPError):
    """HTTP error returned by an OpenAI Completion-like API."""

    def __init__(self, status_code: int, body: str) -> None:
        super().__init__(
            f"OpenAI Completion-like API error {status_code}: {body}",
            status_code=status_code,
            body=body,
        )


class OpenAICompletion(CompletionModel):
    """OpenAI Completion-like API adapter implementing CompletionModel."""

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4.1",
        *,
        base_url: str = _DEFAULT_OPENAI_BASE_URL,
        timeout: float = 60.0,
        temperature: float | None = None,
        client: httpx.AsyncClient | None = None,
        reasoning_effort: str | None = None,
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._temperature = temperature
        self._client = client
        self.model = model
        self.reasoning_effort = reasoning_effort

    @property
    def client(self) -> httpx.AsyncClient:
        """Lazy-initialize the HTTP client on first access."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self._base_url,
                timeout=httpx.Timeout(self._timeout),
                headers={
                    "Authorization": f"Bearer {self._api_key}",
                    "Content-Type": "application/json",
                },
            )
        return self._client

    @classmethod
    def from_env(cls, model: str = "gpt-4.1") -> "OpenAICompletion":
        """Construct from OPENAI_API_KEY."""
        return cls(api_key=os.environ["OPENAI_API_KEY"], model=model)

    async def _open_stream(self, payload: dict[str, Any]) -> httpx.Response:
        """Open the OpenAI streaming response with bounded retry."""
        async for attempt in utils.build_stream_open_retrying(log_event="openai_stream_retry"):
            with attempt:
                request = self.client.build_request(
                    "POST",
                    "/chat/completions",
                    json=payload,
                )
                response = await self.client.send(request, stream=True)
                if response.is_success:
                    return response

                body = (await response.aread()).decode("utf-8", errors="replace")
                await response.aclose()
                raise OpenAIAPIError(response.status_code, body)

        msg = "stream retry loop exited without returning or raising"
        raise RuntimeError(msg)

    def _chunk_from_choice(self, choice: dict[str, Any]) -> CompletionChunk | None:
        delta = choice.get("delta") or {}
        content_delta = delta.get("content")
        if not isinstance(content_delta, str):
            content_delta = None

        thinking_delta = delta.get("reasoning_content")
        if not isinstance(thinking_delta, str):
            thinking_delta = None

        tool_call_deltas: list[ToolCallDelta] | None = None
        raw_tool_calls = delta.get("tool_calls")
        if isinstance(raw_tool_calls, list) and raw_tool_calls:
            tool_call_deltas = []
            for raw_tool_call in raw_tool_calls:
                if not isinstance(raw_tool_call, dict):
                    continue
                function = raw_tool_call.get("function")
                function_name = None
                arguments_delta = None
                if isinstance(function, dict):
                    if isinstance(function.get("name"), str):
                        function_name = function["name"]
                    if isinstance(function.get("arguments"), str):
                        arguments_delta = function["arguments"]

                index = raw_tool_call.get("index", 0)
                if not isinstance(index, int):
                    index = 0

                tool_call_deltas.append(
                    ToolCallDelta(
                        index=index,
                        id=raw_tool_call.get("id")
                        if isinstance(raw_tool_call.get("id"), str)
                        else None,
                        function_name=function_name,
                        arguments_delta=arguments_delta,
                    )
                )
            if not tool_call_deltas:
                tool_call_deltas = None

        finish_reason = choice.get("finish_reason")
        if not isinstance(finish_reason, str):
            finish_reason = None

        if (
            content_delta is None
            and thinking_delta is None
            and tool_call_deltas is None
            and finish_reason is None
        ):
            return None

        return CompletionChunk(
            content_delta=content_delta,
            thinking_delta=thinking_delta,
            tool_call_deltas=tool_call_deltas,
            finish_reason=finish_reason,
        )

    async def complete(self, request: CompletionRequest) -> AsyncIterator[CompletionChunk]:
        """Stream the completion using an OpenAI Completion-like API."""
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": [message.model_dump(exclude_none=True) for message in request.messages],
            "stream": True,
            "stream_options": {"include_usage": True},
        }
        if request.tools:
            payload["tools"] = [tool.model_dump() for tool in request.tools]
        if self.reasoning_effort is not None:
            payload["reasoning_effort"] = self.reasoning_effort
        if self._temperature is not None:
            payload["temperature"] = self._temperature

        logger.debug(
            "openai_stream_start",
            model=self.model,
            n_messages=len(payload["messages"]),
        )

        response = await self._open_stream(payload)
        chunk_count = 0

        try:
            async for data in utils.iter_sse_data(response):
                if data == "[DONE]":
                    break

                try:
                    chunk_data = json.loads(data)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"Invalid OpenAI SSE payload: {data}") from exc

                usage = TokenUsage.from_mapping_usage(
                    chunk_data.get("usage"),
                    nested_aliases=_OPENAI_USAGE_NESTED_ALIASES,
                )

                chunk: CompletionChunk | None = None
                choices = chunk_data.get("choices")
                if isinstance(choices, list) and choices:
                    choice = choices[0]
                    if isinstance(choice, dict):
                        chunk = self._chunk_from_choice(choice)

                if chunk is not None:
                    if usage is not None:
                        chunk = chunk.model_copy(update={"usage": usage})
                    chunk_count += 1
                    yield chunk
                elif usage is not None:
                    yield CompletionChunk(usage=usage)
        finally:
            await response.aclose()
            logger.debug("openai_stream_end", total_chunks=chunk_count)
