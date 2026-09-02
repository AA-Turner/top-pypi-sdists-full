"""``ai.generate_image`` — image synthesis via the UnifiedAIClient pipeline.

Routes through ``execute_ai_request`` so provider selection (Google
Imagen, Together FLUX, OpenAI DALL-E, etc.) falls out of the model id.
Same "audio by reference" approach as ``ai.text_to_speech`` — the
channel system is JSON-only and 10MB-per-image payloads would be a
terrible checkpoint citizen, so we surface file_id / path / URL / base64
in that priority. ``file_id`` leads because the node's output is
PERSISTED: a signed URL stored in a checkpoint is a link that dies,
while an id re-mints a fresh URL forever.

Typical inputs:

- ``prompt``       — free-text description
- ``negative_prompt`` — optional reject list
- ``aspect_ratio`` — "1:1" / "16:9" / "9:16" etc.
- ``count``        — 1..n images (provider-capped)

Declared IDEMPOTENT because most image models are seed-deterministic.
Callers who want each resume to generate fresh images set
``re_execute_on_resume=True`` on the node.
"""

from __future__ import annotations

from typing import Any

from matrx_graph.actions import register_node
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success
from matrx_graph.types.usl import field_extras
from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_ai.graph_nodes.shared import AiUsage, _extract_usage


class GenerateImageInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    model: str = Field(
        min_length=1,
        description=(
            "Image model id. Examples: 'imagen-3', 'FLUX.1-schnell', "
            "'dall-e-3', 'stable-diffusion-xl'."
        ),
        json_schema_extra=field_extras(widget="model_picker"),
    )
    prompt: str = Field(
        min_length=1,
        description="Image description.",
        json_schema_extra=field_extras(widget="textarea", multiline_rows=4),
    )
    negative_prompt: str | None = Field(
        default=None,
        description="Things to avoid (if the provider supports it).",
    )
    aspect_ratio: str = Field(
        default="1:1",
        description="W:H ratio. '1:1', '16:9', '9:16', '4:3', '3:4'.",
    )
    count: int = Field(
        default=1,
        ge=1,
        le=10,
        description="Number of variations to generate.",
    )
    seed: int | None = Field(
        default=None,
        description="Optional seed for deterministic variants.",
    )
    metadata: dict[str, JsonValue] = Field(
        default_factory=dict,
        description="Free-form metadata forwarded to the AI request for audit and routing.",
    )


class GeneratedImage(BaseModel):
    # No extra="allow": every constructor site (_image_from_image_content,
    # _image_from_block) passes exactly these declared fields — nothing
    # dynamic is ever spread in.
    #
    # THE IDENTITY RULE: ``file_id`` is what downstream nodes, checkpoints and
    # chat history carry. A node output is PERSISTED — it is replayed on
    # resume, read by later nodes, and rendered days later. ``url`` for a
    # personal image is a signed S3 URL that dies with its signature, so a node
    # that emitted only the URL left a permanently-dead link behind and no way
    # to re-mint one. Same envelope shape as the sibling ``image.edit.apply``
    # node (aidream/graph_actions/image/edit.py); the fields it can fill from a
    # cld_files record but an ``ImageContent`` block does not carry
    # (``download_url``, ``visibility``) are
    # deliberately absent rather than guessed — resolve them from ``file_id``.
    file_id: str | None = Field(
        default=None,
        description=(
            "cld_files id of the generated image — the durable handle. Pass this "
            "between nodes and re-mint any URL from it; never store a signed URL."
        ),
    )
    path: str | None = Field(
        default=None, description="Local filesystem path, when the provider wrote one."
    )
    url: str | None = Field(
        default=None,
        description=(
            "DURABLE inline-render URL — a CDN/public/external link that outlives "
            "this row. Null for a personal image, whose only URL expires: resolve "
            "one from file_id at the moment you need it."
        ),
    )
    cdn_url: str | None = Field(
        default=None, description="Permanent CDN URL, present only when the image is public."
    )
    data_b64: str | None = Field(
        default=None,
        description="Base64 image bytes, only when the provider returned no persisted file.",
    )
    mime_type: str | None = Field(
        default=None, description="Canonical MIME type of the encoded image."
    )
    size_bytes: int | None = Field(default=None, description="Encoded image size in bytes.")
    width: int | None = Field(default=None, description="Image width in pixels.")
    height: int | None = Field(default=None, description="Image height in pixels.")
    seed: int | None = Field(
        default=None, description="Seed the provider used, when it reports one."
    )


class GenerateImageOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    images: list[GeneratedImage] = Field(
        default_factory=list, description="Every image the provider returned, in order."
    )
    count: int = Field(default=0, description="How many images were generated.")
    model: str = Field(description="Image model id that produced the images.")
    # Canonical usage shape shared by every matrx-ai graph action (same type
    # the failure path already emits under details["usage"]).
    usage: AiUsage = Field(default_factory=AiUsage)


def _shape_image_blocks(response: Any) -> list[GeneratedImage]:
    """Walk ``response.messages`` for ``ImageContent`` blocks.

    Every provider's image-gen translator now yields a ``UnifiedResponse``
    whose ``messages[0].content`` is a list of ``ImageContent`` carrying
    the canonical file URL + mime + optional metadata (seed, revised
    prompt, safety attrs). The previous dict-walker was a fallback
    while provider-side translators didn't exist — kept here as the
    last-ditch path for any code path that still passes raw provider
    responses through.
    """
    from matrx_ai.config.media_config import ImageContent

    images: list[GeneratedImage] = []

    # Preferred shape: UnifiedResponse with ImageContent blocks.
    messages = getattr(response, "messages", None)
    if messages:
        for msg in messages:
            content = getattr(msg, "content", None) or []
            for block in content:
                if isinstance(block, ImageContent):
                    images.append(_image_from_image_content(block))
        if images:
            return images

    # Fallback: raw provider dict shapes (kept for backwards compat).
    return _shape_image_blocks_legacy(response)


def _image_from_image_content(block: Any) -> GeneratedImage:
    """Carry the block's IDENTITY, not just whatever URL it happened to hold.

    ``base_media._build_content_block`` fills the ``ImageContent`` with
    ``file_id`` + ``url`` (CDN when the image is public, an expiring signed URL
    when it is personal — the default). Reading only ``url`` is how a node
    output ended up holding a link that 403s a few hours later.

    So the expiring URL is DROPPED here rather than labelled: this payload is
    written to ``workflow.node_outcome`` and replayed days later, and a signed
    URL is a handoff, never a record. ``file_id`` is the handle that survives;
    every consumer mints its own URL from it. The URL is classified through the
    ONE signed-URL definition (``matrx_files``) — never a second X-Amz regex.
    """
    from matrx_files import is_durable_media_url

    # Caller guarantees an ImageContent (see _shape_image_blocks) — read its
    # fields directly; a defensive getattr here would silently degrade to None
    # the day one of them is renamed.
    metadata = block.metadata or {}
    url = block.url if is_durable_media_url(block.url) else None
    return GeneratedImage(
        file_id=block.file_id,
        path=metadata.get("path"),
        url=url,
        cdn_url=url,
        data_b64=block.base64_data,
        mime_type=block.mime_type,
        size_bytes=block.file_size,
        width=block.width or metadata.get("width"),
        height=block.height or metadata.get("height"),
        seed=metadata.get("seed"),
    )


def _shape_image_blocks_legacy(response: Any) -> list[GeneratedImage]:
    """Legacy dict-walker for any provider response not yet wired through
    the unified ImageContent path. Will be removed once every provider
    image-gen class returns ImageContent."""
    images: list[GeneratedImage] = []
    dump: dict[str, Any] = {}
    for attr in ("model_dump", "dict", "to_dict"):
        method = getattr(response, attr, None)
        if callable(method):
            try:
                candidate = method()
                if isinstance(candidate, dict):
                    dump = candidate
                    break
            except Exception:
                pass

    for key in ("images", "data", "generated"):
        raw = dump.get(key)
        if isinstance(raw, list):
            for item in raw:
                if isinstance(item, dict):
                    images.append(_image_from_block(item))

    content = dump.get("content") or dump.get("messages") or []
    if isinstance(content, list):
        for block in content:
            if not isinstance(block, dict):
                continue
            btype = block.get("type", "")
            if "image" in btype:
                images.append(_image_from_block(block))

    if not images:
        top = _image_from_block(dump)
        if top.file_id or top.path or top.url or top.data_b64:
            images.append(top)

    return images


