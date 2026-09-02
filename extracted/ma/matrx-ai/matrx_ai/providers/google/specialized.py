"""Catalog-routed Google runtimes whose wire contracts are not chat turns.

The Live, Lyria, embeddings, and background Interactions APIs all resolve an
``ai.offering`` through the same catalog as chat.  They deliberately bypass
``UnifiedAIClient.execute`` because none of them is a request/response turn.
"""

from __future__ import annotations

import base64
import warnings
from collections.abc import AsyncIterator, Sequence
from contextlib import AbstractAsyncContextManager
from enum import Enum
from typing import TYPE_CHECKING, Any, Literal

from google.genai import types
from pydantic import BaseModel, ConfigDict, Field, model_validator

from matrx_ai.providers.google.google_client import get_google_client

if TYPE_CHECKING:
    from matrx_ai.catalog.models import ResolvedCallProfile


def _require_wire(profile: ResolvedCallProfile, expected: str) -> None:
    if profile.wire_format != expected:
        raise ValueError(
            f"Model {profile.model_name!r} resolved to {profile.wire_format!r}; "
            f"this runtime requires {expected!r}."
        )


def _json_safe(value: Any) -> Any:
    """Convert SDK models (including binary PCM) into JSON-safe wire data."""
    if isinstance(value, bytes):
        return base64.b64encode(value).decode("ascii")
    if isinstance(value, Enum):
        return _json_safe(value.value)
    if isinstance(value, BaseModel):
        return _json_safe(value.model_dump(mode="python", exclude_none=True))
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, list | tuple):
        return [_json_safe(item) for item in value]
    if hasattr(value, "__dict__"):
        return _json_safe(vars(value))
    return value


class GoogleLiveOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    thinking_level: Literal["minimal", "low", "medium", "high"] = "minimal"
    turn_coverage: Literal["TURN_INCLUDES_ONLY_ACTIVITY", "TURN_INCLUDES_ALL_INPUT"] = (
        "TURN_INCLUDES_ONLY_ACTIVITY"
    )
    response_modalities: list[Literal["TEXT", "AUDIO"]] = Field(default_factory=lambda: ["AUDIO"])
    vad_config: dict[str, Any] = Field(default_factory=dict)
    session_handle: str | None = None
    initial_history_in_client_content: bool = False
    input_audio_transcription: bool = True
    output_audio_transcription: bool = True
    system_instruction: str | None = None

    @model_validator(mode="after")
    def _modalities_are_unique(self) -> GoogleLiveOptions:
        if not self.response_modalities:
            raise ValueError("response_modalities must contain TEXT and/or AUDIO")
        self.response_modalities = list(dict.fromkeys(self.response_modalities))
        return self


class GoogleLiveSession:
    """Thin async session around ``BidiGenerateContent``.

    The host owns authentication and WebSocket fan-in/fan-out.  This class owns
    only provider protocol translation and keeps the resumable handle visible.
    """

    def __init__(self, profile: ResolvedCallProfile, options: GoogleLiveOptions) -> None:
        _require_wire(profile, "google_live")
        self.profile = profile
        self.options = options
        self._context: AbstractAsyncContextManager[Any] | None = None
        self._session: Any = None

    async def __aenter__(self) -> GoogleLiveSession:
        vad = types.AutomaticActivityDetection(**self.options.vad_config)
        config = types.LiveConnectConfig(
            response_modalities=self.options.response_modalities,
            thinking_config=types.ThinkingConfig(
                thinking_level=self.options.thinking_level.upper()
            ),
            realtime_input_config=types.RealtimeInputConfig(
                automatic_activity_detection=vad,
                turn_coverage=self.options.turn_coverage,
            ),
            session_resumption=types.SessionResumptionConfig(handle=self.options.session_handle),
            history_config=types.HistoryConfig(
                initial_history_in_client_content=(self.options.initial_history_in_client_content)
            ),
            input_audio_transcription=(
                types.AudioTranscriptionConfig() if self.options.input_audio_transcription else None
            ),
            output_audio_transcription=(
                types.AudioTranscriptionConfig()
                if self.options.output_audio_transcription
                else None
            ),
            system_instruction=self.options.system_instruction,
        )
        self._context = get_google_client().aio.live.connect(
            model=self.profile.provider_model_id,
            config=config,
        )
        self._session = await self._context.__aenter__()
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        if self._context is not None:
            await self._context.__aexit__(exc_type, exc, tb)

    def _require_session(self) -> Any:
        if self._session is None:
            raise RuntimeError("GoogleLiveSession must be entered before use")
        return self._session

    async def send(self, message: dict[str, Any]) -> None:
        session = self._require_session()
        kind = str(message.get("type", ""))
        if kind == "audio":
            data = base64.b64decode(str(message["data"]))
            await session.send_realtime_input(
                audio=types.Blob(
                    data=data,
                    mime_type=str(message.get("mime_type") or "audio/pcm;rate=16000"),
                )
            )
            return
        if kind in {"image", "video"}:
            blob = types.Blob(
                data=base64.b64decode(str(message["data"])),
                mime_type=str(message["mime_type"]),
            )
            await session.send_realtime_input(**{kind: blob})
            return
        if kind == "realtime_text":
            await session.send_realtime_input(text=str(message["text"]))
            return
        if kind == "client_content":
            await session.send_client_content(
                turns=message.get("turns"),
                turn_complete=bool(message.get("turn_complete", True)),
            )
            return
        if kind == "audio_stream_end":
            await session.send_realtime_input(audio_stream_end=True)
            return
        if kind == "activity_start":
            await session.send_realtime_input(activity_start=types.ActivityStart())
            return
        if kind == "activity_end":
            await session.send_realtime_input(activity_end=types.ActivityEnd())
            return
        raise ValueError(f"Unsupported Google Live client message type: {kind!r}")

    async def receive(self) -> AsyncIterator[dict[str, Any]]:
        async for message in self._require_session().receive():
            yield _json_safe(message)


