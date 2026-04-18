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

import asyncio
import json
import logging
import time
from typing import TYPE_CHECKING, Any, Literal

import litellm
from pydantic import BaseModel, Field

from plato.otel import get_tracer, record_step_cost

litellm.suppress_debug_info = True  # type: ignore[assignment]
logging.getLogger("LiteLLM").setLevel(logging.WARNING)

# Global per-model concurrency semaphores keyed by (model, api_base)
_model_semaphores: dict[tuple[str, str], asyncio.Semaphore] = {}
_model_semaphore_lock = asyncio.Lock()


async def _get_model_semaphore(model: str, api_base: str, limit: int) -> asyncio.Semaphore:
    """Get or create a semaphore for a (model, api_base) pair."""
    key = (model, api_base)
    if key not in _model_semaphores:
        async with _model_semaphore_lock:
            if key not in _model_semaphores:
                _model_semaphores[key] = asyncio.Semaphore(limit)
                logger.info("Created concurrency semaphore: model=%s api_base=%s limit=%d", model, api_base, limit)
    return _model_semaphores[key]


def set_concurrency(model: str, limit: int, api_base: str = "") -> None:
    """Set concurrency limit for a model. Call before any acompletion calls."""
    key = (model, api_base)
    _model_semaphores[key] = asyncio.Semaphore(limit)
    logger.info("Set concurrency: model=%s api_base=%s limit=%d", model, api_base, limit)


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

    def __init__(
        self,
        config: LLMConfig,
        store: ResultStore | None = None,
        *,
        tracer_name: str = "plato.llm",
        atif_source: Literal["agent", "world"] = "agent",
    ) -> None:
        self._model = config.model
        self._api_key = config.api_key or None
        self._max_tokens = config.max_tokens
        self._temperature = config.temperature
        self._store = store
        self._tracer_name = tracer_name
        self._atif_source = atif_source

        # Register concurrency limit if configured
        if config.concurrency > 0:
            set_concurrency(config.model, config.concurrency)

    async def __call__(
        self,
        messages: list[dict],
        *,
        system: str | None = None,
        tools: list[dict] | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
        timeout: int = 120,
        num_retries: int = 5,
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
            tracer_name=self._tracer_name,
            atif_source=self._atif_source,
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
        num_retries: int = 5,
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
            tracer_name=self._tracer_name,
            atif_source=self._atif_source,
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
    reasoning_tokens: int = 0
    prompt_tokens_details: dict[str, Any] = Field(default_factory=dict)
    completion_tokens_details: dict[str, Any] = Field(default_factory=dict)


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

    def _dump_usage_details(value: Any) -> dict[str, Any]:
        if value is None:
            return {}
        if isinstance(value, dict):
            return {k: v for k, v in value.items() if v is not None}
        if hasattr(value, "model_dump"):
            dumped = value.model_dump(exclude_none=True)
            if isinstance(dumped, dict):
                return {k: v for k, v in dumped.items() if v is not None}
        return {}

    def _extract_text(content: Any) -> str:
        if content is None:
            return ""
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts: list[str] = []
            for item in content:
                if isinstance(item, str):
                    parts.append(item)
                    continue
                if not isinstance(item, dict):
                    continue
                text = item.get("text")
                if isinstance(text, str):
                    parts.append(text)
            return "".join(parts)
        return str(content)

    # Extract text
    text = ""
    choice = raw_response.choices[0] if raw_response.choices else None
    if choice and choice.message:
        text = _extract_text(choice.message.content)

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
            reasoning_tokens=getattr(raw_response.usage, "reasoning_tokens", 0) or 0,
            prompt_tokens_details=_dump_usage_details(getattr(raw_response.usage, "prompt_tokens_details", None)),
            completion_tokens_details=_dump_usage_details(
                getattr(raw_response.usage, "completion_tokens_details", None)
            ),
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
    atif_source: Literal["agent", "world"] = "agent",
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
        span.set_attribute("atif.kind", "llm")
        span.set_attribute("atif.step.id", step_id)
        span.set_attribute("atif.step.source", atif_source)
        span.set_attribute("atif.step.message", response.text if response.text else last_user_msg)
        span.set_attribute("atif.step.model_name", model)

        if response.usage.prompt_tokens:
            span.set_attribute("atif.step.prompt_tokens", response.usage.prompt_tokens)
        if response.usage.completion_tokens:
            span.set_attribute("atif.step.completion_tokens", response.usage.completion_tokens)
        if response.usage.reasoning_tokens:
            span.set_attribute("atif.step.reasoning_tokens", response.usage.reasoning_tokens)
        if response.usage.prompt_tokens_details:
            span.set_attribute(
                "atif.step.prompt_tokens_details",
                json.dumps(response.usage.prompt_tokens_details, default=str),
            )
        if response.usage.completion_tokens_details:
            span.set_attribute(
                "atif.step.completion_tokens_details",
                json.dumps(response.usage.completion_tokens_details, default=str),
            )
        if response.cost:
            span.set_attribute("atif.step.cost_usd", response.cost)
        if atif_tool_calls:
            span.set_attribute("atif.step.tool_calls", json.dumps(atif_tool_calls, default=str))

        # Aggregate into the enclosing session_span() if any. No-op outside one.
        record_step_cost(
            cost_usd=response.cost or 0.0,
            prompt_tokens=response.usage.prompt_tokens or 0,
            completion_tokens=response.usage.completion_tokens or 0,
            reasoning_tokens=response.usage.reasoning_tokens or 0,
            model=model,
        )

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
    atif_source: Literal["agent", "world"] = "agent",
    timeout: int = 120,
    num_retries: int = 5,
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
        atif_source: ATIF source label for emitted spans
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

    _emit_llm_span(model, messages, response, duration_ms, tracer_name, atif_source)

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
    atif_source: Literal["agent", "world"] = "agent",
    timeout: int = 120,
    num_retries: int = 5,
    **kwargs: Any,
) -> LLMResponse:
    """Async LLM completion with ATIF tracing.

    Same interface as completion() but async.
    Respects per-model concurrency limits set via set_concurrency().
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

    # Acquire per-model semaphore if one exists
    api_base = kwargs.get("api_base", "")
    sem_key = (model, api_base)
    semaphore = _model_semaphores.get(sem_key)

    if semaphore:
        await semaphore.acquire()
    try:
        start = time.monotonic()
        raw_response = await litellm.acompletion(**call_kwargs)
        duration_ms = (time.monotonic() - start) * 1000
    finally:
        if semaphore:
            semaphore.release()

    response = _parse_response(raw_response, model)

    _emit_llm_span(model, messages, response, duration_ms, tracer_name, atif_source)

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
