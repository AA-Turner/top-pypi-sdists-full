"""Models for epic-tree normalization: hierarchy levels, warnings, and results."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class EpicTreeHierarchyLevel(Enum):
    """Canonical hierarchy levels in an epic tree.

    Maps nesting depth to the logical level of a node:
    - EPIC: root-level work item (depth 0)
    - FEATURE: mid-level deliverable (depth 1)
    - SUBTASK: leaf-level task (depth 2)
    """

    EPIC = "epic"
    FEATURE = "feature"
    SUBTASK = "subtask"


# Mapping from depth to hierarchy level (clamped at subtask for depth >= 2)
_DEPTH_TO_LEVEL: dict[int, EpicTreeHierarchyLevel] = {
    0: EpicTreeHierarchyLevel.EPIC,
    1: EpicTreeHierarchyLevel.FEATURE,
    2: EpicTreeHierarchyLevel.SUBTASK,
}


def derive_epic_tree_hierarchy_level(depth: int, max_depth: int = 3) -> EpicTreeHierarchyLevel:
    """Derive the canonical hierarchy level from a node's depth.

    Computes the effective depth as ``min(depth, max_depth - 1)`` and maps
    it to the corresponding :class:`EpicTreeHierarchyLevel`.

    Args:
        depth: The raw nesting depth of the node (0-based).
        max_depth: The configured maximum depth (default 3). Nodes at or
            beyond ``max_depth - 1`` are clamped to that level.

    Returns:
        The derived hierarchy level for the given depth.
    """
    if depth < 0:
        raise ValueError("depth must be >= 0")
    if max_depth <= 0:
        raise ValueError("max_depth must be > 0")
    if max_depth > 3:
        raise ValueError("max_depth must be <= 3")
    effective_depth = min(depth, max_depth - 1)
    return _DEPTH_TO_LEVEL[min(effective_depth, 2)]


@dataclass(frozen=True)
class NormalizationWarning:
    """A warning emitted when explicit values conflict with depth expectations.

    Attributes:
        ref: The node ``ref`` identifier when present as a string;
            otherwise the sentinel ``"<unknown>"``.
        depth: The raw depth of the node in the tree.
        field: The field name that has a mismatch (``"issueType"`` or ``"labels"``).
        actual_value: The normalized (trimmed, lowercased) actual value found.
        expected_value: The canonical lowercase expected value(s) for the effective depth.
            For label mismatches this can contain a comma-separated list.
    """

    ref: str
    depth: int
    field: str
    actual_value: str
    expected_value: str


@dataclass
class NormalizationResult:
    """Result of normalizing an epic-tree document.

    Attributes:
        document: The normalized document (deep copy of input, with derived values filled in).
        warnings: List of mismatch warnings emitted during normalization.
    """

    document: dict
    warnings: list[NormalizationWarning] = field(default_factory=list)
