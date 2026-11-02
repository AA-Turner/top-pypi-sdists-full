"""Migration plan computation for the nest command.

Computes the target directory layout from the relationship graph, with cycle
detection, multi-parent resolution, depth-cap enforcement, scope filtering,
and consultation of the existing-target index produced by a previous
(possibly partial) migration run.
"""

from __future__ import annotations

import collections
from dataclasses import dataclass, field
from pathlib import Path

from agentic_devtools.cli.speckit.shared.conflict_check import Move

from .discovery import ChildRef, FlatSpec, RelationshipGraph

#: Maximum hierarchy depth: Epic(0) → Feature(1) → Task(2).
MAX_HIERARCHY_DEPTH = 3


@dataclass
class MigrationPlan:
    """Represents the computed migration plan.

    Attributes:
        moves: List of directory moves to execute.
        hierarchy_files: Mapping of target directory path -> ordered child
            references, used to write ``hierarchy.yml`` files with the exact
            GitHub child titles and API ordering.
        scope_hierarchy_files: Optional complete hierarchy mapping used for
            commit-scope resolution when ``hierarchy_files`` is filtered for
            execution.
        excluded_cycles: List of sets of issue numbers in cyclic groups.
        multi_parent_selections: Mapping of issue number -> selected parent for
            issues with multiple candidate parents.
        multi_parent_candidates: Mapping of issue number -> every candidate
            parent considered, so the display layer can name them all.
        remaining_flat: Flat specs that stay at their current location (no
            discovered relationships, or blocked by the depth cap).
        warnings: List of warning messages.
    """

    moves: list[Move] = field(default_factory=list)
    hierarchy_files: dict[str, list[ChildRef]] = field(default_factory=dict)
    scope_hierarchy_files: dict[str, list[ChildRef]] | None = None
    excluded_cycles: list[set[int]] = field(default_factory=list)
    multi_parent_selections: dict[int, int] = field(default_factory=dict)
    multi_parent_candidates: dict[int, list[int]] = field(default_factory=dict)
    remaining_flat: list[FlatSpec] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    existing_root_issues: set[int] = field(default_factory=set)

    @property
    def roots(self) -> list[int]:
        """Return the issue numbers of hierarchy roots for this migration.

        Includes flat-spec roots (moved specs that are not children of any
        other moved spec) and existing-target roots recorded in
        :attr:`existing_root_issues` (already-nested parents whose flat
        descendants are being migrated in a partial-migration run).
        """
        moved = {move.issue_number for move in self.moves}
        hierarchy_files = self.scope_hierarchy_files
        if hierarchy_files is None:
            hierarchy_files = self.hierarchy_files
        children = {child.number for children in hierarchy_files.values() for child in children}
        flat_roots = moved - children
        return sorted(flat_roots | (self.existing_root_issues - children))


def detect_cycles(graph: RelationshipGraph) -> list[set[int]]:
    """Detect cycles in the parent-child relationship graph using DFS.

    Args:
        graph: Mapping of issue_number -> (parent, ordered children).

    Returns:
        List of sets, each set containing issue numbers in a cyclic group.
    """
    visited: set[int] = set()
    in_stack: set[int] = set()
    cycles: list[set[int]] = []

    children_map: dict[int, list[int]] = {}
    for issue, (_, children) in graph.items():
        children_map[issue] = [child.number for child in children if child.number in graph]

    def dfs(node: int, path: list[int]) -> None:
        if node in in_stack:
            cycle_start = path.index(node)
            cycle = set(path[cycle_start:])
            if not any(cycle == existing for existing in cycles):
                cycles.append(cycle)
            return
        if node in visited:
            return

        visited.add(node)
        in_stack.add(node)
        path.append(node)

        for child in children_map.get(node, []):
            dfs(child, path)

        path.pop()
        in_stack.discard(node)

    for issue in graph:
        if issue not in visited:
            dfs(issue, [])

    return cycles


