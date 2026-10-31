"""``ai.image.edit`` — change existing images with an AI image model.

``ai.generate_image`` makes a picture from words alone; ``image.edit.apply``
(aidream) runs fixed, non-AI operations (crop, blur, background removal).
This step is the missing third: an instruction plus one or more existing
images, sent to an image model that edits (gpt-image, Gemini image, FLUX
Kontext, Seedream, Qwen-Image …). An optional mask limits the change to a
region on models that inpaint.

Same funnel as ``ai.generate_image`` (``execute_ai_request`` → the model's
image route). The images ride the user turn as image parts, so each
provider's existing edit path picks them up: OpenAI promotes the call to
``images.edit``, Gemini/Replicate/Together read the image inputs. A mask
rides as an image part with the ``mask`` role (the one vocabulary in
``matrx_ai.media.image_reference_roles``); the role gate refuses it before
the paid call on a model that cannot take one.

Output is the SAME ``GenerateImageOutput`` / ``generated_image_set`` shape as
Create Image — file_id first, expiring URLs dropped.
"""

from __future__ import annotations

import re
from typing import Any

from matrx_graph.actions import register_node
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success
from matrx_graph.types.usl import field_extras
from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_ai.graph_nodes.class_pin import model_class_extras, offering_id_field
from matrx_ai.graph_nodes.image_action import GenerateImageOutput, _shape_image_blocks
from matrx_ai.graph_nodes.mandates import (
    WORKFLOW_STEP_INTELLIGENCE_MANDATE,
    hold_step,
)
from matrx_ai.graph_nodes.shared import _extract_usage, failed_turn_failure

_UUID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE)
_DATA_URI = re.compile(r"^data:([\w.+/-]+);base64,(.+)$", re.DOTALL)


def image_part(ref: str, *, role: str | None = None) -> dict[str, Any]:
    """One image part for a user turn from a platform file id or a URL.

    A file id stays an id (the media pipeline opens it under the run's access
    and never by URL); a ``data:`` URI becomes inline base64; anything else is a URL.
    """
    value = str(ref or "").strip()
    if not value:
        raise ValueError("An image reference is empty; give a file id or a URL.")
    part: dict[str, Any] = {"type": "image"}
    data_uri = _DATA_URI.match(value)
    if _UUID.match(value):
        part["file_id"] = value
    elif data_uri:
        # Inline bytes ride as base64 + mime: a provider translator reads base64_data,
        # and a data: URI left in ``url`` reached the model as no image at all (live, 2026-10-29).
        part["mime_type"] = data_uri.group(1)
        part["base64_data"] = data_uri.group(2)
    else:
        part["url"] = value
    if role:
        part["role"] = role
    return part


class EditImageInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    model: str = Field(
        min_length=1,
        description=(
            "Image model that edits. Examples: 'gpt-image-2.5-flare', "
            "'gemini-3.1-flash-image', 'black-forest-labs/FLUX.2-pro'."
        ),
        json_schema_extra=field_extras(widget="model_picker", **model_class_extras()),
    )
    offering_id: str | None = offering_id_field()
    prompt: str = Field(
        min_length=1,
        description="What to change.",
        json_schema_extra=field_extras(widget="textarea", multiline_rows=4),
    )
    images: list[str] = Field(
        min_length=1,
        max_length=16,
        description=(
            "The images to edit, as platform file ids or URLs. The first is the "
            "one being edited; the rest are references the model may use."
        ),
    )
    mask: str | None = Field(
        default=None,
        description=(
            "Optional mask image (file id or URL). Only the transparent area of "
            "the first image changes. Needs a model that inpaints."
        ),
    )
    aspect_ratio: str | None = Field(
        default=None,
        description="W:H ratio for the result. Empty keeps the model's default.",
    )
    count: int = Field(default=1, ge=1, le=10, description="How many versions to make.")
    seed: int | None = Field(default=None, description="Optional seed.")
    metadata: dict[str, JsonValue] = Field(default_factory=dict)


def edit_config_payload(inputs: EditImageInput) -> dict[str, Any]:
    """The step's UnifiedConfig dict: the instruction plus every image in one user turn."""
    content: list[dict[str, Any]] = [image_part(ref) for ref in inputs.images]
    if inputs.mask:
        content.append(image_part(inputs.mask, role="mask"))
    content.append({"type": "text", "text": inputs.prompt})
    payload: dict[str, Any] = {
        "model": inputs.model,
        "offering_id": inputs.offering_id,
        "messages": [{"role": "user", "content": content}],
        "count": inputs.count,
    }
    if inputs.aspect_ratio:
        payload["aspect_ratio"] = inputs.aspect_ratio
    if inputs.seed is not None:
        payload["seed"] = inputs.seed
    return payload


@register_node(
    name="ai.image.edit",
    display_name="Edit Image with AI",
    description="Change existing images with a written instruction.",
    category=NodeCategory.LLM,
    determinism=ActionTier.NON_DETERMINISTIC,
    input_schema=EditImageInput,
    output_schema=GenerateImageOutput,
    # Same output shape as Create Image (ai.generate_image), so the same kind.
    output_kind="generated_image_set",
    icon="wand-sparkles",
    tags=("ai", "image", "edit", "vision"),
)
async def ai_image_edit(
    ctx: NodeExecutionContext, inputs: EditImageInput
) -> NodeResult[GenerateImageOutput]:
    _ = ctx
    try:
        from matrx_ai.config import UnifiedConfig
        from matrx_ai.orchestrator.executor import execute_ai_request

        held = await hold_step(
            edit_config_payload(inputs),
            spec_type="ai.image",
            consumer="ai.image.edit",
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
        turn_failed = failed_turn_failure(completed, code="edit_failed", model=inputs.model)
        if turn_failed is not None:
            return turn_failed
        images = _shape_image_blocks(getattr(completed, "final_response", None))
        usage = _extract_usage(getattr(completed, "total_usage", None))
        if not images:
            return failure(
                "edit_failed",
                f"ai.image.edit: model '{inputs.model}' returned no images.",
                details={"model": inputs.model, "usage": usage.model_dump(mode="json")},
            )
        return success(
            GenerateImageOutput(images=images, count=len(images), model=inputs.model, usage=usage)
        )
    except Exception as e:
        return failure(
            "edit_failed", f"{type(e).__name__}: {e}", details={"model": inputs.model}
        )
