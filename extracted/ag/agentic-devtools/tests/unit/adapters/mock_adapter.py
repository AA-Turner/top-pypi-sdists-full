"""MockAdapter — test-only IssueAdapter implementation.

Provides a deterministic, network-free implementation of the full
:class:`~agentic_devtools.adapters.base.IssueAdapter` contract for use in
unit tests. Not shipped in the installable package.
"""

from __future__ import annotations

import copy

from agentic_devtools.adapters.base import (
    CommentResult,
    IssueAdapter,
    IssueDetailWithRaw,
    IssueFilters,
    IssueResult,
    IssueSummary,
    IssueTypeInfo,
    NormalizedIssue,
    PropertySchema,
)


class MockAdapter(IssueAdapter):
    """Deterministic mock implementing all IssueAdapter methods.

    Constructor accepts optional overrides for raw issue data and schema
    discovery responses. When no overrides are provided, methods return
    sensible hardcoded defaults.

    Args:
        raw_issue_data: Optional pre-built :class:`IssueDetailWithRaw` returned
            by :meth:`get_issue`.
        issue_types: Optional list of :class:`IssueTypeInfo` dicts to return
            from :meth:`get_issue_types`. Defaults to canonical bug/feature/task.
        type_properties: Optional mapping of type name to list of
            :class:`PropertySchema` dicts for :meth:`get_type_properties`.
    """

    def __init__(
        self,
        raw_issue_data: IssueDetailWithRaw | None = None,
        issue_types: list[IssueTypeInfo] | None = None,
        type_properties: dict[str, list[PropertySchema]] | None = None,
    ) -> None:
        self._raw_issue_data: IssueDetailWithRaw = (
            copy.deepcopy(raw_issue_data) if raw_issue_data is not None else _default_issue_data()
        )
        self._issue_types: list[IssueTypeInfo] = (
            copy.deepcopy(issue_types) if issue_types is not None else _default_issue_types()
        )
        self._type_properties: dict[str, list[PropertySchema]] = (
            copy.deepcopy(type_properties) if type_properties is not None else _default_type_properties()
        )

    # ------------------------------------------------------------------
    # Abstract method implementations
    # ------------------------------------------------------------------

    def create_issue(self, title: str, description: str, labels: list[str] | None = None) -> IssueResult:
        """Return a deterministic issue creation result."""
        return IssueResult(issue_id="MOCK-1", url="https://mock.test/MOCK-1")

    def get_issue(self, issue_id: str) -> IssueDetailWithRaw:
        """Return the injected raw issue data or defaults."""
        return copy.deepcopy(self._raw_issue_data)

    def add_comment(self, issue_id: str, comment: str) -> CommentResult:
        """Return a deterministic comment result."""
        return CommentResult(comment_id="comment-1")

    def list_issues(self, filters: IssueFilters | None = None) -> list[IssueSummary]:
        """Return a single-item list with a summary derived from raw data."""
        data = self.get_issue("any")
        return [
            IssueSummary(
                issue_id=data["issue_id"],
                title=data["title"],
                status=data["status"],
                labels=data["labels"],
                url=data["url"],
            )
        ]

    def normalize(self, issue_detail: IssueDetailWithRaw) -> NormalizedIssue:
        """Normalize issue detail into a provider-agnostic representation."""
        return NormalizedIssue(
            issue_id=issue_detail["issue_id"],
            title=issue_detail["title"],
            description=issue_detail.get("description", ""),
            status=issue_detail.get("status", "unknown"),
            url=issue_detail["url"],
            provider=issue_detail.get("provider") or "mock",
            labels=issue_detail.get("labels", []),
            comments=issue_detail.get("comments", []),
            raw=issue_detail.get("raw") or {},
        )

    # ------------------------------------------------------------------
    # Schema discovery overrides
    # ------------------------------------------------------------------

    def get_issue_types(self) -> list[IssueTypeInfo]:
        """Return configured issue types (canonical defaults or overrides)."""
        return copy.deepcopy(self._issue_types)

    def get_type_properties(self, type_name: str) -> list[PropertySchema]:
        """Return property schema for the given type name."""
        return copy.deepcopy(self._type_properties.get(type_name, []))


# ---------------------------------------------------------------------------
# Default data factories
# ---------------------------------------------------------------------------


def _default_issue_data() -> IssueDetailWithRaw:
    """Return a canonical test issue with required and common optional fields."""
    return IssueDetailWithRaw(
        issue_id="MOCK-42",
        title="Mock issue title",
        description="Mock issue description body.",
        status="open",
        labels=["bug", "test"],
        url="https://mock.test/issues/MOCK-42",
        comments=[],
        provider="mock",
    )


def _default_issue_types() -> list[IssueTypeInfo]:
    """Return canonical bug/feature/task issue types."""
    return [
        IssueTypeInfo(name="bug", description="A software defect or error"),
        IssueTypeInfo(name="feature", description="A new feature request"),
        IssueTypeInfo(name="task", description="A general development task"),
    ]


def _default_type_properties() -> dict[str, list[PropertySchema]]:
    """Return fixed property schemas per canonical type."""
    return {
        "bug": [
            PropertySchema(name="summary", type="string", required=True, allowed_values=None),
            PropertySchema(name="severity", type="string", required=False, allowed_values=["low", "medium", "high"]),
        ],
        "feature": [
            PropertySchema(name="summary", type="string", required=True, allowed_values=None),
            PropertySchema(name="priority", type="string", required=False, allowed_values=["low", "medium", "high"]),
        ],
        "task": [
            PropertySchema(name="summary", type="string", required=True, allowed_values=None),
        ],
    }
