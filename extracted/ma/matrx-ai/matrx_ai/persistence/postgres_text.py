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


@dataclass(frozen=True, slots=True)
class PostgresTextSanitization:
    value: Any
    replacements: int
    paths: tuple[str, ...]


def sanitize_postgres_text(value: Any, *, path: str = "payload") -> PostgresTextSanitization:
    paths: list[str] = []

    def _sanitize(current: Any, current_path: str) -> tuple[Any, int]:
        if isinstance(current, str):
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