def resolve_multi_parent(graph: RelationshipGraph) -> dict[int, int]:
    """Resolve multi-parent conflicts by selecting the lowest-numbered parent.

    When an issue appears as a child of multiple parents in the graph, the
    lowest-numbered parent is selected as the canonical one.

    Args:
        graph: Mapping of issue_number -> (parent, ordered children).

    Returns:
        Mapping of issue_number -> selected_parent, containing only issues
        that actually had more than one candidate parent.
    """
    child_parents = _build_child_parents(graph)

    selections: dict[int, int] = {}
    for child, parents in child_parents.items():
        if len(parents) > 1:
            selections[child] = min(parents)

    return selections


def compute_migration_plan(
    graph: RelationshipGraph,
    flat_specs: list[FlatSpec],
    specs_root: str | Path,
    scope: int | None = None,
    existing_targets: dict[int, Path] | None = None,
) -> MigrationPlan:
    """Compute the migration plan from the flat to the nested layout.

    Respects the depth cap of three levels (Epic=0, Feature=1, Task=2), skips
    cyclic groups, and consults the existing-target index so an ancestor that a
    previous run already relocated is treated as in place while its remaining
    flat descendants are still placed beneath it.

    This is a pure builder: it never exits the process.  When ``scope`` matches
    no specs, an empty plan is returned and the caller decides how to report it.

    Args:
        graph: Relationship graph from ``build_relationship_graph()``.
        flat_specs: List of FlatSpec objects from ``scan_flat_specs()``.
        specs_root: Path to the specs/ directory.
        scope: Optional issue number limiting migration to that issue and its
            transitive descendants (the scoped root itself is included).
        existing_targets: Mapping of issue number -> already-nested directory
            path, from ``scan_existing_targets()``.

    Returns:
        MigrationPlan describing all operations to perform.
    """
    specs_path = Path(specs_root)
    existing = dict(existing_targets or {})
    plan = MigrationPlan()

    spec_map: dict[int, FlatSpec] = {spec.issue_number: spec for spec in flat_specs}

    cycles = detect_cycles(graph)
    plan.excluded_cycles = cycles
    cyclic_issues: set[int] = set()
    for cycle in cycles:
        cyclic_issues.update(cycle)
        plan.warnings.append(
            f"Cyclic relationship detected among issues {sorted(cycle)}. These specs are excluded from migration."
        )

    child_parents = _build_child_parents(graph)

    in_scope = _resolve_scope(graph, scope, existing, specs_path)

    plan.multi_parent_candidates, plan.multi_parent_selections = _resolve_parent_candidates(child_parents, in_scope)

    canonical_parent = _resolve_canonical_parents(graph, plan, in_scope, scope, cyclic_issues)

    for issue in sorted(in_scope):
        if issue in cyclic_issues or issue not in spec_map:
            continue

        spec = spec_map[issue]
        parent = canonical_parent.get(issue)
        children = graph.get(issue, (None, []))[1]
        has_local_children = any(
            child.number in in_scope
            and child.number in graph
            and (child.number in spec_map or child.number in existing)
            for child in children
        )
        parent_is_local = parent is not None and (parent in spec_map or parent in existing)
        if not parent_is_local and not has_local_children:
            # No local hierarchy can be materialized yet: this issue has no
            # in-scope parent with a local presence and no locally present children.
            plan.remaining_flat.append(spec)
            continue

        ancestors = _get_ancestors(canonical_parent, issue, existing, specs_path, max_depth=MAX_HIERARCHY_DEPTH - 1)
        if ancestors is None:
            plan.remaining_flat.append(spec)
            plan.warnings.append(
                f"Issue #{issue} exceeds the {MAX_HIERARCHY_DEPTH}-level depth cap. "
                f"'{spec.path.name}' remains at its current location."
            )
            continue

        # Strip leading non-local ancestors to avoid creating orphan container
        # directories when a local subtree's top issue has a non-local GitHub parent.
        # Skip stripping when the chain was reconstructed from an already-nested path
        # (nearest ancestor in existing) — those parts form a valid existing layout.
        if not (ancestors and ancestors[-1] in existing):
            while ancestors and ancestors[0] not in spec_map and ancestors[0] not in existing:
                ancestors = ancestors[1:]

        target = _target_path(specs_path, ancestors, issue, existing)
        if spec.path == target:
            continue
        plan.moves.append(Move(source=spec.path, target=target, issue_number=issue))

    # Specs with no discovered relationship at all stay exactly where they are.
    for spec in flat_specs:
        if spec.issue_number in cyclic_issues:
            continue
        if spec.issue_number in graph:
            continue
        if any(existing_spec is spec for existing_spec in plan.remaining_flat):
            continue
        plan.remaining_flat.append(spec)

    plan.hierarchy_files = _compute_hierarchy_files(
        graph, canonical_parent, in_scope, cyclic_issues, existing, specs_path, spec_map, plan
    )

    _validate_existing_target_positions(plan.hierarchy_files, existing)

    return plan


