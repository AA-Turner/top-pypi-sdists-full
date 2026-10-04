"""Catalog-routed Google runtimes whose wire contracts are not chat turns.

The Live, Lyria, embeddings, and background Interactions APIs all resolve an
``ai.offering`` through the same catalog as chat.  They deliberately bypass
``UnifiedAIClient.execute`` because none of them is a request/response turn;
embeddings still dispatch through the shared seam
(``UnifiedAIClient._dispatch_with_billing_net``). Live and Lyria are
websocket sessions and remain outside it — but a provider failure on either
(session open, a send, the receive loop) still takes THE provider failure door
(``failure_report.report_provider_failure``) and leaves its classification on
the exception as ``error_info``, so a host shows the person the classified
sentence, never the provider's raw text.
"""

from __future__ import annotations

import base64
import warnings
from collections.abc import AsyncIterator, Sequence
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from enum import Enum
from typing import TYPE_CHECKING, Any, Literal

from google.genai import types
from pydantic import BaseModel, ConfigDict, Field, model_validator

from matrx_ai.providers.google.google_client import get_google_client
from matrx_ai.providers.sdk_drift import route_undeclared_params

if TYPE_CHECKING:
    from matrx_ai.catalog.models import ResolvedCallProfile


@asynccontextmanager
async def _provider_failures(profile: ResolvedCallProfile, route: str) -> AsyncIterator[None]:
    """Wrap ONE provider operation of a realtime session: a failure is
    classified and reported through the provider failure door, its
    classification attached as ``error_info``, then re-raised unchanged."""
    try:
        yield
    except Exception as exc:
        from matrx_ai.providers.failure_report import report_provider_failure

        info = await report_provider_failure(
            exc, provider="google", model=profile.provider_model_id, route=route
        )
        if info is not None and getattr(exc, "error_info", None) is None:
            try:
                exc.error_info = info  # type: ignore[attr-defined]
            except Exception:  # noqa: BLE001 — an immutable exception keeps its own text
                pass
        raise


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


_LIVE_ROUTE = "google/live"
_MUSIC_ROUTE = "google/music"


class _ReportedSession:
    """A Live SDK session whose every send takes the provider failure door.

    ``send`` translates many client message kinds into one of three SDK calls;
    wrapping the calls here keeps the translation free of try/except while a
    malformed CLIENT message (bad base64, unknown kind) still raises as the
    client's own error, never as a provider failure.
    """

    def __init__(self, session: Any, profile: ResolvedCallProfile, route: str) -> None:
        self._session = session
        self._profile = profile
        self._route = route

    async def send_realtime_input(self, **kwargs: Any) -> None:
        async with _provider_failures(self._profile, self._route):
            await self._session.send_realtime_input(**kwargs)

    async def send_client_content(self, **kwargs: Any) -> None:
        async with _provider_failures(self._profile, self._route):
            await self._session.send_client_content(**kwargs)


