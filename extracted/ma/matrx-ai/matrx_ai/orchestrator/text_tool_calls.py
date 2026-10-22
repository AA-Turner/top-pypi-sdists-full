"""A TOOL CALL WRITTEN AS TEXT — found, taken out of the answer, and sent back once.

A model sometimes types its tool call into its reply instead of using the
tool-calling interface: Anthropic's ``<function_calls><invoke name="…">
<parameter name="…">…</parameter></invoke></function_calls>`` markup, the
``<tool_call>{…}</tool_call>`` shape Qwen/Hermes-style models emit, or Llama's
``<function=name>{…}</function>``. The provider reports no tool call, nothing
runs, and the person reads raw markup as if it were the answer (conversation
9b224bf5…, message 388, 2026-10-21: ``</invoke>…<invoke name="task">…`` after a
table, with no ``chat.tool_call`` row).

One detector, one stripper, used by the loop (``orchestrator/executor.py``) at the
one place an assistant turn is received. Markup inside a fenced code block is a
person-facing example, never a call, and is left alone.
"""

from __future__ import annotations

import re

__all__ = [
    "TEXT_TOOL_CALL_CODE",
    "TEXT_TOOL_CALL_NOTICE",
    "TEXT_TOOL_CALL_NOTE",
    "has_text_tool_markup",
    "strip_text_tool_markup",
]

#: Warning code streamed when a turn's text carried a tool call.
TEXT_TOOL_CALL_CODE = "tool_call_written_as_text"

#: The host notice for the ONE re-ask (never appended to the person's message).
TEXT_TOOL_CALL_NOTICE = (
    "SYSTEM NOTICE (not from the user): your last turn wrote a tool call as TEXT "
    "(markup such as <invoke name=...> or <tool_call>). Text is never executed — "
    "nothing ran, and the markup was removed from what the person sees. If you "
    "need the tool, call it through the tool-calling interface now; otherwise "
    "write your answer to the person in plain prose, with no tool markup."
)

#: Appended to the saved answer when the model does it a second time.
TEXT_TOOL_CALL_NOTE = (
    "_(A step the assistant tried to run was written as text, so it did not run.)_"
)

_FENCE = re.compile(r"(```.*?(?:```|\Z)|~~~.*?(?:~~~|\Z))", re.DOTALL)

# Block shapes: an opening tag through its matching close, or — when the model
# stopped mid-call — through the end of the text.
_BLOCKS = (
    re.compile(r"<function_calls\b[^>]*>.*?(?:</function_calls>|\Z)", re.DOTALL),
    re.compile(r"<invoke\s+name\s*=.*?(?:</invoke>|\Z)", re.DOTALL),
    re.compile(r"<parameter\s+name\s*=.*?(?:</parameter>|\Z)", re.DOTALL),
    re.compile(r"<tool_call\b[^>]*>.*?(?:</tool_call>|\Z)", re.DOTALL),
    re.compile(r"<function=[\w.:-]+>.*?(?:</function>|\Z)", re.DOTALL),
)
# Stray closers left behind by a call the model half-wrote.
_STRAYS = re.compile(r"</(?:function_calls|invoke|parameter|tool_call)>")

_DETECT = re.compile(
    r"<function_calls\b|<invoke\s+name\s*=|<parameter\s+name\s*=|</invoke>|"
    r"</function_calls>|<tool_call\b|<function=[\w.:-]+>"
)


def _split_fences(text: str) -> list[tuple[bool, str]]:
    """``(is_code, piece)`` segments; fenced code is never inspected or changed."""
    parts: list[tuple[bool, str]] = []
    last = 0
    for match in _FENCE.finditer(text):
        if match.start() > last:
            parts.append((False, text[last : match.start()]))
        parts.append((True, match.group(0)))
        last = match.end()
    if last < len(text):
        parts.append((False, text[last:]))
    return parts


def has_text_tool_markup(text: str | None) -> bool:
    """True when ``text`` carries tool-call markup outside fenced code."""
    if not text or "<" not in text:
        return False
    return any(not code and _DETECT.search(piece) for code, piece in _split_fences(text))


def strip_text_tool_markup(text: str) -> str:
    """``text`` with every tool-call block and stray closer removed (code fences kept)."""
    if not has_text_tool_markup(text):
        return text
    out: list[str] = []
    for code, piece in _split_fences(text):
        if not code:
            for pattern in _BLOCKS:
                piece = pattern.sub("", piece)
            piece = _STRAYS.sub("", piece)
        out.append(piece)
    cleaned = "".join(out)
    cleaned = re.sub(r"[ \t]+\n", "\n", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()
