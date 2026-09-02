from __future__ import annotations

import json
from typing import Any

from matrx_utils import vcprint

from matrx_ai.config import (
    FinishReason,
    TextContent,
    ThinkingContent,
    TokenUsage,
    ToolCallContent,
    ToolResultContent,
    UnifiedConfig,
    UnifiedMessage,
    UnifiedResponse,
    YouTubeVideoContent,
    serialize_provider_usage,
)
from matrx_ai.config.media_config import ImageContent
from matrx_ai.providers.base_translator import BaseTranslator
from matrx_ai.providers.outbound_params import resolve_outbound_params

# ============================================================================
# CEREBRAS TRANSLATOR
# ============================================================================

class CerebrasTranslator(BaseTranslator):
    """Translates between unified format and Cerebras API (OpenAI-style)"""

    def __init__(self, debug: bool = False):
        super().__init__(debug=debug)

    def _assemble_request(self, config: UnifiedConfig, route_ctx: Any = ""):
        return self.to_cerebras(config, self.require_profile(route_ctx))

    def to_cerebras(self, config: UnifiedConfig, profile: Any) -> dict[str, Any]:
        """
        Convert unified config to Cerebras API format.

        Cerebras uses OpenAI-style messages but with some differences:
        - Uses max_completion_tokens instead of max_output_tokens
        - Tools only work in non-streaming mode
        Param shaping (temperature / top_p / max_completion_tokens / stop /
        seed / reasoning_effort / clear_thinking) is DB-driven via
        profile.controls — the gpt-oss intensity vs GLM on/off reasoning
        contracts are offering overrides, not api_class branches.
        """
        messages = []

        # Add system message if present
        system_text = self.get_system_text(config)
        if system_text:
            messages.append({"role": "system", "content": system_text})

        # Convert messages to OpenAI-style format
        for msg in config.messages:
            # Cerebras uses OpenAI-style messages with role and content
            if msg.role == "tool":
                # Tool results go as role="tool". Image-bearing tool results
                # surface their images as a follow-up user message because
                # Chat Completions role=tool only accepts a string content.
                pending_image_parts: list[dict[str, Any]] = []
                for content in msg.content:
                    if isinstance(content, ToolResultContent):
                        messages.append(content.to_openai_chat())
                        for image_block in content.extract_image_blocks():
                            image_part = image_block.to_openai_chat()
                            if image_part is not None:
                                pending_image_parts.append(image_part)
                if pending_image_parts:
                    messages.append({"role": "user", "content": pending_image_parts})
            else:
                # Regular messages
                message_dict: dict[str, Any] = {"role": msg.role}

                text_parts: list[str] = []
                image_parts: list[dict[str, Any]] = []
                tool_calls: list[dict[str, Any]] = []

                for content in msg.content:
                    if isinstance(content, TextContent):
                        text_parts.append(content.text)
                    elif isinstance(content, ImageContent):
                        image_part = content.to_openai_chat()
                        if image_part is not None:
                            image_parts.append(image_part)
                    elif isinstance(content, ToolCallContent):
                        tool_calls.append(
                            {
                                "id": content.id,
                                "type": "function",
                                "function": {
                                    "name": content.wire_name,
                                    "arguments": json.dumps(content.arguments),
                                },
                            }
                        )
                    elif isinstance(content, YouTubeVideoContent):
                        # YouTube URLs not supported by Cerebras - show warning
                        vcprint(
                            f"YouTube URL '{content.youtube_url}' is not supported by Cerebras models and will be skipped.",
                            "YouTube URL Warning",
                            color="yellow",
                        )

                if image_parts:
                    combined_text = "".join(text_parts)
                    parts: list[dict[str, Any]] = []
                    if combined_text:
                        parts.append({"type": "text", "text": combined_text})
                    parts.extend(image_parts)
                    message_dict["content"] = parts
                elif text_parts:
                    message_dict["content"] = "".join(text_parts)
                elif tool_calls:
                    # Tool-call-only assistant turn: OpenAI-compatible chat
                    # templates (Llama/Qwen/gpt-oss on Cerebras) expect
                    # content=null here, NOT "". An empty string makes the
                    # prior tool-call turn render ambiguously on replay, so the
                    # model fails to see that it already called the tool and
                    # re-issues the same call — an endless, all-succeeding tool
                    # loop the failure-based loop guard never trips. Matches the
                    # groq/xai/together/generic_openai translators.
                    message_dict["content"] = None
                else:
                    message_dict["content"] = ""

                if tool_calls:
                    message_dict["tool_calls"] = tool_calls

                if message_dict["content"] or tool_calls:
                    messages.append(message_dict)

        # Build request
        cerebras_request = {
            "model": config.model,
            "messages": messages,
        }

        # DB-resolved params (temperature / top_p / max_completion_tokens /
        # stop / seed / reasoning_effort / clear_thinking ...).
        cerebras_request.update(resolve_outbound_params(config, profile.controls))

        # Response format — Cerebras (OpenAI-style) validates a specific nested
        # shape; passing the unified config through verbatim 400s. Convert here.
        if config.response_format:
            cerebras_response_format = self.build_openai_chat_response_format(
                config.response_format, "cerebras"
            )
            if cerebras_response_format is not None:
                cerebras_request["response_format"] = cerebras_response_format

        # Tools - Cerebras doesn't support streaming with tools
        # If tools are present, we disable streaming at API level (system stays responsive)
        all_tools = self.build_provider_tools(config, "cerebras")
        if all_tools:
            cerebras_request["tools"] = all_tools
            if config.tool_choice:
                cerebras_request["tool_choice"] = config.tool_choice
            # parallel_tool_calls defaults to True; only emit when explicitly
            # disabled (matches the OpenAI translator). The native Cerebras SDK
            # accepts this kwarg; GLM 4.7 / gpt-oss support parallel tool calls.
            if not config.parallel_tool_calls:
                cerebras_request["parallel_tool_calls"] = False

        # Stream setting - disable if tools are present
        if config.stream and not all_tools:
            cerebras_request["stream"] = True

        vcprint(
            cerebras_request, "--> Cerebras Request", color="magenta", verbose=False
        )

        return cerebras_request

    def from_cerebras(self, response: Any) -> UnifiedResponse:
        """
        Convert Cerebras API response to unified format.

        Cerebras returns OpenAI-style responses:
        - response.id, response.created, response.model always present
        - response.choices is always a list with one item
        - choice.message has: content, reasoning, role, tool_calls (can be null)

        No citation capture: the Cerebras SDK message carries nothing
        citation-like (role/content/reasoning/tool_calls only — verified
        against cerebras.cloud.sdk 2026-08-08).
        - response.usage has: prompt_tokens, completion_tokens, prompt_tokens_details
        """
        messages = []

        if not response.choices:
            vcprint(response, "Cerebras Response", color="red")
            return UnifiedResponse(messages=[], finish_reason=FinishReason.ERROR)

        choice = response.choices[0]
        message = choice.message
        content = []

        # Extract reasoning first (if present)
        if message.reasoning:
            content.append(ThinkingContent(text=message.reasoning, provider="cerebras"))

        # Extract text content
        if message.content:
            content.append(TextContent(text=message.content))

        # Extract tool calls
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments from JSON string if needed
                arguments = (
                    json.loads(tc.function.arguments)
                    if isinstance(tc.function.arguments, str)
                    else tc.function.arguments
                )
                content.append(
                    ToolCallContent(
                        id=tc.id, name=tc.function.name, arguments=arguments
                    )
                )

        # Create unified message
        if content:
            messages.append(
                UnifiedMessage(role="assistant", content=content)
            )

        # Convert usage to TokenUsage with cached tokens
        token_usage = None
        if response.usage:
            # Cerebras provides cached_tokens in prompt_tokens_details
            cached_tokens = 0
            if (
                response.usage.prompt_tokens_details
                and response.usage.prompt_tokens_details.cached_tokens
            ):
                cached_tokens = response.usage.prompt_tokens_details.cached_tokens

            token_usage = TokenUsage(
                input_tokens=response.usage.prompt_tokens - cached_tokens,
                output_tokens=response.usage.completion_tokens,
                cached_input_tokens=cached_tokens,
                matrx_model_name=response.model,
                provider_model_name=response.model,
                api="cerebras",
                response_id=response.id,
                raw_usage=serialize_provider_usage(response.usage),
            )
        else:
            vcprint(
                f"⚠️  WARNING: Cerebras response missing usage data for model {response.model} (response_id: {response.id})",
                color="red",
            )

        # Map finish_reason to unified format
        finish_reason = None
        if choice.finish_reason == "stop":
            finish_reason = FinishReason.STOP
        elif choice.finish_reason == "length":
            finish_reason = FinishReason.MAX_TOKENS
        elif choice.finish_reason == "tool_calls":
            finish_reason = FinishReason.TOOL_CALLS
        elif choice.finish_reason == "content_filter":
            finish_reason = FinishReason.CONTENT_FILTER

        return UnifiedResponse(
            messages=messages,
            usage=token_usage,
            finish_reason=finish_reason,
            stop_reason=choice.finish_reason,
            raw_response=response,
        )
