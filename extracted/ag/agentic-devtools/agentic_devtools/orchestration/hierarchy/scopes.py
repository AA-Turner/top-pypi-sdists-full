"""Validated scope models for hierarchy orchestration agents.

Defines the immutable, mechanically enforced scope declarations used to
create Epic, Feature, and Subtask agents (FR-010). A ``ScopeAgent`` is the
single source of truth for what an agent may evaluate, modify, and review;
dynamically injected context (see ``context.py``) is layered on top of a
scope but can never widen it.

Key invariants (FR-010):

- Every agent scope is immutable once constructed (frozen dataclasses).
- Only ``AgentScopeLevel.SUBTASK`` scopes may declare a non-empty writable
  file boundary; ``EPIC`` and ``FEATURE`` scopes are always review-only.
- File boundaries are repository-relative POSIX paths; a boundary can only
  ever be narrowed by construction, never widened at runtime.
"""

from __future__ import annotations

import posixpath
import re
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class AgentScopeLevel(StrEnum):
    """The hierarchy level of a spawned scope agent.

    ``ORCHESTRATOR`` is not a spawned agent; it is used to attribute trace
    events (FR-012) that originate from the orchestrator itself rather than
    from any single spawned agent (for example ``file_boundary_established``).
    """

    EPIC = "epic"
    FEATURE = "feature"
    SUBTASK = "subtask"
    ORCHESTRATOR = "orchestrator"


class ReviewVerdict(StrEnum):
    """Possible outcomes of a higher-level review decision (FR-013)."""

    APPROVED = "approved"
    REJECTED = "rejected"
    REVISION_REQUESTED = "revision_requested"


class SpecializationCategory(StrEnum):
    """Canonical supported file-type specialization categories (FR-007, FR-008)."""

    PYTHON = "python"
    MARKDOWN = "markdown"
    YAML = "yaml"
    TYPESCRIPT = "typescript"
    UNSUPPORTED_OR_BINARY = "unsupported_or_binary"


#: Logical capability identifiers granted to every scope agent (FR-016).
BASELINE_CAPABILITIES: tuple[str, ...] = (
    "read_repository",
    "search_repository",
    "inspect_diff",
    "report_result",
)

#: Additional capabilities granted only to review-only (Epic/Feature) scopes.
REVIEW_CAPABILITIES: tuple[str, ...] = (
    "validate_scope",
    "evaluate_requirements",
    "evaluate_architecture",
)

#: Additional capabilities granted only to Subtask (writable) scopes.
WRITE_CAPABILITIES: tuple[str, ...] = (
    "write_files",
    "version_control",
)

#: Per-specialization-category capability extensions (FR-016).
SPECIALIZATION_CAPABILITIES: dict[SpecializationCategory, tuple[str, ...]] = {
    SpecializationCategory.PYTHON: ("python_language", "python_test", "python_lint_typecheck"),
    SpecializationCategory.MARKDOWN: ("markdown_authoring", "markdown_lint"),
    SpecializationCategory.YAML: ("yaml_authoring", "yaml_lint"),
    SpecializationCategory.TYPESCRIPT: (
        "typescript_language",
        "typescript_test",
        "typescript_lint_typecheck",
    ),
    SpecializationCategory.UNSUPPORTED_OR_BINARY: (),
}
_WINDOWS_DRIVE_PREFIX_RE = re.compile(r"^[A-Za-z]:/")


class CapabilityProvisioningError(RuntimeError):
    """Raised when a canonical logical capability cannot be mapped to a runtime tool (FR-016)."""

    def __init__(self, capability: str, scope_level: AgentScopeLevel) -> None:
        self.capability = capability
        self.scope_level = scope_level
        super().__init__(f"Required capability '{capability}' could not be provisioned for scope '{scope_level.value}'")


def required_capabilities(
    scope_level: AgentScopeLevel,
    specialization: SpecializationCategory | None = None,
) -> tuple[str, ...]:
    """Return the canonical logical capabilities required for a scope (FR-016).

    Args:
        scope_level: The hierarchy level of the agent (epic/feature/subtask).
        specialization: The file-type specialization for subtask agents, or
            ``None`` for review-only scopes and for a discovery-only subtask
            agent that has not yet been classified.

    Returns:
        An ordered, de-duplicated tuple of logical capability identifiers.
    """
    capabilities: list[str] = list(BASELINE_CAPABILITIES)
    if scope_level in (AgentScopeLevel.EPIC, AgentScopeLevel.FEATURE):
        capabilities.extend(REVIEW_CAPABILITIES)
    elif scope_level == AgentScopeLevel.SUBTASK:
        capabilities.extend(WRITE_CAPABILITIES)
        if specialization is not None:
            capabilities.extend(SPECIALIZATION_CAPABILITIES.get(specialization, ()))
    return tuple(dict.fromkeys(capabilities))


