"""LLM wrapper with ATIF-formatted OpenTelemetry tracing.

Wraps litellm to provide multi-provider LLM access with automatic ATIF span
emission for every call. This gives worlds the same level of tracing visibility
as agents get.

Usage:
    from plato.llm import completion, acompletion

    # Sync
    response = completion(
        model="anthropic/claude-haiku-4-5-20251001",
        messages=[{"role": "user", "content": "Hello"}],
    )

    # Async
    response = await acompletion(
        model="openai/gpt-4o",
        messages=[{"role": "user", "content": "Hello"}],
        tools=[...],
    )

    # Access response (OpenAI format)
    text = response.text                    # convenience: first text content
    tool_calls = response.tool_calls        # convenience: list of tool calls
    tokens = response.usage                 # prompt_tokens, completion_tokens, total_tokens
    cost = response.cost                    # cost in USD (from litellm)

All calls automatically emit ATIF spans via plato.otel when tracing is initialized.
"""

from __future__ import annotations

import json
import logging
import time
from typing import TYPE_CHECKING, Any

import litellm
from pydantic import BaseModel, Field

from plato.otel import get_tracer

litellm.suppress_debug_info = True  # type: ignore[assignment]
logging.getLogger("LiteLLM").setLevel(logging.WARNING)

if TYPE_CHECKING:
    from plato.worlds.config import LLMConfig
    from plato.worlds.result_store import ResultStore

logger = logging.getLogger(__name__)


def _cache_key(model: str, messages: list[dict], **kwargs: Any) -> str:
    """Content-addressed cache key for an LLM call using blake3."""
    import blake3

    def _normalize_content(content: Any) -> Any:
        if isinstance(content, list):
            out = []
            for item in content:
                if isinstance(item, dict) and item.get("type") == "image_url":
                    url = item.get("image_url", {}).get("url", "")
                    out.append({"type": "image_url", "hash": blake3.blake3(url.encode()).hexdigest()[:32]})
                else:
                    out.append(item)
            return out
        return content

    normalized = [{**m, "content": _normalize_content(m.get("content"))} for m in messages]
    clean = {k: v for k, v in sorted(kwargs.items()) if v is not None}
    canonical = json.dumps({"model": model, "messages": normalized, **clean}, sort_keys=True, separators=(",", ":"))
    digest = blake3.blake3(canonical.encode()).hexdigest()[:64]
    return f"llm:{digest}"


class LLMClient:
    """Convenience wrapper around an LLMConfig for worlds.

    Usage:
        client = LLMClient(config)
        response = await client(messages=[...])         # async
        response = client.sync(messages=[...])          # sync

    Caching:
        client = LLMClient(config, store=result_store)
        # Identical calls return cached LLMResponse (text only, no raw)
    """

    def __init__(self, config: LLMConfig, store: ResultStore | None = None) -> None:
        self._model = config.model
        self._api_key = config.api_key or None
        self._max_tokens = config.max_tokens
        self._temperature = config.temperature
        self._store = store

    async def __call__(
        self,
        messages: list[dict],
        *,
        system: str | None = None,
        tools: list[dict] | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
        timeout: int = 120,
        num_retries: int = 2,
        **kwargs: Any,
    ) -> LLMResponse:
        if self._api_key:
            kwargs.setdefault("api_key", self._api_key)

        # Check cache
        if self._store is not None:
            key = _cache_key(self._model, messages, system=system, **kwargs)
            cached = self._store.get(key)
            if cached is not None:
                logger.debug("LLM cache hit: model=%s, key=%s", self._model, key[:20])
                return LLMResponse(**json.loads(cached))

        response = await acompletion(
            model=self._model,
            messages=messages,
            system=system,
            tools=tools,
            max_tokens=max_tokens or self._max_tokens,
            temperature=temperature if temperature is not None else self._temperature,
            timeout=timeout,
            num_retries=num_retries,
            **kwargs,
        )

        # Store in cache (without raw response — not serializable)
        if self._store is not None and response.text:
            data = response.model_dump(exclude={"raw"})
            self._store.put(key, json.dumps(data))

        return response

    async def image_generation(
        self,
        prompt: str,
        *,
        model: str | None = None,
        n: int = 1,
        size: str = "1024x1024",
        response_format: str = "b64_json",
        timeout: int = 120,
        **kwargs: Any,
    ) -> ImageResponse:
        """Generate images via litellm.aimage_generation().

        Args:
            prompt: Text description of the image to generate.
            model: Override model (default: uses client's model).
            n: Number of images to generate.
            size: Image size (e.g. "1024x1024").
            response_format: "b64_json" or "url".
            timeout: Request timeout in seconds.
        """
        if self._api_key:
            kwargs.setdefault("api_key", self._api_key)
        return await aimage_generation(
            prompt=prompt,
            model=model or self._model,
            n=n,
            size=size,
            response_format=response_format,
            timeout=timeout,
            **kwargs,
        )

    def sync(
        self,
        messages: list[dict],
        *,
        system: str | None = None,
        tools: list[dict] | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
        timeout: int = 120,
        num_retries: int = 2,
        **kwargs: Any,
    ) -> LLMResponse:
        if self._api_key:
            kwargs.setdefault("api_key", self._api_key)
        return completion(
            model=self._model,
            messages=messages,
            system=system,
            tools=tools,
            max_tokens=max_tokens or self._max_tokens,
            temperature=temperature if temperature is not None else self._temperature,
            timeout=timeout,
            num_retries=num_retries,
            **kwargs,
        )


