"""Immutable declaration for one JSON mutation command."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat.json_document import JsonValue


@dataclass(frozen=True)
class MutationSpec:
    """Describe endpoint routing and CLI-to-JSON field conversion."""

    path: str
    query_names: tuple[str, ...] = ()
    query_renames: Mapping[str, str] | None = None
    fixed_query: Mapping[str, JsonValue] | None = None
    renames: Mapping[str, str] | None = None
    fixed: Mapping[str, JsonValue] | None = None
    json_names: tuple[str, ...] = ()
    exclusive: tuple[str, ...] = ()
    exclusive_required: bool = False
