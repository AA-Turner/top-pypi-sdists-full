"""Core discovery types: workspaces, resources, and result envelope."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

from spec_kitty_tracker.types import JSONValue

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class DiscoveredWorkspace:
    """A workspace (org, site, group) surfaced by a provider discoverer."""

    id: str
    name: str
    display: str
    kind: str
    provider: str
    provider_context: dict[str, JSONValue] | None = None


@dataclass(frozen=True, slots=True)
class DiscoveredResource:
    """A mappable resource within a workspace boundary."""

    provider: str
    parent_workspace_id: str
    resource_type: str
    stable_ref: str
    display_name: str
    connector_params: dict[str, JSONValue]
    routing_metadata: dict[str, JSONValue]


@dataclass(frozen=True, slots=True)
class DiscoveryResult(Generic[T]):
    """Envelope for a discovery response with truncation flag."""

    items: list[T]
    truncated: bool
