"""ElevenLabs Eleven Music: text to an instrumental music bed, an exact length, billed per generated second.

The api row ``elevenlabs_music`` (migration 1510) routes here. One paid call returns the whole track as raw audio with
no usage object, so the adapter builds the billed usage itself (``audio_second_output``, $/second) BEFORE storing, and
anything after the paid call carries that usage (``paid_output``), so a storage failure never re-buys the track and
never records $0. A body too small for the asked length is a cut-off take (``speech/take_check``), retried by the run.

Instrumental only (``force_instrumental``). The length rides ``config.duration_seconds`` (the one canonical field every
generator takes); ElevenLabs accepts 3 s to 300 s and returns that length, so the caller's margin is the only slack.
A prompt the provider declines (``bad_prompt``) comes back as an EMPTY response with a content-filter finish reason,
exactly like a Gemini decline, so the caller's "retry once with a safer wording" path is the same for every music model.
"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any

from matrx_utils import vcprint

from matrx_ai.config import AudioContent, UnifiedConfig, UnifiedMessage, UnifiedResponse
from matrx_ai.config.finish_reason import FinishReason

from .client import get_elevenlabs_client

if TYPE_CHECKING:
    from matrx_ai.catalog.models import ResolvedCallProfile

#: Provider limits (https://elevenlabs.io/docs/overview/capabilities/music): 3 s to 5 min per generation.
MIN_MUSIC_SECONDS = 3
MAX_MUSIC_SECONDS = 300
#: Used only when the caller named no length at all (a bed is always asked for the video's length by the pipeline).
DEFAULT_MUSIC_KEY = "default_length_seconds"
#: KNOB MIRROR of platform.feature_knob "ai.music" "default_length_seconds"
DEFAULT_MUSIC_MIRROR = 30


def default_music_seconds() -> int:
    """The length asked for when the caller named none, live (``ai.music.default_length_seconds``)."""
    from matrx_ai.knobs import package_knob_number

    return package_knob_number("ai.music", DEFAULT_MUSIC_KEY, DEFAULT_MUSIC_MIRROR,
                               low=MIN_MUSIC_SECONDS, high=MAX_MUSIC_SECONDS)
_OUTPUT_FORMAT = "mp3_44100_128"
#: ElevenLabs error statuses (body ``detail.status``) that mean the PROMPT was declined, not that the service failed.
_DECLINED_STATUSES = frozenset({"bad_prompt", "bad_composition_plan"})


def music_length_seconds(config: UnifiedConfig) -> int:
    """The length to ask for: the config's own ``duration_seconds`` clamped to the provider's 3-300 s."""
    asked = getattr(config, "duration_seconds", None) or default_music_seconds()
    return int(min(MAX_MUSIC_SECONDS, max(MIN_MUSIC_SECONDS, round(float(asked)))))


def music_prompt_text(config: UnifiedConfig) -> str:
    """The last user message's text (the bed's description)."""
    for msg in reversed(getattr(config, "messages", None) or []):
        if str(getattr(msg, "role", "")).lower() != "user":
            continue
        parts = [getattr(c, "text", None) for c in (getattr(msg, "content", None) or [])]
        text = " ".join(p for p in parts if isinstance(p, str) and p.strip()).strip()
        if text:
            return text
    raise ValueError("[ElevenLabs Music] the request has no prompt text; describe the music in the user message.")


def declined_status(exc: BaseException) -> str | None:
    """``bad_prompt`` (etc.) when ElevenLabs answered that it will not make music from this wording, else None."""
    body = getattr(exc, "body", None)
    detail = body.get("detail") if isinstance(body, dict) else None
    status = detail.get("status") if isinstance(detail, dict) else None
    return status if status in _DECLINED_STATUSES else None


class ElevenLabsMusic:
    endpoint_name: str = "[ELEVENLABS MUSIC]"

    def __init__(self) -> None:
        self.client = get_elevenlabs_client()

    async def execute(self, unified_config: UnifiedConfig, profile: ResolvedCallProfile, debug: bool = False) -> UnifiedResponse:
        try:
            return await self._execute_music(unified_config, profile)
        except Exception as e:
            if getattr(e, "error_info", None) is not None:
                raise
            from matrx_ai.providers.errors import classify_elevenlabs_error

            e.error_info = classify_elevenlabs_error(e)
            raise

    def _compose(self, prompt: str, model_id: str, length_ms: int) -> bytes:
        stream = self.client.music.compose(
            prompt=prompt,
            music_length_ms=length_ms,
            model_id=model_id,
            force_instrumental=True,
            output_format=_OUTPUT_FORMAT,
        )
        return b"".join(chunk for chunk in stream if isinstance(chunk, bytes))

    async def _execute_music(self, unified_config: UnifiedConfig, profile: ResolvedCallProfile) -> UnifiedResponse:
        prompt = music_prompt_text(unified_config)
        seconds = music_length_seconds(unified_config)
        model_id = profile.provider_model_id
        matrx_model_name = unified_config.model
        vcprint(f"[ElevenLabs Music] {model_id} {seconds}s", color="blue")
        try:
            audio = await asyncio.to_thread(self._compose, prompt, model_id, seconds * 1000)
        except Exception as exc:
            status = declined_status(exc)
            if status is None:
                raise
            vcprint(f"[ElevenLabs Music] declined the wording ({status}); nothing was generated", color="yellow")
            return UnifiedResponse(
                messages=[UnifiedMessage(role="assistant", content=[], metadata={"finish_reason": FinishReason.CONTENT_FILTER.value,
                                                                                  "declined": status})],
                usage=None,
                finish_reason=FinishReason.CONTENT_FILTER,
            )
        if not audio:
            raise ValueError("ElevenLabs returned an empty music body.")

        from matrx_ai.config.usage_config import build_audio_seconds_billed_usage_async
        from matrx_ai.providers.paid_output import mark_failed_after_paid_call, store_paid_output
        from matrx_ai.speech.take_check import raise_if_truncated_music

        usage = await build_audio_seconds_billed_usage_async(
            seconds=seconds,
            matrx_model_name=matrx_model_name,
            provider_model_name=model_id,
            api="elevenlabs",
            extra_metadata={"music_length_requested_s": seconds, "audio_bytes": len(audio)},
        )
        raise_if_truncated_music(provider="elevenlabs", audio_size_bytes=len(audio), seconds=seconds, usage=usage)
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
                    extra_metadata={"generation": {"kind": "music", "model": model_id, "length_seconds": seconds, "instrumental": True}},
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
                duration_ms=envelope.duration_ms,
                metadata={"generation": {"kind": "music", "model": model_id, "length_seconds": seconds}},
            )
        except Exception as exc:
            mark_failed_after_paid_call(exc, provider="elevenlabs", modality="audio", usage=usage)
            raise
        return UnifiedResponse(
            messages=[UnifiedMessage(role="assistant", content=[item], metadata={"finish_reason": "stop"})],
            usage=usage,
            finish_reason=FinishReason.STOP,
        )
