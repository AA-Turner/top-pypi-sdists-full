from __future__ import annotations

from typing import Any, TypedDict

from google.genai import types
from google.genai.types import (
    Content,
    GenerateContentConfig,
    GenerateContentResponse,
    Part,
)
from matrx_utils import vcprint

from matrx_ai.config import (
    AudioContent,
    CodeExecutionContent,
    CodeExecutionResultContent,
    DocumentContent,
    FinishReason,
    ImageContent,
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
from matrx_ai.config.citations import normalize_google_grounding
from matrx_ai.providers.base_translator import BaseTranslator
from matrx_ai.providers.outbound_params import resolve_outbound_params
from matrx_ai.schema.rules import rewrite_const_as_enum

# ============================================================================
# SAFETY SETTINGS — lowest possible, applied to every text/image generate_content
# ============================================================================
# Gemini blocks legitimate content far too aggressively at its defaults (a
# Wikipedia "Artificial intelligence" page tripped the filter and killed a whole
# research run on 2026-06). We disable every ADJUSTABLE harm category.
#
# Threshold choice: ``OFF`` is the absolute lowest — it disables the filter for
# the category entirely (BLOCK_NONE only stops blocking but still scores). Since
# 2025-05 Google enabled ``OFF`` for ALL harm categories across models, and for
# gemini-2.5+ ``OFF`` is already the per-category default. We set it EXPLICITLY
# so older / non-2.5 models (whose default is BLOCK_MEDIUM_AND_ABOVE) get the
# same treatment — that mismatch is exactly what caused the silent research
# failures. Only the four universally-adjustable categories are listed;
# CIVIC_INTEGRITY is no longer filtered and the image/jailbreak categories are
# model-specific opt-INs, so listing them risks a 400 on models that lack them.
# Built-in core protections (e.g. child safety) are never adjustable and remain.
_LOWEST_SAFETY_SETTINGS: list[types.SafetySetting] = [
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=types.HarmBlockThreshold.OFF,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=types.HarmBlockThreshold.OFF,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=types.HarmBlockThreshold.OFF,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=types.HarmBlockThreshold.OFF,
    ),
]


# Child content-safety (WP13): the STRICTEST adjustable posture, used ONLY when
# the request is for a minor (``ctx.is_minor``). Mirror of _LOWEST_SAFETY_SETTINGS
# with every adjustable harm category flipped to BLOCK_LOW_AND_ABOVE — the
# opposite end of the same four categories, so it never trips a model-specific
# 400 the low posture wouldn't. Built-in child-safety protections are always on
# regardless; this hardens the adjustable layer on top.
_STRICT_MINOR_SAFETY_SETTINGS: list[types.SafetySetting] = [
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
]


def safety_settings_for_request() -> list[types.SafetySetting]:
    """The Google safety posture for the current request (WP13).

    Child content-safety output moderation for the TEXT/chat + image path: when
    the ONE ``ctx.is_minor`` flag is set, use the STRICT adjustable posture so
    Google blocks sexual / self-harm / graphic-violence output at generation
    time (streaming-native — no post-hoc buffering). Everyone else keeps the low
    posture that stops Gemini over-blocking legitimate content. Never raises — a
    missing context degrades to the low (adult) posture, never blocks all AI.
    """
    try:
        from matrx_ai.context.app_context import get_app_context

        if getattr(get_app_context(), "is_minor", False):
            return list(_STRICT_MINOR_SAFETY_SETTINGS)
    except Exception:  # noqa: BLE001 — no context ⇒ adult posture
        pass
    return list(_LOWEST_SAFETY_SETTINGS)


# ============================================================================
# GEMINI TRANSLATOR
# ============================================================================


class GoogleProviderConfig(TypedDict):
    """Type hint for Google API configuration dictionary"""

    model: str
    contents: list[Content]
    config: GenerateContentConfig


