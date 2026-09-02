"""Example tests demonstrating MockAdapter.normalize() usage.

Shows happy-path patterns for using the shared ``mock_adapter`` and
``sample_issue_data`` fixtures to validate normalization behavior with
both default and custom input data.
"""

from __future__ import annotations

from agentic_devtools.adapters.base import IssueDetailWithRaw, NormalizedIssue
from tests.unit.adapters.mock_adapter import MockAdapter


class TestNormalizeWithDefaults:
    """Tests exercising normalize() with default MockAdapter data."""

    def test_normalize_returns_normalized_issue(self, mock_adapter: MockAdapter) -> None:
        """normalize() returns a NormalizedIssue instance."""
        issue_data = mock_adapter.get_issue("any-id")
        result = mock_adapter.normalize(issue_data)
        assert isinstance(result, NormalizedIssue)

    def test_normalize_preserves_identity_fields(self, mock_adapter: MockAdapter) -> None:
        """normalize() populates non-empty identity fields from input."""
        issue_data = mock_adapter.get_issue("any-id")
        result = mock_adapter.normalize(issue_data)
        assert result.issue_id == "MOCK-42"
        assert result.title == "Mock issue title"
        assert result.url == "https://mock.test/issues/MOCK-42"
        assert result.provider == "mock"

    def test_normalize_populates_description(self, mock_adapter: MockAdapter) -> None:
        """normalize() carries over description from input."""
        issue_data = mock_adapter.get_issue("any-id")
        result = mock_adapter.normalize(issue_data)
        assert result.description == "Mock issue description body."

    def test_normalize_populates_status(self, mock_adapter: MockAdapter) -> None:
        """normalize() carries over status from input."""
        issue_data = mock_adapter.get_issue("any-id")
        result = mock_adapter.normalize(issue_data)
        assert result.status == "open"

    def test_get_issue_returns_isolated_data(self, mock_adapter: MockAdapter) -> None:
        """get_issue() returns data that can be mutated without affecting future calls."""
        issue_data = mock_adapter.get_issue("any-id")
        issue_data["title"] = "Mutated title"
        issue_data["labels"].append("mutated")

        fresh_issue_data = mock_adapter.get_issue("any-id")
        assert fresh_issue_data["title"] == "Mock issue title"
        assert fresh_issue_data["labels"] == ["bug", "test"]


class TestNormalizeWithCustomData:
    """Tests exercising normalize() with custom injected data."""

    def test_normalize_with_sample_fixture(
        self, mock_adapter: MockAdapter, sample_issue_data: IssueDetailWithRaw
    ) -> None:
        """normalize() works with the sample_issue_data fixture."""
        result = mock_adapter.normalize(sample_issue_data)
        assert result.issue_id == "SAMPLE-1"
        assert result.title == "Sample issue for testing"
        assert result.provider == "mock"

    def test_normalize_with_custom_adapter(self) -> None:
        """MockAdapter constructed with custom data normalizes it correctly."""
        custom_data = IssueDetailWithRaw(
            issue_id="CUSTOM-99",
            title="Custom title",
            description="Custom description",
            status="closed",
            labels=["custom"],
            url="https://custom.test/99",
            comments=[],
            provider="custom-provider",
        )
        adapter = MockAdapter(raw_issue_data=custom_data)
        result = adapter.normalize(adapter.get_issue("ignored"))
        assert result.issue_id == "CUSTOM-99"
        assert result.title == "Custom title"
        assert result.status == "closed"
        assert result.provider == "custom-provider"
        assert result.labels == ["custom"]
        assert result.raw == {}

    def test_normalize_preserves_raw_provider_payload(self) -> None:
        """normalize() carries through IssueDetailWithRaw.raw content."""
        custom_data = IssueDetailWithRaw(
            issue_id="CUSTOM-100",
            title="Custom title with raw",
            description="Custom description",
            status="open",
            labels=["custom"],
            url="https://custom.test/100",
            comments=[],
            provider="custom-provider",
            raw={"id": 100, "nested": {"source": "provider"}},
        )
        adapter = MockAdapter(raw_issue_data=custom_data)
        result = adapter.normalize(adapter.get_issue("ignored"))
        assert result.raw == {"id": 100, "nested": {"source": "provider"}}

    def test_normalize_matches_sample_normalized_issue(
        self, mock_adapter: MockAdapter, sample_issue_data: IssueDetailWithRaw, sample_normalized_issue: NormalizedIssue
    ) -> None:
        """normalize(sample_issue_data) matches the pre-built sample_normalized_issue."""
        result = mock_adapter.normalize(sample_issue_data)
        assert result.issue_id == sample_normalized_issue.issue_id
        assert result.title == sample_normalized_issue.title
        assert result.url == sample_normalized_issue.url
        assert result.provider == sample_normalized_issue.provider
