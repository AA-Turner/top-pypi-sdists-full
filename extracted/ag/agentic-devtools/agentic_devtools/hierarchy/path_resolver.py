"""Nested filesystem path resolution for spec directories.

Resolves spec directory paths based on hierarchy level:
- Hierarchical: ``specs/{epic}/{feature}/{task}/``
- Standalone/depth-cap: ``specs/{number}-{short-name}/``
"""

from __future__ import annotations

import re
from pathlib import Path

from agentic_devtools.hierarchy.models import HierarchyLevel, HierarchyMetadata


def _slugify(title: str) -> str:
    """Convert a title to a filesystem-safe slug.

    Converts to lowercase, replaces non-alphanumeric characters with hyphens,
    collapses consecutive hyphens, and trims leading/trailing hyphens.

    Args:
        title: The title to slugify.

    Returns:
        A filesystem-safe slug string.
    """
    slug = title.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-") or "spec"


def resolve_spec_path(
    issue_number: int,
    metadata: HierarchyMetadata,
    specs_root: Path,
    *,
    short_name: str = "",
    title: str = "",
    ancestors: list[int] | None = None,
) -> Path:
    """Resolve the spec directory path for an issue.

    Hierarchical issues get nested numeric paths: ``specs/{epic}/{feature}/{task}/``.
    All hierarchy-level directory components are strictly numeric so that ancestor
    references always resolve to the same directory regardless of whether a
    ``short_name``/``title`` was supplied when the ancestor's own spec was created.
    Standalone and depth-cap issues get flat paths: ``specs/{number}-{short-name}/``.

    Args:
        issue_number: The issue number.
        metadata: Hierarchy metadata for the issue.
        specs_root: Root path of the specs directory.
        short_name: Short name for the issue (used only in flat/fallback paths).
        title: Alias for *short_name* — either may be used; *short_name* takes
               precedence when both are supplied.
        ancestors: Ordered list of ancestor issue numbers (grandparent → parent)
                   for hierarchical path construction.

    Returns:
        Path to the issue's spec directory.
    """
    resolved_name = short_name or title  # short_name takes precedence (empty str is falsy)

    # Standalone issues use flat path
    if metadata.level == HierarchyLevel.STANDALONE:
        slug = _slugify(resolved_name) if resolved_name else "spec"
        return specs_root / f"{issue_number}-{slug}"

    # Build hierarchical path from ancestors + this issue (always numeric, no slug)
    if ancestors and metadata.level in (HierarchyLevel.FEATURE, HierarchyLevel.TASK):
        parts = [str(a) for a in ancestors]
        if metadata.parent is not None and metadata.parent not in ancestors:
            parts.append(str(metadata.parent))
        parts.append(str(issue_number))
        return specs_root.joinpath(*parts)

    # Epic-level: strictly numeric
    if metadata.level == HierarchyLevel.EPIC:
        return specs_root / str(issue_number)

    if metadata.parent is not None:
        return specs_root / str(metadata.parent) / str(issue_number)

    # Fallback to flat path
    slug = _slugify(resolved_name) if resolved_name else "spec"
    return specs_root / f"{issue_number}-{slug}"
