"""GLM-5.3 Flash renderer with chunked image-training support.

GLM's checkpoint-owned chat template remains the source of truth for turn
formatting. This renderer supplies the image framing that template expects,
uses the same resize/token-budget math as the trainer, and converts the
unexpanded image marker in a rendered training prompt into River image chunks.
"""

from __future__ import annotations

import json
import math
import re
from typing import Any, cast

from river_client.renderers.base import (
    ContentPart,
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
    ToolCall,
    ToolCallFunction,
    ToolSpec,
    TrainOnWhat,
    TrainingExample,
    UnparsedToolCall,
    _ChunkBuilder,
    _truncate_chunks_to_length,
    image_part,
    image_part_size,
)

IMAGE_BEGIN = "<|begin_of_image|>"
IMAGE_TOKEN = "<|image|>"
IMAGE_END = "<|end_of_image|>"
_IMAGE_MARKER = f"{IMAGE_BEGIN}{IMAGE_TOKEN}{IMAGE_END}"
_EOS = "<|endoftext|>"
_OBSERVATION = "<|observation|>"
_THINK_OPEN = "<think>"
_THINK_CLOSE = "</think>"
_TOOL_CALL_OPEN = "<tool_call>"
_TOOL_CALL_CLOSE = "</tool_call>"
_ARG_KEY_OPEN = "<arg_key>"
_ARG_KEY_CLOSE = "</arg_key>"
_ARG_VALUE_OPEN = "<arg_value>"
_ARG_VALUE_CLOSE = "</arg_value>"
_TOOL_NAME_RE = re.compile(r"[A-Za-z_]\w*", re.ASCII)


def _parse_glm53_tool_call(body: str, raw_text: str) -> ToolCall | UnparsedToolCall:
    """Parse GLM's ``name<arg_key>key</arg_key>...`` call dialect.

    Argument values deliberately stay strings. The checkpoint's template has
    no type marker: it writes strings verbatim and serializes non-strings as
    JSON, so decoding values that merely *look* like JSON would change a
    subsequent template render.
    """
    body = body.strip()
    first_arg = body.find(_ARG_KEY_OPEN)
    name = (body if first_arg < 0 else body[:first_arg]).strip()
    if not name:
        return UnparsedToolCall(raw_text=raw_text, error="Missing function name")
    if _TOOL_NAME_RE.fullmatch(name) is None:
        return UnparsedToolCall(
            raw_text=raw_text,
            error=f"Invalid GLM function name: {name!r}",
        )
    if first_arg < 0:
        return ToolCall(
            type="function",
            id=None,
            function=ToolCallFunction(name=name, arguments="{}"),
        )

    arguments: dict[str, str] = {}
    remaining = body[first_arg:]
    while remaining.strip():
        if not remaining.startswith(_ARG_KEY_OPEN):
            return UnparsedToolCall(
                raw_text=raw_text, error="Malformed GLM argument key"
            )
        key_end = remaining.find(_ARG_KEY_CLOSE, len(_ARG_KEY_OPEN))
        if key_end < 0:
            return UnparsedToolCall(
                raw_text=raw_text, error="Unclosed GLM argument key"
            )
        key = remaining[len(_ARG_KEY_OPEN) : key_end].strip()
        if not key:
            return UnparsedToolCall(raw_text=raw_text, error="Missing argument name")
        remaining = remaining[key_end + len(_ARG_KEY_CLOSE) :].lstrip()
        if not remaining.startswith(_ARG_VALUE_OPEN):
            return UnparsedToolCall(
                raw_text=raw_text, error="Missing GLM argument value"
            )
        value_end = remaining.find(_ARG_VALUE_CLOSE, len(_ARG_VALUE_OPEN))
        if value_end < 0:
            return UnparsedToolCall(
                raw_text=raw_text, error="Unclosed GLM argument value"
            )
        if key in arguments:
            return UnparsedToolCall(
                raw_text=raw_text, error=f"Duplicate GLM argument name: {key}"
            )
        arguments[key] = remaining[len(_ARG_VALUE_OPEN) : value_end]
        remaining = remaining[value_end + len(_ARG_VALUE_CLOSE) :].lstrip()

    return ToolCall(
        type="function",
        id=None,
        function=ToolCallFunction(
            name=name,
            arguments=json.dumps(arguments, ensure_ascii=False),
        ),
    )


