from __future__ import annotations

import json
from copy import deepcopy
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
    VideoContent,
    YouTubeVideoContent,
)
from matrx_ai.config.media_config import ImageContent
from matrx_ai.config.usage_config import openai_compatible_usage_counts, serialize_provider_usage
from matrx_ai.providers.base_translator import BaseTranslator
from matrx_ai.providers.outbound_params import resolve_outbound_params
from matrx_ai.providers.reasoning import openai_compatible_reasoning_text


class GenericOpenAITranslator(BaseTranslator):
    """Translates between unified format and any OpenAI-compatible API."""

    def __init__(self, debug: bool = False):
        super().__init__(debug=debug)

    def _assemble_request(self, config: UnifiedConfig, route_ctx: Any = ""):
        return self.to_generic_openai(config, self.require_profile(route_ctx))

    def to_generic_openai(self, config: UnifiedConfig, profile: Any = None) -> dict[str, Any]:
        """
        Convert unified config to OpenAI-compatible chat completion format.

        Works with any OpenAI-compatible endpoint (HuggingFace TGI, llama.cpp server,
        vLLM, LocalAI, Ollama, etc.). Param shaping (temperature / top_p /
        max_tokens / stop) is DB-driven via ``profile.controls``; a host-catalog
        profile with no rules passes the canonical params through unchanged.
        ``profile`` may be omitted ONLY in provider-less unit contexts — a bare
        call keeps legacy passthrough params via an empty passthrough profile.
        """
        if profile is None:
            from matrx_ai.testing.profile_factory import make_profile

            profile = make_profile(
                model_name=str(getattr(config, "model", "") or "generic"),
                wire_format="generic_openai_chat",
            )
        provider_name = profile.vendor or "generic_openai"
        messages = []

        system_text = self.get_system_text(config)
        if system_text:
            messages.append({"role": "system", "content": system_text})

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
                media_parts: list[dict[str, Any]] = []
                tool_calls: list[dict[str, Any]] = []
                reasoning_parts: list[str] = []

                for content in msg.content:
                    if isinstance(content, TextContent):
                        text_parts.append(content.text)
                    elif isinstance(content, ThinkingContent):
                        reasoning_parts.append(content.text)
                    elif isinstance(content, ImageContent):
                        image_part = (
                            content.to_moonshot_chat()
                            if profile.vendor == "moonshot"
                            else content.to_openai_chat()
                        )
                        if image_part is not None:
                            media_parts.append(image_part)
                    elif isinstance(content, VideoContent):
                        if profile.vendor != "moonshot":
                            vcprint(
                                f"Video input is not supported by {provider_name}; it will not be sent.",
                                "Video Input Warning",
                                color="yellow",
                            )
                            continue
                        media_parts.append(content.to_moonshot_chat())
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
                        vcprint(
                            f"YouTube URL '{content.youtube_url}' is not supported by generic OpenAI-compatible endpoints and will be skipped.",
                            "YouTube URL Warning",
                            color="yellow",
                        )

                if media_parts:
                    # OpenAI Chat Completions multimodal content array —
                    # llama-server / Ollama / vLLM / LocalAI all accept this
                    # exact shape for their vision-enabled models
                    # (e.g. Qwen2-VL, LLaVA, MiniCPM-V).
                    combined_text = "".join(text_parts)
                    parts: list[dict[str, Any]] = []
                    if combined_text:
                        parts.append({"type": "text", "text": combined_text})
                    parts.extend(media_parts)
                    message_dict["content"] = parts
                elif text_parts:
                    message_dict["content"] = "".join(text_parts)
                elif tool_calls:
                    message_dict["content"] = None
                else:
                    message_dict["content"] = ""

                if tool_calls:
                    message_dict["tool_calls"] = tool_calls

                # Kimi's Partial Mode is a message-level extension, not a
                # top-level completion parameter.  The unified message
                # metadata carries it without leaking the Moonshot-specific
                # wire name into other provider translators.
                if profile.vendor == "moonshot" and msg.metadata.get("partial") is True:
                    if msg.role != "assistant":
                        raise ValueError("Moonshot partial mode requires an assistant message")
                    message_dict["partial"] = True
                    if reasoning_parts:
                        message_dict["reasoning_content"] = "".join(reasoning_parts)

                if (
                    text_parts
                    or tool_calls
                    or media_parts
                    or message_dict["content"] == ""
                ):
                    messages.append(message_dict)

        # clear_thinking is a Cerebras-only concept — not forwarded to generic OpenAI providers.
        # disable_reasoning has no generic equivalent — dropped.

        # ``request_defaults`` are trusted API-catalog values, not caller
        # controls. They cover structural provider requirements such as asking
        # a compatible streaming API to include terminal usage. Deep-copy so a
        # provider SDK cannot mutate the immutable resolved catalog profile.
        request_defaults = getattr(profile, "request_defaults", {}) or {}
        request: dict[str, Any] = deepcopy(request_defaults)
        request.update({
            "model": config.model,
            "messages": messages,
        })

        # DB-resolved params (temperature / top_p / max_tokens / stop ...).
        request.update(resolve_outbound_params(config, profile.controls))
        # Response format — OpenAI-compatible Chat Completions validates a
        # specific nested shape; passing the unified config through verbatim
        # 400s on schema-capable backends. Convert here.
        if config.response_format:
            generic_response_format = self.build_openai_chat_response_format(
                config.response_format, provider_name
            )
            if generic_response_format is not None:
                request["response_format"] = generic_response_format
        if config.stream:
            request["stream"] = True

        all_tools = self.build_provider_tools(config, "generic_openai")
        if all_tools:
            request["tools"] = all_tools
            if config.tool_choice:
                request["tool_choice"] = config.tool_choice

        vcprint(request, f"--> {provider_name} Request", color="magenta", verbose=False)
        return request

    def from_generic_openai(
        self,
        response: Any,
        provider_name: str = "generic_openai",
        *,
        matrx_model_name: str | None = None,
    ) -> UnifiedResponse:
        """Convert OpenAI-compatible response to unified format."""
        messages = []

        if not response.choices:
            return UnifiedResponse(messages=[], finish_reason=FinishReason.ERROR)

        choice = response.choices[0]
        message = choice.message
        content = []

        # A durable thinking block is distinct from answer text.  Do not fold it
        # into XML in TextContent: conversation persistence serializes content
        # blocks, and that shortcut makes reasoning unrecoverable on replay.
        reasoning = openai_compatible_reasoning_text(message)
        main_text = message.content or ""

        if reasoning:
            content.append(
                ThinkingContent(
                    text=reasoning,
                    provider="moonshot" if provider_name == "moonshot" else "generic_openai",
                )
            )
        if main_text:
            content.append(TextContent(text=main_text))

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

        # Best-effort citation capture — Perplexity-style top-level `citations`
        # or message `annotations` (OpenAI/Groq dialects). Attached to the text
        # block's metadata["citations"], the canonical cross-provider home the
        # storage layer (TextPart.citations) reads. Guarded: a malformed
        # citation payload must never abort response translation.
        try:
            from matrx_ai.config.citations import normalize_openai_compatible_citations

            compatible_citations = normalize_openai_compatible_citations(
                response, message, main_text
            )
            if compatible_citations:
                normalized_dicts = [
                    c.model_dump(exclude_none=True) for c in compatible_citations
                ]
                text_blocks = [b for b in content if isinstance(b, TextContent)]
                for block in text_blocks:
                    block.metadata.setdefault("citations", normalized_dicts)
                if not text_blocks:
                    vcprint(
                        f"[citations] {provider_name} response carried citations "
                        "but no text block exists to attach them to — dropped "
                        "from storage (raw response still holds them).",
                        color="yellow",
                    )
        except Exception as citation_exc:
            vcprint(
                f"[citations] {provider_name} citation capture failed — "
                f"skipping citations only (answer unaffected): {citation_exc}",
                color="red",
            )

        if content:
            messages.append(
                UnifiedMessage(role="assistant", content=content)
            )

        token_usage = None
        if response.usage:
            input_tokens, output_tokens, cached_input_tokens = openai_compatible_usage_counts(
                response.usage
            )
            token_usage = TokenUsage(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cached_input_tokens=cached_input_tokens,
                matrx_model_name=matrx_model_name or getattr(response, "model", ""),
                provider_model_name=getattr(response, "model", ""),
                api=provider_name,
                response_id=response.id,
                raw_usage=serialize_provider_usage(response.usage),
            )

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
