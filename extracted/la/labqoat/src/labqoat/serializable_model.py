"""Structural type shared by generated response models."""

from __future__ import annotations

from typing import Protocol

from labqoat.json_document import JsonDocument


class SerializableModel(Protocol):
    """Generated model capable of returning its JSON representation."""

    def to_dict(self) -> JsonDocument:
        """Return the validated JSON representation."""
        ...