# Global step counter for ATIF span IDs (per-session)
_step_counter = 0


def _next_step_id() -> int:
    global _step_counter
    _step_counter += 1
    return _step_counter


def reset_step_counter() -> None:
    """Reset the global step counter (useful for tests or new sessions)."""
    global _step_counter
    _step_counter = 0


class TokenUsage(BaseModel):
    """Token usage from an LLM response."""

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class ToolCall(BaseModel):
    """A single tool call from an LLM response."""

    id: str = ""
    function_name: str = ""
    arguments: dict = Field(default_factory=dict)
    arguments_raw: str = ""


class LLMResponse(BaseModel):
    """Unified response from an LLM call.

    Provides convenient access to text, tool calls, usage, and cost
    regardless of the underlying provider.
    """

    model_config = {"arbitrary_types_allowed": True}

    text: str = ""
    tool_calls: list[ToolCall] = Field(default_factory=list)
    usage: TokenUsage = Field(default_factory=TokenUsage)
    cost: float = 0.0
    model: str = ""
    stop_reason: str = ""
    raw: Any = None  # The raw litellm ModelResponse

    @property
    def has_tool_calls(self) -> bool:
        return len(self.tool_calls) > 0


class ImageData(BaseModel):
    """A single generated image."""

    b64_json: str = ""
    url: str = ""
    revised_prompt: str = ""


class ImageResponse(BaseModel):
    """Response from an image generation call."""

    model_config = {"arbitrary_types_allowed": True}

    data: list[ImageData] = Field(default_factory=list)
    model: str = ""
    raw: Any = None


def _convert_tools_to_openai_format(tools: list[dict]) -> list[dict]:
    """Convert Anthropic-style tool dicts to OpenAI function-calling format.

    Accepts both formats:
    - Anthropic: {"name": "...", "description": "...", "input_schema": {...}}
    - OpenAI:    {"type": "function", "function": {"name": "...", ...}}

    Returns OpenAI format always.
    """
    converted = []
    for tool in tools:
        if tool.get("type") == "function":
            # Already OpenAI format
            converted.append(tool)
        elif "name" in tool and "input_schema" in tool:
            # Anthropic format -> OpenAI format
            converted.append(
                {
                    "type": "function",
                    "function": {
                        "name": tool["name"],
                        "description": tool.get("description", ""),
                        "parameters": tool["input_schema"],
                    },
                }
            )
        else:
            # Unknown format, pass through
            converted.append(tool)
    return converted


