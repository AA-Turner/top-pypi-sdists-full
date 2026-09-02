"""Tests for agentic_devtools.adapters.base.IssueAdapter."""

from __future__ import annotations

import inspect

import pytest

from agentic_devtools.adapters.base import (
    CommentResult,
    IssueAdapter,
    IssueDetail,
    IssueDetailWithRaw,
    IssueFilters,
    IssueResult,
    IssueSummary,
    IssueTypeInfo,
    NormalizedIssue,
    PropertySchema,
)


class TestIssueAdapter:
    """Tests for the IssueAdapter abstract base class."""

    def test_cannot_instantiate_directly(self) -> None:
        """IssueAdapter is abstract and cannot be instantiated."""
        with pytest.raises(TypeError):
            IssueAdapter()  # type: ignore[abstract]

    def test_incomplete_subclass_raises_type_error(self) -> None:
        """A subclass missing an abstract method cannot be instantiated."""

        class Incomplete(IssueAdapter):
            def create_issue(self, title: str, description: str, labels: list[str] | None = None) -> IssueResult:
                return IssueResult(issue_id="1", url="")

            # Missing get_issue, add_comment, list_issues, normalize

        with pytest.raises(TypeError):
            Incomplete()  # type: ignore[abstract]

    def test_incomplete_subclass_missing_normalize_raises_type_error(self) -> None:
        """A subclass implementing all methods except normalize cannot be instantiated."""

        class MissingNormalize(IssueAdapter):
            def create_issue(self, title: str, description: str, labels: list[str] | None = None) -> IssueResult:
                return IssueResult(issue_id="1", url="")

            def get_issue(self, issue_id: str) -> IssueDetail:
                return IssueDetail(
                    issue_id=issue_id, title="", description="", status="", labels=[], url="", comments=[]
                )

            def add_comment(self, issue_id: str, comment: str) -> CommentResult:
                return CommentResult(comment_id="c1")

            def list_issues(self, filters: IssueFilters | None = None) -> list[IssueSummary]:
                return []

            def get_issue_types(self) -> list[IssueTypeInfo]:
                return []

            def get_type_properties(self, type_name: str) -> list[PropertySchema]:
                return []

        with pytest.raises(TypeError):
            MissingNormalize()  # type: ignore[abstract]

    def test_base_get_issue_types_raises_not_implemented(self) -> None:
        """Subclass inheriting base get_issue_types raises NotImplementedError."""

        class MinimalAdapter(IssueAdapter):
            def create_issue(self, title: str, description: str, labels: list[str] | None = None) -> IssueResult:
                return IssueResult(issue_id="1", url="")

            def get_issue(self, issue_id: str) -> IssueDetail:
                return IssueDetail(
                    issue_id=issue_id, title="", description="", status="", labels=[], url="", comments=[]
                )

            def add_comment(self, issue_id: str, comment: str) -> CommentResult:
                return CommentResult(comment_id="c1")

            def list_issues(self, filters: IssueFilters | None = None) -> list[IssueSummary]:
                return []

            def normalize(self, issue_detail: IssueDetailWithRaw) -> NormalizedIssue:
                return NormalizedIssue(
                    issue_id="1", title="t", description="", status="open", url="http://x", provider="test"
                )

        adapter = MinimalAdapter()
        with pytest.raises(NotImplementedError, match="get_issue_types"):
            adapter.get_issue_types()

    def test_base_get_type_properties_raises_not_implemented(self) -> None:
        """Subclass inheriting base get_type_properties raises NotImplementedError."""

        class MinimalAdapter(IssueAdapter):
            def create_issue(self, title: str, description: str, labels: list[str] | None = None) -> IssueResult:
                return IssueResult(issue_id="1", url="")

            def get_issue(self, issue_id: str) -> IssueDetail:
                return IssueDetail(
                    issue_id=issue_id, title="", description="", status="", labels=[], url="", comments=[]
                )

            def add_comment(self, issue_id: str, comment: str) -> CommentResult:
                return CommentResult(comment_id="c1")

            def list_issues(self, filters: IssueFilters | None = None) -> list[IssueSummary]:
                return []

            def normalize(self, issue_detail: IssueDetailWithRaw) -> NormalizedIssue:
                return NormalizedIssue(
                    issue_id="1", title="t", description="", status="open", url="http://x", provider="test"
                )

        adapter = MinimalAdapter()
        with pytest.raises(NotImplementedError, match="get_type_properties"):
            adapter.get_type_properties("Bug")

    def test_complete_subclass_can_be_instantiated(self) -> None:
        """A subclass implementing all abstract methods can be instantiated."""

        class Complete(IssueAdapter):
            def create_issue(self, title: str, description: str, labels: list[str] | None = None) -> IssueResult:
                return IssueResult(issue_id="1", url="")

            def get_issue(self, issue_id: str) -> IssueDetail:
                return IssueDetail(
                    issue_id=issue_id, title="", description="", status="", labels=[], url="", comments=[]
                )

            def add_comment(self, issue_id: str, comment: str) -> CommentResult:
                return CommentResult(comment_id="c1")

            def list_issues(self, filters: IssueFilters | None = None) -> list[IssueSummary]:
                return []

            def normalize(self, issue_detail: IssueDetailWithRaw) -> NormalizedIssue:
                return NormalizedIssue(
                    issue_id=issue_detail["issue_id"],
                    title=issue_detail["title"],
                    description=issue_detail["description"],
                    status=issue_detail["status"],
                    url=issue_detail["url"],
                    provider="test",
                )

            def get_issue_types(self) -> list[IssueTypeInfo]:
                return []

            def get_type_properties(self, type_name: str) -> list[PropertySchema]:
                return []

        adapter = Complete()
        assert isinstance(adapter, IssueAdapter)

    def test_normalize_signature_parameter_type(self) -> None:
        """normalize() parameter type annotation is IssueDetailWithRaw."""
        hints = inspect.get_annotations(IssueAdapter.normalize, eval_str=True)
        assert hints["issue_detail"] is IssueDetailWithRaw

    def test_normalize_signature_return_type(self) -> None:
        """normalize() return type annotation is NormalizedIssue."""
        hints = inspect.get_annotations(IssueAdapter.normalize, eval_str=True)
        assert hints["return"] is NormalizedIssue

    def test_normalize_has_docstring(self) -> None:
        """normalize() has a non-empty docstring."""
        assert IssueAdapter.normalize.__doc__
        assert len(IssueAdapter.normalize.__doc__.strip()) > 0

    def test_get_issue_types_signature_return_type(self) -> None:
        """get_issue_types() return type annotation is list[IssueTypeInfo]."""
        hints = inspect.get_annotations(IssueAdapter.get_issue_types, eval_str=True)
        assert hints["return"] == list[IssueTypeInfo]

    def test_get_issue_types_has_docstring(self) -> None:
        """get_issue_types() has a non-empty docstring."""
        assert IssueAdapter.get_issue_types.__doc__
        assert len(IssueAdapter.get_issue_types.__doc__.strip()) > 0

    def test_get_type_properties_signature_parameter_type(self) -> None:
        """get_type_properties() type_name parameter is str."""
        hints = inspect.get_annotations(IssueAdapter.get_type_properties, eval_str=True)
        assert hints["type_name"] is str

    def test_get_type_properties_signature_return_type(self) -> None:
        """get_type_properties() return type annotation is list[PropertySchema]."""
        hints = inspect.get_annotations(IssueAdapter.get_type_properties, eval_str=True)
        assert hints["return"] == list[PropertySchema]

    def test_get_type_properties_has_docstring(self) -> None:
        """get_type_properties() has a non-empty docstring."""
        assert IssueAdapter.get_type_properties.__doc__
        assert len(IssueAdapter.get_type_properties.__doc__.strip()) > 0

    def test_class_docstring_does_not_hardcode_method_count(self) -> None:
        """IssueAdapter class docstring does not hard-code a specific method count."""
        docstring = IssueAdapter.__doc__ or ""
        # Should not contain phrases like "four abstract methods" or "five abstract methods"
        assert "four abstract" not in docstring.lower()
        assert "five abstract" not in docstring.lower()
        assert "six abstract" not in docstring.lower()
        assert "seven abstract" not in docstring.lower()
