"""TRK-M1-08: docs/PUBLIC_API.md is the consolidated M1 compatibility/migration
document, forward-referenced from ``spec_kitty_tracker/__init__.py``:

    "the public surface is grouped semantically instead in the __all__ list
    and in docs/PUBLIC_API.md (TRK-M1-08), not via source-order comments here."

Node criteria for TRK-M1-08 (BEADS_PROGRAM_GRAPH.json): "Document stable
public API, capability negotiation, additive evolution, deprecation/shims,
consumer inventory, legacy negatives, data/credential non-ownership, and
local migration boundaries."

These tests are drift guards in the same spirit as
``test_public_surface_snapshot.py`` and ``test_version_consistency.py``:
the document must exist, must cover each required topic, and its claims
about the live public surface (exported symbol names, capability-flag
names, forbidden legacy keys, deprecated shim module names) must stay in
sync with the actual runtime contract rather than silently drifting stale.
"""

from __future__ import annotations

import re
from pathlib import Path

import spec_kitty_tracker as pkg
from spec_kitty_tracker.capabilities import TrackerCapabilities
from spec_kitty_tracker.mission_sync import FORBIDDEN_TEAMSPACE_LEGACY_KEYS

DOC_PATH = Path(__file__).parent.parent / "docs" / "PUBLIC_API.md"

REQUIRED_SECTIONS = [
    "Stable Public API",
    "Capability Negotiation",
    "Additive Evolution",
    "Deprecation",
    "Consumer Inventory",
    "Legacy Negatives",
    "Data and Credential Non-Ownership",
    "Local Migration Boundaries",
]

DEPRECATED_SHIM_MODULES = [
    "spec_kitty_tracker.workspace_discovery",
    "spec_kitty_tracker.resource_discovery",
]


def _doc_text() -> str:
    assert DOC_PATH.is_file(), f"Missing required TRK-M1-08 deliverable: {DOC_PATH}"
    return DOC_PATH.read_text(encoding="utf-8")


def test_public_api_doc_exists() -> None:
    assert DOC_PATH.is_file(), f"Missing required TRK-M1-08 deliverable: {DOC_PATH}"


def test_public_api_doc_has_all_required_sections() -> None:
    text = _doc_text()
    missing = [heading for heading in REQUIRED_SECTIONS if heading not in text]
    assert not missing, (
        f"docs/PUBLIC_API.md is missing required TRK-M1-08 section heading(s): {missing}"
    )


def test_public_api_doc_documents_every_exported_symbol() -> None:
    """Every name in ``spec_kitty_tracker.__all__`` must be mentioned in the
    doc (word-boundary match), so a future export addition/removal cannot
    silently drift out of the documented public surface.
    """
    text = _doc_text()
    missing = [name for name in pkg.__all__ if not re.search(rf"\b{re.escape(name)}\b", text)]
    assert not missing, (
        "docs/PUBLIC_API.md does not document these exported symbols "
        f"(present in spec_kitty_tracker.__all__): {sorted(missing)}. "
        "Add a mention (grouped semantically) or the doc has drifted from "
        "the live public surface (TRK-M1-08 node criteria: stable public API)."
    )


def test_public_api_doc_lists_every_capability_flag() -> None:
    """Every ``TrackerCapabilities`` field name must appear in the doc's
    capability-negotiation coverage, so a new capability flag cannot ship
    without a documented negotiation rule.
    """
    text = _doc_text()
    flag_names = list(TrackerCapabilities.as_dict(TrackerCapabilities()).keys())
    assert flag_names, "TrackerCapabilities.as_dict() returned no flags -- test fixture is broken"
    missing = [flag for flag in flag_names if not re.search(rf"\b{re.escape(flag)}\b", text)]
    assert not missing, (
        f"docs/PUBLIC_API.md does not mention capability flag(s): {missing} "
        "(TRK-M1-08 node criteria: capability negotiation)."
    )


def test_public_api_doc_lists_forbidden_teamspace_legacy_keys() -> None:
    """Every retired TeamSpace key that tracker denies on egress
    (``FORBIDDEN_TEAMSPACE_LEGACY_KEYS``) must be named in the legacy
    negatives section, so the documented negative contract cannot drift
    silently out of sync with the enforced one.
    """
    text = _doc_text()
    missing = [
        key
        for key in FORBIDDEN_TEAMSPACE_LEGACY_KEYS
        if not re.search(rf"\b{re.escape(key)}\b", text)
    ]
    assert not missing, (
        f"docs/PUBLIC_API.md does not name forbidden legacy key(s): {sorted(missing)} "
        "(TRK-M1-08 node criteria: legacy negatives)."
    )


def test_public_api_doc_names_deprecated_shim_modules() -> None:
    text = _doc_text()
    missing = [mod for mod in DEPRECATED_SHIM_MODULES if mod not in text]
    assert not missing, (
        f"docs/PUBLIC_API.md does not name deprecated shim module(s): {missing} "
        "(TRK-M1-08 node criteria: deprecation/shims)."
    )


def test_public_api_doc_names_known_consumers() -> None:
    """Consumer inventory: the two known downstream products that consume
    Tracker's public contract (TRACKER_ARCH_ROLE.md §5) must be named.
    """
    text = _doc_text()
    for consumer in ("spec-kitty", "spec-kitty-saas"):
        assert consumer in text, (
            f"docs/PUBLIC_API.md does not name known consumer {consumer!r} "
            "(TRK-M1-08 node criteria: consumer inventory)."
        )


def test_public_api_doc_names_credential_sentinel() -> None:
    """Data/credential non-ownership: the doc must name the
    ``NANGO_MANAGED_TOKEN`` sentinel used in place of real credentials in
    hosted-connector construction, proving tracker never mints/persists a
    real provider credential.
    """
    text = _doc_text()
    assert "NANGO_MANAGED_TOKEN" in text, (
        "docs/PUBLIC_API.md does not name the NANGO_MANAGED_TOKEN credential "
        "sentinel (TRK-M1-08 node criteria: data/credential non-ownership)."
    )
