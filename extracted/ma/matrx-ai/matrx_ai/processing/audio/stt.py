from __future__ import annotations

import asyncio
import base64
import io
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from matrx_ai.catalog.models import ResolvedCallProfile


class STTRequest(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, extra="forbid")

    audio_source: str | bytes | io.BytesIO
    model: str
    operation: Literal["transcription", "translation"] = "transcription"
    language: str | None = None
    response_format: Literal["json", "verbose_json", "text"] = "verbose_json"
    temperature: float = Field(default=0.0, ge=0.0, le=1.0)
    timestamp_granularities: list[Literal["word", "segment"]] | None = None


class STTUsage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    duration_seconds: float = 0.0
    billed_duration: float = 0.0
    model: str
    matrx_model_name: str
    api: str
    offering_id: str = ""
    usage_basis: str
    language: str | None = None
    operation: Literal["transcription", "translation"] = "transcription"
    file_size_mb: float = 0.0
    response_format: str = "json"
    metadata: dict[str, Any] = Field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Return the legacy cache/storage shape."""
        return self.model_dump()

    def to_token_usage(self):
        """Build basis-aware usage for the existing request cost spine."""
        from matrx_ai.config.usage_config import TokenUsage

        input_units = duration_to_stt_input_units(
            self.usage_basis, self.billed_duration
        )
        return TokenUsage(
            input_tokens=input_units,
            output_tokens=0,
            cached_input_tokens=0,
            matrx_model_name=self.matrx_model_name,
            provider_model_name=self.model,
            api=self.api,
            offering_id=self.offering_id,
            offering_route="preferred",
            metadata={
                **self.metadata,
                "duration_seconds": self.duration_seconds,
                "billed_duration": self.billed_duration,
                "billing_kind": f"synthetic:{self.usage_basis}",
                "operation": self.operation,
            },
        )


def duration_to_stt_input_units(usage_basis: str, billed_seconds: float) -> int:
    """Convert audio duration into the synthetic units owned by a pricing basis."""
    if usage_basis == "audio_second_input":
        return int(billed_seconds * 100)
    if usage_basis == "audio_hour_input":
        return int(billed_seconds / 3600 * 1_000_000)
    raise ValueError(
        f"STT usage basis {usage_basis!r} is unsupported. Add an explicit "
        "duration-to-unit conversion before routing this offering."
    )


class STTResult(BaseModel):
    text: str
    usage: STTUsage
    segments: list[Any] | None = None
    language: str | None = None
    duration: float | None = None
    quality_metrics: dict[str, Any] = Field(default_factory=dict)
    raw_response: dict[str, Any] | None = None


@runtime_checkable
class STTClient(Protocol):
    async def execute(self, request: STTRequest, profile: ResolvedCallProfile) -> STTResult: ...


async def prepare_audio_file(
    audio_source: str | bytes | io.BytesIO,
    *,
    max_file_size_mb: float,
) -> tuple[tuple[str, bytes], float]:
    if isinstance(audio_source, str):
        if audio_source.startswith(("http://", "https://")):
            from matrx_ai.media import fetch_media

            audio_data = await asyncio.to_thread(
                fetch_media, audio_source, target_format="bytes"
            )
            filename = "audio.wav"
        elif audio_source.startswith("data:"):
            audio_data = base64.b64decode(audio_source.split(",", 1)[1])
            filename = "audio.wav"
        else:
            path = Path(audio_source)
            if not path.exists():
                raise FileNotFoundError(f"Audio file not found: {audio_source}")
            audio_data = path.read_bytes()
            filename = path.name
    elif isinstance(audio_source, bytes):
        audio_data = audio_source
        filename = "audio.wav"
    elif isinstance(audio_source, io.BytesIO):
        audio_data = audio_source.getvalue()
        filename = "audio.wav"
    else:
        raise TypeError(f"Unsupported audio_source type: {type(audio_source).__name__}")
    size_mb = len(audio_data) / (1024 * 1024)
    if size_mb > max_file_size_mb:
        raise ValueError(
            f"Audio file too large ({size_mb:.2f} MB); provider limit is "
            f"{max_file_size_mb:.2f} MB. Chunk the audio before transcription."
        )
    return (filename, audio_data), size_mb


async def execute_stt(request: STTRequest) -> STTResult:
    from matrx_ai.catalog.resolve import resolve_call_profile
    from matrx_ai.providers.unified_client import UnifiedAIClient

    profile = await resolve_call_profile(request.model)
    if profile.client_attr != "stt":
        raise ValueError(
            f"Model {profile.model_name!r} resolves to {profile.client_attr!r}, not the "
            "catalog STT channel. Point its offering at a *_stt ai.api row."
        )
    client = getattr(UnifiedAIClient(), profile.wire_format)
    if not isinstance(client, STTClient):
        raise TypeError(
            f"Provider factory {profile.wire_format!r} does not implement STTClient.execute"
        )
    return await client.execute(request, profile)


__all__ = [
    "STTClient",
    "STTRequest",
    "STTResult",
    "STTUsage",
    "execute_stt",
    "duration_to_stt_input_units",
    "prepare_audio_file",
]
