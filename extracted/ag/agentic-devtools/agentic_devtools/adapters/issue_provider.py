"""IssueProvider protocol and result types for hierarchy-capable adapters.

Defines the ``IssueProvider`` protocol (structural subtyping via
``typing.Protocol``) plus the ``ProviderIssueResult`` and ``ProviderLinkResult``
dataclasses used as return types, the ``VALID_ISSUE_TYPES`` constant, and the
``InMemoryIssueProvider`` test fake.

This module is supplementary to the existing ``IssueAdapter`` ABC — it does
NOT replace it.  Concrete adapters MAY implement both interfaces.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

from agentic_devtools.adapters.exceptions import AdapterValidationError

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Canonical set of provider-neutral issue types.
# Adapters validate ``issue_type`` parameters against this set.  The values are
# intentionally lowercase and provider-agnostic — concrete adapters map them to
# provider-native equivalents (e.g., GitHub labels, Jira issue types).
VALID_ISSUE_TYPES: frozenset[str] = frozenset({"epic", "feature", "subtask", "task", "bug"})

# Provider-neutral hierarchy rank used to validate parent-child pairs.  A pair
# is permitted only when the parent's rank is strictly less than the child's
# rank, so a parent must always sit *above* its child in the hierarchy.  This
# rejects, for example, an epic-as-child, a subtask-as-parent, or same-level
# nesting such as a ``task`` under a ``feature`` (both rank 1).
HIERARCHY_RANK: dict[str, int] = {
    "epic": 0,
    "feature": 1,
    "task": 1,
    "bug": 1,
    "subtask": 2,
}


def check_hierarchy_pair(child_type: str, parent_type: str) -> None:
    """Validate a provider-neutral parent-child issue-type pair.

    Both types must be members of :data:`VALID_ISSUE_TYPES` (case-insensitive)
    and the parent must rank strictly above the child in :data:`HIERARCHY_RANK`.

    Args:
        child_type: The child node's issue type.
        parent_type: The parent node's issue type.

    Raises:
        AdapterValidationError: If either type is unsupported or the pair is not
            a permitted parent-above-child combination.
    """
    child_norm = child_type.lower().strip() if isinstance(child_type, str) else ""
    parent_norm = parent_type.lower().strip() if isinstance(parent_type, str) else ""
    if child_norm not in HIERARCHY_RANK:
        raise AdapterValidationError(
            f"Unsupported child issue type {child_type!r}. Valid types: {sorted(HIERARCHY_RANK)}"
        )
    if parent_norm not in HIERARCHY_RANK:
        raise AdapterValidationError(
            f"Unsupported parent issue type {parent_type!r}. Valid types: {sorted(HIERARCHY_RANK)}"
        )
    if HIERARCHY_RANK[parent_norm] >= HIERARCHY_RANK[child_norm]:
        raise AdapterValidationError(
            f"Invalid hierarchy pair: a {parent_norm!r} cannot be the parent of a {child_norm!r}."
        )


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class IssueTypeMappingError(ValueError):
    """Raised when an issue type cannot be mapped to the provider's native type.

    Inherits from :class:`ValueError` so callers typed against
    :class:`IssueProvider` can handle unsupported-type validation consistently
    across all adapters with a single ``except ValueError`` clause.

    For example, GitHub does not support a native "sub-task" issue type — the
    adapter raises this when the requested type has no valid mapping.
    """


# ---------------------------------------------------------------------------
# Result dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ProviderIssueResult:
    """Result of an issue-level operation (create, resolve, set_issue_type, apply_labels).

    Instances are *shallowly* immutable (frozen dataclass): attribute
    rebinding is blocked, but the ``metadata`` dict itself is mutable — callers
    must not mutate it in place.  Use ``to_dict()`` for JSON serialization.

    Attributes:
        identifier: Provider-native issue identifier (GitHub issue number as
            string, or Jira issue key like ``"PROJ-123"``).
        url: Web URL for the issue on its platform.  Populated for all
            non-dry-run results; empty string for dry-run.
        status: One of ``"created"``, ``"existing"``, ``"dry-run"``,
            ``"updated"``, ``"no-op"``, ``"resolved"`` depending on the method.
        metadata: Arbitrary extra data (e.g., GitHub database ID, labels).
            Do not mutate this dict after construction.
    """

    identifier: str
    url: str
    status: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable dictionary representation."""
        return {
            "identifier": self.identifier,
            "url": self.url,
            "status": self.status,
            "metadata": copy.deepcopy(self.metadata),
        }