def _resolve_scope(
    graph: RelationshipGraph,
    scope: int | None,
    existing: dict[int, Path] | None = None,
    specs_path: Path | None = None,
) -> set[int]:
    """Return the set of in-scope issue numbers for the plan.

    When ``scope`` is provided, the result includes ``scope`` itself plus all
    transitive descendants found via three complementary traversals:

    1. **Children-list traversal** (via ``collect_descendants``): walks each
       graph entry's ``children`` list.  This covers issues that are both flat
       specs *and* have their children listed in the graph.
    2. **Existing-target traversal**: adds already-nested issues whose path is
       below the scoped issue's directory (e.g. ``specs/10/20/`` is a nested
       descendant of scope 10).  This seeds the reverse traversal below so that
       flat specs with a parent that is already nested are discovered even when
       that parent has no flat-spec graph entry.
    3. **Parent-edge traversal**: scans graph entries whose ``parent`` field
       points to a node in the current in-scope set.  This covers flat specs
       whose parent is an already-nested node that is absent from ``graph``
       (e.g. ``specs/10/`` already exists; flat spec 20 has ``parent=10`` in
       the graph but 10 has no graph entry).

    The three traversals together ensure that ``--scope 10`` correctly discovers
    all flat specs descending from issue 10, including those below already-nested
    intermediate directories.
    """
    if scope is None:
        return set(graph.keys())

    # Forward traversal via children lists
    in_scope = collect_descendants(graph, scope)
    in_scope.add(scope)

    # Existing-target traversal: add already-nested descendants of scope so the
    # reverse traversal below can discover flat specs parented under them.
    if existing and specs_path:
        for issue_num, nested_path in existing.items():
            if issue_num in in_scope:
                continue
            try:
                rel_parts = nested_path.relative_to(specs_path).parts
            except ValueError:
                continue
            if str(scope) in rel_parts:
                in_scope.add(issue_num)
                queue_seed = collections.deque([issue_num])
                while queue_seed:
                    current_existing = queue_seed.popleft()
                    for other_num, other_path in existing.items():
                        if other_num in in_scope:
                            continue
                        try:
                            other_parts = other_path.relative_to(specs_path).parts
                        except ValueError:
                            continue
                        if str(current_existing) in other_parts:
                            in_scope.add(other_num)
                            queue_seed.append(other_num)

    # Reverse traversal via parent edges — handles already-nested ancestors
    # that are absent from graph but referenced as parent by flat specs.
    parent_to_children: dict[int, list[int]] = {}
    for issue, (parent, _) in graph.items():
        if parent is not None:
            parent_to_children.setdefault(parent, []).append(issue)

    queue: collections.deque[int] = collections.deque(in_scope)
    while queue:
        current = queue.popleft()
        for child in parent_to_children.get(current, []):
            if child not in in_scope:
                in_scope.add(child)
                queue.append(child)

    return in_scope


def _resolve_parent_candidates(
    child_parents: dict[int, list[int]], in_scope: set[int]
) -> tuple[dict[int, list[int]], dict[int, int]]:
    """Compute candidate parents and the lowest-numbered selection per child."""
    candidates: dict[int, list[int]] = {}
    selections: dict[int, int] = {}
    for issue, parents in child_parents.items():
        if issue not in in_scope:
            continue
        scoped_parents = sorted(parent for parent in parents if parent in in_scope)
        if len(scoped_parents) > 1:
            candidates[issue] = scoped_parents
            selections[issue] = scoped_parents[0]
    return candidates, selections


