"""Shared type definitions for issue adapters.

Contains all TypedDict result types originally defined in ``base.py``, plus:

- :class:`IssueDetailWithRaw` — extends :class:`IssueDetail` with a ``raw`` field.
- :class:`NormalizedIssue` — frozen dataclass representing a provider-agnostic
  normalized issue with identity validation and coercion.

Schema discovery types (see :mod:`agentic_devtools.adapters.base`):

- :class:`IssueTypeInfo` — describes an available issue type (``name``,
  ``description``).
- :class:`PropertySchema` — describes a single field of an issue type (``name``,
  ``type``, ``required``, ``allowed_values``).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from typing_extensions import TypedDict

from agentic_devtools.adapters.exceptions import AdapterValidationError
from agentic_devtools.orchestration.execution.types import JSONValue

# ---------------------------------------------------------------------------
# Shared result TypedDicts (moved from base.py)
# ---------------------------------------------------------------------------


class Comment(TypedDict):
    """A single comment on an issue."""

    comment_id: str
    body: str
    created_at: str


class IssueResult(TypedDict):
    """Result of creating an issue."""

    issue_id: str
    url: str


class _IssueDetailRequired(TypedDict, total=True):
    """Required fields for issue details (private implementation base)."""

    issue_id: str
    title: str
    description: str
    status: str
    labels: list[str]
    url: str
    comments: list[Comment]


class IssueDetail(_IssueDetailRequired, total=False):
    """Full detail of a single issue.

    Required fields (always present):
        issue_id: Platform-specific unique issue identifier.
        title: Issue title / summary text.
        description: Full issue description body.
        status: Current workflow status (e.g. "open", "in_progress", "closed").
        labels: List of labels/tags applied to the issue.
        url: Web URL for the issue on its platform.
        comments: List of :class:`Comment` objects on this issue.

    Optional normalization fields (present when adapter populates them):
        issue_type: The issue type classification (e.g. "bug", "story", "task",
            "epic"). Adapter-specific; no enum enforced.
            Example: ``"bug"``
        priority: Priority level as a human-readable string (e.g. "high",
            "medium", "low", "P1"). Adapter-specific naming.
            Example: ``"high"``
        assignees: List of usernames or display names assigned to the issue.
            An empty list indicates no assignees; key absence means the adapter
            did not fetch assignee data.
            Example: ``["alice", "bob"]``
        custom_fields: Arbitrary key-value mapping of provider-specific custom
            fields. Values may be nested dicts, lists, or scalar types.
            Must be JSON-serializable for persistence.
            Example: ``{"sprint": "Sprint 42", "story_points": 5}``
        provider: Identifier for the originating platform adapter (e.g.
            "github", "jira", "markdown"). Useful for downstream normalization.
            Example: ``"jira"``
        raw_metadata: Opaque provider-specific metadata preserved verbatim
            from the API response. Structure varies by adapter; must be
            JSON-serializable.
            Example: ``{"api_version": "3", "expand": "changelog"}``
    """

    issue_type: str
    priority: str
    assignees: list[str]
    custom_fields: dict[str, JSONValue]
    provider: str
    raw_metadata: JSONValue


class CommentResult(TypedDict):
    """Result of adding a comment."""

    comment_id: str


class IssueSummary(TypedDict):
    """Summary of an issue for list results."""

    issue_id: str
    title: str
    status: str
    labels: list[str]
    url: str


class IssueFilters(TypedDict, total=False):
    """Optional filters for listing issues."""

    labels: list[str]
    state: str
    assignee: str


# ---------------------------------------------------------------------------
# Schema discovery TypedDicts
# ---------------------------------------------------------------------------


class IssueTypeInfo(TypedDict):
    """Describes an available issue type in a project or repository.

    Attributes:
        name: Identifier for the issue type. May be a human-readable display
            name (e.g. "Bug", "Story") or a lowercase slug (e.g. "bug",
            "feature") depending on the provider. GitHub uses lowercase slugs;
            Jira uses display names.
        description: Human-readable purpose or explanation of the type.
    """

    name: str
    description: str


class PropertySchema(TypedDict):
    """Describes a single field/property of an issue type.

    Attributes:
        name: Field identifier (e.g. "summary", "priority", "story_points").
        type: Free-form type label (e.g. "string", "number", "boolean",
            "array"). Providers may use their own native type labels.
        required: Whether the field is required when creating an issue of this
            type.
        allowed_values: Constrained set of acceptable values, or ``None`` when
            the field is unconstrained.
    """

    name: str
    type: str
    required: bool
    allowed_values: list[str] | None


# ---------------------------------------------------------------------------
# Extended TypedDict: IssueDetailWithRaw
# ---------------------------------------------------------------------------


class IssueDetailWithRaw(IssueDetail, total=False):
    """Issue detail extended with raw provider response data.

    Inherits all fields from :class:`IssueDetail` and optionally adds a
    ``raw`` dict containing the unmodified provider API response, enabling
    downstream normalizers to access fields not covered by the base schema.
    """

    raw: dict[str, Any]


# ---------------------------------------------------------------------------
# Normalized issue dataclass
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class NormalizedIssue:
    """Provider-agnostic normalized representation of an issue.

    All adapters' ``normalize()`` method returns an instance of this class,
    ensuring a uniform contract for downstream consumers (template renderers,
    spec generators, etc.).

    Identity fields (``issue_id``, ``title``, ``url``, ``provider``) are
    validated in ``__post_init__`` as non-empty strings —
    ``None``, non-string, empty, or whitespace-only values raise
    :class:`AdapterValidationError`.

    Coercion rules applied in ``__post_init__``:
        - ``description``: ``None`` → ``""``
        - ``comments``: ``None`` → ``[]``
        - ``labels``: non-list → ``[]``
        - ``status``: ``None`` or non-string → ``"unknown"``; lowercased
    """

    issue_id: str
    title: str
    url: str
    provider: str
    description: str
    status: str
    labels: list[str] = field(default_factory=list)
    comments: list[Comment] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""
    raw: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate identity fields and coerce optional fields."""
        # Identity validation
        for field_name in ("issue_id", "title", "url", "provider"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise AdapterValidationError(f"NormalizedIssue.{field_name} must be a non-empty string; got {value!r}")

        # Coerce description
        if getattr(self, "description") is None:
            object.__setattr__(self, "description", "")

        # Coerce comments then defensive-copy to prevent external mutation
        comments = getattr(self, "comments")
        object.__setattr__(self, "comments", [] if comments is None else list(comments))

        # Coerce labels then defensive-copy to prevent external mutation
        labels = getattr(self, "labels")
        object.__setattr__(self, "labels", [] if labels is None or not isinstance(labels, list) else list(labels))

        # Coerce status
        status = getattr(self, "status")
        if status is None or not isinstance(status, str):
            object.__setattr__(self, "status", "unknown")
        else:
            object.__setattr__(self, "status", status.lower())

        # Defensive-copy raw to prevent external mutation
        object.__setattr__(self, "raw", dict(getattr(self, "raw")))

    def __hash__(self) -> int:
        """NormalizedIssue is not hashable due to mutable fields."""
        raise TypeError(f"unhashable type: '{type(self).__name__}'")
