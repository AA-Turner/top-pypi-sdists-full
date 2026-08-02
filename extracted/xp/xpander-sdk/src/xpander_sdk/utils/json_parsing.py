import ast
import json
from typing import Any, Optional


def parse_structured_string(value: str) -> Optional[Any]:
    """Parse a string that plausibly encodes a dict/list, returning None on failure.

    Four tiers, mirroring the leniency LLM tool-call payloads need in practice:
    strict JSON, then ``strict=False`` (literal newlines/tabs in string values),
    then a Python literal (single quotes), then unescaped-quote repair (heredoc
    content with interior double quotes). The repair treats a quote followed by
    ``,:}]`` as a real terminator, so it recovers single-quoted tokens like
    ``print("x")`` but not multi-arg ``print("a", "b")`` (those still return
    None - same loud failure as before). Plain text never parses; returns None.
    """
    stripped = value.strip()
    if not (stripped.startswith(("{", "[")) and stripped.endswith(("}", "]"))):
        return None
    try:
        parsed = json.loads(stripped)
        if isinstance(parsed, (dict, list)):
            return parsed
    except Exception:
        pass
    try:
        parsed = json.loads(stripped, strict=False)
        if isinstance(parsed, (dict, list)):
            return parsed
    except Exception:
        pass
    try:
        parsed = ast.literal_eval(stripped)
        if isinstance(parsed, (dict, list, tuple)):
            return list(parsed) if isinstance(parsed, tuple) else parsed
    except Exception:
        pass
    try:
        parsed = json.loads(_repair_unescaped_quotes(stripped), strict=False)
        if isinstance(parsed, (dict, list)):
            return parsed
    except Exception:
        pass
    return None


def _repair_unescaped_quotes(text: str) -> str:
    """Escape interior double quotes a model forgot to escape inside JSON string values.

    Bash heredocs / quoted prose inside a stringified payload defeat every strict
    parse tier. A quote inside a string counts as the real terminator only when
    the next non-whitespace char is valid JSON structure (,:}]) or end-of-input.
    """
    out: list[str] = []
    in_str = escape = False
    n = len(text)
    for i, ch in enumerate(text):
        if not in_str:
            if ch == '"':
                in_str = True
            out.append(ch)
            continue
        if escape:
            out.append(ch)
            escape = False
            continue
        if ch == "\\":
            out.append(ch)
            escape = True
            continue
        if ch == '"':
            j = i + 1
            while j < n and text[j] in " \t\r\n":
                j += 1
            if j >= n or text[j] in ',:}]':
                in_str = False
                out.append(ch)
            else:
                out.append('\\"')
            continue
        out.append(ch)
    return "".join(out)
