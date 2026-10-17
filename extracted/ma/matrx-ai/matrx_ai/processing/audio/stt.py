from __future__ import annotations

import asyncio
import base64
import io
import logging
import math
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from matrx_ai.catalog.models import ResolvedCallProfile


class STTRequest(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, extra="forbid")

    audio_source: str | bytes | io.BytesIO
    model: str
    #: The chosen CLASS of ``model`` (an ai.offering of it); ``None`` = its preferred class.
    offering_id: str | None = None
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


class STTWord(BaseModel):
    """One spoken word on the audio clock (seconds). ``confidence``/``speaker``
    are filled only when the provider supplies them."""

    text: str
    start: float
    end: float
    confidence: float | None = None
    speaker: str | None = None


def clamp_words_monotonic(raw_words: list[Any] | None) -> list[STTWord]:
    """The ONE shared clean-up for provider word timings (rule ``proportional@1``).

    Whisper-class providers stretch each word's end to the next start and let
    ~4 in 90 words overlap their neighbour. Provider order is kept (it is the spoken
    order; never re-sorted), and where a
    word starts inside its predecessor the two share their combined span in
    proportion to their raw durations (see ``_apply_proportional_clamp``), so
    start_i <= end_i <= start_(i+1). Honest gaps (start > previous end) are
    left untouched. Output is identical to the TypeScript ``clampWordTimings``
    on the shared golden fixture. Accepts
    dicts or objects with ``word``/``text``, ``start``, ``end``; skips items
    without text or numeric times.
    """
    items: list[STTWord] = []
    for raw in raw_words or []:
        get = raw.get if isinstance(raw, dict) else lambda k, d=None, _r=raw: getattr(_r, k, d)
        text = get("word") if get("word") is not None else get("text")
        start, end = get("start"), get("end")
        if not isinstance(text, str) or not text.strip():
            continue
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)):
            continue
        conf = get("confidence")
        speaker = get("speaker") if get("speaker") is not None else get("speaker_id")
        items.append(
            STTWord(
                text=text.strip(),
                start=float(start),
                end=float(end),
                confidence=float(conf) if isinstance(conf, (int, float)) else None,
                speaker=str(speaker) if speaker is not None else None,
            )
        )
    return _apply_proportional_clamp(items)


#: Identifier of THE clamp rule; recorded on every Alignment (``source.clamp``).
WORD_CLAMP_RULE = "proportional@1"


def _round4(n: float) -> float:
    # JS ``Math.round(n * 10000) / 10000`` (half up), not Python's banker's rounding:
    # the TypeScript twin (apps/shared/media/src/video/words.ts) must match to the bit.
    return math.floor(n * 10000 + 0.5) / 10000


def _apply_proportional_clamp(items: list[STTWord]) -> list[STTWord]:
    """Rule ``proportional@1`` over words in provider order (twin of ``clampWordTimings``).

    Walk in order. When word i starts before word i-1 ends, the two share the span
    [lo, hi] with lo = (clamped) start of i-1 and hi = max(end i-1, end i); the boundary
    splits it in proportion to the two RAW durations (rounded to 0.1 ms). Every other word is
    left as is, so an honest silence (start > previous end) is never filled; a start never
    precedes the previous start and an end never precedes its own start.
    """
    raw = [(w.start, w.end) for w in items]
    out = [w.model_copy() for w in items]
    for i, cur in enumerate(out):
        if cur.end < cur.start:
            cur.end = cur.start
        if i == 0:
            continue
        prev = out[i - 1]
        if cur.start < prev.start:
            cur.start = prev.start
        if cur.end < cur.start:
            cur.end = cur.start
        if cur.start < prev.end:
            lo = prev.start
            hi = max(prev.end, cur.end)
            d_prev = max(0.0, raw[i - 1][1] - raw[i - 1][0])
            d_cur = max(0.0, raw[i][1] - raw[i][0])
            share = d_prev / (d_prev + d_cur) if d_prev + d_cur > 0 else 0.5
            split = _round4(lo + (hi - lo) * share)
            prev.end = split
            cur.start = split
            cur.end = hi
    return out


