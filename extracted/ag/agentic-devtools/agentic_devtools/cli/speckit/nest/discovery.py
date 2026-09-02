"""Flat spec discovery and relationship graph assembly for the nest command.

Scans the specs/ directory for flat spec directories matching the
{number}-{slug}/ pattern, indexes already-nested numeric target directories,
and builds a parent-child relationship graph by querying the GitHub API.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from agentic_devtools.hierarchy.github_detector import GitHubHierarchyDetector

#: Maximum directory depth (relative to specs_root) traversed when scanning.
#: ``specs/{epic}/{feature}/{task}`` is depth 3.
MAX_SCAN_DEPTH = 3

#: Number of issues whose metadata is fetched per batch, bounding the API
#: request burst for large spec sets (NFR-001).
BATCH_SIZE = 25

# Matches "HTTP 404" / "404" / "not found" signals from the gh CLI.
_NOT_FOUND_RE = re.compile(r"\b(?:HTTP )?404\b|not found", re.IGNORECASE)

_FLAT_SPEC_PATTERN = re.compile(r"^(\d+)-(.+)$")
_NUMERIC_DIR_PATTERN = re.compile(r"^\d+$")


@dataclass
class FlatSpec:
    """Represents a discovered flat spec directory.

    Attributes:
        issue_number: The issue number extracted from the directory name.
        path: The full path to the spec directory.
        slug: The slug portion of the directory name.
    """

    issue_number: int
    path: Path
    slug: str


@dataclass(frozen=True)
class ChildRef:
    """An ordered child reference discovered from the GitHub API.

    Attributes:
        number: The child issue number.
        title: The exact human-readable GitHub issue title.
        order: The child's position in the GitHub API response, or ``None``
            when ordering could not be determined.
    """

    number: int
    title: str
    order: int | None = None


#: Mapping of issue number -> (parent issue number or ``None``, ordered children).
RelationshipGraph = dict[int, tuple[int | None, list[ChildRef]]]


@dataclass
class RelationshipDiscovery:
    """Result of assembling the relationship graph.

    Attributes:
        graph: The assembled relationship graph.
        warnings: Recoverable warnings (e.g. missing/deleted issues).
    """

    graph: RelationshipGraph = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)


def extract_issue_number(directory_name: str) -> int | None:
    """Extract the leading issue number from a ``{number}-{slug}`` directory name.

    Args:
        directory_name: The directory name to parse.

    Returns:
        The leading issue number, or ``None`` when the name does not follow the
        ``{number}-{slug}`` pattern (e.g. a slug-only name or a purely numeric
        nested directory).
    """
    match = _FLAT_SPEC_PATTERN.match(directory_name)
    if match is None:
        return None
    return int(match.group(1))


def scan_flat_specs(specs_root: str | Path, max_depth: int = MAX_SCAN_DEPTH) -> list[FlatSpec]:
    """Scan the specs/ tree for flat spec directories.

    Matches directories with the ``{number}-{slug}/`` naming pattern at any
    depth up to ``max_depth`` (relative to ``specs_root``), so specs left flat
    inside a partially migrated hierarchy are still discovered. Directories
    whose name is purely numeric are already-nested hierarchy nodes: they are
    traversed as containers but never reported as migration candidates.
    Non-matching directory names are also traversed as containers so mixed
    legacy layouts can still expose flat descendants. A flat-spec directory
    containing another flat-spec directory or a numeric nested target is
    rejected because planning both would create overlapping or ambiguous
    migrations.

    Args:
        specs_root: Path to the specs/ directory.
        max_depth: Maximum traversal depth relative to ``specs_root``.

    Returns:
        List of FlatSpec objects, ordered by path.

    Raises:
        ValueError: If ``max_depth`` is not a positive integer, duplicate flat
            spec directories are discovered for the same issue number, or a
            flat-spec directory contains nested flat-spec or numeric-target
            descendants.
    """
    if max_depth <= 0:
        raise ValueError(f"max_depth must be a positive integer, got: {max_depth}")

    specs_path = Path(specs_root)
    flat_specs: list[FlatSpec] = []
    seen_issue_paths: dict[int, Path] = {}

    if not specs_path.is_dir():
        return flat_specs

    def _walk(directory: Path, depth: int) -> None:
        if depth > max_depth:
            return
        for entry in sorted(directory.iterdir()):
            if entry.is_symlink():
                continue
            if not entry.is_dir():
                continue
            match = _FLAT_SPEC_PATTERN.match(entry.name)
            if match:
                issue_number = int(match.group(1))
                duplicate_path = seen_issue_paths.get(issue_number)
                if duplicate_path is not None:
                    raise ValueError(
                        "Found duplicate flat spec directories for the same issue number: "
                        f"{duplicate_path} and {entry} both map to #{issue_number}. "
                        "Resolve the duplicate sources before running nest."
                    )
                seen_issue_paths[issue_number] = entry
                flat_specs.append(
                    FlatSpec(
                        issue_number=issue_number,
                        path=entry,
                        slug=match.group(2),
                    )
                )
                nested_candidates: list[Path] = []
                nested_numeric_targets: list[Path] = []

                def _find_nested_candidates(candidate_dir: Path, candidate_depth: int) -> None:
                    if candidate_depth > max_depth:
                        return
                    for child in sorted(candidate_dir.iterdir()):
                        if child.is_symlink() or not child.is_dir():
                            continue
                        if _FLAT_SPEC_PATTERN.match(child.name):
                            nested_candidates.append(child)
                        elif _NUMERIC_DIR_PATTERN.match(child.name):
                            nested_numeric_targets.append(child)
                        else:
                            _find_nested_candidates(child, candidate_depth + 1)

                _find_nested_candidates(entry, depth + 1)
                if nested_candidates:
                    raise ValueError(
                        "Found overlapping flat spec directories: "
                        f"{entry} contains {nested_candidates[0]}. "
                        "Separate the sources before running nest."
                    )
                if nested_numeric_targets:
                    raise ValueError(
                        "Found mixed flat and nested spec directories: "
                        f"{entry} contains nested target {nested_numeric_targets[0]}. "
                        "Materialize or relocate the nested hierarchy before running nest."
                    )
                continue
            _walk(entry, depth + 1)

    _walk(specs_path, 1)
    return flat_specs


def scan_existing_targets(specs_root: str | Path, max_depth: int = MAX_SCAN_DEPTH) -> dict[int, Path]:
    """Index already-migrated nested target directories.

    Walks the specs/ tree collecting directories whose name is purely numeric.
    These represent specs that a previous (possibly partial) migration run has
    already relocated, so they must not be moved again. Numeric directories
    nested under any non-numeric container are skipped because they are not
    canonical hierarchy targets and would later break ancestor resolution.

    Args:
        specs_root: Path to the specs/ directory.
        max_depth: Maximum traversal depth relative to ``specs_root``.

    Returns:
        Mapping of issue number -> existing nested directory path.

    Raises:
        ValueError: If ``max_depth`` is not a positive integer, or duplicate
            nested target directories are found for the same issue number.
    """
    if max_depth <= 0:
        raise ValueError(f"max_depth must be a positive integer, got: {max_depth}")

    specs_path = Path(specs_root)
    targets: dict[int, Path] = {}

    if not specs_path.is_dir():
        return targets

    def _walk(directory: Path, depth: int, *, numeric_ancestors_only: bool) -> None:
        if depth > max_depth:
            return
        for entry in sorted(directory.iterdir()):
            if entry.is_symlink():
                continue
            if not entry.is_dir():
                continue
            is_numeric = _NUMERIC_DIR_PATTERN.match(entry.name) is not None
            if is_numeric and numeric_ancestors_only:
                issue_number = int(entry.name)
                duplicate_path = targets.get(issue_number)
                if duplicate_path is not None and duplicate_path != entry:
                    raise ValueError(
                        "Found duplicate nested target directories for the same issue number: "
                        f"{duplicate_path} and {entry} both map to #{issue_number}. "
                        "Resolve the duplicate nested targets before running nest."
                    )
                targets[issue_number] = entry
            _walk(entry, depth + 1, numeric_ancestors_only=numeric_ancestors_only and is_numeric)

    _walk(specs_path, 1, numeric_ancestors_only=True)
    return targets


def build_relationship_graph(owner: str, repo: str, flat_specs: list[FlatSpec]) -> RelationshipDiscovery:
    """Build a parent-child relationship graph from the GitHub API.

    Issue metadata is fetched in bounded batches (:data:`BATCH_SIZE`) so a
    large spec set does not issue an unbounded burst of API calls.  A per-issue
    "not found" (404) response is recoverable: a warning is recorded and the
    spec is omitted from the graph so it remains flat.  Any other failure — for
    example an authentication/permission error — propagates so the run fails
    fast.  Rate-limit backoff is handled inside the detector layer.

    Child ordering from the GitHub API response is preserved.  When a child
    carries no explicit order value, a warning is recorded and the response
    position is used instead.

    Args:
        owner: GitHub repository owner.
        repo: GitHub repository name.
        flat_specs: List of flat spec directories to query.

    Returns:
        A :class:`RelationshipDiscovery` holding the graph and any warnings.

    Raises:
        Exception: Propagates repository-wide detector failures unchanged.
    """
    result = RelationshipDiscovery()
    if not flat_specs:
        return result

    detector = GitHubHierarchyDetector(owner, repo)

    # Validate repository access once before issuing per-issue queries.
    # A repo-level 404 or auth failure (wrong name, private repo, or bad token)
    # would otherwise manifest as per-issue 404 warnings and silently yield an
    # empty plan instead of a clear actionable failure.
    detector.validate_repository_access()

    for batch in _batched(flat_specs, BATCH_SIZE):
        for spec in batch:
            try:
                metadata = detector.build_metadata(spec.issue_number)
            except Exception as exc:
                exc_str = str(exc)
                if _NOT_FOUND_RE.search(exc_str):
                    result.warnings.append(
                        f"Issue #{spec.issue_number} was not found on GitHub. "
                        f"'{spec.path.name}' will remain at its current location."
                    )
                    continue
                raise

            children, ordering_ambiguous = _collect_children(metadata)
            if ordering_ambiguous:
                result.warnings.append(
                    f"Issue #{spec.issue_number} children carry no explicit ordering; "
                    "the GitHub API response order is used."
                )
            result.graph[spec.issue_number] = (metadata.parent, children)

    return result


def _collect_children(metadata: object) -> tuple[list[ChildRef], bool]:
    """Collect ordered, de-duplicated children from detector metadata.

    Only ``children`` (direct children within the depth cap) are included.
    ``informational_children`` are children beyond the three-level cap whose
    directories remain flat; they MUST NOT be added to graph edges or they
    would appear in ``hierarchy.yml`` referencing non-nested paths.

    Args:
        metadata: A ``HierarchyMetadata`` instance from the detector.

    Returns:
        Tuple of (ordered children, ordering-was-ambiguous flag).
    """
    direct = list(getattr(metadata, "children", []))

    children: list[ChildRef] = []
    seen: set[int] = set()
    ambiguous = False

    for position, child in enumerate(direct):
        if child.number in seen:
            continue
        seen.add(child.number)
        if child.order is None:
            ambiguous = True
            order = position
        else:
            order = child.order
        children.append(ChildRef(number=child.number, title=child.title, order=order))

    # A single child has no ordering ambiguity worth reporting.
    return children, ambiguous and len(children) > 1


def _batched(items: list[FlatSpec], size: int) -> list[list[FlatSpec]]:
    """Split ``items`` into consecutive batches of at most ``size`` entries."""
    return [items[index : index + size] for index in range(0, len(items), size)]
