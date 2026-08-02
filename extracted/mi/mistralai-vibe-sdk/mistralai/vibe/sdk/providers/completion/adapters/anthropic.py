"""Anthropic Messages API adapter — CompletionModel implementation.

Thin wrapper that maps CompletionRequest to Anthropic Messages payloads,
opens an SSE stream, and maps the typed event stream to CompletionChunk.
"""

import json
import os
import re
from collections.abc import AsyncIterator, Sequence
from typing import Any

import httpx
import structlog

from mistralai.vibe.sdk.providers.completion import utils
from mistralai.vibe.sdk.providers.completion.messages import Message
from mistralai.vibe.sdk.providers.completion.port import CompletionModel
from mistralai.vibe.sdk.providers.completion.types import (
    CompletionChunk,
    CompletionRequest,
    ToolCallDelta,
    ToolDefinition,
)
from mistralai.vibe.sdk.providers.completion.usage import TokenUsage

logger = structlog.get_logger()

_DEFAULT_ANTHROPIC_BASE_URL = "https://api.anthropic.com"
_ANTHROPIC_API_VERSION = "2023-06-01"
_BETA_FEATURES = (
    "interleaved-thinking-2025-05-14,"
    "fine-grained-tool-streaming-2025-05-14,"
    "prompt-caching-2024-07-31,"
    "context-1m-2025-08-07"
)
_DEFAULT_MAX_TOKENS = 4096
_ADAPTIVE_MAX_TOKENS = 32_768
_CACHEABLE_BLOCK_TYPES = frozenset({"text", "image", "tool_result"})


class AnthropicAPIError(utils.StreamHTTPError):
    """HTTP error returned by the Anthropic Messages API."""

    def __init__(self, status_code: int, body: str) -> None:
        super().__init__(
            f"Anthropic Messages API error {status_code}: {body}",
            status_code=status_code,
            body=body,
        )


def _sanitize_tool_call_id(tool_id: str | None) -> str:
    """Anthropic tool ids must match ``[a-zA-Z0-9_-]+``."""
    return re.sub(r"[^a-zA-Z0-9_-]", "_", tool_id or "")


class AnthropicMapper:
    """Convert standardized messages/tools into Anthropic Messages format."""

    def prepare_messages(
        self, messages: Sequence[Message]
    ) -> tuple[str | None, list[dict[str, Any]]]:
        """Return ``(system_prompt, converted_messages)``.

        Anthropic carries the system prompt out-of-band (top-level ``system``),
        and tool results are ``user`` messages containing ``tool_result``
        blocks, merged into the preceding user turn when adjacent.
        """
        system_parts: list[str] = []
        converted: list[dict[str, Any]] = []

        for msg in messages:
            match msg.role:
                case "system":
                    if msg.content:
                        system_parts.append(msg.content)
                case "user":
                    converted.append({"role": "user", "content": msg.content or ""})
                case "assistant":
                    converted.append(self._convert_assistant_message(msg))
                case "tool":
                    self._append_tool_result(converted, msg)

        system_prompt = "\n\n".join(system_parts) if system_parts else None
        return system_prompt, converted

    def _convert_assistant_message(self, msg: Message) -> dict[str, Any]:
        content: list[dict[str, Any]] = []
        if msg.content:
            content.append({"type": "text", "text": msg.content})
        for tc in msg.tool_calls or []:
            try:
                tool_input = json.loads(tc.function.arguments or "{}")
            except json.JSONDecodeError:
                tool_input = {}
            content.append(
                {
                    "type": "tool_use",
                    "id": _sanitize_tool_call_id(tc.id),
                    "name": tc.function.name,
                    "input": tool_input,
                }
            )
        return {"role": "assistant", "content": content if content else ""}

    def _append_tool_result(self, converted: list[dict[str, Any]], msg: Message) -> None:
        tool_result = {
            "type": "tool_result",
            "tool_use_id": _sanitize_tool_call_id(msg.tool_call_id),
            "content": msg.content or "",
        }

        if not converted or converted[-1]["role"] != "user":
            converted.append({"role": "user", "content": [tool_result]})
            return

        existing_content = converted[-1]["content"]
        if isinstance(existing_content, str):
            converted[-1]["content"] = (
                [{"type": "text", "text": existing_content}, tool_result]
                if existing_content
                else [tool_result]
            )
        else:
            existing_content.append(tool_result)

    def prepare_tools(self, tools: list[ToolDefinition] | None) -> list[dict[str, Any]] | None:
        if not tools:
            return None
        return [
            {
                "name": tool.function.name,
                "description": tool.function.description,
                "input_schema": tool.function.parameters,
            }
            for tool in tools
        ]


