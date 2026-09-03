"""Qwen3 family renderer for chat template formatting."""

from __future__ import annotations

import json
import re

from river_client.renderers.base import (
    ContentPart,
    Message,
    ParsedResponse,
    Renderer,
    TextPart,
    ThinkingPart,
    ToolCall,
    ToolSpec,
    TrainOnWhat,
    TrainingExample,
    Tokenizer,
    ToolCallFunction,
    UnparsedToolCall,
)

# ─── Constants ───────────────────────────────────────────────────────────

_IM_START = "<|im_start|>"
_IM_END = "<|im_end|>"

# ── qwen3_coder tool-call grammar ────────────────────────────────────────
# Qwen3.5/3.6 emit tool calls in the qwen3_coder XML dialect (this is also
# what sglang parses server-side via ``--tool-call-parser qwen3_coder``):
#
#   <tool_call>
#   <function=NAME>
#   <parameter=KEY>
#   VALUE
#   </parameter>
#   </function>
#   </tool_call>
#
# These regexes mirror ``sglang.srt.function_call.qwen3_coder_detector`` so
# client-side parsing matches the server's non-streaming parser, including
# the tolerance for a trailing unclosed ``<function=`` / ``<parameter=``.
_FUNCTION_RE = re.compile(r"<function=(.*?)</function>|<function=(.*)$", re.DOTALL)
_PARAMETER_RE = re.compile(
    r"<parameter=(.*?)(?:</parameter>|(?=<parameter=)|(?=</function>)|$)",
    re.DOTALL,
)

# ── Reasoning-effort instructions (Qwen3.8+) ─────────────────────────────
# Qwen3.8 added a ``reasoning_effort`` chat-template control that prepends a
# fixed instruction to the system message. Copied verbatim from the
# published ``chat_template.jinja`` — the model was post-trained on these
# exact strings, so they are model-family syntax rather than prose we own,
# and they must not be paraphrased. ``medium`` deliberately maps to no
# instruction at all (the template leaves ``reasoning_instructions`` empty),
# which is why this is a dict of strings and not a bare list of levels.
#
# Only consulted when thinking is enabled, matching the template's
# ``{%- if enable_thinking is undefined or enable_thinking is true %}``
# guard. Qwen3.5/3.6 have no such control; their renderers pass
# ``reasoning_effort=None`` and emit nothing.
QWEN38_REASONING_EFFORT_INSTRUCTIONS: dict[str, str] = {
    "xhigh": (
        "Reasoning effort is set to xhigh. Please think carefully through the "
        "task, validate key assumptions, consider plausible alternatives, and "
        "prioritize correctness, consistency, and clarity in the final answer."
    ),
    "medium": "",
    "low": (
        "Reasoning effort is set to low. Keep your thinking brief and focused, "
        "moving directly to the conclusion without unnecessary elaboration."
    ),
}


def _strip_edge_newlines(value: str) -> str:
    """Drop a single leading/trailing newline around a parameter value.

    qwen3_coder places each value on its own line between the
    ``<parameter=..>`` open tag and its close tag; the framing newlines
    are structural, not part of the value.
    """
    if value.startswith("\n"):
        value = value[1:]
    if value.endswith("\n"):
        value = value[:-1]
    return value


def _reject_json_constant(_token: str):
    raise ValueError(f"non-standard JSON constant: {_token}")


def _coerce_param_value(raw: str):
    """Best-effort typing of a parameter value without a tool schema.

    ``parse_response`` has no access to the tool definitions, so we can't
    type by declared schema the way the server-side detector does. We
    attempt a JSON decode (covering ints, floats, booleans, null, arrays
    and objects) and fall back to the raw string — matching the detector's
    "unknown type degenerates to string" behavior.

    ``parse_constant`` rejects the non-standard ``NaN``/``Infinity`` tokens
    that ``json.loads`` otherwise accepts, so they stay strings rather than
    round-tripping into a value that strict JSON consumers would choke on.
    """
    try:
        return json.loads(raw, parse_constant=_reject_json_constant)
    except (json.JSONDecodeError, ValueError):
        return raw


