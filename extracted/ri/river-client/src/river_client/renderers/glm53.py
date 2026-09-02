"""GLM-5.3 Flash renderer with chunked image-training support.

GLM's checkpoint-owned chat template remains the source of truth for turn
formatting. This renderer supplies the image framing that template expects,
uses the same resize/token-budget math as the trainer, and converts the
unexpanded image marker in a rendered training prompt into River image chunks.
"""

from __future__ import annotations

import math
from typing import cast

from river_client.renderers.base import (
    ImageChunk,
    ImageFormat,
    ImagePart,
    Message,
    ParsedResponse,
    Renderer,
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

IMAGE_BEGIN = "<|begin_of_image|>"
IMAGE_TOKEN = "<|image|>"
IMAGE_END = "<|end_of_image|>"
_IMAGE_MARKER = f"{IMAGE_BEGIN}{IMAGE_TOKEN}{IMAGE_END}"


def glm_smart_resize(
    height: int,
    width: int,
    *,
    factor: int = 28,
    min_image_tokens: int = 16,
    max_image_tokens: int = 8000,
) -> tuple[int, int]:
    """Return GLM's aligned image canvas for a still image."""
    if height <= 0 or width <= 0:
        raise ValueError(f"height/width must be positive (got {height}x{width})")
    if factor <= 0 or min_image_tokens <= 0 or max_image_tokens < min_image_tokens:
        raise ValueError(
            "require factor > 0 and 0 < min_image_tokens <= max_image_tokens "
            f"(got {factor=}, {min_image_tokens=}, {max_image_tokens=})"
        )

    # GLM's temporal factor occurs on both sides of every token-budget
    # comparison for still images, so it cancels here. The worker's Python and
    # Rust preprocessors use the same resulting canvas geometry.
    min_pixels = min_image_tokens * factor**2
    max_pixels = max_image_tokens * factor**2

    def align(value: int) -> int:
        return math.ceil(value / factor) * factor

    target_height = align(height)
    target_width = align(width)
    if target_height * target_width < min_pixels:
        scale = math.sqrt(min_pixels / (height * width))
        target_height = align(max(1, math.ceil(height * scale)))
        target_width = align(max(1, math.ceil(width * scale)))

    if target_height * target_width <= max_pixels:
        return target_height, target_width
    if max_pixels < factor**2:
        raise ValueError(
            f"max_image_tokens={max_image_tokens} is too small for one "
            "aligned GLM-5.3 image patch"
        )

    low, high = 1, height
    best_height, best_width = factor, factor
    while low <= high:
        content_height = (low + high) // 2
        content_width = max(1, width * content_height // height)
        candidate_height = align(content_height)
        candidate_width = align(content_width)
        if candidate_height * candidate_width <= max_pixels:
            best_height, best_width = candidate_height, candidate_width
            low = content_height + 1
        else:
            high = content_height - 1
    return best_height, best_width


class Glm53FlashRenderer(Renderer):
    """Vision-aware renderer for GLM-5.3 Flash.

    Tool calling is intentionally unsupported until GLM's tool-template
    contract is wired into River. Rejecting it here prevents an image-capable
    renderer from silently dropping tool declarations or tool-call history.
    """

    DEFAULT_PATCH_SIZE = 14
    DEFAULT_MERGE_SIZE = 2
    DEFAULT_MIN_IMAGE_TOKENS = 16
    DEFAULT_MAX_IMAGE_TOKENS = 8000

    def __init__(
        self,
        tokenizer: Tokenizer,
        *,
        patch_size: int = DEFAULT_PATCH_SIZE,
        merge_size: int = DEFAULT_MERGE_SIZE,
        min_image_tokens: int = DEFAULT_MIN_IMAGE_TOKENS,
        max_image_tokens: int = DEFAULT_MAX_IMAGE_TOKENS,
    ) -> None:
        super().__init__(tokenizer)
        if patch_size <= 0 or merge_size <= 0:
            raise ValueError("GLM image patch_size and merge_size must be positive")
        self.patch_size = patch_size
        self.merge_size = merge_size
        self.min_image_tokens = min_image_tokens
        self.max_image_tokens = max_image_tokens
        self._image_token_id = self._lookup_token_id(IMAGE_TOKEN)

    def _lookup_token_id(self, token: str) -> int:
        token_id = self.tokenizer.convert_tokens_to_ids(token)
        unk_token_id = getattr(self.tokenizer, "unk_token_id", None)
        if token_id is None or (unk_token_id is not None and token_id == unk_token_id):
            raise ValueError(
                f"Tokenizer does not recognize {token!r}. Glm53FlashRenderer "
                "requires the GLM-5.3 Flash tokenizer."
            )
        return int(token_id)

    def image_token_count(self, height: int, width: int) -> int:
        """Return the number of expanded GLM image placeholders."""
        target_height, target_width = glm_smart_resize(
            height,
            width,
            factor=self.patch_size * self.merge_size,
            min_image_tokens=self.min_image_tokens,
            max_image_tokens=self.max_image_tokens,
        )
        return (
            (target_height // self.patch_size)
            * (target_width // self.patch_size)
            // self.merge_size**2
        )

    def image_chunk(
        self,
        data: bytes,
        *,
        format: str = "png",
        height: int | None = None,
        width: int | None = None,
    ) -> ImageChunk:
        """Build an image chunk with checkpoint-aligned token accounting."""
        if height is None or width is None:
            height, width = image_part_size(
                image_part(data, format=cast("ImageFormat", format))
            )
        return ImageChunk(
            type="image",
            data=data,
            format=cast("ImageFormat", format),
            expected_tokens=self.image_token_count(height, width),
        )

    def _render_messages(
        self, messages: list[Message], *, tools: list[ToolSpec] | None = None
    ) -> tuple[list[dict[str, str]], list[ImagePart]]:
        if tools or any(
            "tool_calls" in message or message["role"] == "tool" for message in messages
        ):
            raise NotImplementedError(
                "GLM-5.3 Flash tool rendering is not implemented; do not combine "
                "tools or tool messages with this renderer."
            )
        rendered: list[dict[str, str]] = []
        image_parts: list[ImagePart] = []
        for message in messages:
            content = message["content"]
            if isinstance(content, str):
                rendered_content = content
            else:
                parts: list[str] = []
                for part in content:
                    part_type = part["type"]
                    if part_type == "text":
                        parts.append(cast(TextPart, part)["text"])
                    elif part_type == "thinking":
                        thinking = cast(ThinkingPart, part)["thinking"]
                        parts.append(f"<think>{thinking}</think>")
                    elif part_type == "image":
                        image_parts.append(cast(ImagePart, part))
                        parts.append(_IMAGE_MARKER)
                    else:
                        raise ValueError(
                            f"Unsupported content part type: {part_type!r}"
                        )
                rendered_content = "".join(parts)
            rendered.append({"role": message["role"], "content": rendered_content})
        return rendered, image_parts

    def _apply_template(
        self, messages: list[dict[str, str]], *, add_generation_prompt: bool
    ) -> str:
        rendered = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=add_generation_prompt,
        )
        if not isinstance(rendered, str):
            raise TypeError("GLM tokenizer chat template did not return a string")
        return rendered

    def _encode(self, prompt: str) -> list[int]:
        return list(self.tokenizer.encode(prompt, add_special_tokens=False))

    @staticmethod
    def _common_prefix_length(left: list[int], right: list[int]) -> int:
        index = 0
        while index < min(len(left), len(right)) and left[index] == right[index]:
            index += 1
        return index

    @staticmethod
    def _common_suffix_length(left: list[int], right: list[int], prefix: int) -> int:
        length = 0
        while (
            length < len(left) - prefix
            and length < len(right) - prefix
            and left[-1 - length] == right[-1 - length]
        ):
            length += 1
        return length

    def build_prompt_str(
        self,
        messages: list[Message],
        *,
        tools: list[ToolSpec] | None = None,
    ) -> str:
        rendered, _image_parts = self._render_messages(messages, tools=tools)
        return self._apply_template(rendered, add_generation_prompt=True)

    def build_sample_prompt(
        self,
        messages: list[Message],
        *,
        tools: list[ToolSpec] | None = None,
    ) -> SamplePrompt:
        rendered, image_parts = self._render_messages(messages, tools=tools)
        return SamplePrompt(
            prompt=self._apply_template(rendered, add_generation_prompt=True),
            images=[part["image"] for part in image_parts],
            image_formats=[part["format"] for part in image_parts],
        )

    def get_stop_strings(self) -> list[str]:
        eos_token = getattr(self.tokenizer, "eos_token", None)
        return [eos_token] if isinstance(eos_token, str) and eos_token else []

    def parse_response(self, text: str) -> ParsedResponse:
        for stop in self.get_stop_strings():
            if text.endswith(stop):
                return ParsedResponse(
                    message=Message(role="assistant", content=text[: -len(stop)]),
                    stop_found=True,
                )
        return ParsedResponse(
            message=Message(role="assistant", content=text),
            stop_found=False,
        )

    def build_training_example(
        self,
        messages: list[Message],
        *,
        train_on: TrainOnWhat = TrainOnWhat.LAST_ASSISTANT,
        train_on_eos: bool = True,
        max_length: int | None = None,
    ) -> TrainingExample:
        rendered, image_parts = self._render_messages(messages)
        full_ids = self._encode(
            self._apply_template(rendered, add_generation_prompt=False)
        )
        weights = [0.0] * len(full_ids)
        assistant_indexes = [
            index
            for index, message in enumerate(rendered)
            if message["role"] == "assistant"
        ]
        last_assistant_index = assistant_indexes[-1] if assistant_indexes else -1

        for index in assistant_indexes:
            if train_on == TrainOnWhat.LAST_ASSISTANT and index != last_assistant_index:
                continue
            if train_on not in (TrainOnWhat.LAST_ASSISTANT, TrainOnWhat.ALL_ASSISTANT):
                continue
            without_content = [dict(message) for message in rendered]
            without_content[index]["content"] = ""
            without_ids = self._encode(
                self._apply_template(without_content, add_generation_prompt=False)
            )
            prefix = self._common_prefix_length(full_ids, without_ids)
            suffix = self._common_suffix_length(full_ids, without_ids, prefix)
            content_end = len(full_ids) - suffix
            weights[prefix:content_end] = [1.0] * (content_end - prefix)
            if train_on_eos:
                eos_token_id = getattr(self.tokenizer, "eos_token_id", None)
                if eos_token_id is not None:
                    for token_index in range(content_end, len(full_ids)):
                        if full_ids[token_index] == eos_token_id:
                            weights[token_index] = 1.0
                            break

        builder = _ChunkBuilder()
        image_index = 0
        for token_id, weight in zip(full_ids, weights, strict=True):
            if token_id != self._image_token_id:
                builder.add_text([token_id], weight)
                continue
            if image_index >= len(image_parts):
                raise ValueError(
                    "GLM chat template contains more image markers than supplied images"
                )
            part = image_parts[image_index]
            image_index += 1
            height, width = image_part_size(part)
            builder.add_image(
                data=part["image"],
                format=part["format"],
                expected_tokens=self.image_token_count(height, width),
                placeholder_id=self._image_token_id,
            )
        if image_index != len(image_parts):
            raise ValueError(
                "GLM received images with no matching image marker in the chat template"
            )
        builder.finish()

        input_ids = builder.flat_ids
        if max_length is not None and len(input_ids) > max_length:
            model_input, expanded_length = _truncate_chunks_to_length(
                builder.chunks, max_length
            )
            input_ids = input_ids[:expanded_length]
            weights = builder.weights[:expanded_length]
        else:
            model_input = builder.chunks
            weights = builder.weights
        return TrainingExample(
            input_ids=input_ids,
            weights=weights,
            model_input=model_input,
        )


__all__ = [
    "Glm53FlashRenderer",
    "IMAGE_BEGIN",
    "IMAGE_END",
    "IMAGE_TOKEN",
    "glm_smart_resize",
]