def _resolve_canonical_parents(
    graph: RelationshipGraph,
    plan: MigrationPlan,
    in_scope: set[int],
    scope: int | None,
    cyclic_issues: set[int],
) -> dict[int, int | None]:
    """Determine the single canonical parent for every in-scope issue."""
    canonical_parent: dict[int, int | None] = {}
    for issue in sorted(in_scope):
        if issue in cyclic_issues:
            continue
        if issue in plan.multi_parent_selections:
            selected = plan.multi_parent_selections[issue]
            canonical_parent[issue] = selected
            plan.warnings.append(
                f"Issue #{issue} has multiple candidate parents "
                f"{plan.multi_parent_candidates[issue]}; selected #{selected} (lowest-numbered)."
            )
            continue

        parent_from_graph = graph.get(issue, (None, []))[0]
        if parent_from_graph is None or scope is None or parent_from_graph in in_scope:
            canonical_parent[issue] = parent_from_graph
            continue

        canonical_parent[issue] = None
        plan.warnings.append(
            f"Issue #{issue} has parent #{parent_from_graph} outside the scoped migration set. "
            "It will be placed at the scope root."
        )
    return canonical_parent


def _compute_hierarchy_files(
    graph: RelationshipGraph,
    canonical_parent: dict[int, int | None],
    in_scope: set[int],
    cyclic_issues: set[int],
    existing: dict[int, Path],
    specs_path: Path,
    spec_map: dict[int, FlatSpec],
    plan: MigrationPlan,
) -> dict[str, list[ChildRef]]:
    """Compute the hierarchy.yml payload for every parent directory.

    Child ordering and titles come straight from the GitHub API metadata, so
    no numeric re-sorting is applied.
    """
    hierarchy_files: dict[str, list[ChildRef]] = {}

    parent_children: dict[int, list[int]] = {}
    for issue in sorted(in_scope):
        if issue in cyclic_issues:
            continue
        parent = canonical_parent.get(issue)
        # Accept parents that are either in the flat-spec scope (still to be
        # moved) or already nested (present in existing_targets).  The latter
        # handles unscoped runs and --scope N where N is already a nested dir.
        if parent is not None and (parent in in_scope or parent in existing):
            parent_children.setdefault(parent, []).append(issue)

    for parent_issue, child_issues in sorted(parent_children.items()):
        ancestors = _get_ancestors(
            canonical_parent, parent_issue, existing, specs_path, max_depth=MAX_HIERARCHY_DEPTH - 1
        )
        if ancestors is None:
            continue
        # Strip leading non-local ancestors to avoid creating orphan container
        # directories when the parent's own ancestry chain reaches a non-local issue.
        if not (ancestors and ancestors[-1] in existing):
            while ancestors and ancestors[0] not in spec_map and ancestors[0] not in existing:
                ancestors = ancestors[1:]
        parent_dir = _target_path(specs_path, ancestors, parent_issue, existing)
        if parent_issue not in spec_map and parent_issue not in existing:
            continue

        ordered = [child for child in graph.get(parent_issue, (None, []))[1] if child.number in set(child_issues)]
        known = {child.number for child in ordered}
        for missing in sorted(number for number in child_issues if number not in known):
            ordered.append(ChildRef(number=missing, title=f"Issue #{missing}", order=None))
            plan.warnings.append(
                f"Issue #{missing} has no GitHub title metadata; a placeholder title is used in hierarchy.yml."
            )
        hierarchy_files[str(parent_dir)] = ordered
        # Record already-nested parents as "existing roots" so resolve_commit_scope
        # can infer the correct commit scope for partial-migration runs.
        if parent_issue not in spec_map and parent_issue in existing:
            plan.existing_root_issues.add(parent_issue)

    return hierarchy_files


def collect_descendants(graph: RelationshipGraph, root: int) -> set[int]:
    """Collect all transitive descendants of a root issue.

    Args:
        graph: Mapping of issue_number -> (parent, ordered children).
        root: The root issue number.

    Returns:
        Set of descendant issue numbers (excluding ``root`` itself).
    """
    descendants: set[int] = set()
    queue: collections.deque[int] = collections.deque([root])
    while queue:
        current = queue.popleft()
        _, children = graph.get(current, (None, []))
        for child in children:
            if child.number in graph and child.number not in descendants:
                descendants.add(child.number)
                queue.append(child.number)
    return descendants