#: Why ``STTResult.words`` is what it is. Asking for words and getting none is
#: never silent: ``unsupported_by_provider`` (the adapter cannot supply them) and
#: ``none_returned`` (it can, this clip yielded none) both announce themselves.
WordsStatus = Literal["not_requested", "provided", "unsupported_by_provider", "none_returned"]


def words_status_for(request: STTRequest, result: STTResult, *, supported: bool) -> WordsStatus:
    """The ONE place that decides a result's ``words_status`` (every adapter inherits it)."""
    if "word" not in (request.timestamp_granularities or []):
        return "not_requested"
    if result.words:
        return "provided"
    return "none_returned" if supported else "unsupported_by_provider"


class STTResult(BaseModel):
    text: str
    usage: STTUsage
    segments: list[Any] | None = None
    #: Word timings, monotonic (see ``clamp_words_monotonic``). Filled only
    #: when the request asked for the "word" granularity.
    words: list[STTWord] | None = None
    #: Set by ``execute_stt`` from the request + adapter capability; see ``WordsStatus``.
    words_status: WordsStatus = "not_requested"
    language: str | None = None
    duration: float | None = None
    quality_metrics: dict[str, Any] = Field(default_factory=dict)
    raw_response: dict[str, Any] | None = None
    #: Provider sends this result took (transient refusals retried at the seam).
    attempts: int = 1


#: Extra sends a transient, unbilled STT refusal gets at the dispatch seam
#: (``UnifiedAIClient._dispatch_with_billing_net``) — every caller, one policy. CAPS.
STT_TRANSIENT_RETRIES = 2


@runtime_checkable
class STTClient(Protocol):
    async def execute(self, request: STTRequest, profile: ResolvedCallProfile) -> STTResult: ...


#: The containers the STT providers actually accept, verbatim from the 400 a
#: Groq transcription returns for anything else:
#: ``file must be one of the following types: [flac mp3 mp4 mpeg mpga m4a ogg
#: opus wav webm]`` (reproduced 2026-09-17). OpenAI's Whisper endpoint accepts
#: the same set. The provider decides by the multipart FILENAME's extension,
#: not by sniffing the bytes — an M4B audiobook is byte-identical MP4/AAC and
#: is still refused purely for being called ``.m4b``.
#: The provider's real request-body ceiling, in megabytes, when the catalog
#: offering declares none. Measured against the live Groq endpoint on
#: 2026-09-18: a 24.20 MB FLAC transcribed, a 27.0 MB FLAC came back
#: ``413 Request Entity Too Large``. The catalog said 100 MB (Groq's dev-tier
#: number), the lane chunked to 80% of that, and a two-hour audiobook died on
#: its first chunk. A ceiling nobody measured is a guess, and the safe guess
#: is the documented floor.
DEFAULT_PROVIDER_AUDIO_LIMIT_MB: float = 25.0

PROVIDER_ACCEPTED_AUDIO_SUFFIXES: frozenset[str] = frozenset({
    ".flac", ".mp3", ".mp4", ".mpeg", ".mpga", ".m4a", ".ogg", ".opus",
    ".wav", ".webm",
})


_AUDIO_SUFFIX_BY_MIME: dict[str, str] = {
    "audio/flac": ".flac",
    "audio/x-flac": ".flac",
    "audio/mpeg": ".mp3",
    "audio/mp3": ".mp3",
    "audio/mp4": ".m4a",
    "audio/m4a": ".m4a",
    "audio/x-m4a": ".m4a",
    "audio/ogg": ".ogg",
    "audio/opus": ".opus",
    "audio/wav": ".wav",
    "audio/x-wav": ".wav",
    "audio/wave": ".wav",
    "audio/webm": ".webm",
    "video/mp4": ".mp4",
    "video/webm": ".webm",
}


def _suffix_for_unknown_mime(mime: str) -> str:
    """No declared type keeps the historical ``.wav``; an unknown one keeps its own name."""
    if not mime:
        return ".wav"
    subtype = mime.split("/", 1)[-1].split("+", 1)[0]
    return f".{subtype}" if subtype else ".wav"


