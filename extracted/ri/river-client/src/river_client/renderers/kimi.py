"""Kimi K2.5/K2.6 renderer (chat template + MoonViT vision support).

Follows the official checkpoint ``chat_template.jinja`` shipped with
``nvidia/Kimi-K2.6-NVFP4`` / ``moonshotai/Kimi-K2.6``:

* Turns are ``<|im_user|>user<|im_middle|>…<|im_end|>`` /
  ``<|im_assistant|>assistant<|im_middle|>…<|im_end|>`` — no newline
  separators between turns.
* Tool declarations are their OWN leading section
  (``<|im_system|>tool_declare<|im_middle|>{json}<|im_end|>``), not part
  of the system message.
* Tool results render under the ``<|im_system|>tool`` marker as
  ``## Return of {tool_call_id}\\n{content}``.  (River's agent-side
  ``kimi.jinja2`` historically used ``<|im_user|>tool`` — this renderer
  follows the official checkpoint template.)
* Assistant turns always carry a ``<think>…</think>`` block: empty for
  history turns, the actual reasoning for the current (post-last-user)
  turn when thinking is enabled.
* Each image renders as
  ``<|media_begin|>image<|media_content|><|media_pad|><|media_end|>``.
  Inference keeps the single un-expanded ``<|media_pad|>`` (the serving
  processor expands it); training emits an :class:`ImageChunk` whose
  ``expected_tokens`` pre-expands the placeholder run server-side.

Per-image token count is a Python port of Kimi's NaViT resize math
(``navit_resize_config`` in the model's vision processing code): unlike
Qwen's ``smart_resize`` the image is never upscaled, and the padded
``(H, W)`` are rounded up to ``merge_kernel_size * patch_size`` = 28.
The ``ImageChunk.expected_tokens`` field is the safety net — the worker
fails fast with ``(expected, got, h, w)`` if the prediction drifts from
its processor's output.
"""

from __future__ import annotations

import json
import math
import re
from typing import cast

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

# ─── Special tokens ──────────────────────────────────────────────────────

_IM_END = "<|im_end|>"
_IM_MIDDLE = "<|im_middle|>"
_IM_USER = "<|im_user|>"
_IM_ASSISTANT = "<|im_assistant|>"
_IM_SYSTEM = "<|im_system|>"

MEDIA_BEGIN = "<|media_begin|>"
MEDIA_CONTENT = "<|media_content|>"
MEDIA_PAD = "<|media_pad|>"
MEDIA_END = "<|media_end|>"

_MEDIA_IMAGE_OPEN = f"{MEDIA_BEGIN}image{MEDIA_CONTENT}"

_TOOL_CALLS_BEGIN = "<|tool_calls_section_begin|>"
_TOOL_CALLS_END = "<|tool_calls_section_end|>"
_TOOL_CALL_BEGIN = "<|tool_call_begin|>"
_TOOL_CALL_ARG_BEGIN = "<|tool_call_argument_begin|>"
_TOOL_CALL_END = "<|tool_call_end|>"

_THINK_CLOSED_RE = re.compile(r"<think>(.*?)</think>", re.DOTALL)
_THINK_OPEN_RE = re.compile(r"<think>.*$", re.DOTALL)
_TOOL_SECTION_RE = re.compile(
    re.escape(_TOOL_CALLS_BEGIN) + r"(.*?)" + re.escape(_TOOL_CALLS_END),
    re.DOTALL,
)
_TOOL_CALL_RE = re.compile(
    re.escape(_TOOL_CALL_BEGIN)
    + r"(.*?)"
    + re.escape(_TOOL_CALL_ARG_BEGIN)
    + r"(.*?)"
    + r"(?:"
    + re.escape(_TOOL_CALL_END)
    + r"|(?="
    + re.escape(_TOOL_CALL_BEGIN)
    + r")|$)",
    re.DOTALL,
)
_NAMED_CALL_ID_RE = re.compile(r"^(?:functions\.)?(?P<name>[\w.\-]+):(?P<index>\d+)$")
_BARE_CALL_ID_RE = re.compile(r"^\d+$")


# ─── NaViT token-count math ──────────────────────────────────────────────