def _translate_session_settings(
    profile: ResolvedCallProfile, settings: dict[str, Any]
) -> dict[str, Any]:
    """Canonical Live session settings -> the cells' translated value per canonical key.

    Runs ``translate_session_settings`` (the shared outbound pass), then reads
    each key back under its rule's provider key. A key the cells dropped comes
    back absent, so the SDK config omits it rather than sending a raw value.
    """
    from matrx_ai.catalog.controls import flatten_dotted
    from matrx_ai.providers.outbound_params import translate_session_settings

    controls = profile.controls
    params = translate_session_settings(settings, controls, model=profile.provider_model_id)
    flat = {**params, **flatten_dotted(params)}
    out: dict[str, Any] = {}
    for key in settings:
        rule = controls.rules.get(key)
        wire_key = (getattr(rule, "provider_key", None) if rule is not None else None) or key
        if wire_key in flat:
            out[key] = flat[wire_key]
    return out


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
        # The session settings go through the translation cells like every
        # other seam (thinking level, turn coverage, response modalities); this
        # class only shapes the translated values into the SDK config.
        translated = _translate_session_settings(
            self.profile,
            {
                "thinking_level": self.options.thinking_level,
                "turn_coverage": self.options.turn_coverage,
                "response_modalities": self.options.response_modalities,
            },
        )
        thinking_level = translated.get("thinking_level")
        config = types.LiveConnectConfig(
            response_modalities=translated.get("response_modalities"),
            thinking_config=(
                types.ThinkingConfig(thinking_level=str(thinking_level).upper())
                if thinking_level is not None
                else None
            ),
            realtime_input_config=types.RealtimeInputConfig(
                automatic_activity_detection=vad,
                turn_coverage=translated.get("turn_coverage"),
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
        async with _provider_failures(self.profile, _LIVE_ROUTE):
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
        session = _ReportedSession(self._require_session(), self.profile, _LIVE_ROUTE)
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
        async with _provider_failures(self.profile, _LIVE_ROUTE):
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
        async with _provider_failures(self.profile, _MUSIC_ROUTE):
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
        weighted = [types.WeightedPrompt(text=item.text, weight=item.weight) for item in prompts]
        async with _provider_failures(self.profile, _MUSIC_ROUTE):
            await self._require_session().set_weighted_prompts(weighted)

    async def set_config(self, config: dict[str, Any]) -> None:
        # Music settings (bpm, density, guidance, temperature…) go through the
        # cells like every session seam; a key the cells drop is not sent.
        generation_config = types.LiveMusicGenerationConfig(
            **_translate_session_settings(self.profile, dict(config))
        )
        async with _provider_failures(self.profile, _MUSIC_ROUTE):
            await self._require_session().set_music_generation_config(generation_config)

    async def control(self, action: Literal["play", "pause", "stop", "reset_context"]) -> None:
        operation = getattr(self._require_session(), action)
        async with _provider_failures(self.profile, _MUSIC_ROUTE):
            await operation()

    async def receive(self) -> AsyncIterator[dict[str, Any]]:
        async with _provider_failures(self.profile, _MUSIC_ROUTE):
            async for message in self._require_session().receive():
                yield _json_safe(message)


class GoogleEmbeddingResult(BaseModel):
    model: str
    dimensions: int
    vectors: list[list[float]]


class GoogleEmbeddingPart(BaseModel):
    """A public embedding input part translated only at the Google boundary."""

    model_config = ConfigDict(extra="forbid")

    type: Literal["text", "uri", "inline"]
    text: str | None = None
    uri: str | None = None
    data: str | None = None
    mime_type: str | None = None

    @model_validator(mode="after")
    def validate_payload(self) -> GoogleEmbeddingPart:
        if self.type == "text" and self.text:
            return self
        if self.type == "uri" and self.uri:
            return self
        if self.type == "inline" and self.data and self.mime_type:
            try:
                base64.b64decode(self.data, validate=True)
            except ValueError as exc:
                raise ValueError("inline embedding data must be valid base64") from exc
            return self
        raise ValueError(f"Incomplete {self.type!r} embedding part")

    def to_google(self) -> types.Part:
        if self.type == "text" and self.text:
            return types.Part.from_text(text=self.text)
        if self.type == "uri" and self.uri:
            return types.Part.from_uri(file_uri=self.uri, mime_type=self.mime_type)
        if self.type == "inline" and self.data and self.mime_type:
            return types.Part.from_bytes(
                data=base64.b64decode(self.data, validate=True),
                mime_type=self.mime_type,
            )
        raise AssertionError("GoogleEmbeddingPart was not validated")


def embedding_contents(
    inputs: Sequence[str | Sequence[GoogleEmbeddingPart]],
) -> list[Any]:
    """Translate the host's stable embedding envelope at the provider seam."""
    contents: list[Any] = []
    for value in inputs:
        if isinstance(value, str):
            contents.append(value)
        else:
            contents.append(types.Content(role="user", parts=[part.to_google() for part in value]))
    return contents


#: Extra sends a transient, unbilled embedding refusal gets at the dispatch
#: seam. google-genai never retries by default, so before this a dropped
#: connection failed the whole ingestion. CAPS.
EMBEDDING_TRANSIENT_RETRIES = 2


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
        # The width goes through the ``dimensions`` cell (range, product
        # default) like every other seam — never a hand-written range check.
        translated = _translate_session_settings(
            self.profile, {"dimensions": output_dimensionality}
        )
        config = types.EmbedContentConfig(
            output_dimensionality=translated.get("dimensions"),
            task_type=task_type,
            title=title,
        )
        from matrx_ai.providers.errors import mark_billing_checked
        from matrx_ai.providers.unified_client import UnifiedAIClient

        async def _embed() -> Any:
            try:
                return await get_google_client().aio.models.embed_content(
                    model=self.profile.provider_model_id,
                    contents=contents,
                    config=config,
                )
            except BaseException as exc:
                # A refused embedding returns nothing billable: the adapter
                # looked, so LAYER 2 must not report a forgotten capture.
                mark_billing_checked(exc)
                raise

        # The shared dispatch seam: admission on the Google pool, the
        # out-of-credit alarm and LAYER 2 — for every caller of this runtime.
        # An embedding is a pure function of its input and bills only a
        # returned response: a refused batch is safe to send again.
        response = await UnifiedAIClient._dispatch_with_billing_net(
            _embed, profile=self.profile, transient_retries=EMBEDDING_TRANSIENT_RETRIES
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
            _create = get_google_client().aio.interactions.create
            result = await _create(**route_undeclared_params(_create, kwargs, provider="google"))
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
    "GoogleEmbeddingPart",
    "GoogleEmbeddingResult",
    "GoogleEmbeddingRuntime",
    "GoogleLiveOptions",
    "GoogleLiveSession",
    "GoogleMusicSession",
    "WeightedMusicPrompt",
    "embedding_contents",
]
