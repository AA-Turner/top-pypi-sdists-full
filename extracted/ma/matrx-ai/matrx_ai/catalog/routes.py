"""Canonical routing metadata for catalog APIs outside turn-based dispatch.

Most ``ai.api.translator_key`` values name a ``UnifiedAIClient`` provider
attribute directly.  These routes are deliberately different: they resolve
through the shared catalog, but execute through a specialized runtime rather
than ``UnifiedAIClient.execute()``.
"""

from __future__ import annotations

NON_TURN_CLIENT_ATTRS: dict[str, str] = {
    "extraction_gliner": "extraction",
    "openai_embeddings": "embedding",
    "openai_realtime": "realtime",
    "xai_realtime": "realtime",
    "google_live": "realtime",
    "google_music_realtime": "music_realtime",
    "google_embeddings": "embedding",
    "groq_stt": "stt",
}

SPECIAL_WIRE_FORMATS: frozenset[str] = frozenset(NON_TURN_CLIENT_ATTRS)


def client_attr_for_wire_format(wire_format: str) -> str:
    """Return the execution channel for a catalog wire-format token."""
    return NON_TURN_CLIENT_ATTRS.get(wire_format, wire_format)


__all__ = [
    "NON_TURN_CLIENT_ATTRS",
    "SPECIAL_WIRE_FORMATS",
    "client_attr_for_wire_format",
]
