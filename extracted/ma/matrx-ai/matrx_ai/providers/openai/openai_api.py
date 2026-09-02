from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any

import rich
from matrx_connect.context.events import CitationPayload
from matrx_utils import vcprint
from openai import AsyncOpenAI
from openai.types.responses import Response as OpenAIResponse

from matrx_ai.config import (
    AudioContent,
    TokenUsage,
    UnifiedConfig,
    UnifiedMessage,
    UnifiedResponse,
)
from matrx_ai.config.citations import normalize_openai_annotation
from matrx_ai.context.emitter_protocol import Emitter
from matrx_ai.providers.keys import keyed_provider_client
from matrx_ai.providers.outbound_capture import (
    make_capture_http_client,
    stamp_call_meta,
)
from matrx_ai.providers.snapshot import capture_request_payload

from .translator import OpenAITranslator

if TYPE_CHECKING:  # circular-by-design: catalog.models imports providers.resolved_capabilities
    from matrx_ai.catalog.models import ResolvedCallProfile

DEBUG_OVERRIDE = False


class OpenAIChat:
    """OpenAI Responses API-specific endpoint implementation."""

    endpoint_name: str
    debug: bool

    # Memoized on the RESOLVED KEY VALUE — a host-side key rotation builds a
    # fresh SDK client on the next request (no process restart).
    client = keyed_provider_client(
        "OPENAI_API_KEY",
        factory=lambda api_key: AsyncOpenAI(
            api_key=api_key,
            http_client=make_capture_http_client(),
        ),
    )

    def __init__(self, debug: bool = False):
        self.endpoint_name = "[OPENAI CHAT]"
        self.translator = OpenAITranslator(debug=debug)
        self.debug = debug
        self._event_samples = {}
        self._reasoning_started = {}  # Track reasoning items that have received content
        # Reasoning items for which we've emitted the content-less "reasoning
        # started" lifecycle signal (keyed by reasoning item id). Independent of
        # _reasoning_started, which only tracks items that streamed summary TEXT.
        self._reasoning_signaled_ids: set[str] = set()

        if DEBUG_OVERRIDE:
            self.debug = True

    def to_provider_config(
        self, config: UnifiedConfig, profile: ResolvedCallProfile
    ) -> dict[str, Any]:
        return self.translator.build_request(config, profile)

    def to_unified_response(
        self, response: OpenAIResponse, matrx_model_name: str
    ) -> UnifiedResponse:
        """Convert OpenAI API response to unified format"""

        return self.translator.from_openai(response, matrx_model_name)

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
        matrx_model_name = unified_config.model

        vcprint(
            f"[OpenAI Chat] executing wire={profile.wire_format}, debug={self.debug}",
            color="blue",
        )

        try:
            # TTS is a capability fact (audio out, no text out) — never a name
            # or api_class probe. Mirrors translate_request's speech predicate.
            caps = profile.capabilities
            if caps.produces_audio and not caps.produces_text:
                return await self._execute_tts(unified_config, profile, emitter, matrx_model_name)

            # Build provider-specific config
            config_data = self.to_provider_config(unified_config, profile)
            capture_request_payload(
                config_data,
                provider="openai",
                wire_format=profile.wire_format,
                debug=debug,
            )
            stamp_call_meta(
                provider="openai",
                model=matrx_model_name,
                is_streaming=bool(unified_config.stream),
            )

            if self.debug:
                rich.print(config_data)

            if unified_config.stream:
                return await self._execute_streaming(config_data, emitter, matrx_model_name)
            else:
                return await self._execute_non_streaming(config_data, emitter, matrx_model_name)

        except Exception as e:
            if getattr(e, "error_info", None) is not None:
                raise

            from matrx_ai.providers.errors import classify_openai_error

            error_info = classify_openai_error(e)
            e.error_info = error_info
            raise

    async def _execute_tts(
        self,
        unified_config: UnifiedConfig,
        profile: ResolvedCallProfile,
        emitter: Emitter,
        matrx_model_name: str,
    ) -> UnifiedResponse:
        """Execute OpenAI TTS request via client.audio.speech.create."""
        from matrx_ai.catalog.resolve import resolve_tts_voice
        from matrx_ai.config.dictionary_config import apply_tts_dictionary

        tts = unified_config.tts_voice_config
        model = profile.provider_model_id
        voice = resolve_tts_voice(profile, tts._primary_voice() if tts else None)

        # OpenAI TTS supports: mp3, opus, aac, flac, wav, pcm
        valid_formats = {"mp3", "opus", "aac", "flac", "wav", "pcm"}
        audio_format = (unified_config.audio_format or "mp3").lower()
        if audio_format not in valid_formats:
            audio_format = "mp3"

        text_parts: list[str] = []
        for msg in unified_config.messages:
            if hasattr(msg, "content"):
                for c in msg.content:
                    if hasattr(c, "text") and c.text:
                        text_parts.append(c.text)
        input_text = " ".join(text_parts).strip() or "."

        # Multi-speaker configs collapse to a single voice for OpenAI.
        # Strip speaker labels (e.g. "Alex: ") so they aren't read aloud.
        if tts:
            input_text = tts.strip_speaker_labels(input_text)

        # Custom Dictionary pronunciation floor — OpenAI TTS `input` is plain text
        # (no SSML/phoneme/lexicon); substitute respellings before send. A soft
        # `instructions` directive could augment on gpt-4o-mini-tts (future).
        # See docs/dictionary/providers/openai.md.
        input_text = apply_tts_dictionary(
            unified_config.dictionary, input_text, provider="openai", model=model
        )

        vcprint(f"[OpenAI TTS] model={model} voice={voice} format={audio_format}", color="blue")

        stamp_call_meta(provider="openai", model=matrx_model_name, is_streaming=False)
        response = await self.client.audio.speech.create(
            model=model,
            voice=voice,
            input=input_text,
            response_format=audio_format,
        )

        audio_bytes = response.content

        mime_map = {
            "mp3": "audio/mpeg",
            "opus": "audio/opus",
            "aac": "audio/aac",
            "flac": "audio/flac",
            "wav": "audio/wav",
            "pcm": "audio/pcm",
        }
        mime_type = mime_map.get(audio_format, "audio/mpeg")

        # Phase 2c — envelope path so the FE gets file_id +
        # durable URLs + canonical MediaGenerationMetadata
        # for OpenAI TTS just like ElevenLabs.
        from matrx_ai.media import save_media_envelope_async
        from matrx_ai.media.generation_metadata import map_tts_audio_response

        gen_meta = map_tts_audio_response(
            provider="openai",
            model=model,
            prompt=input_text[:4096],
            voice=voice,
            audio_format=audio_format,
        )
        envelope = await save_media_envelope_async(
            content=audio_bytes,
            mime_type=mime_type,
            audio_format=audio_format,
            prompt=input_text,
            model=model,
            provider="openai",
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
        # endpoint returns raw bytes with no usage object. Basis-aware: a
        # character_input model bills the chars; a token-priced model with no
        # usage (gpt-4o-mini-tts) is flagged loudly rather than billed $0 silently.
        from matrx_ai.config.usage_config import build_character_billed_usage_async

        usage = await build_character_billed_usage_async(
            characters=len(input_text),
            matrx_model_name=matrx_model_name,
            provider_model_name=model,
            api="openai",
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
            "url": envelope.url,
            "cdn_url": envelope.cdn_url,
            "download_url": envelope.download_url,
        }
        await emitter.send_data(
            MediaBlockData(
                block=cloud_file_to_media_block(
                    synthetic_record,
                    url_set=url_set,
                    kind_override="audio",
                )
            )
        )
        await asyncio.sleep(0)

        return unified_response

    async def _execute_non_streaming(
        self,
        config_data: dict[str, Any],
        emitter: Emitter,
        matrx_model_name: str,
    ) -> UnifiedResponse:
        """Execute non-streaming OpenAI request"""

        # Remove stream parameter if present
        config_data_copy = config_data.copy()
        config_data_copy.pop("stream", None)

        # Make API call
        response: OpenAIResponse = await self.client.responses.create(**config_data_copy)

        content = ""
        for item in response.output:
            item_type = item.type
            if item_type == "reasoning":
                # Collect reasoning text first
                reasoning_text = ""
                for summary_item in item.summary:
                    reasoning_text += summary_item.text
                # Only add tags if there's actual content
                if reasoning_text.strip():
                    content += "\n<reasoning>\n"
                    content += reasoning_text
                    content += "\n</reasoning>\n"
            elif item_type == "message":
                if item.content:
                    for content_item in item.content:
                        if content_item.type == "output_text":
                            content += content_item.text

        await emitter.send_chunk(content)

        return self.to_unified_response(response, matrx_model_name)

    async def _execute_streaming(
        self,
        config_data: dict[str, Any],
        emitter: Emitter,
        matrx_model_name: str,
    ) -> UnifiedResponse:
        """Execute streaming OpenAI request"""

        # Clear reasoning tracking for this stream
        self._reasoning_started = {}
        self._reasoning_signaled_ids = set()

        final_response: OpenAIResponse | None = None
        # Terminal Response seen on ANY terminal event, including
        # ``response.failed``. Distinct from ``final_response`` (the value we
        # RETURN, which still excludes ``failed`` so a genuine failure rides the
        # retry path). OpenAI bills the call the instant it starts and carries
        # the usage block on the ``failed`` event; we keep it here ONLY to
        # recover that billed usage and stamp it onto the error below, so a
        # failed cx_request carries real cost instead of $0 (the cost-tracking
        # gap). It never changes what is returned.
        billable_response: OpenAIResponse | None = None

        try:
            # ``Responses.stream`` recursively transforms every typed request field
            # before it reaches httpx.  That SDK-owned walk is synchronous CPU work
            # despite its async spelling and a large tool catalog can freeze the
            # shared server loop for >1s.  The translator has already produced the
            # final OpenAI wire body, so send it through the SDK's documented
            # ``extra_body`` seam.  Only the two tiny required placeholders are
            # transformed; extra_body overrides them with the real wire values.
            wire_body = dict(config_data)
            wire_body["stream"] = True
            async with self.client.responses.stream(
                input="",
                model="wire-body",
                extra_body=wire_body,
            ) as stream:
                async for event in stream:
                    await self._handle_event(event, emitter)

                    # Capture the terminal Response off the success/incomplete
                    # terminal events. The OpenAI SDK only stores its internal
                    # ``_completed_response`` for ``response.completed``, so
                    # ``stream.get_final_response()`` RAISES
                    # ("Didn't receive a `response.completed` event.") on
                    # ``response.incomplete`` (e.g. a reasoning model that hit
                    # ``max_output_tokens``) — even though the text already fully
                    # streamed to the client. Grabbing ``event.response`` directly
                    # means a token-capped response is returned with its real
                    # finish_reason (MAX_TOKENS) instead of being discarded and
                    # retried, which is what silently lost the user's answer.
                    #
                    # ``response.failed`` is deliberately NOT captured into
                    # ``final_response``: a genuine server-side failure is
                    # potentially transient, so it falls through to
                    # ``get_final_response()`` below (which raises) and rides the
                    # normal retry path. We DO capture its billed usage.
                    if event.type in (
                        "response.completed",
                        "response.incomplete",
                    ):
                        final_response = event.response
                        billable_response = event.response
                    elif event.type == "response.failed":
                        billable_response = getattr(event, "response", None)

                # No success/incomplete terminal event (a ``response.failed`` or a
                # genuine mid-stream break) — fall back to the SDK accumulator,
                # which raises if nothing usable arrived. That is a real error and
                # SHOULD propagate to the retry path — but FIRST stamp the billed
                # usage from the failed Response onto the error so the cost is
                # recorded on the failed row.
                if final_response is None:
                    try:
                        final_response = await stream.get_final_response()
                    except BaseException as stream_exc:
                        self._attach_billed_usage_from_response(
                            stream_exc, billable_response, matrx_model_name
                        )
                        raise

            return self.to_unified_response(final_response, matrx_model_name)
        except BaseException as exc:
            # Any failure/cancel before a terminal event: best-effort stamp of
            # whatever billed usage we observed (usually none for OpenAI, which
            # only emits usage on the terminal event — the hook stays correct for
            # providers that stream usage incrementally). Re-raise UNCHANGED.
            self._attach_billed_usage_from_response(exc, billable_response, matrx_model_name)
            raise

    def _attach_billed_usage_from_response(
        self,
        exc: BaseException,
        response: OpenAIResponse | None,
        matrx_model_name: str,
    ) -> None:
        """Stamp billed ``TokenUsage`` from a terminal Response onto a failing /
        cancelling exception so the orchestrator records real cost on the failed
        cx_request row. Best-effort — never raises, never overwrites."""
        # LAYER 2: the mark means "an adapter LOOKED", which is true even when
        # there is nothing to attach — it must precede every early return.
        from matrx_ai.providers.errors import mark_billing_checked

        mark_billing_checked(exc)
        if response is None:
            return
        usage = getattr(response, "usage", None)
        if usage is None:
            return
        try:
            from matrx_ai.providers.errors import attach_billed_usage

            token_usage = TokenUsage.from_openai(
                usage,
                matrx_model_name=matrx_model_name,
                provider_model_name=getattr(response, "model", "") or "",
                response_id=getattr(response, "id", "") or "",
            )
            attach_billed_usage(exc, token_usage)
        except Exception as err:
            from matrx_ai.providers.errors import report_billed_usage_capture_failure

            report_billed_usage_capture_failure("openai", err)

    async def _handle_event(self, event: Any, emitter: Emitter):
        """Handle individual streaming event"""
        await asyncio.sleep(0)

        event_type = event.type
        if event_type and event_type not in self._event_samples:
            self._event_samples[event_type] = event

        # Text content streaming
        if event_type == "response.output_text.delta":
            await emitter.send_chunk(event.delta)

        # Reasoning streaming events
        elif event_type == "response.output_item.added" and event.item.type == "reasoning":
            # Don't send the <reasoning> opening TEXT tag yet — wait for actual
            # summary content (which never comes under reasoning_summary="never").
            # But DO emit the content-less lifecycle signal: this reasoning item
            # is added even when the summary is suppressed, so it's the reliable
            # "the model is thinking now" marker. The UI leaves the heartbeat gap.
            reasoning_id = getattr(event.item, "id", None)
            if reasoning_id and reasoning_id not in self._reasoning_signaled_ids:
                self._reasoning_signaled_ids.add(reasoning_id)
                await emitter.send_reasoning_state("started")
            if self.debug:
                vcprint(f"Reasoning item added: {event.item.id}", color="blue")

        elif event_type == "response.reasoning_summary_text.delta":
            # Only send opening tag on first actual content
            reasoning_id = getattr(event, "item_id", None)
            if reasoning_id and reasoning_id not in self._reasoning_started:
                await emitter.send_chunk("\n<reasoning>\n")
                self._reasoning_started[reasoning_id] = True
                if self.debug:
                    vcprint(f"Reasoning content started: {reasoning_id}", color="blue")
            await emitter.send_chunk(event.delta)

        elif event_type == "response.output_item.done" and event.item.type == "reasoning":
            # Only send closing TEXT tag if we sent the opening one.
            reasoning_id = event.item.id
            if reasoning_id in self._reasoning_started:
                await emitter.send_chunk("\n</reasoning>\n")
                del self._reasoning_started[reasoning_id]
                if self.debug:
                    vcprint(
                        f"Reasoning completed with content: {reasoning_id}",
                        color="blue",
                    )
            elif self.debug:
                vcprint(f"Reasoning completed with no content: {reasoning_id}", color="blue")
            # Close the content-less lifecycle signal regardless of whether
            # summary text streamed — pairs with the "started" emitted on
            # output_item.added.
            if reasoning_id in self._reasoning_signaled_ids:
                self._reasoning_signaled_ids.discard(reasoning_id)
                await emitter.send_reasoning_state("stopped")

        # Web-search / file citation annotation attaching to the answer text.
        # The Responses API delivers annotations mid-stream as
        # `response.output_text.annotation.added` — normalize and emit a typed
        # `citation` event LIVE (the same annotations also arrive on the final
        # Response and are normalized into metadata["citations"] by
        # TextContent.from_openai for persistence).
        elif event_type == "response.output_text.annotation.added":
            annotation = getattr(event, "annotation", None)
            if annotation is not None:
                # A malformed annotation must never abort the in-flight answer;
                # the final Response still carries it for persistence.
                try:
                    raw_annotation = (
                        annotation.model_dump()
                        if hasattr(annotation, "model_dump")
                        else (annotation if isinstance(annotation, dict) else dict(annotation))
                    )
                    normalized = normalize_openai_annotation(raw_annotation, "")
                    await emitter.send_citation(
                        CitationPayload(
                            block_index=getattr(event, "content_index", None),
                            citation=normalized.model_dump(exclude_none=True),
                        )
                    )
                except Exception as citation_exc:
                    vcprint(
                        f"[OPENAI CITATIONS] Failed to normalize/emit an "
                        f"annotation — skipping this citation only "
                        f"(answer stream unaffected): {citation_exc}",
                        color="red",
                    )

        # Function/tool call completed
        elif event_type == "response.output_item.done" and event.item.type == "message":
            for content_item in event.item.content:
                if content_item.type == "function_call":
                    vcprint(content_item, "Function Call", color="magenta")

        # Stream lifecycle events
        elif event_type == "response.created":
            vcprint("\n\n[OPENAI API CHAT] Response Stream Started", color="cyan")

        elif event_type == "response.completed":
            if self.debug:
                vcprint("OpenAI Response Stream Completed", color="green")
                vcprint(
                    self._event_samples,
                    "Unique Event Types & Samples",
                    color="magenta",
                    verbose=False,
                )
                self._event_samples = {}

        elif event_type == "error":
            error_data = getattr(event, "error", {})
            await emitter.send_error(
                error_type="streaming_error",
                message=str(error_data),
                user_message="An error occurred during streaming.",
            )

    async def _debug_event(self, event: Any):
        """Debug logging for events"""
        event_type = event.type

        if event_type == "response.output_text.delta":
            delta = event.delta
            print(delta, end="", flush=True)
        elif event_type == "response.output_item.added":
            item = event.item
            vcprint(item, "Output Item Added", color="blue")
        elif event_type == "response.created":
            vcprint("=================== RESPONSE STARTED ===================", color="blue")
        elif event_type == "response.completed":
            vcprint(
                "=================== RESPONSE COMPLETED ===================",
                color="green",
            )
        else:
            vcprint(event, f"Event: {event_type}", color="yellow")
