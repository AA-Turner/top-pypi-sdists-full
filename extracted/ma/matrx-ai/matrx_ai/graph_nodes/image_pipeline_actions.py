"""Image-pipeline actions: concept → prompt → generation → QC.

The user-facing principle: a *good* image-generation pipeline is **not**
"send a topic to an image model and pray." It is a small, well-typed
chain of actions where each step has one job and the right model::

    topic
      └─► ai.image.concept_generate      (large model — picks visual ideas)
            └─► ai.image.prompt_write    (small + strict — one image prompt per idea)
                  └─► ai.generate_image  (image model — already exists)
                        └─► ai.image.qc_judge  (vision model — pass/fail)

These three actions sit in matrx-ai because they are generic patterns
applicable to any product. The actual *workflow* that wires them
(``media.images.produce``) lives at the workflow-definition layer.

Strict-JSON output enforcement: every action that asks the model to
return structured data uses Pydantic ``model_validate_json(strict=True)``
on the response, raising :class:`ImagePipelineError` on parse failure.
The retry-on-parse-failure fallback covers transient model output
slop without masking real schema drift.
"""

from __future__ import annotations

from typing import Any

from matrx_graph.actions import register_node
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from matrx_graph.types.usl import field_extras
from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_ai.graph_nodes._strict_json import (
    StrictJsonError,
    llm_messages_to_pydantic,
    llm_to_pydantic,
    node_panel_hooks,
)

DEFAULT_CONCEPT_MODEL = "claude-sonnet-4-6"
DEFAULT_PROMPT_MODEL = "claude-haiku-4-5-20251001"
DEFAULT_QC_MODEL = "claude-sonnet-4-6"


class ImagePipelineError(StrictJsonError):
    """Raised when an image-pipeline action fails to produce valid output."""


# ============================================================================
# ai.image.concept_generate
# ============================================================================


