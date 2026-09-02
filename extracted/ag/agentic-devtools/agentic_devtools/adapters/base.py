"""Abstract issue adapter interface and shared result types.

Defines the ``IssueAdapter`` ABC that all platform-specific adapters must
implement, plus the shared ``TypedDict`` result types used across adapters.

Type definitions live in :mod:`agentic_devtools.adapters.types` and are
re-exported here for backward compatibility.
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal

from agentic_devtools.adapters.pull_request_comments import (
    PullRequestCommentAdapter,
    PullRequestCommentCapability,
    PullRequestCommentRequest,
    PullRequestCommentResult,
)
from agentic_devtools.adapters.types import (
    Comment,
    CommentResult,
    IssueDetail,
    IssueDetailWithRaw,
    IssueFilters,
    IssueResult,
    IssueSummary,
    IssueTypeInfo,
    NormalizedIssue,
    PropertySchema,
    _IssueDetailRequired,
)
from agentic_devtools.orchestration.execution.types import JSONValue

# Re-export all symbols for backward compatibility
__all__ = [
    "Comment",
    "CommentResult",
    "IssueAdapter",
    "IssueDetail",
    "IssueDetailWithRaw",
    "IssueFilters",
    "IssueResult",
    "IssueSummary",
    "IssueTypeInfo",
    "JSONValue",
    "NormalizedIssue",
    "PropertySchema",
    "PullRequestThreadReplyRequest",
    "PullRequestThreadReplyResult",
    "PullRequestCommentAdapter",
    "PullRequestCommentCapability",
    "PullRequestCommentRequest",
    "PullRequestCommentResult",
    "ReplyToPullRequestThreadRequest",
    "ReplyToPullRequestThreadResult",
    "is_valid_github_repository",
    "_IssueDetailRequired",
]


_GITHUB_SLUG_RE = re.compile(r"^[A-Za-z0-9_.][A-Za-z0-9_.-]*$")


def is_valid_github_repository(repository: str) -> bool:
    owner, separator, repo = repository.partition("/")
    return (
        separator == "/"
        and bool(_GITHUB_SLUG_RE.fullmatch(owner))
        and bool(_GITHUB_SLUG_RE.fullmatch(repo))
        and owner not in {"..", "."}
        and repo not in {"..", "."}
    )


@dataclass(frozen=True)
class PullRequestThreadReplyRequest:
    """Provider-neutral request for replying to an existing PR discussion."""

    provider: Literal["azure_devops", "github"]
    repository: str
    pull_request_number: int
    discussion_id: int | str
    body: str
    resolve: bool = False
    review_thread_id: str | None = None
    dry_run: bool = False
    azure_organization: str | None = None
    azure_project: str | None = None

    def __post_init__(self) -> None:
        if self.provider not in {"azure_devops", "github"}:
            raise ValueError(f"Unsupported code-hosting provider: {self.provider!r}")
        if not isinstance(self.repository, str) or not self.repository.strip():
            raise ValueError("repository is required")
        if (
            not isinstance(self.pull_request_number, int)
            or isinstance(self.pull_request_number, bool)
            or self.pull_request_number <= 0
        ):
            raise ValueError("pull_request_number must be positive")
        if not isinstance(self.body, str) or not self.body.strip():
            raise ValueError("body must not be empty or whitespace-only")
        if not isinstance(self.resolve, bool):
            raise ValueError(f"resolve must be a boolean, got {self.resolve!r}")
        if not isinstance(self.dry_run, bool):
            raise ValueError(f"dry_run must be a boolean, got {self.dry_run!r}")
        if self.provider == "github":
            if not is_valid_github_repository(self.repository):
                raise ValueError("GitHub repository must use owner/repo form without whitespace")
            if (
                isinstance(self.discussion_id, bool)
                or not str(self.discussion_id).isdigit()
                or int(self.discussion_id) <= 0
            ):
                raise ValueError("GitHub discussion_id must be a positive numeric review comment ID")
            if self.review_thread_id is not None and (
                not isinstance(self.review_thread_id, str)
                or not self.review_thread_id.strip()
                or self.review_thread_id.isdigit()
            ):
                raise ValueError("GitHub review_thread_id must be a non-numeric GraphQL node ID")
        elif (
            isinstance(self.discussion_id, bool)
            or not str(self.discussion_id).isdigit()
            or int(self.discussion_id) <= 0
        ):
            raise ValueError("Azure DevOps discussion_id must be a positive numeric thread ID")

    @property
    def pull_request_id(self) -> int:
        """Backward-compatible alias for the normalized pull-request number."""
        return self.pull_request_number

    def to_dict(self) -> dict[str, object]:
        """Serialize the request for task metadata and worker arguments."""
        data: dict[str, object] = {
            "provider": self.provider,
            "repository": self.repository,
            "pull_request_number": self.pull_request_number,
            "discussion_id": self.discussion_id,
            "body": self.body,
            "resolve": self.resolve,
            "review_thread_id": self.review_thread_id,
            "dry_run": self.dry_run,
        }
        if self.azure_organization is not None:
            data["azure_organization"] = self.azure_organization
        if self.azure_project is not None:
            data["azure_project"] = self.azure_project
        return data


@dataclass(frozen=True)
class PullRequestThreadReplyResult:
    """Normalized result of a pull-request thread reply operation."""

    provider: Literal["azure_devops", "github"]
    repository: str
    pull_request_number: int
    discussion_id: int | str
    resolution_requested: bool
    mutation_status: str
    reply_id: int | str | None = None
    resolution_status: str = "not_requested"
    diagnostics: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        """Serialize the result using stable CLI-style field names."""
        return {
            "provider": self.provider,
            "repository": self.repository,
            "pullRequestNumber": self.pull_request_number,
            "discussionId": self.discussion_id,
            "resolutionRequested": self.resolution_requested,
            "mutationStatus": self.mutation_status,
            "replyId": self.reply_id,
            "resolutionStatus": self.resolution_status,
            "diagnostics": list(self.diagnostics),
        }


ReplyToPullRequestThreadRequest = PullRequestThreadReplyRequest
ReplyToPullRequestThreadResult = PullRequestThreadReplyResult


# ---------------------------------------------------------------------------
# Abstract base class
# ---------------------------------------------------------------------------


class IssueAdapter(ABC):
    """Abstract base class for issue-tracking platform adapters.

    Concrete subclasses must implement the core abstract methods:
    :meth:`create_issue`, :meth:`get_issue`, :meth:`add_comment`,
    :meth:`list_issues`, and :meth:`normalize`.

    :meth:`get_issue_types` and :meth:`get_type_properties` have default
    implementations that raise :exc:`NotImplementedError`; subclasses may
    override them to provide real schema discovery. Keeping these methods
    non-abstract preserves backward compatibility for existing adapters.
    """

    @abstractmethod
    def create_issue(self, title: str, description: str, labels: list[str] | None = None) -> IssueResult:
        """Create a new issue.

        Args:
            title: Issue title / summary.
            description: Issue description body.
            labels: Optional list of labels to apply.

        Returns:
            An :class:`IssueResult` with the new issue ID and URL.
        """

    @abstractmethod
    def get_issue(self, issue_id: str) -> IssueDetailWithRaw:
        """Retrieve full details of an issue.

        Args:
            issue_id: Platform-specific issue identifier.

        Returns:
            An :class:`IssueDetailWithRaw` with the issue's metadata and
            comments.  The ``raw`` field may be absent if the adapter does not
            expose the underlying provider response.
        """

    @abstractmethod
    def add_comment(self, issue_id: str, comment: str) -> CommentResult:
        """Add a comment to an existing issue.

        Args:
            issue_id: Platform-specific issue identifier.
            comment: Comment body text.

        Returns:
            A :class:`CommentResult` with the new comment ID.
        """

    @abstractmethod
    def list_issues(self, filters: IssueFilters | None = None) -> list[IssueSummary]:
        """List issues, optionally filtered.

        Args:
            filters: Optional :class:`IssueFilters` to narrow results.

        Returns:
            A list of :class:`IssueSummary` items.
        """

    @abstractmethod
    def normalize(self, issue_detail: IssueDetailWithRaw) -> NormalizedIssue:
        """Normalize a raw issue detail into a provider-agnostic representation.

        Transforms platform-specific :class:`IssueDetailWithRaw` data into a
        uniform :class:`NormalizedIssue` instance suitable for downstream
        consumers (template renderers, spec generators, etc.).

        Args:
            issue_detail: An :class:`IssueDetailWithRaw` containing the full
                issue data and an optional raw provider response payload.

        Returns:
            A :class:`NormalizedIssue` with validated identity fields and
            coerced optional fields.
        """

    # ------------------------------------------------------------------
    # Default (non-abstract) implementations — backward-compatible stubs
    # These methods raise NotImplementedError rather than being declared
    # @abstractmethod so that existing adapters remain instantiable until
    # real schema discovery is implemented (see #1782).
    # ------------------------------------------------------------------

    def get_issue_types(self) -> list[IssueTypeInfo]:
        """Return all issue types available in the configured project or repository.

        The default implementation raises :exc:`NotImplementedError`. Concrete
        subclasses should override this method to provide real discovery.
        Implementations should return at least one entry representing a baseline
        default type when no specific types are discoverable; existing adapters
        that return an empty list remain backward-compatible.

        Returns:
            A list of :class:`IssueTypeInfo` items.
        """
        raise NotImplementedError(f"{type(self).__name__}.get_issue_types() is not yet implemented; see #1782")

    def get_type_properties(self, type_name: str) -> list[PropertySchema]:
        """Return the field schema for a specific issue type identified by name.

        Args:
            type_name: Non-empty string identifying the issue type. Values
                should come from the ``name`` field of entries returned by
                :meth:`get_issue_types`.
                Concrete implementations may raise ``ValueError`` for empty or
                invalid type names; the ABC performs no runtime validation.

        The default implementation raises :exc:`NotImplementedError`. Concrete
        subclasses should override this method to provide real schema discovery.

        Returns:
            A list of :class:`PropertySchema` items describing the type's
            fields.
        """
        raise NotImplementedError(f"{type(self).__name__}.get_type_properties() is not yet implemented; see #1782")
