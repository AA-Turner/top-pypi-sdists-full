"""Secret redaction for tool-call args and free-form result text.

Used before tool-call payloads enter the persisted ``<recent_actions>``
block in continuation messages. The optimizer must never persist API keys,
session tokens, cookies, etc., so we run a structured walker on dict-shaped
args and a regex sweep on free-form strings.
"""

import re
from typing import Any, Dict

_SECRET_KEY_PATTERN = re.compile(
    r"(?i)(authorization|api[_-]?key|apikey|x[_-]?api[_-]?key|access[_-]?token|"
    r"refresh[_-]?token|session[_-]?token|bearer|secret|client[_-]?secret|"
    r"password|passwd|cookie|set[_-]?cookie|credential|private[_-]?key|"
    r"id[_-]?token)"
)
_REDACTED_PLACEHOLDER = "[REDACTED]"

# Inline-text redaction patterns — applied to free-form strings (tool result
# payloads, stringified args). Each substitutes the secret value with
# `[REDACTED]` while keeping the surrounding context intact.
_INLINE_SECRET_PATTERNS = [
    # `Authorization: Bearer xxxxx` / `bearer xxxxx`
    (
        re.compile(r"(?i)(bearer\s+)[A-Za-z0-9._\-+/=]{8,}"),
        r"\1" + _REDACTED_PLACEHOLDER,
    ),
    # `api_key=xxxxx`, `apikey: xxxxx`, `x-api-key=xxxxx` (key=value form)
    (
        re.compile(
            r"(?i)\b(authorization|api[_-]?key|apikey|x[_-]?api[_-]?key|"
            r"access[_-]?token|refresh[_-]?token|session[_-]?token|secret|"
            r"client[_-]?secret|password|passwd|cookie|set[_-]?cookie|"
            r"credential|private[_-]?key|id[_-]?token)"
            r"(\s*[:=]\s*)([^\s,;\"'}]+)"
        ),
        r"\1\2" + _REDACTED_PLACEHOLDER,
    ),
    # JSON-shaped: `"api_key": "xxxxx"` or `"api_key":"xxxxx"`
    (
        re.compile(
            r"(?i)\"(authorization|api[_-]?key|apikey|x[_-]?api[_-]?key|"
            r"access[_-]?token|refresh[_-]?token|session[_-]?token|secret|"
            r"client[_-]?secret|password|passwd|cookie|set[_-]?cookie|"
            r"credential|private[_-]?key|id[_-]?token)\"(\s*:\s*)\"[^\"]*\""
        ),
        r'"\1"\2"' + _REDACTED_PLACEHOLDER + '"',
    ),
]


def _redact_sensitive_payload(obj: Any) -> Any:
    """Walk ``obj`` recursively, masking values whose key looks sensitive.

    Used on structured tool-call args before they are serialized into the
    ``<recent_actions>`` block, so any API key / token / cookie fields are
    not leaked into the persisted continuation message.
    """
    if isinstance(obj, dict):
        out: Dict[Any, Any] = {}
        for k, v in obj.items():
            if isinstance(k, str) and _SECRET_KEY_PATTERN.search(k):
                out[k] = _REDACTED_PLACEHOLDER
            else:
                out[k] = _redact_sensitive_payload(v)
        return out
    if isinstance(obj, list):
        return [_redact_sensitive_payload(v) for v in obj]
    if isinstance(obj, tuple):
        return tuple(_redact_sensitive_payload(v) for v in obj)
    if isinstance(obj, str):
        return _redact_sensitive_text(obj)
    return obj


def _redact_sensitive_text(text: str) -> str:
    """Mask common credential-shaped patterns in free-form strings."""
    if not text:
        return text
    out = text
    for pattern, replacement in _INLINE_SECRET_PATTERNS:
        out = pattern.sub(replacement, out)
    return out
