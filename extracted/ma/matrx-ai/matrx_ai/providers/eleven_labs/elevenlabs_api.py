from __future__ import annotations

import asyncio
import base64
import uuid
from collections.abc import Callable, Iterator
from typing import TYPE_CHECKING

from matrx_connect.context.events import InfoPayload
from matrx_utils import vcprint

from matrx_ai.config import (
    AudioContent,
    UnifiedConfig,
    UnifiedMessage,
    UnifiedResponse,
)
from matrx_ai.context.emitter_protocol import Emitter
from matrx_ai.providers.outbound_capture import (
    emit_explicit_context_analysis,
    stamp_call_meta,
)

from .client import get_elevenlabs_client

if TYPE_CHECKING:  # circular-by-design: catalog.models imports providers.resolved_capabilities
    from matrx_ai.catalog.models import ResolvedCallProfile


_AUDIO_STREAM_DONE = object()
_ELEVENLABS_MP3_OUTPUT_FORMAT = "mp3_44100_128"


class ElevenLabsChat:
    """ElevenLabs TTS endpoint. Dialogue-capable models (capabilities jsonb
    ``features: ["dialogue"]`` → ``profile.capabilities.supports_dialogue``)
    go through the text_to_dialogue API; every other model goes through the
    plain text-to-speech endpoint (eleven_flash_v2_5 rejects dialogue with
    "does not support dialogue")."""

    endpoint_name: str = "[ELEVENLABS CHAT]"

    def __init__(self) -> None:
        self.client = get_elevenlabs_client()

    @staticmethod
    def _tts_stream_id() -> str:
        from matrx_ai.context.app_context import get_app_context

        try:
            request_id = getattr(get_app_context(), "request_id", None)
        except Exception:
            request_id = None
        return str(request_id) if request_id else uuid.uuid4().hex

    @staticmethod
    async def _emit_audio_stream_chunk(
        emitter: Emitter,
        *,
        stream_id: str,
        seq: int,
        data: bytes,
    ) -> None:
        from matrx_connect.context.data_types import AudioStreamChunkData

        await emitter.send_data(
            AudioStreamChunkData(
                stream_id=stream_id,
                seq=seq,
                audio_base64=base64.b64encode(data).decode("ascii"),
                mime_type="audio/mpeg",
                encoding="mp3",
                sample_rate=44100,
                bits_per_sample=16,
                channels=1,
            )
        )
        await asyncio.sleep(0)

    async def _collect_streaming_bytes(
        self,
        stream_factory: Callable[[], Iterator[bytes]],
        emitter: Emitter,
        *,
        stream_id: str,
        first_seq: int,
        emit_mp3_chunks: bool,
    ) -> tuple[bytes, int]:
        """Drain one synchronous SDK stream without blocking the event loop.

        The producer owns the SDK iterator in a worker thread. Every MP3 chunk
        is handed to the async consumer immediately for ordered event emission,
        while the exact same bytes are retained for canonical persistence.
        """

        loop = asyncio.get_running_loop()
        queue: asyncio.Queue[bytes | object] = asyncio.Queue()
        producer_state: dict[str, BaseException | None] = {"error": None}
        collected = bytearray()

        def _produce() -> None:
            try:
                for chunk in stream_factory():
                    if not isinstance(chunk, bytes) or not chunk:
                        continue
                    collected.extend(chunk)
                    loop.call_soon_threadsafe(queue.put_nowait, chunk)
            except BaseException as exc:
                producer_state["error"] = exc
            finally:
                loop.call_soon_threadsafe(queue.put_nowait, _AUDIO_STREAM_DONE)

        producer = loop.run_in_executor(None, _produce)
        seq = first_seq
        while True:
            item = await queue.get()
            if item is _AUDIO_STREAM_DONE:
                break
            assert isinstance(item, bytes)
            if emit_mp3_chunks:
                await self._emit_audio_stream_chunk(
                    emitter,
                    stream_id=stream_id,
                    seq=seq,
                    data=item,
                )
                seq += 1

        await producer
        if producer_state["error"] is not None:
            raise producer_state["error"]
        return bytes(collected), seq

    async def execute(
        self,
        unified_config: UnifiedConfig,
        profile: ResolvedCallProfile,
        debug: bool = False,
    ) -> UnifiedResponse:
        from matrx_ai.context.app_context import get_app_context

        emitter: Emitter = get_app_context().emitter
        matrx_model_name = unified_config.model

        vcprint(f"[ElevenLabs Chat] executing wire={profile.wire_format}", color="blue")

        try:
            return await self._execute_tts(unified_config, profile, emitter, matrx_model_name)
        except Exception as e:
            from matrx_ai.providers.errors import classify_elevenlabs_error

            error_info = classify_elevenlabs_error(e)
            e.error_info = error_info
            raise

    @staticmethod
    async def _build_locators(unified_config: UnifiedConfig) -> list:
        """Coerce config locator dicts → SDK PronunciationDictionaryVersionLocator
        objects (max 3). When the request carried none, ask the host-injected
        resolver for the user's published dictionary. Best-effort; never raises."""
        raw = list(getattr(unified_config, "pronunciation_dictionary_locators", None) or [])
        if not raw:
            try:
                from matrx_ai._ext import get_pronunciation_locator_resolver

                resolver = get_pronunciation_locator_resolver()
                if resolver is not None:
                    from matrx_ai.context.app_context import get_app_context

                    user_id = getattr(get_app_context(), "user_id", None)
                    raw = list(await resolver(user_id=user_id) or [])
            except Exception:  # noqa: BLE001 — best-effort, never break a render
                raw = []
        if not raw:
            return []
        from elevenlabs.types.pronunciation_dictionary_version_locator import (
            PronunciationDictionaryVersionLocator,
        )

        out = []
        for item in raw[:3]:
            pid = item.get("pronunciation_dictionary_id")
            vid = item.get("version_id")
            if pid and vid:
                out.append(
                    PronunciationDictionaryVersionLocator(
                        pronunciation_dictionary_id=pid, version_id=vid
                    )
                )
        return out

    async def _execute_tts(
        self,
        unified_config: UnifiedConfig,
        profile: ResolvedCallProfile,
        emitter: Emitter,
        matrx_model_name: str,
    ) -> UnifiedResponse:
        tts = unified_config.tts_voice_config
        if not tts or not tts.is_configured:
            raise ValueError(
                "[ElevenLabs TTS] No tts_voice configured. "
                "Pass tts_voice as a list of {text, voice_id} dicts for dialogue mode, "
                "or a string voice_id for single-speaker mode."
            )

        audio_format = (unified_config.audio_format or "mp3").lower()
        # ElevenLabs output_format uses a compound string like "mp3_44100_128"
        valid_codecs = {"mp3", "wav", "pcm", "ulaw"}
        codec = audio_format if audio_format in valid_codecs else "mp3"
        mime_map = {
            "mp3": "audio/mpeg",
            "wav": "audio/wav",
            "pcm": "audio/pcm",
            "ulaw": "audio/basic",
        }
        mime_type = mime_map.get(codec, "audio/mpeg")
        emit_mp3_chunks = codec == "mp3"
        stream_id = self._tts_stream_id()
        seq = 0

        model_in = profile.provider_model_id
        from matrx_ai.catalog.resolve import resolve_tts_voice, validate_tts_voices

        if tts.is_dialogue:
            validate_tts_voices(profile, [turn.voice_id for turn in tts.dialogue_turns])
        else:
            tts.voice = resolve_tts_voice(profile, tts._primary_voice())

        # Resolve dialogue inputs — dialogue mode uses inline voice_ids;
        # single-speaker mode extracts text from messages and wraps it.
        if tts.is_dialogue:
            batched_inputs, model = tts.to_elevenlabs(model=model_in)
        else:
            text_parts: list[str] = []
            for msg in unified_config.messages:
                if hasattr(msg, "content"):
                    for c in msg.content:
                        if hasattr(c, "text") and c.text:
                            text_parts.append(c.text)
            input_text = " ".join(text_parts).strip() or "."
            input_text = tts.strip_speaker_labels(input_text)
            batched_inputs, model = tts.to_elevenlabs(text=input_text, model=model_in)

        # Custom Dictionary pronunciation. ElevenLabs `text_to_dialogue` (our
        # multi-speaker path) does NOT honor pronunciation_dictionary_locators,
        # and eleven_flash_v2_5 silently drops phoneme rules — so when the request
        # carries a dictionary, the alias-substitution floor is the only mechanism
        # that reliably applies custom pronunciation here. We rewrite the spoken
        # text and skip the (ineffective) native locators in that case. Native
        # locators remain a best-effort fallback ONLY when no in-config dictionary
        # was supplied. See docs/dictionary/providers/elevenlabs.md.
        from matrx_ai.config.dictionary_config import DictionaryConfig, apply_tts_dictionary

        _dconf = DictionaryConfig.coerce(unified_config.dictionary)
        _use_substitution = _dconf is not None and not _dconf.is_empty
        if _use_substitution:
            for _batch in batched_inputs:
                for _turn in _batch:
                    _t = _turn.get("text")
                    if _t:
                        _turn["text"] = apply_tts_dictionary(
                            _dconf, _t, provider="elevenlabs", model=model
                        )

        vcprint(
            f"[ElevenLabs TTS] model={model} batches={len(batched_inputs)} "
            f"turns={sum(len(b) for b in batched_inputs)} codec={codec}",
            color="blue",
        )

        await emitter.send_info(
            InfoPayload(
                code="tts_generating",
                system_message=f"Generating audio ({sum(len(b) for b in batched_inputs)} dialogue turns)...",
                user_message="Generating audio...",
            )
        )

        # Native pronunciation-dictionary locators (ElevenLabs only), resolved
        # host-side and passed straight through. Max 3, applied in order. Skipped
        # when we already applied the alias-substitution floor above (the request
        # carried a dictionary) — locators would be redundant or ineffective.
        locators = [] if _use_substitution else await self._build_locators(unified_config)

        # Endpoint routing is DATA-driven: the model's capabilities jsonb declares
        # "dialogue" in `features` (→ profile.capabilities.supports_dialogue).
        # Non-dialogue models (eleven_flash_v2_5) get rejected by text_to_dialogue
        # with "does not support dialogue" — they go through the plain
        # text-to-speech endpoint, one call per turn (each turn keeps its own
        # voice_id). A tts_quality tier override can swap the model away from the
        # profile's own (profile capabilities then describe the WRONG model), so
        # the dialogue API is used only when the resolved model IS the profile's
        # model AND that model declares the capability; the plain endpoint is the
        # safe route for every ElevenLabs TTS model.
        use_dialogue_api = (
            profile.capabilities.supports_dialogue and model == profile.provider_model_id
        )
        endpoint_label = "text-to-dialogue" if use_dialogue_api else "text-to-speech"
        vcprint(
            f"[ElevenLabs TTS] endpoint={endpoint_label} "
            f"(supports_dialogue={profile.capabilities.supports_dialogue})",
            color="blue",
        )

        # ElevenLabs SDK is synchronous — run each batch in a thread executor
        # so the event loop stays free for heartbeats and status events.
        all_audio_bytes = b""
        for i, batch in enumerate(batched_inputs):
            batch_num = i + 1
            total_batches = len(batched_inputs)
            char_count = sum(len(t["text"]) for t in batch)
            vcprint(
                f"[ElevenLabs TTS] Requesting batch {batch_num}/{total_batches} ({char_count} chars)",
                color="cyan",
            )
            if total_batches > 1:
                await emitter.send_info(
                    InfoPayload(
                        code="tts_batch_progress",
                        system_message=f"Processing batch {batch_num}/{total_batches}...",
                        user_message=f"Generating audio part {batch_num} of {total_batches}...",
                    )
                )

            stamp_call_meta(
                provider="elevenlabs",
                model=matrx_model_name,
                is_streaming=True,
                attempt=batch_num,
            )
            try:
                await emit_explicit_context_analysis(
                    provider="elevenlabs",
                    method="POST",
                    url=(
                        f"https://api.elevenlabs.io/v1/text-to-dialogue/stream?model_id={model}"
                        if use_dialogue_api
                        else f"https://api.elevenlabs.io/v1/text-to-speech/{{voice_id}}/stream?model_id={model}"
                    ),
                    headers={"Content-Type": "application/json"},
                    body={"inputs": batch, "model_id": model},
                    is_streaming=True,
                    model=matrx_model_name,
                    attempt=batch_num,
                )
            except Exception:
                pass

            def _stream_batch(turns: list[dict]) -> Iterator[bytes]:
                if use_dialogue_api:
                    kwargs: dict = {"inputs": turns, "model_id": model}
                    if emit_mp3_chunks:
                        kwargs["output_format"] = _ELEVENLABS_MP3_OUTPUT_FORMAT
                    if locators:
                        kwargs["pronunciation_dictionary_locators"] = locators
                    yield from self.client.text_to_dialogue.stream(**kwargs)
                    return
                # Plain text-to-speech: one call per turn, each with its own
                # voice_id (a single-speaker request is exactly one turn).
                for turn in turns:
                    turn_kwargs: dict = {
                        "voice_id": turn["voice_id"],
                        "text": turn["text"],
                        "model_id": model,
                    }
                    if emit_mp3_chunks:
                        turn_kwargs["output_format"] = _ELEVENLABS_MP3_OUTPUT_FORMAT
                    if locators:
                        turn_kwargs["pronunciation_dictionary_locators"] = locators
                    yield from self.client.text_to_speech.stream(**turn_kwargs)

            batch_bytes, seq = await self._collect_streaming_bytes(
                lambda: _stream_batch(batch),
                emitter,
                stream_id=stream_id,
                first_seq=seq,
                emit_mp3_chunks=emit_mp3_chunks,
            )
            all_audio_bytes += batch_bytes
            vcprint(
                f"[ElevenLabs TTS] Batch {batch_num} complete: {len(batch_bytes)} bytes",
                color="cyan",
            )

        await emitter.send_info(
            InfoPayload(
                code="tts_saving",
                system_message=f"Audio received ({len(all_audio_bytes):,} bytes). Saving...",
                user_message="Audio received. Saving...",
            )
        )

        # Phase 2b/3b — switch to the envelope path so the FE gets
        # file_id, durable URLs, and the full canonical
        # MediaGenerationMetadata stamped into cld_files.metadata.generation.
        from matrx_ai.media import save_media_envelope_async
        from matrx_ai.media.generation_metadata import map_elevenlabs_audio_response

        # Pull voice identity from the resolved TTS config for the
        # canonical metadata. Dialogue mode has multiple voices; for
        # single-speaker the first voice_id is the canonical one.
        voice_id: str | None = None
        voice_name: str | None = None
        try:
            first_input = batched_inputs[0][0] if batched_inputs and batched_inputs[0] else None
            if first_input:
                voice_id = first_input.get("voice_id")
            voice_name = getattr(tts, "voice_name", None) or getattr(tts, "name", None)
        except Exception:
            pass

        total_chars = sum(len(t["text"]) for b in batched_inputs for t in b)

        # Concatenate every dialogue input's text as the canonical
        # "prompt" — gives the audit log a single representation of
        # what the model was asked to say.
        prompt_text = " ".join(t.get("text", "") for b in batched_inputs for t in b).strip()

        gen_meta = map_elevenlabs_audio_response(
            raw=None,
            request_kwargs={},
            prompt=prompt_text[:4096],
            model=model,
            voice_id=voice_id,
            voice_name=voice_name,
            char_count=total_chars,
            audio_format=codec,
            is_dialogue=tts.is_dialogue,
        )

        envelope = await save_media_envelope_async(
            content=all_audio_bytes,
            mime_type=mime_type,
            audio_format=codec,
            prompt=prompt_text,
            model=model,
            provider="elevenlabs",
            feature="ai_audio",
            extra_metadata={"generation": gen_meta.model_dump(exclude_none=True)},
        )
        vcprint(f"[ElevenLabs TTS] Saved: file_id={envelope.file_id}", color="green")

        audio_content = AudioContent(
            url=envelope.url,
            file_id=envelope.file_id,
            mime_type=mime_type,
            file_size=envelope.size_bytes,
            duration_ms=envelope.duration_ms,
            metadata={"generation": gen_meta.model_dump(exclude_none=True)},
        )
        msg = UnifiedMessage(role="assistant", content=[audio_content])

        # Bill by characters actually sent (post-dictionary, summed across every
        # dialogue turn) — ElevenLabs streams raw bytes with no usage object. See
        # build_character_billed_usage for the basis-aware contract.
        from matrx_ai.config.usage_config import build_character_billed_usage_async

        usage = await build_character_billed_usage_async(
            characters=total_chars,
            matrx_model_name=matrx_model_name,
            provider_model_name=model,
            api="elevenlabs",
        )

        unified_response = UnifiedResponse(messages=[msg], usage=usage)

        # Emit a canonical matrx-owned AudioBlock so the FE has file_id,
        # durable cdn/download URLs, AND the generation
        # metadata block all on the wire.
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
        from matrx_connect.context.data_types import AudioStreamEndData

        await emitter.send_data(
            AudioStreamEndData(
                stream_id=stream_id,
                total_chunks=seq,
                url=envelope.url,
                mime_type=mime_type,
                file_id=envelope.file_id,
                cdn_url=envelope.cdn_url,
                download_url=envelope.download_url,
                duration_ms=envelope.duration_ms,
                sample_rate=44100 if emit_mp3_chunks else 24000,
                bits_per_sample=16,
                channels=1,
            )
        )
        await asyncio.sleep(0)

        return unified_response
