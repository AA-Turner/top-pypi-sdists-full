"""ElevenLabs Sound Effects: text to a short sound effect, billed per generated second.

The api row ``elevenlabs_sound_effects`` (migration 1615) routes here. Same shape as Eleven Music
(``music_api.py``): one paid call returns raw audio with no usage object, so the adapter builds the billed usage
itself (``audio_second_output``, $/second) BEFORE storing, and anything after the paid call carries that usage
(``paid_output``), so a storage failure never re-buys the effect and never records $0.

The length rides ``config.duration_seconds`` (the one canonical field every generator takes), clamped to the
provider's 0.5-30 s. Left empty, the model picks the length and the bill is the length it returned (the mp3 is a
constant 128 kbps, so its size is its length).
"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any

from matrx_utils import vcprint

from matrx_ai.config import AudioContent, UnifiedConfig, UnifiedMessage, UnifiedResponse
from matrx_ai.config.finish_reason import FinishReason
from matrx_ai.providers.sdk_drift import route_undeclared_params

from .client import get_elevenlabs_client
from .music_api import declined_status, music_prompt_text

if TYPE_CHECKING:
    from matrx_ai.catalog.models import ResolvedCallProfile

#: Provider limits (https://elevenlabs.io/docs/api-reference/text-to-sound-effects/convert).
MIN_EFFECT_SECONDS = 0.5
MAX_EFFECT_SECONDS = 30.0
_OUTPUT_FORMAT = "mp3_44100_128"
#: Bytes in one second of ``mp3_44100_128`` (128 kbit/s, constant bit rate).
MP3_128_BYTES_PER_SECOND = 16_000


def effect_length_seconds(config: UnifiedConfig) -> float | None:
    """The length to ask for, clamped to 0.5-30 s; ``None`` lets the model choose."""
    asked = getattr(config, "duration_seconds", None)
    if asked is None:
        return None
    return round(min(MAX_EFFECT_SECONDS, max(MIN_EFFECT_SECONDS, float(asked))), 2)


def mp3_seconds(audio: bytes) -> float:
    """The length of a ``mp3_44100_128`` body, from its size."""
    return round(len(audio) / MP3_128_BYTES_PER_SECOND, 3)


class ElevenLabsSoundEffects:
    endpoint_name: str = "[ELEVENLABS SOUND EFFECTS]"

    def __init__(self) -> None:
        self.client = get_elevenlabs_client()

    async def execute(
        self, unified_config: UnifiedConfig, profile: ResolvedCallProfile, debug: bool = False
    ) -> UnifiedResponse:
        try:
            return await self._execute_effect(unified_config, profile)
        except Exception as e:
            if getattr(e, "error_info", None) is not None:
                raise
            from matrx_ai.providers.errors import classify_elevenlabs_error

            e.error_info = classify_elevenlabs_error(e)
            raise

    def _convert(self, prompt: str, model_id: str, seconds: float | None) -> bytes:
        kwargs: dict[str, Any] = {
            "text": prompt,
            "model_id": model_id,
            "output_format": _OUTPUT_FORMAT,
        }
        if seconds is not None:
            kwargs["duration_seconds"] = seconds
        convert = self.client.text_to_sound_effects.convert
        stream = convert(
            **route_undeclared_params(convert, kwargs, provider="elevenlabs", model=model_id)
        )
        return b"".join(chunk for chunk in stream if isinstance(chunk, bytes))

    async def _execute_effect(
        self, unified_config: UnifiedConfig, profile: ResolvedCallProfile
    ) -> UnifiedResponse:
        prompt = music_prompt_text(unified_config)
        asked = effect_length_seconds(unified_config)
        model_id = profile.provider_model_id
        vcprint(
            f"[ElevenLabs Sound Effects] {model_id} {asked if asked is not None else 'auto'}s",
            color="blue",
        )
        try:
            audio = await asyncio.to_thread(self._convert, prompt, model_id, asked)
        except Exception as exc:
            status = declined_status(exc)
            if status is None:
                raise
            vcprint(
                f"[ElevenLabs Sound Effects] declined the wording ({status}); nothing was generated",
                color="yellow",
            )
            return UnifiedResponse(
                messages=[
                    UnifiedMessage(
                        role="assistant",
                        content=[],
                        metadata={
                            "finish_reason": FinishReason.CONTENT_FILTER.value,
                            "declined": status,
                        },
                    )
                ],
                usage=None,
                finish_reason=FinishReason.CONTENT_FILTER,
            )
        if not audio:
            raise ValueError("ElevenLabs returned an empty sound effect body.")

        from matrx_ai.config.usage_config import build_audio_seconds_billed_usage_async
        from matrx_ai.providers.paid_output import mark_failed_after_paid_call, store_paid_output

        seconds = asked if asked is not None else mp3_seconds(audio)
        usage = await build_audio_seconds_billed_usage_async(
            seconds=seconds,
            matrx_model_name=unified_config.model,
            provider_model_name=model_id,
            api="elevenlabs",
            extra_metadata={"effect_length_requested_s": asked, "audio_bytes": len(audio)},
        )
        generation = {"kind": "sound_effect", "model": model_id, "length_seconds": seconds}
        try:
            from matrx_ai.media import save_media_envelope_async

            envelope = await store_paid_output(
                lambda: save_media_envelope_async(
                    content=audio,
                    mime_type="audio/mpeg",
                    audio_format="mp3",
                    prompt=prompt,
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
            messages=[
                UnifiedMessage(role="assistant", content=[item], metadata={"finish_reason": "stop"})
            ],
            usage=usage,
            finish_reason=FinishReason.STOP,
        )