class AnthropicCompletion(CompletionModel):
    """Anthropic Messages API adapter implementing CompletionModel."""

    def __init__(
        self,
        api_key: str,
        model: str = "claude-sonnet-4-5",
        *,
        base_url: str = _DEFAULT_ANTHROPIC_BASE_URL,
        timeout: float = 60.0,
        max_tokens: int = _DEFAULT_MAX_TOKENS,
        thinking: str = "off",
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._client = client
        self._mapper = AnthropicMapper()
        self.model = model
        self.max_tokens = max_tokens
        self.thinking = thinking

    @property
    def client(self) -> httpx.AsyncClient:
        """Lazy-initialize the HTTP client on first access."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self._base_url,
                timeout=httpx.Timeout(self._timeout),
                headers={
                    "x-api-key": self._api_key,
                    "anthropic-version": _ANTHROPIC_API_VERSION,
                    "anthropic-beta": _BETA_FEATURES,
                    "Content-Type": "application/json",
                },
            )
        return self._client

    @classmethod
    def from_env(cls, model: str = "claude-sonnet-4-5") -> "AnthropicCompletion":
        """Construct from ANTHROPIC_API_KEY."""
        return cls(api_key=os.environ["ANTHROPIC_API_KEY"], model=model)

    def _apply_thinking_config(self, payload: dict[str, Any]) -> None:
        """Enable Anthropic extended thinking when configured."""
        if self.thinking == "off":
            payload["max_tokens"] = self.max_tokens
            return
        payload["thinking"] = {"type": "adaptive", "display": "summarized"}
        payload["output_config"] = {"effort": self.thinking}
        payload["max_tokens"] = max(self.max_tokens, _ADAPTIVE_MAX_TOKENS)

    @staticmethod
    def _build_system_blocks(system_prompt: str | None) -> list[dict[str, Any]]:
        if not system_prompt:
            return []
        return [
            {
                "type": "text",
                "text": system_prompt,
                "cache_control": {"type": "ephemeral"},
            }
        ]

    @staticmethod
    def _add_cache_control_to_last_user_message(messages: list[dict[str, Any]]) -> None:
        if not messages:
            return
        last_message = messages[-1]
        if last_message.get("role") != "user":
            return
        content = last_message.get("content")
        if not isinstance(content, list) or not content:
            return
        last_block = content[-1]
        if last_block.get("type") in _CACHEABLE_BLOCK_TYPES:
            last_block["cache_control"] = {"type": "ephemeral"}

    def _build_payload(
        self,
        *,
        system_prompt: str | None,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "stream": True,
        }
        self._apply_thinking_config(payload)
        if system_blocks := self._build_system_blocks(system_prompt):
            payload["system"] = system_blocks
        if tools:
            payload["tools"] = tools
        self._add_cache_control_to_last_user_message(messages)
        return payload

    async def _open_stream(self, payload: dict[str, Any]) -> httpx.Response:
        """Open the Anthropic streaming response with bounded retry."""
        async for attempt in utils.build_stream_open_retrying(log_event="anthropic_stream_retry"):
            with attempt:
                request = self.client.build_request(
                    "POST",
                    "/v1/messages",
                    json=payload,
                )
                response = await self.client.send(request, stream=True)
                if response.is_success:
                    return response

                body = (await response.aread()).decode("utf-8", errors="replace")
                await response.aclose()
                raise AnthropicAPIError(response.status_code, body)

        msg = "stream retry loop exited without returning or raising"
        raise RuntimeError(msg)

    @staticmethod
    def _input_usage(usage_data: dict[str, Any]) -> TokenUsage | None:
        input_tokens = usage_data.get("input_tokens", 0)
        cache_read = usage_data.get("cache_read_input_tokens", 0)
        cache_write = usage_data.get("cache_creation_input_tokens", 0)
        if not (input_tokens or cache_read or cache_write):
            return None
        return TokenUsage(
            input_tokens=input_tokens,
            cache_read_tokens=cache_read,
            cache_write_tokens=cache_write,
        )

    def _chunk_from_event(self, data: dict[str, Any]) -> CompletionChunk | None:
        """Map a single Anthropic stream event to a CompletionChunk."""
        event_type = data.get("type")
        match event_type:
            case "message_start":
                usage = self._input_usage(data.get("message", {}).get("usage", {}))
                return CompletionChunk(usage=usage) if usage is not None else None
            case "content_block_start":
                return self._chunk_from_block_start(data)
            case "content_block_delta":
                return self._chunk_from_block_delta(data)
            case "message_delta":
                return self._chunk_from_message_delta(data)
            case "error":
                error = data.get("error", {})
                error_type = error.get("type", "unknown_error")
                error_message = error.get("message", "Unknown streaming error")
                raise RuntimeError(f"Anthropic stream error ({error_type}): {error_message}")
            case _:
                # content_block_stop / message_stop / ping → nothing to emit.
                return None

    @staticmethod
    def _chunk_from_block_start(data: dict[str, Any]) -> CompletionChunk | None:
        block = data.get("content_block", {})
        index = data.get("index", 0)
        match block.get("type"):
            case "tool_use":
                return CompletionChunk(
                    tool_call_deltas=[
                        ToolCallDelta(
                            index=index,
                            id=block.get("id"),
                            function_name=block.get("name"),
                        )
                    ]
                )
            case "thinking":
                thinking = block.get("thinking", "")
                return CompletionChunk(thinking_delta=thinking) if thinking else None
            case _:
                return None

    @staticmethod
    def _chunk_from_block_delta(data: dict[str, Any]) -> CompletionChunk | None:
        delta = data.get("delta", {})
        index = data.get("index", 0)
        match delta.get("type"):
            case "text_delta":
                return CompletionChunk(content_delta=delta.get("text", ""))
            case "thinking_delta":
                return CompletionChunk(thinking_delta=delta.get("thinking", ""))
            case "input_json_delta":
                return CompletionChunk(
                    tool_call_deltas=[
                        ToolCallDelta(
                            index=index,
                            arguments_delta=delta.get("partial_json", ""),
                        )
                    ]
                )
            case _:
                # signature_delta has no home in CompletionChunk → drop it.
                return None

    @staticmethod
    def _chunk_from_message_delta(data: dict[str, Any]) -> CompletionChunk | None:
        delta = data.get("delta", {})
        finish_reason = delta.get("stop_reason")
        usage_data = data.get("usage", {})
        output_tokens = usage_data.get("output_tokens", 0) if usage_data else 0
        usage = TokenUsage(output_tokens=output_tokens) if output_tokens else None
        if finish_reason is None and usage is None:
            return None
        return CompletionChunk(finish_reason=finish_reason, usage=usage)

    async def complete(self, request: CompletionRequest) -> AsyncIterator[CompletionChunk]:
        """Stream the completion using the Anthropic Messages API."""
        system_prompt, messages = self._mapper.prepare_messages(request.messages)
        tools = self._mapper.prepare_tools(request.tools)
        payload = self._build_payload(
            system_prompt=system_prompt,
            messages=messages,
            tools=tools,
        )

        logger.debug(
            "anthropic_stream_start",
            model=self.model,
            n_messages=len(messages),
        )

        response = await self._open_stream(payload)
        chunk_count = 0

        try:
            async for raw in utils.iter_sse_data(response):
                try:
                    data = json.loads(raw)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"Invalid Anthropic SSE payload: {raw}") from exc

                chunk = self._chunk_from_event(data)
                if chunk is not None:
                    chunk_count += 1
                    yield chunk
        finally:
            await response.aclose()
            logger.debug("anthropic_stream_end", total_chunks=chunk_count)