class WeightedMusicPrompt(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(min_length=1, max_length=500)
    weight: float

    @model_validator(mode="after")
    def _weight_is_nonzero(self) -> WeightedMusicPrompt:
        if self.weight == 0:
            raise ValueError("Lyria prompt weights must be non-zero")
        return self


class GoogleMusicSession:
    """Persistent Lyria RealTime session (48 kHz stereo PCM output)."""

    def __init__(self, profile: ResolvedCallProfile) -> None:
        _require_wire(profile, "google_music_realtime")
        self.profile = profile
        self._context: AbstractAsyncContextManager[Any] | None = None
        self._session: Any = None

    async def __aenter__(self) -> GoogleMusicSession:
        self._context = get_google_client().aio.live.music.connect(
            model=self.profile.provider_model_id
        )
        self._session = await self._context.__aenter__()
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        if self._context is not None:
            await self._context.__aexit__(exc_type, exc, tb)

    def _require_session(self) -> Any:
        if self._session is None:
            raise RuntimeError("GoogleMusicSession must be entered before use")
        return self._session

    async def set_prompts(self, prompts: Sequence[WeightedMusicPrompt]) -> None:
        if not prompts:
            raise ValueError("Lyria requires at least one weighted prompt")
        await self._require_session().set_weighted_prompts(
            [types.WeightedPrompt(text=item.text, weight=item.weight) for item in prompts]
        )

    async def set_config(self, config: dict[str, Any]) -> None:
        await self._require_session().set_music_generation_config(
            types.LiveMusicGenerationConfig(**config)
        )

    async def control(self, action: Literal["play", "pause", "stop", "reset_context"]) -> None:
        await getattr(self._require_session(), action)()

    async def receive(self) -> AsyncIterator[dict[str, Any]]:
        async for message in self._require_session().receive():
            yield _json_safe(message)


class GoogleEmbeddingResult(BaseModel):
    model: str
    dimensions: int
    vectors: list[list[float]]


class GoogleEmbeddingRuntime:
    def __init__(self, profile: ResolvedCallProfile) -> None:
        _require_wire(profile, "google_embeddings")
        self.profile = profile

    async def embed(
        self,
        contents: Any,
        *,
        output_dimensionality: int | None = None,
        task_type: str | None = None,
        title: str | None = None,
    ) -> GoogleEmbeddingResult:
        if output_dimensionality is not None and not 128 <= output_dimensionality <= 3072:
            raise ValueError("output_dimensionality must be between 128 and 3072")
        config = types.EmbedContentConfig(
            output_dimensionality=output_dimensionality,
            task_type=task_type,
            title=title,
        )
        response = await get_google_client().aio.models.embed_content(
            model=self.profile.provider_model_id,
            contents=contents,
            config=config,
        )
        vectors = [list(item.values or []) for item in (response.embeddings or [])]
        dimensions = len(vectors[0]) if vectors else int(output_dimensionality or 0)
        return GoogleEmbeddingResult(
            model=self.profile.provider_model_id,
            dimensions=dimensions,
            vectors=vectors,
        )


class GoogleBackgroundInteractionRuntime:
    """Create and inspect durable Google Interactions background work."""

    def __init__(self, profile: ResolvedCallProfile) -> None:
        _require_wire(profile, "google_interactions")
        self.profile = profile

    async def create(
        self,
        interaction_input: Any,
        *,
        previous_interaction_id: str | None = None,
    ) -> dict[str, Any]:
        kwargs: dict[str, Any] = {
            "agent": self.profile.provider_model_id,
            "input": interaction_input,
            "background": True,
            "store": True,
        }
        if previous_interaction_id:
            kwargs["previous_interaction_id"] = previous_interaction_id
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore", message="Interactions usage is experimental.*", category=UserWarning
            )
            result = await get_google_client().aio.interactions.create(**kwargs)
        return _json_safe(result)

    async def get(self, interaction_id: str) -> dict[str, Any]:
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore", message="Interactions usage is experimental.*", category=UserWarning
            )
            result = await get_google_client().aio.interactions.get(id=interaction_id)
        return _json_safe(result)


__all__ = [
    "GoogleBackgroundInteractionRuntime",
    "GoogleEmbeddingResult",
    "GoogleEmbeddingRuntime",
    "GoogleLiveOptions",
    "GoogleLiveSession",
    "GoogleMusicSession",
    "WeightedMusicPrompt",
]
