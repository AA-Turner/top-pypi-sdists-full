"""Property change detection and logging on re-discovery.

Compares freshly discovered property schemas against previously saved ones,
classifying each property as NEW, REMOVED, EXCLUDED, CHANGED, or UNCHANGED.
Preserves manual ``included_in_template=false`` exclusions and emits
structured log entries for every detected change.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

_logger = logging.getLogger(__name__)

CATEGORY_ORDER: dict[str, int] = {
    "NEW": 0,
    "REMOVED": 1,
    "EXCLUDED": 2,
    "CHANGED": 3,
    "UNCHANGED": 4,
}

EXCLUDED_ATTRS: frozenset[str] = frozenset({"included_in_template"})

_MISSING_SENTINEL = "<missing>"


@dataclass
class PropertyChange:
    """A single detected change entry for a property.

    Attributes:
        key: The property name/key.
        category: One of NEW, REMOVED, EXCLUDED, CHANGED, UNCHANGED.
        attribute: The specific attribute that changed (None for baseline entries).
        details: Additional context (old/new values, flags, etc.).
    """

    key: str
    category: str
    attribute: str | None = None
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class PropertyChangeResult:
    """Result of property change detection.

    Attributes:
        merged: The merged property dict (fresh-discovery order, exclusions preserved).
        has_changes: Whether persistence is needed (True for bootstrap or merged schema changes).
        changes: Sorted list of PropertyChange entries describing all detected changes.
    """

    merged: dict[str, dict[str, Any]]
    has_changes: bool
    changes: list[PropertyChange] = field(default_factory=list)


def detect_property_changes(
    saved: dict[str, dict[str, Any]] | None,
    fresh: dict[str, dict[str, Any]],
) -> PropertyChangeResult:
    """Detect changes between saved and freshly discovered property schemas.

    Args:
        saved: Previously persisted property schema keyed by property name,
            or ``None`` for first-time discovery (bootstrap).
        fresh: Freshly discovered property schema keyed by property name.

    Returns:
        A ``PropertyChangeResult`` with the merged schema, change indicator,
        and sorted list of change entries.
    """
    changes: list[PropertyChange] = []
    merged: dict[str, dict[str, Any]] = {}

    # Bootstrap case: saved is None means first-time discovery
    if saved is None:
        for key, props in fresh.items():
            entry = dict(props)
            entry.setdefault("included_in_template", True)
            merged[key] = entry
            changes.append(
                PropertyChange(
                    key=key,
                    category="NEW",
                    details={"included_in_template": True},
                )
            )
        _sort_changes(changes)
        _log_changes(changes)
        _log_summary(changes)
        return PropertyChangeResult(merged=merged, has_changes=True, changes=changes)

    # Normal case: compare saved vs fresh
    saved_keys = set(saved.keys())
    fresh_keys = set(fresh.keys())

    new_keys = fresh_keys - saved_keys
    removed_keys = saved_keys - fresh_keys
    common_keys = saved_keys & fresh_keys

    # Track distinct property categories for summary
    # Process NEW properties
    for key in new_keys:
        entry = dict(fresh[key])
        entry.setdefault("included_in_template", True)
        merged[key] = entry
        changes.append(
            PropertyChange(
                key=key,
                category="NEW",
                details={"included_in_template": True},
            )
        )

    # Process REMOVED properties (omit from merged)
    for key in removed_keys:
        changes.append(
            PropertyChange(
                key=key,
                category="REMOVED",
                details={},
            )
        )

    # Process common properties
    for key in common_keys:
        saved_prop = saved[key]
        fresh_prop = fresh[key]
        is_excluded = not saved_prop.get("included_in_template", True)

        # Build merged entry from fresh data, preserving included_in_template
        entry = dict(fresh_prop)
        if is_excluded:
            entry["included_in_template"] = False
        else:
            entry.setdefault("included_in_template", saved_prop.get("included_in_template", True))

        # Detect attribute changes (excluding included_in_template)
        attr_changes = _diff_attributes(saved_prop, fresh_prop)

        if is_excluded:
            # Baseline EXCLUDED entry always emitted for excluded properties
            changes.append(
                PropertyChange(
                    key=key,
                    category="EXCLUDED",
                    attribute=None,
                    details={"included_in_template": False},
                )
            )
            # Per-attribute EXCLUDED entries for any attribute changes
            for attr, old_val, new_val in attr_changes:
                changes.append(
                    PropertyChange(
                        key=key,
                        category="EXCLUDED",
                        attribute=attr,
                        details={"old": old_val, "new": new_val, "included_in_template": False},
                    )
                )
        elif attr_changes:
            # CHANGED entries for non-excluded properties with attribute changes
            for attr, old_val, new_val in attr_changes:
                changes.append(
                    PropertyChange(
                        key=key,
                        category="CHANGED",
                        attribute=attr,
                        details={"old": old_val, "new": new_val},
                    )
                )
        else:
            # UNCHANGED
            changes.append(
                PropertyChange(
                    key=key,
                    category="UNCHANGED",
                    details={},
                )
            )

        merged[key] = entry

    # Reorder merged to match fresh-discovery insertion order
    ordered_merged: dict[str, dict[str, Any]] = {}
    for key in fresh:
        ordered_merged[key] = merged[key]
    merged = ordered_merged

    _sort_changes(changes)
    _log_changes(changes)
    _log_summary(changes)

    # Determine has_changes from persisted schema delta, not category labels.
    has_changes = merged != saved

    return PropertyChangeResult(merged=merged, has_changes=has_changes, changes=changes)


def _diff_attributes(
    saved_prop: dict[str, Any],
    fresh_prop: dict[str, Any],
) -> list[tuple[str, Any, Any]]:
    """Diff all attributes between saved and fresh property dicts.

    Excludes keys in ``EXCLUDED_ATTRS`` from comparison.
    Uses ``<missing>`` sentinel for keys present on only one side.

    Returns:
        List of (attribute_name, old_value, new_value) tuples for changed attributes.
    """
    all_attrs = (set(saved_prop.keys()) | set(fresh_prop.keys())) - EXCLUDED_ATTRS
    diffs: list[tuple[str, Any, Any]] = []

    for attr in sorted(all_attrs):
        saved_has = attr in saved_prop
        fresh_has = attr in fresh_prop

        if saved_has and fresh_has:
            old_val = saved_prop[attr]
            new_val = fresh_prop[attr]
            if old_val != new_val:
                diffs.append((attr, old_val, new_val))
        elif saved_has and not fresh_has:
            diffs.append((attr, saved_prop[attr], _MISSING_SENTINEL))
        else:
            # fresh_has and not saved_has
            diffs.append((attr, _MISSING_SENTINEL, fresh_prop[attr]))

    return diffs


def _sort_changes(changes: list[PropertyChange]) -> None:
    """Sort changes deterministically per FR-011.

    Order: category (NEW < REMOVED < EXCLUDED < CHANGED < UNCHANGED),
    then alphabetical by key, then baseline before attribute-level,
    then alphabetical by attribute name.
    """
    changes.sort(
        key=lambda c: (
            CATEGORY_ORDER[c.category],
            c.key,
            (0 if c.attribute is None else 1, c.attribute or ""),
        )
    )


def _log_changes(changes: list[PropertyChange]) -> None:
    """Emit per-property log entries at INFO level."""
    for change in changes:
        if change.category == "UNCHANGED":
            _logger.info(
                "UNCHANGED: property '%s' is unchanged",
                change.key,
            )
        elif change.category == "NEW":
            _logger.info(
                "NEW: property '%s' discovered (included_in_template=true)",
                change.key,
            )
        elif change.category == "REMOVED":
            _logger.info(
                "REMOVED: property '%s' no longer present in provider",
                change.key,
            )
        elif change.category == "EXCLUDED":
            if change.attribute is None:
                _logger.info(
                    "EXCLUDED: property '%s' is excluded from template (included_in_template=false)",
                    change.key,
                )
            else:
                _logger.info(
                    "EXCLUDED: property '%s' attribute '%s' changed from '%s' to '%s' "
                    "(included_in_template=false preserved)",
                    change.key,
                    change.attribute,
                    change.details.get("old", ""),
                    change.details.get("new", ""),
                )
        else:  # CHANGED
            _logger.info(
                "CHANGED: property '%s' attribute '%s' changed from '%s' to '%s'",
                change.key,
                change.attribute,
                change.details.get("old", ""),
                change.details.get("new", ""),
            )


def _log_summary(changes: list[PropertyChange]) -> None:
    """Emit a single summary log line with counts per category (distinct properties)."""
    # Count distinct properties per category
    category_keys: dict[str, set[str]] = {
        "NEW": set(),
        "REMOVED": set(),
        "EXCLUDED": set(),
        "CHANGED": set(),
        "UNCHANGED": set(),
    }
    for change in changes:
        category_keys[change.category].add(change.key)

    _logger.info(
        "Property change detection complete: %d new, %d removed, %d excluded, %d changed, %d unchanged",
        len(category_keys["NEW"]),
        len(category_keys["REMOVED"]),
        len(category_keys["EXCLUDED"]),
        len(category_keys["CHANGED"]),
        len(category_keys["UNCHANGED"]),
    )