def get_ancestors(
    canonical_parent: dict[int, int | None],
    issue: int,
    max_depth: int = MAX_HIERARCHY_DEPTH - 1,
) -> list[int] | None:
    """Return the ancestor chain (root first) for an issue.

    Args:
        canonical_parent: Mapping of issue number -> canonical parent.
        issue: The issue whose ancestors are requested.
        max_depth: Maximum number of ancestors allowed by the depth cap.

    Returns:
        Ancestor chain in root-first order, or ``None`` when the chain is
        longer than ``max_depth`` (i.e. the depth cap is exceeded).

    Raises:
        ValueError: If ``max_depth`` is negative.
    """
    if max_depth < 0:
        raise ValueError(f"max_depth must be non-negative, got: {max_depth}")

    ancestors: list[int] = []
    current = canonical_parent.get(issue)
    seen: set[int] = {issue}
    while current is not None:
        if current in seen:
            break
        if len(ancestors) >= max_depth:
            return None
        ancestors.append(current)
        seen.add(current)
        current = canonical_parent.get(current)
    ancestors.reverse()
    return ancestors


def _get_ancestors(
    canonical_parent: dict[int, int | None],
    issue: int,
    existing: dict[int, Path],
    specs_path: Path,
    max_depth: int,
) -> list[int] | None:
    """Ancestor chain resolution that also honours already-nested ancestors.

    When the nearest ancestor already exists in the nested layout, its known
    on-disk depth is used so a partially migrated tree still yields a correct
    (and depth-capped) target path.
    """
    chain = get_ancestors(canonical_parent, issue, max_depth=max_depth)
    if chain is None:
        return None
    if not chain:
        return chain

    nearest = chain[-1]
    existing_path = existing.get(nearest)
    if existing_path is None:
        return chain

    try:
        parts = existing_path.relative_to(specs_path).parts
    except ValueError:
        return chain

    if len(parts) > max_depth:
        return None
    return [int(part) for part in parts]


def _target_path(specs_path: Path, ancestors: list[int], issue: int, existing: dict[int, Path]) -> Path:
    """Compute the target directory for an issue given its ancestor chain."""
    existing_path = existing.get(issue)
    if existing_path is not None:
        return existing_path
    return specs_path.joinpath(*[str(ancestor) for ancestor in ancestors], str(issue))


def _validate_existing_target_positions(
    hierarchy_files: dict[str, list[ChildRef]],
    existing: dict[int, Path],
) -> None:
    """Validate that each existing child target is nested under its hierarchy parent.

    When a child issue has an already-migrated directory (in *existing*), that
    directory must sit at ``<parent_dir>/<child_number>/``.  If it does not, the
    hierarchy file would reference a child that lives at a different location,
    producing an internally inconsistent tree.

    Args:
        hierarchy_files: Mapping of parent directory path string ->
            ordered child references (as returned by ``_compute_hierarchy_files``).
        existing: Mapping of issue number -> already-nested directory path.

    Raises:
        ValueError: If any existing child target is at the wrong location.
    """
    for parent_dir_str, children in hierarchy_files.items():
        parent_path = Path(parent_dir_str)
        for child_ref in children:
            child_existing = existing.get(child_ref.number)
            if child_existing is None:
                continue
            expected = parent_path / str(child_ref.number)
            if child_existing != expected:
                raise ValueError(
                    f"Existing target #{child_ref.number} is at '{child_existing}' but "
                    f"must be at '{expected}' (as a child of '{parent_path}'). "
                    "Relocate the existing target to its canonical nested position "
                    "before running nest."
                )


def _build_child_parents(graph: RelationshipGraph) -> dict[int, list[int]]:
    """Build a reverse map of child issue number to candidate parents."""
    child_parents: dict[int, list[int]] = {}
    for issue, (_, children) in graph.items():
        for child in children:
            if child.number not in graph:
                continue
            child_parents.setdefault(child.number, []).append(issue)
    return child_parents