def _parse_qwen_tool_call_block(
    tool_call_body: str, raw_text: str
) -> ToolCall | UnparsedToolCall:
    """Parse the inside of a qwen3_coder ``<tool_call>`` block."""
    func_match = _FUNCTION_RE.search(tool_call_body)
    if not func_match:
        return UnparsedToolCall(
            raw_text=raw_text, error="No <function=...> in tool call"
        )
    func_body = func_match.group(1) or func_match.group(2) or ""
    if ">" not in func_body:
        return UnparsedToolCall(raw_text=raw_text, error="Malformed <function=...> tag")
    name_end = func_body.index(">")
    func_name = func_body[:name_end].strip()
    if not func_name:
        return UnparsedToolCall(raw_text=raw_text, error="Missing function name")

    params_str = func_body[name_end + 1 :]
    arguments: dict = {}
    for p_match in _PARAMETER_RE.findall(params_str):
        if ">" not in p_match:
            continue
        p_idx = p_match.index(">")
        p_name = p_match[:p_idx].strip()
        p_val = _strip_edge_newlines(p_match[p_idx + 1 :])
        arguments[p_name] = _coerce_param_value(p_val)

    return ToolCall(
        type="function",
        id=None,
        function=ToolCallFunction(
            name=func_name,
            arguments=json.dumps(arguments, ensure_ascii=False),
        ),
    )


def parse_qwen_content_blocks(
    content: str,
) -> tuple[list[ContentPart], list[ToolCall | UnparsedToolCall]] | None:
    """Parse Qwen3 <think> and <tool_call> response blocks.

    Qwen3 thinking/tool tags are model-family syntax, not renderer-generic
    syntax. Closed blocks are parsed wherever they appear. A trailing unclosed
    <think> block is treated as thinking because long generations can truncate
    before emitting </think>.
    """
    if "<think>" not in content and "<tool_call>" not in content:
        return None

    parts: list[ContentPart] = []
    tool_calls: list[ToolCall | UnparsedToolCall] = []
    pos = 0

    pattern = re.compile(
        r"<think>(.*?)</think>|<tool_call>(.*?)</tool_call>", re.DOTALL
    )

    for match in pattern.finditer(content):
        text_before = content[pos : match.start()]
        if text_before:
            parts.append(TextPart(type="text", text=text_before))

        if match.group(1) is not None:
            thinking = match.group(1)
            if thinking:
                parts.append(ThinkingPart(type="thinking", thinking=thinking))
        else:
            tool_call_body = match.group(2)
            raw_text = match.group(0)
            tool_calls.append(_parse_qwen_tool_call_block(tool_call_body, raw_text))

        pos = match.end()

    remaining = content[pos:]
    if remaining:
        think_start = remaining.find("<think>")
        tool_start = remaining.find("<tool_call>")
        if think_start >= 0 and (tool_start < 0 or think_start < tool_start):
            text_before = remaining[:think_start]
            if text_before:
                parts.append(TextPart(type="text", text=text_before))
            thinking = remaining[think_start + len("<think>") :]
            if thinking:
                parts.append(ThinkingPart(type="thinking", thinking=thinking))
        else:
            parts.append(TextPart(type="text", text=remaining))

    return parts, tool_calls


def _normalize_thinking_whitespace(parts: list[ContentPart]) -> list[ContentPart]:
    """Trim the structural whitespace the template puts around ``<think>``.

    The official template renders reasoning as ``<think>\\n{r}\\n</think>\\n\\n``
    then the answer, and on the way back trims the reasoning and strips the
    leading newlines off the following text. Mirror that so a parsed message
    round-trips cleanly through :meth:`_render_message_text`.
    """
    normalized: list[ContentPart] = []
    prev_thinking = False
    for p in parts:
        if p["type"] == "thinking":
            normalized.append(
                ThinkingPart(type="thinking", thinking=p["thinking"].strip())
            )
            prev_thinking = True
        elif p["type"] == "text":
            text_val = p["text"].lstrip("\n") if prev_thinking else p["text"]
            normalized.append(TextPart(type="text", text=text_val))
            prev_thinking = False
        else:
            normalized.append(p)
            prev_thinking = False
    return normalized


