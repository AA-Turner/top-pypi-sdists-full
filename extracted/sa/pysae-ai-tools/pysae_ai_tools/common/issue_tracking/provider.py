"""The ``IssueTrackingProvider`` contract shared by every host implementation.

Operations that some hosts lack — epics and owner-scoped (group) labels, which
GitHub has no native equivalent for — are gated behind :class:`Capability`.
A provider declares what it supports via ``capabilities``; calling a gated
operation on a provider that lacks it raises :class:`UnsupportedCapability`
rather than failing obscurely deep in an API call.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import ClassVar

from .models import Epic, Issue, Label
from .platform import Platform


class Capability(str, Enum):
    """An operation that only some host platforms support."""

    EPICS = "epics"
    OWNER_LABELS = "owner_labels"


class UnsupportedCapability(RuntimeError):
    """Raised when a gated operation is called on a provider that lacks it."""

    def __init__(self, platform: Platform, capability: Capability) -> None:
        self.platform = platform
        self.capability = capability
        super().__init__(f"{platform.value} provider does not support capability {capability.value!r}")


class IssueTrackingProvider(ABC):
    """Host-agnostic gateway for issue, epic and label operations.

    Concrete providers set ``platform`` and ``capabilities`` and implement every
    method. Gated methods (epics, owner labels) must call :meth:`require` first so
    an unsupported host fails with :class:`UnsupportedCapability`.
    """

    platform: ClassVar[Platform]
    capabilities: ClassVar[frozenset[Capability]] = frozenset()

    def supports(self, capability: Capability) -> bool:
        return capability in self.capabilities

    def require(self, capability: Capability) -> None:
        if not self.supports(capability):
            raise UnsupportedCapability(self.platform, capability)

    # ─── Issues ──────────────────────────────────────────────────────────────

    @abstractmethod
    def current_user(self) -> str:
        """Username of the authenticated account."""

    @abstractmethod
    def get_issue(self, iid: str) -> Issue:
        """Fetch a single issue by its number."""

    @abstractmethod
    def create_issue(
        self,
        *,
        title: str,
        description: str,
        labels: list[str],
        assignees: list[str],
        weight: int | None = None,
    ) -> Issue:
        """Create an issue and return it."""

    @abstractmethod
    def update_issue(
        self,
        iid: str,
        *,
        title: str | None = None,
        description: str | None = None,
        add_labels: list[str] | None = None,
        remove_labels: list[str] | None = None,
    ) -> Issue:
        """Update an issue's title, description, or label set."""

    @abstractmethod
    def close_issue(self, iid: str) -> Issue:
        """Close an issue, returning its updated state.

        Pure state transition: it does not touch labels (``workflow::`` columns
        stay as the caller left them — board logic is another layer). Idempotent:
        closing an already-closed issue succeeds. Not gated by a capability —
        every host supports closing natively.
        """

    @abstractmethod
    def reopen_issue(self, iid: str) -> Issue:
        """Reopen a closed issue, returning its updated state. Idempotent."""

    @abstractmethod
    def list_issues(
        self,
        *,
        search: str | None = None,
        assignee: str | None = None,
        labels: list[str] | None = None,
        state: str = "opened",
    ) -> list[Issue]:
        """List issues of the project, optionally filtered."""

    @abstractmethod
    def add_note(self, iid: str, body: str) -> None:
        """Post a comment on an issue."""

    # ─── Owner-scoped labels (Capability.OWNER_LABELS) ───────────────────────

    @abstractmethod
    def ensure_owner_label(self, name: str, *, color: str = "", description: str = "") -> Label:
        """Create the owner-scoped label if absent, returning it either way."""

    # ─── Epics (Capability.EPICS) ────────────────────────────────────────────

    @abstractmethod
    def list_open_epics(self) -> list[Epic]:
        """Every open epic under the owner namespace."""

    @abstractmethod
    def get_epic(self, iid: str) -> Epic:
        """Fetch a single epic by its number."""

    @abstractmethod
    def create_epic(self, *, title: str, description: str = "", labels: list[str] | None = None) -> Epic:
        """Create an epic under the owner namespace."""

    @abstractmethod
    def update_epic(
        self,
        iid: str,
        *,
        title: str | None = None,
        description: str | None = None,
        add_labels: list[str] | None = None,
        remove_labels: list[str] | None = None,
    ) -> Epic:
        """Update an epic's title, description, or label set."""

    @abstractmethod
    def attach_to_epic(self, issue_iid: str, epic_iid: str, *, project: str | None = None) -> None:
        """Attach an issue to an epic.

        ``project`` targets a repo other than the context's (for cross-project
        attachment to an owner-level epic); a bare name is namespaced under the
        owner. Defaults to the context's project.
        """
