"""Fill ``{{name}}`` references in a recorded read with this run's values.

A recorded read's code can hold ``'{{global.project_name}}'`` inside a JS string
literal where it compares against that variable. ``fill_code`` puts the value
in, escaped for any JS string literal; ``fill_text`` does the same for plain
text (the query, condition and expected value sent to heal). Only names in
``variables`` are filled; every other ``{{...}}`` is left as is.
"""
from __future__ import annotations

import re

_TOKEN_RE = re.compile(r"\{\{\s*([^{}]+?)\s*\}\}")
_JS_ESCAPES = {
    "\\": "\\\\", "'": "\\'", '"': '\\"', "`": "\\`", "$": "\\$",
    "\n": "\\n", "\r": "\\r", " ": "\\u2028", " ": "\\u2029",
}


def js_string_escape(value: str) -> str:
    """*value* escaped to sit inside a single-, double- or back-quoted JS string."""
    out = []
    for ch in value:
        if ch in _JS_ESCAPES:
            out.append(_JS_ESCAPES[ch])
        elif ord(ch) < 0x20:
            out.append(f"\\u{ord(ch):04x}")
        else:
            out.append(ch)
    return "".join(out)


def _fill(text, variables, render):
    if not text or not variables:
        return text

    def sub(m: re.Match[str]) -> str:
        name = m.group(1).strip()
        if name not in variables:
            return m.group(0)
        return render("" if variables[name] is None else str(variables[name]))

    return _TOKEN_RE.sub(sub, text)


def fill_code(code: str | None, variables: dict | None) -> str | None:
    """*code* with each known ``{{name}}`` replaced by its JS-escaped value."""
    return _fill(code, variables, js_string_escape)


def fill_text(text: str | None, variables: dict | None) -> str | None:
    """*text* with each known ``{{name}}`` replaced by its value."""
    return _fill(text, variables, lambda v: v)
