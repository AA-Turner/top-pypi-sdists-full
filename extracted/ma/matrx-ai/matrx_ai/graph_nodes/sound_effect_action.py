"""``ai.generate_sound_effect`` — a short sound effect from a written description.

The thin node over ElevenLabs Sound Effects (api ``elevenlabs_sound_effects``, billed per
generated second). Same funnel and output as Create Music (``execute_ai_request``; the model
id picks the route; ``TextToSpeechOutput`` / ``generated_audio``: file_id first, expiring
URLs dropped). The length rides ``duration_seconds`` (1-30 whole seconds); empty lets the model pick.
"""

from __future__ import annotations

from typing import Any

from matrx_graph.actions import register_node
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success
from matrx_graph.types.usl import field_extras
from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_ai.graph_nodes.class_pin import model_class_extras, offering_id_field
from matrx_ai.graph_nodes.mandates import (
    WORKFLOW_STEP_INTELLIGENCE_MANDATE,
    hold_step,
)
from matrx_ai.graph_nodes.shared import _extract_usage, failed_turn_failure
from matrx_ai.graph_nodes.tts_action import TextToSpeechOutput, _pick_audio_refs


class GenerateSoundEffectInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    model: str = Field(
        default="eleven_text_to_sound_v2",
        min_length=1,
        description="Sound effect model id, e.g. 'eleven_text_to_sound_v2'.",
        json_schema_extra=field_extras(widget="model_picker", **model_class_extras()),
    )
    offering_id: str | None = offering_id_field()
    prompt: str = Field(
        min_length=1,
        description="The sound to make, e.g. 'a heavy wooden door creaking open'.",
        json_schema_extra=field_extras(widget="textarea", multiline_rows=3),
    )
    duration_seconds: int | None = Field(
        default=None,
        ge=1,
        le=30,
        description="Length in whole seconds (1-30). Empty lets the model choose.",
    )
    metadata: dict[str, JsonValue] = Field(default_factory=dict)


def sound_effect_config_payload(inputs: GenerateSoundEffectInput) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": inputs.model,
        "offering_id": inputs.offering_id,
        "messages": [{"role": "user", "content": inputs.prompt}],
    }
    if inputs.duration_seconds is not None:
        payload["duration_seconds"] = inputs.duration_seconds
    return payload


@register_node(
    name="ai.generate_sound_effect",
    display_name="Create Sound Effect",
    description="Make a short sound effect from a written description.",
    category=NodeCategory.LLM,
    determinism=ActionTier.NON_DETERMINISTIC,
    input_schema=GenerateSoundEffectInput,
    output_schema=TextToSpeechOutput,
    output_kind="generated_audio",
    icon="audio-lines",
    tags=("ai", "audio", "sound", "generation"),
)
async def ai_generate_sound_effect(
    ctx: NodeExecutionContext, inputs: GenerateSoundEffectInput
) -> NodeResult[TextToSpeechOutput]:
    _ = ctx
    try:
        from matrx_files import is_durable_media_url

        from matrx_ai.config import UnifiedConfig
        from matrx_ai.orchestrator.executor import execute_ai_request

        held = await hold_step(
            sound_effect_config_payload(inputs),
            spec_type="ai.sound_effect",
            consumer="ai.generate_sound_effect",
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
        turn_failed = failed_turn_failure(completed, code="sound_effect_failed", model=inputs.model)
        if turn_failed is not None:
            return turn_failed
        response = getattr(completed, "final_response", None)
        refs = _pick_audio_refs(response)
        usage = _extract_usage(getattr(completed, "total_usage", None))
        if not (refs.file_id or refs.path or refs.url or refs.b64):
            finish = str(getattr(response, "finish_reason", "") or "")
            declined = "content_filter" in finish.lower()
            return failure(
                "sound_effect_declined" if declined else "sound_effect_failed",
                (
                    f"ai.generate_sound_effect: model '{inputs.model}' declined this description; "
                    "reword it and run again."
                    if declined
                    else f"ai.generate_sound_effect: model '{inputs.model}' returned no audio."
                ),
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
                duration_seconds=refs.duration_seconds or float(inputs.duration_seconds or 0),
                model=inputs.model,
                usage=usage,
            )
        )
    except Exception as e:
        return failure("sound_effect_failed", f"{type(e).__name__}: {e}", details={"model": inputs.model})
