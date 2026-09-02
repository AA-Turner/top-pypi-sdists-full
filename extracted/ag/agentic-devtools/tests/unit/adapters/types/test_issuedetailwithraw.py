"""Tests for agentic_devtools.adapters.types.IssueDetailWithRaw."""

from __future__ import annotations

from agentic_devtools.adapters.types import IssueDetail, IssueDetailWithRaw


class TestIssueDetailWithRaw:
    """Tests for the IssueDetailWithRaw TypedDict."""

    def test_construction_with_raw(self) -> None:
        """IssueDetailWithRaw can be constructed with a raw field."""
        detail: IssueDetailWithRaw = {
            "issue_id": "123",
            "title": "Test",
            "description": "Desc",
            "status": "open",
            "labels": ["bug"],
            "url": "https://example.com/123",
            "comments": [],
            "raw": {"full_response": True},
        }
        assert detail["raw"] == {"full_response": True}
        assert detail["issue_id"] == "123"

    def test_extends_issue_detail(self) -> None:
        """IssueDetailWithRaw extends IssueDetail (has all base fields)."""
        # Verify that all required keys from IssueDetail are present in IssueDetailWithRaw
        for key in IssueDetail.__required_keys__:
            assert key in IssueDetailWithRaw.__required_keys__ | IssueDetailWithRaw.__optional_keys__

    def test_raw_field_is_optional(self) -> None:
        """The raw field is optional (total=False)."""
        assert "raw" in IssueDetailWithRaw.__optional_keys__
