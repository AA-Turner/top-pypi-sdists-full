"""``ai.voice_to_voice`` — the same speech, delivery and timing, in another voice.

The thin node over ElevenLabs Voice Changer (api ``elevenlabs_voice_changer``, billed per
second of audio). The speech comes in the way Transcribe Audio takes it — a platform
``file_id`` (opened by the media boundary under the run's access, never fetched by URL here)
or an ``audio_source`` (URL or base64 / ``data:`` audio) — and goes out the way Text to Speech
returns it (``TextToSpeechOutput`` / ``generated_audio``: file_id first, expiring URLs dropped).
An empty ``voice`` takes the model's catalog default voice.
"""

from __future__ import annotations

import re
from typing import Any

from matrx_graph.actions import register_node
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success
from matrx_graph.types.usl import field_extras
from pydantic import BaseModel, ConfigDict, Field, JsonValue, model_validator

from matrx_ai.graph_nodes.class_pin import model_class_extras, offering_id_field
from matrx_ai.graph_nodes.mandates import (
    WORKFLOW_STEP_INTELLIGENCE_MANDATE,
    hold_step,
)
from matrx_ai.graph_nodes.shared import _extract_usage, failed_turn_failure
from matrx_ai.graph_nodes.tts_action import TextToSpeechOutput, _pick_audio_refs

_DATA_URI = re.compile(r"^data:([\w.+/-]+);base64,(.+)$", re.DOTALL)
_BASE64 = re.compile(r"^[A-Za-z0-9+/=\s]{64,}$")


class VoiceToVoiceInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    file_id: str | None = Field(
        default=None,
        description="A platform audio or video file with the speech. Give this or audio_source.",
        json_schema_extra=field_extras(widget="text"),
    )
    audio_source: str | None = Field(
        default=None,
        description="The speech as an HTTP(S) URL or base64 audio (with or without a data: prefix). Give this or file_id.",
        json_schema_extra=field_extras(widget="text"),
    )
    model: str = Field(
        default="eleven_multilingual_sts_v2",
        min_length=1,
        description="Voice changer model id, e.g. 'eleven_multilingual_sts_v2'.",
        json_schema_extra=field_extras(widget="model_picker", **model_class_extras()),
    )
    offering_id: str | None = offering_id_field()
    voice: str | None = Field(
        default=None,
        description="The voice to speak in (ElevenLabs voice id). Empty uses the model's default voice.",
    )
    metadata: dict[str, JsonValue] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _exactly_one_source(self) -> VoiceToVoiceInput:
        has_file = bool((self.file_id or "").strip())
        has_source = bool((self.audio_source or "").strip())
        if has_file and has_source:
            raise ValueError("Voice to Voice was given both a file and an audio source; give exactly one.")
        if not has_file and not has_source:
            raise ValueError("Voice to Voice needs speech to change: give a file or an audio source.")
        return self


def audio_part(inputs: VoiceToVoiceInput) -> dict[str, Any]:
    """The speech as one audio part: a file id stays an id, a data: URI or bare base64 rides inline, a URL is a URL."""
    if (inputs.file_id or "").strip():
        return {"type": "audio", "file_id": str(inputs.file_id).strip()}
    source = str(inputs.audio_source or "").strip()
    data_uri = _DATA_URI.match(source)
    if data_uri:
        return {"type": "audio", "mime_type": data_uri.group(1), "base64_data": data_uri.group(2)}
    if source.startswith(("http://", "https://")):
        return {"type": "audio", "url": source}
    if _BASE64.match(source):
        return {"type": "audio", "mime_type": "audio/mpeg", "base64_data": re.sub(r"\s", "", source)}
    raise ValueError("Voice to Voice: audio_source must be an http(s) URL or base64 audio.")


def voice_to_voice_config_payload(inputs: VoiceToVoiceInput) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": inputs.model,
        "offering_id": inputs.offering_id,
        "messages": [{"role": "user", "content": [audio_part(inputs)]}],
    }
    if inputs.voice:
        # UnifiedConfig reads ``tts_voice`` (a ``voice`` key is dropped), as Text to Speech sends it.
        payload["tts_voice"] = inputs.voice
    return payload


@register_node(
    name="ai.voice_to_voice",
    display_name="Voice to Voice",
    description="Say the same speech in another voice, keeping its delivery and timing.",
    category=NodeCategory.LLM,
    determinism=ActionTier.NON_DETERMINISTIC,
    input_schema=VoiceToVoiceInput,
    output_schema=TextToSpeechOutput,
    output_kind="generated_audio",
    icon="audio-waveform",
    tags=("ai", "audio", "speech", "voice"),
)
async def ai_voice_to_voice(
    ctx: NodeExecutionContext, inputs: VoiceToVoiceInput
) -> NodeResult[TextToSpeechOutput]:
    _ = ctx
    try:
        from matrx_files import is_durable_media_url

        from matrx_ai.config import UnifiedConfig
        from matrx_ai.orchestrator.executor import execute_ai_request

        held = await hold_step(
            voice_to_voice_config_payload(inputs),
            spec_type="ai.voice_to_voice",
            consumer="ai.voice_to_voice",
            metadata=inputs.metadata,
        )
        config = UnifiedConfig.from_dict(held.config)
        completed = await execute_ai_request(
            config,
            max_iterations=1,
            max_retries_per_iteration=2,
            metadata=held.metadata,
            mandate_key=WORKFLOW_STEP_INTELLIGENCE_MANDATE,
        )
        turn_failed = failed_turn_failure(completed, code="voice_to_voice_failed", model=inputs.model)
        if turn_failed is not None:
            return turn_failed
        response = getattr(completed, "final_response", None)
        refs = _pick_audio_refs(response)
        usage = _extract_usage(getattr(completed, "total_usage", None))
        if not (refs.file_id or refs.path or refs.url or refs.b64):
            return failure(
                "voice_to_voice_failed",
                f"ai.voice_to_voice: model '{inputs.model}' returned no audio.",
                details={"model": inputs.model, "usage": usage.model_dump(mode="json")},
            )
        durable = refs.url if is_durable_media_url(refs.url) else None
        return success(
            TextToSpeechOutput(
                file_id=refs.file_id,
                audio_path=refs.path,
                audio_url=durable,
                audio_cdn_url=durable,
                audio_b64=refs.b64,
                mime_type=refs.mime,
                duration_seconds=refs.duration_seconds or 0.0,
                model=inputs.model,
                usage=usage,
            )
        )
    except Exception as e:
        return failure("voice_to_voice_failed", f"{type(e).__name__}: {e}", details={"model": inputs.model})