def provision_capabilities(
    scope_level: AgentScopeLevel,
    specialization: SpecializationCategory | None,
    available_tools: frozenset[str],
) -> tuple[str, ...]:
    """Map required logical capabilities onto available runtime tools.

    Args:
        scope_level: The hierarchy level of the agent.
        specialization: The file-type specialization, if any.
        available_tools: The set of logical capability identifiers the
            runtime is able to supply.

    Returns:
        The tuple of provisioned capabilities (identical to
        ``required_capabilities`` when provisioning succeeds).

    Raises:
        CapabilityProvisioningError: If any required capability is not in
            ``available_tools``.
    """
    required = required_capabilities(scope_level, specialization)
    for capability in required:
        if capability not in available_tools:
            raise CapabilityProvisioningError(capability, scope_level)
    return required


@dataclass(frozen=True)
class ArtifactReference:
    """A reference to a verified specification artifact.

    Attributes:
        path: Repository-relative path to the artifact (e.g. ``spec.md``).
        issue_key: The issue/spec-directory key the artifact belongs to.
        available: Whether the artifact currently exists and is non-empty.
    """

    path: str
    issue_key: str
    available: bool = True


@dataclass(frozen=True)
class FileBoundary:
    """An immutable, mechanically enforced writable-file boundary (FR-010).

    Only ``AgentScopeLevel.SUBTASK`` agents may hold a non-empty boundary.
    Paths are repository-relative POSIX paths (no leading ``/``, no ``..``
    traversal). Enforcement is performed by ``is_within`` and is the sole
    authority used by the orchestrator to accept or block a write attempt.
    """

    paths: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for raw in self.paths:
            if (
                not raw
                or raw.startswith("/")
                or ".." in raw.split("/")
                or "\\" in raw
                or _WINDOWS_DRIVE_PREFIX_RE.match(raw)
            ):
                msg = f"Invalid repository-relative boundary path: {raw!r}"
                raise ValueError(msg)
            if posixpath.normpath(raw) != raw:
                msg = f"Non-canonical repository-relative boundary path: {raw!r}"
                raise ValueError(msg)

    @property
    def is_empty(self) -> bool:
        """Return True if this boundary grants no writable paths."""
        return len(self.paths) == 0

    def is_within(self, candidate_path: str) -> bool:
        """Return True if ``candidate_path`` is exactly one of the granted paths.

        Rejects any candidate containing a backslash: the boundary format is
        POSIX-only, so a Windows-style path such as ``..\\secret.py`` or a
        drive path such as ``C:\\repo\\file.py`` must never be treated as
        within the boundary.
        """
        if "\\" in candidate_path:
            return False
        return candidate_path in self.paths

    def union(self, other: FileBoundary) -> FileBoundary:
        """Return a new boundary that is the union of this and ``other``."""
        merged = tuple(dict.fromkeys((*self.paths, *other.paths)))
        return FileBoundary(paths=merged)

    def overlaps(self, other: FileBoundary) -> tuple[str, ...]:
        """Return the paths shared between this boundary and ``other``."""
        other_set = set(other.paths)
        return tuple(p for p in self.paths if p in other_set)


@dataclass(frozen=True)
class ReviewAuthority:
    """Declares whether a scope may render review decisions and/or resolve conflicts.

    Attributes:
        can_review: Whether this scope may approve/reject/request revision
            on lower-scope output (FR-013).
        can_resolve_conflicts: Whether this scope is an eligible FR-018
            conflict-resolution authority.
    """

    can_review: bool = False
    can_resolve_conflicts: bool = False


