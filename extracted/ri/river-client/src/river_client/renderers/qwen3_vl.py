"""Qwen3.5 vision renderer (extends :class:`Qwen35Renderer` for images).

Qwen3-VL and Qwen3.5-VL share the same chat template (``<|im_start|>``
turn markers) and the same vision tokens (``<|vision_start|>`` /
``<|vision_end|>`` framing ``<|image_pad|>`` placeholders). This
renderer threads :class:`ImagePart` content through both the training
(chunked) and the inference (flat-string) rendering paths.

Per-image placeholder count comes from a Python port of HuggingFace's
``Qwen2VLImageProcessor.smart_resize`` so the count the renderer emits
matches what the worker's ``AutoProcessor`` will actually produce. The
``ImageChunk.expected_tokens`` field is the safety net: the worker
fails fast with ``(expected, got, h, w)`` if the prediction drifts
from what its processor produces.
"""

from __future__ import annotations

import math
from typing import cast

from river_client.renderers.base import (
    ImageChunk,
    ImagePart,
    Message,
    SamplePrompt,
    TextPart,
    ThinkingPart,
    Tokenizer,
    ToolSpec,
    TrainOnWhat,
    TrainingExample,
    _ChunkBuilder,
    _truncate_chunks_to_length,
    image_part,
    image_part_size,
)
from river_client.renderers.qwen3 import (
    Qwen35Renderer,
    _IM_END,
    _IM_START,
)


VISION_START = "<|vision_start|>"
VISION_END = "<|vision_end|>"
IMAGE_PAD = "<|image_pad|>"


def _validate_image_part_renderable(part: ImagePart) -> None:
    """Raise early on bad image bytes / extreme aspect ratios.

    Used on the inference path where ``image_part_size`` would
    otherwise be a dead expression — we don't need the dimensions
    (the worker-side vision processor re-derives them from the bytes
    and expands ``<|image_pad|>`` placeholders accordingly), but we *do*
    want renderer-side errors to surface at the client API boundary instead
    of as a processor traceback five frames deep on the worker.
    ``image_part_size`` already does PIL-based bytes validation, so calling it
    for its side-effect is the cheapest way to get that guarantee.
    """
    _ = image_part_size(part)


def smart_resize(
    height: int,
    width: int,
    *,
    factor: int = 32,
    min_pixels: int = 65536,
    max_pixels: int = 16777216,
    max_ratio: int = 200,
) -> tuple[int, int]:
    """Python port of HF's ``Qwen2VLImageProcessor.smart_resize``.

    Rounds both axes to a multiple of ``factor = patch_size *
    merge_size`` and clamps total pixels to the
    ``[min_pixels, max_pixels]`` envelope. The output matches what the
    worker's image processor will resize to, so the renderer can
    predict the per-image placeholder count exactly when callers pass
    pre-resized images.

    Defaults match Qwen3-VL's and Qwen3.5's ``preprocessor_config.json``
    on HuggingFace (``patch_size=16``, ``merge_size=2`` → ``factor=32``;
    ``shortest_edge=65536`` ≈ 256², ``longest_edge=16777216`` = 4096²).
    Older Qwen2-VL checkpoints shipped with ``patch_size=14`` / smaller
    pixel envelopes — pass overrides via :class:`Qwen35VLRenderer` ctor
    when training a Qwen2-VL.
    """
    if height <= 0 or width <= 0:
        raise ValueError(f"height/width must be positive (got {height}x{width})")
    if max(height, width) / min(height, width) > max_ratio:
        raise ValueError(
            f"Aspect ratio {max(height, width) / min(height, width):.1f} "
            f"exceeds max_ratio={max_ratio} for ({height}, {width})"
        )

    h_bar = max(factor, round(height / factor) * factor)
    w_bar = max(factor, round(width / factor) * factor)
    if h_bar * w_bar > max_pixels:
        beta = math.sqrt(height * width / max_pixels)
        h_bar = max(factor, math.floor(height / beta / factor) * factor)
        w_bar = max(factor, math.floor(width / beta / factor) * factor)
    elif h_bar * w_bar < min_pixels:
        beta = math.sqrt(min_pixels / (height * width))
        h_bar = math.ceil(height * beta / factor) * factor
        w_bar = math.ceil(width * beta / factor) * factor
    return h_bar, w_bar


