"""Span-complete hook for per-trace ``tool_registry_hash`` metadata."""

from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aigie.client import Aigie


def stamp_tool_hash(aigie: Aigie, payload: dict) -> None:
    """Stamp ``payload`` from the client's ``trace_id -> tool hash`` map."""
    registry = getattr(aigie, "_tool_hash_by_trace", None)
    if not isinstance(registry, dict) or not registry:
        return
    trace_id = payload.get("trace_id")
    tool_hash = registry.get(trace_id) if trace_id else None
    if not isinstance(tool_hash, str) or not tool_hash:
        return
    # Keep active traces fresh in the bounded registry.
    move_to_end = getattr(registry, "move_to_end", None)
    if callable(move_to_end):
        with suppress(KeyError):
            move_to_end(trace_id)
    metadata = payload.get("metadata")
    if not isinstance(metadata, dict):
        metadata = payload["metadata"] = {}
    metadata.setdefault("tool_registry_hash", tool_hash)


class ToolHashStamper:
    """Stamp each span of a bound trace with its tool catalog hash."""

    def __init__(self, aigie: Aigie) -> None:
        self._aigie = aigie

    def __call__(self, payload: dict) -> None:
        stamp_tool_hash(self._aigie, payload)
