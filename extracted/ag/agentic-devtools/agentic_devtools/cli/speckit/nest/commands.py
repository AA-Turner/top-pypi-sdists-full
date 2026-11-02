"""Synchronous orchestration for the nest command.

Plan display is the default behavior. Pass --execute to perform the
migration. Pass --dry-run to compute the plan without writes.
"""

from __future__ import annotations

import hashlib
import json
import re as _re
import subprocess
import sys
from pathlib import Path

from agentic_devtools.cli.speckit.hierarchy import HierarchyValidationError
from agentic_devtools.cli.speckit.shared.hierarchy import load_hierarchy

from .crossref import CrossRefUpdate, scan_crossrefs
from .discovery import ChildRef, FlatSpec, build_relationship_graph, scan_existing_targets, scan_flat_specs
from .display import format_migration_plan
from .execution import execute_migration
from .plan import MigrationPlan, compute_migration_plan

# Matches GitHub HTTPS remotes: https://github.com/owner/repo[.git]
_GITHUB_HTTPS_RE = _re.compile(r"^https://github\.com/([^/]+)/([^/]+?)(?:\.git)?$")
# Matches GitHub SSH remotes: git@github.com:owner/repo[.git]
_GITHUB_SSH_RE = _re.compile(r"^git@github\.com:([^/]+)/([^/]+?)(?:\.git)?$")


