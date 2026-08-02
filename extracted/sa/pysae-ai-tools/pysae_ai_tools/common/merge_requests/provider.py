"""The ``MergeRequestProvider`` contract shared by every host implementation.

Mirror of :mod:`pysae_ai_tools.common.issue_tracking.provider` for merge
requests / pull requests. Operations that only some hosts render identically —
approvals (GitHub forbids self-approval, GitLab allows it by default) and
server-side rebase (GitHub has no endpoint) — are gated behind :class:`Capability`.
A provider declares what it supports via ``capabilities``; calling a gated
operation on a provider that lacks it raises :class:`UnsupportedCapability`
rather than failing obscurely deep in an API call.

``RepoContext`` and ``Platform`` are reused verbatim from ``issue_tracking`` —
they are host-generic coordinates, not issue-specific.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import ClassVar

from ..issue_tracking.platform import Platform
from .models import MergeRequest, Note


class Capability(str, Enum):
    """An operation that only some host platforms support."""

    APPROVALS = "approvals"
    REBASE = "rebase"


class UnsupportedCapability(RuntimeError):
    """Raised when a gated operation is called on a provider that lacks it."""

    def __init__(self, platform: Platform, capability: Capability) -> None:
        self.platform = platform
        self.capability = capability
        super().__init__(f"{platform.value} provider does not support capability {capability.value!r}")


class MergeRequestProvider(ABC):
    """Host-agnostic gateway for merge-request / pull-request operations.

    Concrete providers set ``platform`` and ``capabilities`` and implement every
    method. Gated methods (approve, rebase) must call :meth:`require` first so an
    unsupported host fails with :class:`UnsupportedCapability`.
    """

    platform: ClassVar[Platform]
    capabilities: ClassVar[frozenset[Capability]] = frozenset()

    def supports(self, capability: Capability) -> bool:
        return capability in self.capabilities

    def require(self, capability: Capability) -> None:
        if not self.supports(capability):
            raise UnsupportedCapability(self.platform, capability)

    # ─── Core operations (every host) ────────────────────────────────────────

    @abstractmethod
    def current_user(self) -> str:
        """Username of the authenticated account."""

    @abstractmethod
    def get_mr(self, iid: str) -> MergeRequest:
        """Fetch a single merge request by its number."""

    @abstractmethod
    def create_mr(
        self,
        *,
        title: str,
        description: str,
        source_branch: str,
        target_branch: str,
        labels: list[str],
        assignees: list[str],
        draft: bool = False,
        remove_source_branch: bool = False,
    ) -> MergeRequest:
        """Open a merge request and return it.

        ``remove_source_branch`` requests deleting the source branch on merge; it
        is honoured where the host supports it at creation (GitLab) and ignored
        otherwise (GitHub deletes branches through a repo-level setting).
        """

    @abstractmethod
    def update_mr(
        self,
        iid: str,
        *,
        title: str | None = None,
        description: str | None = None,
        add_labels: list[str] | None = None,
        remove_labels: list[str] | None = None,
        draft: bool | None = None,
    ) -> MergeRequest:
        """Update a merge request's title, body, label set, or draft state."""

    @abstractmethod
    def list_mrs(
        self,
        *,
        search: str | None = None,
        author: str | None = None,
        assignee: str | None = None,
        labels: list[str] | None = None,
        state: str = "opened",
    ) -> list[MergeRequest]:
        """List merge requests of the project, optionally filtered."""

    @abstractmethod
    def add_note(self, iid: str, body: str) -> None:
        """Post a comment on a merge request."""

    @abstractmethod
    def list_notes(self, iid: str) -> list[Note]:
        """List the comments on a merge request (each with its author's username)."""

    @abstractmethod
    def update_note(self, iid: str, note_id: str, body: str) -> None:
        """Edit an existing comment on a merge request."""

    @abstractmethod
    def set_reviewers(self, iid: str, usernames: list[str]) -> None:
        """Set the merge request's reviewers to exactly ``usernames``."""

    @abstractmethod
    def merge(self, iid: str) -> MergeRequest:
        """Merge the request server-side, letting the host apply its project defaults."""

    # ─── Approvals (Capability.APPROVALS) ────────────────────────────────────

    @abstractmethod
    def approve(self, iid: str) -> None:
        """Approve the merge request (GitLab approval / GitHub APPROVE review)."""

    @abstractmethod
    def approvals_count(self, iid: str) -> int:
        """Number of current approvals (GitLab ``approved_by`` / GitHub APPROVE reviews).

        On-demand (a dedicated API call), never folded into :meth:`get_mr`, so the
        merge poll loop stays cheap.
        """

    # ─── Rebase (Capability.REBASE) ──────────────────────────────────────────

    @abstractmethod
    def rebase(self, iid: str) -> None:
        """Rebase the merge request onto its target branch, server-side."""
