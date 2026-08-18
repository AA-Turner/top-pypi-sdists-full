"""Ollama native API adapter - CompletionModel implementation.

Thin wrapper that maps CompletionRequest to Ollama /api/chat payloads,
opens an NDJSON stream, and maps chunks to CompletionChunk.

Uses Ollama's native API (not the OpenAI-compatible shim) because the
latter silently drops tool_calls in streaming mode.
"""

import json
from collections.abc import AsyncIterator
from typing import Any

import httpx
import structlog

from mistralai.vibe.sdk.providers.completion import utils
from mistralai.vibe.sdk.providers.completion.messages import Message, text_content_for_provider
from mistralai.vibe.sdk.providers.completion.port import CompletionModel
from mistralai.vibe.sdk.providers.completion.types import (
    CompletionChunk,
    CompletionRequest,
    ToolCallDelta,
)
from mistralai.vibe.sdk.providers.completion.usage import TokenUsage

logger = structlog.get_logger()
_DEFAULT_OLLAMA_BASE_URL = "http://localhost:11434"


class OllamaAPIError(utils.StreamHTTPError):
    """HTTP error returned by the Ollama API."""

    def __init__(self, status_code: int, body: str) -> None:
        super().__init__(
            f"Ollama API error {status_code}: {body}",
            status_code=status_code,
            body=body,
        )


def _parse_tool_call_deltas(
    raw_tool_calls: list[Any], *, index_offset: int = 0
) -> list[ToolCallDelta] | None:
    """Parse Ollama tool calls into SDK ToolCallDelta values.

    ``index_offset`` ensures indices are unique across chunks when Ollama
    streams each parallel tool call as a separate NDJSON line.
    """
    deltas: list[ToolCallDelta] = []
    for i, raw_tool_call in enumerate(raw_tool_calls):
        if not isinstance(raw_tool_call, dict):
            continue
        function = raw_tool_call.get("function") or {}
        function_name = function.get("name") if isinstance(function, dict) else None
        arguments = function.get("arguments") if isinstance(function, dict) else None
        arguments_delta = json.dumps(arguments) if arguments is not None else None
        idx = index_offset + i
        deltas.append(
            ToolCallDelta(
                index=idx,
                id=f"ollama_call_{idx}",
                function_name=function_name,
                arguments_delta=arguments_delta,
            )
        )
    return deltas or None


def _parse_arguments(raw: str) -> dict[str, Any]:
    """Parse a JSON-encoded arguments string, falling back to ``{}``."""
    if not raw:
        return {}
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _convert_messages(messages: list[Message]) -> list[dict[str, Any]]:
    """Convert SDK Messages to Ollama's native message format.

    Tool-result messages need ``tool_name`` (Ollama's native binding field)
    instead of ``tool_call_id``.  The name is resolved from the preceding
    assistant message's tool_calls list.
    """
    tool_id_to_name: dict[str, str] = {}
    converted: list[dict[str, Any]] = []
    for message in messages:
        if message.tool_calls:
            for tc in message.tool_calls:
                tool_id_to_name[tc.id] = tc.function.name

        msg: dict[str, Any] = {"role": message.role}
        text_content = text_content_for_provider("Ollama", message.content)
        if text_content is not None:
            msg["content"] = text_content
        if message.tool_calls:
            msg["tool_calls"] = [
                {
                    "function": {
                        "name": tc.function.name,
                        "arguments": _parse_arguments(tc.function.arguments),
                    },
                }
                for tc in message.tool_calls
            ]
        if message.role == "tool" and message.tool_call_id:
            name = tool_id_to_name.get(message.tool_call_id)
            if name:
                msg["tool_name"] = name
        converted.append(msg)
    return converted


class OllamaCompletion(CompletionModel):
    """Ollama native API adapter implementing CompletionModel."""

    def __init__(
        self,
        model: str,
        *,
        base_url: str = _DEFAULT_OLLAMA_BASE_URL,
        timeout: float = 120.0,
        temperature: float | None = None,
        think: bool | str | None = None,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._temperature = temperature
        self._think = think
        self._client = client
        self._model = model

    @property
    def model(self) -> str:
        return self._model

    @property
    def client(self) -> httpx.AsyncClient:
        """Lazy-initialize the HTTP client on first access."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self._base_url,
                timeout=httpx.Timeout(self._timeout),
                headers={"Content-Type": "application/json"},
            )
        return self._client

    async def _open_stream(self, payload: dict[str, Any]) -> httpx.Response:
        """Open the Ollama streaming response with bounded retry."""
        async for attempt in utils.build_stream_open_retrying(log_event="ollama_stream_retry"):
            with attempt:
                request = self.client.build_request(
                    "POST",
                    "/api/chat",
                    json=payload,
                )
                response = await self.client.send(request, stream=True)
                if response.is_success:
                    return response

                body = (await response.aread()).decode("utf-8", errors="replace")
                await response.aclose()
                raise OllamaAPIError(response.status_code, body)

        msg = "stream retry loop exited without returning or raising"
        raise RuntimeError(msg)

    def _build_payload(self, request: CompletionRequest) -> dict[str, Any]:
        """Assemble the Ollama /api/chat request payload."""
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": _convert_messages(request.messages),
            "stream": True,
        }
        if request.tools:
            payload["tools"] = [tool.model_dump() for tool in request.tools]
        if self._think is not None:
            payload["think"] = self._think
        if self._temperature is not None:
            payload["options"] = {"temperature": self._temperature}
        return payload

    async def complete(self, request: CompletionRequest) -> AsyncIterator[CompletionChunk]:
        """Stream the completion using Ollama's native /api/chat endpoint."""
        payload = self._build_payload(request)

        logger.debug(
            "ollama_stream_start",
            model=self.model,
            n_messages=len(payload["messages"]),
        )

        response = await self._open_stream(payload)
        chunk_count = 0
        saw_tool_calls = False
        tool_call_count = 0

        try:
            async for line in response.aiter_lines():
                if not line.strip():
                    continue

                try:
                    data = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"Invalid Ollama NDJSON payload: {line}") from exc

                if "error" in data:
                    raise OllamaAPIError(200, str(data["error"]))

                message = data.get("message") or {}
                done = data.get("done", False)

                content_delta = message.get("content")
                if not isinstance(content_delta, str) or not content_delta:
                    content_delta = None

                thinking_delta = message.get("thinking")
                if not isinstance(thinking_delta, str) or not thinking_delta:
                    thinking_delta = None

                tool_call_deltas: list[ToolCallDelta] | None = None
                raw_tool_calls = message.get("tool_calls")
                if isinstance(raw_tool_calls, list) and raw_tool_calls:
                    saw_tool_calls = True
                    tool_call_deltas = _parse_tool_call_deltas(
                        raw_tool_calls, index_offset=tool_call_count
                    )
                    tool_call_count += len(raw_tool_calls)

                if (
                    content_delta is not None
                    or thinking_delta is not None
                    or tool_call_deltas is not None
                ):
                    chunk_count += 1
                    yield CompletionChunk(
                        content_delta=content_delta,
                        thinking_delta=thinking_delta,
                        tool_call_deltas=tool_call_deltas,
                    )

                if done:
                    usage = TokenUsage(
                        input_tokens=data.get("prompt_eval_count", 0),
                        output_tokens=data.get("eval_count", 0),
                    )
                    finish_reason = "tool_calls" if saw_tool_calls else "stop"
                    chunk_count += 1
                    yield CompletionChunk(
                        finish_reason=finish_reason,
                        usage=usage,
                    )
                    break
        finally:
            await response.aclose()
            logger.debug("ollama_stream_end", total_chunks=chunk_count)
