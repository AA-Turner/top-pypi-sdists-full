"""Runtime hierarchy input generation and validation (FR-001, FR-014, FR-015).

Provider-verified issue relationships (delivered by the Spec Nesting
Infrastructure dependency, "Feature A") are always authoritative. This
module generates a deterministic *runtime* hierarchy input file in the
workflow state directory before each orchestration run, using those
verified relationships together with any existing on-disk
``hierarchy.yml`` metadata (see ``agentic_devtools.hierarchy.metadata_io``)
purely as a divergence check — never as a substitute for the verified
relationships.

The runtime hierarchy input file is *runtime data*, not a source-controlled
repository file: it lives under the workflow state directory and is
regenerated for every run.
"""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from agentic_devtools.hierarchy.metadata_io import read_hierarchy_yml
from agentic_devtools.hierarchy.models import HierarchyLevel


class HierarchyDiscoveryError(ValueError):
    """Raised when hierarchy relationships are invalid or ambiguous (FR-014).

    Attributes:
        reason: A short machine-stable discovery-failure reason
            (e.g. ``"cycle_detected"``, ``"duplicate_parent"``, ``"unresolved_issue"``).
    """

    def __init__(self, reason: str, message: str) -> None:
        self.reason = reason
        super().__init__(message)


_SAFE_RUN_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


@dataclass(frozen=True)
class ProviderIssueRelationship:
    """A single provider-verified issue relationship (Feature A output).

    Attributes:
        issue_key: The issue's stable key (e.g. ``"1867"`` or ``"PROJ-123"``).
        parent_key: The verified parent issue key, or ``None`` for a top-level issue.
        title: Human-readable title, for context/logging only.
        level: Provider-verified hierarchy level when available. This is
            required to distinguish a direct Epic parent from a Feature parent.
        resolvable: Whether the provider could resolve this issue at all. A
            referenced parent key that is not itself present and resolvable
            in the relationship map is treated as unresolved.
    """

    issue_key: str
    parent_key: str | None = None
    title: str = ""
    resolvable: bool = True
    level: HierarchyLevel | None = None


