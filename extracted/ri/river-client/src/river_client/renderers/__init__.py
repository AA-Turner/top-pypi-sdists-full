"""Renderer module for formatting chat conversations for River's API.

Usage:
    from river_client.renderers import get_renderer, image_part

    renderer = get_renderer("Qwen/Qwen3.6-35B-A3B-FP8")

    # Text-only
    prompt = renderer.build_prompt_str(messages)

    # Multimodal SFT (vision-enabled renderers)
    messages = [
        {"role": "user", "content": [
            image_part(png_bytes, format="png", height=224, width=224),
            {"type": "text", "text": "What is this?"},
        ]},
        {"role": "assistant", "content": "A red circle."},
    ]
    example = renderer.build_training_example(messages)
    model.forward_backward(data=[example.to_dict()], loss_fn="cross_entropy")

    # Multimodal sampling
    sp = renderer.build_sample_prompt(messages[:-1])  # drop the target assistant turn
    samples = model.sample(**sp.to_kwargs())
"""

from __future__ import annotations

import re

from river_client.renderers.base import (
    ContentPart,
    EncodedTextChunk,
    ImageChunk,
    ImagePart,
    Message,
    ModelInputChunk,
    ParsedResponse,
    Renderer,
    SamplePrompt,
    TextPart,
    ThinkingPart,
    Tokenizer,
    ToolCall,
    ToolSpec,
    TrainOnWhat,
    TrainingExample,
    UnparsedToolCall,
    get_text_content,
    image_part,
    image_part_size,
    remove_thinking,
)
from river_client.renderers.deepseek import (
    DeepSeekV4Renderer,
    dsml_tools_block,
    parse_deepseek_content_blocks,
    strip_deepseek_thinking_from_text,
)
from river_client.renderers.glm53 import Glm53FlashRenderer
from river_client.renderers.kimi import (
    KimiRenderer,
    kimi_image_token_count,
    parse_kimi_k2_content_blocks,
)
from river_client.renderers.qwen3 import (
    QWEN38_REASONING_EFFORT_INSTRUCTIONS,
    Qwen35DisableThinkingRenderer,
    Qwen35Renderer,
)
from river_client.renderers.qwen3_vl import Qwen35VLRenderer


def _is_qwen_vl(name_lower: str) -> bool:
    """Detect Qwen vision-language variants by HuggingFace name conventions.

    Two naming generations:

    * **Qwen3** kept text and vision in separate checkpoint families;
      vision variants carry the explicit ``-VL-`` infix
      (``Qwen/Qwen3-VL-235B-A22B-Instruct``).
    * **Qwen3.5** unified the lineup — every Qwen3.5 checkpoint
      (``Qwen3.5-35B-A3B``, ``Qwen3.5-397B-A17B`` and any future
      sibling) is a vision-language model out of the box, using the
      same ``<|vision_start|>``/``<|image_pad|>``/``<|vision_end|>``
      tokens. There is no ``-VL-`` infix because there is no
      non-multimodal Qwen3.5 to disambiguate from.

    Qwen3.5/3.6/3.8 (and legacy ``-VL-`` names) are served today, so
    everything here routes to the vision-capable Qwen3.5 renderer.
    """
    if "qwen3-vl" in name_lower:
        return True
    # Qwen3.5 and the later minors that reuse the same architecture
    # (``model_type=qwen3_5`` through at least 3.8) are unified multimodal —
    # every checkpoint exposes the vision tokens. Enumerated rather than
    # range-matched so a future minor that breaks the pattern cannot silently
    # inherit this routing; same contract as the trainer's
    # ``is_qwen3_5_family``.
    if "qwen3.5" in name_lower or "qwen3_5" in name_lower:
        return True
    if "qwen3.6" in name_lower or "qwen3_6" in name_lower:
        return True
    if _is_qwen38_template(name_lower):
        return True
    return False


def _is_qwen38_template(name_lower: str) -> bool:
    """Detect checkpoints using the revised Qwen3.8 chat template.

    3.8 kept the Qwen3.5 architecture but changed two rendering contracts,
    so the renderer needs different defaults even though the model class is
    identical:

    * ``reasoning_effort`` (new, default ``xhigh``) prepends a fixed
      instruction to the system turn — see
      ``qwen3.QWEN38_REASONING_EFFORT_INSTRUCTIONS``.
    * ``preserve_thinking`` flipped to default-on, i.e. reasoning blocks
      from earlier assistant turns stay in the rendered history.

    Rendering a 3.8 checkpoint with the 3.6 defaults yields a prompt prefix
    the model was never post-trained on, so this is a correctness gate, not
    a cosmetic one.
    """
    return "qwen3.8" in name_lower or "qwen3_8" in name_lower