@dataclass(frozen=True)
class ScopeAgent:
    """An immutable, mechanically enforced agent scope declaration (FR-010).

    Attributes:
        agent_id: Stable identifier for the spawned agent (e.g. ``epic-123``).
        scope_level: The hierarchy level of this agent.
        issue_key: The issue key this agent is responsible for.
        artifacts: Verified artifact references available to this agent.
        file_boundary: The writable-file boundary (always empty for
            review-only scopes).
        specialization: The file-type specialization category, if any.
        review_authority: What review/conflict-resolution powers this scope has.
        capabilities: The provisioned canonical logical capabilities.
        discovery_only: Whether this is a discovery-only general Subtask
            agent with an initially empty boundary (FR-007).
        sibling_ids: Known sibling agent identifiers for context (FR-011, SC-012).
    """

    agent_id: str
    scope_level: AgentScopeLevel
    issue_key: str
    artifacts: tuple[ArtifactReference, ...] = ()
    file_boundary: FileBoundary = field(default_factory=FileBoundary)
    specialization: SpecializationCategory | None = None
    review_authority: ReviewAuthority = field(default_factory=ReviewAuthority)
    capabilities: tuple[str, ...] = ()
    discovery_only: bool = False
    sibling_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.scope_level in (AgentScopeLevel.EPIC, AgentScopeLevel.FEATURE):
            if not self.file_boundary.is_empty:
                msg = f"Review-only scope '{self.scope_level.value}' must not declare a file boundary"
                raise ValueError(msg)
            if self.discovery_only:
                msg = f"Review-only scope '{self.scope_level.value}' cannot be discovery_only"
                raise ValueError(msg)
        if self.scope_level == AgentScopeLevel.ORCHESTRATOR:
            msg = "ORCHESTRATOR is not a valid spawned-agent scope level"
            raise ValueError(msg)
        if self.scope_level == AgentScopeLevel.SUBTASK and self.discovery_only:
            if not self.file_boundary.is_empty:
                msg = "A discovery_only Subtask agent must have an empty file boundary"
                raise ValueError(msg)
            if self.specialization is not None:
                msg = "A discovery_only Subtask agent must not declare a specialization"
                raise ValueError(msg)

    @property
    def can_modify_files(self) -> bool:
        """Return True only for Subtask agents (FR-010)."""
        return self.scope_level == AgentScopeLevel.SUBTASK

    def may_write(self, candidate_path: str) -> bool:
        """Return True if this agent is permitted to write to ``candidate_path``."""
        return self.can_modify_files and self.file_boundary.is_within(candidate_path)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-safe dict for trace/context payloads."""
        return {
            "agent_id": self.agent_id,
            "scope_level": self.scope_level.value,
            "issue_key": self.issue_key,
            "artifacts": [{"path": a.path, "issue_key": a.issue_key, "available": a.available} for a in self.artifacts],
            "file_boundary": list(self.file_boundary.paths),
            "specialization": self.specialization.value if self.specialization else None,
            "review_authority": {
                "can_review": self.review_authority.can_review,
                "can_resolve_conflicts": self.review_authority.can_resolve_conflicts,
            },
            "capabilities": list(self.capabilities),
            "discovery_only": self.discovery_only,
            "sibling_ids": list(self.sibling_ids),
        }


def make_review_only_scope(
    *,
    agent_id: str,
    scope_level: AgentScopeLevel,
    issue_key: str,
    artifacts: tuple[ArtifactReference, ...] = (),
    capabilities: tuple[str, ...] = (),
    can_resolve_conflicts: bool = False,
    sibling_ids: tuple[str, ...] = (),
) -> ScopeAgent:
    """Construct an Epic or Feature (review-only) scope agent."""
    if scope_level not in (AgentScopeLevel.EPIC, AgentScopeLevel.FEATURE):
        msg = "make_review_only_scope requires EPIC or FEATURE scope_level"
        raise ValueError(msg)
    return ScopeAgent(
        agent_id=agent_id,
        scope_level=scope_level,
        issue_key=issue_key,
        artifacts=artifacts,
        file_boundary=FileBoundary(),
        specialization=None,
        review_authority=ReviewAuthority(can_review=True, can_resolve_conflicts=can_resolve_conflicts),
        capabilities=capabilities,
        discovery_only=False,
        sibling_ids=sibling_ids,
    )


def make_subtask_scope(
    *,
    agent_id: str,
    issue_key: str,
    file_boundary: FileBoundary,
    specialization: SpecializationCategory | None,
    capabilities: tuple[str, ...] = (),
    discovery_only: bool = False,
    sibling_ids: tuple[str, ...] = (),
) -> ScopeAgent:
    """Construct a Subtask (writable) scope agent."""
    return ScopeAgent(
        agent_id=agent_id,
        scope_level=AgentScopeLevel.SUBTASK,
        issue_key=issue_key,
        artifacts=(),
        file_boundary=file_boundary,
        specialization=specialization,
        review_authority=ReviewAuthority(can_review=False, can_resolve_conflicts=False),
        capabilities=capabilities,
        discovery_only=discovery_only,
        sibling_ids=sibling_ids,
    )