@dataclass(frozen=True)
class HierarchyChain:
    """The resolved epic/feature/subtask chain for one assigned issue.

    ``epic_key`` and/or ``feature_key`` may be ``None`` for reduced or
    standalone assignments (FR-003, FR-004). ``divergence_notes`` records
    any observed mismatch between the provider-verified chain and an
    existing on-disk ``hierarchy.yml``; the chain itself always reflects
    the provider-verified relationships regardless of divergence.
    """

    subtask_key: str
    feature_key: str | None = None
    epic_key: str | None = None
    divergence_notes: tuple[str, ...] = ()

    @property
    def levels_found(self) -> list[str]:
        """Return the list of hierarchy levels present in this chain, for trace records."""
        levels = ["subtask"]
        if self.feature_key is not None:
            levels.append("feature")
        if self.epic_key is not None:
            levels.append("epic")
        return levels

    @property
    def is_standalone(self) -> bool:
        """Return True when neither a feature parent nor epic grandparent was found."""
        return self.feature_key is None and self.epic_key is None

    def to_dict(self) -> dict[str, object]:
        """Serialize to a JSON-safe dict for the runtime hierarchy input file."""
        return {
            "subtask_key": self.subtask_key,
            "feature_key": self.feature_key,
            "epic_key": self.epic_key,
            "divergence_notes": list(self.divergence_notes),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> HierarchyChain:
        """Deserialize a chain previously written by ``to_dict``.

        Raises ``ValueError`` if any field has an unexpected type so that
        callers receive a controlled error instead of a silently coerced
        hierarchy (e.g. ``subtask_key: null`` becoming the string ``"None"``).
        """
        subtask_key = data.get("subtask_key")
        if not isinstance(subtask_key, str) or not subtask_key.strip():
            msg = "Invalid subtask_key in hierarchy chain data: expected non-empty non-whitespace str, got "
            raise ValueError(f"{msg}{subtask_key!r}")

        feature_key = data.get("feature_key")
        if feature_key is not None and not isinstance(feature_key, str):
            raise ValueError(f"Invalid feature_key in hierarchy chain data: expected str or None, got {feature_key!r}")
        if isinstance(feature_key, str) and not feature_key.strip():
            raise ValueError("Invalid feature_key in hierarchy chain data: expected non-empty string when provided")

        epic_key = data.get("epic_key")
        if epic_key is not None and not isinstance(epic_key, str):
            raise ValueError(f"Invalid epic_key in hierarchy chain data: expected str or None, got {epic_key!r}")
        if isinstance(epic_key, str) and not epic_key.strip():
            raise ValueError("Invalid epic_key in hierarchy chain data: expected non-empty string when provided")

        divergence_notes_raw = data.get("divergence_notes", [])
        if not isinstance(divergence_notes_raw, (list, tuple)):
            _got = type(divergence_notes_raw).__name__
            raise ValueError(f"Invalid divergence_notes in hierarchy chain data: expected list, got {_got!r}")
        for i, note in enumerate(divergence_notes_raw):
            if not isinstance(note, str):
                raise ValueError(f"Invalid divergence_notes[{i}] in hierarchy chain data: expected str, got {note!r}")

        return cls(
            subtask_key=subtask_key,
            feature_key=feature_key,
            epic_key=epic_key,
            divergence_notes=tuple(divergence_notes_raw),
        )


def discover_hierarchy_chain(
    subtask_key: str,
    relationships: Mapping[str, ProviderIssueRelationship],
    *,
    max_depth: int = 8,
) -> HierarchyChain:
    """Walk provider-verified relationships from ``subtask_key`` up to an epic.

    Args:
        subtask_key: The assigned issue's key.
        relationships: Provider-verified relationships keyed by issue key.
        max_depth: Safety bound on ancestor traversal (also used to detect
            cycles that would otherwise loop indefinitely).

    Returns:
        A ``HierarchyChain`` describing the (possibly partial) ancestry.

    Raises:
        ValueError: If ``max_depth`` is not a positive integer.
        HierarchyDiscoveryError: If a cycle, duplicate parent reference, or
            an unresolved ancestor issue is encountered.
    """
    if isinstance(max_depth, bool) or not isinstance(max_depth, int):
        raise ValueError(f"max_depth must be a positive integer, got {max_depth!r}")
    if max_depth < 1:
        raise ValueError(f"max_depth must be a positive integer, got {max_depth!r}")
    subtask = relationships.get(subtask_key)
    if subtask is None:
        raise HierarchyDiscoveryError(
            "unresolved_issue", f"Issue '{subtask_key}' is not present in provider relationships"
        )
    if not subtask.resolvable:
        raise HierarchyDiscoveryError(
            "unresolved_issue", f"Issue '{subtask_key}' could not be resolved by the provider"
        )

    visited: list[str] = [subtask_key]
    ancestors: list[str] = []
    current = subtask
    while True:
        claims = [rel.parent_key for rel in relationships.values() if rel.issue_key == current.issue_key]
        if len(set(claims)) > 1:
            raise HierarchyDiscoveryError(
                "duplicate_parent",
                f"Conflicting parent claims for '{current.issue_key}': {claims}",
            )
        if current.parent_key is None:
            break
        parent_key = current.parent_key
        if parent_key in visited:
            raise HierarchyDiscoveryError(
                "cycle_detected",
                f"Cycle detected in hierarchy ancestry starting at '{subtask_key}': {visited + [parent_key]}",
            )
        if len(visited) > max_depth:
            raise HierarchyDiscoveryError(
                "cycle_detected", f"Ancestor chain for '{subtask_key}' exceeds max_depth={max_depth}"
            )
        parent = relationships.get(parent_key)
        if parent is None or not parent.resolvable:
            raise HierarchyDiscoveryError(
                "unresolved_issue", f"Parent issue '{parent_key}' of '{visited[-1]}' could not be resolved"
            )
        visited.append(parent_key)
        ancestors.append(parent_key)
        current = parent

    if len(ancestors) > 2:
        # More than feature+epic levels is an ambiguous/unsupported depth for this feature.
        raise HierarchyDiscoveryError(
            "ambiguous_depth",
            f"Hierarchy for '{subtask_key}' has {len(ancestors)} ancestor levels; only feature+epic are supported",
        )

    chain_nodes = [subtask, *(relationships[key] for key in ancestors)]
    if len(ancestors) == 2:
        expected_levels = [HierarchyLevel.TASK, HierarchyLevel.FEATURE, HierarchyLevel.EPIC]
    elif len(ancestors) == 1 and chain_nodes[-1].level == HierarchyLevel.EPIC:
        expected_levels = [HierarchyLevel.TASK, HierarchyLevel.EPIC]
    elif len(ancestors) == 1:
        expected_levels = [HierarchyLevel.TASK, HierarchyLevel.FEATURE]
    else:
        expected_levels = []
    for node, expected_level in zip(chain_nodes, expected_levels):
        if node.level is not None and node.level is not expected_level:
            raise HierarchyDiscoveryError(
                "ambiguous_level",
                f"Issue '{node.issue_key}' declares level '{node.level.value}'; expected '{expected_level.value}'",
            )

    feature_key = ancestors[0] if len(ancestors) >= 1 else None
    epic_key = ancestors[1] if len(ancestors) >= 2 else None
    if len(ancestors) == 1 and current.level == HierarchyLevel.EPIC:
        feature_key = None
        epic_key = ancestors[0]
    return HierarchyChain(subtask_key=subtask_key, feature_key=feature_key, epic_key=epic_key)


def detect_duplicate_parent_claims(relationships: list[ProviderIssueRelationship]) -> list[str]:
    """Return issue keys claimed with two different parents by distinct relationship records.

    Provider responses are ordinarily de-duplicated into a single mapping
    before use; this helper accepts the raw list of relationship records
    (which may legitimately contain more than one entry for the same issue
    key when merging multiple provider queries) and flags any issue key for
    which two records disagree on the parent. This signals inconsistent
    provider data (FR-014) rather than a legitimate hierarchy and MUST stop
    the affected path.
    """
    seen: dict[str, str | None] = {}
    duplicates: list[str] = []
    for rel in relationships:
        key = rel.issue_key
        if key in seen and seen[key] != rel.parent_key:
            if key not in duplicates:
                duplicates.append(key)
        seen[key] = rel.parent_key
    return duplicates


def _spec_dir_hierarchy_yml(spec_dir: Path) -> Path:
    return spec_dir / "hierarchy.yml"


def compute_divergence(chain: HierarchyChain, spec_dir: Path | None) -> tuple[str, ...]:
    """Compare a provider-verified chain against an on-disk ``hierarchy.yml``, if any.

    The provider-verified ``chain`` remains authoritative regardless of the
    outcome; this only produces human-readable divergence notes to record
    in the runtime hierarchy input and in the ``hierarchy_discovery`` trace
    event.
    """
    if spec_dir is None:
        return ()
    yml_path = _spec_dir_hierarchy_yml(spec_dir)
    if not yml_path.exists():
        return ("hierarchy.yml is missing; using provider-verified relationships only",)
    try:
        metadata = read_hierarchy_yml(yml_path)
    except (FileNotFoundError, ValueError) as exc:
        return (f"hierarchy.yml could not be parsed: {exc}",)

    notes: list[str] = []
    on_disk_parent = str(metadata.parent) if metadata.parent is not None else None
    verified_parent = (chain.feature_key or chain.epic_key) if metadata.level == HierarchyLevel.TASK else None
    if metadata.level == HierarchyLevel.TASK and on_disk_parent != verified_parent:
        notes.append(
            f"hierarchy.yml parent '{on_disk_parent}' diverges from provider-verified parent '{verified_parent}'"
        )
    return tuple(notes)


def generate_runtime_hierarchy_input(
    state_dir: Path,
    run_id: str,
    chain: HierarchyChain,
) -> Path:
    """Write the runtime hierarchy input file for one orchestration run.

    The file is written under ``<state_dir>/orchestration/hierarchy/<run_id>/``
    and is treated as ephemeral runtime data: it is regenerated for every
    run and MUST NOT be relied upon by any other run.

    Returns:
        The path to the written runtime hierarchy input file.
    """
    if not _SAFE_RUN_ID_RE.fullmatch(run_id):
        raise ValueError("run_id must be a single safe filesystem path segment")
    run_dir = state_dir / "orchestration" / "hierarchy" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    input_path = run_dir / "runtime-hierarchy-input.json"
    input_path.write_text(json.dumps(chain.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return input_path


def read_runtime_hierarchy_input(input_path: Path) -> HierarchyChain:
    """Read a previously generated runtime hierarchy input file."""
    data = json.loads(input_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(
            f"Runtime hierarchy input file must contain a JSON object, got {type(data).__name__!r}: {input_path}"
        )
    return HierarchyChain.from_dict(data)


@dataclass(frozen=True)
class DiscoveryResult:
    """The outcome of a full hierarchy discovery + runtime input generation pass."""

    outcome: str  # "success" | "partial" | "failed"
    chain: HierarchyChain | None
    error: str | None = None
    input_path: Path | None = None


def run_discovery(
    subtask_key: str,
    relationships: Mapping[str, ProviderIssueRelationship],
    *,
    state_dir: Path,
    run_id: str,
    spec_dir: Path | None = None,
) -> DiscoveryResult:
    """Discover the hierarchy for ``subtask_key`` and generate the runtime input file.

    This is the single Phase-1 entry point combining ``discover_hierarchy_chain``,
    ``compute_divergence``, and ``generate_runtime_hierarchy_input``. On
    discovery failure (FR-014), no runtime input file is written and the
    ``outcome`` is ``"failed"``.
    """
    duplicates = detect_duplicate_parent_claims(list(relationships.values()))
    if subtask_key in duplicates:
        return DiscoveryResult(outcome="failed", chain=None, error=f"duplicate_parent: {subtask_key}")

    try:
        chain = discover_hierarchy_chain(subtask_key, relationships)
    except HierarchyDiscoveryError as exc:
        return DiscoveryResult(outcome="failed", chain=None, error=f"{exc.reason}: {exc}")

    divergence = compute_divergence(chain, spec_dir)
    if divergence:
        chain = HierarchyChain(
            subtask_key=chain.subtask_key,
            feature_key=chain.feature_key,
            epic_key=chain.epic_key,
            divergence_notes=divergence,
        )

    input_path = generate_runtime_hierarchy_input(state_dir, run_id, chain)
    # A fully standalone chain (FR-004) and a complete epic+feature+subtask
    # chain are both "success": they are the expected shapes, not degraded
    # ones. Any other shape (feature-only, or divergence from an existing
    # hierarchy.yml) is reported as "partial" so degradation can be recorded.
    is_complete = chain.epic_key is not None and chain.feature_key is not None
    outcome = "success" if (chain.is_standalone or is_complete) and not divergence else "partial"
    return DiscoveryResult(outcome=outcome, chain=chain, error=None, input_path=input_path)