def _is_kimi(name_lower: str) -> bool:
    """Detect Kimi K2.x checkpoints by segment-anchored name matching.

    Covers ``nvidia/Kimi-K2.6-NVFP4`` (and hyphen-suffixed deployment
    aliases like ``-131K``), ``moonshotai/Kimi-K2.6``, and the K2.5
    generation, which shares the chat template, ``<|media_pad|>`` id and
    MoonViT processor. The rule is identical to the api-server's
    ``image_placeholder_token_id_for_model`` anchoring — a segment of
    ``kimi`` or ``kimi<digit>…`` — so client-side renderer selection and
    server-side ingress can never disagree on family membership
    (``kimiko`` is rejected by both; a future ``kimi2`` is accepted by
    both).
    """
    segments = re.split(r"[^a-z0-9]", name_lower)
    return any(
        seg == "kimi" or (seg.startswith("kimi") and seg[4:5].isdigit())
        for seg in segments
    )


def _is_glm53_flash(name_lower: str) -> bool:
    """Detect GLM-5.3 Flash deployment aliases by normalized name segments.

    This matches River API ingress: separators and common deployment suffixes
    are accepted, while a longer unrelated segment such as paglm53flash is
    not.
    """
    segments = [segment for segment in re.split(r"[^a-z0-9]+", name_lower) if segment]
    return any(
        "".join(segments[start : start + width]) == "glm53flash"
        for width in range(1, 5)
        for start in range(len(segments) - width + 1)
    )


def _is_deepseek_v4(name_lower: str) -> bool:
    """Detect DeepSeek V4 checkpoints by name.

    Same substring rule as river-serve's ``model_family.detect_family``, so
    client-side renderer selection and server-side family dispatch can never
    disagree. Covers ``deepseek-ai/DeepSeek-V4-Flash-0731`` and quantized
    twins that keep the ``DeepSeek-V4`` infix.

    V3-lineage checkpoints are deliberately excluded: they share the
    ``<｜User｜>``/``<｜Assistant｜>`` markers but have no thinking mode and no
    DSML tools, so rendering them as V4 would put tokens in the prompt that
    the model was never trained on.
    """
    return "deepseek-v4" in name_lower


