"""Tests for agentic_devtools.adapters.types.NormalizedIssue."""

from __future__ import annotations

import pytest

from agentic_devtools.adapters.exceptions import AdapterValidationError
from agentic_devtools.adapters.types import Comment, NormalizedIssue


class TestNormalizedIssue:
    """Tests for the NormalizedIssue frozen dataclass."""

    def test_happy_path_construction(self) -> None:
        """NormalizedIssue can be constructed with all fields populated."""
        issue = NormalizedIssue(
            issue_id="123",
            title="Test Issue",
            description="A description",
            status="open",
            labels=["bug", "critical"],
            url="https://example.com/issues/123",
            provider="github",
            comments=[{"comment_id": "c1", "body": "hello", "created_at": "2024-01-01"}],
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-02T00:00:00Z",
            raw={"number": 123},
        )
        assert issue.issue_id == "123"
        assert issue.title == "Test Issue"
        assert issue.description == "A description"
        assert issue.status == "open"
        assert issue.labels == ["bug", "critical"]
        assert issue.url == "https://example.com/issues/123"
        assert issue.provider == "github"
        assert issue.comments == [{"comment_id": "c1", "body": "hello", "created_at": "2024-01-01"}]
        assert issue.created_at == "2024-01-01T00:00:00Z"
        assert issue.updated_at == "2024-01-02T00:00:00Z"
        assert issue.raw == {"number": 123}

    def test_frozen_immutability(self) -> None:
        """NormalizedIssue fields cannot be reassigned."""
        issue = NormalizedIssue(
            issue_id="1",
            title="T",
            description="D",
            status="open",
            url="https://x.com/1",
            provider="github",
        )
        with pytest.raises(AttributeError):
            issue.title = "new"  # type: ignore[misc]

    def test_identity_validation_issue_id_none(self) -> None:
        """None issue_id raises AdapterValidationError."""
        with pytest.raises(AdapterValidationError, match="issue_id"):
            NormalizedIssue(
                issue_id=None,  # type: ignore[arg-type]
                title="T",
                description="D",
                status="open",
                url="https://x.com/1",
                provider="github",
            )

    def test_identity_validation_issue_id_empty(self) -> None:
        """Empty issue_id raises AdapterValidationError."""
        with pytest.raises(AdapterValidationError, match="issue_id"):
            NormalizedIssue(
                issue_id="",
                title="T",
                description="D",
                status="open",
                url="https://x.com/1",
                provider="github",
            )

    def test_identity_validation_issue_id_whitespace(self) -> None:
        """Whitespace-only issue_id raises AdapterValidationError."""
        with pytest.raises(AdapterValidationError, match="issue_id"):
            NormalizedIssue(
                issue_id="   ",
                title="T",
                description="D",
                status="open",
                url="https://x.com/1",
                provider="github",
            )

    @pytest.mark.parametrize(
        ("field_name", "field_value"),
        [
            ("issue_id", 123),
            ("title", 123),
            ("url", 123),
            ("provider", 123),
        ],
    )
    def test_identity_validation_fields_require_strings(
        self,
        field_name: str,
        field_value: object,
    ) -> None:
        """Identity fields reject non-string values."""
        kwargs: dict[str, object] = {
            "issue_id": "1",
            "title": "T",
            "description": "D",
            "status": "open",
            "url": "https://x.com/1",
            "provider": "github",
        }
        kwargs[field_name] = field_value

        with pytest.raises(AdapterValidationError, match=field_name):
            NormalizedIssue(**kwargs)  # type: ignore[arg-type]

    def test_identity_validation_title_empty(self) -> None:
        """Empty title raises AdapterValidationError."""
        with pytest.raises(AdapterValidationError, match="title"):
            NormalizedIssue(
                issue_id="1",
                title="",
                description="D",
                status="open",
                url="https://x.com/1",
                provider="github",
            )

    def test_identity_validation_url_empty(self) -> None:
        """Empty url raises AdapterValidationError."""
        with pytest.raises(AdapterValidationError, match="url"):
            NormalizedIssue(
                issue_id="1",
                title="T",
                description="D",
                status="open",
                url="",
                provider="github",
            )

    def test_identity_validation_provider_empty(self) -> None:
        """Empty provider raises AdapterValidationError."""
        with pytest.raises(AdapterValidationError, match="provider"):
            NormalizedIssue(
                issue_id="1",
                title="T",
                description="D",
                status="open",
                url="https://x.com/1",
                provider="",
            )

    def test_coercion_description_none(self) -> None:
        """None description is coerced to empty string."""
        issue = NormalizedIssue(
            issue_id="1",
            title="T",
            description=None,  # type: ignore[arg-type]
            status="open",
            url="https://x.com/1",
            provider="github",
        )
        assert issue.description == ""

    def test_coercion_comments_none(self) -> None:
        """None comments is coerced to empty list."""
        issue = NormalizedIssue(
            issue_id="1",
            title="T",
            description="D",
            status="open",
            url="https://x.com/1",
            provider="github",
            comments=None,  # type: ignore[arg-type]
        )
        assert issue.comments == []

    def test_coercion_labels_non_list(self) -> None:
        """Non-list labels is coerced to empty list."""
        issue = NormalizedIssue(
            issue_id="1",
            title="T",
            description="D",
            status="open",
            url="https://x.com/1",
            provider="github",
            labels="not-a-list",  # type: ignore[arg-type]
        )
        assert issue.labels == []

    def test_coercion_status_none(self) -> None:
        """None status is coerced to 'unknown'."""
        issue = NormalizedIssue(
            issue_id="1",
            title="T",
            description="D",
            status=None,  # type: ignore[arg-type]
            url="https://x.com/1",
            provider="github",
        )
        assert issue.status == "unknown"

    def test_coercion_status_non_string(self) -> None:
        """Non-string status is coerced to 'unknown'."""
        issue = NormalizedIssue(
            issue_id="1",
            title="T",
            description="D",
            status=42,  # type: ignore[arg-type]
            url="https://x.com/1",
            provider="github",
        )
        assert issue.status == "unknown"

    def test_coercion_status_lowercased(self) -> None:
        """Status string is lowercased."""
        issue = NormalizedIssue(
            issue_id="1",
            title="T",
            description="D",
            status="OPEN",
            url="https://x.com/1",
            provider="github",
        )
        assert issue.status == "open"

    def test_import_from_base_module(self) -> None:
        """NormalizedIssue can be imported from agentic_devtools.adapters.base."""
        from agentic_devtools.adapters.base import NormalizedIssue as FromBase

        assert FromBase is NormalizedIssue

    def test_not_hashable(self) -> None:
        """NormalizedIssue raises TypeError on hash() due to mutable fields."""
        issue = NormalizedIssue(
            issue_id="1",
            title="T",
            description="D",
            status="open",
            url="https://x.com/1",
            provider="github",
        )
        with pytest.raises(TypeError, match="unhashable"):
            hash(issue)

    def test_has_docstring(self) -> None:
        """NormalizedIssue has a non-empty class-level docstring."""
        assert NormalizedIssue.__doc__
        assert len(NormalizedIssue.__doc__.strip()) > 0

    def test_defensive_copy_labels(self) -> None:
        """Mutating the original labels list does not affect NormalizedIssue."""
        original_labels = ["bug", "critical"]
        issue = NormalizedIssue(
            issue_id="1",
            title="T",
            description="D",
            status="open",
            url="https://x.com/1",
            provider="github",
            labels=original_labels,
        )
        original_labels.append("new-label")
        assert issue.labels == ["bug", "critical"]

    def test_defensive_copy_comments(self) -> None:
        """Mutating the original comments list does not affect NormalizedIssue."""
        comment: Comment = {"comment_id": "c1", "body": "hello", "created_at": "2024-01-01"}
        original_comments: list[Comment] = [comment]
        issue = NormalizedIssue(
            issue_id="1",
            title="T",
            description="D",
            status="open",
            url="https://x.com/1",
            provider="github",
            comments=original_comments,
        )
        original_comments.append({"comment_id": "c2", "body": "bye", "created_at": "2024-01-02"})
        assert len(issue.comments) == 1
        assert issue.comments[0]["comment_id"] == "c1"

    def test_defensive_copy_raw(self) -> None:
        """Mutating the original raw dict does not affect NormalizedIssue."""
        original_raw: dict[str, int] = {"number": 123}
        issue = NormalizedIssue(
            issue_id="1",
            title="T",
            description="D",
            status="open",
            url="https://x.com/1",
            provider="github",
            raw=original_raw,
        )
        original_raw["extra"] = 999  # type: ignore[assignment]
        assert issue.raw == {"number": 123}
