"""Sandbox group (ARM) models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SandboxGroup:
    """A sandbox group resource (ARM)."""
    id: str | None = None
    name: str = ""
    location: str = ""
    tags: dict[str, str] = field(default_factory=dict)
    properties: dict[str, Any] = field(default_factory=dict)
    identity: dict[str, Any] | None = None

    @classmethod
    def _from_dict(cls, d: dict) -> SandboxGroup:
        return cls(
            id=d.get("id"),
            name=d.get("name", ""),
            location=d.get("location", ""),
            tags=d.get("tags", {}),
            properties=d.get("properties", {}),
            identity=d.get("identity"),
        )
