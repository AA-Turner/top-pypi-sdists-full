"""Ripple-65B renderer: the checkpoint's ChatML template with JSON tool calls.

The template frames turns with ``<|im_start|>``/``<|im_end|>``, writes
reasoning as ``<think>\\n{reasoning}\\n</think>\\n`` before the answer, and
writes each call as ``\\n<tool_call>\\n{"name": ..., "arguments": {...}}\\n
</tool_call>`` after it. Rendering goes through the checkpoint's own template,
so prompts and training datums are the tokens the model was post-trained on.
"""

from __future__ import annotations

import json

from river_client.renderers.base import (
    ContentPart,
    ParsedResponse,
    SamplePrompt,
    ThinkingPart,
    ToolCall,
    ToolCallFunction,
    ToolSpec,
    UnparsedToolCall,
    append_visible_text,
    parsed_text_content,
    rejected_call_text,
)
from river_client.renderers.checkpoint_text import CheckpointTextRenderer
from river_client.renderers.tool_arguments import (
    find_outside_json_strings,
    standard_json,
)

_THINK_OPEN = "<think>"
_THINK_CLOSE = "</think>"
_TOOL_CALL_OPEN = "<tool_call>"
_TOOL_CALL_CLOSE = "</tool_call>"


def _strip_one(text: str, *, leading: bool, trailing: bool) -> str:
    """Drop one framing newline the template writes around a block."""
    if leading and text.startswith("\n"):
        text = text[1:]
    if trailing and text.endswith("\n"):
        text = text[:-1]
    return text


def _parse_ripple_call(body: str, raw_text: str) -> ToolCall | UnparsedToolCall:
    """One closed block's JSON: exactly a string ``name`` and object ``arguments``.

    Any other member would be dropped from the call, so it rejects the block
    instead (R1); so does anything that is not one standard JSON object (R5).
    """
    try:
        call = standard_json(body)
    except ValueError as exc:
        return UnparsedToolCall(
            raw_text=raw_text, error=f"Ripple tool call is not valid JSON: {exc}"
        )
    if not isinstance(call, dict) or set(call) != {"name", "arguments"}:
        return UnparsedToolCall(
            raw_text=raw_text,
            error='Ripple tool call must be {"name": ..., "arguments": {...}}',
        )
    name, arguments = call["name"], call["arguments"]
    if not isinstance(name, str) or not name:
        return UnparsedToolCall(raw_text=raw_text, error="Missing function name")
    if not isinstance(arguments, dict):
        return UnparsedToolCall(
            raw_text=raw_text, error="Ripple tool call arguments must be a JSON object"
        )
    return ToolCall(
        type="function",
        id=None,
        function=ToolCallFunction(
            name=name, arguments=json.dumps(arguments, ensure_ascii=False)
        ),
    )


def parse_ripple_content_blocks(
    content: str,
) -> tuple[list[ContentPart], list[ToolCall | UnparsedToolCall]] | None:
    """Split Ripple output into reasoning, visible text and tool-call blocks.

    Returns None when the output holds no block. A closed ``<think>`` block is
    reasoning whatever it holds; an unclosed one (a truncated generation) ends
    where the next call opens. A call's JSON runs to the first ``</tool_call>``
    outside a JSON string; a block the output ends inside, or that another
    ``<tool_call>`` interrupts, is rejected whole. The newlines the template
    writes around reasoning and before each call are framing, not text.
    """
    if _THINK_OPEN not in content and _TOOL_CALL_OPEN not in content:
        return None

    parts: list[ContentPart] = []
    calls: list[ToolCall | UnparsedToolCall] = []
    pos = 0
    while True:
        think_at = content.find(_THINK_OPEN, pos)
        call_at = content.find(_TOOL_CALL_OPEN, pos)
        if think_at < 0 and call_at < 0:
            break
        if call_at < 0 or 0 <= think_at < call_at:
            append_visible_text(parts, content[pos:think_at])
            body = think_at + len(_THINK_OPEN)
            close = content.find(_THINK_CLOSE, body)
            if close >= 0:
                thinking = content[body:close]
                pos = close + len(_THINK_CLOSE)
                if content.startswith("\n", pos):
                    pos += 1
            else:
                next_call = content.find(_TOOL_CALL_OPEN, body)
                pos = len(content) if next_call < 0 else next_call
                thinking = content[body:pos]
            thinking = _strip_one(thinking, leading=True, trailing=True)
            if thinking:
                parts.append(ThinkingPart(type="thinking", thinking=thinking))
            continue
        append_visible_text(
            parts, _strip_one(content[pos:call_at], leading=False, trailing=True)
        )
        body = call_at + len(_TOOL_CALL_OPEN)
        end, marker = find_outside_json_strings(
            content, (_TOOL_CALL_CLOSE, _TOOL_CALL_OPEN), body
        )
        if marker != _TOOL_CALL_CLOSE:
            calls.append(
                UnparsedToolCall(
                    raw_text=content[call_at:end], error="Unclosed Ripple tool call"
                )
            )
            pos = end
            continue
        pos = end + len(_TOOL_CALL_CLOSE)
        calls.append(_parse_ripple_call(content[body:end], content[call_at:pos]))
    append_visible_text(parts, content[pos:])
    return parts, calls


def _find_or_end(text: str, marker: str, start: int) -> int:
    at = text.find(marker, start)
    return len(text) if at < 0 else at


