from __future__ import annotations

import asyncio
import json
from typing import TYPE_CHECKING, Any

from groq import AsyncGroq
from matrx_connect.context.events import InfoPayload
from matrx_utils import vcprint

from matrx_ai.config import (
    AudioContent,
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

from .translator import GroqTranslator

if TYPE_CHECKING:  # circular-by-design: catalog.models imports providers.resolved_capabilities
    from matrx_ai.catalog.models import ResolvedCallProfile

DEBUG_OVERRIDE = False

class GroqChat:
    """Groq API-specific endpoint implementation (OpenAI-style)."""

    endpoint_name: str
    debug: bool

    # Memoized on the RESOLVED KEY VALUE — a host-side key rotation builds a
    # fresh SDK client on the next request (no process restart).
    client = keyed_provider_client(
        "GROQ_API_KEY",
        factory=lambda api_key: AsyncGroq(
            api_key=api_key,
            http_client=make_capture_http_client(),
        ),
    )

    def __init__(self, debug: bool = False):
        self.endpoint_name = "[GROQ CHAT]"
        self.translator = GroqTranslator(debug=debug)
        self.debug = debug

        if DEBUG_OVERRIDE:
            self.debug = True

    def to_provider_config(
        self, config: UnifiedConfig, profile: ResolvedCallProfile
    ) -> dict[str, Any]:
        return self.translator.build_request(config, profile)

    def to_unified_response(self, response: Any, model: str = "") -> UnifiedResponse:
        """Convert Groq response to unified format"""
        return self.translator.from_groq(response)

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

        vcprint(f"[Groq Chat] executing wire={profile.wire_format}", color="blue")

        try:
            # TTS is a capability fact (audio out, no text out) — never a name
            # or api_class probe. Mirrors translate_request's speech predicate.
            caps = profile.capabilities
            if caps.produces_audio and not caps.produces_text:
                return await self._execute_tts(unified_config, profile, emitter, unified_config.model)

            # Build provider-specific config
            config_data = self.to_provider_config(unified_config, profile)
            capture_request_payload(
                config_data,
                provider="groq",
                wire_format=profile.wire_format,
                debug=debug,
            )
            stamp_call_meta(
                provider="groq",
                model=unified_config.model,
                is_streaming=bool(config_data.get("stream", False)),
            )

            vcprint(config_data, "Groq API Config Data", color="blue", verbose=debug)

            if config_data.get("stream", False):
                return await self._execute_streaming(
                    config_data, emitter, unified_config.model
                )
            else:
                return await self._execute_non_streaming(
                    config_data, emitter, unified_config.model
                )

        except Exception as e:
            if getattr(e, "error_info", None) is not None:
                raise

            from matrx_ai.providers.errors import classify_provider_error

            error_info = classify_provider_error("groq", e)
            e.error_info = error_info
            raise

    async def _execute_tts(
        self,
        unified_config: UnifiedConfig,
        profile: ResolvedCallProfile,
        emitter: Emitter,
        matrx_model_name: str,
    ) -> UnifiedResponse:
        """Execute Groq Orpheus TTS via client.audio.speech.create."""
        from matrx_ai.catalog.resolve import resolve_tts_voice
        from matrx_ai.config.dictionary_config import apply_tts_dictionary
        from matrx_ai.config.tts_config import GroqTTSRegistry

        tts = unified_config.tts_voice_config
        model = profile.provider_model_id
        voice = resolve_tts_voice(profile, tts._primary_voice() if tts else None)

        # Groq Orpheus only supports wav
        audio_format = GroqTTSRegistry.resolve_format(unified_config.audio_format)
        mime_type = "audio/wav"

        # Extract input text
        text_parts: list[str] = []
        for msg in unified_config.messages:
            if hasattr(msg, "content"):
                for c in msg.content:
                    if hasattr(c, "text") and c.text:
                        text_parts.append(c.text)
        raw_text = " ".join(text_parts).strip() or "."

        # Multi-speaker configs collapse to a single voice for Groq.
        # Strip speaker labels (e.g. "Alex: ") so they aren't read aloud.
        if tts:
            raw_text = tts.strip_speaker_labels(raw_text)

        # Custom Dictionary pronunciation floor — Orpheus is plain-text only with
        # no native pronunciation channel. Substitute respellings BEFORE the
        # 200-char validation, since substitution can lengthen the text.
        # See docs/dictionary/providers/groq.md.
        raw_text = apply_tts_dictionary(
            unified_config.dictionary, raw_text, provider="groq", model=model
        )

        input_text = GroqTTSRegistry.validate_input_length(raw_text)

        vcprint(f"[Groq TTS] model={model} voice={voice} format={audio_format}", color="blue")

        stamp_call_meta(provider="groq", model=matrx_model_name, is_streaming=False)
        response = await self.client.audio.speech.create(
            model=model,
            voice=voice,
            input=input_text,
            response_format=audio_format,
        )

        # groq-sdk >=1 returns AsyncBinaryAPIResponse. Its bytes are exposed by
        # the async read() contract; `.content` belonged to the older wrapper.
        audio_bytes = await response.read()

        # Phase 2c — envelope path so the FE gets file_id +
        # durable URLs + canonical MediaGenerationMetadata.
        from matrx_ai.media import save_media_envelope_async
        from matrx_ai.media.generation_metadata import map_tts_audio_response

        gen_meta = map_tts_audio_response(
            provider="groq", model=model, prompt=input_text[:4096],
            voice=voice, audio_format=audio_format,
        )
        envelope = await save_media_envelope_async(
            content=audio_bytes,
            mime_type=mime_type,
            audio_format=audio_format,
            prompt=input_text,
            model=model,
            provider="groq",
            feature="ai_audio",
            extra_metadata={"generation": gen_meta.model_dump(exclude_none=True)},
        )

        audio_content = AudioContent(
            url=envelope.url,
            file_id=envelope.file_id,
            mime_type=mime_type,
            file_size=envelope.size_bytes,
            duration_ms=envelope.duration_ms,
            metadata={"generation": gen_meta.model_dump(exclude_none=True)},
        )
        msg = UnifiedMessage(role="assistant", content=[audio_content])

        # Bill by characters actually sent (post-dictionary) — the speech
        # endpoint returns raw bytes with no usage object. See
        # build_character_billed_usage for the basis-aware contract.
        from matrx_ai.config.usage_config import build_character_billed_usage_async

        usage = await build_character_billed_usage_async(
            characters=len(input_text),
            matrx_model_name=matrx_model_name,
            provider_model_name=model,
            api="groq",
        )

        unified_response = UnifiedResponse(messages=[msg], usage=usage)

        from matrx_connect.context.data_types import MediaBlockData
        from matrx_connect.context.media_block import cloud_file_to_media_block
        synthetic_record = {
            "id": envelope.file_id,
            "storage_uri": envelope.storage_uri,
            "file_path": envelope.file_path,
            "file_name": envelope.file_name,
            "mime_type": envelope.mime_type or mime_type,
            "size_bytes": envelope.size_bytes,
            "visibility": envelope.visibility,
            "duration_ms": envelope.duration_ms,
            "metadata": {"generation": gen_meta.model_dump(exclude_none=True)},
        }
        url_set = {
            "url": envelope.url, "cdn_url": envelope.cdn_url,
            "download_url": envelope.download_url,
        }
        await emitter.send_data(MediaBlockData(
            block=cloud_file_to_media_block(
                synthetic_record, url_set=url_set, kind_override="audio",
            )
        ))
        await asyncio.sleep(0)

        return unified_response

    async def _execute_non_streaming(
        self,
        config_data: dict[str, Any],
        emitter: Emitter,
        model: str,
    ) -> UnifiedResponse:
        """Execute non-streaming Groq request"""

        vcprint("[Groq] Starting API call (non-streaming)...", color="cyan")

        # Native async API call
        response = await self.client.chat.completions.create(**config_data)

        vcprint("[Groq] API call completed, processing response...", color="cyan")
        vcprint(response, "Groq Response", color="green", verbose=self.debug)

        # Convert to unified format first
        vcprint("[Groq] Converting to unified format...", color="cyan")
        converted_response = self.to_unified_response(response, model)
        vcprint(
            f"[Groq] Conversion complete. {len(converted_response.messages)} messages",
            color="cyan",
        )

        # Send content through emitter
        vcprint("[Groq] Sending content to stream handler...", color="cyan")
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

        # Citations captured by the translator onto text blocks — emit the
        # typed events at settle.
        from matrx_ai.providers.citation_emit import emit_citations_from_response

        await emit_citations_from_response(converted_response, emitter, "GROQ")

        vcprint("[Groq] Non-streaming execution completed successfully", color="green")
        return converted_response

    async def _execute_streaming(
        self,
        config_data: dict[str, Any],
        emitter: Emitter,
        model: str,
    ) -> UnifiedResponse:
        """Execute streaming Groq request"""

        vcprint("[Groq] Starting API call (streaming)...", color="cyan")

        # Native async streaming
        stream = await self.client.chat.completions.create(**config_data)

        vcprint(
            "[Groq] Stream connection established, processing chunks...", color="cyan"
        )

        # Accumulate response data for final unified response
        accumulated_content = ""
        accumulated_reasoning = ""
        in_think_block = False
        accumulated_tool_calls = []
        accumulated_annotations: list[Any] = []
        usage_data = None
        finish_reason = None
        response_id = None

        # Process stream chunks
        from matrx_ai.providers.errors import stream_with_billed_usage

        async for chunk in stream_with_billed_usage(stream, model=model, api="groq"):
            response_id = chunk.id

            if not chunk.choices:
                if chunk.usage:
                    usage_data = chunk.usage
                continue

            choice = chunk.choices[0]
            delta = choice.delta

            # Citation annotations (document_citation / function_citation)
            # arrive on deltas — collect for settle-time normalization.
            delta_annotations = getattr(delta, "annotations", None)
            if delta_annotations:
                accumulated_annotations.extend(delta_annotations)

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
                if in_think_block:
                    await emitter.send_chunk("\n</reasoning>\n")
                    await emitter.send_reasoning_state("stopped")
                    in_think_block = False
                accumulated_content += delta.content
                await emitter.send_chunk(delta.content)
                await asyncio.sleep(0)

            # Handle tool calls
            if getattr(delta, "tool_calls", None):
                for tc in delta.tool_calls:
                    while len(accumulated_tool_calls) <= tc.index:
                        accumulated_tool_calls.append(
                            {"id": "", "name": "", "arguments": ""}
                        )

                    if tc.id:
                        accumulated_tool_calls[tc.index]["id"] = tc.id
                    if tc.function.name:
                        accumulated_tool_calls[tc.index]["name"] = tc.function.name
                    if tc.function.arguments:
                        accumulated_tool_calls[tc.index]["arguments"] += (
                            tc.function.arguments
                        )

            # Capture finish reason
            if choice.finish_reason:
                finish_reason = choice.finish_reason

            # Capture usage from final chunk
            if chunk.usage:
                usage_data = chunk.usage

        if in_think_block:
            await emitter.send_chunk("\n</reasoning>")
            await emitter.send_reasoning_state("stopped")

        # Build unified response from accumulated data
        content = []

        if accumulated_reasoning:
            content.append(ThinkingContent(text=accumulated_reasoning, provider="groq"))
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

        # Settle-time citation capture — mirror from_groq: normalize the
        # accumulated delta annotations onto the text block's
        # metadata["citations"]. Guarded: malformed citations never abort.
        if accumulated_annotations:
            try:
                from matrx_ai.config.citations import normalize_openai_compatible_citations

                groq_citations = normalize_openai_compatible_citations(
                    None, {"annotations": accumulated_annotations}, accumulated_content
                )
                if groq_citations:
                    normalized_dicts = [
                        c.model_dump(exclude_none=True) for c in groq_citations
                    ]
                    for block in content:
                        if isinstance(block, TextContent):
                            block.metadata.setdefault("citations", normalized_dicts)
            except Exception as citation_exc:
                vcprint(
                    f"[Groq] citation capture failed — skipping citations only "
                    f"(answer unaffected): {citation_exc}",
                    color="red",
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
                api="groq",
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

        vcprint("[Groq] Streaming execution completed successfully", color="green")

        unified_response = UnifiedResponse(
            messages=messages,
            usage=token_usage,
            finish_reason=unified_finish_reason,
            stop_reason=finish_reason,
        )

        # Emit the typed citation events at settle (annotations only arrive on
        # the terminal deltas).
        from matrx_ai.providers.citation_emit import emit_citations_from_response

        await emit_citations_from_response(unified_response, emitter, "GROQ")

        return unified_response
