from __future__ import annotations

import json
from typing import Any

from matrx_utils import vcprint
from xai_sdk.chat import (
    assistant,
    system,
    text,
    tool_result,
    user,
)
from xai_sdk.chat import (
    image as xai_image,
)
from xai_sdk.chat import (
    tool as xai_tool,
)
from xai_sdk.proto import chat_pb2
from xai_sdk.tools import web_search, x_search

from matrx_ai.config import (
    FinishReason,
    ProviderCharge,
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
from matrx_ai.config.citations import normalize_xai_citations
from matrx_ai.config.media_config import ImageContent
from matrx_ai.providers.base_translator import BaseTranslator
from matrx_ai.providers.outbound_params import resolve_outbound_params


def provider_charge_from_xai_usage(usage: Any) -> ProviderCharge | None:
    """Extract xAI's exact USD charge when the response carries one."""
    try:
        from xai_sdk.cost import cost_usd_from_usage

        reported_cost = cost_usd_from_usage(usage)
    except (AttributeError, TypeError, ValueError):
        return None
    if reported_cost is None:
        return None
    return ProviderCharge(
        amount_usd=reported_cost,
        raw_amount=getattr(usage, "cost_in_usd_ticks"),
        raw_unit="usd_tick_1e-10",
        field_path="usage.cost_in_usd_ticks",
    )

# ============================================================================
# XAI TRANSLATOR — native xai_sdk (gRPC) request/response shaping
# ============================================================================
#
# Unlike the OpenAI-compatible shim it replaced, this builds native xai_sdk
# proto objects so we get first-class reasoning_effort + the server-side
# web_search() / x_search() tools. ``to_xai`` returns a kwargs dict ready for
# ``AsyncClient.chat.create(**kwargs)``; ``from_xai`` converts the native
# Response back to the unchanged UnifiedResponse contract.


class XAITranslator(BaseTranslator):
    """Translates between the unified format and the native xAI Grok SDK."""

    def __init__(self, debug: bool = False):
        super().__init__(debug=debug)

    # ------------------------------------------------------------------ build
    def _assemble_request(self, config: UnifiedConfig, route_ctx: Any = ""):
        return self.to_xai(config, self.require_profile(route_ctx))

    def to_xai(self, config: UnifiedConfig, profile: Any) -> dict[str, Any]:
        """Convert unified config to native xai_sdk ``chat.create`` kwargs.

        Values may be proto objects (messages, tools, response_format), so the
        result is NOT JSON-serializable — use ``debug_summary`` for logging.

        Param shaping (temperature / top_p / max_tokens / stop /
        reasoning_effort) is DB-driven via ``profile.controls`` — the
        none-floors-to-low (xai_standard) vs none-disables (xai_reasoning)
        contracts are offering-override value_maps, not api_class branches.
        """
        kwargs: dict[str, Any] = {
            "model": config.model,
            "messages": self._build_messages(config),
        }
        kwargs.update(resolve_outbound_params(config, profile.controls))

        if config.parallel_tool_calls is not None:
            kwargs["parallel_tool_calls"] = config.parallel_tool_calls

        response_format = self._build_response_format(config)
        if response_format is not None:
            kwargs["response_format"] = response_format

        tools = self._build_tools(config)
        if tools:
            kwargs["tools"] = tools
            if config.tool_choice == "required":
                # native enum literal; a per-tool force would use required_tool(name)
                kwargs["tool_choice"] = "required"
            elif config.tool_choice in ("auto", "none"):
                kwargs["tool_choice"] = config.tool_choice

        return kwargs

    def _build_messages(self, config: UnifiedConfig) -> list[chat_pb2.Message]:
        messages: list[chat_pb2.Message] = []

        system_text = self.get_system_text(config)
        if system_text:
            messages.append(system(text(system_text)))

        for msg in config.messages:
            if msg.role == "system":
                sys_text = "".join(
                    c.text for c in msg.content if isinstance(c, TextContent)
                )
                if sys_text:
                    messages.append(system(text(sys_text)))
                continue

            if msg.role == "tool":
                # role=tool carries one tool_result per ToolResultContent.
                # Image-bearing results surface their images as a follow-up
                # user message (native tool_result content is text-only).
                pending_images: list[chat_pb2.Content] = []
                for content in msg.content:
                    if isinstance(content, ToolResultContent):
                        oa = content.to_openai_chat()
                        result_str = oa.get("content") if isinstance(oa, dict) else None
                        if not isinstance(result_str, str):
                            result_str = json.dumps(result_str) if result_str is not None else ""
                        messages.append(
                            tool_result(result_str, tool_call_id=oa.get("tool_call_id"))
                        )
                        for image_block in content.extract_image_blocks():
                            img = self._image_content(image_block)
                            if img is not None:
                                pending_images.append(img)
                if pending_images:
                    messages.append(user(*pending_images))
                continue

            # user / assistant
            text_parts: list[str] = []
            image_parts: list[chat_pb2.Content] = []
            tool_calls: list[chat_pb2.ToolCall] = []

            for content in msg.content:
                if isinstance(content, TextContent):
                    text_parts.append(content.text)
                elif isinstance(content, ImageContent):
                    img = self._image_content(content)
                    if img is not None:
                        image_parts.append(img)
                elif isinstance(content, ToolCallContent):
                    tool_calls.append(
                        chat_pb2.ToolCall(
                            id=content.id,
                            function=chat_pb2.FunctionCall(
                                name=content.wire_name,
                                arguments=json.dumps(content.arguments),
                            ),
                        )
                    )
                elif isinstance(content, YouTubeVideoContent):
                    vcprint(
                        f"YouTube URL '{content.youtube_url}' is not supported by xAI "
                        "models and will be skipped.",
                        "YouTube URL Warning",
                        color="yellow",
                    )

            combined_text = "".join(text_parts)

            if msg.role == "assistant" and tool_calls:
                # Assistant turns that carried tool calls need the tool_calls
                # field populated directly (the assistant() builder is content-only).
                content_protos: list[chat_pb2.Content] = []
                if combined_text:
                    content_protos.append(text(combined_text))
                content_protos.extend(image_parts)
                messages.append(
                    chat_pb2.Message(
                        role=chat_pb2.MessageRole.ROLE_ASSISTANT,
                        content=content_protos,
                        tool_calls=tool_calls,
                    )
                )
                continue

            parts: list[chat_pb2.Content] = []
            if combined_text:
                parts.append(text(combined_text))
            parts.extend(image_parts)
            if not parts:
                parts.append(text(""))

            if msg.role == "assistant":
                messages.append(assistant(*parts))
            else:
                messages.append(user(*parts))

        return messages

    @staticmethod
    def _image_content(content: Any) -> chat_pb2.Content | None:
        """Convert a resolved image block to a native xai_sdk image Content.

        Reuses the OpenAI-chat serializer (which already resolves to a URL or a
        data: URI) and feeds its url string into the native ``image()`` builder.
        """
        oa = content.to_openai_chat()
        if not isinstance(oa, dict):
            return None
        url = (oa.get("image_url") or {}).get("url")
        if not url:
            return None
        return xai_image(url)

    def _build_tools(self, config: UnifiedConfig) -> list[chat_pb2.Tool]:
        tools: list[chat_pb2.Tool] = []

        # Function tools — reuse the provider-agnostic dedup chokepoint, then
        # convert the deduped OpenAI-chat declarations to native proto tools.
        for decl in self.build_provider_tools(config, "xai"):
            fn = decl.get("function") if isinstance(decl, dict) else None
            if not isinstance(fn, dict) or not fn.get("name"):
                continue
            tools.append(
                xai_tool(
                    name=fn["name"],
                    description=fn.get("description", "") or "",
                    parameters=fn.get("parameters") or {"type": "object", "properties": {}},
                )
            )

        # Server-side native tools — mixed into the same list (xAI allows it).
        if config.internal_web_search:
            tools.append(web_search())
        if config.internal_x_search:
            tools.append(x_search())

        return tools

    def _build_response_format(
        self, config: UnifiedConfig
    ) -> chat_pb2.ResponseFormat | None:
        """Convert the unified response_format to a native proto.

        json_schema → FORMAT_TYPE_JSON_SCHEMA(+schema); json_object →
        FORMAT_TYPE_JSON_OBJECT. Reuses the shared OpenAI-chat normalizer so the
        accepted unified shapes match every other chat provider.
        """
        if not config.response_format:
            return None

        oa = self.build_openai_chat_response_format(config.response_format, "xai")
        if not isinstance(oa, dict):
            return None

        rf_type = oa.get("type")
        if rf_type == "json_schema":
            schema = (oa.get("json_schema") or {}).get("schema")
            if schema is None:
                vcprint(
                    "⚠️  xAI: json_schema response_format had no schema; omitting.",
                    color="yellow",
                )
                return None
            return chat_pb2.ResponseFormat(
                format_type=chat_pb2.FORMAT_TYPE_JSON_SCHEMA,
                schema=json.dumps(schema),
            )
        if rf_type == "json_object":
            return chat_pb2.ResponseFormat(format_type=chat_pb2.FORMAT_TYPE_JSON_OBJECT)
        return None

    @staticmethod
    def debug_summary(kwargs: dict[str, Any]) -> dict[str, Any]:
        """A JSON-serializable rendering of the native kwargs for logging/snapshot."""
        tools = kwargs.get("tools") or []
        tool_names: list[str] = []
        for t in tools:
            if t.HasField("function"):
                tool_names.append(t.function.name)
            elif t.HasField("web_search"):
                tool_names.append("web_search")
            elif t.HasField("x_search"):
                tool_names.append("x_search")
            else:
                tool_names.append("<native>")
        rf = kwargs.get("response_format")
        return {
            "model": kwargs.get("model"),
            "message_count": len(kwargs.get("messages") or []),
            "reasoning_effort": kwargs.get("reasoning_effort"),
            "tools": tool_names,
            "tool_choice": kwargs.get("tool_choice"),
            "temperature": kwargs.get("temperature"),
            "top_p": kwargs.get("top_p"),
            "max_tokens": kwargs.get("max_tokens"),
            "response_format": (
                chat_pb2.FormatType.Name(rf.format_type) if rf is not None else None
            ),
        }

    # --------------------------------------------------------------- response
    def from_xai(self, response: Any) -> UnifiedResponse:
        """Convert a native xai_sdk Response to the unified format."""
        content: list[Any] = []

        reasoning = getattr(response, "reasoning_content", None)
        if isinstance(reasoning, str) and reasoning:
            content.append(ThinkingContent(text=reasoning, provider="xai"))

        if response.content:
            content.append(TextContent(text=response.content))

        for tc in response.tool_calls:
            raw_args = tc.function.arguments
            try:
                arguments = json.loads(raw_args) if raw_args else {}
            except (ValueError, TypeError):
                arguments = {}
            content.append(
                ToolCallContent(id=tc.id, name=tc.function.name, arguments=arguments)
            )

        messages: list[UnifiedMessage] = []
        if content:
            messages.append(
                UnifiedMessage(role="assistant", content=content)
            )

        token_usage = None
        usage = getattr(response, "usage", None)
        if usage is not None and getattr(usage, "total_tokens", 0):
            provider_charge = provider_charge_from_xai_usage(usage)
            token_usage = TokenUsage(
                input_tokens=usage.prompt_tokens,
                output_tokens=usage.completion_tokens,
                matrx_model_name=response.proto.model,
                provider_model_name=response.proto.model,
                api="xai",
                response_id=response.id,
                raw_usage=serialize_provider_usage(usage),
                provider_charge=provider_charge,
            )
        else:
            vcprint(
                f"⚠️  WARNING: xAI response missing usage data (response_id: {response.id})",
                color="red",
            )

        finish_reason = _FINISH_REASON_MAP.get(response.finish_reason)

        unified = UnifiedResponse(
            messages=messages,
            usage=token_usage,
            finish_reason=finish_reason,
            stop_reason=response.finish_reason,
        )

        # Citations from web_search / x_search. Response-level raw list is kept
        # (existing consumers), and the canonical NormalizedCitation shape is
        # attached to the message's TEXT block(s) metadata["citations"] — the
        # cross-provider home the storage layer (TextPart.citations) reads.
        citations = list(getattr(response, "citations", []) or [])
        if citations:
            unified.metadata["citations"] = citations
            normalized = [
                c.model_dump(exclude_none=True) for c in normalize_xai_citations(citations)
            ]
            text_blocks = [
                item
                for message in messages
                for item in (message.content or [])
                if isinstance(item, TextContent)
            ]
            for block in text_blocks:
                block.metadata.setdefault("citations", normalized)
            if not text_blocks:
                vcprint(
                    "[citations] xAI response carried citations but no text "
                    "block exists to attach them to — normalized citations "
                    "remain only in response-level metadata['citations_normalized'].",
                    color="yellow",
                )
                unified.metadata["citations_normalized"] = normalized

        return unified


_FINISH_REASON_MAP = {
    "REASON_STOP": FinishReason.STOP,
    "REASON_MAX_LEN": FinishReason.MAX_TOKENS,
    "REASON_MAX_CONTEXT": FinishReason.MAX_TOKENS,
    "REASON_TOOL_CALLS": FinishReason.TOOL_CALLS,
}