def get_renderer(
    model_name: str,
    *,
    thinking: bool | None = None,
    strip_thinking_from_history: bool | None = None,
    tokenizer: Tokenizer | None = None,
    tokenizer_revision: str | None = None,
    reasoning_effort: str | None = None,
) -> Renderer:
    """Create a renderer by auto-detecting the model family.

    Loads the tokenizer (if not provided) and selects the correct
    renderer class based on the model name.

    Args:
        model_name: HuggingFace model name (e.g., "Qwen/Qwen3.6-35B-A3B-FP8").
        thinking: Whether to enable thinking mode. None (default) auto-detects
            from model naming heuristics. Explicitly set to override.
        strip_thinking_from_history: For thinking-enabled renderers, whether
            to strip <think> blocks from non-last assistant messages. None
            (default) takes the model family's own default — True for
            Qwen3.5/3.6 and Kimi, False for Qwen3.8, whose template flipped
            ``preserve_thinking`` to default-on.
        tokenizer: Pre-loaded tokenizer. If None, loads via AutoTokenizer.
        tokenizer_revision: Optional immutable Hugging Face revision used when
            loading the tokenizer.
        reasoning_effort: Qwen3.8 only — ``xhigh`` (the model's own default),
            ``medium`` or ``low``. None takes the family default. Passing it
            for a family whose template has no such control is an error
            rather than a silent no-op.

    Returns:
        Configured Renderer instance.

    Raises:
        ValueError: If the model family is not supported, or if
            ``reasoning_effort`` is set for a family that does not have it.
    """
    if tokenizer is None:
        # Route through the River tokenizer loader so hyphen-suffixed
        # deployment aliases (e.g. ``nvidia/Kimi-K2.6-NVFP4-131K``)
        # resolve to their canonical tokenizer repo instead of 404ing.
        from river_client.tokenizers import load_tokenizer

        tokenizer = load_tokenizer(
            base_model=model_name,
            revision=tokenizer_revision,
        )

    name_lower = model_name.lower()
    is_qwen38 = _is_qwen38_template(name_lower)

    if reasoning_effort is not None and not is_qwen38:
        raise ValueError(
            f"reasoning_effort is not supported for {model_name}. Only the "
            f"Qwen3.8 chat template defines it; Qwen3.5/3.6 and Kimi have no "
            f"equivalent control, so setting it here would be silently "
            f"dropped."
        )

    if _is_qwen_vl(name_lower):
        # Qwen3.5+ are unified vision models served with the qwen3_coder
        # tool dialect. The vision renderer carries the shared chat/tool/
        # thinking logic plus <|vision_start|>/<|vision_end|>/<|image_pad|>.
        from river_client.renderers.qwen3_vl import Qwen35VLRenderer

        return Qwen35VLRenderer(
            tokenizer,
            # 3.8 defaults ``preserve_thinking`` on, which is the inverse of
            # this flag; 3.5/3.6 default it off.
            strip_thinking_from_history=(
                not is_qwen38
                if strip_thinking_from_history is None
                else strip_thinking_from_history
            ),
            thinking=True if thinking is None else thinking,
            reasoning_effort=((reasoning_effort or "xhigh") if is_qwen38 else None),
        )

    if _is_glm53_flash(name_lower):
        return Glm53FlashRenderer(tokenizer)

    if _is_kimi(name_lower):
        return KimiRenderer(
            tokenizer,
            strip_thinking_from_history=(
                True
                if strip_thinking_from_history is None
                else strip_thinking_from_history
            ),
            thinking=True if thinking is None else thinking,
        )

    if _is_deepseek_v4(name_lower):
        return DeepSeekV4Renderer(
            tokenizer,
            # The reference encoder drops history reasoning by default.
            strip_thinking_from_history=(
                True
                if strip_thinking_from_history is None
                else strip_thinking_from_history
            ),
            thinking=True if thinking is None else thinking,
        )

    raise ValueError(
        f"Unsupported model: {model_name}. "
        f"Supported families: Qwen3.5 / Qwen3.6 / Qwen3.8 (e.g. "
        f"Qwen/Qwen3.8-27B-FP8), Kimi K2.5/K2.6 (e.g. "
        f"nvidia/Kimi-K2.6-NVFP4), GLM-5.3 Flash (e.g. "
        f"zai-org/GLM-5.3-Flash) and DeepSeek V4 (e.g. "
        f"deepseek-ai/DeepSeek-V4-Flash-0731). Construct a renderer "
        f"directly, e.g., Qwen35VLRenderer(tokenizer) / Glm53FlashRenderer(tokenizer) / "
        f"KimiRenderer(tokenizer) / DeepSeekV4Renderer(tokenizer)."
    )


__all__ = [
    # Content types
    "ContentPart",
    "ImagePart",
    "Message",
    "ParsedResponse",
    "Renderer",
    "TextPart",
    "ThinkingPart",
    # Chunk types for the multimodal wire format
    "EncodedTextChunk",
    "ImageChunk",
    "ModelInputChunk",
    # Training/inference output types
    "SamplePrompt",
    "TrainingExample",
    # Tooling
    "Tokenizer",
    "ToolCall",
    "ToolSpec",
    "TrainOnWhat",
    "UnparsedToolCall",
    # Concrete renderers
    "DeepSeekV4Renderer",
    "Glm53FlashRenderer",
    "KimiRenderer",
    "QWEN38_REASONING_EFFORT_INSTRUCTIONS",
    "Qwen35DisableThinkingRenderer",
    "Qwen35Renderer",
    "Qwen35VLRenderer",
    "dsml_tools_block",
    "parse_deepseek_content_blocks",
    "parse_kimi_k2_content_blocks",
    "strip_deepseek_thinking_from_text",
    # Factory
    "get_renderer",
    # Construction helpers
    "image_part",
    "image_part_size",
    "kimi_image_token_count",
    # Generic content utilities
    "get_text_content",
    "remove_thinking",
]
