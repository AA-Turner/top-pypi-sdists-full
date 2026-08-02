"""XML 1.0 safety helpers for the ``<recent_actions>`` block.

Tool results sometimes contain ANSI escapes, null bytes, control chars, or
literal ``"`` that would produce malformed XML when interpolated into the
attribute set or text body of the action entry template. These helpers
strip the illegal characters and escape the rest before rendering.
"""

import re

# XML 1.0 forbids most C0 control characters AND the C1 range (0x7F-0x9F).
# These cannot be expressed via entity references — they must be stripped
# before XML escaping. Tools sometimes emit ANSI escapes (\x1b), null bytes,
# backspaces, etc. inside their result payloads; without stripping these the
# resulting <recent_actions> block becomes a malformed prompt.
_ILLEGAL_XML_CHARS_RE = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]")


def _strip_illegal_xml_chars(text: str) -> str:
    """Remove XML 1.0-illegal control characters, keeping TAB / LF / CR."""
    if not text:
        return ""
    return _ILLEGAL_XML_CHARS_RE.sub("", text)


def _xml_attr_escape(text: str) -> str:
    """Escape value for inclusion inside double-quoted XML attribute.

    ``xml.sax.saxutils.escape`` does NOT escape ``"`` by default — leaving
    attribute values vulnerable to malformed-XML injection when content
    contains a literal double quote (e.g. tool name `tool"name`). Pass the
    extra entity mapping to cover that case.
    """
    from xml.sax.saxutils import escape as _xml_escape

    return _xml_escape(_strip_illegal_xml_chars(text), {'"': "&quot;"})


def _looks_like_error_payload(text: str) -> bool:
    """Heuristic: tool result text indicates failure.

    Catches the activity-log shape ``{"detail":"error(500): ..."}`` and similar.
    Used as a fallback when the agno ``tool_call_error`` attr is missing/None.
    """
    if not text:
        return False
    head = text.lstrip()[:200].lower()
    return (
        head.startswith("error(")
        or '"detail":"error' in head
        or '"detail": "error' in head
        or "internal server error" in head
    )
