from __future__ import annotations

from typing import TYPE_CHECKING, Any

from groq import AsyncGroq

from matrx_ai.processing.audio.stt import (
    STTRequest,
    STTResult,
    STTUsage,
    prepare_audio_file,
)
from matrx_ai.providers.keys import resolve_api_key
from matrx_ai.providers.outbound_params import resolve_outbound_params

if TYPE_CHECKING:
    from matrx_ai.catalog.models import ResolvedCallProfile

_clients: dict[str, AsyncGroq] = {}


def _client() -> AsyncGroq:
    key = resolve_api_key("GROQ_API_KEY", required=True)
    assert key is not None
    client = _clients.get(key)
    if client is None:
        client = AsyncGroq(api_key=key)
        _clients[key] = client
    return client


class GroqSTT:
    """Catalog-dispatched Groq speech-to-text client."""

    async def execute(self, request: STTRequest, profile: ResolvedCallProfile) -> STTResult:
        stt_meta = profile.offering_metadata.get("stt", {})
        max_size = float(stt_meta.get("max_file_size_mb", 100.0))
        file_tuple, file_size_mb = await prepare_audio_file(
            request.audio_source,
            max_file_size_mb=max_size,
        )
        params = resolve_outbound_params(request, profile.controls)
        params.update(
            file=file_tuple,
            model=profile.provider_model_id,
            response_format=request.response_format,
        )
        if request.timestamp_granularities and request.response_format == "verbose_json":
            params["timestamp_granularities"] = request.timestamp_granularities
        operation = request.operation
        if operation == "translation":
            response = await _client().audio.translations.create(**params)
        else:
            response = await _client().audio.transcriptions.create(**params)
        return self._parse_response(
            response,
            profile=profile,
            request=request,
            file_size_mb=file_size_mb,
        )

    @staticmethod
    def _parse_response(
        response: Any,
        *,
        profile: ResolvedCallProfile,
        request: STTRequest,
        file_size_mb: float,
    ) -> STTResult:
        if isinstance(response, str):
            raw: dict[str, Any] = {"text": response}
        elif hasattr(response, "model_dump"):
            raw = response.model_dump()
        elif isinstance(response, dict):
            raw = dict(response)
        else:
            raw = {
                key: getattr(response, key)
                for key in ("text", "language", "duration", "segments")
                if getattr(response, key, None) is not None
            }
        duration = float(raw.get("duration") or 0.0)
        stt_meta = profile.offering_metadata.get("stt", {})
        minimum = float(stt_meta.get("minimum_billed_seconds", 0.0))
        segments = raw.get("segments")
        quality: dict[str, Any] = {}
        if isinstance(segments, list) and segments:
            for key in ("avg_logprob", "no_speech_prob", "compression_ratio"):
                values = [segment.get(key) for segment in segments if segment.get(key) is not None]
                if values:
                    quality[key] = sum(float(value) for value in values) / len(values)
        usage = STTUsage(
            duration_seconds=duration,
            billed_duration=max(duration, minimum),
            model=profile.provider_model_id,
            matrx_model_name=profile.model_name,
            api=profile.vendor,
            offering_id=profile.offering_id,
            usage_basis=profile.usage_basis or "",
            language=raw.get("language") or request.language,
            operation=request.operation,
            file_size_mb=file_size_mb,
            response_format=request.response_format,
        )
        return STTResult(
            text=str(raw.get("text") or ""),
            usage=usage,
            segments=segments if isinstance(segments, list) else None,
            language=raw.get("language") or request.language,
            duration=duration,
            quality_metrics=quality,
            raw_response=raw,
        )


# Compatibility result names; the old synchronous, model-owning client is gone.
TranscriptionResult = STTResult
TranscriptionUsage = STTUsage

__all__ = ["GroqSTT", "TranscriptionResult", "TranscriptionUsage"]