def kimi_image_token_count(
    height: int,
    width: int,
    *,
    patch_size: int = 14,
    merge_kernel_size: int = 2,
    in_patch_limit: int = 16384,
    patch_limit_on_one_side: int = 512,
    fixed_output_tokens: int | None = None,
) -> int:
    """Number of ``<|media_pad|>`` slots Kimi's processor emits per image.

    Exact port of the NaViT resize math in Kimi's vision processing
    (``navit_resize_config``): scale = ``min(1, s1, s2, s3)`` — never
    upscales — then pad each side up to a multiple of
    ``merge_kernel_size * patch_size`` and count merged patches.
    Defaults match ``nvidia/Kimi-K2.6-NVFP4``'s
    ``preprocessor_config.json`` ``media_proc_cfg``.
    """
    if height <= 0 or width <= 0:
        raise ValueError(f"height/width must be positive (got {height}x{width})")
    if fixed_output_tokens is not None:
        return fixed_output_tokens

    s1 = math.sqrt(
        in_patch_limit
        / (max(1.0, width // patch_size) * max(1.0, height // patch_size))
    )
    s2 = patch_limit_on_one_side * patch_size / width
    s3 = patch_limit_on_one_side * patch_size / height
    scale = min(1.0, s1, s2, s3)
    side_limit = patch_limit_on_one_side * patch_size
    new_w = min(max(1, int(width * scale)), side_limit)
    new_h = min(max(1, int(height * scale)), side_limit)

    factor = merge_kernel_size * patch_size
    pad_h = (factor - new_h % factor) % factor
    pad_w = (factor - new_w % factor) % factor
    return ((new_h + pad_h) // factor) * ((new_w + pad_w) // factor)


# ─── Response-content parsing ────────────────────────────────────────────


def _infer_tool_name(tools: list[ToolSpec], arguments: object) -> str | None:
    """Infer a Kimi bare-counter call's function from its argument schema."""
    if len(tools) == 1:
        return tools[0]["name"]
    if not tools or not isinstance(arguments, dict):
        return None

    argument_keys = set(arguments)
    best_name: str | None = None
    best_score = -1
    for tool in tools:
        properties = set(tool["parameters"].get("properties", {}))
        if not properties:
            continue
        score = len(argument_keys & properties) - len(argument_keys - properties)
        if score > best_score:
            best_name = tool["name"]
            best_score = score
    return best_name


def _tool_name_for_id(
    tool_call_id: str, tools: list[ToolSpec], arguments: object
) -> str | None:
    named = _NAMED_CALL_ID_RE.fullmatch(tool_call_id)
    if named is not None:
        return named.group("name")
    if _BARE_CALL_ID_RE.fullmatch(tool_call_id) is not None:
        return _infer_tool_name(tools, arguments)
    return None


def _parse_kimi_tool_section(
    section: str, *, tools: list[ToolSpec] | None = None
) -> list[ToolCall | UnparsedToolCall]:
    """Parse one ``<|tool_calls_section_begin|>`` body.

    Call ids normally follow ``functions.{name}:{index}``; Kimi can also
    emit bare numeric ids. The latter require ``tools`` so the function can
    be inferred from the JSON argument keys. A call that cannot be identified
    or whose argument body fails JSON parsing is surfaced as an
    :class:`UnparsedToolCall` rather than silently dropped.
    """
    results: list[ToolCall | UnparsedToolCall] = []
    for call_id_raw, args_str in _TOOL_CALL_RE.findall(section):
        call_id = call_id_raw.strip()
        try:
            arguments = json.loads(args_str.strip())
        except json.JSONDecodeError as exc:
            results.append(
                UnparsedToolCall(
                    raw_text=f"{_TOOL_CALL_BEGIN}{call_id_raw}"
                    f"{_TOOL_CALL_ARG_BEGIN}{args_str}{_TOOL_CALL_END}",
                    error=f"tool call arguments are not valid JSON: {exc}",
                )
            )
            continue

        if (
            isinstance(arguments, dict)
            and "name" in arguments
            and "arguments" in arguments
        ):
            name = arguments["name"]
            arguments = arguments["arguments"]
        else:
            name = _tool_name_for_id(call_id, tools or [], arguments)

        if not isinstance(name, str):
            results.append(
                UnparsedToolCall(
                    raw_text=f"{_TOOL_CALL_BEGIN}{call_id_raw}"
                    f"{_TOOL_CALL_ARG_BEGIN}{args_str}{_TOOL_CALL_END}",
                    error=(
                        f"Could not determine Kimi tool name from call ID {call_id!r}"
                    ),
                )
            )
            continue

        results.append(
            ToolCall(
                type="function",
                id=call_id or None,
                function=ToolCallFunction(
                    name=name,
                    arguments=json.dumps(
                        arguments if isinstance(arguments, dict) else {},
                        ensure_ascii=False,
                    ),
                ),
            )
        )
    return results


def _restore_prefilled_think(text: str) -> str:
    """Restore the opening tag omitted by Kimi's generation prefill."""
    if "<think>" not in text and "</think>" in text:
        return "<think>" + text
    return text


def _parse_kimi_content_parts(text: str) -> list[ContentPart]:
    """Split Kimi response text into structured thinking and text parts."""
    parts: list[ContentPart] = []
    pos = 0
    for match in _THINK_CLOSED_RE.finditer(text):
        before = text[pos : match.start()]
        if before:
            parts.append(TextPart(type="text", text=before))
        if match.group(1):
            parts.append(ThinkingPart(type="thinking", thinking=match.group(1)))
        pos = match.end()
    remaining = text[pos:]
    if remaining:
        open_idx = remaining.find("<think>")
        if open_idx >= 0:
            # Unclosed trailing think block (truncated generation).
            if remaining[:open_idx]:
                parts.append(TextPart(type="text", text=remaining[:open_idx]))
            thinking = remaining[open_idx + len("<think>") :]
            if thinking:
                parts.append(ThinkingPart(type="thinking", thinking=thinking))
        else:
            parts.append(TextPart(type="text", text=remaining))
    return parts


def parse_kimi_k2_content_blocks(
    content: str, *, tools: list[ToolSpec] | None = None
) -> tuple[list[ContentPart], list[ToolCall | UnparsedToolCall]] | None:
    """Parse a Kimi K2 completion into text and structured tool calls.

    Kimi terminates a response with its tool-call section, so content before
    that section is returned as structured text and thinking parts. Standard
    Kimi call ids include the function name; for bare numeric ids, pass the
    original tool specifications to infer the function from the call's JSON
    argument keys.

    Returns ``None`` when the response contains no Kimi tool-call section.
    """
    section_match = _TOOL_SECTION_RE.search(content)
    if section_match is None:
        return None

    prefix = _restore_prefilled_think(content[: section_match.start()])
    parts = _parse_kimi_content_parts(prefix)
    return parts, _parse_kimi_tool_section(section_match.group(1), tools=tools)


# ─── Renderer ────────────────────────────────────────────────────────────


class KimiRenderer(Renderer):
    """Renderer for Kimi K2.5/K2.6 (text + MoonViT vision).

    ``thinking`` mirrors the official template's ``enable_thinking``:
    the generation prompt prefills ``<think>`` (model reasons) or
    ``<think></think>`` (model answers directly).
    ``strip_thinking_from_history`` empties the ``<think>`` block of
    non-current assistant turns, matching the template's history
    rendering.
    """

    def __init__(
        self,
        tokenizer: Tokenizer,
        *,
        strip_thinking_from_history: bool = True,
        thinking: bool = True,
        patch_size: int = 14,
        merge_kernel_size: int = 2,
        in_patch_limit: int = 16384,
        patch_limit_on_one_side: int = 512,
        fixed_output_tokens: int | None = None,
    ) -> None:
        super().__init__(tokenizer)
        self.strip_thinking_from_history = strip_thinking_from_history
        self.thinking = thinking
        self.patch_size = patch_size
        self.merge_kernel_size = merge_kernel_size
        self.in_patch_limit = in_patch_limit
        self.patch_limit_on_one_side = patch_limit_on_one_side
        self.fixed_output_tokens = fixed_output_tokens

        self._media_pad_id = self._lookup_token_id(MEDIA_PAD)

    def _lookup_token_id(self, token: str) -> int:
        try:
            tid = self.tokenizer.convert_tokens_to_ids(token)
        except (KeyError, ValueError) as exc:
            raise ValueError(
                f"Tokenizer does not recognize {token!r}. KimiRenderer "
                "requires the Kimi K2.5/K2.6 tokenizer."
            ) from exc
        unk_id = getattr(self.tokenizer, "unk_token_id", None)
        if tid is None or tid < 0 or (unk_id is not None and tid == unk_id):
            raise ValueError(
                f"Tokenizer does not recognize {token!r}. KimiRenderer "
                "requires the Kimi K2.5/K2.6 tokenizer."
            )
        return int(tid)

    # ── Token-count math ─────────────────────────────────────────────

    def image_token_count(self, height: int, width: int) -> int:
        """Return the number of ``<|media_pad|>`` slots for an image."""
        return kimi_image_token_count(
            height,
            width,
            patch_size=self.patch_size,
            merge_kernel_size=self.merge_kernel_size,
            in_patch_limit=self.in_patch_limit,
            patch_limit_on_one_side=self.patch_limit_on_one_side,
            fixed_output_tokens=self.fixed_output_tokens,
        )

    def image_chunk(
        self,
        data: bytes,
        *,
        format: str = "png",
        height: int | None = None,
        width: int | None = None,
    ) -> ImageChunk:
        """Build an :class:`ImageChunk` with ``expected_tokens`` computed
        client-side. ``height``/``width`` make this Pillow-free."""
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

    # ── Shared template helpers ──────────────────────────────────────

    @staticmethod
    def _last_user_index(messages: list[Message]) -> int:
        last = -1
        for i, m in enumerate(messages):
            if m["role"] == "user":
                last = i
        return last

    @staticmethod
    def _header(message: Message) -> str:
        role = message["role"]
        if role == "assistant":
            return f"{_IM_ASSISTANT}assistant{_IM_MIDDLE}"
        if role == "system":
            return f"{_IM_SYSTEM}system{_IM_MIDDLE}"
        if role == "tool":
            return f"{_IM_SYSTEM}tool{_IM_MIDDLE}"
        return f"{_IM_USER}{role}{_IM_MIDDLE}"

    @staticmethod
    def _tool_result_prefix(message: Message) -> str:
        return f"## Return of {message.get('tool_call_id', '')}\n"

    def _split_reasoning(self, message: Message) -> tuple[str, str]:
        """Split assistant content into ``(reasoning, answer_text)``."""
        content = message["content"]
        if isinstance(content, str):
            # Raw sampled text starts INSIDE the reasoning block (the
            # generation prompt prefilled "<think>"), so an un-opened
            # leading ``</think>`` means everything before it is
            # reasoning — mirror ``parse_response``'s restoration so
            # sampled text round-trips into history/training turns.
            if "<think>" not in content and "</think>" in content:
                content = "<think>" + content
            reasoning = "".join(_THINK_CLOSED_RE.findall(content)).strip()
            answer = _THINK_CLOSED_RE.sub("", content)
            answer = _THINK_OPEN_RE.sub("", answer)
            return reasoning, answer.lstrip("\n")
        reasoning = "".join(
            p["thinking"] for p in content if p["type"] == "thinking"
        ).strip()
        answer = "".join(p["text"] for p in content if p["type"] == "text")
        return reasoning, answer

    def _think_block(self, message: Message, *, is_reasoning_turn: bool) -> str:
        """The mandatory assistant ``<think>`` block (may be empty)."""
        keep = is_reasoning_turn or not self.strip_thinking_from_history
        reasoning, _ = self._split_reasoning(message)
        return f"<think>{reasoning if keep else ''}</think>"

    def _format_tool_calls(self, tool_calls: list[ToolCall]) -> str:
        parts = [_TOOL_CALLS_BEGIN]
        for i, tc in enumerate(tool_calls):
            func = tc.get("function") or {}
            name = func.get("name", "")
            args = func.get("arguments", {})
            args_str = (
                args if isinstance(args, str) else json.dumps(args, ensure_ascii=False)
            )
            call_id = tc.get("id") or f"functions.{name}:{i}"
            parts.append(
                f"{_TOOL_CALL_BEGIN}{call_id}"
                f"{_TOOL_CALL_ARG_BEGIN}{args_str}{_TOOL_CALL_END}"
            )
        parts.append(_TOOL_CALLS_END)
        return "".join(parts)

    def _tool_declare_section(self, tools: list[ToolSpec] | None) -> str:
        if not tools:
            return ""
        return (
            f"{_IM_SYSTEM}tool_declare{_IM_MIDDLE}"
            f"{json.dumps(list(tools), ensure_ascii=False)}{_IM_END}"
        )

    def _generation_prompt(self) -> str:
        think = "<think>" if self.thinking else "<think></think>"
        return f"{_IM_ASSISTANT}assistant{_IM_MIDDLE}{think}"

    def build_system_message_with_tools(
        self, tools: list[ToolSpec], system_prompt: str = ""
    ) -> Message:
        raise NotImplementedError(
            "Kimi advertises tools in a dedicated <|im_system|>tool_declare "
            "section, not inside the system message. Pass tools=... to "
            "build_prompt_str / build_sample_prompt / build_training_example."
        )

    # ── Inference rendering ──────────────────────────────────────────

    def get_stop_strings(self) -> list[str]:
        return [_IM_END]

    def build_prompt_str(
        self,
        messages: list[Message],
        *,
        tools: list[ToolSpec] | None = None,
    ) -> str:
        return self.build_sample_prompt(messages, tools=tools).prompt

    def build_sample_prompt(
        self,
        messages: list[Message],
        *,
        tools: list[ToolSpec] | None = None,
    ) -> SamplePrompt:
        """Render a conversation for inference.

        Each :class:`ImagePart` renders as a single un-expanded
        ``<|media_begin|>image<|media_content|><|media_pad|><|media_end|>``
        run (the serving processor expands the placeholder), with the raw
        bytes collected into :attr:`SamplePrompt.images` in document
        order — the api-server enforces exactly one un-expanded
        placeholder per image.
        """
        parts: list[str] = [self._tool_declare_section(tools)]
        images: list[bytes] = []
        image_formats: list[str] = []

        last_user_index = self._last_user_index(messages)
        for idx, msg in enumerate(messages):
            parts.append(self._header(msg))
            if msg["role"] == "tool":
                parts.append(self._tool_result_prefix(msg))
            if msg["role"] == "assistant":
                parts.append(
                    self._think_block(msg, is_reasoning_turn=idx > last_user_index)
                )
                _, answer = self._split_reasoning(msg)
                parts.append(answer)
            else:
                parts.append(self._render_parts_for_sample(msg, images, image_formats))
            if msg["role"] == "assistant" and "tool_calls" in msg:
                parts.append(self._format_tool_calls(msg["tool_calls"]))
            parts.append(_IM_END)

        parts.append(self._generation_prompt())
        return SamplePrompt(
            prompt="".join(parts),
            images=images,
            image_formats=image_formats,
        )

    def _render_parts_for_sample(
        self,
        message: Message,
        images: list[bytes],
        image_formats: list[str],
    ) -> str:
        content = message["content"]
        if isinstance(content, str):
            return content
        rendered: list[str] = []
        for p in content:
            ptype = p["type"]
            if ptype == "text":
                rendered.append(cast(TextPart, p)["text"])
            elif ptype == "image":
                part = cast(ImagePart, p)
                # Validates the bytes at the client boundary (decode
                # failures surface here instead of five frames deep in
                # the serving processor).
                _ = image_part_size(part)
                rendered.append(_MEDIA_IMAGE_OPEN + MEDIA_PAD + MEDIA_END)
                images.append(part["image"])
                image_formats.append(part["format"])
            elif ptype == "thinking":
                continue
            else:
                raise ValueError(f"Unsupported content part type: {ptype!r}")
        return "".join(rendered)

    # ── Response parsing ─────────────────────────────────────────────

    def parse_response(self, text: str) -> ParsedResponse:
        """Parse sampled text into a structured assistant Message."""
        stop_found = text.endswith(_IM_END)
        if stop_found:
            text = text[: -len(_IM_END)]

        text = _restore_prefilled_think(text)

        tool_results: list[ToolCall | UnparsedToolCall] = []
        section_match = _TOOL_SECTION_RE.search(text)
        if section_match:
            tool_results = _parse_kimi_tool_section(section_match.group(1))
            text = text[: section_match.start()] + text[section_match.end() :]

        parts = _parse_kimi_content_parts(text)

        message: Message = {"role": "assistant", "content": parts if parts else ""}
        tool_calls = [t for t in tool_results if "function" in t]
        unparsed = [t for t in tool_results if "error" in t]
        if tool_calls:
            message["tool_calls"] = cast("list[ToolCall]", tool_calls)
        if unparsed:
            message["unparsed_tool_calls"] = cast("list[UnparsedToolCall]", unparsed)
        return ParsedResponse(message=message, stop_found=stop_found)

    # ── Training rendering ───────────────────────────────────────────

    def build_training_example(
        self,
        messages: list[Message],
        *,
        train_on: TrainOnWhat = TrainOnWhat.LAST_ASSISTANT,
        train_on_eos: bool = True,
        max_length: int | None = None,
        tools: list[ToolSpec] | None = None,
    ) -> TrainingExample:
        """Build a chunked SFT example with interleaved text + images.

        Turn markers and media framing get weight 0. Image placeholder
        slots get weight 0 (no LM loss on visual tokens). Content of
        trainable assistant messages — including its ``<think>`` block
        and rendered tool calls — gets weight 1; the trailing
        ``<|im_end|>`` is trainable iff ``train_on_eos``.
        """
        builder = _ChunkBuilder()

        def _add(text: str, weight: float) -> None:
            if text:
                builder.add_text(
                    self.tokenizer.encode(text, add_special_tokens=False), weight
                )

        _add(self._tool_declare_section(tools), 0.0)

        last_assistant_idx = -1
        for idx, msg in enumerate(messages):
            if msg["role"] == "assistant":
                last_assistant_idx = idx
        last_user_index = self._last_user_index(messages)

        for idx, msg in enumerate(messages):
            is_assistant = msg["role"] == "assistant"
            if train_on == TrainOnWhat.LAST_ASSISTANT:
                trainable = is_assistant and idx == last_assistant_idx
            elif train_on == TrainOnWhat.ALL_ASSISTANT:
                trainable = is_assistant
            else:
                trainable = False
            content_weight = 1.0 if trainable else 0.0

            _add(self._header(msg), 0.0)

            if msg["role"] == "tool":
                _add(self._tool_result_prefix(msg), 0.0)

            if is_assistant:
                _add(
                    self._think_block(msg, is_reasoning_turn=idx > last_user_index),
                    content_weight,
                )
                _, answer = self._split_reasoning(msg)
                _add(answer, content_weight)
            else:
                self._render_parts_for_training(msg, builder, content_weight)

            if is_assistant and "tool_calls" in msg:
                _add(self._format_tool_calls(msg["tool_calls"]), content_weight)

            eos_weight = 1.0 if (trainable and train_on_eos) else 0.0
            _add(_IM_END, eos_weight)

        builder.finish()

        input_ids = builder.flat_ids
        weights = builder.weights
        model_input = builder.chunks

        if max_length is not None and len(input_ids) > max_length:
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

    def _render_parts_for_training(
        self,
        message: Message,
        builder: _ChunkBuilder,
        content_weight: float,
    ) -> None:
        content = message["content"]
        if isinstance(content, str):
            if content:
                builder.add_text(
                    self.tokenizer.encode(content, add_special_tokens=False),
                    content_weight,
                )
            return
        for p in content:
            ptype = p["type"]
            if ptype == "text":
                text = cast(TextPart, p)["text"]
                if text:
                    builder.add_text(
                        self.tokenizer.encode(text, add_special_tokens=False),
                        content_weight,
                    )
            elif ptype == "image":
                part = cast(ImagePart, p)
                h, w = image_part_size(part)
                builder.add_text(
                    self.tokenizer.encode(_MEDIA_IMAGE_OPEN, add_special_tokens=False),
                    0.0,
                )
                builder.add_image(
                    data=part["image"],
                    format=part["format"],
                    expected_tokens=self.image_token_count(h, w),
                    placeholder_id=self._media_pad_id,
                )
                builder.add_text(
                    self.tokenizer.encode(MEDIA_END, add_special_tokens=False),
                    0.0,
                )
            elif ptype == "thinking":
                continue
            else:
                raise ValueError(f"Unsupported content part type: {ptype!r}")