def _strip_reasoning(content: str) -> str:
    """``content`` without its reasoning blocks, found as the parser finds them.

    Calls are copied whole, so a ``<think>`` inside call JSON stays. Text a
    dropped block separated stays separated by a newline, as parsing keeps it,
    so it cannot join into markup.
    """
    out: list[str] = []
    has_text = separate = False
    pos = 0
    while True:
        think_at = _find_or_end(content, _THINK_OPEN, pos)
        call_at = _find_or_end(content, _TOOL_CALL_OPEN, pos)
        if text := content[pos : min(think_at, call_at)]:
            out.append("\n" + text if separate else text)
            has_text, separate = True, False
        if call_at < think_at:
            end, marker = find_outside_json_strings(
                content,
                (_TOOL_CALL_CLOSE, _TOOL_CALL_OPEN),
                call_at + len(_TOOL_CALL_OPEN),
            )
            pos = end + len(_TOOL_CALL_CLOSE) if marker == _TOOL_CALL_CLOSE else end
            out.append(content[call_at:pos])
            separate = False
        elif think_at < len(content):
            body = think_at + len(_THINK_OPEN)
            close = content.find(_THINK_CLOSE, body)
            if close >= 0:
                pos = close + len(_THINK_CLOSE)
                if content.startswith("\n", pos):
                    pos += 1
            else:
                pos = _find_or_end(content, _TOOL_CALL_OPEN, body)
            separate = separate or has_text
        else:
            return "".join(out)


def _inline_parts(parts: list[ContentPart], *, strip: bool) -> str:
    """Text and reasoning parts in order, each block as the template writes it.

    Parsing separates text that a block split with a newline; a written
    block separates it again, so that newline is dropped.
    """
    out: list[str] = []
    has_text = after_block = False
    for part in parts:
        if part["type"] == "text":
            text = part["text"]
            if has_text and after_block and text.startswith("\n"):
                text = text[1:]
            out.append(text)
            has_text, after_block = has_text or bool(text), False
        elif part["thinking"] and not strip:
            out.append(f"{_THINK_OPEN}\n{part['thinking']}\n{_THINK_CLOSE}\n")
            after_block = True
    return "".join(out)


class RippleRenderer(CheckpointTextRenderer):
    """Text-only renderer for ricursiveAI/Ripple-65B through its own template.

    The template has no thinking switch: the generation prompt is a bare
    assistant header and the model opens its own ``<think>`` block. It writes
    a non-empty ``reasoning_content`` as one block before the content, and
    content verbatim, so reasoning parts are written into the content in
    their order, each in the block the template would write: joining them
    into one field could turn their text into markup, or move reasoning
    after text before it. ``strip_thinking_from_history`` drops reasoning
    from turns before the last user turn, in every form; the template's own
    ``clear_thinking`` would also drop it from the turn being trained or
    continued, so it is never passed.
    """

    empty_reasoning_field = True

    def __init__(self, tokenizer, *, strip_thinking_from_history=False):
        super().__init__(
            tokenizer,
            thinking=True,
            strip_thinking_from_history=strip_thinking_from_history,
        )

    def _message(self, message, *, history):
        strip = history and self.strip_thinking_from_history
        content = message.get("content")
        if message.get("role") == "assistant" and isinstance(content, str):
            if strip:
                message = {**message, "content": _strip_reasoning(content)}
        elif (
            message.get("role") == "assistant"
            and content
            and not isinstance(message.get("reasoning_content"), str)
            and all(part["type"] in ("text", "thinking") for part in content)
        ):
            message = {**message, "content": _inline_parts(content, strip=strip)}
        rejected = rejected_call_text(message) if message.get("tool_calls") else ""
        if rejected:
            message = {k: v for k, v in message.items() if k != "unparsed_tool_calls"}
        m = super()._message(message, history=history)
        if strip:
            m.pop("reasoning_content", None)
        if rejected:
            # A rejected block may hold an open JSON string, which runs to the
            # end of the output, so it must follow the calls as the model wrote
            # them (R1). The template writes calls after the content, so they
            # are written here in its exact form, with the blocks after them.
            calls = "".join(
                "\n<tool_call>\n"
                + json.dumps(
                    {
                        "name": call["function"]["name"],
                        "arguments": call["function"]["arguments"],
                    },
                    ensure_ascii=False,
                )
                + "\n</tool_call>"
                for call in m.pop("tool_calls")
            )
            if not (m["content"] or m.get("reasoning_content")):
                # The template opens a bare call turn without its newline.
                calls = calls[1:]
            m["content"] += calls + rejected
        return m

    def _template_kwargs(self):
        return {}

    def get_stop_strings(self):
        # Both of the checkpoint's EOS ids end a generation.
        return ["<|im_end|>", "<|endoftext|>"]

    def build_continuation_prompt(self, messages, *, last_stop):
        prefix = "" if last_stop in self.get_stop_strings() else "<|im_end|>"
        return SamplePrompt(prefix + "\n" + self._observation_suffix(messages), [], [])

    def parse_response(
        self, text: str, *, tools: list[ToolSpec] | None = None
    ) -> ParsedResponse:
        # Calls carry their own JSON types, so ``tools`` is not needed.
        stopped = False
        for stop in self.get_stop_strings():
            if text.endswith(stop):
                text, stopped = text[: -len(stop)], True
                break
        parsed = parse_ripple_content_blocks(text)
        if parsed is None:
            return ParsedResponse(
                {"role": "assistant", "content": parsed_text_content(text)}, stopped
            )
        parts, calls = parsed
        message = {"role": "assistant", "content": parts}
        valid = [c for c in calls if "function" in c]
        invalid = [c for c in calls if "error" in c]
        if valid:
            message["tool_calls"] = valid
        if invalid:
            message["unparsed_tool_calls"] = invalid
        return ParsedResponse(message, stopped)
