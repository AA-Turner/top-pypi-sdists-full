from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any

from cerebras.cloud.sdk import AsyncCerebras
from matrx_connect.context.events import InfoPayload
from matrx_utils import vcprint

from matrx_ai.config import (
    TextContent,
    ThinkingContent,
    ToolCallContent,
    UnifiedConfig,
    UnifiedResponse,
)
from matrx_ai.context.emitter_protocol import Emitter
from matrx_ai.providers.keys import keyed_provider_client
from matrx_ai.providers.outbound_capture import (
    make_capture_http_client,
    stamp_call_meta,
)
from matrx_ai.providers.snapshot import capture_request_payload

from .translator import CerebrasTranslator

if TYPE_CHECKING:  # circular-by-design: catalog.models imports providers.resolved_capabilities
    from matrx_ai.catalog.models import ResolvedCallProfile

DEBUG_OVERRIDE = False


class CerebrasChat:
    """Cerebras API-specific endpoint implementation (OpenAI-style)."""

    endpoint_name: str
    debug: bool

    # Memoized on the RESOLVED KEY VALUE — a host-side key rotation builds a
    # fresh SDK client on the next request (no process restart). The warmup
    # rationale in __init__ still holds: warm() probes THIS async client.
    client = keyed_provider_client(
        "CEREBRAS_API_KEY",
        factory=lambda api_key: AsyncCerebras(
            api_key=api_key,
            http_client=make_capture_http_client(),
            warm_tcp_connection=False,
        ),
    )

    def __init__(self, debug: bool = False):
        # warm_tcp_connection=False is REQUIRED here. With the SDK default
        # (True), AsyncCerebras.__init__ constructs a *synchronous* Cerebras
        # client whose own constructor issues a blocking GET /v1/tcp_warming
        # (cerebras_cloud_sdk _client.py:320). On an async event loop that
        # blocking HTTP call freezes the ENTIRE process for ~2s (caught by the
        # loop watchdog).
        #
        # We do NOT lose the warmup — we just do it the right way. Cerebras'
        # guidance for a long-lived (non-serverless) process is: construct the
        # client ONCE, reuse it, and keep its connection warm for low TTFT. We
        # satisfy all three: the client is cached process-wide (UnifiedAIClient
        # provider cache), and we re-issue the SAME /v1/tcp_warming probe
        # ASYNCHRONOUSLY via ``warm()`` against this async client — which warms
        # the live connection pool that actually serves requests (strictly
        # better than the SDK's sync warmup that warms then immediately closes a
        # throwaway sync connection), with zero loop blocking.
        self.endpoint_name = "[CEREBRAS CHAT]"
        self.translator = CerebrasTranslator(debug=debug)
        self.debug = debug
        self._warm_task: asyncio.Task | None = None

        if DEBUG_OVERRIDE:
            self.debug = True

        # Kick off the async warmup immediately if a loop is running (it is,
        # whenever this client is built lazily inside a request). No loop (import
        # time / sync construction) → skipped; warm() can be called at startup.
        try:
            loop = asyncio.get_running_loop()
            self._warm_task = loop.create_task(self.warm())
        except RuntimeError:
            pass

    async def warm(self) -> None:
        """Pre-establish the TCP/TLS connection to Cerebras for low TTFT.

        Async equivalent of the SDK's built-in ``/v1/tcp_warming`` probe (which
        the SDK runs synchronously in its constructor and which we disable via
        ``warm_tcp_connection=False`` so it never freezes the event loop).
        Running it on the live async client warms the connection pool that
        actually serves requests. Best-effort — never raises. Idempotent and
        cheap to call again (e.g. from an app-startup pre-warm hook so even the
        first real request is hot)."""
        try:
            from cerebras.cloud.sdk._base_client import make_request_options

            await self.client.get(
                "/v1/tcp_warming",
                cast_to=str,
                options=make_request_options(timeout=1),
            )
        except Exception as e:
            vcprint(
                f"{self.endpoint_name} tcp warmup skipped: {e}",
                color="yellow",
                verbose=DEBUG_OVERRIDE,
            )

    def to_provider_config(
        self, config: UnifiedConfig, profile: ResolvedCallProfile
    ) -> dict[str, Any]:
        return self.translator.build_request(config, profile)

    def to_unified_response(self, response: Any, model: str = "") -> UnifiedResponse:
        """Convert Cerebras response to unified format"""
        return self.translator.from_cerebras(response)

    async def execute(
        self,
        unified_config: UnifiedConfig,
        profile: ResolvedCallProfile,
        debug: bool = False,
    ) -> UnifiedResponse:
        from matrx_ai.context.app_context import get_app_context

        emitter = get_app_context().emitter
        self.debug = debug
        if DEBUG_OVERRIDE:
            self.debug = True
        self.translator.debug = debug

        # Build provider-specific config
        config_data = self.to_provider_config(unified_config, profile)
        capture_request_payload(
            config_data,
            provider="cerebras",
            wire_format=profile.wire_format,
            debug=debug,
        )
        stamp_call_meta(
            provider="cerebras",
            model=unified_config.model,
            is_streaming=bool(config_data.get("stream", False)),
        )

        vcprint(config_data, "Cerebras API Config Data", color="blue", verbose=debug)

        try:
            # Translator has already set stream correctly based on tools
            if config_data.get("stream", False):
                return await self._execute_streaming(config_data, emitter, unified_config.model)
            else:
                return await self._execute_non_streaming(config_data, emitter, unified_config.model)

        except Exception as e:
            # Import here to avoid circular dependency
            from matrx_ai.providers.errors import classify_provider_error

            error_info = classify_provider_error("cerebras", e)
            e.error_info = error_info
            raise

    async def _execute_non_streaming(
        self,
        config_data: dict[str, Any],
        emitter: Emitter,
        model: str,
    ) -> UnifiedResponse:
        """Execute non-streaming Cerebras request"""

        vcprint("[Cerebras] Starting API call (non-streaming)...", color="cyan")

        # Native async API call - no executor needed!
        response = await self.client.chat.completions.create(**config_data)

        vcprint("[Cerebras] API call completed, processing response...", color="cyan")
        vcprint(response, "Cerebras Response", color="green", verbose=self.debug)

        # Convert to unified format first
        vcprint("[Cerebras] Converting to unified format...", color="cyan")
        converted_response = self.to_unified_response(response, model)
        vcprint(
            f"[Cerebras] Conversion complete. {len(converted_response.messages)} messages",
            color="cyan",
        )

        # Send content through emitter
        vcprint("[Cerebras] Sending content to stream handler...", color="cyan")
        for message in converted_response.messages:
            for content in message.content:
                if isinstance(content, ThinkingContent):
                    # Wrap reasoning in XML tags
                    await emitter.send_chunk(f"\n<reasoning>\n{content.text}\n</reasoning>\n")
                elif isinstance(content, TextContent):
                    await emitter.send_chunk(content.text)
                elif isinstance(content, ToolCallContent):
                    await emitter.send_info(
                        InfoPayload(
                            code="tool_processing",
                            system_message=f"Executing {content.name}",
                            user_message=f"Using tool {content.name}",
                            metadata={"tool_call": content.name},
                        )
                    )

        vcprint("[Cerebras] Non-streaming execution completed successfully", color="green")
        return converted_response

    async def _execute_streaming(
        self,
        config_data: dict[str, Any],
        emitter: Emitter,
        model: str,
    ) -> UnifiedResponse:
        """Execute streaming Cerebras request"""

        vcprint("[Cerebras] Starting API call (streaming)...", color="cyan")

        # Native async streaming - stream=True already in config_data from translator
        stream = await self.client.chat.completions.create(**config_data)

        vcprint(
            "[Cerebras] Stream connection established, processing chunks...",
            color="cyan",
        )

        # Accumulate response data to reconstruct full response object
        accumulated_content = ""
        accumulated_reasoning = ""
        accumulated_tool_calls = []
        usage_data = None
        finish_reason = None
        response_id = None
        response_created = None
        response_model = None

        first_reasoning_chunk = True

        # Process stream chunks
        # Chunk structure is 100% predictable:
        # - chunk.id, chunk.created, chunk.model always present
        # - chunk.choices is always a list with one item (index 0)
        # - choice.delta has: content, reasoning, role, tokens, tool_calls (all can be null)
        # - choice.finish_reason is null except final chunk
        # - chunk.usage is null except final chunk
        from matrx_ai.providers.errors import stream_with_billed_usage

        async for chunk in stream_with_billed_usage(stream, model=model, api="cerebras"):
            response_id = chunk.id  # Always present
            response_created = chunk.created  # Always present
            response_model = chunk.model  # Always present

            # Choices is always a list with one item
            choice = chunk.choices[0]
            delta = choice.delta

            # Handle reasoning chunks (delta.reasoning can be null or string)
            if delta.reasoning:
                accumulated_reasoning += delta.reasoning

                if first_reasoning_chunk:
                    await emitter.send_reasoning_state("started")
                    await emitter.send_chunk("\n<reasoning>\n")
                    first_reasoning_chunk = False

                await emitter.send_chunk(delta.reasoning)
                await asyncio.sleep(0)

            # Handle content chunks (delta.content can be null or string)
            if delta.content:
                # Close reasoning tag if we were in reasoning
                if accumulated_reasoning and not first_reasoning_chunk:
                    await emitter.send_chunk("\n</reasoning>\n")
                    await emitter.send_reasoning_state("stopped")
                    first_reasoning_chunk = True  # Reset for potential future reasoning

                accumulated_content += delta.content
                await emitter.send_chunk(delta.content)
                await asyncio.sleep(0)

            # Handle tool calls (delta.tool_calls can be null or list)
            if delta.tool_calls:
                for tc in delta.tool_calls:
                    # Accumulate tool call data
                    while len(accumulated_tool_calls) <= tc.index:
                        accumulated_tool_calls.append({"id": "", "name": "", "arguments": ""})

                    if tc.id:
                        accumulated_tool_calls[tc.index]["id"] = tc.id
                    if tc.function.name:
                        accumulated_tool_calls[tc.index]["name"] = tc.function.name
                    if tc.function.arguments:
                        accumulated_tool_calls[tc.index]["arguments"] += tc.function.arguments

            # Capture finish reason (only in final chunk)
            if choice.finish_reason:
                finish_reason = choice.finish_reason

            # Capture usage from final chunk
            if chunk.usage:
                usage_data = chunk.usage

        # Close reasoning tag if still open
        if accumulated_reasoning and not first_reasoning_chunk:
            await emitter.send_chunk("\n</reasoning>\n")
            await emitter.send_reasoning_state("stopped")

        # Reconstruct a ChatCompletion-like response object to pass through translator
        # This ensures consistency with non-streaming path and keeps conversion logic in one place
        from types import SimpleNamespace

        # Build tool_calls list if we have any
        tool_calls_list = []
        for tc_data in accumulated_tool_calls:
            if tc_data["name"]:  # Only add if we have a name
                tool_calls_list.append(
                    SimpleNamespace(
                        id=tc_data["id"],
                        type="function",
                        function=SimpleNamespace(
                            name=tc_data["name"], arguments=tc_data["arguments"]
                        ),
                    )
                )

        # Create message object matching Cerebras response structure
        message = SimpleNamespace(
            role="assistant",
            content=accumulated_content or None,
            reasoning=accumulated_reasoning or None,
            tool_calls=tool_calls_list if tool_calls_list else None,
        )

        # Create choice object
        choice = SimpleNamespace(index=0, message=message, finish_reason=finish_reason)

        # Create full response object matching ChatCompletion structure
        mock_response = SimpleNamespace(
            id=response_id,
            created=response_created,
            model=response_model,
            choices=[choice],
            usage=usage_data,
        )

        vcprint(
            "[Cerebras] Stream accumulated, converting through translator...",
            color="cyan",
        )

        # Convert through translator (same path as non-streaming)
        converted_response = self.to_unified_response(mock_response, model)

        vcprint("[Cerebras] Streaming execution completed successfully", color="green")

        return converted_response
