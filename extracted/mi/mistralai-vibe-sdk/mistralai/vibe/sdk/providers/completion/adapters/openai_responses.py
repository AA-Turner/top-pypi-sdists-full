"""OpenAI Responses API adapter - CompletionModel implementation."""

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
_OPENAI_RESPONSES_USAGE_NESTED_ALIASES = {
    "cached_tokens": ("input_tokens_details", "cached_tokens"),
    "cache_write_tokens": ("input_tokens_details", "cache_write_tokens"),
    "reasoning_tokens": ("output_tokens_details", "reasoning_tokens"),
}


class OpenAIResponsesAPIError(utils.StreamHTTPError):
    """HTTP error returned by the OpenAI Responses API."""

    def __init__(self, status_code: int, body: str) -> None:
        super().__init__(
            f"OpenAI Responses API error {status_code}: {body}",
            status_code=status_code,
            body=body,
        )


class OpenAIResponsesCompletion(CompletionModel):
    """OpenAI Responses API adapter implementing CompletionModel."""

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
        reasoning_summary: str | None = "auto",
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._temperature = temperature
        self._client = client
        self.model = model
        self.reasoning_effort = reasoning_effort
        self.reasoning_summary = reasoning_summary

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
    def from_env(cls, model: str = "gpt-4.1") -> "OpenAIResponsesCompletion":
        """Construct from OPENAI_API_KEY."""
        return cls(api_key=os.environ["OPENAI_API_KEY"], model=model)

    async def _open_stream(self, payload: dict[str, Any]) -> httpx.Response:
        """Open the OpenAI Responses streaming response with bounded retry."""
        async for attempt in utils.build_stream_open_retrying(
            log_event="openai_responses_stream_retry"
        ):
            with attempt:
                request = self.client.build_request(
                    "POST",
                    "/responses",
                    json=payload,
                )
                response = await self.client.send(request, stream=True)
                if response.is_success:
                    return response

                body = (await response.aread()).decode("utf-8", errors="replace")
                await response.aclose()
                raise OpenAIResponsesAPIError(response.status_code, body)

        msg = "stream retry loop exited without returning or raising"
        raise RuntimeError(msg)

    @staticmethod
    def _event_usage(event: dict[str, Any]) -> TokenUsage | None:
        response = event.get("response")
        if not isinstance(response, dict):
            return None
        return TokenUsage.from_mapping_usage(
            response.get("usage"),
            nested_aliases=_OPENAI_RESPONSES_USAGE_NESTED_ALIASES,
        )

    def _chunk_from_event(self, event: dict[str, Any]) -> CompletionChunk | None:
        event_type = event.get("type")
        match event_type:
            case "response.output_text.delta" | "response.refusal.delta":
                delta = event.get("delta")
                return CompletionChunk(content_delta=delta) if isinstance(delta, str) else None
            case "response.reasoning_text.delta" | "response.reasoning_summary_text.delta":
                delta = event.get("delta")
                return CompletionChunk(thinking_delta=delta) if isinstance(delta, str) else None
            case "response.output_item.added":
                item = event.get("item")
                if not isinstance(item, dict) or item.get("type") != "function_call":
                    return None
                output_index = event.get("output_index", 0)
                call_id = item.get("call_id")
                name = item.get("name")
                index = output_index if isinstance(output_index, int) else 0
                call_id = call_id if isinstance(call_id, str) else None
                name = name if isinstance(name, str) else None
                return CompletionChunk(
                    tool_call_deltas=[
                        ToolCallDelta(
                            index=index,
                            id=call_id,
                            function_name=name,
                        )
                    ]
                )
            case "response.function_call_arguments.delta":
                delta = event.get("delta")
                if not isinstance(delta, str):
                    return None
                output_index = event.get("output_index", 0)
                index = output_index if isinstance(output_index, int) else 0
                return CompletionChunk(
                    tool_call_deltas=[
                        ToolCallDelta(
                            index=index,
                            arguments_delta=delta,
                        )
                    ]
                )
            case "response.completed":
                response = event.get("response")
                output = response.get("output") if isinstance(response, dict) else None
                has_tool_calls = isinstance(output, list) and any(
                    isinstance(item, dict) and item.get("type") == "function_call"
                    for item in output
                )
                return CompletionChunk(
                    finish_reason="tool_calls" if has_tool_calls else "stop",
                    usage=self._event_usage(event),
                )
            case "response.incomplete":
                response = event.get("response")
                details = response.get("incomplete_details") if isinstance(response, dict) else None
                finish_reason = details.get("reason") if isinstance(details, dict) else None
                return CompletionChunk(
                    finish_reason=finish_reason,
                    usage=self._event_usage(event),
                )
            case "response.failed" | "error":
                response = event.get("response")
                error = (response.get("error") or {}) if isinstance(response, dict) else event
                error_code = error.get("code", "unknown_error")
                error_message = error.get("message", "Unknown streaming error")
                raise RuntimeError(f"OpenAI Responses stream error ({error_code}): {error_message}")
            case _:
                return None

    def _build_payload(self, request: CompletionRequest) -> dict[str, Any]:
        input_items: list[dict[str, Any]] = []
        for message in request.messages:
            if message.role == "tool":
                input_items.append(
                    {
                        "type": "function_call_output",
                        "call_id": message.tool_call_id or "",
                        "output": message.content or "",
                    }
                )
            elif message.role == "assistant":
                if message.content is not None:
                    input_items.append(
                        {"type": "message", "role": "assistant", "content": message.content}
                    )
                for tool_call in message.tool_calls or []:
                    input_items.append(
                        {
                            "type": "function_call",
                            "call_id": tool_call.id,
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments,
                        }
                    )
                if message.content is None and not message.tool_calls:
                    input_items.append({"type": "message", "role": "assistant", "content": ""})
            else:
                input_items.append(
                    {"type": "message", "role": message.role, "content": message.content or ""}
                )

        payload: dict[str, Any] = {
            "model": self.model,
            "input": input_items,
            "stream": True,
        }
        if request.tools:
            payload["tools"] = [
                {
                    "type": "function",
                    "name": tool.function.name,
                    "description": tool.function.description,
                    "parameters": tool.function.parameters,
                    "strict": False,
                }
                for tool in request.tools
            ]
        if self.reasoning_effort is not None:
            payload["reasoning"] = {"effort": self.reasoning_effort}
            if self.reasoning_summary is not None:
                payload["reasoning"]["summary"] = self.reasoning_summary
        if self._temperature is not None:
            payload["temperature"] = self._temperature
        return payload

    async def complete(self, request: CompletionRequest) -> AsyncIterator[CompletionChunk]:
        """Stream the completion using the OpenAI Responses API."""
        payload = self._build_payload(request)

        logger.debug(
            "openai_responses_stream_start",
            model=self.model,
            n_input_items=len(payload["input"]),
        )

        response = await self._open_stream(payload)
        chunk_count = 0

        try:
            async for data in utils.iter_sse_data(response):
                if data == "[DONE]":
                    break

                try:
                    event = json.loads(data)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"Invalid OpenAI Responses SSE payload: {data}") from exc

                chunk = self._chunk_from_event(event)
                if chunk is not None:
                    chunk_count += 1
                    yield chunk
        finally:
            await response.aclose()
            logger.debug("openai_responses_stream_end", total_chunks=chunk_count)