class Qwen35VLRenderer(Qwen35Renderer):
    """Vision-aware renderer for Qwen3-VL / Qwen3.5-VL.

    Inherits :class:`Qwen35Renderer`'s chat template, thinking/tool
    handling, and ``parse_response``; overrides the training and
    inference rendering paths to interleave :class:`ImagePart` content
    with text by emitting ``<|vision_start|><|image_pad|>×N<|vision_end|>``
    runs at each image position.
    """

    # Defaults match Qwen3-VL's and Qwen3.5's ``preprocessor_config.json``
    # on HuggingFace. Older Qwen2-VL checkpoints shipped with
    # ``patch_size=14`` and a smaller pixel envelope — pass overrides
    # via the ctor when targeting one of those.
    DEFAULT_PATCH_SIZE = 16
    DEFAULT_MERGE_SIZE = 2
    DEFAULT_MIN_PIXELS = 65536  # 256² — Qwen3-VL/3.5 shortest_edge
    DEFAULT_MAX_PIXELS = 16777216  # 4096² — Qwen3-VL/3.5 longest_edge

    def __init__(
        self,
        tokenizer: Tokenizer,
        *,
        strip_thinking_from_history: bool = True,
        thinking: bool = True,
        reasoning_effort: str | None = None,
        patch_size: int = DEFAULT_PATCH_SIZE,
        merge_size: int = DEFAULT_MERGE_SIZE,
        min_pixels: int = DEFAULT_MIN_PIXELS,
        max_pixels: int = DEFAULT_MAX_PIXELS,
    ) -> None:
        super().__init__(
            tokenizer,
            strip_thinking_from_history=strip_thinking_from_history,
            thinking=thinking,
            reasoning_effort=reasoning_effort,
        )
        self.patch_size = patch_size
        self.merge_size = merge_size
        self.factor = patch_size * merge_size
        self.min_pixels = min_pixels
        self.max_pixels = max_pixels

        self._image_pad_id = self._lookup_token_id(IMAGE_PAD)
        self._vision_start_id = self._lookup_token_id(VISION_START)
        self._vision_end_id = self._lookup_token_id(VISION_END)

    def _lookup_token_id(self, token: str) -> int:
        tid = self.tokenizer.convert_tokens_to_ids(token)
        unk_id = getattr(self.tokenizer, "unk_token_id", None)
        if tid is None or (unk_id is not None and tid == unk_id):
            raise ValueError(
                f"Tokenizer does not recognize {token!r}. Qwen35VLRenderer "
                "requires a vision-enabled Qwen tokenizer."
            )
        return int(tid)

    # ── Token-count math ─────────────────────────────────────────────

    def image_token_count(self, height: int, width: int) -> int:
        """Return the number of ``<|image_pad|>`` slots for an image.

        Mirrors HF's smart_resize → patch grid → 2×2 spatial merge
        pipeline. The result equals what
        ``Qwen2VLImageProcessor.preprocess`` would emit for the same
        image dimensions.
        """
        h_bar, w_bar = smart_resize(
            height,
            width,
            factor=self.factor,
            min_pixels=self.min_pixels,
            max_pixels=self.max_pixels,
        )
        return (h_bar // self.factor) * (w_bar // self.factor)

    def image_chunk(
        self,
        data: bytes,
        *,
        format: str = "png",
        height: int | None = None,
        width: int | None = None,
    ) -> ImageChunk:
        """Build a ready-to-use :class:`ImageChunk` with ``expected_tokens``
        computed client-side.

        The returned chunk is valid for BOTH ``forward_backward``
        (``model_input`` datums, where the worker verifies
        ``expected_tokens`` against its processor output) and
        ``sample(model_input=...)`` — so one chunk list drives the whole
        sample → train → sample loop, with image slots contributing
        ``expected_tokens`` positions of weight 0.0 in training weights.

        ``height``/``width`` make this Pillow-free; when omitted the
        dimensions are read from the image header via Pillow.
        """
        if height is None or width is None:
            height, width = image_part_size(
                image_part(data, format=format)  # type: ignore[arg-type]
            )
        return ImageChunk(
            type="image",
            data=data,
            format=format,  # type: ignore[typeddict-item]
            expected_tokens=self.image_token_count(height, width),
        )

    # ── Training rendering ───────────────────────────────────────────

    def build_training_example(
        self,
        messages: list[Message],
        *,
        train_on: TrainOnWhat = TrainOnWhat.LAST_ASSISTANT,
        train_on_eos: bool = True,
        max_length: int | None = None,
    ) -> TrainingExample:
        """Build chunked SFT example with interleaved text + image chunks.

        Header tokens always get weight 0. Image placeholder slots
        always get weight 0 (no LM loss on visual tokens). Completion
        tokens of trainable assistant messages get weight 1; the
        trailing ``<|im_end|>`` is included in the loss iff
        ``train_on_eos`` is True.
        """
        builder = _ChunkBuilder()

        # Same reason as the text path: the trained prefix must match the
        # served one.
        messages = self._apply_reasoning_effort(messages)

        last_assistant_idx = -1
        for idx, msg in enumerate(messages):
            if msg["role"] == "assistant":
                last_assistant_idx = idx
        last_user_index = self._last_user_index(messages)

        eos_ids = self.tokenizer.encode(_IM_END, add_special_tokens=False)

        for idx, msg in enumerate(messages):
            is_assistant = msg["role"] == "assistant"
            if train_on == TrainOnWhat.LAST_ASSISTANT:
                trainable = is_assistant and idx == last_assistant_idx
            elif train_on == TrainOnWhat.ALL_ASSISTANT:
                trainable = is_assistant
            else:
                trainable = False
            content_weight = 1.0 if trainable else 0.0

            maybe_newline = "\n" if idx > 0 else ""
            role = self._get_role(msg)
            header_str = f"{maybe_newline}{_IM_START}{role}\n"
            header_ids = self.tokenizer.encode(header_str, add_special_tokens=False)
            builder.add_text(header_ids, 0.0)

            is_reasoning_turn = is_assistant and idx > last_user_index
            answer_has_text = self._render_content_for_training(
                msg,
                builder,
                content_weight=content_weight,
                is_reasoning_turn=is_reasoning_turn,
            )

            if "tool_calls" in msg:
                sep = "\n\n" if answer_has_text else ""
                tc_ids = self.tokenizer.encode(
                    sep + self._format_tool_calls(msg["tool_calls"]),
                    add_special_tokens=False,
                )
                builder.add_text(tc_ids, content_weight)

            eos_weight = 1.0 if (trainable and train_on_eos) else 0.0
            builder.add_text(eos_ids, eos_weight)

        builder.finish()

        input_ids = builder.flat_ids
        weights = builder.weights
        model_input = builder.chunks

        if max_length is not None and len(input_ids) > max_length:
            # Drive the flat slice off the *chunk-aligned* expanded
            # length so the chunked form (which can be cut earlier if
            # an image straddles the boundary) and the flat form stay
            # consistent with what TrainingExample's __post_init__
            # validates.
            model_input, expanded_length = _truncate_chunks_to_length(
                model_input, max_length
            )
            input_ids = input_ids[:expanded_length]
            weights = weights[:expanded_length]

        return TrainingExample(
            input_ids=input_ids,
            weights=weights,
            model_input=model_input,
        )

    def _render_content_for_training(
        self,
        message: Message,
        builder: _ChunkBuilder,
        *,
        content_weight: float,
        is_reasoning_turn: bool,
    ) -> bool:
        """Render one message's content into ``builder``.

        Returns whether the answer (post-``<think>``) carried any text/image
        content, so the caller can decide the tool-call separator.
        """
        content = message["content"]

        if message["role"] == "tool":
            # The official Qwen3-VL template supports images INSIDE the
            # <tool_response> block, so tool-output images must render as
            # image chunks here (not get flattened to text and dropped).
            # Text is buffered so a text-only tool message tokenizes
            # identically to the old single-string encode; the buffer only
            # flushes at image boundaries, which is lossless because the
            # vision markers are special tokens.
            if isinstance(content, str):
                full = f"<tool_response>\n{content}\n</tool_response>"
                builder.add_text(
                    self.tokenizer.encode(full, add_special_tokens=False),
                    content_weight,
                )
                return True
            buf = "<tool_response>\n"
            for p in content:
                ptype = p["type"]
                if ptype == "text":
                    buf += cast(TextPart, p)["text"]
                elif ptype == "thinking":
                    buf += f"<think>{cast(ThinkingPart, p)['thinking']}</think>"
                elif ptype == "image":
                    part = cast(ImagePart, p)
                    h, w = image_part_size(part)
                    expected = self.image_token_count(h, w)
                    if buf:
                        builder.add_text(
                            self.tokenizer.encode(buf, add_special_tokens=False),
                            content_weight,
                        )
                        buf = ""
                    builder.add_text([self._vision_start_id], 0.0)
                    builder.add_image(
                        data=part["image"],
                        format=part["format"],
                        expected_tokens=expected,
                        placeholder_id=self._image_pad_id,
                    )
                    builder.add_text([self._vision_end_id], 0.0)
                else:
                    raise ValueError(f"Unsupported content part type: {ptype!r}")
            buf += "\n</tool_response>"
            builder.add_text(
                self.tokenizer.encode(buf, add_special_tokens=False), content_weight
            )
            return True

        emit_think = message["role"] == "assistant" and (
            is_reasoning_turn or not self.strip_thinking_from_history
        )

        if isinstance(content, str):
            reasoning, text = self._split_reasoning(message)
            if emit_think:
                builder.add_text(
                    self.tokenizer.encode(
                        f"<think>\n{reasoning}\n</think>\n\n", add_special_tokens=False
                    ),
                    content_weight,
                )
            if text:
                builder.add_text(
                    self.tokenizer.encode(text, add_special_tokens=False),
                    content_weight,
                )
            return bool(text.strip())

        parts = [p for p in content if p["type"] != "thinking"]
        if emit_think:
            reasoning = "".join(
                p["thinking"] for p in content if p["type"] == "thinking"
            ).strip()
            builder.add_text(
                self.tokenizer.encode(
                    f"<think>\n{reasoning}\n</think>\n\n", add_special_tokens=False
                ),
                content_weight,
            )

        answer_has_content = False
        for p in parts:
            ptype = p["type"]
            if ptype == "text":
                part = cast(TextPart, p)
                if part["text"].strip():
                    answer_has_content = True
                tokens = self.tokenizer.encode(part["text"], add_special_tokens=False)
                builder.add_text(tokens, content_weight)
            elif ptype == "image":
                part = cast(ImagePart, p)
                answer_has_content = True
                h, w = image_part_size(part)
                expected = self.image_token_count(h, w)
                builder.add_text([self._vision_start_id], 0.0)
                builder.add_image(
                    data=part["image"],
                    format=part["format"],
                    expected_tokens=expected,
                    placeholder_id=self._image_pad_id,
                )
                builder.add_text([self._vision_end_id], 0.0)
            else:
                raise ValueError(f"Unsupported content part type: {ptype!r}")
        return answer_has_content

    # ── Inference rendering ──────────────────────────────────────────

    def build_sample_prompt(
        self,
        messages: list[Message],
        *,
        tools: list[ToolSpec] | None = None,
    ) -> SamplePrompt:
        """Render a conversation for inference with expanded image placeholders.

        The returned ``prompt`` already contains the per-image
        ``<|vision_start|><|image_pad|>×N<|vision_end|>`` run for each
        :class:`ImagePart` in document order, so the inference tokenizer can
        splice features at the right positions without re-running the chat
        template.
        """
        msgs = list(messages)
        if tools:
            tool_msg = self.build_system_message_with_tools(
                tools,
                system_prompt=self._extract_system_prompt(msgs),
            )
            msgs = self._replace_or_prepend_system(msgs, tool_msg)
        msgs = self._apply_reasoning_effort(msgs)

        prompt_parts: list[str] = []
        images: list[bytes] = []
        image_formats: list[str] = []

        last_user_index = self._last_user_index(msgs)
        for idx, msg in enumerate(msgs):
            maybe_newline = "\n" if idx > 0 else ""
            role = self._get_role(msg)
            prompt_parts.append(f"{maybe_newline}{_IM_START}{role}\n")

            content_str, answer_has_text = self._render_content_for_sample(
                msg,
                images,
                image_formats,
                is_reasoning_turn=(
                    msg["role"] == "assistant" and idx > last_user_index
                ),
            )
            prompt_parts.append(content_str)

            if "tool_calls" in msg:
                tc_text = self._format_tool_calls(msg["tool_calls"])
                # Separator keys off the *answer* text (post-<think>), not the
                # whole rendered string — otherwise a reasoning turn whose only
                # output is a tool call would inject an extra blank line vs the
                # training path (and the official template).
                sep = "\n\n" if answer_has_text else ""
                prompt_parts.append(sep + tc_text)

            prompt_parts.append(_IM_END)

        prefix = "\n" if msgs else ""
        prompt_parts.append(
            f"{prefix}{_IM_START}assistant\n{self._generation_think_prefix()}"
        )

        return SamplePrompt(
            prompt="".join(prompt_parts),
            images=images,
            image_formats=image_formats,
        )

    def _render_content_for_sample(
        self,
        message: Message,
        images: list[bytes],
        image_formats: list[str],
        *,
        is_reasoning_turn: bool,
    ) -> tuple[str, bool]:
        """Render content for the sample prompt.

        Returns ``(rendered, answer_has_text)`` where ``answer_has_text``
        reflects whether the answer (post-``<think>``) carried any text/image
        content — used to pick the tool-call separator consistently with the
        training path.
        """
        content = message["content"]

        if message["role"] == "tool":
            # Mirrors the training path: tool-output images render as
            # single-placeholder runs inside the <tool_response> block per
            # the official Qwen3-VL template.
            if isinstance(content, str):
                return f"<tool_response>\n{content}\n</tool_response>", True
            rendered_tool: list[str] = ["<tool_response>\n"]
            for p in content:
                ptype = p["type"]
                if ptype == "text":
                    rendered_tool.append(cast(TextPart, p)["text"])
                elif ptype == "thinking":
                    rendered_tool.append(
                        f"<think>{cast(ThinkingPart, p)['thinking']}</think>"
                    )
                elif ptype == "image":
                    part = cast(ImagePart, p)
                    _validate_image_part_renderable(part)
                    rendered_tool.append(VISION_START + IMAGE_PAD + VISION_END)
                    images.append(part["image"])
                    image_formats.append(part["format"])
                else:
                    raise ValueError(f"Unsupported content part type: {ptype!r}")
            rendered_tool.append("\n</tool_response>")
            return "".join(rendered_tool), True

        emit_think = message["role"] == "assistant" and (
            is_reasoning_turn or not self.strip_thinking_from_history
        )

        if isinstance(content, str):
            reasoning, text = self._split_reasoning(message)
            prefix = f"<think>\n{reasoning}\n</think>\n\n" if emit_think else ""
            return prefix + text, bool(text.strip())

        parts = [p for p in content if p["type"] != "thinking"]
        rendered: list[str] = []
        if emit_think:
            reasoning = "".join(
                p["thinking"] for p in content if p["type"] == "thinking"
            ).strip()
            rendered.append(f"<think>\n{reasoning}\n</think>\n\n")
        answer_has_text = False
        for p in parts:
            ptype = p["type"]
            if ptype == "text":
                part = cast(TextPart, p)
                if part["text"].strip():
                    answer_has_text = True
                rendered.append(part["text"])
            elif ptype == "image":
                part = cast(ImagePart, p)
                # **Single-placeholder form** for inference. The prompt and
                # images are passed through the model processor, which expands
                # one ``<|image_pad|>`` per image into the right number of
                # LLM-side placeholders based on
                # the image processor's ``image_grid_thw``. The
                # pre-validation surfaces bad bytes / extreme aspect
                # ratios at the renderer layer instead of as a
                # confusing HF processor traceback five frames down.
                _validate_image_part_renderable(part)
                answer_has_text = True
                rendered.append(VISION_START + IMAGE_PAD + VISION_END)
                images.append(part["image"])
                image_formats.append(part["format"])
            else:
                raise ValueError(f"Unsupported content part type: {ptype!r}")
        return "".join(rendered), answer_has_text