def nest_command(
    specs_root: str | Path | None = None,
    execute: bool = False,
    dry_run: bool = False,
    scope: int | None = None,
    owner: str | None = None,
    repo: str | None = None,
    expected_plan_fingerprint: str | None = None,
) -> str | None:
    """Orchestrate the nest migration command.

    Default behavior: compute and display the migration plan.
    --execute: perform the migration after computing the plan.
    --dry-run: compute and display without writes (same as default but
    explicitly signals intent).

    Args:
        specs_root: Path to the specs/ directory. Defaults to ./specs.
        execute: If True, perform the migration.
        dry_run: If True, compute plan only (no writes, no commits).
        scope: Optional issue number to limit migration scope.
        owner: GitHub repository owner. Auto-detected if not provided.
        repo: GitHub repository name. Auto-detected if not provided.
        expected_plan_fingerprint: Optional fingerprint of the approved
            migration plan. When provided, execution aborts if the freshly
            computed plan differs from the approved preview plan.

    Returns:
        Fingerprint of the computed migration plan when a plan is produced;
        otherwise ``None`` (for early exits such as missing specs).
    """
    if specs_root is None:
        specs_root = Path.cwd() / "specs"
    specs_root = Path(specs_root)

    if not specs_root.exists():
        print("Error: specs/ directory not found.", file=sys.stderr)
        sys.exit(1)

    if not specs_root.is_dir():
        print(f"Error: specs/ path is not a directory: {specs_root}", file=sys.stderr)
        sys.exit(1)

    # Auto-detect owner/repo from git remote if not provided
    if owner is None or repo is None:
        detected_owner, detected_repo = _detect_owner_repo()
        owner = owner or detected_owner
        repo = repo or detected_repo

    if not owner or not repo:
        print(
            "Error: Could not determine GitHub owner/repo. "
            "Use --owner and --repo flags or ensure a GitHub remote is configured.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Phase 1: Scan for flat specs and already-migrated targets
    print("Scanning for flat spec directories...")
    try:
        flat_specs = scan_flat_specs(specs_root)
        existing_targets = scan_existing_targets(specs_root)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    if not flat_specs and not existing_targets:
        print("No flat spec directories found. Nothing to migrate.")
        return None

    if flat_specs:
        print(f"Found {len(flat_specs)} flat spec directories.")
        flat_issue_numbers = {s.issue_number for s in flat_specs}
        extra_sources = [
            FlatSpec(issue_number=issue_number, path=issue_path, slug=issue_path.name)
            for issue_number, issue_path in sorted(existing_targets.items())
            if issue_number not in flat_issue_numbers
        ]
        graph_sources = flat_specs + extra_sources
        if extra_sources:
            print(f"Also including {len(extra_sources)} already-nested issue directories in relationship discovery.")
    else:
        print(
            "No flat spec directories found; checking existing nested issue directories for hierarchy materialization."
        )
        graph_sources = [
            FlatSpec(issue_number=issue_number, path=issue_path, slug=issue_path.name)
            for issue_number, issue_path in sorted(existing_targets.items())
        ]

    # Phase 2: Build relationship graph
    print("Querying GitHub API for parent/child relationships...")
    discovery = build_relationship_graph(owner, repo, graph_sources)
    for warning in discovery.warnings:
        print(f"  ⚠ {warning}")

    # Phase 3: Compute migration plan
    try:
        plan = compute_migration_plan(
            discovery.graph,
            flat_specs,
            specs_root,
            scope=scope,
            existing_targets=existing_targets,
        )
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    plan.warnings = discovery.warnings + plan.warnings

    discovered_issues = set(existing_targets) | {spec.issue_number for spec in flat_specs}
    discovered_issues.update(discovery.graph)
    if scope is not None and scope not in discovered_issues:
        # A scoped spec that stays flat (isolated, cyclic, depth-capped) or only
        # needs hierarchy materialization still has a known scope and must render.
        print(f"No specs matched scope #{scope}. Nothing to migrate.")
        return None

    # Phase 4: Scan for cross-references
    crossref_updates = scan_crossrefs(plan.moves, specs_root)
    actionable_hierarchy_files = _filter_actionable_hierarchy_files(plan)
    display_plan = _copy_plan_with_hierarchy_files(plan, actionable_hierarchy_files)
    filtered_plan = _copy_plan_with_hierarchy_files(plan, actionable_hierarchy_files, preserve_scope_relationships=True)
    plan_fingerprint = _compute_plan_fingerprint(filtered_plan, crossref_updates)

    if expected_plan_fingerprint is not None and expected_plan_fingerprint != plan_fingerprint:
        print(
            "Error: Migration plan changed since approval. Re-run preview and confirm again.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Phase 5: Display plan
    print(format_migration_plan(display_plan))

    if crossref_updates:
        print(f"Cross-reference updates needed: {len(crossref_updates)}")
        for update in crossref_updates:
            print(f"  {update.file_path}:{update.line_number}: {update.old_ref} → {update.new_ref}")
        print()

    if not plan.moves and not actionable_hierarchy_files and not crossref_updates:
        # Nothing to execute. If the rendered plan explains why candidates were
        # excluded (cycle, depth cap, etc.), keep the final status neutral so
        # it does not contradict the detailed plan output above.
        if plan.remaining_flat or plan.warnings:
            print("No executable migration changes were identified. See the plan output above for details.")
        else:
            print("All specs are standalone or already nested. Nothing to migrate.")
        return None

    if dry_run:
        print("DRY RUN — No changes made.")
        return plan_fingerprint

    if not execute:
        print(
            "Plan computed. Pass --execute to perform the migration, "
            "or --dry-run to explicitly preview without changes."
        )
        return plan_fingerprint

    # Phase 6: Execute. execute_migration() owns preflight, HEAD capture, the
    # full mutating sequence, staging, the commit, and rollback on failure.
    try:
        execute_migration(filtered_plan, specs_root, crossref_updates, scope=scope)
    except (ValueError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Migration complete. {len(plan.moves)} specs migrated and committed.")
    return plan_fingerprint


def _filter_actionable_hierarchy_files(plan: MigrationPlan) -> dict[str, list[ChildRef]]:
    """Return only hierarchy files whose merge would change repository state."""
    actionable: dict[str, list[ChildRef]] = {}
    for dir_path_str, children in plan.hierarchy_files.items():
        try:
            already_done = _hierarchy_is_already_materialized(Path(dir_path_str), children)
        except (HierarchyValidationError, OSError) as exc:
            print(
                f"Error: Cannot read existing hierarchy file in {dir_path_str}: {exc}",
                file=sys.stderr,
            )
            sys.exit(1)
        if not already_done:
            actionable[dir_path_str] = children
    return actionable


def _hierarchy_is_already_materialized(dir_path: Path, children: list[ChildRef]) -> bool:
    """Return True when every planned child already exists with matching metadata."""
    hierarchy_path = dir_path / "hierarchy.yml"
    if hierarchy_path.is_symlink():
        raise OSError(f"symlinked hierarchy file is not allowed: {hierarchy_path}")
    if not hierarchy_path.exists():
        return False

    existing_children = {child.key: child for child in load_hierarchy(hierarchy_path).children}
    for child in children:
        existing = existing_children.get(str(child.number))
        if existing is None or existing.title != child.title or existing.order != child.order:
            return False
    return True


def _copy_plan_with_hierarchy_files(
    plan: MigrationPlan,
    hierarchy_files: dict[str, list[ChildRef]],
    preserve_scope_relationships: bool = False,
) -> MigrationPlan:
    """Copy *plan* while substituting the hierarchy file mapping."""
    return MigrationPlan(
        moves=list(plan.moves),
        hierarchy_files=hierarchy_files,
        scope_hierarchy_files=plan.hierarchy_files if preserve_scope_relationships else plan.scope_hierarchy_files,
        excluded_cycles=[set(cycle) for cycle in plan.excluded_cycles],
        multi_parent_selections=dict(plan.multi_parent_selections),
        multi_parent_candidates={issue: list(candidates) for issue, candidates in plan.multi_parent_candidates.items()},
        remaining_flat=list(plan.remaining_flat),
        warnings=list(plan.warnings),
        existing_root_issues=set(plan.existing_root_issues),
    )


def _compute_plan_fingerprint(plan: MigrationPlan, crossref_updates: list[CrossRefUpdate]) -> str:
    """Return a deterministic fingerprint for the computed migration plan."""
    payload = {
        "moves": sorted((str(move.source), str(move.target), move.issue_number) for move in plan.moves),
        "remaining_flat": sorted((spec.issue_number, spec.slug, str(spec.path)) for spec in plan.remaining_flat),
        "warnings": sorted(plan.warnings),
        "roots": sorted(plan.roots),
        "existing_root_issues": sorted(plan.existing_root_issues),
        "hierarchy_files": [
            (
                dir_path,
                [(child.number, child.title, child.order) for child in children],
            )
            for dir_path, children in sorted(plan.hierarchy_files.items())
        ],
        "crossref_updates": sorted(
            (str(update.file_path), update.line_number, update.old_ref, update.new_ref) for update in crossref_updates
        ),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _detect_owner_repo() -> tuple[str | None, str | None]:
    """Detect owner/repo from a GitHub git remote origin URL.

    Only matches GitHub HTTPS (``https://github.com/owner/repo``) and
    GitHub SSH (``git@github.com:owner/repo``) formats.  Non-GitHub remotes
    (e.g. GitLab, Azure DevOps) return ``(None, None)`` so callers do not
    silently target the wrong repository.
    """
    result = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        capture_output=True,
        text=True,
        shell=False,
    )
    if result.returncode != 0:
        return None, None

    url = result.stdout.strip()
    match = _GITHUB_HTTPS_RE.match(url) or _GITHUB_SSH_RE.match(url)
    if match:
        return match.group(1), match.group(2)
    return None, None
