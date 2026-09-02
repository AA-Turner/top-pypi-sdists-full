"""Atomic migration execution and rollback for the nest command.

Implements preflight checks (clean working tree), atomic execution
(snapshot HEAD → move dirs → write hierarchy.yml → apply crossref updates),
and rollback on failure (git reset --hard + git clean -fd -- specs/).
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from agentic_devtools.cli.git.operations import create_commit
from agentic_devtools.cli.speckit.shared.commit import format_commit_message
from agentic_devtools.cli.speckit.shared.conflict_check import check_target_conflicts
from agentic_devtools.cli.speckit.shared.hierarchy import (
    ChildEntry,
    HierarchyNode,
    hierarchy_level_for_path,
    load_hierarchy,
    save_hierarchy,
)

from .crossref import CrossRefUpdate, apply_crossref_updates
from .plan import MigrationPlan
from .readme_index import update_readme


def preflight_check(specs_root: str | Path) -> None:
    """Ensure repository is in a clean state before migration.

    Validates:
    - Clean working tree (no unstaged changes)
    - Clean git index (no staged changes)
    - No untracked files under specs/

    Untracked files **outside** specs/ are allowed: staging is scoped to the
    specs root, so unrelated work-in-progress files are never committed.

    Args:
        specs_root: Path to the specs/ directory.

    Raises:
        SystemExit: If any preflight check fails.
    """
    # Check for staged changes
    result = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        capture_output=True,
        text=True,
        shell=False,
    )
    if result.returncode == 1:
        print(
            "Error: Git index has staged changes. Commit or stash changes before running nest migration.",
            file=sys.stderr,
        )
        sys.exit(1)
    elif result.returncode != 0:
        print(
            f"Error: git diff --cached failed: {result.stderr.strip()}",
            file=sys.stderr,
        )
        sys.exit(1)

    # Check for unstaged changes
    result = subprocess.run(
        ["git", "diff", "--quiet"],
        capture_output=True,
        text=True,
        shell=False,
    )
    if result.returncode == 1:
        print(
            "Error: Working tree has unstaged changes. Commit or stash changes before running nest migration.",
            file=sys.stderr,
        )
        sys.exit(1)
    elif result.returncode != 0:
        print(
            f"Error: git diff failed: {result.stderr.strip()}",
            file=sys.stderr,
        )
        sys.exit(1)

    # Check for untracked files under specs/
    try:
        specs_relpath = _specs_repo_relative_pathspec(specs_root)
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    result = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard", specs_relpath],
        capture_output=True,
        text=True,
        shell=False,
    )
    if result.returncode != 0:
        print(
            "Error: git ls-files failed while checking for untracked files under specs/. "
            "Ensure you are running inside a git repository and specs/ is within the repo.",
            file=sys.stderr,
        )
        sys.exit(1)
    if result.stdout.strip():
        print(
            "Error: Untracked files found under specs/. Remove or commit them before running nest migration.",
            file=sys.stderr,
        )
        sys.exit(1)


def build_commit_message(roots: list[int], move_count: int) -> str:
    """Build the conventional-commit message for a migration commit.

    Args:
        roots: Sorted list of hierarchy root issue numbers included in this
            commit.  A single-element list produces the same output as the
            previous single-scope API.  A multi-element list produces a
            comma-separated scope and footer (per the repo commit convention for
            multiple unrelated issues).
        move_count: Number of directories moved by the migration.

    Returns:
        The formatted commit message.

    Raises:
        ValueError: If ``roots`` is empty, any root is not a positive integer,
            or ``move_count`` is negative.
    """
    if not roots:
        raise ValueError("roots must be a non-empty list of positive issue numbers")
    for r in roots:
        if r <= 0:
            raise ValueError(f"scope must be a positive issue number, got: {r}")
    if move_count < 0:
        raise ValueError(f"move_count must be non-negative, got: {move_count}")

    scope_str = ", ".join(f"#{r}" for r in roots)
    # footer per commit convention: single issue → "#N"; multiple unrelated
    # issues → "#N, #M". Passed as a pre-formatted str; format_commit_message
    # uses str values verbatim.
    footer = ", ".join(f"#{r}" for r in roots)

    description = (
        f"materialize nested hierarchy for {len(roots)} root{'s' if len(roots) != 1 else ''}"
        if move_count == 0
        else f"migrate {move_count} flat specs to nested hierarchy"
    )
    return format_commit_message(
        commit_type="refactor",
        scope=scope_str,
        description=description,
        issue=footer,
        co_authored=True,
    )


def resolve_commit_scope(plan: MigrationPlan, explicit_scope: int | None = None) -> list[int]:
    """Resolve the sorted list of issue numbers used as the commit scope.

    An explicit ``--scope``/``--issue`` value always wins and is returned as a
    single-element list.  Otherwise all hierarchy roots of the plan are
    returned as a sorted list, allowing a single unscoped atomic commit to
    migrate multiple independent hierarchies at once.

    For partial migrations whose root already exists in the nested layout, the
    root issue is supplied via :attr:`MigrationPlan.existing_root_issues` by
    :func:`compute_migration_plan`.

    Args:
        plan: The computed migration plan.
        explicit_scope: The user-supplied scope, when provided.

    Returns:
        List of resolved root issue numbers (single-element when an explicit
        scope is given or the plan has one root; multi-element for unscoped
        plans with multiple independent roots).

    Raises:
        ValueError: If no explicit scope was given and the plan contains zero
            hierarchy roots.
    """
    if explicit_scope is not None:
        return [explicit_scope]

    roots = plan.roots
    if not roots:
        raise ValueError(
            "Cannot infer a commit scope: the migration plan contains no hierarchy roots. Specify --scope N."
        )
    return roots


def execute_migration(
    plan: MigrationPlan,
    specs_root: str | Path,
    crossref_updates: list[CrossRefUpdate] | None = None,
    scope: int | None = None,
) -> None:
    """Execute the migration plan atomically.

    Owns the complete atomic sequence: validation → HEAD capture → preflight →
    directory moves → ``hierarchy.yml`` creation → cross-reference rewrite →
    ``specs/README.md`` index update → scoped staging → single commit.  Any
    failure after the HEAD capture triggers :func:`rollback_migration`, so the
    repository is never left in a partially migrated state.  The rollback
    boundary covers both normal exceptions *and* ``BaseException`` cancellations
    (e.g. ``KeyboardInterrupt``) via a ``finally`` guard.

    Args:
        plan: The computed migration plan.
        specs_root: Path to the specs/ directory.
        crossref_updates: Optional list of cross-reference updates to apply.
        scope: Explicit commit scope; inferred from the plan when omitted.

    Raises:
        ValueError: If target conflicts, pre-existing hierarchy.yml files, or an
            unresolvable commit scope are detected. No filesystem writes have
            occurred at that point, so no rollback is needed.
        RuntimeError: If HEAD cannot be captured, or if a post-capture step
            fails (after rollback has been attempted).
    """
    specs_path = Path(specs_root)

    # --- Validation: no writes have happened yet, so failures need no rollback.
    conflicts = check_target_conflicts(plan.moves)
    if conflicts:
        raise ValueError(
            "Target directory conflicts detected. Cannot proceed.\n"
            "Conflicting paths:\n" + "\n".join(f"  - {c}" for c in conflicts)
        )

    existing_hierarchies = _find_existing_hierarchy_files(plan)
    if existing_hierarchies:
        raise ValueError(
            "hierarchy.yml files already exist at planned locations. "
            "Remove or archive them before running nest migration.\n"
            "Existing files:\n" + "\n".join(f"  - {path}" for path in existing_hierarchies)
        )

    hierarchy_targets = [Path(path) for path in plan.hierarchy_files]
    symlinked_components = _symlinked_target_components(plan.moves, specs_path, extra_targets=hierarchy_targets)
    if symlinked_components:
        raise ValueError(
            "Planned target paths traverse symlinked directories. Cannot proceed safely.\n"
            "Symlinked components:\n" + "\n".join(f"  - {c}" for c in symlinked_components)
        )

    commit_roots = resolve_commit_scope(plan, scope)
    commit_message = build_commit_message(commit_roots, len(plan.moves))

    preflight_check(specs_path)
    pre_run_head = _capture_head()

    # --- Mutating sequence: everything below is inside the rollback boundary.
    # Catch BaseException so that cancellations (e.g. KeyboardInterrupt) also
    # trigger rollback, preserving the atomicity guarantee.
    try:
        _apply_moves(plan)
        _write_hierarchy_files(plan, specs_path)
        if crossref_updates:
            apply_crossref_updates(crossref_updates)
        update_readme(specs_path)
        _stage_specs(specs_path)
        create_commit(message=commit_message, dry_run=False)
    except BaseException as exc:
        print(
            f"Migration failed: {exc}. Rolling back...",
            file=sys.stderr,
        )
        if rollback_migration(pre_run_head, specs_path):
            print("Rollback complete. Repository restored to pre-migration state.", file=sys.stderr)
        else:
            print(
                "Rollback attempted, but the repository may not be fully restored. "
                "Inspect the warnings above before proceeding.",
                file=sys.stderr,
            )
        if isinstance(exc, Exception):
            # Regular exception: wrap for a clear caller-facing error message.
            raise RuntimeError(f"Migration failed and was rolled back: {exc}") from exc
        # BaseException (e.g. KeyboardInterrupt) — re-raise bare so that
        # signal semantics (SIGINT exit) are preserved for the caller.
        raise


def _find_existing_hierarchy_files(plan: MigrationPlan) -> list[Path]:
    """Find moved-source hierarchy.yml files that the migration would overwrite.

    Existing hierarchy files at already-nested target locations are merged
    during ``_write_hierarchy_files`` so partial migrations can extend prior
    runs safely.  The only remaining silent-overwrite risk is a moved source
    directory that already contains its own ``hierarchy.yml``: after the move it
    would land at the target path and then be overwritten by ``save_hierarchy()``.

    Both real files and dangling symlinks are included: ``.exists()`` returns
    ``False`` for dangling symlinks but ``is_symlink()`` catches them, and
    after the move ``save_hierarchy`` would follow the link and could write
    outside the repository.
    """
    move_source_by_target = {str(move.target): move.source for move in plan.moves}
    existing_hierarchies: list[Path] = []
    for dir_path_str in plan.hierarchy_files:
        source_dir = move_source_by_target.get(dir_path_str)
        if source_dir is not None:
            candidate = source_dir / "hierarchy.yml"
            if candidate.exists() or candidate.is_symlink():
                existing_hierarchies.append(candidate)
    return existing_hierarchies


def _apply_moves(plan: MigrationPlan) -> None:
    """Move every planned spec directory to its target location."""
    for move in plan.moves:
        move.target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(move.source), str(move.target))


def _symlinked_target_components(
    moves: list,
    specs_root: Path,
    *,
    extra_targets: list[Path] | None = None,
) -> list[str]:
    """Collect symlinked existing directory components on planned target paths.

    Walks every directory ancestor of each planned target path (from
    ``specs_root`` down to the target leaf, exclusive of ``specs_root`` itself)
    and returns the string representations of any that already exist as
    symlinks. A symlinked parent like ``specs/100 -> ../outside`` would cause
    ``mkdir`` and ``shutil.move``/``write_text`` to write outside the
    repository, so the caller must abort before any filesystem mutations when
    this list is non-empty.

    Args:
        moves: Sequence of :class:`Move` objects from the migration plan.
        specs_root: Absolute path to the specs directory.
        extra_targets: Additional planned target directories (for example,
            hierarchy-only ``hierarchy.yml`` locations that do not correspond to
            a move target).

    Returns:
        Sorted, deduplicated list of symlinked path strings.
    """
    seen: set[str] = set()
    result: list[str] = []
    target_paths = [move.target for move in moves]
    if extra_targets:
        target_paths.extend(extra_targets)
    for path in target_paths:
        chain: list[Path] = []
        while path != specs_root and path != path.parent:
            chain.append(path)
            path = path.parent
        for ancestor in reversed(chain):  # specs_root → target
            key = str(ancestor)
            if key in seen:
                continue
            seen.add(key)
            if ancestor.is_symlink():
                result.append(key)
    return sorted(result)


def _write_hierarchy_files(plan: MigrationPlan, specs_path: Path) -> None:
    """Write a hierarchy.yml for every parent directory in the plan."""
    for dir_path_str, children in plan.hierarchy_files.items():
        dir_path = Path(dir_path_str)
        dir_path.mkdir(parents=True, exist_ok=True)
        hierarchy_path = dir_path / "hierarchy.yml"
        child_entries = [ChildEntry(key=str(child.number), title=child.title, order=child.order) for child in children]
        if hierarchy_path.exists():
            node = _merge_existing_hierarchy(hierarchy_path, child_entries)
        else:
            node = _build_hierarchy_node(dir_path, specs_path, child_entries)
        save_hierarchy(node, hierarchy_path)


def _build_hierarchy_node(dir_path: Path, specs_path: Path, child_entries: list[ChildEntry]) -> HierarchyNode:
    """Build a fresh hierarchy node for a directory that has no existing file."""
    parent_dir = dir_path.parent
    parent_key: str | None = None
    if parent_dir != specs_path and parent_dir.name.isdigit():
        parent_key = parent_dir.name
    return HierarchyNode(
        title=f"Issue #{dir_path.name}" if dir_path.name.isdigit() else dir_path.name,
        level=hierarchy_level_for_path(dir_path, specs_path),
        parent=parent_key,
        children=child_entries,
    )


def _merge_existing_hierarchy(hierarchy_path: Path, child_entries: list[ChildEntry]) -> HierarchyNode:
    """Merge planned children into an existing hierarchy file.

    Existing metadata and existing children are preserved. A planned child that
    already exists with different title/order metadata is rejected as a
    conflicting definition rather than being silently rewritten.
    """
    node = load_hierarchy(hierarchy_path)
    existing_children = {child.key: child for child in node.children}
    for child in child_entries:
        existing = existing_children.get(child.key)
        if existing is None:
            node.children.append(child)
            existing_children[child.key] = child
            continue
        if existing.title != child.title or existing.order != child.order:
            raise ValueError(
                f"Conflicting child definition for issue #{child.key} in '{hierarchy_path}'. "
                "Resolve the existing hierarchy.yml entry before running nest migration."
            )
    return node


def _capture_head() -> str:
    """Return the current HEAD SHA.

    Raises:
        RuntimeError: If HEAD cannot be resolved.
    """
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        shell=False,
    )
    if result.returncode != 0 or not result.stdout.strip():
        raise RuntimeError("Could not determine the current HEAD SHA. Aborting migration.")
    return result.stdout.strip()


def _stage_specs(specs_root: str | Path) -> None:
    """Stage only the specs/ tree so unrelated changes are never committed.

    Raises:
        RuntimeError: If staging fails.
    """
    specs_relpath = _specs_repo_relative_pathspec(specs_root)
    result = subprocess.run(
        ["git", "add", "--all", "--", specs_relpath],
        capture_output=True,
        text=True,
        shell=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"git add failed for '{specs_relpath}': {result.stderr.strip()}")


def rollback_migration(pre_run_head: str, specs_root: str | Path) -> bool:
    """Roll back a failed migration to the pre-migration state.

    Performs git reset --hard to the captured HEAD SHA, then cleans
    untracked files under specs/ only.

    Args:
        pre_run_head: The git HEAD SHA before migration started.
        specs_root: Path to the specs/ directory.

    Returns:
        True when both git rollback steps succeed, else False.
    """
    reset_result = subprocess.run(
        ["git", "reset", "--hard", pre_run_head],
        capture_output=True,
        text=True,
        shell=False,
    )
    rollback_succeeded = True
    if reset_result.returncode != 0:
        rollback_succeeded = False
        print(
            f"Warning: git reset --hard failed during rollback: {reset_result.stderr.strip()}",
            file=sys.stderr,
        )

    try:
        specs_relpath = _specs_repo_relative_pathspec(specs_root)
    except RuntimeError as exc:
        rollback_succeeded = False
        print(f"Warning: could not compute specs path for git clean during rollback: {exc}", file=sys.stderr)
    else:
        clean_result = subprocess.run(
            ["git", "clean", "-fd", "--", specs_relpath],
            capture_output=True,
            text=True,
            shell=False,
        )
        if clean_result.returncode != 0:
            rollback_succeeded = False
            print(
                f"Warning: git clean failed during rollback: {clean_result.stderr.strip()}",
                file=sys.stderr,
            )

    return rollback_succeeded


def _specs_repo_relative_pathspec(specs_root: str | Path) -> str:
    """Return a repository-root-relative git pathspec for specs_root."""
    repo_root_result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        shell=False,
    )
    if repo_root_result.returncode != 0:
        failure_detail = repo_root_result.stderr.strip() or f"no error output (exit code {repo_root_result.returncode})"
        raise RuntimeError(f"git rev-parse --show-toplevel failed: {failure_detail}")

    repo_root = Path(repo_root_result.stdout.strip()).resolve()
    specs_path = Path(specs_root).resolve()
    try:
        return specs_path.relative_to(repo_root).as_posix()
    except ValueError as exc:
        raise RuntimeError(f"specs_root '{specs_path}' is outside the repository root '{repo_root}'") from exc