class ImageConcept(BaseModel):
    """A visual idea a downstream prompt-writer can turn into an image prompt."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, description="Short label (3-6 words).")
    description: str = Field(
        min_length=1,
        description=(
            "One paragraph describing what the image should depict — subject, "
            "composition, key visual elements. NOT a final image prompt."
        ),
    )
    suggested_style: str = Field(
        default="",
        description=(
            "Hint for the prompt-writer: realistic photo, clean diagram, "
            "watercolor, infographic, etc. Empty string if no preference."
        ),
    )


class ConceptGenerateInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    topic: str = Field(
        min_length=1,
        description="Subject the concepts should illustrate.",
        json_schema_extra=field_extras(widget="textarea", multiline_rows=2),
    )
    audience: str | None = Field(
        default=None,
        description=(
            "Optional audience hint (e.g. '9th grade biology', "
            "'startup pitch deck'). Shapes complexity + style."
        ),
    )
    num_concepts: int = Field(default=3, ge=1, le=10)
    style_hint: str | None = Field(
        default=None,
        description="Optional global style hint applied to every concept.",
    )
    model: str = Field(default=DEFAULT_CONCEPT_MODEL)
    metadata: dict[str, JsonValue] = Field(default_factory=dict)


class ConceptGenerateOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    concepts: list[ImageConcept]


@register_node(
    name="ai.image.concept_generate",
    display_name="Brainstorm Image Ideas",
    description="Come up with visual ideas to illustrate a topic.",
    category=NodeCategory.LLM,
    determinism=ActionTier.NON_DETERMINISTIC,
    input_schema=ConceptGenerateInput,
    output_schema=ConceptGenerateOutput,
    output_kind="image_concepts_result",
    icon="lightbulb",
    tags=("ai", "image", "concept"),
)
async def image_concept_generate(
    ctx: NodeExecutionContext, inputs: ConceptGenerateInput
) -> NodeResult[ConceptGenerateOutput]:
    on_delta, on_reset = node_panel_hooks(getattr(getattr(ctx, "app", None), "emitter", None))
    audience_clause = f" The audience is: {inputs.audience}." if inputs.audience else ""
    style_clause = (
        f" Apply this overall style hint to every concept: {inputs.style_hint}."
        if inputs.style_hint
        else ""
    )

    system_instruction = (
        "You select strong visual concepts for illustrating a topic. "
        # The enforced schema (with the leading __kind discriminator) is
        # appended by llm_to_pydantic itself — a second, __kind-less copy here
        # would contradict the wire schema the model is bound to.
        "Rules:\n"
        "1. Choose visually distinct concepts — do not pick three near-identical ideas.\n"
        "2. Each concept should be illustratable in a single image.\n"
        "3. Prefer concrete, image-able subjects over abstractions.\n"
        "4. Avoid copyrighted characters, real people, brand logos.\n"
        "5. Output JSON ONLY. No prose, no preamble, no code fences."
    )
    user_message = (
        f"Topic: {inputs.topic}\n"
        f"Generate exactly {inputs.num_concepts} visual concepts.{audience_clause}{style_clause}"
    )

    try:
        # Raised errors (ImagePipelineError) are synthesized by the scheduler
        # into the same Failure shape — code = exception class name.
        return success(
            await llm_to_pydantic(
                model=inputs.model,
                system=system_instruction,
                user=user_message,
                output_cls=ConceptGenerateOutput,
                max_tokens=2048,
                metadata=inputs.metadata,
                on_delta=on_delta,
                on_reset=on_reset,
                # This node settles as the registered `image_concepts_result`
                # kind — tag the WIRE too so the streamed JSON self-identifies
                # from its first chunk (leading `__kind` const).
                wire_kind="image_concepts_result",
            )
        )
    except StrictJsonError as e:
        raise ImagePipelineError(str(e), raw_output=getattr(e, "raw_output", "")) from e


# ============================================================================
# ai.image.prompt_write
# ============================================================================


class ImagePromptSpec(BaseModel):
    """A ready-to-execute image prompt with negative-prompt + ratio guidance."""

    model_config = ConfigDict(extra="forbid")

    prompt: str = Field(min_length=1)
    negative_prompt: str = Field(default="")
    aspect_ratio: str = Field(default="1:1")
    style: str = Field(default="")


class PromptWriteInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    concept: ImageConcept = Field(
        description="The visual concept to render. Output of ai.image.concept_generate."
    )
    n_prompts: int = Field(
        default=1,
        ge=1,
        le=5,
        description="Number of prompt variations to write for this concept.",
    )
    style_preset: str | None = Field(
        default=None,
        description=(
            "Optional preset name: 'photographic', 'flat-illustration', "
            "'watercolor', 'isometric-diagram', 'cinematic'. Composes with "
            "concept.suggested_style."
        ),
    )
    aspect_ratio: str = Field(default="1:1")
    model: str = Field(default=DEFAULT_PROMPT_MODEL)
    metadata: dict[str, JsonValue] = Field(default_factory=dict)


class _PromptWriteLlmOutput(BaseModel):
    """What the MODEL is asked for — prompts only, nothing it could get wrong."""

    model_config = ConfigDict(extra="forbid")

    prompts: list[ImagePromptSpec]


class PromptWriteOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prompts: list[ImagePromptSpec]
    concept_name: str = Field(
        default="",
        description=(
            "Name of the concept these prompts render. The pipeline fans OUT "
            "over concepts and fans back IN, and without this echo a gathered "
            "prompt set cannot be traced to the idea it came from."
        ),
    )


_STYLE_PRESETS: dict[str, str] = {
    "photographic": "ultra-realistic photograph, natural lighting, shallow depth of field, 35mm",
    "flat-illustration": "flat vector illustration, bold outlines, limited color palette, clean composition",
    "watercolor": "loose watercolor painting, soft edges, paper texture, expressive brushstrokes",
    "isometric-diagram": "clean isometric diagram, 30-degree angle, labeled parts, technical illustration",
    "cinematic": "cinematic still, dramatic lighting, wide aspect, color-graded, film grain",
}


@register_node(
    name="ai.image.prompt_write",
    display_name="Write Image Prompts",
    description="Write ready-to-use image descriptions for a visual idea.",
    category=NodeCategory.LLM,
    determinism=ActionTier.NON_DETERMINISTIC,
    input_schema=PromptWriteInput,
    output_schema=PromptWriteOutput,
    output_kind="image_prompts_result",
    icon="pen-tool",
    tags=("ai", "image", "prompt"),
)
async def image_prompt_write(
    ctx: NodeExecutionContext, inputs: PromptWriteInput
) -> NodeResult[PromptWriteOutput]:
    on_delta, on_reset = node_panel_hooks(getattr(getattr(ctx, "app", None), "emitter", None))

    style_layers: list[str] = []
    if inputs.concept.suggested_style:
        style_layers.append(inputs.concept.suggested_style.strip())
    if inputs.style_preset:
        preset_text = _STYLE_PRESETS.get(inputs.style_preset, inputs.style_preset)
        style_layers.append(preset_text)
    style_block = ", ".join(s for s in style_layers if s)

    system_instruction = (
        "You write image-generation prompts. You receive ONE concept and "
        "produce ready-to-execute prompts.\n"
        # The enforced schema (with the leading __kind discriminator) is
        # appended by llm_to_pydantic itself — a second, __kind-less copy here
        # would contradict the wire schema the model is bound to.
        "Rules:\n"
        "1. Each `prompt` is a single dense sentence (40-80 words), describing "
        "subject, composition, lighting, materials, mood — in that order.\n"
        "2. `negative_prompt` lists what to avoid; keep it short, comma-separated.\n"
        "3. `aspect_ratio` reflects the user's request unless the concept "
        "demands otherwise (e.g. 'isometric-diagram' → 4:3 or 16:9).\n"
        "4. NO copyrighted characters, real people, brand logos.\n"
        "5. Output JSON ONLY. No prose, no preamble, no code fences."
    )
    user_message = (
        f"Concept name: {inputs.concept.name}\n"
        f"Concept description: {inputs.concept.description}\n"
        f"Style guidance: {style_block or 'none'}\n"
        f"Aspect ratio: {inputs.aspect_ratio}\n"
        f"Write exactly {inputs.n_prompts} prompt(s)."
    )

    try:
        # Raised errors (ImagePipelineError) are synthesized by the scheduler
        # into the same Failure shape — code = exception class name.
        written = await llm_to_pydantic(
            model=inputs.model,
            system=system_instruction,
            user=user_message,
            output_cls=_PromptWriteLlmOutput,
            max_tokens=1024,
            metadata=inputs.metadata,
            on_delta=on_delta,
            on_reset=on_reset,
            # This node settles as the registered `image_prompts_result` kind
            # (only `__kind` is required there — `concept_name` is echoed in
            # by the node after the call). Tag the WIRE so the streamed JSON
            # self-identifies from its first chunk.
            wire_kind="image_prompts_result",
        )
        return success(
            PromptWriteOutput(prompts=written.prompts, concept_name=inputs.concept.name)
        )
    except StrictJsonError as e:
        raise ImagePipelineError(str(e), raw_output=getattr(e, "raw_output", "")) from e


# ============================================================================
# ai.image.qc_judge — vision-model image evaluation
# ============================================================================


class ImageQcVerdict(BaseModel):
    """Vision-model verdict on whether an image meets the concept + criteria."""

    model_config = ConfigDict(extra="forbid")

    passed: bool
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str = Field(min_length=1)
    failure_modes: list[str] = Field(default_factory=list)
    suggested_retry_prompt: str | None = Field(
        default=None,
        description=(
            "When passed=False, an optional revised prompt to feed back to "
            "ai.image.prompt_write or ai.generate_image."
        ),
    )


class ImageQcInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    image_url: str | None = Field(
        default=None,
        description="HTTPS URL of the image. Either this or image_b64 required.",
    )
    image_b64: str | None = Field(
        default=None,
        description="Base64-encoded image data (no data: prefix).",
    )
    image_mime_type: str = Field(
        default="image/png",
        description="Required when image_b64 is supplied.",
    )
    expected_concept: ImageConcept | None = Field(
        default=None,
        description="The concept the image was supposed to depict. Strongly recommended.",
    )
    extra_criteria: list[str] = Field(
        default_factory=list,
        description=(
            "Additional pass criteria the judge should check (e.g. "
            "'no text overlay', 'photorealistic, not cartoon')."
        ),
    )
    model: str = Field(default=DEFAULT_QC_MODEL)
    api_key: str | None = Field(
        default=None,
        description="Override ANTHROPIC_API_KEY for this call.",
    )


class ImageQcOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    verdict: ImageQcVerdict
    image_url: str = Field(
        default="",
        description=(
            "The image this verdict judged, when it was given as a URL. QC runs "
            "fanned out over a batch of generated images and the gathered "
            "verdicts carried no trace of which image each one judged. Empty "
            "for an inline base64 image, which has no address to echo."
        ),
    )


async def _resolve_image_url_to_block(image_url: str) -> dict[str, Any] | None:
    """Resolve an image URL to a provider-neutral base64 content block.

    Delegates to THE ONE builder (``matrx_ai.media.media_blocks.resolve_media_block``).
    Returns ``None`` when no cloud FileManager is injected (standalone install) or
    the resolver failed, so the caller can fall back to passing the URL through.
    """
    from matrx_ai.media.media_blocks import resolve_media_block

    # Workflow image-pipeline node resolving a pipeline-produced ref — declare it.
    return await resolve_media_block(image_url, access_label="image-pipeline-node")


@register_node(
    name="ai.image.qc_judge",
    display_name="Review Image Quality",
    description="Have AI review a generated image and pass or fail it, with reasons.",
    category=NodeCategory.LLM,
    determinism=ActionTier.NON_DETERMINISTIC,
    input_schema=ImageQcInput,
    output_schema=ImageQcOutput,
    output_kind="image_qc_result",
    icon="eye",
    tags=("ai", "image", "vision", "qc"),
)
async def image_qc_judge(
    ctx: NodeExecutionContext, inputs: ImageQcInput
) -> NodeResult[ImageQcOutput]:
    on_delta, on_reset = node_panel_hooks(getattr(getattr(ctx, "app", None), "emitter", None))
    if not inputs.image_url and not inputs.image_b64:
        raise ImagePipelineError("ai.image.qc_judge requires either image_url or image_b64.")

    from matrx_ai.providers.keys import resolve_api_key

    api_key = inputs.api_key or resolve_api_key("ANTHROPIC_API_KEY")
    if not api_key:
        raise ImagePipelineError(
            "No Anthropic API key available. The host should provide one via "
            "ANTHROPIC_API_KEY or AppContext.api_keys; users do not need to "
            "supply their own."
        )

    image_block: dict[str, Any]
    if inputs.image_url:
        # NEVER hand a raw user-supplied URL to Anthropic to fetch: it may be
        # one of OUR share links (the provider would scrape share-page HTML, not
        # the S3 bytes), an expired signed URL, or an unreachable external URL.
        # Resolve to inline base64 through the canonical FileManager primitive
        # first — idempotent, recognizes our /files/{id} + share-link shapes,
        # and safely pre-fetches genuinely-external URLs. Falls back to URL
        # passthrough only on a standalone install with no cloud resolver.
        resolved = await _resolve_image_url_to_block(inputs.image_url)
        if resolved is not None:
            image_block = resolved
        else:
            image_block = {
                "type": "image",
                "url": inputs.image_url,
            }
    else:
        image_block = {
            "type": "image",
            "base64_data": inputs.image_b64,
            "mime_type": inputs.image_mime_type,
        }

    rubric_lines: list[str] = []
    if inputs.expected_concept:
        rubric_lines.append(
            f"Expected concept: {inputs.expected_concept.name} — "
            f"{inputs.expected_concept.description}"
        )
        if inputs.expected_concept.suggested_style:
            rubric_lines.append(f"Style: {inputs.expected_concept.suggested_style}")
    rubric_lines.extend(f"Criterion: {c}" for c in inputs.extra_criteria)
    rubric_text = "\n".join(rubric_lines) or "Criterion: image is well-composed and on-topic."

    text_block = {
        "type": "text",
        "text": (
            f"Evaluate the image above against this rubric:\n\n{rubric_text}\n\n"
            "Return a structured pass/fail verdict. Be strict — false positives "
            "undermine the pipeline."
        ),
    }
    try:
        verdict = await llm_messages_to_pydantic(
            model=inputs.model,
            system=(
                "You are an exacting visual-quality evaluator. Judge only the supplied "
                "image against the user's rubric and report concrete evidence."
            ),
            messages=[{"role": "user", "content": [image_block, text_block]}],
            output_cls=ImageQcVerdict,
            max_tokens=1024,
            api_keys={"ANTHROPIC_API_KEY": api_key},
            metadata=getattr(inputs, "metadata", None),
            on_delta=on_delta,
            on_reset=on_reset,
            # The MODEL emits the inner verdict, and `image_qc_verdict` is its
            # registered kind (the node then wraps it as `image_qc_result`).
            # Tagging the wire with the verdict's own kind keeps the streamed
            # claim honest — the node-level wrapper kind would name a shape
            # the stream does not have.
            wire_kind="image_qc_verdict",
        )
    except StrictJsonError as exc:
        raise ImagePipelineError(str(exc), raw_output=getattr(exc, "raw_output", "")) from exc
    return success(ImageQcOutput(verdict=verdict, image_url=inputs.image_url or ""))
