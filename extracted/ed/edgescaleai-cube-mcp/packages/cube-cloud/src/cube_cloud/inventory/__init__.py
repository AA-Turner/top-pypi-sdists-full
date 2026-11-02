"""Cube inventory facts (customer, site label, serial, status, location) for the console.

These fields live in the `edgescale-inventory` service rather than in Apollo, which
is why the console could only ever show `cube-o2e87m9a` — see **OI-2** in
`docs/console-spec.md`. `client.py` carries the four load-bearing rules (authorized
cluster set in, exact-match join, ambiguity resolves to absence, failure is silent to
the page); `records.py` carries the containment boundary that keeps the rest of a
record — IPMI password, MACs, router serials, operator notes — out of the browser.
"""

from __future__ import annotations

from cube_cloud.inventory.client import (
    InventoryError,
    InventoryLookup,
    NO_MATCH,
    Resolution,
    build_index,
    build_index_detailed,
    invalidate,
    is_enabled,
    lookup,
    lookup_each,
    lookup_fleet,
)
from cube_cloud.inventory.records import (
    CARRIED_KEYS,
    HARDWARE_KEYS,
    HARDWARE_SUMMARY_FIELDS,
    SUMMARY_FIELDS,
    Hardware,
    InventoryRecord,
    hardware_from_raw,
    record_from_raw,
)

__all__ = [
    "CARRIED_KEYS",
    "HARDWARE_KEYS",
    "HARDWARE_SUMMARY_FIELDS",
    "SUMMARY_FIELDS",
    "Hardware",
    "InventoryError",
    "InventoryLookup",
    "InventoryRecord",
    "NO_MATCH",
    "Resolution",
    "build_index",
    "build_index_detailed",
    "hardware_from_raw",
    "invalidate",
    "is_enabled",
    "lookup",
    "lookup_each",
    "lookup_fleet",
    "record_from_raw",
]
