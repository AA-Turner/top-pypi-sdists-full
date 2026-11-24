from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

_POSTGRES_TEXT_REPLACEMENT = "\ufffd"

# Two things a Python str can hold that PostgreSQL text/json/jsonb refuse:
# the NUL byte, and a LONE surrogate half (a JS string cut mid-emoji, or a
# scraped page's broken escape, decodes to one; json.dumps then writes
# "\udc80" and Postgres answers 22P02 "Unicode low surrogate must follow a
# high surrogate"). A properly paired high+low is legal and left alone.
_POSTGRES_ILLEGAL_TEXT = re.compile(
    "\x00|[\ud800-\udbff](?![\udc00-\udfff])|(?<![\ud800-\udbff])[\udc00-\udfff]"
)


#: A lone surrogate half alone (no NUL): not valid Unicode, so it cannot be encoded as UTF-8 and every provider SDK
#: refuses a request body carrying one. The send boundary replaces it on the wire (config/send_boundary.py).
LONE_SURROGATE = re.compile("[\ud800-\udbff](?![\udc00-\udfff])|(?<![\ud800-\udbff])[\udc00-\udfff]")

#: ANY surrogate half, paired or not. A single character class is scanned ~20x faster than the alternation with
#: lookarounds above (5M chars: 14ms against 270ms), so it is the gate: the lookaround pattern runs only on a string
#: that holds a surrogate at all. Before this gate the send boundary ran the slow pattern over every wire field on
#: the event loop and froze the whole server for 1.3-4.6s on long conversations (event_loop_stall
#: aidream-api:004bd02ae7555485, 2026-11-11).
_ANY_SURROGATE = re.compile("[\ud800-\udfff]")


def may_hold_illegal_text(value: str) -> bool:
    """Whether ``value`` can hold a NUL or a surrogate half. ``str.isascii`` is O(1) in CPython (a flag on the
    object), so the common case - ASCII text, base64, JSON - costs nothing."""
    if value.isascii():
        return "\x00" in value
    return "\x00" in value or _ANY_SURROGATE.search(value) is not None


def _holds_surrogate(value: str) -> bool:
    return not value.isascii() and _ANY_SURROGATE.search(value) is not None


def replace_lone_surrogates(value: Any) -> tuple[Any, int]:
    """``value`` with every lone surrogate half (in any nested str, dict key or item, list or tuple) replaced by
    U+FFFD, and how many were replaced. Unchanged containers are returned as they are."""
    if isinstance(value, str):
        if not _holds_surrogate(value):
            return value, 0
        return LONE_SURROGATE.subn(_POSTGRES_TEXT_REPLACEMENT, value)
    if isinstance(value, dict):
        out: dict[Any, Any] = {}
        total = 0
        for key, item in value.items():
            clean_key, a = replace_lone_surrogates(key)
            clean_item, b = replace_lone_surrogates(item)
            out[clean_key] = clean_item
            total += a + b
        return (out if total else value), total
    if isinstance(value, (list, tuple)):
        items = [replace_lone_surrogates(item) for item in value]
        total = sum(n for _, n in items)
        if not total:
            return value, 0
        cleaned = [v for v, _ in items]
        return (tuple(cleaned) if isinstance(value, tuple) else cleaned), total
    return value, 0


@dataclass(frozen=True, slots=True)
class PostgresTextSanitization:
    value: Any
    replacements: int
    paths: tuple[str, ...]


def sanitize_postgres_text(value: Any, *, path: str = "payload") -> PostgresTextSanitization:
    paths: list[str] = []

    def _sanitize(current: Any, current_path: str) -> tuple[Any, int]:
        if isinstance(current, str):
            if not may_hold_illegal_text(current):
                return current, 0
            clean, count = _POSTGRES_ILLEGAL_TEXT.subn(_POSTGRES_TEXT_REPLACEMENT, current)
            if count:
                paths.append(current_path)
                return clean, count
            return current, 0
        if isinstance(current, dict):
            changed = False
            replacements = 0
            sanitized: dict[Any, Any] = {}
            for key, item in current.items():
                clean_key, key_count = _sanitize(key, f"{current_path}.<key>")
                clean_item, item_count = _sanitize(item, f"{current_path}.{clean_key}")
                if clean_key in sanitized:
                    raise ValueError(
                        f"PostgreSQL text sanitization would collide at {current_path}"
                    )
                sanitized[clean_key] = clean_item
                replacements += key_count + item_count
                changed = changed or key_count > 0 or item_count > 0
            return (sanitized if changed else current), replacements
        if isinstance(current, list):
            items: list[Any] = []
            replacements = 0
            changed = False
            for index, item in enumerate(current):
                clean_item, item_count = _sanitize(item, f"{current_path}[{index}]")
                items.append(clean_item)
                replacements += item_count
                changed = changed or item_count > 0
            return (items if changed else current), replacements
        if isinstance(current, tuple):
            items: list[Any] = []
            replacements = 0
            changed = False
            for index, item in enumerate(current):
                clean_item, item_count = _sanitize(item, f"{current_path}[{index}]")
                items.append(clean_item)
                replacements += item_count
                changed = changed or item_count > 0
            return (tuple(items) if changed else current), replacements
        return current, 0

    sanitized, replacements = _sanitize(value, path)
    return PostgresTextSanitization(
        value=sanitized,
        replacements=replacements,
        paths=tuple(dict.fromkeys(paths))[:20],
    )
