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
from matrx_ai.providers.reasoning import openai_compatible_reasoning_text

# ============================================================================
# TOGETHER TRANSLATOR
# ============================================================================


class TogetherTranslator(BaseTranslator):
    """Translates between unified format and Together AI API (OpenAI-style)"""

    def __init__(self, debug: bool = False):
        super().__init__(debug=debug)

    def _assemble_request(self, config: UnifiedConfig, route_ctx: Any = ""):
        return self.to_together(config, self.require_profile(route_ctx))

    def to_together(self, config: UnifiedConfig, profile: Any) -> dict[str, Any]:
        """
        Convert unified config to Together API format.

        Together uses OpenAI-style messages with full streaming + tools support.
        Param shaping (temperature / top_p / max_tokens / stop /
        reasoning_effort|reasoning.enabled) is DB-driven via profile.controls —
        the together_reasoning processor always sends an explicit effort (OUR
        default "high"; omitting the field makes the PROVIDER default to "max").
        """
        messages = []

        # Add system message if present
        system_text = self.get_system_text(config)
        if system_text:
            messages.append({"role": "system", "content": system_text})

        # Convert messages to OpenAI-style format
        for msg in config.messages:
            if msg.role == "tool":
                # Image-bearing tool results surface their images as a
                # follow-up user message (Chat Completions role=tool only
                # accepts a string content).
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
                        # YouTube URLs not supported by Together - show warning
                        vcprint(
                            f"YouTube URL '{content.youtube_url}' is not supported by Together models and will be skipped.",
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
                    message_dict["content"] = None
                else:
                    message_dict["content"] = ""

                if tool_calls:
                    message_dict["tool_calls"] = tool_calls

                if text_parts or tool_calls or image_parts or message_dict["content"] == "":
                    messages.append(message_dict)

        # clear_thinking is a Cerebras-only concept — not forwarded to Together.
        # Reasoning: Together/Z.AI thinking models stream on delta.reasoning_content
        # (together_api.py). Omitting reasoning_effort makes the PROVIDER default
        # to "max" — we never do that. ThinkingConfig.to_together_reasoning_params
        # always sends an explicit effort (OUR default = "high").

        # Build request
        together_request = {
            "model": config.model,
            "messages": messages,
        }

        # DB-resolved params (temperature / top_p / max_tokens / stop /
        # reasoning_effort|reasoning.enabled — the processor always sends an
        # explicit reasoning value so the provider "max" default never applies).
        together_request.update(resolve_outbound_params(config, profile.controls))
        # Response format — Together (OpenAI-style) validates a specific nested
        # shape; passing the unified config through verbatim 400s. Convert here.
        if config.response_format:
            together_response_format = self.build_openai_chat_response_format(
                config.response_format, "together"
            )
            if together_response_format is not None:
                together_request["response_format"] = together_response_format
        if config.stream:
            together_request["stream"] = True
            # Together's OpenAI-compatible endpoint omits usage from streaming
            # chunks unless explicitly requested.  The v2 SDK does not expose
            # stream_options as a typed argument, so pass it through its
            # documented escape hatch rather than sacrificing token streaming.
            together_request["extra_body"] = {
                "stream_options": {"include_usage": True}
            }

        # Tools - Together supports streaming with tools
        all_tools = self.build_provider_tools(config, "together")
        if all_tools:
            together_request["tools"] = all_tools
            if config.tool_choice:
                together_request["tool_choice"] = config.tool_choice

        vcprint(together_request, "--> Together Request", color="magenta", verbose=False)
        return together_request

    def from_together(self, response: Any) -> UnifiedResponse:
        """Convert Together API response to unified format.

        No citation capture: the Together SDK ChoiceMessage carries nothing
        citation-like (content/role/function_call/reasoning/tool_calls only —
        verified against the together SDK 2026-08-08).
        """
        messages = []

        if not response.choices:
            return UnifiedResponse(messages=[], finish_reason=FinishReason.ERROR)

        choice = response.choices[0]
        message = choice.message
        content = []

        reasoning = openai_compatible_reasoning_text(message)
        if reasoning:
            content.append(ThinkingContent(text=reasoning, provider="together"))

        # Extract text content
        if message.content:
            content.append(TextContent(text=message.content))

        # Extract tool calls
        if message.tool_calls:
            for tc in message.tool_calls:
                arguments = (
                    json.loads(tc.function.arguments)
                    if isinstance(tc.function.arguments, str)
                    else tc.function.arguments
                )
                content.append(
                    ToolCallContent(id=tc.id, name=tc.function.name, arguments=arguments)
                )

        if content:
            messages.append(UnifiedMessage(role="assistant", content=content))

        # Convert usage to TokenUsage
        token_usage = None
        if response.usage:
            token_usage = TokenUsage(
                input_tokens=response.usage.prompt_tokens,
                output_tokens=response.usage.completion_tokens,
                matrx_model_name=response.model,
                provider_model_name=response.model,
                api="together",
                response_id=response.id,
                raw_usage=serialize_provider_usage(response.usage),
            )
        else:
            vcprint(
                f"⚠️  WARNING: Together response missing usage data for model {response.model} (response_id: {response.id})",
                color="red",
            )

        # Map finish_reason
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
