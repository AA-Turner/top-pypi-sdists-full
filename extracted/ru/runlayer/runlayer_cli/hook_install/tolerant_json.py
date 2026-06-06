"""Stdlib-only JSONC fallback for hook-config files (no ``json5`` in the bundle)."""

from __future__ import annotations

import json
import re

_TRAILING_COMMA_RE = re.compile(r",(\s*[}\]])")


def _strip_line_comments(text: str) -> str:
    """Strip ``//`` line comments while preserving ``//`` inside JSON strings.

    A regex with a lookbehind can't reliably tell whether a ``//`` sits inside
    a string value (e.g. ``"file:///foo"`` or ``"\\\\server\\share"``), so we
    walk the text and toggle an ``in_string`` flag on unescaped ``"``.
    """
    out: list[str] = []
    in_string = False
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if in_string:
            if ch == "\\" and i + 1 < n:
                out.append(ch)
                out.append(text[i + 1])
                i += 2
                continue
            if ch == '"':
                in_string = False
            out.append(ch)
            i += 1
            continue
        if ch == '"':
            in_string = True
            out.append(ch)
            i += 1
            continue
        if ch == "/" and i + 1 < n and text[i + 1] == "/":
            nl = text.find("\n", i + 2)
            i = n if nl == -1 else nl
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def loads(text: str) -> object:
    """Parse JSON text, tolerating ``//`` line comments + trailing commas."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        cleaned = _strip_line_comments(text)
        cleaned = _TRAILING_COMMA_RE.sub(r"\1", cleaned)
        return json.loads(cleaned)


def read_dict(text: str) -> dict:
    """Like ``loads`` but coerces ``None`` / empty / non-dict inputs to ``{}``."""
    if not text or not text.strip():
        return {}
    parsed = loads(text)
    if isinstance(parsed, dict):
        return parsed
    return {}
