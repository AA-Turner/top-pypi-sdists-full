"""``ToolInvocationResult`` repr-string unwrapping.

When agno serializes a tool message, the content may be either a structured
dict, a JSON string, or — when wrapped by xpander's ``ToolInvocationResult``
pydantic model — the model's ``repr()`` form ``tool_id=... result=...``.
Layer 1 needs to extract just the ``result`` payload so the workspace blob
and inline preview carry the actual tool output, not the wrapper metadata.
"""

import ast
import json
import re
from typing import Any, Optional

_TOOL_INVOCATION_REPR_PREFIX = "tool_id="


def _extract_balanced_value(content: str, start: int) -> Optional[str]:
    """Extract a Python-literal value starting at ``content[start]``,
    balancing braces/brackets and tracking quoted strings.

    Supports dicts (``{...}``), lists (``[...]``), and quoted strings.
    Returns the substring for the value, or ``None`` if it cannot be parsed.
    """
    if start >= len(content):
        return None
    ch = content[start]
    if ch in ("'", '"'):
        end = start + 1
        escape = False
        while end < len(content):
            c = content[end]
            if escape:
                escape = False
            elif c == "\\":
                escape = True
            elif c == ch:
                return content[start : end + 1]
            end += 1
        return None
    if ch in ("{", "["):
        open_char = ch
        close_char = "}" if ch == "{" else "]"
        depth = 0
        in_string = False
        string_char = None
        escape = False
        end = start
        while end < len(content):
            c = content[end]
            if escape:
                escape = False
                end += 1
                continue
            if c == "\\":
                escape = True
                end += 1
                continue
            if in_string:
                if c == string_char:
                    in_string = False
            elif c in ("'", '"'):
                in_string = True
                string_char = c
            elif c == open_char:
                depth += 1
            elif c == close_char:
                depth -= 1
                if depth == 0:
                    return content[start : end + 1]
            end += 1
        return None
    # Bare value: read until next `  <field>=` marker or end of string.
    tail = content[start:]
    m = re.search(r"\s\w+=", tail)
    return (tail[: m.start()] if m else tail).strip()


def _extract_repr_field(content: str, field_name: str) -> Any:
    """Pull a single field value out of a pydantic ``repr()`` string.

    Tries JSON first, then ``ast.literal_eval``. Returns the raw value
    string on parse failure, or ``None`` when the field isn't present.
    """
    if not isinstance(content, str):
        return None
    marker = f" {field_name}="
    if content.startswith(f"{field_name}="):
        start = len(field_name) + 1
    else:
        idx = content.find(marker)
        if idx == -1:
            return None
        start = idx + len(marker)
    raw = _extract_balanced_value(content, start)
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except Exception:
        pass
    try:
        return ast.literal_eval(raw)
    except Exception:
        return raw


def _head_tail_preview(text: str, head: int, tail: int) -> str:
    """Return ``text`` if short, else ``start … [marker] … end``.

    The middle is replaced with an explicit ``[…N chars summarized…]`` marker
    so callers (and downstream LLMs) can see content was elided, not truncated.
    """
    if not text:
        return ""
    if len(text) <= head + tail:
        return text
    elided = len(text) - head - tail
    return f"{text[:head]}\n[…{elided} chars summarized…]\n{text[-tail:]}"


def unwrap_tool_result_content(content: Any) -> str:
    """Return a clean serialized form of a tool message content.

    If *content* looks like the ``repr()`` of a ``ToolInvocationResult``
    (starts with ``tool_id=``), extract just the ``result`` field and
    JSON-serialize it. This strips the pydantic wrapper (tool_id, task_id,
    payload, status_code, is_success, ...) so the workspace and preview carry
    only the actual tool output.

    For any other content type the value is returned as its string form.
    """
    if content is None:
        return ""
    if not isinstance(content, str):
        # Pydantic models, dicts, etc. — prefer a JSON serialization when
        # possible; fall back to ``str()``.
        try:
            return json.dumps(content, default=str, ensure_ascii=False)
        except Exception:
            return str(content)
    stripped = content.lstrip()
    if not stripped.startswith(_TOOL_INVOCATION_REPR_PREFIX):
        return content
    result = _extract_repr_field(content, "result")
    if result is None:
        return content
    if isinstance(result, str):
        return result
    try:
        return json.dumps(result, default=str, ensure_ascii=False)
    except Exception:
        return str(result)
