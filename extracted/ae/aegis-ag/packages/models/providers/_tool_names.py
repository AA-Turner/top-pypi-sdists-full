"""Provider-specific tool-name normalization helpers."""

from __future__ import annotations

import hashlib
import re

_TOOL_NAME_PATTERN = re.compile(r"^[A-Za-z0-9_-]{1,128}$")


def provider_tool_name(tool_name: str, used_aliases: set[str]) -> str:
    """Return a provider-safe tool alias while preserving reversibility.

    Providers like Anthropic reject tool names containing dots or other
    punctuation. We preserve the original internal tool id separately and expose
    a safe alias on the wire.
    """

    original = tool_name.strip()
    if _TOOL_NAME_PATTERN.match(original) and original not in used_aliases:
        return original

    sanitized = re.sub(r"[^A-Za-z0-9_-]", "_", original)
    sanitized = re.sub(r"_+", "_", sanitized).strip("_") or "tool"
    if _TOOL_NAME_PATTERN.match(sanitized) and sanitized not in used_aliases:
        return sanitized

    digest = hashlib.sha1(original.encode("utf-8", errors="replace")).hexdigest()[:8]
    index = 0
    while True:
        suffix = f"_{digest}" if index == 0 else f"_{digest}_{index + 1}"
        max_base_length = max(1, 128 - len(suffix))
        base = sanitized[:max_base_length].rstrip("_") or "tool"
        candidate = f"{base}{suffix}"
        if candidate not in used_aliases and _TOOL_NAME_PATTERN.match(candidate):
            return candidate
        index += 1
