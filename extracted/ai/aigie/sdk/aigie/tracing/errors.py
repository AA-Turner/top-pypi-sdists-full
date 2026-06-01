"""Framework-agnostic error blob written into span.metadata["error"].

This is the canonical shape every framework adapter must produce via
:meth:`aigie.autonomous.adapters.base.FrameworkAdapter.extract_error`.
The platform clusters and analyzes errors based on this shape, so the
fields and field names are part of the wire contract — do not rename.

The dataclass is frozen on purpose: the enricher hook only writes the
result once into ``span_dict["metadata"]["error"]``, never mutates it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class KytteError:
    """Canonical error payload attached to failed spans."""

    type: str
    """Free-form error type, framework-native is fine. Examples:
    ``"ClientError"``, ``"AgentError"``, ``"not_found"``. Used as a
    coarse first-pass cluster key by the platform."""

    message: str
    """Human-readable error message. Not truncated."""

    severity: str
    """One of ``"low"`` | ``"medium"`` | ``"high"`` | ``"critical"``. String
    not Enum on purpose — keeps the wire shape stable and removes coupling."""

    is_transient: bool
    """True if a retry has a reasonable chance of succeeding (timeouts,
    rate limits, transient network errors)."""

    source: str
    """Where in the framework the error surfaced. One of
    ``"model"`` | ``"tool"`` | ``"node"`` | ``"agent"`` | ``"framework"``."""

    raw: str | None = None
    """Original error text/repr. Optional, useful for debugging."""

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "type": self.type,
            "message": self.message,
            "severity": self.severity,
            "is_transient": self.is_transient,
            "source": self.source,
        }
        if self.raw is not None:
            out["raw"] = self.raw
        return out
