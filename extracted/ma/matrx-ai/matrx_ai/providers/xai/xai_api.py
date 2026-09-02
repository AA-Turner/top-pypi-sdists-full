from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any

import xai_sdk
from matrx_connect.context.events import InfoPayload
from matrx_utils import vcprint

from matrx_ai.config import (
    AudioContent,
    TextContent,
    ThinkingContent,
    TokenUsage,
    ToolCallContent,
    UnifiedConfig,
    UnifiedMessage,
    UnifiedResponse,
)
from matrx_ai.context.emitter_protocol import Emitter
from matrx_ai.providers.keys import keyed_provider_client, resolve_api_key
from matrx_ai.providers.outbound_capture import (
    make_capture_http_client,
    stamp_call_meta,
)
from matrx_ai.providers.reasoning import emit_complete_reasoning_block
from matrx_ai.providers.snapshot import capture_request_payload

from .translator import XAITranslator

if TYPE_CHECKING:  # circular-by-design: catalog.models imports providers.resolved_capabilities
    from matrx_ai.catalog.models import ResolvedCallProfile

DEBUG_OVERRIDE = False


class XAIChat:
    """xAI Grok chat endpoint — native ``xai_sdk.AsyncClient`` (gRPC).

    Mirrors the image/video providers' lazy-client pattern. Using the native
    SDK (rather than the OpenAI-compatible shim) is what unlocks first-class
    ``reasoning_effort`` and the server-side ``web_search()`` / ``x_search()``
    tools. TTS keeps its own dedicated httpx endpoint (``_execute_tts``).
    """

    endpoint_name: str
    debug: bool

    def __init__(self, debug: bool = False):
        self.endpoint_name = "[XAI CHAT]"
        self.translator = XAITranslator(debug=debug)
        self.debug = debug
        # Tracks whether we've emitted the content-less "reasoning started"
        # signal for the current stream but not yet "stopped".
        self._reasoning_signaled = False

        if DEBUG_OVERRIDE:
            self.debug = True

    # Built lazily on first ACCESS (grpc.aio needs a running event loop, so
    # never at import/__init__ time) and memoized on the RESOLVED KEY VALUE —
    # a host-side key rotation builds a fresh SDK client on the next request.
    client = keyed_provider_client(
        "XAI_API_KEY",
        factory=lambda api_key: xai_sdk.AsyncClient(api_key=api_key),
    )

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

        vcprint(f"[xAI Chat] executing wire={profile.wire_format}", color="blue")

        try:
            # TTS is a capability fact (audio out, no text out) — never a name
            # or api_class probe. Mirrors translate_request's speech predicate.
            caps = profile.capabilities
            if caps.produces_audio and not caps.produces_text:
                return await self._execute_tts(unified_config, profile, emitter, unified_config.model)

            # Build native xai_sdk create() kwargs (proto objects inside).
            create_kwargs = self.translator.build_request(unified_config, profile)

            debug_summary = self.translator.debug_summary(create_kwargs)
            capture_request_payload(
                debug_summary,
                provider="xai",
                wire_format=profile.wire_format,
                debug=debug,
            )
            stamp_call_meta(
                provider="xai",
                model=unified_config.model,
                is_streaming=bool(unified_config.stream),
            )
            vcprint(debug_summary, "xAI API Config Data", color="blue", verbose=debug)

            chat = self.client.chat.create(**create_kwargs)

            if unified_config.stream:
                return await self._execute_streaming(chat, emitter, unified_config.model)
            else:
                return await self._execute_non_streaming(chat, emitter, unified_config.model)

        except Exception as e:
            if getattr(e, "error_info", None) is not None:
                raise

            from matrx_ai.providers.errors import classify_xai_error

            error_info = classify_xai_error(e)
            e.error_info = error_info
            raise

    async def _execute_tts(
        self,
        unified_config: UnifiedConfig,
        profile: ResolvedCallProfile,
        emitter: Emitter,
        matrx_model_name: str,
    ) -> UnifiedResponse:
        """Execute xAI TTS via POST https://api.x.ai/v1/tts.

        xAI TTS uses a dedicated endpoint incompatible with the OpenAI-style
        client.audio.speech.create — we call it directly via httpx.
        """
        from matrx_ai.catalog.resolve import resolve_tts_voice
        from matrx_ai.config.dictionary_config import apply_tts_dictionary
        from matrx_ai.config.tts_config import XAITTSRegistry

        tts = unified_config.tts_voice_config
        voice = resolve_tts_voice(profile, tts._primary_voice() if tts else None)

        # audio_format → codec
        codec = XAITTSRegistry.resolve_codec(unified_config.audio_format)
        output_format = XAITTSRegistry.resolve_output_format(codec=codec)

        # Extract input text
        text_parts: list[str] = []
        for msg in unified_config.messages:
            if hasattr(msg, "content"):
                for c in msg.content:
                    if hasattr(c, "text") and c.text:
                        text_parts.append(c.text)
        raw_text = " ".join(text_parts).strip() or "."

        # Multi-speaker configs collapse to a single voice for xAI.
        # Strip speaker labels (e.g. "Alex: ") so they aren't read aloud.
        if tts:
            raw_text = tts.strip_speaker_labels(raw_text)

        # Custom Dictionary pronunciation floor — xAI Grok TTS has no native
        # pronunciation channel (no SSML/phoneme/lexicon), so substitute
        # respellings before length validation. See docs/dictionary/providers/xai.md.
        raw_text = apply_tts_dictionary(
            unified_config.dictionary, raw_text, provider="xai", model=matrx_model_name
        )

        input_text = XAITTSRegistry.validate_text_length(raw_text, truncate=True)

        api_key = resolve_api_key("XAI_API_KEY") or ""
        payload: dict[str, Any] = {
            "text": input_text,
            "voice_id": voice,
            "language": "en",
            "output_format": output_format,
        }

        vcprint(f"[xAI TTS] voice={voice} codec={codec}", color="blue")

        stamp_call_meta(provider="xai", model=matrx_model_name, is_streaming=False)
        async with make_capture_http_client(timeout=120.0) as http:
            resp = await http.post(
                "https://api.x.ai/v1/tts",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            resp.raise_for_status()
            audio_bytes = resp.content

        codec_to_mime = {
            "mp3": "audio/mpeg",
            "wav": "audio/wav",
            "pcm": "audio/pcm",
            "mulaw": "audio/basic",
            "alaw": "audio/alaw",
        }
        mime_type = codec_to_mime.get(codec, "audio/mpeg")

        # Phase 2c — envelope path so the FE gets file_id +
        # durable URLs + canonical MediaGenerationMetadata.
        from matrx_ai.media import save_media_envelope_async
        from matrx_ai.media.generation_metadata import map_tts_audio_response

        gen_meta = map_tts_audio_response(
            provider="xai", model=profile.provider_model_id,
            prompt=input_text[:4096], voice=voice, audio_format=codec,
            extra={"language": "en"},
        )
        envelope = await save_media_envelope_async(
            content=audio_bytes,
            mime_type=mime_type,
            audio_format=codec,
            prompt=input_text,
            model=profile.provider_model_id,
            provider="xai",
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

        # Bill by characters actually sent (post-dictionary) — the TTS endpoint
        # returns raw bytes with no usage object. See
        # build_character_billed_usage for the basis-aware contract.
        from matrx_ai.config.usage_config import build_character_billed_usage_async

        usage = await build_character_billed_usage_async(
            characters=len(input_text),
            matrx_model_name=matrx_model_name,
            provider_model_name=profile.provider_model_id,
            api="xai",
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
        chat: Any,
        emitter: Emitter,
        model: str,
    ) -> UnifiedResponse:
        """Execute a non-streaming native xAI request."""

        vcprint("[xAI] Starting API call (non-streaming)...", color="cyan")

        response = await chat.sample()

        vcprint("[xAI] API call completed, processing response...", color="cyan")
        vcprint(response.content, "xAI Response", color="green", verbose=self.debug)

        converted_response = self.translator.from_xai(response)

        # xAI delivers citations only on the settled response (web_search /
        # x_search URL list) — emit the normalized citations now, mirroring
        # Google's settle-time pattern.
        from matrx_ai.providers.citation_emit import emit_citations_from_response

        await emit_citations_from_response(converted_response, emitter, "XAI")

        # Emit content (non-streaming has no live deltas, so push it now).
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

        vcprint("[xAI] Non-streaming execution completed successfully", color="green")
        return converted_response

    @staticmethod
    def _billed_usage_from_response(final_response: Any) -> TokenUsage | None:
        """Extract billed TokenUsage from a (possibly partial) streamed xAI
        response — same shape ``from_xai`` records on success, but touching ONLY
        the usage fields so it stays valid on a mid-stream response whose
        messages/tool_calls are incomplete. Returns None when no usage is
        present yet (nothing was billed)."""
        if final_response is None:
            return None
        usage = getattr(final_response, "usage", None)
        if usage is None or not getattr(usage, "total_tokens", 0):
            return None
        proto = getattr(final_response, "proto", None)
        model_name = getattr(proto, "model", None)
        from matrx_ai.config import serialize_provider_usage
        from matrx_ai.providers.xai.translator import provider_charge_from_xai_usage
        return TokenUsage(
            input_tokens=getattr(usage, "prompt_tokens", 0),
            output_tokens=getattr(usage, "completion_tokens", 0),
            matrx_model_name=model_name,
            provider_model_name=model_name,
            api="xai",
            response_id=getattr(final_response, "id", None),
            raw_usage=serialize_provider_usage(usage),
            provider_charge=provider_charge_from_xai_usage(usage),
        )

    def _attach_billed_usage(self, exc: BaseException, final_response: Any) -> None:
        """Stamp xAI-billed token usage from a (possibly partial) streamed
        response onto a raised/cancelling exception, so a mid-flight failure
        records real cost instead of cost=0. Fully best-effort — cost capture
        must never mask the real error."""
        # LAYER 2: the mark means "an adapter LOOKED", which is true even when
        # there is nothing to attach — it must precede every early return.
        from matrx_ai.providers.errors import mark_billing_checked

        mark_billing_checked(exc)
        try:
            from matrx_ai.providers.errors import attach_billed_usage

            attach_billed_usage(exc, self._billed_usage_from_response(final_response))
        except Exception:
            pass

    async def _execute_streaming(
        self,
        chat: Any,
        emitter: Emitter,
        model: str,
    ) -> UnifiedResponse:
        """Execute a streaming native xAI request.

        ``chat.stream()`` yields ``(response, chunk)`` where ``response`` is the
        accumulating full object. We emit ``chunk.content`` live and build the
        final UnifiedResponse from the terminal ``response`` (full tool_calls /
        usage / finish_reason / citations) via the shared ``from_xai``.
        """

        vcprint("[xAI] Starting API call (streaming)...", color="cyan")

        final_response = None
        self._reasoning_signaled = False
        try:
            async for response, chunk in chat.stream():
                final_response = response
                # Reasoning signal (best-effort): on reasoning models the
                # accumulating response exposes reasoning_content, which grows
                # during thinking BEFORE any answer content. Emit the
                # content-less "started" the first time we see it — this is the
                # only live evidence xAI gives that the model is thinking. A
                # no-op on non-reasoning models (reasoning_content stays empty).
                reasoning = getattr(response, "reasoning_content", None)
                if reasoning and not self._reasoning_signaled:
                    self._reasoning_signaled = True
                    await emitter.send_reasoning_state("started")
                delta = chunk.content
                if delta:
                    # First answer token — reasoning is over.
                    if self._reasoning_signaled:
                        self._reasoning_signaled = False
                        await emitter.send_reasoning_state("stopped")
                    await emitter.send_chunk(delta)
                    await asyncio.sleep(0)
        except BaseException as exc:
            # The stream raised AFTER xAI has already billed us for the tokens
            # generated so far (safety block mid-stream, network drop, client
            # disconnect -> CancelledError, shutdown). Stamp the billed usage onto
            # the exception so the orchestrator's failure finalizer records real
            # cost instead of cost=0. Best-effort: never let cost capture mask the
            # real error (attach_billed_usage swallows attribute-set failures and
            # is a no-op on None usage).
            self._attach_billed_usage(exc, final_response)
            raise

        vcprint("[xAI] Stream complete, building unified response...", color="cyan")

        # Safety net: close an outstanding reasoning signal (e.g. a turn that
        # reasoned then went straight to a tool call with no answer content).
        if self._reasoning_signaled:
            self._reasoning_signaled = False
            await emitter.send_reasoning_state("stopped")

        if final_response is None:
            return UnifiedResponse(messages=[])

        converted = self.translator.from_xai(final_response)

        # Citations exist only on the terminal accumulated response (xAI emits
        # no live citation deltas, by provider design) — this settle-time
        # emission is the earliest possible point, same as Google grounding.
        from matrx_ai.providers.citation_emit import emit_citations_from_response

        await emit_citations_from_response(converted, emitter, "XAI")

        # Surface tool-call intent the same way the non-streaming path does.
        for message in converted.messages:
            for content in message.content:
                if isinstance(content, ToolCallContent):
                    await emitter.send_info(InfoPayload(
                        code="tool_processing",
                        system_message=f"Executing {content.name}",
                        user_message=f"Using tool {content.name}",
                        metadata={"tool_call": content.name},
                    ))

        vcprint("[xAI] Streaming execution completed successfully", color="green")
        return converted
