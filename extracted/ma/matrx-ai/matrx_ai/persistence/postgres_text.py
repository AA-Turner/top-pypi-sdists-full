from __future__ import annotations

from dataclasses import dataclass
from typing import Any

_POSTGRES_TEXT_REPLACEMENT = "\ufffd"


@dataclass(frozen=True, slots=True)
class PostgresTextSanitization:
    value: Any
    replacements: int
    paths: tuple[str, ...]


def sanitize_postgres_text(value: Any, *, path: str = "payload") -> PostgresTextSanitization:
    paths: list[str] = []

    def _sanitize(current: Any, current_path: str) -> tuple[Any, int]:
        if isinstance(current, str):
            count = current.count("\x00")
            if count:
                paths.append(current_path)
                return current.replace("\x00", _POSTGRES_TEXT_REPLACEMENT), count
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
