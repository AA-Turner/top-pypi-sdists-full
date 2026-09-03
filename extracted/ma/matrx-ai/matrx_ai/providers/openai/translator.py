from __future__ import annotations

from typing import Any

import rich
from matrx_utils import vcprint
from openai.types.responses import Response as OpenAIResponse
from openai.types.responses import ResponseOutputItem as OpenAIResponseOutputItem

from matrx_ai.config import (
    FinishReason,
    TokenUsage,
    UnifiedConfig,
    UnifiedMessage,
    UnifiedResponse,
)
from matrx_ai.config.enums import Role
from matrx_ai.config.extra_config import WebSearchCallContent
from matrx_ai.config.message_config import (
    iter_images_by_role,
    pick_image_by_role,
    pick_text_by_role,
)
from matrx_ai.config.tools_config import ToolCallContent
from matrx_ai.config.unified_content import TextContent, ThinkingContent
from matrx_ai.providers.base_translator import BaseTranslator
from matrx_ai.providers.cache_guard import normalize_openai_prompt_cache_key
from matrx_ai.providers.outbound_params import resolve_outbound_params

# ============================================================================
# OPENAI TRANSLATOR
# ============================================================================


class OpenAITranslator(BaseTranslator):
    """Translates between unified format and OpenAI Responses API"""

    def __init__(self, debug: bool = False):
        super().__init__(debug=debug)

    def _assemble_request(self, config: UnifiedConfig, route_ctx: Any = ""):
        return self.to_openai(config, self.require_profile(route_ctx))

    def to_openai(self, config: UnifiedConfig, profile: Any) -> dict[str, Any]:
        """
        Convert unified config to OpenAI Responses API format.

        Creates developer message from config.system_instruction.
        Delegates message conversion to UnifiedMessage.to_openai_items().

        Param shaping (temperature / top_p / max_output_tokens / reasoning.*)
        is DB-driven via ``profile.controls`` (ai.api.rules <-
        ai.offering.override). The gpt-5.x reasoning dialects mark
        temperature/top_p ``supported:false`` and map reasoning_effort /
        reasoning_summary onto ``reasoning.effort`` / ``reasoning.summary`` —
        rules data, no api_class branches here.
        """
        messages = []
        include_items = []

        if self.debug:
            rich.print(config)

        # Add developer message from system_instruction if present
        system_text = self.get_system_text(config)
        if system_text:
            messages.append(
                {
                    "role": "developer",
                    "content": [{"type": "input_text", "text": system_text}],
                }
            )

        # Process all messages - delegate to message method
        for msg in config.messages:
            converted = msg.to_openai_items_modified()
            if self.debug:
                rich.print(converted)
            messages.extend(converted)

        # Build request
        openai_request = {"model": config.model, "input": messages}

        tools = self.build_provider_tools(config, "openai")
        if config.internal_web_search:
            tools.append({"type": "web_search_preview"})

        if tools:
            openai_request["tools"] = tools

        # DB-resolved params: temperature / top_p / max_output_tokens plus the
        # reasoning dialects' nested ``reasoning`` object (dotted provider keys
        # already expanded by the control engine).
        openai_request.update(resolve_outbound_params(config, profile.controls))

        # Response format — OpenAI Responses API expects a ``text.format``
        # object. Convert here (the old verbatim/string-compare logic never
        # matched, so structured output silently never engaged).
        if config.response_format:
            text_format = self._build_openai_text_format(config.response_format)
            if text_format is not None:
                # MERGE into any existing ``text`` object — the DB-resolved
                # params may already have landed ``text.verbosity`` there.
                text_obj = openai_request.get("text")
                if not isinstance(text_obj, dict):
                    text_obj = {}
                    openai_request["text"] = text_obj
                text_obj["format"] = text_format

        # Tool choice
        if config.tool_choice:
            openai_request["tool_choice"] = config.tool_choice

        # Parallel tool calls
        if not config.parallel_tool_calls:
            openai_request["parallel_tool_calls"] = False

        # Stream - Stream is not included in the request and is handled be the execution logic
        # if config.stream:
        #     openai_request["stream"] = True

        # Reasoning-capable dialects (the rules declare reasoning_effort
        # supported) get encrypted reasoning content in the response so
        # stateless multi-turn replay of reasoning items keeps working — even
        # on a turn whose effort resolved to "omit the field" (auto).
        if profile.controls.rule_for("reasoning_effort").supported is not False:
            include_items.append("reasoning.encrypted_content")

        if include_items:
            openai_request["include"] = include_items

        if config.store is not None:
            openai_request["store"] = config.store

        if config.prompt_cache_key:
            openai_request["prompt_cache_key"] = normalize_openai_prompt_cache_key(
                config.prompt_cache_key
            )

        return openai_request

    @staticmethod
    def _build_openai_text_format(
        response_format: Any,
    ) -> dict[str, Any] | None:
        """Map the unified ``response_format`` onto the OpenAI Responses API
        ``text.format`` object.

        IMPORTANT: the Responses API FLATTENS the schema config directly under
        ``format`` — unlike Chat Completions, ``name`` / ``schema`` / ``strict``
        are NOT nested under a ``json_schema`` key:
          - ``{"type": "text"}``
          - ``{"type": "json_object"}``                         (valid JSON, no schema)
          - ``{"type": "json_schema", "name", "schema", "strict"?}`` (schema-enforced)

        ``json_schema`` *requires* ``name`` + ``schema`` (both Required in the
        SDK's ResponseFormatTextJSONSchemaConfigParam).
        """
        if not isinstance(response_format, dict):
            return None

        fmt_type = response_format.get("type")
        if fmt_type == "text":
            return {"type": "text"}
        if fmt_type == "json_object":
            return {"type": "json_object"}
        if fmt_type != "json_schema":
            vcprint(
                response_format,
                "WARNING: Unknown response format type",
                color="red",
            )
            return {"type": "text"}

        # Locate name / strict / schema across the shapes response_format can
        # arrive in: a full OpenAI envelope ({name, schema, strict}), a raw JSON
        # Schema nested under json_schema, or a bare {"type": "json_schema"}
        # placeholder with no schema at all.
        inner = response_format.get("json_schema")
        name: str | None = None
        strict: bool | None = None
        schema: dict[str, Any] | None = None
        if isinstance(inner, dict):
            if isinstance(inner.get("schema"), dict):
                schema = inner["schema"]
                name = inner.get("name")
                strict = inner.get("strict")
            elif {"type", "properties", "items"} & inner.keys():
                schema = inner  # inner IS the raw JSON Schema
        elif isinstance(response_format.get("schema"), dict):
            schema = response_format["schema"]
            name = response_format.get("name")
            strict = response_format.get("strict")

        # json_schema mode requires a schema whose ROOT is an object
        # ({"type": "object"}). A missing schema, or an array/scalar-root schema
        # (e.g. a top-level list of records), can't be used. The frontend should
        # reject non-object roots up front, but we downgrade defensively to
        # json_object here so a slip-through still produces valid JSON instead of
        # a 400. This is a runtime ADJUSTMENT (schema is NOT enforced) — log it
        # loudly so it's never mistaken for the configured behaviour.
        downgrade_reason: str | None = None
        if not isinstance(schema, dict):
            downgrade_reason = "no JSON Schema was supplied with the json_schema request"
        elif not (
            schema.get("type") == "object"
            or (schema.get("type") is None and isinstance(schema.get("properties"), dict))
        ):
            downgrade_reason = (
                f"schema root is not an object (type={schema.get('type')!r}); "
                "OpenAI requires an object root"
            )
        if downgrade_reason is not None:
            vcprint(
                data={
                    "provider": "openai",
                    "requested": response_format,
                    "downgraded_to": "json_object",
                    "reason": downgrade_reason,
                },
                title=(
                    "⚠️  OPENAI ADJUSTMENT: json_schema → json_object — schema is "
                    "NOT enforced (valid JSON only). The frontend should reject this; "
                    "do NOT persist it as a saved config."
                ),
                color="yellow",
                verbose=True,
            )
            return {"type": "json_object"}

        # OpenAI strict structured output rejects advisory bounds it does not
        # support (minItems/maxItems/pattern/…); reduce to its accepted subset at
        # the shared seam. The stored schema keeps the rich bounds.
        schema = OpenAITranslator.sanitize_structured_output_schema(schema, "openai")

        # Flattened directly under format — NOT nested under json_schema.
        text_format: dict[str, Any] = {
            "type": "json_schema",
            "name": name or "response",
            "schema": schema,
        }
        # strict carries hard schema constraints (object root, additionalProperties
        # false everywhere, restricted JSON Schema subset) — enabling it on an
        # arbitrary schema can itself 400. Only set it when explicitly opted in.
        if strict is not None:
            text_format["strict"] = bool(strict)

        return text_format

    def from_openai(self, response: OpenAIResponse, matrx_model_name: str) -> UnifiedResponse:
        """
        Convert OpenAI Responses API response to unified format.

        OpenAI returns flat output items (reasoning, function_call, message, etc.)
        as siblings. We must reorganize them into the canonical message structure:

        - Reasoning (+ hosted web-search calls) lead, in an 'output' role message
          when reasoning is present, otherwise 'assistant'.
        - Assistant text follows, in its own 'assistant' message.
        - Tool calls come LAST, in their own 'assistant' message, so the tool_use
          blocks sit immediately before the role='tool' results the executor
          appends next. See ``_build_unified_messages`` — this ordering is a
          correctness requirement, not cosmetics.
        - A text-only response is a single 'assistant' message.

        This normalization ensures OpenAI responses match the same canonical DB
        structure that Anthropic and Google already produce.
        """
        messages = self._build_unified_messages(response.output)
        # vcprint(messages, "[OPENAI TRANSLATOR] Unified Messages", color="pink")

        token_usage = TokenUsage.from_openai(
            response.usage,
            matrx_model_name=matrx_model_name,
            provider_model_name=response.model,
            response_id=response.id,
        )

        finish_reason = None
        if response.status == "completed":
            finish_reason = FinishReason.STOP
        elif response.status == "incomplete":
            finish_reason = FinishReason.MAX_TOKENS
        elif response.status == "failed":
            finish_reason = FinishReason.ERROR

        return UnifiedResponse(
            messages=messages,
            usage=token_usage,
            finish_reason=finish_reason,
            raw_response=response,
        )

    def _build_unified_messages(
        self, output_items: list[OpenAIResponseOutputItem]
    ) -> list[UnifiedMessage]:
        """
        Convert OpenAI's flat output items into canonical UnifiedMessage list.

        Collects thinking, tool_call, web_search, and text content blocks from the
        raw output, then assembles them into properly-roled messages matching the
        DB contract all providers share.
        """
        thinking_blocks: list[ThinkingContent] = []
        tool_call_blocks: list[ToolCallContent] = []
        web_search_blocks: list[WebSearchCallContent] = []
        text_blocks: list[TextContent] = []

        for item in output_items:
            # vcprint(item, "[OPENAI TRANSLATOR] Output Item", color="cyan")

            if item.type == "reasoning":
                thinking_blocks.append(ThinkingContent.from_openai(item))

            elif item.type == "function_call":
                tool_call_blocks.append(ToolCallContent.from_openai(item))

            elif item.type == "web_search_call":
                web_search_blocks.append(WebSearchCallContent.from_openai(item))

            elif item.type == "message":
                for content_item in item.content:
                    if content_item.type == "output_text":
                        # item.id (the Responses API output-item id) rides on
                        # TextContent.id — that's what to_openai_items replays.
                        # It must NOT touch UnifiedMessage.id (cx_message.id only).
                        text_blocks.append(TextContent.from_openai(content_item, item.id))
                    elif content_item.type == "refusal":
                        vcprint(content_item, "[OPENAI TRANSLATOR] Refusal", color="red")
                        text_blocks.append(TextContent(text=content_item.refusal or ""))
                    else:
                        vcprint(
                            content_item, "[OPENAI TRANSLATOR] Unknown content type", color="red"
                        )
            else:
                vcprint(
                    item, f"[OPENAI TRANSLATOR] Unknown output item type: {item.type}", color="red"
                )

        has_thinking = bool(thinking_blocks)
        has_tool_calls = bool(tool_call_blocks)
        has_text = bool(text_blocks)

        messages: list[UnifiedMessage] = []

        # ORDER IS LOAD-BEARING — tool calls go LAST, in their own message.
        #
        # The executor appends this turn's role='tool' results immediately after
        # these messages, and every provider requires a tool_use's tool_result to
        # be in the IMMEDIATELY-following message (Anthropic 400s otherwise) — a
        # rule `MessageList.sanitize` enforces before every provider call.
        # Grouping the tool calls with the reasoning blocks and emitting the
        # assistant TEXT message after them put a text message BETWEEN a tool_use
        # and its result: sanitize then deleted the tool_use as "non-adjacent",
        # deleted its now-orphaned tool_result, and deleted the emptied
        # role='tool' message. Those messages never reached cx_message, so the
        # tool call vanished from the persisted transcript AND from the model's
        # own history on the next iteration — silently, visible only after a page
        # reload. Reproduced live 2026-08-11 (conversation b0562a35…,
        # call_MrmUn3pwQLTCzwXQGqFlinL2); 251 occurrences in the preceding 30
        # days of app_log.
        #
        # Flattened by `to_openai_items_modified`, this replays as reasoning →
        # web_search → message → function_call: OpenAI's OWN output order, which
        # also satisfies the Responses API rule that a reasoning item be
        # immediately followed by its associated output item (previously the
        # function_call was replayed between the reasoning and its message).
        pre_text_content = [*thinking_blocks, *web_search_blocks]

        if pre_text_content:
            role = Role.OUTPUT if has_thinking else Role.ASSISTANT
            messages.append(
                UnifiedMessage(
                    role=role,
                    content=pre_text_content,
                )
            )

        if has_text:
            messages.append(
                UnifiedMessage(
                    role=Role.ASSISTANT,
                    content=text_blocks,
                )
            )

        if has_tool_calls:
            messages.append(
                UnifiedMessage(
                    role=Role.ASSISTANT,
                    content=list(tool_call_blocks),
                )
            )

        return messages




    def to_openai_video_extend(self, config: UnifiedConfig) -> dict[str, Any]:
        """Build kwargs for ``POST /v1/videos/extensions`` — extends an
        existing video by up to 20 seconds (max 6 extensions = 120s total).

        ``config.video_input`` carries the source video (must be an
        OpenAI-hosted video_id; the boundary resolver should have populated
        ``resolved_url`` or ``file_id``).
        """
        prompt = self._extract_prompt(config)
        if config.video_input is None:
            raise ValueError("to_openai_video_extend requires config.video_input")

        # Sora extension takes the previous video_id (we store it in file_id
        # when the source originated from OpenAI).
        video_id = getattr(config.video_input, "file_id", None) or (
            config.video_input.get("file_id") if isinstance(config.video_input, dict) else None
        )
        if not video_id:
            raise ValueError(
                "video extension requires the original OpenAI video_id on video_input.file_id"
            )

        kwargs: dict[str, Any] = {
            "video_id": video_id,
            "prompt": prompt,
        }
        if config.duration_seconds is not None:
            kwargs["seconds"] = str(min(20, int(config.duration_seconds)))
        return kwargs

    def to_openai_video_edit(self, config: UnifiedConfig) -> dict[str, Any]:
        """Build kwargs for ``POST /v1/videos/edits`` — remix an existing
        video with a new prompt."""
        prompt = self._extract_prompt(config)
        if config.video_input is None:
            raise ValueError("to_openai_video_edit requires config.video_input")
        video_id = getattr(config.video_input, "file_id", None) or (
            config.video_input.get("file_id") if isinstance(config.video_input, dict) else None
        )
        if not video_id:
            raise ValueError(
                "video edit requires the original OpenAI video_id on video_input.file_id"
            )
        return {
            "video_id": video_id,
            "prompt": prompt,
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _extract_prompt(self, config: UnifiedConfig) -> str:
        prompt = pick_text_by_role(config.messages, None) or ""
        if not prompt and config.system_instruction:
            prompt = self.get_system_text(config) or ""
        return prompt


    @staticmethod
    def _mediaref_to_file_tuple(ref: Any) -> Any | None:
        """Convert a MediaRef-shaped object (already resolved at the boundary)
        into a tuple (filename, bytes, mime_type) suitable for openai's
        multipart upload, or a file-like object.

        Resolution priority: ``base64_data`` → ``resolved_url`` → ``url``.
        Returns None on failure.
        """
        if ref is None:
            return None

        b64 = getattr(ref, "base64_data", None) or (
            ref.get("base64_data") if isinstance(ref, dict) else None
        )
        url = (
            getattr(ref, "resolved_url", None)
            or getattr(ref, "url", None)
            or (ref.get("resolved_url") or ref.get("url") if isinstance(ref, dict) else None)
        )
        mime = (
            getattr(ref, "mime_type", None)
            or (ref.get("mime_type") if isinstance(ref, dict) else None)
            or "image/png"
        )
        ext = "png"
        if mime.endswith("/jpeg") or mime.endswith("/jpg"):
            ext = "jpg"
        elif mime.endswith("/webp"):
            ext = "webp"

        import base64 as _b64

        if b64:
            try:
                data = _b64.b64decode(b64)
            except Exception:
                return None
            return (f"image.{ext}", data, mime)

        # No fallback URL fetch — the AI Dream API boundary
        # (normalize_request_body) is responsible for pre-fetching bytes
        # via FileManager.resolve_media_async(..., needs_bytes=True). If
        # we get here without base64_data, the boundary didn't run or
        # its resolver failed — log loudly instead of silently degrading.
        from matrx_utils import vcprint

        vcprint(
            f"[openai.translator] _mediaref_to_file_tuple: ref carried url={url!r} "
            f"but no resolved base64_data — the boundary normalizer failed to pre-fetch. "
            f"Dropping this file.",
            color="red",
        )
        return None
