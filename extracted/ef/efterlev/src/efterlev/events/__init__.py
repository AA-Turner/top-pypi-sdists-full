"""Efterlev Studio event spine — a typed, renderer-agnostic event stream.

The single source of truth for what's happening during a run. Producers
(scan + the gap agent) emit typed events; renderers subscribe — the
browser Studio (live via SSE) and a JSONL recorder (`efterlev.events.recorder`,
the transport `studio --live` tails).

The spine is deliberately additive and decoupled: producers call
`emit(event)`, which is a no-op when no bus is active (the normal CLI
path, so behavior is unchanged), and publishes to the active bus when
Studio or a test has one bound — mirroring `active_store` /
`active_boundary_config`. See DECISIONS 2026-05-22 (Efterlev Studio,
spine-first) and design.local.md "VISION — Efterlev Studio".
"""

from __future__ import annotations

from efterlev.events.bus import (
    EventBus,
    active_event_bus,
    emit,
    get_active_bus,
    set_active_bus,
)
from efterlev.events.schema import (
    AgentFinished,
    AgentStarted,
    BatchStarted,
    ClassificationStatus,
    EvidenceFound,
    KsiClassified,
    KsiEvidenced,
    ScanFinished,
    ScanStarted,
    StudioEvent,
)

__all__ = [
    "AgentFinished",
    "AgentStarted",
    "BatchStarted",
    "ClassificationStatus",
    "EventBus",
    "EvidenceFound",
    "KsiClassified",
    "KsiEvidenced",
    "ScanFinished",
    "ScanStarted",
    "StudioEvent",
    "active_event_bus",
    "emit",
    "get_active_bus",
    "set_active_bus",
]