def _parse_response(raw_response: Any, model: str) -> LLMResponse:
    """Parse a litellm ModelResponse into our LLMResponse."""
    # Extract text
    text = ""
    choice = raw_response.choices[0] if raw_response.choices else None
    if choice and choice.message:
        text = choice.message.content or ""

    # Extract tool calls
    tool_calls = []
    if choice and choice.message and choice.message.tool_calls:
        for tc in choice.message.tool_calls:
            args_raw = tc.function.arguments if tc.function.arguments else ""
            try:
                args = json.loads(args_raw) if args_raw else {}
            except (json.JSONDecodeError, TypeError):
                args = {}
            tool_calls.append(
                ToolCall(
                    id=tc.id or "",
                    function_name=tc.function.name or "",
                    arguments=args,
                    arguments_raw=args_raw,
                )
            )

    # Extract usage
    usage = TokenUsage()
    if raw_response.usage:
        usage = TokenUsage(
            prompt_tokens=raw_response.usage.prompt_tokens or 0,
            completion_tokens=raw_response.usage.completion_tokens or 0,
            total_tokens=raw_response.usage.total_tokens or 0,
        )

    # Extract cost
    cost = 0.0
    try:
        cost = litellm.completion_cost(completion_response=raw_response)
    except Exception:
        pass

    # Extract stop reason
    stop_reason = ""
    if choice:
        stop_reason = choice.finish_reason or ""

    return LLMResponse(
        text=text,
        tool_calls=tool_calls,
        usage=usage,
        cost=cost,
        model=model,
        stop_reason=stop_reason,
        raw=raw_response,
    )


def _emit_llm_span(
    model: str,
    messages: list[dict],
    response: LLMResponse,
    duration_ms: float,
    tracer_name: str = "plato.llm",
) -> None:
    """Emit an ATIF-formatted span for an LLM call."""
    tracer = get_tracer(tracer_name)
    step_id = _next_step_id()

    # Build message summary for the span
    last_user_msg = ""
    for msg in reversed(messages):
        if msg.get("role") == "user":
            content = msg.get("content", "")
            if isinstance(content, str):
                last_user_msg = content[:500]
            elif isinstance(content, list):
                parts = []
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        parts.append(item.get("text", ""))
                last_user_msg = " ".join(parts)[:500]
            break

    # Build tool_calls list for ATIF
    atif_tool_calls = None
    if response.has_tool_calls:
        atif_tool_calls = [
            {
                "tool_call_id": tc.id,
                "function_name": tc.function_name,
                "arguments": tc.arguments,
            }
            for tc in response.tool_calls
        ]

    with tracer.start_as_current_span(f"atif.step.{step_id}") as span:
        span.set_attribute("atif.step.id", step_id)
        span.set_attribute("atif.step.source", "agent")
        span.set_attribute("atif.step.message", response.text[:2000] if response.text else last_user_msg)
        span.set_attribute("atif.step.model_name", model)

        if response.usage.prompt_tokens:
            span.set_attribute("atif.step.prompt_tokens", response.usage.prompt_tokens)
        if response.usage.completion_tokens:
            span.set_attribute("atif.step.completion_tokens", response.usage.completion_tokens)
        if response.cost:
            span.set_attribute("atif.step.cost_usd", response.cost)
        if atif_tool_calls:
            span.set_attribute("atif.step.tool_calls", json.dumps(atif_tool_calls, default=str))

        # Extra attributes for LLM-specific tracing
        span.set_attribute("llm.duration_ms", duration_ms)
        span.set_attribute("llm.stop_reason", response.stop_reason)
        span.set_attribute("llm.message_count", len(messages))


