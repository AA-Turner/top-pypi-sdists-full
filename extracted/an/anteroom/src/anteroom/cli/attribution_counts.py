"""Shared count helper for attribution renderers (#1473).

Centralises the logic for reading section counts from either an
``AttributionSnapshot`` dataclass or a persisted dict, preferring the
canonical ``<section>_count`` fields added in #1473 and falling back to
a truncation-aware computation for older snapshots that lack them.
"""

from __future__ import annotations

from typing import Any


def _real_count_from_list(items: list[Any]) -> int:
    """Compute the real item count from a (possibly capped) section list.

    When a section exceeds SECTION_CAP the list ends with a sentinel
    ``{"truncated": N}``.  This helper recovers the original count so
    renderers display the true number rather than ``cap + 1``.
    """
    if not items:
        return 0
    last = items[-1]
    truncated_n = last.get("truncated", 0) if isinstance(last, dict) and "truncated" in last else 0
    real_items = len(items) - (1 if truncated_n else 0)
    return real_items + truncated_n


def _attribution_count(snapshot: Any, section: str) -> int:
    """Return the real item count for *section* in *snapshot*.

    Prefers the canonical ``<section>_count`` integer field added in
    #1473.  Falls back to a truncation-aware computation on the list in
    two cases:

    1. The field is absent (older persisted dicts that pre-date #1473).
    2. The field is 0 but the section list is non-empty.  This handles
       ``AttributionSnapshot`` instances constructed directly (in tests or
       replay paths) without going through ``build_attribution`` — the
       dataclass defaults all count fields to 0.

    Works with both ``AttributionSnapshot`` dataclass instances and plain
    dicts (deserialized from ``messages.metadata["attribution"]``).
    """
    count_field = f"{section}_count"

    if isinstance(snapshot, dict):
        stored = snapshot.get(count_field)
        items: list[Any] = list(snapshot.get(section) or [])
    else:
        stored_attr = getattr(snapshot, count_field, None)
        stored = stored_attr
        items = list(getattr(snapshot, section, None) or [])

    # Use the canonical field when it's present and positive, OR when both
    # the field and the list agree on zero (genuinely empty section).
    if stored is not None:
        try:
            n = int(stored)
        except (TypeError, ValueError):
            n = None
        if n is not None and (n > 0 or not items):
            return n

    # Fallback: compute from the list, handling the truncation sentinel.
    return _real_count_from_list(items)
