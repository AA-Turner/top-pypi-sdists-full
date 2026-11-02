"""Hierarchy placement logic for the retro-spec command.

Determines the correct directory location for a retroactively generated
spec based on parent relationships and the existing directory structure.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

from agentic_devtools.cli.speckit.shared.github_api import discover_relationships


@dataclass
class PlacementResult:
    """Result of hierarchy placement resolution.

    Attributes:
        target_path: The resolved target directory path.
        parent_issue: Parent issue number, if any.
        needs_hierarchy_update: Whether the parent's hierarchy.yml needs updating.
    """

    target_path: Path
    parent_issue: int | None = None
    needs_hierarchy_update: bool = False


def resolve_placement(
    owner: str,
    repo: str,
    issue_number: int,
    specs_root: str | Path,
    issue_title: str = "",
) -> PlacementResult:
    """Resolve the target placement for a retroactive spec.

    Determines where to place the spec based on parent relationships:
    - If no parent: place at specs/{issue_number}-{slug}/ when title is available
      (fallback: specs/{issue_number}/ when title is empty)
    - If parent has canonical nested path: place beneath it
    - If parent is at legacy flat path: abort with guidance

    Respects the depth cap of 3 levels (Epic=0, Feature=1, Task=2).

    Args:
        owner: GitHub repository owner.
        repo: GitHub repository name.
        issue_number: The issue to place.
        specs_root: Path to the specs/ directory.
        issue_title: GitHub issue title used to name standalone specs.

    Returns:
        PlacementResult with the resolved target path.

    Raises:
        SystemExit: If parent exists only at a legacy flat path.
    """
    specs_path = Path(specs_root)
    parent, _ = discover_relationships(owner, repo, issue_number)
    flat_target = (
        specs_path / f"{issue_number}-{_slugify(issue_title)}" if issue_title else specs_path / str(issue_number)
    )

    if parent is None:
        # No parent — retain the established flat naming convention.
        return PlacementResult(
            target_path=flat_target,
            parent_issue=None,
            needs_hierarchy_update=False,
        )

    # Bounded search for an existing parent directory: check root + 1 level deep.
    # A parent at level 0 (specs/{parent}/) puts the child at level 1 (within cap).
    # A parent at level 1 (specs/*/{parent}/) puts the child at level 2 (within cap).
    # No valid parent can live at level 2 or deeper without pushing the child beyond
    # the 3-level depth cap, so a deeper rglob walk is both unnecessary and expensive.
    canonical_parent_path: Path | None = None
    parent_name = str(parent)
    if specs_path.is_dir():
        level0 = specs_path / parent_name
        if level0.is_dir() and not level0.is_symlink():
            canonical_parent_path = level0
        else:
            for l1_dir in sorted(specs_path.iterdir(), key=lambda path: path.name):
                if l1_dir.is_symlink() or not l1_dir.is_dir() or not l1_dir.name.isdigit():
                    continue
                candidate = l1_dir / parent_name
                if candidate.is_dir() and not candidate.is_symlink():
                    canonical_parent_path = candidate
                    break

    if canonical_parent_path is not None:
        hierarchy_path = canonical_parent_path / "hierarchy.yml"
        if hierarchy_path.is_symlink():
            print(
                f"Error: Parent issue #{parent} has a symlinked hierarchy.yml "
                f"({hierarchy_path.relative_to(specs_path)}), which retro-spec will not modify.\n"
                "Replace it with a regular file before creating a child spec.",
                file=sys.stderr,
            )
            sys.exit(1)
        # Check depth cap: count ancestors
        target = canonical_parent_path / str(issue_number)
        # Count depth from specs_root
        depth = len(target.relative_to(specs_path).parts) - 1
        if depth > 2:
            # Exceeds depth cap — place at flat path
            return PlacementResult(
                target_path=flat_target,
                parent_issue=parent,
                needs_hierarchy_update=False,
            )
        return PlacementResult(
            target_path=target,
            parent_issue=parent,
            needs_hierarchy_update=True,
        )

    # Check for legacy flat parents at any depth (e.g., specs/10/20-feature/).
    # Guard against specs_root not existing before iterating.
    if specs_path.is_dir():
        for entry in specs_path.rglob("*"):
            if entry.is_symlink() or not entry.is_dir():
                continue
            if entry.name.startswith(f"{parent}-"):
                print(
                    f"Error: Parent issue #{parent} exists only at a legacy flat path "
                    f"({entry.relative_to(specs_path)}/). Cannot create a hybrid path.\n"
                    f"Migrate the parent first using: agdt-speckit-nest --scope {parent} --execute",
                    file=sys.stderr,
                )
                sys.exit(1)
            relative_parts = entry.relative_to(specs_path).parts
            if entry.name == parent_name and any(not part.isdigit() for part in relative_parts[:-1]):
                print(
                    f"Error: Parent issue #{parent} exists below a non-numeric ancestor "
                    f"({entry.relative_to(specs_path)}/), which is not a canonical hierarchy path.\n"
                    f"Move the parent into a numeric hierarchy before creating a child.",
                    file=sys.stderr,
                )
                sys.exit(1)

    # Parent has no spec directory — place at root level
    return PlacementResult(
        target_path=flat_target,
        parent_issue=parent,
        needs_hierarchy_update=False,
    )


def _slugify(title: str) -> str:
    """Convert an issue title into a safe, stable directory slug."""
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug[:80].rstrip("-") or "spec"
