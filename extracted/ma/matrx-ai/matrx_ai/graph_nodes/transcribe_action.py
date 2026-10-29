"""``ai.transcribe`` — catalog-dispatched speech transcription.

Why this exists separately from ``ai.llm.chat``: transcription is a
non-chat task. The UnifiedAIClient path assumes a messages list and
returns a chat-shaped response. Here the input is a platform file
(``file_id``) or an audio source (path, URL, bytes-as-base64), and the output
is plain text, timed segments and language — no messages, no finish reason,
no tool calls.

A ``file_id`` is opened by the HOST through the ``managed_file_transcriber``
seam (aidream: the files service's access check, streamed download, chunking
for long audio). This package never fetches a platform file by URL.

Declared IDEMPOTENT because the same audio always transcribes to the same
text (deterministic temperature=0 path), so resume-after-crash can reuse
a prior outcome without double-charging Groq.
"""

from __future__ import annotations

from typing import Any, Literal

from matrx_graph.actions import register_node
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from matrx_graph.types.usl import field_extras
from pydantic import BaseModel, ConfigDict, Field, JsonValue, model_validator

from matrx_ai._ext import get_ext, has_ext
from matrx_ai.graph_nodes.class_pin import (
    class_pin_kwargs,
    model_class_extras,
    offering_id_field,
)
from matrx_ai.graph_nodes.shared import AiUsage


class TranscribeInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    file_id: str | None = Field(
        default=None,
        description=(
            "A platform file to transcribe (audio or video). Opened by the host under "
            "the run's access; long audio is split and stitched. Give this or audio_source."
        ),
        json_schema_extra=field_extras(widget="text"),
    )
    audio_source: str | None = Field(
        default=None,
        description=(
            "Audio location — absolute path, HTTP(S) URL, or base64-encoded "
            "audio (with or without data: prefix). Supported formats: "
            "flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, webm. Give this or file_id."
        ),
        json_schema_extra=field_extras(widget="text"),
    )
    model: str = Field(
        default="stt-default",
        description="Catalog model or alias whose offering uses an STT translator.",
        json_schema_extra=field_extras(widget="model_picker", **model_class_extras()),
    )
    offering_id: str | None = offering_id_field()
    language: str | None = Field(
        default=None,
        description="ISO-639-1 language code ('en', 'es', 'fr', …). Auto-detect when None.",
        json_schema_extra=field_extras(widget="text", placeholder="en"),
    )
    temperature: float = Field(default=0.0, ge=0.0, le=1.0)
    response_format: Literal["json", "verbose_json", "text"] = "verbose_json"

    @model_validator(mode="after")
    def _exactly_one_source(self) -> TranscribeInput:
        has_file = bool((self.file_id or "").strip())
        has_source = bool((self.audio_source or "").strip())
        if has_file and has_source:
            raise ValueError(
                "Transcribe Audio was given both a file and an audio source; give exactly one."
            )
        if not has_file and not has_source:
            raise ValueError(
                "Transcribe Audio needs something to transcribe: give a file or an audio source."
            )
        return self


class TranscriptSegment(BaseModel):
    """One timed stretch of speech, on the audio's own clock (seconds from its start)."""

    model_config = ConfigDict(extra="forbid")

    index: int
    start_s: float = 0.0
    end_s: float = 0.0
    text: str


#: The host seam that transcribes a platform file by id (aidream: the files service).
MANAGED_FILE_TRANSCRIBER_EXT = "managed_file_transcriber"


class TranscriptionUsage(AiUsage):
    """Canonical AiUsage extended with the duration figure Groq bills by.

    Whisper is billed per audio second, not per token — ``duration_seconds``
    is the one extra field the transcription provider reports (AiUsage is a
    closed model, so the key must be declared to survive validation)."""

    duration_seconds: float | None = Field(
        default=None,
        description="Audio duration billed by the transcription provider, in seconds.",
    )


class TranscribeOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str
    language: str | None = None
    duration_seconds: float = 0.0
    model: str
    #: Timed segments, in order. Empty when the provider returned none (the "text" format).
    segments: list[TranscriptSegment] = Field(default_factory=list)
    # Canonical usage shape shared by every matrx-ai graph action, plus the
    # duration-based billing figure.
    usage: TranscriptionUsage = Field(default_factory=TranscriptionUsage)