def _image_from_block(block: dict[str, Any]) -> GeneratedImage:
    from matrx_files import is_durable_media_url

    raw_url = block.get("url") or block.get("image_url") or block.get("b64_json_url")
    # Same durability rule as the ImageContent path: only a URL that outlives
    # this row may be persisted. A provider dict that carries only an expiring
    # link contributes its file_id and nothing else.
    url = raw_url if is_durable_media_url(raw_url) else None
    cdn = block.get("cdn_url")
    return GeneratedImage(
        # Same identity rule as the ImageContent path: if the raw provider dict
        # carries a file_id, it is the only handle worth persisting.
        file_id=block.get("file_id"),
        path=block.get("path") or block.get("file_path") or block.get("local_path"),
        url=url,
        cdn_url=cdn if is_durable_media_url(cdn) else url,
        data_b64=block.get("data") or block.get("b64") or block.get("base64"),
        mime_type=block.get("mime_type") or block.get("content_type"),
        size_bytes=block.get("size_bytes"),
        width=block.get("width"),
        height=block.get("height"),
        seed=block.get("seed"),
    )


@register_node(
    name="ai.generate_image",
    display_name="Create Image",
    description="Create images from a written description.",
    category=NodeCategory.LLM,
    determinism=ActionTier.IDEMPOTENT,
    input_schema=GenerateImageInput,
    output_schema=GenerateImageOutput,
    # The registered platform Shape IS this node's output contract (seed:
    # matrx-frontend migrations/content_ir_seed_media_io_kinds.sql, schema
    # derived from GenerateImageOutput — keep the two in lockstep).
    output_kind="generated_image_set",
    icon="image",
    tags=("ai", "image", "generation", "vision"),
)
async def ai_generate_image(
    ctx: NodeExecutionContext, inputs: GenerateImageInput
) -> NodeResult[GenerateImageOutput]:
    _ = ctx

    try:
        from matrx_ai.config import UnifiedConfig
        from matrx_ai.orchestrator.executor import execute_ai_request

        config_payload: dict[str, Any] = {
            "model": inputs.model,
            "messages": [{"role": "user", "content": inputs.prompt}],
            "count": inputs.count,
            "aspect_ratio": inputs.aspect_ratio,
        }
        if inputs.negative_prompt:
            config_payload["negative_prompt"] = inputs.negative_prompt
        if inputs.seed is not None:
            config_payload["seed"] = inputs.seed

        config = UnifiedConfig.from_dict(config_payload)

        completed = await execute_ai_request(
            config,
            max_iterations=1,
            max_retries_per_iteration=2,
            metadata=inputs.metadata or None,
        )

        response = getattr(completed, "final_response", None)
        images = _shape_image_blocks(response)

        usage_raw = getattr(completed, "total_usage", None)
        # One canonical extractor (shared with the failure path below) — the
        # old hand-rolled loop read a non-existent ``totals`` attribute off
        # AggregatedUsage and silently reported empty usage.
        usage = _extract_usage(usage_raw)

        if not images:
            # Paid call with no artifact — fail with the billed usage in
            # details so the scheduler's cost settlement records the spend.
            return failure(
                "generation_failed",
                f"ai.generate_image: provider returned no images for model '{inputs.model}'.",
                details={
                    "model": inputs.model,
                    "usage": _extract_usage(usage_raw).model_dump(mode="json"),
                },
            )

        return success(
            GenerateImageOutput(
                images=images,
                count=len(images),
                model=inputs.model,
                usage=usage,
            )
        )
    except Exception as e:
        return failure(
            "generation_failed",
            f"{type(e).__name__}: {e}",
            details={"model": inputs.model},
        )