def parse_glm53_content_blocks(
    content: str,
    *,
    thinking: bool | None = None,
) -> tuple[list[ContentPart], list[ToolCall | UnparsedToolCall]]:
    """Parse a GLM-5.3 Flash completion into reasoning, text, and tools.

    ``thinking`` says whether the generation prompt opened a ``<think>``
    block. When omitted, a closing (or explicit opening) think tag selects
    thinking mode; a bare tool call selects non-thinking mode. This keeps the
    public parser useful for both checkpoint-template defaults while the
    renderer itself always passes its configured mode.
    """
    if thinking is None:
        thinking = (
            content.startswith(_THINK_OPEN)
            or _THINK_CLOSE in content
            or _TOOL_CALL_OPEN not in content
        )

    parts: list[ContentPart] = []
    remainder = content
    if thinking:
        if remainder.startswith(_THINK_OPEN):
            remainder = remainder[len(_THINK_OPEN) :]
        think_end = remainder.find(_THINK_CLOSE)
        if think_end >= 0:
            reasoning = remainder[:think_end]
            remainder = remainder[think_end + len(_THINK_CLOSE) :].lstrip("\n")
        else:
            # A configured thinking prompt should normally close its block
            # before invoking a tool. Still split at a call marker so a
            # truncated or template-mismatched completion cannot silently
            # discard the invocation.
            first_tool = remainder.find(_TOOL_CALL_OPEN)
            if first_tool < 0:
                return (
                    [ThinkingPart(type="thinking", thinking=remainder)]
                    if remainder
                    else [],
                    [],
                )
            reasoning = remainder[:first_tool]
            remainder = remainder[first_tool:]
        if reasoning:
            parts.append(ThinkingPart(type="thinking", thinking=reasoning))

    tool_results: list[ToolCall | UnparsedToolCall] = []
    position = 0
    while True:
        open_at = remainder.find(_TOOL_CALL_OPEN, position)
        if open_at < 0:
            break
        text_before = remainder[position:open_at]
        if text_before:
            parts.append(TextPart(type="text", text=text_before))
        body_start = open_at + len(_TOOL_CALL_OPEN)
        close_at = remainder.find(_TOOL_CALL_CLOSE, body_start)
        if close_at < 0:
            tool_results.append(
                UnparsedToolCall(
                    raw_text=remainder[open_at:], error="Unclosed GLM tool call"
                )
            )
            return parts, tool_results
        raw_text = remainder[open_at : close_at + len(_TOOL_CALL_CLOSE)]
        tool_results.append(
            _parse_glm53_tool_call(remainder[body_start:close_at], raw_text)
        )
        position = close_at + len(_TOOL_CALL_CLOSE)
    text_after = remainder[position:]
    if text_after:
        parts.append(TextPart(type="text", text=text_after))
    return parts, tool_results


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

    The checkpoint-owned template supplies the tools instruction block and
    renders assistant calls as ``<tool_call>`` blocks. This renderer preserves
    the structured call and tool-result fields that template consumes while
    it expands GLM image markers into River image chunks.
    """

    DEFAULT_PATCH_SIZE = 14
    DEFAULT_MERGE_SIZE = 2
    DEFAULT_MIN_IMAGE_TOKENS = 16
    DEFAULT_MAX_IMAGE_TOKENS = 8000

    def __init__(
        self,
        tokenizer: Tokenizer,
        *,
        thinking: bool = True,
        strip_thinking_from_history: bool = False,
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
        self.thinking = thinking
        self.strip_thinking_from_history = strip_thinking_from_history
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
        self, messages: list[Message]
    ) -> tuple[list[dict[str, Any]], list[ImagePart]]:
        rendered: list[dict[str, Any]] = []
        image_parts: list[ImagePart] = []
        for message in messages:
            content = message["content"]
            has_structured_reasoning = isinstance(message.get("reasoning_content"), str)
            if isinstance(content, str):
                rendered_content = content
            else:
                parts: list[str] = []
                for part in content:
                    part_type = part["type"]
                    if part_type == "text":
                        parts.append(cast(TextPart, part)["text"])
                    elif part_type == "thinking":
                        if has_structured_reasoning:
                            continue
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
            rendered_content += "".join(
                call["raw_text"] for call in message.get("unparsed_tool_calls", [])
            )
            rendered_message: dict[str, Any] = {
                "role": message["role"],
                "content": rendered_content,
            }
            if "reasoning_content" in message:
                rendered_message["reasoning_content"] = message["reasoning_content"]
            if "tool_calls" in message:
                rendered_message["tool_calls"] = [
                    self._tool_call_for_template(call) for call in message["tool_calls"]
                ]
            for field in ("tool_call_id", "name"):
                if field in message:
                    rendered_message[field] = message[field]
            rendered.append(rendered_message)
        return rendered, image_parts

    @staticmethod
    def _tool_call_for_template(call: ToolCall) -> dict[str, Any]:
        """Normalize River's JSON-string arguments for GLM's Jinja template."""
        function = call["function"]
        if _TOOL_NAME_RE.fullmatch(function["name"]) is None:
            raise ValueError(f"Invalid GLM function name: {function['name']!r}")
        arguments = function.get("arguments", {})
        if isinstance(arguments, str):
            try:
                arguments = json.loads(arguments)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"GLM tool call {function['name']!r} has invalid JSON arguments"
                ) from exc
        if not isinstance(arguments, dict):
            raise ValueError(
                f"GLM tool call {function['name']!r} arguments must be a JSON object"
            )
        return {
            "type": "function",
            "id": call.get("id"),
            "function": {"name": function["name"], "arguments": arguments},
        }

    def _apply_template(
        self,
        messages: list[dict[str, Any]],
        *,
        add_generation_prompt: bool,
        tools: list[ToolSpec] | None = None,
    ) -> str:
        rendered = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=add_generation_prompt,
            tools=tools,
            enable_thinking=self.thinking,
            clear_thinking=self.strip_thinking_from_history,
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
        rendered, _image_parts = self._render_messages(messages)
        return self._apply_template(rendered, add_generation_prompt=True, tools=tools)

    def build_sample_prompt(
        self,
        messages: list[Message],
        *,
        tools: list[ToolSpec] | None = None,
    ) -> SamplePrompt:
        rendered, image_parts = self._render_messages(messages)
        return SamplePrompt(
            prompt=self._apply_template(
                rendered, add_generation_prompt=True, tools=tools
            ),
            images=[part["image"] for part in image_parts],
            image_formats=[part["format"] for part in image_parts],
        )

    def get_stop_strings(self) -> list[str]:
        stops = [_OBSERVATION]
        eos_token = getattr(self.tokenizer, "eos_token", None)
        if isinstance(eos_token, str) and eos_token and eos_token not in stops:
            stops.append(eos_token)
        elif _EOS not in stops:
            stops.append(_EOS)
        return stops

    def parse_response(self, text: str) -> ParsedResponse:
        stop_found = False
        for stop in self.get_stop_strings():
            if text.endswith(stop):
                text = text[: -len(stop)]
                stop_found = True
                break

        parts, tool_results = parse_glm53_content_blocks(text, thinking=self.thinking)
        message: Message = {"role": "assistant", "content": parts if parts else ""}
        tool_calls = [result for result in tool_results if "function" in result]
        unparsed = [result for result in tool_results if "error" in result]
        if tool_calls:
            message["tool_calls"] = tool_calls  # type: ignore[assignment]
        if unparsed:
            message["unparsed_tool_calls"] = unparsed  # type: ignore[assignment]
        return ParsedResponse(message=message, stop_found=stop_found)

    def build_training_example(
        self,
        messages: list[Message],
        *,
        train_on: TrainOnWhat = TrainOnWhat.LAST_ASSISTANT,
        train_on_eos: bool = True,
        max_length: int | None = None,
        tools: list[ToolSpec] | None = None,
    ) -> TrainingExample:
        rendered, image_parts = self._render_messages(messages)
        full_ids = self._encode(
            self._apply_template(rendered, add_generation_prompt=False, tools=tools)
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
            # The GLM template emits reasoning and calls from structured
            # fields, not ``content``. Remove all assistant output fields so
            # their token ranges receive the same training weight as text.
            without_content[index].pop("reasoning_content", None)
            without_content[index].pop("tool_calls", None)
            without_ids = self._encode(
                self._apply_template(
                    without_content, add_generation_prompt=False, tools=tools
                )
            )
            prefix = self._common_prefix_length(full_ids, without_ids)
            suffix = self._common_suffix_length(full_ids, without_ids, prefix)
            generated_end = len(full_ids) - suffix
            content_end, terminator_end = self._turn_terminator_range(
                full_ids, generated_end
            )
            weights[prefix:content_end] = [1.0] * (content_end - prefix)
            if train_on_eos and terminator_end is not None:
                weights[content_end:terminator_end] = [1.0] * (
                    terminator_end - content_end
                )

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

    def _turn_terminator_range(
        self, input_ids: list[int], generated_end: int
    ) -> tuple[int, int | None]:
        """Return the content end and adjacent stop range for one assistant turn."""
        for stop in self.get_stop_strings():
            stop_ids = self._encode(stop)
            if (
                stop_ids
                and input_ids[generated_end - len(stop_ids) : generated_end] == stop_ids
            ):
                return generated_end - len(stop_ids), generated_end
        for stop in self.get_stop_strings():
            stop_ids = self._encode(stop)
            if (
                stop_ids
                and input_ids[generated_end : generated_end + len(stop_ids)] == stop_ids
            ):
                return generated_end, generated_end + len(stop_ids)
        return generated_end, None


__all__ = [
    "Glm53FlashRenderer",
    "IMAGE_BEGIN",
    "IMAGE_END",
    "IMAGE_TOKEN",
    "glm_smart_resize",
    "parse_glm53_content_blocks",
]
