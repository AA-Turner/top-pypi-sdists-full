"""Thin re-export adapter for hierarchy persistence.

Re-exports load_hierarchy and save_hierarchy from the existing
agentic_devtools/cli/speckit/hierarchy.py module. No depth-cap logic
here — depth-cap enforcement belongs at detection/path-resolution
call sites, not in this I/O adapter.
"""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.cli.speckit.hierarchy import (
    ChildEntry,
    HierarchyLevel,
    HierarchyNode,
    load_hierarchy,
    save_hierarchy,
)


def hierarchy_level_for_path(path: Path, specs_root: Path) -> HierarchyLevel:
    """Map directory depth under specs/ to hierarchy level.

    Depth is calculated as ``len(path.relative_to(specs_root).parts) - 1``.

    Depth mapping:
    - specs/{epic}/... -> EPIC (depth 0)
    - specs/{epic}/{feature}/... -> FEATURE (depth 1)
    - deeper paths -> TASK (depth >= 2)

    If path is outside specs_root, returns TASK as a safe fallback.
    """
    try:
        depth = len(path.relative_to(specs_root).parts) - 1
    except ValueError:
        return HierarchyLevel.TASK

    if depth <= 0:
        return HierarchyLevel.EPIC
    if depth == 1:
        return HierarchyLevel.FEATURE
    return HierarchyLevel.TASK


__all__ = [
    "ChildEntry",
    "HierarchyLevel",
    "HierarchyNode",
    "hierarchy_level_for_path",
    "load_hierarchy",
    "save_hierarchy",
]