def provider_accepts_audio_container(filename: str) -> bool:
    """Would an STT provider accept a file under this NAME?

    🚨 The whole audiobook class, 2026-09-17: a two-hour ``.m4b`` under the
    byte ceiling was handed to the provider untouched because the only
    question anyone asked was "is it small enough?". The provider answered
    ``400 unsupported_audio_format`` and the person read "We couldn't
    transcribe that recording (APIStatusError)". Callers holding an arbitrary
    file ask THIS question first and transcode when the answer is no.
    """
    return Path(filename).suffix.lower() in PROVIDER_ACCEPTED_AUDIO_SUFFIXES


async def provider_audio_limit_mb(model: str) -> float:
    """The byte ceiling THIS model's provider actually enforces, in MB.

    🚨 One truth, not two. ``GroqSTT.execute`` reads the offering's
    ``stt.max_file_size_mb`` and refuses above it; before this, callers that
    had to CHUNK for the same ceiling carried their own copy of the number.
    The copy said 100 and the provider said 25, so every chunk the audiobook
    lane planned was three times too big (413, live, 2026-09-18).
    """
    from matrx_ai.catalog.resolve import resolve_call_profile

    profile = await resolve_call_profile(model)
    stt_meta = profile.offering_metadata.get("stt", {}) or {}
    try:
        limit = float(stt_meta.get("max_file_size_mb") or DEFAULT_PROVIDER_AUDIO_LIMIT_MB)
    except (TypeError, ValueError):
        limit = DEFAULT_PROVIDER_AUDIO_LIMIT_MB
    return limit if limit > 0 else DEFAULT_PROVIDER_AUDIO_LIMIT_MB


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
            header, _, encoded = audio_source.partition(",")
            audio_data = base64.b64decode(encoded)
            # The container is the data URI's declared type, never a guess: a
            # FLAC or an AMR voice memo named "audio.wav" is sent to the
            # provider under a lie, and an unaccepted container must be refused
            # here, by name, so the caller transcodes it.
            mime = header[5:].split(";", 1)[0].strip().lower()
            filename = f"audio{_AUDIO_SUFFIX_BY_MIME.get(mime, _suffix_for_unknown_mime(mime))}"
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
    if not provider_accepts_audio_container(filename):
        # Never spend a paid round-trip to be told this, and never let the
        # provider's own wording be the first honest sentence about it.
        raise ValueError(
            f"Audio container {Path(filename).suffix or '(none)'!r} is not one the "
            f"transcription provider accepts "
            f"({', '.join(sorted(PROVIDER_ACCEPTED_AUDIO_SUFFIXES))}). "
            "Transcode the audio before transcription."
        )
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

    profile = await resolve_call_profile(request.model, offering_id=request.offering_id)
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
    # The shared dispatch seam: admission on the Groq pool, the out-of-credit
    # alarm and LAYER 2 — the same pipe every chat and media call takes.
    sends = 0

    async def _send() -> STTResult:
        nonlocal sends
        sends += 1
        return await client.execute(request, profile)

    result = await UnifiedAIClient._dispatch_with_billing_net(
        _send,
        profile=profile,
        provider_client=client,
        transient_retries=STT_TRANSIENT_RETRIES,
    )
    result.attempts = sends
    # An adapter declares word support with ``supports_word_timestamps = True``;
    # one that doesn't is reported, never silently answered with no words.
    result.words_status = words_status_for(
        request, result, supported=bool(getattr(client, "supports_word_timestamps", False))
    )
    if result.words_status == "unsupported_by_provider":
        logging.getLogger(__name__).warning(
            "STT word timestamps requested but provider %r cannot supply them", profile.wire_format
        )
    return result


__all__ = [
    "DEFAULT_PROVIDER_AUDIO_LIMIT_MB",
    "PROVIDER_ACCEPTED_AUDIO_SUFFIXES",
    "STTClient",
    "STTRequest",
    "STTResult",
    "STTUsage",
    "execute_stt",
    "duration_to_stt_input_units",
    "prepare_audio_file",
    "provider_accepts_audio_container",
    "provider_audio_limit_mb",
]
