"""ElevenLabs Voice Changer (speech to speech): the same speech, delivery and timing, in another voice.

The api row ``elevenlabs_voice_changer`` (migration 1615) routes here. Input is the last user message's audio part
(a platform file the media boundary resolved under the run's access, a URL, or inline base64); the voice is
``tts_voice`` resolved through the catalog (``resolve_tts_voice``), so an empty voice takes the model's catalog
default voice. Billed per second of audio (``audio_second_output``, $0.002/s): the output is a constant 128 kbps
mp3, so its size is its length. Same paid-output discipline as Eleven Music: the usage is built before storing and
carried by any failure after the paid call.
"""

from __future__ import annotations

import asyncio
import base64
from typing import TYPE_CHECKING, Any

from matrx_utils import vcprint

from matrx_ai.config import AudioContent, UnifiedConfig, UnifiedMessage, UnifiedResponse
from matrx_ai.config.finish_reason import FinishReason

from .client import get_elevenlabs_client
from .sound_effects_api import mp3_seconds

if TYPE_CHECKING:
    from matrx_ai.catalog.models import ResolvedCallProfile

_OUTPUT_FORMAT = "mp3_44100_128"


def source_audio_part(config: UnifiedConfig) -> AudioContent:
    """The audio to re-voice: the last audio part of the last user message that carries one."""
    for msg in reversed(getattr(config, "messages", None) or []):
        if str(getattr(msg, "role", "")).lower() != "user":
            continue
        for part in reversed(getattr(msg, "content", None) or []):
            if isinstance(part, AudioContent):
                return part
    raise ValueError("[ElevenLabs Voice Changer] the request has no audio; give the speech to re-voice as an audio part.")


async def resolve_file_audio(part: AudioContent) -> None:
    """Open a platform file id under the run's access — the same resolver the client runs for image and
    document parts (``_resolve_media_ref_item`` over the host's cloud file manager), never a URL fetch."""
    if not part.file_id or part.base64_data or part.resolved_url:
        return
    from matrx_ai._ext import get_ext, has_ext

    if not has_ext("get_cloud_file_manager"):
        raise ValueError("[ElevenLabs Voice Changer] this host cannot open platform files; give a URL or base64 audio.")
    from matrx_ai.providers.unified_client import _resolve_media_ref_item

    await _resolve_media_ref_item(get_ext("get_cloud_file_manager")(), part)


async def source_audio_bytes(part: AudioContent) -> bytes:
    """The part's bytes: inline base64 first, else the platform file opened under the run's access, else the URL given."""
    await resolve_file_audio(part)
    if part.base64_data:
        return base64.b64decode(part.base64_data)
    url = part.resolved_url or part.url
    if not url:
        raise ValueError(
            "[ElevenLabs Voice Changer] the audio part has no bytes and no resolvable location"
            + (f" ({part.resolver_error})" if part.resolver_error else "")
            + "; give a file id the run can open, a URL, or base64 audio."
        )
    from matrx_ai.media import fetch_media

    data = await asyncio.to_thread(fetch_media, url, target_format="bytes")
    if not isinstance(data, bytes) or not data:
        raise ValueError("[ElevenLabs Voice Changer] the audio location returned no bytes.")
    return data


class ElevenLabsVoiceChanger:
    endpoint_name: str = "[ELEVENLABS VOICE CHANGER]"

    def __init__(self) -> None:
        self.client = get_elevenlabs_client()

    async def execute(self, unified_config: UnifiedConfig, profile: ResolvedCallProfile, debug: bool = False) -> UnifiedResponse:
        try:
            return await self._execute_change(unified_config, profile)
        except Exception as e:
            if getattr(e, "error_info", None) is not None:
                raise
            from matrx_ai.providers.errors import classify_elevenlabs_error

            e.error_info = classify_elevenlabs_error(e)
            raise

    def _convert(self, audio: bytes, voice_id: str, model_id: str) -> bytes:
        stream = self.client.speech_to_speech.convert(
            voice_id,
            audio=("speech", audio),
            model_id=model_id,
            output_format=_OUTPUT_FORMAT,
        )
        return b"".join(chunk for chunk in stream if isinstance(chunk, bytes))

    async def _execute_change(self, unified_config: UnifiedConfig, profile: ResolvedCallProfile) -> UnifiedResponse:
        from matrx_ai.catalog.resolve import resolve_tts_voice

        tts = unified_config.tts_voice_config
        voice_id = resolve_tts_voice(profile, tts._primary_voice() if tts else None)
        source = await source_audio_bytes(source_audio_part(unified_config))
        model_id = profile.provider_model_id
        vcprint(f"[ElevenLabs Voice Changer] {model_id} voice={voice_id} in={len(source)}B", color="blue")
        audio = await asyncio.to_thread(self._convert, source, voice_id, model_id)
        if not audio:
            raise ValueError("ElevenLabs returned an empty voice changer body.")

        from matrx_ai.config.usage_config import build_audio_seconds_billed_usage_async
        from matrx_ai.providers.paid_output import mark_failed_after_paid_call, store_paid_output

        seconds = mp3_seconds(audio)
        usage = await build_audio_seconds_billed_usage_async(
            seconds=seconds,
            matrx_model_name=unified_config.model,
            provider_model_name=model_id,
            api="elevenlabs",
            extra_metadata={"source_audio_bytes": len(source), "audio_bytes": len(audio), "voice_id": voice_id},
        )
        generation = {"kind": "voice_change", "model": model_id, "voice_id": voice_id, "length_seconds": seconds}
        try:
            from matrx_ai.media import save_media_envelope_async

            envelope = await store_paid_output(
                lambda: save_media_envelope_async(
                    content=audio,
                    mime_type="audio/mpeg",
                    audio_format="mp3",
                    model=model_id,
                    provider="elevenlabs",
                    feature="ai_audio",
                    extra_metadata={"generation": generation},
                ),
                provider="elevenlabs",
                modality="audio",
                usage=usage,
            )
            item: Any = AudioContent(
                url=envelope.url,
                file_id=envelope.file_id,
                mime_type="audio/mpeg",
                file_size=envelope.size_bytes,
                duration_ms=envelope.duration_ms or int(seconds * 1000),
                metadata={"generation": generation},
            )
        except Exception as exc:
            mark_failed_after_paid_call(exc, provider="elevenlabs", modality="audio", usage=usage)
            raise
        return UnifiedResponse(
            messages=[UnifiedMessage(role="assistant", content=[item], metadata={"finish_reason": "stop"})],
            usage=usage,
            finish_reason=FinishReason.STOP,
        )