@dataclass(frozen=True)
class ProviderLinkResult:
    """Result of a link-level operation or a pre-protocol label application.

    Primary use cases: ``link_subissue`` and ``add_blocked_by``, where
    ``source_id`` / ``target_id`` are issue identifiers.

    Legacy use: the non-conforming ``apply_labels`` implementations on
    ``GitHubProvider`` and ``JiraProvider`` also return this type — in those
    cases ``target_id`` holds a label string rather than an issue identifier.
    New code should use :class:`ProviderIssueResult` (as the protocol requires).

    Instances are immutable (frozen dataclass).  Use ``to_dict()`` for JSON
    serialization.

    Attributes:
        source_id: Identifier of the source issue in the relationship.
            For ``link_subissue``: the parent.
            For ``add_blocked_by``: the blocker.
            For legacy ``apply_labels``: the issue being labelled.
        target_id: Identifier of the target issue in the relationship.
            For ``link_subissue``: the child.
            For ``add_blocked_by``: the blocked issue.
            For legacy ``apply_labels``: the label string.
        status: One of ``"linked"``, ``"already-linked"``, ``"dry-run"``.
    """

    source_id: str
    target_id: str
    status: str

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable dictionary representation."""
        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "status": self.status,
        }


# ---------------------------------------------------------------------------
# Protocol
# ---------------------------------------------------------------------------


@runtime_checkable
class IssueProvider(Protocol):
    """Protocol for hierarchy-capable issue providers.

    Defines exactly 8 methods: ``create_issue``, ``link_subissue``,
    ``add_blocked_by``, ``apply_labels``, ``set_issue_type``,
    ``resolve_identifier``, ``normalize_identifier``, ``format_identifier``.

    All mutation methods accept a keyword-only ``dry_run`` parameter.  When
    ``True``, the method MUST NOT perform any mutating API calls — it returns
    a result with ``status="dry-run"`` describing what *would* happen.

    Adapters MUST NOT independently consult state, env vars, or CLI flags for
    dry-run — the ``dry_run`` bool passed by the caller is the sole source of
    truth.

    Identifiers are always strings.  For GitHub, the issue number is
    represented as a plain numeric string (e.g., ``"42"``).  For Jira, the
    issue key is used (e.g., ``"PROJ-123"``).  The ``normalize_identifier``
    and ``format_identifier`` methods handle provider-specific formatting.
    """

    def create_issue(
        self,
        title: str,
        body: str,
        issue_type: str,
        *,
        parent_id: str | None = None,
        labels: list[str] | None = None,
        idempotency_key: str | None = None,
        dry_run: bool = False,
    ) -> ProviderIssueResult:
        """Create an issue on the provider.

        Args:
            title: Issue title / summary.  Must be non-empty after stripping
                whitespace; raises ``ValueError`` otherwise.
            body: Issue description body.
            issue_type: Provider-neutral type — must be a member of
                ``VALID_ISSUE_TYPES``.  Raises ``ValueError`` with sorted
                valid values if not.
            parent_id: Provider-native parent identifier, or ``None``.  If
                provided, must be a non-empty string; raises ``ValueError``
                otherwise.
            labels: Optional list of label strings to apply at creation time.
            idempotency_key: Optional deduplication key.  If a previous call
                used the same key, the existing issue is returned with
                ``status="existing"`` instead of creating a duplicate.
            dry_run: When ``True``, skip mutations and return a preview result
                with ``status="dry-run"``.

        Returns:
            A :class:`ProviderIssueResult` with status ``"created"``,
            ``"existing"``, or ``"dry-run"``.

        Raises:
            ValueError: If title is empty, issue_type is unsupported, or
                parent_id is provided but empty.
        """
        ...  # pragma: no cover

    def set_issue_type(
        self,
        identifier: str,
        issue_type: str,
        *,
        dry_run: bool = False,
    ) -> ProviderIssueResult:
        """Set the issue type on an existing issue.

        Validates ``issue_type`` against ``VALID_ISSUE_TYPES``; raises
        ``ValueError`` with the sorted valid types if the value is
        unsupported.

        Args:
            identifier: Provider-native issue identifier.  Must reference an
                existing issue; raises ``ValueError`` if not found.
            issue_type: Provider-neutral type to apply.
            dry_run: When ``True``, skip mutations and return
                ``status="dry-run"``.

        Returns:
            A :class:`ProviderIssueResult` with status ``"updated"``,
            ``"no-op"``, or ``"dry-run"``.  ``"no-op"`` is returned when the
            requested type already matches the issue's current type.
            ``metadata["issue_type"]`` is set to the applied type.

        Raises:
            ValueError: If identifier is missing or issue_type is unsupported.
        """
        ...  # pragma: no cover

    def resolve_identifier(
        self,
        identifier: str,
        *,
        dry_run: bool = False,
    ) -> ProviderIssueResult:
        """Resolve an existing issue identifier to full details.

        When ``dry_run=False``, the identifier must reference an existing
        issue; raises ``ValueError`` if not found.  When ``dry_run=True``,
        the lookup is skipped and the normalized identifier is returned with
        empty ``url`` and empty ``metadata``.

        Empty or whitespace-only identifiers raise ``ValueError`` regardless
        of ``dry_run``.

        Args:
            identifier: Provider-native issue identifier.
            dry_run: When ``True``, skip API calls and return
                ``status="dry-run"``.

        Returns:
            A :class:`ProviderIssueResult` with status ``"resolved"`` or
            ``"dry-run"``, with ``metadata["internal_id"]`` populated when
            resolved.

        Raises:
            ValueError: If identifier is empty/whitespace or (when not
                dry_run) not found.
        """
        ...  # pragma: no cover

    def link_subissue(
        self,
        parent_id: str,
        child_id: str,
        *,
        dry_run: bool = False,
    ) -> ProviderLinkResult:
        """Create a parent-child link between two issues.

        Direction convention: ``source_id`` in the result is the parent,
        ``target_id`` is the child.

        Both identifiers must be non-empty strings referencing existing
        issues; raises ``ValueError`` if either is empty or not found.

        Idempotent: if the link already exists, returns
        ``status="already-linked"`` without error.

        Args:
            parent_id: Provider-native parent identifier.
            child_id: Provider-native child identifier.
            dry_run: When ``True``, skip mutations and return
                ``status="dry-run"``.

        Returns:
            A :class:`ProviderLinkResult` with status ``"linked"``,
            ``"already-linked"``, or ``"dry-run"``.

        Raises:
            ValueError: If either identifier is empty or not found.
        """
        ...  # pragma: no cover

    def add_blocked_by(
        self,
        issue_id: str,
        blocked_by_id: str,
        *,
        dry_run: bool = False,
    ) -> ProviderLinkResult:
        """Declare that *issue_id* is blocked by *blocked_by_id*.

        Self-blocking (``issue_id == blocked_by_id``) raises ``ValueError``.

        Both identifiers must be non-empty strings referencing existing
        issues; raises ``ValueError`` if either is empty or not found.

        Idempotent: if the blocking relationship already exists, returns
        ``status="already-linked"`` without error.

        Args:
            issue_id: The issue that is blocked.
            blocked_by_id: The issue doing the blocking.
            dry_run: When ``True``, skip mutations and return
                ``status="dry-run"``.

        Returns:
            A :class:`ProviderLinkResult` with status ``"linked"``,
            ``"already-linked"``, or ``"dry-run"``.

        Raises:
            ValueError: If self-blocking, either identifier is empty, or
                either identifier is not found.
        """
        ...  # pragma: no cover

    def apply_labels(
        self,
        identifier: str,
        labels: list[str],
        *,
        dry_run: bool = False,
    ) -> ProviderIssueResult:
        """Apply labels to an issue (idempotent).

        When ``dry_run=True``, returns ``status="dry-run"`` regardless of
        label state (FR-010 precedence).  In dry-run mode no provider call is
        made, the identifier is **not** validated against existing issues, and
        ``metadata["labels"]`` is a sorted preview of the *requested* labels
        only (not a union with any pre-existing labels).

        When ``dry_run=False``:
        - Empty ``labels`` list or all labels already present → ``"no-op"``.
        - At least one new label applied → ``"updated"``.
        - ``metadata["labels"]`` contains the full post-operation label set
          (sorted).

        Args:
            identifier: Provider-native issue identifier.  When
                ``dry_run=False`` it must reference an existing issue; raises
                ``ValueError`` if not found.  In dry-run mode existence is not
                checked.
            labels: List of label strings to apply.
            dry_run: When ``True``, skip mutations.

        Returns:
            A :class:`ProviderIssueResult` with status ``"updated"``,
            ``"no-op"``, or ``"dry-run"``.  For non-dry-run results
            ``metadata["labels"]`` reflects the post-operation label state; for
            dry-run results it reflects only the requested labels.

        Raises:
            ValueError: If (when ``dry_run=False``) the identifier is not
                found.
        """
        ...  # pragma: no cover

    def normalize_identifier(self, identifier: str) -> str:
        """Normalize a provider-native identifier to its canonical form.

        This is a pure string transformation with no side effects or API
        calls.  For GitHub, strips a leading ``#`` if present (e.g.,
        ``"#42"`` → ``"42"``).  For Jira, returns the identifier unchanged.

        Args:
            identifier: The identifier to normalize.  Must be non-empty
                after stripping whitespace; raises ``ValueError`` otherwise.

        Returns:
            The canonical form of the identifier.

        Raises:
            ValueError: If identifier is empty or whitespace-only.
        """
        ...  # pragma: no cover

    def format_identifier(self, identifier: str) -> str:
        """Format a canonical identifier for display.

        This is a pure string transformation with no side effects or API
        calls.  For GitHub, prepends ``#`` if not present (e.g.,
        ``"42"`` → ``"#42"``).  For Jira, returns the identifier unchanged.

        Args:
            identifier: The canonical identifier to format.  Must be
                non-empty after stripping whitespace; raises ``ValueError``
                otherwise.

        Returns:
            The display-formatted identifier.

        Raises:
            ValueError: If identifier is empty or whitespace-only.
        """
        ...  # pragma: no cover


# ---------------------------------------------------------------------------
# Companion capability protocol
# ---------------------------------------------------------------------------


@runtime_checkable
class HierarchyValidationProvider(Protocol):
    """Companion capability protocol for provider-contract hierarchy validation.

    This is a *separate*, runtime-checkable protocol from
    :class:`IssueProvider` — it does not extend or alter the eight-method
    ``IssueProvider`` contract.  Providers that can validate issue types and
    parent-child hierarchy pairs without performing any mutation implement it
    in addition to :class:`IssueProvider`.

    Both methods are non-mutating: they never create, link, or otherwise change
    provider state.  They raise a shared adapter-layer validation exception
    (:class:`~agentic_devtools.adapters.exceptions.AdapterValidationError` or a
    subclass) to signal an unsupported type or an impermissible pair, so callers
    can translate a single exception family into their own validation errors.
    """

    def validate_issue_type(self, issue_type: str) -> None:
        """Validate that *issue_type* is supported by this provider.

        Enables standalone-node validation (for example an epic with no
        children) independently of any pair check.

        Raises:
            AdapterValidationError: If the type is unsupported or unmapped.
        """
        ...  # pragma: no cover

    def validate_hierarchy_pair(self, child_type: str, parent_type: str) -> None:
        """Validate that the *parent_type* → *child_type* pairing is permitted.

        Raises:
            AdapterValidationError: If the combination is not permitted.
        """
        ...  # pragma: no cover


class InMemoryIssueProvider:
    """In-memory fake implementation of IssueProvider for testing.

    Provides deterministic, single-threaded behavior with full contract
    compliance.  All state is stored in plain Python data structures and
    inspectable via public properties.

    Supports two identifier styles:
    - ``"github"``: identifiers are numeric strings; ``normalize_identifier``
      strips ``#``, ``format_identifier`` prepends ``#``.
    - ``"jira"``: identifiers are passed through unchanged by both methods.

    Args:
        identifier_style: One of ``"github"`` or ``"jira"``.  Controls the
            behavior of ``normalize_identifier`` and ``format_identifier``.
    """

    def __init__(self, identifier_style: str = "github") -> None:
        _valid_styles = {"github", "jira"}
        if identifier_style not in _valid_styles:
            raise ValueError(
                f"Unsupported identifier_style {identifier_style!r}. Valid styles: {sorted(_valid_styles)}"
            )
        self._identifier_style = identifier_style
        self._issues: dict[str, dict[str, Any]] = {}
        self._next_id: int = 1
        self._parent_child: set[tuple[str, str]] = set()
        self._blocked_by: set[tuple[str, str]] = set()
        self._idempotency_keys: dict[str, str] = {}

    # -- Public inspection properties --

    @property
    def issues(self) -> dict[str, dict[str, Any]]:
        """Return a deep copy of all stored issues keyed by identifier."""
        return copy.deepcopy(self._issues)

    @property
    def parent_child_links(self) -> set[tuple[str, str]]:
        """Return a copy of all parent-child link tuples (parent, child)."""
        return set(self._parent_child)

    @property
    def blocked_by_links(self) -> set[tuple[str, str]]:
        """Return a copy of all blocked-by tuples (issue, blocker)."""
        return set(self._blocked_by)

    # -- Protocol methods --

    def create_issue(
        self,
        title: str,
        body: str,
        issue_type: str,
        *,
        parent_id: str | None = None,
        labels: list[str] | None = None,
        idempotency_key: str | None = None,
        dry_run: bool = False,
    ) -> ProviderIssueResult:
        """Create an issue in the in-memory store.

        Validates title is non-empty and issue_type is in VALID_ISSUE_TYPES.
        Handles idempotency via idempotency_key.  Respects dry_run.

        See :meth:`IssueProvider.create_issue` for full contract.
        """
        if not title or not title.strip():
            raise ValueError("title must be a non-empty string")
        if issue_type not in VALID_ISSUE_TYPES:
            raise ValueError(f"Unsupported issue_type {issue_type!r}. Valid types: {sorted(VALID_ISSUE_TYPES)}")
        if parent_id is not None and (not parent_id or not parent_id.strip()):
            raise ValueError("parent_id must be a non-empty string when provided")

        if dry_run:
            return ProviderIssueResult(identifier="", url="", status="dry-run")

        # Idempotency check
        if idempotency_key and idempotency_key in self._idempotency_keys:
            existing_id = self._idempotency_keys[idempotency_key]
            return ProviderIssueResult(
                identifier=existing_id,
                url=f"https://fake.test/issues/{existing_id}",
                status="existing",
                metadata={"labels": sorted(self._issues[existing_id].get("labels", []))},
            )

        identifier = str(self._next_id)
        self._next_id += 1

        issue_labels = sorted(set(labels)) if labels else []
        self._issues[identifier] = {
            "title": title,
            "body": body,
            "issue_type": issue_type,
            "parent_id": parent_id,
            "labels": issue_labels,
        }

        if idempotency_key:
            self._idempotency_keys[idempotency_key] = identifier

        return ProviderIssueResult(
            identifier=identifier,
            url=f"https://fake.test/issues/{identifier}",
            status="created",
            metadata={"labels": sorted(issue_labels)},
        )

    def set_issue_type(
        self,
        identifier: str,
        issue_type: str,
        *,
        dry_run: bool = False,
    ) -> ProviderIssueResult:
        """Set the issue type on an existing in-memory issue.

        See :meth:`IssueProvider.set_issue_type` for full contract.
        """
        if not identifier or not identifier.strip():
            raise ValueError("identifier must be a non-empty string")
        if issue_type not in VALID_ISSUE_TYPES:
            raise ValueError(f"Unsupported issue_type {issue_type!r}. Valid types: {sorted(VALID_ISSUE_TYPES)}")
        if identifier not in self._issues:
            raise ValueError(f"Issue {identifier!r} not found")

        if dry_run:
            return ProviderIssueResult(
                identifier=identifier,
                url="",
                status="dry-run",
                metadata={"issue_type": issue_type},
            )

        if self._issues[identifier].get("issue_type") == issue_type:
            return ProviderIssueResult(
                identifier=identifier,
                url=f"https://fake.test/issues/{identifier}",
                status="no-op",
                metadata={"issue_type": issue_type},
            )

        self._issues[identifier]["issue_type"] = issue_type
        return ProviderIssueResult(
            identifier=identifier,
            url=f"https://fake.test/issues/{identifier}",
            status="updated",
            metadata={"issue_type": issue_type},
        )

    def resolve_identifier(
        self,
        identifier: str,
        *,
        dry_run: bool = False,
    ) -> ProviderIssueResult:
        """Resolve an identifier in the in-memory store.

        See :meth:`IssueProvider.resolve_identifier` for full contract.
        """
        if not identifier or not identifier.strip():
            raise ValueError("identifier must be a non-empty string")

        if dry_run:
            normalized = self.normalize_identifier(identifier)
            return ProviderIssueResult(
                identifier=normalized,
                url="",
                status="dry-run",
                metadata={},
            )

        if identifier not in self._issues:
            raise ValueError(f"Issue {identifier!r} not found")

        return ProviderIssueResult(
            identifier=identifier,
            url=f"https://fake.test/issues/{identifier}",
            status="resolved",
            metadata={"internal_id": identifier},
        )

    def link_subissue(
        self,
        parent_id: str,
        child_id: str,
        *,
        dry_run: bool = False,
    ) -> ProviderLinkResult:
        """Create a parent-child link in the in-memory store.

        See :meth:`IssueProvider.link_subissue` for full contract.
        """
        if not parent_id or not parent_id.strip():
            raise ValueError("parent_id must be a non-empty string")
        if not child_id or not child_id.strip():
            raise ValueError("child_id must be a non-empty string")

        if parent_id not in self._issues:
            raise ValueError(f"Parent issue {parent_id!r} not found")
        if child_id not in self._issues:
            raise ValueError(f"Child issue {child_id!r} not found")

        if dry_run:
            return ProviderLinkResult(source_id=parent_id, target_id=child_id, status="dry-run")

        link = (parent_id, child_id)
        if link in self._parent_child:
            return ProviderLinkResult(source_id=parent_id, target_id=child_id, status="already-linked")

        self._parent_child.add(link)
        return ProviderLinkResult(source_id=parent_id, target_id=child_id, status="linked")

    def add_blocked_by(
        self,
        issue_id: str,
        blocked_by_id: str,
        *,
        dry_run: bool = False,
    ) -> ProviderLinkResult:
        """Declare a blocking relationship in the in-memory store.

        See :meth:`IssueProvider.add_blocked_by` for full contract.
        """
        if not issue_id or not issue_id.strip():
            raise ValueError("issue_id must be a non-empty string")
        if not blocked_by_id or not blocked_by_id.strip():
            raise ValueError("blocked_by_id must be a non-empty string")
        if issue_id == blocked_by_id:
            raise ValueError("An issue cannot block itself")

        if issue_id not in self._issues:
            raise ValueError(f"Issue {issue_id!r} not found")
        if blocked_by_id not in self._issues:
            raise ValueError(f"Blocker issue {blocked_by_id!r} not found")

        if dry_run:
            return ProviderLinkResult(source_id=blocked_by_id, target_id=issue_id, status="dry-run")

        edge = (issue_id, blocked_by_id)
        if edge in self._blocked_by:
            return ProviderLinkResult(source_id=blocked_by_id, target_id=issue_id, status="already-linked")

        self._blocked_by.add(edge)
        return ProviderLinkResult(source_id=blocked_by_id, target_id=issue_id, status="linked")

    def apply_labels(
        self,
        identifier: str,
        labels: list[str],
        *,
        dry_run: bool = False,
    ) -> ProviderIssueResult:
        """Apply labels to an in-memory issue.

        See :meth:`IssueProvider.apply_labels` for full contract.
        """
        if not identifier or not identifier.strip():
            raise ValueError("identifier must be a non-empty string")

        if dry_run:
            # Dry-run preview: report only the requested labels (sorted, unique)
            # without reading existing state.  Per the protocol, dry-run makes no
            # provider call and does not validate issue existence.
            preview_labels = sorted({lbl for lbl in labels})
            return ProviderIssueResult(
                identifier=identifier,
                url="",
                status="dry-run",
                metadata={"labels": preview_labels},
            )

        if identifier not in self._issues:
            raise ValueError(f"Issue {identifier!r} not found")

        current_labels = set(self._issues[identifier].get("labels", []))
        new_labels = set(labels) - current_labels
        if not new_labels:
            return ProviderIssueResult(
                identifier=identifier,
                url=f"https://fake.test/issues/{identifier}",
                status="no-op",
                metadata={"labels": sorted(current_labels)},
            )

        updated_labels = current_labels | new_labels
        self._issues[identifier]["labels"] = sorted(updated_labels)
        return ProviderIssueResult(
            identifier=identifier,
            url=f"https://fake.test/issues/{identifier}",
            status="updated",
            metadata={"labels": sorted(updated_labels)},
        )

    def normalize_identifier(self, identifier: str) -> str:
        """Normalize identifier per the configured style.

        See :meth:`IssueProvider.normalize_identifier` for full contract.
        """
        if not identifier or not identifier.strip():
            raise ValueError("identifier must be a non-empty string")

        if self._identifier_style == "github":
            stripped = identifier.removeprefix("#")
            if not stripped:
                raise ValueError("identifier must be a non-empty string after normalization")
            return stripped
        return identifier

    def format_identifier(self, identifier: str) -> str:
        """Format identifier for display per the configured style.

        See :meth:`IssueProvider.format_identifier` for full contract.
        """
        if not identifier or not identifier.strip():
            raise ValueError("identifier must be a non-empty string")

        if self._identifier_style == "github":
            if not identifier.startswith("#"):
                return f"#{identifier}"
            return identifier
        return identifier

    # -- HierarchyValidationProvider methods --

    def validate_issue_type(self, issue_type: str) -> None:
        """Validate an issue type against the provider-neutral type set.

        See :meth:`HierarchyValidationProvider.validate_issue_type`.
        """
        normalized = issue_type.lower().strip() if isinstance(issue_type, str) else ""
        if normalized not in VALID_ISSUE_TYPES:
            raise AdapterValidationError(
                f"Unsupported issue_type {issue_type!r}. Valid types: {sorted(VALID_ISSUE_TYPES)}"
            )

    def validate_hierarchy_pair(self, child_type: str, parent_type: str) -> None:
        """Validate a parent-child issue-type pair.

        See :meth:`HierarchyValidationProvider.validate_hierarchy_pair`.
        """
        self.validate_issue_type(child_type)
        self.validate_issue_type(parent_type)
        check_hierarchy_pair(child_type, parent_type)

    # -- IdempotencyQueryProvider methods --

    def find_existing_issue(self, orchestration_key: str) -> ProviderIssueResult | None:
        """Find issue by orchestration key embedded in body.

        Searches all stored issues for a body containing the given key.
        Also checks the idempotency_keys mapping.

        Raises:
            ValueError: If multiple issues match (ambiguous state — FR-008).
        """
        from agentic_devtools.adapters.orchestration_key import extract_orchestration_key

        matches: list[str] = []
        for identifier, data in self._issues.items():
            body_val = data.get("body")
            key = extract_orchestration_key(body_val if isinstance(body_val, str) else "")
            if key == orchestration_key:
                matches.append(identifier)
        if len(matches) > 1:
            raise ValueError(f"Ambiguous: key {orchestration_key!r} matched {len(matches)} issues: {matches}")
        if not matches:
            # Check idempotency_keys mapping as fallback
            ident = self._idempotency_keys.get(orchestration_key)
            if ident is not None:
                matches.append(ident)
        if not matches:
            return None
        ident = matches[0]
        return ProviderIssueResult(
            identifier=ident,
            url=f"https://fake.test/issues/{ident}",
            status="existing",
        )

    def find_existing_link(self, parent_provider_id: str, child_provider_id: str) -> ProviderLinkResult | None:
        """Check if a parent-child link already exists.

        Returns ProviderLinkResult with status="already-linked" if found,
        None if not found.
        """
        if (parent_provider_id, child_provider_id) in self._parent_child:
            return ProviderLinkResult(
                source_id=parent_provider_id,
                target_id=child_provider_id,
                status="already-linked",
            )
        return None

    def find_existing_dependency(
        self, issue_provider_id: str, blocked_by_provider_id: str
    ) -> ProviderLinkResult | None:
        """Check if a blocking dependency already exists.

        Returns ProviderLinkResult with status="already-linked" if found,
        None if not found.
        """
        if (issue_provider_id, blocked_by_provider_id) in self._blocked_by:
            return ProviderLinkResult(
                source_id=blocked_by_provider_id,
                target_id=issue_provider_id,
                status="already-linked",
            )
        return None