def strip_qwen_thinking_from_text(text: str) -> str:
    """Remove Qwen3 thinking blocks from text history."""
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    text = re.sub(r"<think>.*$", "", text, flags=re.DOTALL)
    return text.lstrip()


class Qwen35Renderer(Renderer):
    """Renderer for the unified Qwen3.5+ family (3.5, 3.6, 3.8).

    Qwen3.5+ are unified (vision-capable) checkpoints served with the
    qwen3_coder tool-calling dialect (``<function=..><parameter=..>``) and
    the ``<|im_start|>``/``<|im_end|>`` chat template with ``<think>``
    reasoning blocks. This class owns the text/tool/thinking rendering;
    :class:`~river_client.renderers.qwen3_vl.Qwen35VLRenderer` extends it to
    interleave image content.

    ``strip_thinking_from_history`` controls whether ``<think>`` blocks are
    dropped from non-last assistant messages in multi-turn history. It is
    the inverse of the official template's ``preserve_thinking``, whose
    default flipped between generations: 3.5/3.6 default to dropping
    history thinking, 3.8 defaults to preserving it. :func:`get_renderer`
    picks the right default per model name; construct directly only if you
    want to override it.

    ``reasoning_effort`` is the Qwen3.8 control described in
    :data:`QWEN38_REASONING_EFFORT_INSTRUCTIONS`. ``None`` (3.5/3.6) emits
    nothing.

    Template format:
        <|im_start|>system
        {content}<|im_end|>
        <|im_start|>user
        {content}<|im_end|>
        <|im_start|>assistant
        {content}<|im_end|>
    """

    def __init__(
        self,
        tokenizer: Tokenizer,
        *,
        strip_thinking_from_history: bool = True,
        thinking: bool = True,
        reasoning_effort: str | None = None,
    ) -> None:
        super().__init__(tokenizer)
        self.strip_thinking_from_history = strip_thinking_from_history
        # ``thinking=False`` mirrors the official template's
        # ``enable_thinking=False``: the generation prompt prefills an empty
        # reasoning block so the model answers directly. It only changes the
        # generation prefill — assistant turns still render their (possibly
        # empty) ``<think>`` block, exactly like the HF template.
        self.thinking = thinking
        if (
            reasoning_effort is not None
            and reasoning_effort not in QWEN38_REASONING_EFFORT_INSTRUCTIONS
        ):
            # The official template raises on an unknown level rather than
            # silently falling back, so a typo can't quietly change how the
            # model reasons. Match that.
            supported = ", ".join(sorted(QWEN38_REASONING_EFFORT_INSTRUCTIONS))
            raise ValueError(
                f"Unsupported reasoning_effort {reasoning_effort!r}. "
                f"Supported levels: {supported}."
            )
        self.reasoning_effort = reasoning_effort

    # ── Prompt building ──────────────────────────────────────────────

    def build_prompt_str(
        self,
        messages: list[Message],
        *,
        tools: list[ToolSpec] | None = None,
    ) -> str:
        """Render messages into a Qwen3 prompt string for sampling.

        Args:
            messages: Conversation history.
            tools: Optional tool specs injected into the system message.

        Returns:
            Complete prompt string ending with generation prompt.
        """
        msgs = list(messages)

        # Inject tools into system message
        if tools:
            tool_msg = self.build_system_message_with_tools(
                tools,
                system_prompt=self._extract_system_prompt(msgs),
            )
            # Replace existing system message or prepend
            msgs = self._replace_or_prepend_system(msgs, tool_msg)
        msgs = self._apply_reasoning_effort(msgs)

        last_user_index = self._last_user_index(msgs)
        parts: list[str] = []
        for idx, msg in enumerate(msgs):
            header, content = self._render_message_text(
                msg,
                is_reasoning_turn=(
                    msg["role"] == "assistant" and idx > last_user_index
                ),
                idx=idx,
            )
            parts.append(header + content)

        # Generation prompt. The official Qwen3.5/3.6 template prefills the
        # opening reasoning tag (``<think>\n`` for thinking mode); the
        # disable-thinking variant prefills an empty block instead.
        prefix = "\n" if parts else ""
        parts.append(f"{prefix}{_IM_START}assistant\n{self._generation_think_prefix()}")
        return "".join(parts)

    def get_stop_strings(self) -> list[str]:
        return [_IM_END]

    @staticmethod
    def _last_user_index(messages: list[Message]) -> int:
        """Index of the last ``user`` message (tool turns don't count)."""
        last = -1
        for i, m in enumerate(messages):
            if m["role"] == "user":
                last = i
        return last

    def _generation_think_prefix(self) -> str:
        """Reasoning prefix appended to the generation prompt.

        ``<think>\\n`` for thinking mode; an empty ``<think>\\n\\n</think>\\n\\n``
        block when thinking is disabled.
        """
        return "<think>\n" if self.thinking else "<think>\n\n</think>\n\n"

    # ── Response parsing ─────────────────────────────────────────────

    def parse_response(self, text: str) -> ParsedResponse:
        """Parse sampled text into a structured assistant Message.

        Strips trailing <|im_end|> if present. Extracts <think> and
        <tool_call> blocks into structured parts.
        """
        stop_found = text.endswith(_IM_END)
        if stop_found:
            text = text[: -len(_IM_END)]

        # The generation prompt prefills the opening "<think>\n", so sampled
        # text starts inside the reasoning block. Restore the tag so the
        # think block parses into a ThinkingPart.
        if "<think>" not in text and "</think>" in text:
            text = "<think>\n" + text

        message: Message = {"role": "assistant", "content": text}

        result = parse_qwen_content_blocks(text)
        if result is not None:
            parts, tool_results = result
            message["content"] = _normalize_thinking_whitespace(parts)
            tool_calls = [t for t in tool_results if "function" in t]
            unparsed = [t for t in tool_results if "error" in t]
            if tool_calls:
                message["tool_calls"] = tool_calls  # type: ignore[assignment]
            if unparsed:
                message["unparsed_tool_calls"] = unparsed  # type: ignore[assignment]

        return ParsedResponse(message=message, stop_found=stop_found)

    # ── SFT training ─────────────────────────────────────────────────

    def build_training_example(
        self,
        messages: list[Message],
        *,
        train_on: TrainOnWhat = TrainOnWhat.LAST_ASSISTANT,
        train_on_eos: bool = True,
        max_length: int | None = None,
        tools: list[ToolSpec] | None = None,
    ) -> TrainingExample:
        """Build input_ids and per-token weights for SFT.

        Tokenizes each message as header + content separately.
        Headers always get weight=0. Content weight depends on train_on.

        Args:
            messages: Full conversation including target assistant response.
            train_on: Which assistant messages get weight=1.
            train_on_eos: If True, include <|im_end|> in trainable weights.
            max_length: Truncate from end if set.
        """
        all_ids: list[int] = []
        all_weights: list[float] = []

        # Training must see the same system turn inference will, or the LoRA
        # is fit against a prompt prefix the served model never gets.
        messages = list(messages)
        if tools:
            tool_msg = self.build_system_message_with_tools(
                tools,
                system_prompt=self._extract_system_prompt(messages),
            )
            messages = self._replace_or_prepend_system(messages, tool_msg)
        messages = self._apply_reasoning_effort(messages)

        last_assistant_idx = -1
        for idx, msg in enumerate(messages):
            if msg["role"] == "assistant":
                last_assistant_idx = idx
        last_user_index = self._last_user_index(messages)

        for idx, msg in enumerate(messages):
            header_str, content_str = self._render_message_text(
                msg,
                is_reasoning_turn=(
                    msg["role"] == "assistant" and idx > last_user_index
                ),
                idx=idx,
            )

            header_ids = self.tokenizer.encode(header_str, add_special_tokens=False)
            content_ids = self.tokenizer.encode(content_str, add_special_tokens=False)

            # Determine if this message's content is trainable
            is_assistant = msg["role"] == "assistant"
            if train_on == TrainOnWhat.LAST_ASSISTANT:
                trainable = is_assistant and idx == last_assistant_idx
            elif train_on == TrainOnWhat.ALL_ASSISTANT:
                trainable = is_assistant
            else:
                trainable = False

            content_weight = 1.0 if trainable else 0.0

            # Header: always weight=0
            all_ids.extend(header_ids)
            all_weights.extend([0.0] * len(header_ids))

            if trainable and not train_on_eos:
                # Split content into pre-eos and eos
                eos_ids = self.tokenizer.encode(_IM_END, add_special_tokens=False)
                if (
                    len(content_ids) >= len(eos_ids)
                    and content_ids[-len(eos_ids) :] == eos_ids
                ):
                    pre_eos = content_ids[: -len(eos_ids)]
                    all_ids.extend(pre_eos)
                    all_weights.extend([content_weight] * len(pre_eos))
                    all_ids.extend(eos_ids)
                    all_weights.extend([0.0] * len(eos_ids))
                else:
                    all_ids.extend(content_ids)
                    all_weights.extend([content_weight] * len(content_ids))
            else:
                all_ids.extend(content_ids)
                all_weights.extend([content_weight] * len(content_ids))

        if max_length is not None and len(all_ids) > max_length:
            all_ids = all_ids[:max_length]
            all_weights = all_weights[:max_length]

        return TrainingExample(input_ids=all_ids, weights=all_weights)

    # ── Tool support ─────────────────────────────────────────────────

    def build_system_message_with_tools(
        self, tools: list[ToolSpec], system_prompt: str = ""
    ) -> Message:
        """Create system message with qwen3_coder tool specifications.

        Qwen3.5/3.6 use the qwen3_coder tool-calling dialect: function
        signatures are advertised in a ``<tools>`` block and each call is
        emitted as ``<function=..>`` with nested ``<parameter=..>`` tags
        (NOT the older Hermes JSON-in-``<tool_call>`` form). This matches
        how the model is served (``--tool-call-parser qwen3_coder``) and
        how :meth:`_format_tool_calls` renders history.
        """
        tools_text = ""
        if tools:
            # ``tojson`` in the HF template renders each tool as-is; the
            # OpenAI-compatible server passes function-wrapped tools, so we
            # match that wrapping. ensure_ascii=False mirrors Jinja tojson.
            tool_lines = "\n".join(
                json.dumps(
                    {"type": "function", "function": tool},
                    ensure_ascii=False,
                )
                for tool in tools
            )
            tools_text = (
                "# Tools\n\n"
                "You have access to the following functions:\n\n"
                f"<tools>\n{tool_lines}\n</tools>\n\n"
                "If you choose to call a function ONLY reply in the following "
                "format with NO suffix:\n\n"
                "<tool_call>\n"
                "<function=example_function_name>\n"
                "<parameter=example_parameter_1>\n"
                "value_1\n"
                "</parameter>\n"
                "<parameter=example_parameter_2>\n"
                "This is the value for the second parameter\n"
                "that can span\n"
                "multiple lines\n"
                "</parameter>\n"
                "</function>\n"
                "</tool_call>\n\n"
                "<IMPORTANT>\n"
                "Reminder:\n"
                "- Function calls MUST follow the specified format: an inner "
                "<function=...></function> block must be nested within "
                "<tool_call></tool_call> XML tags\n"
                "- Required parameters MUST be specified\n"
                "- You may provide optional reasoning for your function call in "
                "natural language BEFORE the function call, but NOT after\n"
                "- If there is no function call available, answer the question "
                "like normal with your current knowledge and do not tell the "
                "user about function calls\n"
                "</IMPORTANT>"
            )

        # The official template emits the tool block FIRST, then appends any
        # user-supplied system prompt after a blank line.
        if system_prompt and tools_text:
            content = tools_text + "\n\n" + system_prompt
        elif tools_text:
            content = tools_text
        else:
            content = system_prompt

        return Message(role="system", content=content)

    # ── Internal helpers ─────────────────────────────────────────────

    def _render_message_text(
        self,
        message: Message,
        *,
        is_reasoning_turn: bool,
        idx: int,
    ) -> tuple[str, str]:
        """Render a message into (header_str, content_str).

        Header: '<|im_start|>role\\n' (weight=0 in training)
        Content: 'body<|im_end|>' (weight=0 or 1 depending on train_on)

        ``is_reasoning_turn`` marks assistant turns that come *after* the
        last user query — the official Qwen3.5/3.6 template wraps those in a
        ``<think>\\n..\\n</think>\\n\\n`` block (empty reasoning included),
        while historical assistant turns render their answer text only.
        """
        maybe_newline = "\n" if idx > 0 else ""
        role = self._get_role(message)
        header = f"{maybe_newline}{_IM_START}{role}\n"

        if message["role"] == "tool":
            content = message["content"]
            text = content if isinstance(content, str) else self._parts_to_text(content)
            return header, f"<tool_response>\n{text}\n</tool_response>{_IM_END}"

        reasoning, text = self._split_reasoning(message)
        emit_think = message["role"] == "assistant" and (
            is_reasoning_turn or not self.strip_thinking_from_history
        )

        body = ""
        if emit_think:
            body += f"<think>\n{reasoning}\n</think>\n\n"
        body += text

        if "tool_calls" in message:
            tc_text = self._format_tool_calls(message["tool_calls"])
            if text.strip():
                body += "\n\n" + tc_text
            elif emit_think:
                # Think block already ended with a blank line.
                body += tc_text
            else:
                body = tc_text

        return header, body + _IM_END

    def _get_role(self, message: Message) -> str:
        """Map message role to Qwen3 role. 'tool' -> 'user'."""
        role = message["role"]
        return "user" if role == "tool" else role

    def _split_reasoning(self, message: Message) -> tuple[str, str]:
        """Split assistant content into (reasoning, answer_text).

        Mirrors the official template's extraction: reasoning is whatever
        sits inside a ``<think>..</think>`` block, answer text is what
        follows it. Returns ``("", full_text)`` when there is no think
        block.
        """
        content = message["content"]
        if isinstance(content, str):
            if "</think>" in content:
                reasoning = (
                    content.split("</think>")[0].rstrip("\n").split("<think>")[-1]
                )
                text = content.split("</think>")[-1].lstrip("\n")
            else:
                reasoning, text = "", content
            return reasoning.strip(), text

        self._reject_non_text_parts(content)
        reasoning_parts = [p["thinking"] for p in content if p["type"] == "thinking"]
        text_parts = [p["text"] for p in content if p["type"] == "text"]
        return "".join(reasoning_parts).strip(), "".join(text_parts)

    def _parts_to_text(self, parts: list[ContentPart]) -> str:
        """Convert content parts to plain text string."""
        self._reject_non_text_parts(parts)
        result: list[str] = []
        for p in parts:
            if p["type"] == "text":
                result.append(p["text"])
            elif p["type"] == "thinking":
                result.append(f"<think>{p['thinking']}</think>")
        return "".join(result)

    def _reject_non_text_parts(self, parts: list[ContentPart]) -> None:
        """Fail loudly on content this text-only renderer cannot express.

        Silently dropping image parts would produce corrupt training data
        or prompts; a mis-selected renderer should raise instead.
        Qwen35VLRenderer overrides the rendering paths with image-aware
        versions and never routes image parts through these helpers.
        """
        for p in parts:
            if p["type"] not in ("text", "thinking"):
                raise ValueError(
                    f"{type(self).__name__} cannot render {p['type']!r} content "
                    "parts; use Qwen35VLRenderer for image input."
                )

    def _format_tool_calls(self, tool_calls: list[ToolCall]) -> str:
        """Format tool calls into qwen3_coder ``<tool_call>`` XML blocks.

        Emits the ``<function=..><parameter=..>`` dialect that Qwen3.5/3.6
        were trained on and that sglang parses via
        ``--tool-call-parser qwen3_coder``. Scalar argument values are
        rendered verbatim; objects/arrays are JSON-serialized.
        """
        blocks: list[str] = []
        for tc in tool_calls:
            name = tc["function"]["name"]
            raw_args = tc["function"].get("arguments") or {}
            if isinstance(raw_args, str):
                try:
                    args = json.loads(raw_args)
                except (json.JSONDecodeError, ValueError):
                    args = {}
            elif isinstance(raw_args, dict):
                args = raw_args
            else:
                args = {}
            if not isinstance(args, dict):
                args = {}

            param_lines: list[str] = []
            for key, value in args.items():
                if isinstance(value, str):
                    val_str = value
                else:
                    val_str = json.dumps(value, ensure_ascii=False)
                param_lines.append(f"<parameter={key}>\n{val_str}\n</parameter>")

            inner = f"<function={name}>\n"
            if param_lines:
                inner += "\n".join(param_lines) + "\n"
            inner += "</function>"
            blocks.append(f"<tool_call>\n{inner}\n</tool_call>")
        return "\n".join(blocks)

    def _apply_reasoning_effort(self, messages: list[Message]) -> list[Message]:
        """Prepend the Qwen3.8 reasoning-effort instruction to the system turn.

        Mirrors the 3.8 template: the instruction goes at the very top of the
        system message — ahead of any ``# Tools`` block, which is why callers
        run this *after* tool injection — and a system message is created when
        the conversation has none. ``medium`` contributes no instruction, and
        the whole control is gated on thinking being enabled.

        A no-op for 3.5/3.6 (``reasoning_effort is None``), which keeps this
        one helper safe to call from every rendering entry point.
        """
        if self.reasoning_effort is None or not self.thinking:
            return messages

        instruction = QWEN38_REASONING_EFFORT_INSTRUCTIONS[self.reasoning_effort]
        system_idx = next(
            (i for i, m in enumerate(messages) if m["role"] == "system"), None
        )

        if not instruction:
            # ``medium``. 3.8 drops an empty system turn entirely instead of
            # emitting the bare ``<|im_start|>system\n<|im_end|>`` that 3.6
            # produces, so there is nothing left to render.
            if system_idx is not None and not self._system_has_content(
                messages[system_idx]
            ):
                return [*messages[:system_idx], *messages[system_idx + 1 :]]
            return messages

        if system_idx is None:
            return [Message(role="system", content=instruction), *messages]

        # Preserve the caller's system content, including the structured
        # (list-of-parts) form — replacing it with a plain string would drop
        # their prompt.
        content = messages[system_idx]["content"]
        if isinstance(content, str):
            stripped = content.strip()
            merged: str | list[ContentPart] = (
                f"{instruction}\n\n{stripped}" if stripped else instruction
            )
        else:
            merged = [
                TextPart(type="text", text=f"{instruction}\n\n"),
                *content,
            ]
        return [
            *messages[:system_idx],
            Message(role="system", content=merged),
            *messages[system_idx + 1 :],
        ]

    @staticmethod
    def _system_has_content(message: Message) -> bool:
        """Whether a system turn renders to anything after trimming."""
        content = message["content"]
        if isinstance(content, str):
            return bool(content.strip())
        return any(part["type"] == "text" and part["text"].strip() for part in content)

    def _extract_system_prompt(self, messages: list[Message]) -> str:
        """Extract existing system prompt text, or empty string."""
        for msg in messages:
            if msg["role"] == "system":
                content = msg["content"]
                return content if isinstance(content, str) else ""
        return ""

    def _replace_or_prepend_system(
        self, messages: list[Message], system_msg: Message
    ) -> list[Message]:
        """Replace existing system message or prepend one."""
        result: list[Message] = []
        replaced = False
        for msg in messages:
            if msg["role"] == "system" and not replaced:
                result.append(system_msg)
                replaced = True
            else:
                result.append(msg)
        if not replaced:
            result.insert(0, system_msg)
        return result


class Qwen35DisableThinkingRenderer(Qwen35Renderer):
    """Renderer for Qwen3.5 / Qwen3.6 with thinking disabled.

    Matches the official template with ``enable_thinking=False``: the
    generation prompt prefills an *empty* reasoning block
    (``<think>\\n\\n</think>\\n\\n``) so the model answers directly. Assistant
    turns with no reasoning content already render that empty block via the
    base class, so no other override is needed.
    """

    def __init__(self, tokenizer: Tokenizer) -> None:
        super().__init__(tokenizer, strip_thinking_from_history=True, thinking=False)
