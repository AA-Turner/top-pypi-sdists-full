from __future__ import annotations

import asyncio
import json
from typing import TYPE_CHECKING, Any

from matrx_connect.context.events import InfoPayload
from matrx_utils import vcprint
from together import AsyncTogether

from matrx_ai.config import (
    FinishReason,
    TextContent,
    ThinkingContent,
    TokenUsage,
    ToolCallContent,
    UnifiedConfig,
    UnifiedMessage,
    UnifiedResponse,
    serialize_provider_usage,
)
from matrx_ai.context.emitter_protocol import Emitter
from matrx_ai.providers.keys import keyed_provider_client
from matrx_ai.providers.outbound_capture import (
    make_capture_http_client,
    stamp_call_meta,
)
from matrx_ai.providers.reasoning import (
    emit_complete_reasoning_block,
    openai_compatible_reasoning_text,
)
from matrx_ai.providers.snapshot import capture_request_payload

from .translator import TogetherTranslator

if TYPE_CHECKING:  # circular-by-design: catalog.models imports providers.resolved_capabilities
    from matrx_ai.catalog.models import ResolvedCallProfile

DEBUG_OVERRIDE = False

class TogetherChat:
    """Together AI API-specific endpoint implementation (OpenAI-style)."""

    endpoint_name: str
    debug: bool

    # Memoized on the RESOLVED KEY VALUE — a host-side key rotation builds a
    # fresh SDK client on the next request (no process restart).
    client = keyed_provider_client(
        "TOGETHER_API_KEY",
        factory=lambda api_key: AsyncTogether(
            api_key=api_key,
            http_client=make_capture_http_client(),
        ),
    )

    def __init__(self, debug: bool = False):
        self.endpoint_name = "[TOGETHER CHAT]"
        self.translator = TogetherTranslator(debug=debug)
        self.debug = debug

        if DEBUG_OVERRIDE:
            self.debug = True

    def to_provider_config(
        self, config: UnifiedConfig, profile: ResolvedCallProfile
    ) -> dict[str, Any]:
        return self.translator.build_request(config, profile)

    def to_unified_response(self, response: Any, model: str = "") -> UnifiedResponse:
        """Convert Together response to unified format"""
        return self.translator.from_together(response)

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
            provider="together",
            wire_format=profile.wire_format,
            debug=debug,
        )
        stamp_call_meta(
            provider="together",
            model=unified_config.model,
            is_streaming=bool(config_data.get("stream", False)),
        )

        vcprint(config_data, "Together API Config Data", color="blue", verbose=debug)

        try:
            # Translator sets stream correctly
            if config_data.get("stream", False):
                return await self._execute_streaming(
                    config_data, emitter, unified_config.model
                )
            else:
                return await self._execute_non_streaming(
                    config_data, emitter, unified_config.model
                )

        except Exception as e:
            # Import here to avoid circular dependency
            from matrx_ai.providers.errors import classify_provider_error

            error_info = classify_provider_error("together", e)
            e.error_info = error_info
            raise

    async def _execute_non_streaming(
        self,
        config_data: dict[str, Any],
        emitter: Emitter,
        model: str,
    ) -> UnifiedResponse:
        """Execute non-streaming Together request"""

        vcprint("[Together] Starting API call (non-streaming)...", color="cyan")

        # Native async API call
        response = await self.client.chat.completions.create(**config_data)

        vcprint("[Together] API call completed, processing response...", color="cyan")
        vcprint(response, "Together Response", color="green", verbose=self.debug)

        # Convert to unified format first
        vcprint("[Together] Converting to unified format...", color="cyan")
        converted_response = self.to_unified_response(response, model)
        vcprint(
            f"[Together] Conversion complete. {len(converted_response.messages)} messages",
            color="cyan",
        )

        # Send content through emitter
        vcprint("[Together] Sending content to stream handler...", color="cyan")
        for message in converted_response.messages:
            for content in message.content:
                if isinstance(content, ThinkingContent):
                    await emit_complete_reasoning_block(emitter, content.text)
                elif isinstance(content, TextContent):
                    await emitter.send_chunk(content.text)
                elif isinstance(content, ToolCallContent):
                    await emitter.send_info(InfoPayload(
                        code="tool_processing",
                        system_message=f"Executing {content.name}",
                        user_message=f"Using tool {content.name}",
                        metadata={"tool_call": content.name},
                    ))

        vcprint(
            "[Together] Non-streaming execution completed successfully", color="green"
        )
        return converted_response

    async def _execute_streaming(
        self,
        config_data: dict[str, Any],
        emitter: Emitter,
        model: str,
    ) -> UnifiedResponse:
        """Execute streaming Together request"""

        vcprint("[Together] Starting API call (streaming)...", color="cyan")

        # Native async streaming
        stream = await self.client.chat.completions.create(**config_data)

        vcprint(
            "[Together] Stream connection established, processing chunks...",
            color="cyan",
        )

        # Accumulate response data for final unified response
        accumulated_content = ""
        accumulated_reasoning = ""
        in_think_block = False
        accumulated_tool_calls = []
        usage_data = None
        finish_reason = None
        response_id = None

        # Process stream chunks
        from matrx_ai.providers.errors import stream_with_billed_usage

        async for chunk in stream_with_billed_usage(stream, model=model, api="together"):
            response_id = chunk.id

            # vcprint(chunk, "Together Stream Chunk", color="magenta")

            # Capture usage from final chunk (can come without choices)
            if chunk.usage:
                usage_data = chunk.usage

            # Only process choice-specific data if choices exist
            if not chunk.choices:
                continue

            choice = chunk.choices[0]
            delta = choice.delta

            reasoning_chunk = openai_compatible_reasoning_text(delta)
            if reasoning_chunk:
                accumulated_reasoning += reasoning_chunk
                if not in_think_block:
                    await emitter.send_reasoning_state("started")
                    await emitter.send_chunk("<reasoning>")
                    in_think_block = True
                await emitter.send_chunk(reasoning_chunk)
                await asyncio.sleep(0)

            # Handle content chunks
            if delta.content:
                # Close the reasoning block before the first real content token.
                if in_think_block:
                    await emitter.send_chunk("\n</reasoning>\n")
                    await emitter.send_reasoning_state("stopped")
                    in_think_block = False
                accumulated_content += delta.content
                await emitter.send_chunk(delta.content)
                await asyncio.sleep(0)

            # Handle tool calls - Together API doesn't always include this field
            # Together can return tool_calls as dicts or objects
            if hasattr(delta, "tool_calls") and delta.tool_calls:
                if self.debug:
                    vcprint(delta, "Together Tool Calls", color="magenta")
                for tc in delta.tool_calls:
                    # Handle both dict and object formats
                    tc_index_raw = (
                        tc.get("index")
                        if isinstance(tc, dict)
                        else getattr(tc, "index", None)
                    )
                    tc_index = int(tc_index_raw) if tc_index_raw is not None else None
                    tc_id = (
                        tc.get("id")
                        if isinstance(tc, dict)
                        else getattr(tc, "id", None)
                    )
                    tc_func = (
                        tc.get("function")
                        if isinstance(tc, dict)
                        else getattr(tc, "function", None)
                    )

                    if tc_index is None:
                        continue

                    while len(accumulated_tool_calls) <= tc_index:
                        accumulated_tool_calls.append(
                            {"id": "", "name": "", "arguments": ""}
                        )

                    if tc_id:
                        accumulated_tool_calls[tc_index]["id"] = tc_id

                    if tc_func:
                        # Function can also be dict or object
                        func_name = (
                            tc_func.get("name")
                            if isinstance(tc_func, dict)
                            else getattr(tc_func, "name", None)
                        )
                        func_args = (
                            tc_func.get("arguments")
                            if isinstance(tc_func, dict)
                            else getattr(tc_func, "arguments", None)
                        )

                        if func_name:
                            accumulated_tool_calls[tc_index]["name"] = func_name
                        if func_args:
                            # Arguments might be a dict or string
                            if isinstance(func_args, dict):
                                accumulated_tool_calls[tc_index]["arguments"] = (
                                    json.dumps(func_args)
                                )
                            else:
                                accumulated_tool_calls[tc_index]["arguments"] += (
                                    func_args
                                )

            # Capture finish reason
            if choice.finish_reason:
                finish_reason = choice.finish_reason

        # Close an unclosed reasoning block (e.g. hit max_tokens mid-reasoning).
        if in_think_block:
            await emitter.send_chunk("\n</reasoning>")
            await emitter.send_reasoning_state("stopped")

        # Build unified response from accumulated data
        content = []

        if accumulated_reasoning:
            content.append(ThinkingContent(text=accumulated_reasoning, provider="together"))
        if accumulated_content:
            content.append(TextContent(text=accumulated_content))

        for tc_data in accumulated_tool_calls:
            if tc_data["name"]:
                arguments = (
                    json.loads(tc_data["arguments"]) if tc_data["arguments"] else {}
                )
                content.append(
                    ToolCallContent(
                        id=tc_data["id"], name=tc_data["name"], arguments=arguments
                    )
                )

        messages = []
        if content:
            messages.append(
                UnifiedMessage(role="assistant", content=content)
            )

        # Convert usage to TokenUsage
        token_usage = None
        if usage_data:
            token_usage = TokenUsage(
                input_tokens=usage_data.prompt_tokens,
                output_tokens=usage_data.completion_tokens,
                matrx_model_name=model,
                provider_model_name=model,
                api="together",
                response_id=response_id or "",
                raw_usage=serialize_provider_usage(usage_data),
            )

        # Map finish_reason to unified format
        unified_finish_reason = None
        if finish_reason == "stop":
            unified_finish_reason = FinishReason.STOP
        elif finish_reason == "length":
            unified_finish_reason = FinishReason.MAX_TOKENS
        elif finish_reason == "tool_calls":
            unified_finish_reason = FinishReason.TOOL_CALLS
        elif finish_reason == "content_filter":
            unified_finish_reason = FinishReason.CONTENT_FILTER

        vcprint("[Together] Streaming execution completed successfully", color="green")

        return UnifiedResponse(
            messages=messages,
            usage=token_usage,
            finish_reason=unified_finish_reason,
            stop_reason=finish_reason,
        )
