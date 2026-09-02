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
# GROQ TRANSLATOR
# ============================================================================

class GroqTranslator(BaseTranslator):
    """Translates between unified format and Groq API (OpenAI-style)"""

    def __init__(self, debug: bool = False):
        super().__init__(debug=debug)

    def _assemble_request(self, config: UnifiedConfig, route_ctx: Any = ""):
        return self.to_groq(config, self.require_profile(route_ctx))

    def to_groq(self, config: UnifiedConfig, profile: Any) -> dict[str, Any]:
        """
        Convert unified config to Groq API format.

        Groq uses OpenAI-style messages with full streaming + tools support.
        Param shaping (temperature / top_p / max_completion_tokens / stop /
        reasoning_effort / reasoning_format) is DB-driven via profile.controls
        — the gpt-oss / qwen3 reasoning dialects are offering overrides
        (value_map + default + const), not api_class branches.
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
                        # YouTube URLs not supported by Groq - show warning
                        vcprint(
                            f"YouTube URL '{content.youtube_url}' is not supported by Groq models and will be skipped.",
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

        # clear_thinking is a Cerebras-only concept — not forwarded to Groq.
        # disable_reasoning has no equivalent on Groq (no reasoning support) — dropped.

        # Build request
        groq_request = {
            "model": config.model,
            "messages": messages,
        }

        # DB-resolved params (temperature / top_p / max_completion_tokens /
        # stop / reasoning_effort / reasoning_format ...).
        groq_request.update(resolve_outbound_params(config, profile.controls))
        if config.stream:
            groq_request["stream"] = True

        # Tools - Groq supports streaming with tools
        all_tools = self.build_provider_tools(config, "groq")

        # Response format — Groq (OpenAI-style) validates a specific nested
        # shape; passing the unified config through verbatim 400s. Convert here.
        groq_response_format = (
            self.build_openai_chat_response_format(config.response_format, "groq")
            if config.response_format
            else None
        )
        json_mode = (
            groq_response_format is not None
            and groq_response_format.get("type") in ("json_object", "json_schema")
        )

        # Groq rejects json mode combined with tools ("json mode cannot be
        # combined with tool/function calling"). When both are requested we keep
        # JSON mode and DROP the tools — these are small models and a caller who
        # asked for structured JSON is better served by guaranteed-valid JSON
        # than by tool access. This is a runtime ADJUSTMENT to keep the request
        # working for testing; it must never be silently persisted as the
        # configured behaviour, so we log it loudly every time it happens.
        if json_mode and all_tools:
            vcprint(
                data={
                    "provider": "groq",
                    "model": config.model,
                    "dropped_tool_count": len(all_tools),
                    "dropped_tools": [
                        t.get("function", {}).get("name", t.get("type", "?"))
                        for t in all_tools
                    ],
                    "kept_response_format": groq_response_format,
                },
                title=(
                    "⚠️  GROQ ADJUSTMENT: dropped tools to honour JSON mode — "
                    "Groq forbids json_object/json_schema + tools in one request. "
                    "Tools were REMOVED for this call so structured output works. "
                    "Do NOT persist this combination as a saved config; either "
                    "request JSON mode without tools, or tools without JSON mode."
                ),
                color="yellow",
                verbose=True,
            )
        elif all_tools:
            groq_request["tools"] = all_tools
            if config.tool_choice:
                groq_request["tool_choice"] = config.tool_choice

        if groq_response_format is not None:
            groq_request["response_format"] = groq_response_format

        vcprint(groq_request, "--> Groq Request", color="magenta", verbose=False)
        return groq_request

    def from_groq(self, response: Any) -> UnifiedResponse:
        """Convert Groq API response to unified format"""
        messages = []

        if not response.choices:
            return UnifiedResponse(messages=[], finish_reason=FinishReason.ERROR)

        choice = response.choices[0]
        message = choice.message
        content = []

        reasoning = openai_compatible_reasoning_text(message)
        if reasoning:
            content.append(ThinkingContent(text=reasoning, provider="groq"))

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
                    ToolCallContent(
                        id=tc.id, name=tc.function.name, arguments=arguments
                    )
                )

        # Best-effort citation capture — Groq message `annotations`
        # (document_citation / function_citation dialects, verified against the
        # groq SDK 2026-08-08). Attached to the text block's
        # metadata["citations"], the canonical cross-provider home. Guarded: a
        # malformed citation payload must never abort response translation.
        try:
            from matrx_ai.config.citations import normalize_openai_compatible_citations

            groq_citations = normalize_openai_compatible_citations(
                response, message, message.content or ""
            )
            if groq_citations:
                normalized_dicts = [c.model_dump(exclude_none=True) for c in groq_citations]
                for block in content:
                    if isinstance(block, TextContent):
                        block.metadata.setdefault("citations", normalized_dicts)
        except Exception as citation_exc:
            vcprint(
                f"[citations] groq citation capture failed — skipping citations "
                f"only (answer unaffected): {citation_exc}",
                color="red",
            )

        if content:
            messages.append(
                UnifiedMessage(role="assistant", content=content)
            )

        # Convert usage to TokenUsage
        token_usage = None
        if response.usage:
            token_usage = TokenUsage(
                input_tokens=response.usage.prompt_tokens,
                output_tokens=response.usage.completion_tokens,
                matrx_model_name=response.model,
                provider_model_name=response.model,
                api="groq",
                response_id=response.id,
                raw_usage=serialize_provider_usage(response.usage),
            )
        else:
            vcprint(
                f"⚠️  WARNING: Groq response missing usage data for model {response.model} (response_id: {response.id})",
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