@register_node(
    name="ai.transcribe",
    display_name="Transcribe Audio",
    description="Turn speech in an audio file into written text.",
    category=NodeCategory.LLM,
    determinism=ActionTier.IDEMPOTENT,
    input_schema=TranscribeInput,
    output_schema=TranscribeOutput,
    output_kind="transcription_result",
    icon="mic",
    tags=("ai", "audio", "speech"),
)
async def ai_transcribe(
    ctx: NodeExecutionContext, inputs: TranscribeInput
) -> NodeResult[TranscribeOutput]:
    if inputs.file_id and inputs.file_id.strip():
        return await _transcribe_file(ctx, inputs)

    from matrx_ai.processing.audio.stt import STTRequest, execute_stt

    result = await execute_stt(
        STTRequest(
            audio_source=inputs.audio_source,
            model=inputs.model,
            **class_pin_kwargs(inputs.model, inputs.offering_id, where="ai.transcribe"),
            language=inputs.language,
            response_format=inputs.response_format,
            temperature=inputs.temperature,
        )
    )

    # TranscriptionResult is a dataclass-ish object; pull fields with getattr.
    text = getattr(result, "text", "") or ""
    language = getattr(result, "language", None)
    duration = float(getattr(result, "duration", 0.0) or 0.0)
    usage_raw = getattr(result, "usage", None)
    usage_fields: dict[str, JsonValue] = {}
    if usage_raw is not None:
        # Groq's usage object is duration-billed: of the probed attrs only
        # ``duration_seconds`` exists today; token attrs stay for any future
        # usage shape.
        for attr in (
            "input_tokens",
            "output_tokens",
            "total_tokens",
            "duration_seconds",
            "cost_usd",
        ):
            val = getattr(usage_raw, attr, None)
            if val is not None:
                usage_fields[attr] = val
    usage = TranscriptionUsage.model_validate(usage_fields)
    if usage_raw is not None:
        from matrx_ai.config.usage_config import ensure_pricing_lookup

        await ensure_pricing_lookup()
        usage.cost_usd = usage_raw.to_token_usage().calculate_cost()

    # Hard failures raise inside the selected STT client — the scheduler synthesizes
    # those into the same Failure shape (code = exception class name).
    return success(
        TranscribeOutput(
            text=text,
            language=language,
            duration_seconds=duration,
            model=result.usage.matrx_model_name,
            segments=_segments(getattr(result, "segments", None)),
            usage=usage,
        )
    )


def _segments(raw: list[Any] | None) -> list[TranscriptSegment]:
    """Provider segments (dicts or objects with start / end / text) as the step's shape."""
    out: list[TranscriptSegment] = []
    for item in raw or []:
        get = item.get if isinstance(item, dict) else (lambda k, _i=item: getattr(_i, k, None))
        start = float(get("start") or 0.0)
        out.append(
            TranscriptSegment(
                index=len(out),
                start_s=start,
                end_s=float(get("end") or start),
                text=str(get("text") or ""),
            )
        )
    return out


async def _transcribe_file(
    ctx: NodeExecutionContext, inputs: TranscribeInput
) -> NodeResult[TranscribeOutput]:
    """A platform file, opened and transcribed by the host. Billing happens at the same
    provider dispatch seam as the audio-source path; the step reports the billed duration."""
    if not has_ext(MANAGED_FILE_TRANSCRIBER_EXT):
        raise RuntimeError(
            "Transcribe Audio cannot open a platform file on this host: no "
            f"{MANAGED_FILE_TRANSCRIBER_EXT!r} is installed. Give an audio source instead."
        )
    if class_pin_kwargs(inputs.model, inputs.offering_id, where="ai.transcribe"):
        raise ValueError(
            "Transcribe Audio cannot pin a provider offering when transcribing a platform file; "
            "choose the model only, or give an audio source."
        )
    response = await get_ext(MANAGED_FILE_TRANSCRIBER_EXT)(
        str(inputs.file_id).strip(),
        model=inputs.model,
        language=inputs.language,
        organization_id=getattr(ctx, "organization_id", None),
    )
    duration = float(getattr(response, "duration", 0.0) or 0.0)
    meta = getattr(response, "meta", None)
    return success(
        TranscribeOutput(
            text=str(getattr(response, "text", "") or ""),
            language=getattr(response, "language", None),
            duration_seconds=duration,
            model=str(getattr(meta, "model", "") or inputs.model),
            segments=_segments(getattr(response, "segments", None)),
            usage=TranscriptionUsage(duration_seconds=duration or None),
        )
    )