def completion(
    model: str,
    messages: list[dict],
    *,
    tools: list[dict] | None = None,
    max_tokens: int = 4096,
    temperature: float | None = None,
    system: str | None = None,
    tracer_name: str = "plato.llm",
    timeout: int = 120,
    num_retries: int = 2,
    **kwargs: Any,
) -> LLMResponse:
    """Synchronous LLM completion with ATIF tracing.

    Args:
        model: Model identifier (e.g., "anthropic/claude-haiku-4-5-20251001", "openai/gpt-4o")
        messages: Chat messages in OpenAI format
        tools: Tool definitions (accepts both Anthropic and OpenAI formats)
        max_tokens: Maximum output tokens
        temperature: Sampling temperature
        system: System prompt (prepended as a system message)
        tracer_name: OTel tracer name for spans
        timeout: Request timeout in seconds
        num_retries: Number of retries on failure
        **kwargs: Additional arguments passed to litellm.completion()

    Returns:
        LLMResponse with text, tool_calls, usage, cost
    """

    # Prepend system message if provided
    if system:
        messages = [{"role": "system", "content": system}] + messages

    # Convert tools to OpenAI format
    call_kwargs: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "timeout": timeout,
        "num_retries": num_retries,
        **kwargs,
    }
    if tools:
        call_kwargs["tools"] = _convert_tools_to_openai_format(tools)
    if temperature is not None:
        call_kwargs["temperature"] = temperature

    start = time.monotonic()
    raw_response = litellm.completion(**call_kwargs)
    duration_ms = (time.monotonic() - start) * 1000

    response = _parse_response(raw_response, model)

    _emit_llm_span(model, messages, response, duration_ms, tracer_name)

    logger.debug(
        "LLM call: model=%s, tokens=%d/%d, cost=$%.4f, duration=%.0fms",
        model,
        response.usage.prompt_tokens,
        response.usage.completion_tokens,
        response.cost,
        duration_ms,
    )

    return response


async def acompletion(
    model: str,
    messages: list[dict],
    *,
    tools: list[dict] | None = None,
    max_tokens: int = 4096,
    temperature: float | None = None,
    system: str | None = None,
    tracer_name: str = "plato.llm",
    timeout: int = 120,
    num_retries: int = 2,
    **kwargs: Any,
) -> LLMResponse:
    """Async LLM completion with ATIF tracing.

    Same interface as completion() but async.
    """

    # Prepend system message if provided
    if system:
        messages = [{"role": "system", "content": system}] + messages

    call_kwargs: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "timeout": timeout,
        "num_retries": num_retries,
        **kwargs,
    }
    if tools:
        call_kwargs["tools"] = _convert_tools_to_openai_format(tools)
    if temperature is not None:
        call_kwargs["temperature"] = temperature

    start = time.monotonic()
    raw_response = await litellm.acompletion(**call_kwargs)
    duration_ms = (time.monotonic() - start) * 1000

    response = _parse_response(raw_response, model)

    _emit_llm_span(model, messages, response, duration_ms, tracer_name)

    logger.debug(
        "LLM call: model=%s, tokens=%d/%d, cost=$%.4f, duration=%.0fms",
        model,
        response.usage.prompt_tokens,
        response.usage.completion_tokens,
        response.cost,
        duration_ms,
    )

    return response


def _parse_image_response(raw_response: Any, model: str) -> ImageResponse:
    """Parse a litellm ImageResponse into our ImageResponse."""
    data = []
    for item in getattr(raw_response, "data", []):
        data.append(
            ImageData(
                b64_json=getattr(item, "b64_json", "") or "",
                url=getattr(item, "url", "") or "",
                revised_prompt=getattr(item, "revised_prompt", "") or "",
            )
        )
    return ImageResponse(data=data, model=model, raw=raw_response)


def image_generation(
    prompt: str,
    model: str,
    *,
    n: int = 1,
    size: str = "1024x1024",
    response_format: str = "b64_json",
    timeout: int = 120,
    **kwargs: Any,
) -> ImageResponse:
    """Synchronous image generation via litellm."""
    start = time.monotonic()
    raw = litellm.image_generation(
        prompt=prompt,
        model=model,
        n=n,
        size=size,
        response_format=response_format,
        timeout=timeout,
        **kwargs,
    )
    duration_ms = (time.monotonic() - start) * 1000
    logger.info("Image generation: model=%s, duration=%.0fms", model, duration_ms)
    return _parse_image_response(raw, model)


async def aimage_generation(
    prompt: str,
    model: str,
    *,
    n: int = 1,
    size: str = "1024x1024",
    response_format: str = "b64_json",
    timeout: int = 120,
    **kwargs: Any,
) -> ImageResponse:
    """Async image generation via litellm."""
    start = time.monotonic()
    raw = await litellm.aimage_generation(
        prompt=prompt,
        model=model,
        n=n,
        size=size,
        response_format=response_format,
        timeout=timeout,
        **kwargs,
    )
    duration_ms = (time.monotonic() - start) * 1000
    logger.info("Image generation: model=%s, duration=%.0fms", model, duration_ms)
    return _parse_image_response(raw, model)
