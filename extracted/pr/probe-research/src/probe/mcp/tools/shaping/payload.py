"""to_dict(): a payload struct (a frozen dataclass naming a fixed response shape) as its wire dict."""

from __future__ import annotations

from dataclasses import fields, is_dataclass
from typing import Any


def to_dict(payload: Any) -> dict[str, Any]:
    """One key per field, in declaration order (the wire order). A None value stays as a null key:
    absence means something else on this wire. Nested structs, and lists of them, pack too."""
    return {item.name: _to_wire(getattr(payload, item.name)) for item in fields(payload)}


def _to_wire(value: Any) -> Any:
    if is_dataclass(value) and not isinstance(value, type):
        return to_dict(value)
    if isinstance(value, list):
        return [_to_wire(item) for item in value]
    return value
