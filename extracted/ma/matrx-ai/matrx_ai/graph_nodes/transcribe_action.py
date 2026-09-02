"""``ai.transcribe`` — catalog-dispatched speech transcription.

Why this exists separately from ``ai.llm.chat``: transcription is a
non-chat task. The UnifiedAIClient path assumes a messages list and
returns a chat-shaped response. Here the input is an audio source (path,
URL, bytes-as-base64) and the output is plain text + timing + language —
no messages, no finish reason, no tool calls.

Declared IDEMPOTENT because the same audio always transcribes to the same
text (deterministic temperature=0 path), so resume-after-crash can reuse
a prior outcome without double-charging Groq.
"""

from __future__ import annotations

from typing import Literal

from matrx_graph.actions import register_node
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from matrx_graph.types.usl import field_extras
from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_ai.graph_nodes.shared import AiUsage


class TranscribeInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    audio_source: str = Field(
        min_length=1,
        description=(
            "Audio location — absolute path, HTTP(S) URL, or base64-encoded "
            "audio (with or without data: prefix). Supported formats: "
            "flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, webm."
        ),
        json_schema_extra=field_extras(widget="text"),
    )
    model: str = Field(
        default="stt-default",
        description="Catalog model or alias whose offering uses an STT translator.",
        json_schema_extra=field_extras(widget="select"),
    )
    language: str | None = Field(
        default=None,
        description="ISO-639-1 language code ('en', 'es', 'fr', …). Auto-detect when None.",
        json_schema_extra=field_extras(widget="text", placeholder="en"),
    )
    temperature: float = Field(default=0.0, ge=0.0, le=1.0)
    response_format: Literal["json", "verbose_json", "text"] = "verbose_json"


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
    _ = ctx

    from matrx_ai.processing.audio.stt import STTRequest, execute_stt

    result = await execute_stt(
        STTRequest(
            audio_source=inputs.audio_source,
            model=inputs.model,
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
            usage=usage,
        )
    )
