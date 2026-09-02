"""``ai.generate_video`` / ``ai.edit_video`` / ``ai.extend_video`` — video
synthesis via the UnifiedAIClient pipeline.

Mirrors ``image_action.py``. Routes to the right provider via the model
id; the provider class polls the long-running operation and returns
``UnifiedResponse`` with ``VideoContent`` carrying the canonical file URL.

Declared NON-IDEMPOTENT because video generation is non-deterministic
(seed-deterministic on some models, but most have stochastic frames).
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


class GenerateVideoInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    model: str = Field(
        min_length=1,
        description=(
            "Video model id. Examples: 'veo-3.1-generate-preview', "
            "'sora-2', 'sora-2-pro', 'grok-imagine-video', "
            "'google/veo-3.0-fast-audio' (Together), 'google/veo-3.1' (Replicate)."
        ),
        json_schema_extra=field_extras(widget="model_picker"),
    )
    prompt: str = Field(
        min_length=1,
        description="Video description.",
        json_schema_extra=field_extras(widget="textarea", multiline_rows=4),
    )
    aspect_ratio: str = Field(
        default="16:9",
        description="W:H ratio. '16:9', '9:16', '1:1', '4:3', '3:4'.",
    )
    resolution: str = Field(
        default="720p",
        description="Output resolution. '480p', '720p', '1080p', '4K'.",
    )
    duration_seconds: int = Field(
        default=8,
        ge=1,
        le=120,
        description="Video duration in seconds.",
    )
    image_input_url: str | None = Field(
        default=None,
        description="Optional starting image URL for image-to-video.",
    )
    last_frame_image_url: str | None = Field(
        default=None,
        description=("Optional ending image URL for first→last interpolation (Veo 3.1, Kling)."),
    )
    negative_prompt: str | None = Field(default=None)
    audio_enabled: bool | None = Field(
        default=None,
        description="Enable native audio (Veo 3+). Defaults provider-side.",
    )
    seed: int | None = Field(default=None)
    metadata: dict[str, JsonValue] = Field(default_factory=dict)


class GeneratedVideo(BaseModel):
    # No extra="allow": the only constructor site (_shape_video_blocks)
    # passes exactly these declared fields — nothing dynamic is spread in.
    #
    # THE IDENTITY RULE (same as GeneratedImage in image_action.py): ``file_id``
    # is the durable handle a node output carries. A node output is PERSISTED —
    # replayed on resume, read by later nodes, rendered days later — so a
    # personal video's signed ``url`` is dead by the time anyone reads it and
    # there is nothing to re-mint from. The provider's ``VideoContent`` block
    # already knows the id at persist time; emitting only the URL threw it away.
    file_id: str | None = Field(
        default=None,
        description=(
            "cld_files id of the generated video — the durable handle. Pass this "
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
            "this row. Null for a personal video, whose only URL expires: resolve "
            "one from file_id at the moment you need it."
        ),
    )
    cdn_url: str | None = Field(
        default=None, description="Permanent CDN URL, present only when the video is public."
    )
    mime_type: str | None = Field(
        default=None, description="Canonical MIME type of the encoded video."
    )
    duration_seconds: float | None = Field(
        default=None, description="Video duration in seconds, when the provider reports one."
    )


class GenerateVideoOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    videos: list[GeneratedVideo] = Field(
        default_factory=list, description="Every video the provider returned, in order."
    )
    count: int = Field(default=0, description="How many videos were generated.")
    model: str = Field(description="Video model id that produced the videos.")
    # Canonical usage shape shared by every matrx-ai graph action (same type
    # the failure path already emits under details["usage"]).
    usage: AiUsage = Field(default_factory=AiUsage)


def _shape_video_blocks(response: Any) -> list[GeneratedVideo]:
    """Walk ``response.messages`` for ``VideoContent`` blocks.

    Carries the block's IDENTITY, not just whatever URL it happened to hold —
    ``base_media._build_content_block`` fills ``VideoContent.file_id`` alongside
    the URL (CDN when public, an expiring signed URL when personal). The expiring
    one is DROPPED, not labelled: this payload lands in ``workflow.node_outcome``
    and is replayed days later, and a signed URL is a handoff, never a record.
    Durability is decided by the ONE classifier (``matrx_files``).
    """
    from matrx_files import is_durable_media_url

    from matrx_ai.config.media_config import VideoContent

    videos: list[GeneratedVideo] = []
    messages = getattr(response, "messages", None) or []
    for msg in messages:
        content = getattr(msg, "content", None) or []
        for block in content:
            if isinstance(block, VideoContent):
                metadata = getattr(block, "metadata", None) or {}
                url = block.url if is_durable_media_url(block.url) else None
                duration = metadata.get("duration_seconds")
                if duration is None and block.duration_ms is not None:
                    duration = block.duration_ms / 1000.0
                videos.append(
                    GeneratedVideo(
                        file_id=block.file_id,
                        path=metadata.get("path"),
                        url=url,
                        cdn_url=url,
                        mime_type=block.mime_type,
                        duration_seconds=duration,
                    )
                )
    return videos


@register_node(
    name="ai.generate_video",
    display_name="Create Video",
    description="Create a video from a written description.",
    category=NodeCategory.LLM,
    determinism=ActionTier.NON_DETERMINISTIC,
    input_schema=GenerateVideoInput,
    output_schema=GenerateVideoOutput,
    # Shared by generate/edit/extend — one output shape, one kind (seed:
    # matrx-frontend migrations/content_ir_seed_media_io_kinds.sql).
    output_kind="generated_video_set",
    icon="video",
    tags=("ai", "video", "generation"),
)
async def ai_generate_video(
    ctx: NodeExecutionContext, inputs: GenerateVideoInput
) -> NodeResult[GenerateVideoOutput]:
    _ = ctx
    return await _run_video_action(inputs, video_action="generate")


class EditVideoInput(GenerateVideoInput):
    video_input_url: str = Field(
        min_length=1,
        description="URL of the video to edit (xAI grok-imagine-video, OpenAI Sora 2 edits).",
    )


@register_node(
    name="ai.edit_video",
    display_name="Edit Video",
    description="Change an existing video using a written instruction.",
    category=NodeCategory.LLM,
    determinism=ActionTier.NON_DETERMINISTIC,
    input_schema=EditVideoInput,
    output_schema=GenerateVideoOutput,
    # Shared by generate/edit/extend — one output shape, one kind (seed:
    # matrx-frontend migrations/content_ir_seed_media_io_kinds.sql).
    output_kind="generated_video_set",
    icon="video",
    tags=("ai", "video", "edit"),
)
async def ai_edit_video(
    ctx: NodeExecutionContext, inputs: EditVideoInput
) -> NodeResult[GenerateVideoOutput]:
    _ = ctx
    return await _run_video_action(inputs, video_action="edit")


class ExtendVideoInput(GenerateVideoInput):
    video_input_url: str = Field(
        min_length=1,
        description="URL of the video to extend.",
    )


@register_node(
    name="ai.extend_video",
    display_name="Extend Video",
    description="Make an existing video longer by a few seconds.",
    category=NodeCategory.LLM,
    determinism=ActionTier.NON_DETERMINISTIC,
    input_schema=ExtendVideoInput,
    output_schema=GenerateVideoOutput,
    # Shared by generate/edit/extend — one output shape, one kind (seed:
    # matrx-frontend migrations/content_ir_seed_media_io_kinds.sql).
    output_kind="generated_video_set",
    icon="video",
    tags=("ai", "video", "extend"),
)
async def ai_extend_video(
    ctx: NodeExecutionContext, inputs: ExtendVideoInput
) -> NodeResult[GenerateVideoOutput]:
    _ = ctx
    return await _run_video_action(inputs, video_action="extend")


# ----------------------------------------------------------------------
# Shared executor
# ----------------------------------------------------------------------


async def _run_video_action(
    inputs: GenerateVideoInput, *, video_action: str
) -> NodeResult[GenerateVideoOutput]:
    try:
        from matrx_ai.config import UnifiedConfig
        from matrx_ai.orchestrator.executor import execute_ai_request

        config_payload: dict[str, Any] = {
            "model": inputs.model,
            "messages": [{"role": "user", "content": inputs.prompt}],
            "aspect_ratio": inputs.aspect_ratio,
            "resolution": inputs.resolution,
            "duration_seconds": inputs.duration_seconds,
            "video_action": video_action,
        }
        if inputs.image_input_url:
            config_payload["image_input"] = {"url": inputs.image_input_url}
        if inputs.last_frame_image_url:
            config_payload["last_frame_image"] = {"url": inputs.last_frame_image_url}
        if inputs.negative_prompt:
            config_payload["negative_prompt"] = inputs.negative_prompt
        if inputs.audio_enabled is not None:
            config_payload["audio_enabled"] = inputs.audio_enabled
        if inputs.seed is not None:
            config_payload["seed"] = inputs.seed
        # video_input only relevant for edit/extend.
        video_input_url = getattr(inputs, "video_input_url", None)
        if video_input_url:
            config_payload["video_input"] = {"url": video_input_url}

        config = UnifiedConfig.from_dict(config_payload)
        completed = await execute_ai_request(
            config,
            max_iterations=1,
            max_retries_per_iteration=2,
            metadata=inputs.metadata or None,
        )

        response = getattr(completed, "final_response", None)
        videos = _shape_video_blocks(response)

        usage_raw = getattr(completed, "total_usage", None)
        # One canonical extractor (shared with the failure path below) — the
        # old hand-rolled loop read a non-existent ``totals`` attribute off
        # AggregatedUsage and silently reported empty usage.
        usage = _extract_usage(usage_raw)

        if not videos:
            # Paid call with no artifact — fail with the billed usage in
            # details so the scheduler's cost settlement records the spend.
            return failure(
                "generation_failed",
                f"ai.{video_action}_video: provider returned no videos for model '{inputs.model}'.",
                details={
                    "model": inputs.model,
                    "video_action": video_action,
                    "usage": _extract_usage(usage_raw).model_dump(mode="json"),
                },
            )

        return success(
            GenerateVideoOutput(
                videos=videos,
                count=len(videos),
                model=inputs.model,
                usage=usage,
            )
        )
    except Exception as e:
        return failure(
            "generation_failed",
            f"{type(e).__name__}: {e}",
            details={"model": inputs.model, "video_action": video_action},
        )
