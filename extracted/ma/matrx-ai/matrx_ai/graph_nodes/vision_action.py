"""``ai.vision.read`` — look at an image and answer in text.

Ask AI (``ai.llm.chat``) takes words only. This step sends one or more
images plus an instruction to a vision model in a single raw call — no
agent, no tools. Three jobs, one funnel:

* ``describe``   — say what the image shows;
* ``read_text``  — OCR: write out every word visible in the image;
* ``ask``        — answer the step's own instruction about the image.

The instruction is the step's own visible field. When the author leaves it
empty, the mode's one-line default (``MODE_INSTRUCTIONS``, shown in the
field's description) is used — never a hidden prompt.

Same result shape as Ask AI (``AiExecutionResult`` / ``agent_result``), so a
downstream step reads ``final_text`` either way. ``output_schema`` asks for
structured output exactly like Ask AI does.
"""

from __future__ import annotations

import asyncio
from typing import Any, Literal

from matrx_graph.actions import register_node
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult
from matrx_graph.types.usl import field_extras
from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_ai.graph_nodes.class_pin import model_class_extras, offering_id_field
from matrx_ai.graph_nodes.image_edit_action import image_part
from matrx_ai.graph_nodes.mandates import (
    WORKFLOW_STEP_INTELLIGENCE_MANDATE,
    hold_step,
)
from matrx_ai.graph_nodes.shared import AiExecutionResult, normalize_completed_result

VisionMode = Literal["describe", "read_text", "ask"]

#: The default instruction per mode, used only when the step's own instruction is empty.
MODE_INSTRUCTIONS: dict[str, str] = {
    "describe": "Describe this image clearly and completely.",
    "read_text": (
        "Write out all of the text visible in this image, exactly as written, "
        "keeping its reading order and line breaks. Write nothing else."
    ),
}


class VisionReadInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    model: str = Field(
        min_length=1,
        description="A model that can see images, e.g. 'gemini-3-flash' or 'gpt-5-mini'.",
        json_schema_extra=field_extras(widget="model_picker", **model_class_extras()),
    )
    offering_id: str | None = offering_id_field()
    images: list[str] = Field(
        min_length=1,
        max_length=20,
        description="The images to look at, as platform file ids or URLs.",
    )
    mode: VisionMode = Field(
        default="describe",
        description="describe = say what it shows; read_text = write out its text (OCR); ask = answer the instruction.",
    )
    instruction: str | None = Field(
        default=None,
        description=(
            "What to do with the image. Empty uses the mode's default: describe -> "
            f"'{MODE_INSTRUCTIONS['describe']}' read_text -> '{MODE_INSTRUCTIONS['read_text']}'"
        ),
        json_schema_extra=field_extras(widget="textarea", multiline_rows=3),
    )
    system_instruction: str | None = Field(default=None)
    temperature: float | None = Field(default=None, ge=0.0, le=2.0)
    max_tokens: int | None = Field(default=None, ge=1)
    output_schema: dict[str, JsonValue] | None = Field(
        default=None,
        description="Optional JSON schema; when set the reply is structured output.",
    )
    metadata: dict[str, JsonValue] = Field(default_factory=dict)


def vision_instruction(inputs: VisionReadInput) -> str:
    """The instruction sent with the images: the step's own, else the mode's default."""
    own = (inputs.instruction or "").strip()
    if own:
        return own
    if inputs.mode == "ask":
        raise ValueError("Read an Image in 'ask' mode needs an instruction: say what to ask.")
    return MODE_INSTRUCTIONS[inputs.mode]


def vision_config_payload(inputs: VisionReadInput) -> dict[str, Any]:
    content: list[dict[str, Any]] = [image_part(ref) for ref in inputs.images]
    content.append({"type": "text", "text": vision_instruction(inputs)})
    payload: dict[str, Any] = {
        "model": inputs.model,
        "offering_id": inputs.offering_id,
        "messages": [{"role": "user", "content": content}],
        "system_instruction": inputs.system_instruction,
    }
    if inputs.mode == "read_text" and inputs.temperature is None:
        # Transcription, not invention; the translator drops it for models that refuse it.
        payload["temperature"] = 0.0
    elif inputs.temperature is not None:
        payload["temperature"] = inputs.temperature
    if inputs.max_tokens is not None:
        payload["max_tokens"] = inputs.max_tokens
    if inputs.output_schema is not None:
        from matrx_ai.graph_nodes.llm_action import _build_response_format

        payload["response_format"] = _build_response_format(inputs.output_schema)
    return payload


@register_node(
    name="ai.vision.read",
    display_name="Read an Image",
    description="Describe an image, read the text in it, or answer a question about it.",
    category=NodeCategory.LLM,
    determinism=ActionTier.NON_DETERMINISTIC,
    input_schema=VisionReadInput,
    output_schema=AiExecutionResult,
    output_kind="agent_result",
    icon="scan-eye",
    tags=("ai", "vision", "image", "ocr"),
)
async def ai_vision_read(
    ctx: NodeExecutionContext, inputs: VisionReadInput
) -> NodeResult[AiExecutionResult]:
    from matrx_ai.config import UnifiedConfig
    from matrx_ai.orchestrator.executor import execute_ai_request

    _ = ctx
    held = await hold_step(
        vision_config_payload(inputs),
        spec_type="ai.vision",
        consumer=f"ai.vision.{inputs.mode}",
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
    return await asyncio.to_thread(normalize_completed_result, completed)