class GoogleTranslator(BaseTranslator):
    """Translates between unified format and Google Gemini API"""

    from google.genai import types

    def __init__(self, debug: bool = False):
        super().__init__(debug=debug)

    def _assemble_request(self, config: UnifiedConfig, route_ctx: Any = ""):
        return self.to_google(config, self.require_profile(route_ctx))

    def to_google(self, config: UnifiedConfig, profile: Any) -> GoogleProviderConfig:
        """
        Convert unified request to Google provider format efficiently.
        Combines to_gemini and generate_google_config into a single optimized method.

        This method does everything in ONE efficient pass:
        1. Processes messages and builds 'contents' array (from to_gemini)
        2. Directly builds types.GenerateContentConfig object (from generate_google_config)
        3. Returns both in the exact structure needed by execute()

        Param shaping (temperature / max_output_tokens / thinking_config) is
        DB-driven via ``profile.controls`` — the google_thinking (budget) vs
        google_thinking_3 (thinking_level, flash/pro family) dialects are the
        ``google_thinking`` processor's per-offering ``processor_config``, not
        api_class branches. TTS is a capability fact (audio out, no text out).

        Returns:
            Dict with:
                - contents: List of message contents in Google format
                - config: types.GenerateContentConfig object ready for API call
        """
        caps = profile.capabilities
        is_tts = caps.produces_audio and not caps.produces_text
        # ========================
        # STEP 1: Build contents (from messages)
        # ========================
        contents: list[Content] = []

        for msg in config.messages:
            google_content: Content | None = msg.to_google_content()
            if google_content:
                contents.append(google_content)

        # An empty `contents` is NEVER a valid Gemini request — the SDK raises a bare
        # ValueError('contents are required.') before any HTTP call, which then gets
        # misclassified as a retryable provider error and burns 2 paid retries. This
        # is always a request-CONSTRUCTION bug on our side (a message list that
        # filtered/sanitized down to nothing), so refuse it here, loudly, naming the
        # real cause — never send an empty request and blame Google for rejecting it.
        if not contents:
            vcprint(
                data={
                    "message_count": len(config.messages),
                    "model": getattr(config, "model", None),
                },
                title="🚨 Gemini request built with EMPTY contents — refusing to send",
                color="red",
            )
            raise ValueError(
                "Refusing to send a Gemini request with empty `contents`: the message "
                f"list ({len(config.messages)} message(s)) produced zero renderable "
                "contents. This is a request-construction bug (messages filtered or "
                "sanitized to nothing), not a Google failure."
            )

        # ========================
        # STEP 2: Build GenerateContentConfig directly
        # ========================
        try:
            # Build generation config kwargs
            generation_config_kwargs = {}

            # System instruction handling:
            # - Standard models: pass as system_instruction on the config object.
            # - TTS models: system_instruction is not supported — the directive is
            #   folded into the first user turn in the TTS block below, AFTER the
            #   speaker-label check runs. Folding it here instead would let the
            #   "Current date: …" preamble be scanned as a phantom speaker label
            #   and break multi-speaker speaker-name reconciliation.
            system_text = self.get_system_text(config)
            if system_text and not is_tts:
                generation_config_kwargs["system_instruction"] = system_text

            # DB-resolved params: temperature / max_output_tokens plus the
            # thinking_config fragment written by the ``google_thinking``
            # processor (mode legacy|gemini_3 + flash/pro family are
            # per-offering processor_config data).
            generation_config_kwargs.update(resolve_outbound_params(config, profile.controls))

            # TTS / Speech config
            if is_tts:
                # response_modalities is a Google implementation detail — always audio
                generation_config_kwargs["response_modalities"] = ["audio"]

                tts = config.tts_voice_config
                if tts and tts.is_configured:
                    # Reconcile + validate speaker labels against the PURE
                    # transcript: to_google() rewrites the script's labels to the
                    # configured speaker names. This MUST run before the system
                    # directive is folded in below — otherwise the "Current date:
                    # …" preamble is scanned as a phantom speaker label and the
                    # multi-speaker name check fails on a count mismatch.
                    speech_config = tts.to_google(contents)
                    if speech_config:
                        generation_config_kwargs["speech_config"] = speech_config

                # Google TTS has no system_instruction field — fold the directive
                # into the start of the user turn now that the speaker-name check
                # has run on the clean transcript. Chat-only decorations (the
                # "Current date: …" line, tools list, guidelines, context block)
                # were already stripped for this non-chat model at dispatch
                # (unified_client._strip_chat_decorations_if_non_fc, which runs on
                # EVERY path before to_google), so what get_system_text returns
                # here is the agent's own directive only.
                if system_text:
                    self._prepend_system_to_user_content(contents, system_text)

            # Response format — Gemini structured output. A raw JSON Schema normally
            # goes on ``response_json_schema`` (NOT ``response_schema``, which is the
            # OpenAPI-subset Schema type) and requires ``response_mime_type``.
            #
            # Google Search and streamed structured output are compatible on Gemini
            # 3.7 Flash. Re-verified 2026-08-17 with 12/12 genuinely grounded,
            # citation-heavy responses: every concatenated stream was complete JSON
            # and passed the requested schema. Keep the provider-native contract on
            # the same single call whether or not Search is enabled.
            if config.response_format and not is_tts:
                google_schema = self._build_google_response_schema(config.response_format)
                if google_schema is not None:
                    generation_config_kwargs["response_mime_type"] = "application/json"
                    generation_config_kwargs["response_json_schema"] = google_schema

            # Safety posture on every text + image generate_content call:
            # low for adults (Gemini over-blocks legitimate content), STRICT for
            # a minor (WP13 output moderation). TTS (audio-only) takes no
            # safety_settings — a no-op at best and a 400 at worst — so excluded.
            if not is_tts:
                generation_config_kwargs["safety_settings"] = safety_settings_for_request()

            # Create the config object
            generated_config: GenerateContentConfig = types.GenerateContentConfig(
                **generation_config_kwargs
            )

            # ========================
            # STEP 3: Process tools directly on config object
            # ========================
            # Tools that a model can't honour are stripped at the provider
            # boundary BEFORE this runs (unified_client._warn_and_strip_leaked_tools,
            # the loud fallback to the canonical request-prep gates). So for a
            # non-function-calling model config.tools is already empty here — no
            # per-provider tool guard is needed.
            raw_tools = self.build_provider_tools(config, "google")

            tools_list: list[Any] = []

            # Function / custom tools (the agent's own tools, context tools, …).
            if raw_tools:
                tools_list.extend(types.Tool(function_declarations=[tool]) for tool in raw_tools)

            # Built-in Google tools (Google Search grounding, URL context). On
            # Gemini 3 these ride ALONGSIDE function tools in the same request;
            # on Gemini 2.5/earlier that combination 400s, so we keep the
            # historical either/or there (built-ins only when there are no
            # function tools). "Gemini 3 generation" is read from the DATA: the
            # offering's thinking rule runs the google_thinking processor in
            # gemini_3 mode — exactly the Gemini-3 dialect marker.
            reasoning_rule = profile.controls.rule_for("reasoning_effort")
            supports_builtin_plus_function = (
                reasoning_rule.processor == "google_thinking"
                and reasoning_rule.processor_config.get("mode") == "gemini_3"
            )
            built_in_added = False
            if supports_builtin_plus_function or not raw_tools:
                if config.internal_url_context:
                    tools_list.append(types.Tool(url_context=types.UrlContext()))
                    built_in_added = True
                if config.internal_web_search:
                    tools_list.append(types.Tool(googleSearch=types.GoogleSearch()))
                    built_in_added = True

            if tools_list:
                generated_config.tools = tools_list
                # We do MANUAL function-calling: the SDK hands us the functionCall
                # parts and our orchestrator dispatches them. Tell the SDK so
                # explicitly. Two effects: (1) it skips the per-call "Tools at
                # indices [...] are not compatible with AFC" WARNING (it early-
                # returns in should_disable_afc before that log line), and (2) it
                # GUARANTEES the SDK never auto-executes a tool in a hidden loop —
                # the day a python callable ever slips into the tool list, AFC
                # being on-by-default would have it silently run, bypassing our
                # executor, persistence, and cost capture. disable=True only;
                # leave maximum_remote_calls unset (a positive value alongside
                # disable=True triggers a different SDK warning).
                generated_config.automatic_function_calling = types.AutomaticFunctionCallingConfig(
                    disable=True
                )

            # tool_config: the function-calling mode (when tool_choice is set) AND —
            # REQUIRED by Gemini when built-in tools ride ALONGSIDE function tools —
            # include_server_side_tool_invocations=True. Without that flag Google
            # rejects the mixed request: 400 "Please enable
            # tool_config.include_server_side_tool_invocations to use Built-in tools
            # with Function calling." (set even when tool_choice is unset).
            tool_config_kwargs: dict[str, Any] = {}
            if raw_tools and config.tool_choice:
                if config.tool_choice == "none":
                    mode = "NONE"
                elif config.tool_choice == "required":
                    mode = "ANY"
                else:
                    mode = "AUTO"
                tool_config_kwargs["function_calling_config"] = types.FunctionCallingConfig(
                    mode=mode
                )
            if raw_tools and built_in_added:
                tool_config_kwargs["include_server_side_tool_invocations"] = True
            if tool_config_kwargs:
                generated_config.tool_config = types.ToolConfig(**tool_config_kwargs)

        except Exception as e:
            vcprint(e, "Error in to_provider_config", color="red")
            raise

        # ========================
        # STEP 4: Return final structure
        # ========================
        return {
            "model": config.model,
            "contents": contents,
            "config": generated_config,
        }

    @staticmethod
    def _build_google_response_schema(
        response_format: Any,
    ) -> dict[str, Any] | None:
        """Extract the raw JSON Schema for Gemini's ``response_json_schema``.

        Gemini (https://ai.google.dev/gemini-api/docs/structured-output) accepts a
        standard JSON Schema via ``response_json_schema`` (paired with
        ``response_mime_type='application/json'``). This returns just the schema
        dict — the caller sets the mime type. ``response_schema`` (the OpenAPI
        subset) is intentionally NOT used.

        Returns ``None`` when no usable object-root schema is present. Gemini has
        no ``json_object`` fallback that enforces structure, so on ``None`` the
        caller omits the schema and the model falls back to prompt instructions.
        """
        if not isinstance(response_format, dict):
            return None

        fmt_type = response_format.get("type")
        # text / json_object have no Gemini schema equivalent — nothing to enforce.
        if fmt_type != "json_schema":
            return None

        # Locate the schema across the shapes response_format can arrive in: a
        # full OpenAI-style envelope ({name, schema, strict}), a raw JSON Schema
        # nested under json_schema, or a bare {"type":"json_schema"} placeholder.
        inner = response_format.get("json_schema")
        schema: dict[str, Any] | None = None
        if isinstance(inner, dict):
            if isinstance(inner.get("schema"), dict):
                schema = inner["schema"]
            elif {"type", "properties", "items"} & inner.keys():
                schema = inner  # inner IS the raw JSON Schema
        elif isinstance(response_format.get("schema"), dict):
            schema = response_format["schema"]

        # Gemini requires an object-root schema. No usable / non-object-root
        # schema → omit structured output. This is a runtime ADJUSTMENT (schema
        # NOT enforced) — log loudly so it's never mistaken for configured behaviour.
        downgrade_reason: str | None = None
        if not isinstance(schema, dict):
            downgrade_reason = "no JSON Schema was supplied with the json_schema request"
        elif not (
            schema.get("type") == "object"
            or (schema.get("type") is None and isinstance(schema.get("properties"), dict))
        ):
            downgrade_reason = (
                f"schema root is not an object (type={schema.get('type')!r}); "
                "Gemini requires an object root"
            )
        if downgrade_reason is not None:
            vcprint(
                data={
                    "provider": "google",
                    "requested": response_format,
                    "downgraded_to": "none (prompt-only)",
                    "reason": downgrade_reason,
                },
                title=(
                    "⚠️  GOOGLE ADJUSTMENT: structured output OMITTED — schema is "
                    "NOT enforced (prompt-only). Gemini has no json_object fallback. "
                    "The frontend should reject this; do NOT persist it as a saved config."
                ),
                color="yellow",
                verbose=True,
            )
            return None

        # Route through the shared per-provider seam for consistency with every
        # other structured-output boundary. Gemini's response_json_schema is
        # permissive — it accepts minItems/maxItems/pattern verbatim (the exact
        # shape that 400s Cerebras/Anthropic) — so "google" strips NOTHING today
        # and the rich schema is enforced in full. If a Gemini quirk ever
        # surfaces, one entry in unsupported_structured_output_keywords fixes it.
        sanitized = GoogleTranslator.sanitize_structured_output_schema(schema, "google")

        # THE ONE demonstrated Gemini quirk (2026-08-11): it does not honour
        # `const`. Measured on gemini-3.6-flash, 12 runs per cell against a
        # single-valued discriminator — `const` came back correct 1/12 (0/12
        # with Search grounding), `enum: [value]` 12/12. It is not a keyword to
        # STRIP (that would drop the constraint entirely) but one to REWRITE
        # into its identical-meaning form, so the constraint survives AND Gemini
        # enforces it. Request-boundary only: the stored schema keeps `const`,
        # which is the more precise keyword and is honoured as-is elsewhere.
        return rewrite_const_as_enum(sanitized)

    # ------------------------------------------------------------------
    # Image generation: Imagen 4 (dedicated text-only endpoint)
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # Image generation: Gemini 3.1 image (multimodal generate_content)
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # Internal helpers for media-ref → google.genai.types.Image conversion
    # ------------------------------------------------------------------

    def _extract_prompt(self, config: UnifiedConfig) -> str:
        """Pull the latest UN-TAGGED user TextContent — the main prompt.
        Skips role-tagged TextContent (negative_prompt, style_prompt, etc.)
        which the translator reads separately via pick_text_by_role."""
        from matrx_ai.config.message_config import pick_text_by_role

        prompt = pick_text_by_role(config.messages, None) or ""
        if not prompt and config.system_instruction:
            prompt = self.get_system_text(config) or ""
        return prompt

    @staticmethod
    def _iter_image_refs(config: UnifiedConfig):
        """Yield every MediaRef-shaped image input on UnifiedConfig in
        a stable order: image_input first, then image_inputs."""
        if config.image_input is not None:
            yield config.image_input
        yield from config.image_inputs or []

    @staticmethod
    def _mediaref_to_genai_image(ref: Any) -> Any | None:
        """Convert a MediaRef-shaped object (already resolved at the AI Dream
        boundary) into a ``google.genai.types.Image``.

        Returns None when the ref is missing or doesn't carry usable data.
        Resolution priority: ``base64_data`` → ``resolved_url`` → ``url``
        → ``file_uri`` (gs:// for Vertex).
        """
        if ref is None:
            return None

        # Plain dict shape (not the Pydantic MediaRef) — duck-type extraction.
        b64 = getattr(ref, "base64_data", None) or (
            ref.get("base64_data") if isinstance(ref, dict) else None
        )
        url = (
            getattr(ref, "resolved_url", None)
            or getattr(ref, "url", None)
            or (ref.get("resolved_url") or ref.get("url") if isinstance(ref, dict) else None)
        )
        file_uri = getattr(ref, "file_uri", None) or (
            ref.get("file_uri") if isinstance(ref, dict) else None
        )
        mime = (
            getattr(ref, "mime_type", None)
            or (ref.get("mime_type") if isinstance(ref, dict) else None)
            or "image/png"
        )

        if b64:
            import base64

            try:
                data = base64.b64decode(b64)
            except Exception:
                return None
            return types.Image(image_bytes=data, mime_type=mime)
        if file_uri and file_uri.startswith("gs://"):
            return types.Image(gcs_uri=file_uri, mime_type=mime)
        # No fallback URL fetch here — the AI Dream API boundary
        # (normalize_request_body) is responsible for pre-fetching bytes
        # via FileManager.resolve_media_async(..., needs_bytes=True). If
        # we get here without base64_data or a gs:// uri, the boundary
        # didn't run or its resolver failed — log loudly so the gap is
        # visible instead of silently degrading.
        from matrx_utils import vcprint

        vcprint(
            f"[google.translator] _mediaref_to_genai_image: ref carried url={url!r} "
            f"but no resolved base64_data — the boundary normalizer failed to pre-fetch. "
            f"Dropping this image.",
            color="red",
        )
        return None

    @staticmethod
    def _prepend_system_to_user_content(
        contents: list[dict],
        system_text: str,
    ) -> None:
        """Prepend system instruction text to the first user turn.

        Google TTS models do not support system_instruction on the config object.
        The only way to pass directive context is to include it at the start of
        the first user message, separated by a blank line so the model reads it
        as preamble rather than transcript content.

        Mutates `contents` in-place — no return value.
        """
        prefix = system_text.strip()
        if not prefix:
            return

        for content in contents:
            if not isinstance(content, dict) or content.get("role") != "user":
                continue
            parts = content.get("parts", [])
            for part in parts:
                if isinstance(part, dict) and part.get("text"):
                    part["text"] = prefix + "\n\n" + part["text"]
                    return
                elif hasattr(part, "text") and part.text:
                    # Wrap the types.Part — rebuild as dict so mutation is safe
                    part.text = prefix + "\n\n" + part.text
                    return
            # First user turn has no text parts yet — insert one at the front
            parts.insert(0, {"text": prefix})
            return

    @staticmethod
    def _scan_prompt_block(
        chunk: GenerateContentResponse,
        prior_reason: Any,
        prior_message: str | None,
    ) -> tuple[Any, str | None]:
        """Extract a prompt-level block reason from a chunk's prompt_feedback.

        Gemini reports an input-side safety block on ``prompt_feedback`` with no
        candidates. Returns ``(reason, message)`` — keeping the first non-empty
        values seen across the stream. Never raises (best-effort).
        """
        try:
            pf = getattr(chunk, "prompt_feedback", None)
            if pf is not None:
                reason = getattr(pf, "block_reason", None)
                if reason and not prior_reason:
                    return reason, getattr(pf, "block_reason_message", None)
        except Exception:
            pass
        return prior_reason, prior_message

    # Finish reasons that mean Google's safety / content filter blocked the
    # response. Our safety_settings are already at the lowest possible level
    # (every adjustable harm category = OFF), so anything here is a NON-adjustable
    # core protection or an input-side prompt block — a Google-side wall we cannot
    # lower on a standard Developer API key. We scream so it is impossible to miss.
    _SAFETY_FINISH_REASONS: frozenset[FinishReason] = frozenset(
        {
            FinishReason.SAFETY,
            FinishReason.CONTENT_FILTER,
            FinishReason.RECITATION,
            FinishReason.PROHIBITED_CONTENT,
            FinishReason.SPII,
            FinishReason.BLOCKLIST,
            FinishReason.IMAGE_SAFETY,
            FinishReason.IMAGE_PROHIBITED_CONTENT,
            FinishReason.IMAGE_RECITATION,
        }
    )

    @classmethod
    def _log_safety_block(
        cls,
        *,
        finish_reason: FinishReason | None,
        matrx_model_name: str,
        model_version: str | None,
        prompt_block_reason: Any = None,
        prompt_block_message: str | None = None,
    ) -> None:
        """Emit a LOUD RED banner whenever Google blocks a response on safety.

        Fires for both candidate-level safety finish reasons and prompt-level
        (input-side) blocks. Best-effort — never raises.
        """
        is_prompt_block = bool(prompt_block_reason)
        is_finish_block = finish_reason in cls._SAFETY_FINISH_REASONS
        if not (is_prompt_block or is_finish_block):
            return

        try:
            block_kind = "INPUT/PROMPT-LEVEL" if is_prompt_block else "OUTPUT/CANDIDATE-LEVEL"
            reason_detail = str(prompt_block_reason) if is_prompt_block else str(finish_reason)
            msg = prompt_block_message or "(no block_reason_message provided by Google)"
            banner = (
                "\n"
                "================================================================================\n"
                "🚨🚨🚨  GOOGLE SAFETY BLOCK  🚨🚨🚨\n"
                "================================================================================\n"
                f"  block kind     : {block_kind}\n"
                f"  reason         : {reason_detail}\n"
                f"  finish_reason  : {finish_reason}\n"
                f"  matrx model    : {matrx_model_name}\n"
                f"  provider model : {model_version}\n"
                f"  google message : {msg}\n"
                "--------------------------------------------------------------------------------\n"
                "  Our safety_settings are ALREADY at the lowest level (every adjustable harm\n"
                "  category = OFF). This block came from a NON-adjustable core protection or an\n"
                "  input-side prompt filter — Google will not let us lower it on a standard\n"
                "  Developer API key. Consider routing this agent to another provider (OpenAI).\n"
                "================================================================================\n"
            )
            vcprint(banner, color="red")
        except Exception:
            pass

    async def from_google_async(
        self,
        chunks: list[GenerateContentResponse],
        matrx_model_name: str,
        audio_format: str | None = None,
    ) -> UnifiedResponse:
        """The ONE Google response → ``UnifiedResponse`` conversion.

        Uses the async ``from_google_async`` classmethods on AudioContent /
        ImageContent / VideoContent for inline media so:
          - The persisted cld_files row has file_id / file_uri /
            size_bytes / probed dims populated
          - SOCIAL_BASELINE + kind-specific variants render automatically
          - ``metadata.generation`` is stamped
          - The returned content carries file_id (so
            _emit_media_from_response on the Google API caller side
            emits ``origin: "matrx"`` blocks with all URL flavours)

        Closes the last "external origin audio" surface. Every Google API
        caller is async, so this is the only conversion there is — the sync
        twin that persisted media URL-only (no ``file_id``) is deleted.
        """
        content = []
        all_candidates = []
        usage_metadata = None
        # One entry per PROVIDER CALL in this chunk list. Segmented TTS
        # concatenates the chunks of N separate Gemini calls into one list
        # (each call's final chunk carries that call's usage_metadata) —
        # keeping only the last one under-recorded every multi-segment
        # episode's cost to ~one segment (found 2026-08-10: a full podcast
        # billed as 131 input tokens). Single-call streams contribute exactly
        # one entry, so the summed path is identical for them.
        segment_usages: list[Any] = []
        finish_reason = None
        accumulated_text = ""
        google_thought_signature = None
        grounding_metadata = None
        model_version = None
        response_id = None
        last_chunk = None
        # Streaming TTS yields the audio as many raw-PCM segments across chunks.
        # They are pieces of ONE render — concatenate them and persist a single
        # file after the loop. Saving each segment separately produced N
        # truncated files (the latent multi-chunk bug).
        audio_pcm_segments: list[bytes] = []
        audio_raw_mime: str | None = None
        prompt_block_reason = None  # prompt-level safety block (no candidates)
        prompt_block_message = None

        for chunk in chunks:
            prompt_block_reason, prompt_block_message = self._scan_prompt_block(
                chunk, prompt_block_reason, prompt_block_message
            )
            if chunk.candidates:
                for cand in chunk.candidates:
                    all_candidates.append(cand)
                    if cand.finish_reason:
                        finish_reason = FinishReason.from_google(cand.finish_reason)
                        if chunk.usage_metadata is not None and (
                            not segment_usages or segment_usages[-1] is not chunk.usage_metadata
                        ):
                            segment_usages.append(chunk.usage_metadata)
                        usage_metadata = chunk.usage_metadata
                        model_version = chunk.model_version
                        response_id = chunk.response_id
                        last_chunk = chunk

                    if cand.grounding_metadata:
                        grounding_metadata = cand.grounding_metadata

                    if cand.content and cand.content.parts:
                        for part in cand.content.parts:
                            part: Part

                            if part.thought:
                                content.append(ThinkingContent.from_google(part))
                            elif part.text:
                                accumulated_text += part.text
                                if part.thought_signature:
                                    google_thought_signature = part.thought_signature
                            elif part.function_call:
                                content.append(ToolCallContent.from_google(part))
                            elif part.function_response:
                                content.append(ToolResultContent.from_google(part))
                            elif part.executable_code:
                                content.append(CodeExecutionContent.from_google(part))
                            elif part.code_execution_result:
                                content.append(CodeExecutionResultContent.from_google(part))
                            elif part.inline_data:
                                # Phase 2c — async envelope path for inline media.
                                mime = (part.inline_data.mime_type or "").lower()
                                if mime.startswith("audio/"):
                                    # Defer: collect the raw PCM segment and save
                                    # one concatenated file after the loop.
                                    audio_pcm_segments.append(part.inline_data.data)
                                    audio_raw_mime = part.inline_data.mime_type or audio_raw_mime
                                    converted = None
                                elif mime.startswith("image/"):
                                    converted = await ImageContent.from_google_async(part)
                                elif mime.startswith("video/"):
                                    converted = await VideoContent.from_google_async(part)
                                else:
                                    # Every branch is the ENVELOPE path: inline bytes
                                    # must come back with a file_id. A sync classmethod
                                    # here would persist a signed url with no identity
                                    # into chat.message.
                                    converted = (
                                        (await DocumentContent.from_google_async(part))
                                        or (await ImageContent.from_google_async(part))
                                        or (
                                            await AudioContent.from_google_async(
                                                part, audio_format=audio_format
                                            )
                                        )
                                        or (await VideoContent.from_google_async(part))
                                    )
                                if converted:
                                    content.append(converted)

                            elif part.file_data:
                                # file_data references are external URIs — no envelope
                                # needed; sync classmethods handle them correctly.
                                converted = (
                                    YouTubeVideoContent.from_google(part)
                                    or ImageContent.from_google(part)
                                    or AudioContent.from_google(part)
                                    or VideoContent.from_google(part)
                                    or DocumentContent.from_google(part)
                                )
                                if converted:
                                    content.append(converted)

                            elif part.thought_signature:
                                content.append(ThinkingContent.from_google(part))

        if audio_pcm_segments:
            # One render → one concatenated file (fixes the per-segment
            # multi-file bug for any multi-chunk TTS stream).
            audio_item = await AudioContent.from_raw_audio_async(
                b"".join(audio_pcm_segments),
                audio_raw_mime or "audio/L16",
                audio_format=audio_format,
            )
            if audio_item:
                content.append(audio_item)

        # Prompt-level safety block (no candidates): map the block reason to a
        # finish_reason so the orchestrator captures it rather than silently
        # returning an empty response.
        if finish_reason is None and prompt_block_reason:
            finish_reason = FinishReason.from_google(prompt_block_reason)

        self._log_safety_block(
            finish_reason=finish_reason,
            matrx_model_name=matrx_model_name,
            model_version=model_version,
            prompt_block_reason=prompt_block_reason,
            prompt_block_message=prompt_block_message,
        )

        if accumulated_text:
            metadata = {}
            if google_thought_signature:
                metadata["google_thought_signature"] = google_thought_signature
            if grounding_metadata:
                # Raw grounding_metadata kept for existing consumers; the
                # canonical cross-provider shape lives in metadata["citations"].
                metadata["grounding_metadata"] = grounding_metadata
                normalized = normalize_google_grounding(grounding_metadata, accumulated_text)
                if normalized:
                    metadata["citations"] = [c.model_dump(exclude_none=True) for c in normalized]
            content.append(TextContent(text=accumulated_text, metadata=metadata))

        messages = []
        if content:
            messages.append(
                UnifiedMessage(
                    role="assistant",
                    content=content,
                    metadata={"finish_reason": finish_reason},
                )
            )

        token_usage = None
        if usage_metadata:
            token_usage = TokenUsage.from_gemini(
                usage_metadata,
                matrx_model_name=matrx_model_name,
                provider_model_name=model_version,
                response_id=response_id,
            )
            if len(segment_usages) > 1:
                # Segmented TTS: this chunk list holds N provider calls' worth
                # of billed work — sum every call's usage instead of recording
                # only the final segment's (a full episode once billed as 131
                # input tokens). raw_usage keeps the last segment's verbatim
                # block; the call count is recorded beside it.
                token_usage.input_tokens = sum(u.prompt_token_count or 0 for u in segment_usages)
                token_usage.output_tokens = sum(
                    u.candidates_token_count or 0 for u in segment_usages
                )
                token_usage.cached_input_tokens = sum(
                    u.cached_content_token_count or 0 for u in segment_usages
                )
                token_usage.metadata["segmented_provider_calls"] = len(segment_usages)
        else:
            vcprint(
                f"⚠️  WARNING: Gemini response missing usage metadata for model {model_version}",
                color="red",
            )

        raw_response = last_chunk
        if last_chunk is not None:
            last_chunk.candidates = all_candidates

        return UnifiedResponse(
            messages=messages,
            usage=token_usage,
            finish_reason=finish_reason,
            raw_response=raw_response,
        )
