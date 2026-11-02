"""Canonical value objects (Standardized Node Result System, Layer 3 —
graph-generic tier).

Concepts that recur INSIDE payloads across many nodes have exactly one
canonical model, imported — never re-declared. Core fields are frozen;
extension is by subclass, never loose keys. Evolution is additive only.

Domain-specific value objects live in their owning package — AI usage/cost is
matrx-ai's (``matrx_ai.graph_nodes.shared.AiUsage`` is the canonical workflow
usage shape; matrx-graph deliberately stays schema-blind to it and duck-reads
the ``usage`` dict in ``node_cost_from_output``). This module holds only the
concepts EVERY node source shares.
"""

from __future__ import annotations

import time

from pydantic import BaseModel, ConfigDict


class Timing(BaseModel):
    """Canonical wall-clock timing. ONE field name — ``elapsed_ms`` — ends
    the elapsed_ms / duration_ms / total_api_duration_ms divergence.

    Construct via ``Timing.since(started)`` where ``started`` is a
    ``time.monotonic()`` stamp taken before the work.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    elapsed_ms: int

    @classmethod
    def since(cls, monotonic_start: float) -> Timing:
        return cls(elapsed_ms=int((time.monotonic() - monotonic_start) * 1000))
