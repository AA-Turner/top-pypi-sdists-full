"""Tests for _build_metadata in issue_type_discovery."""

from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import patch

from agentic_devtools.cli.config.project_config import (
    IssueTypeEntry,
    ProjectIssueTypesMetadata,
)
from agentic_devtools.cli.setup.issue_type_discovery import _build_metadata


class TestBuildMetadata:
    """Tests for _build_metadata."""

    def test_first_discovery_sets_both_timestamps(self) -> None:
        """First discovery sets lastDiscovered and lastRefreshed to the same value."""
        types: list[IssueTypeEntry] = [
            IssueTypeEntry(id="Bug", name="Bug", description="", is_subtask=False, properties=[])
        ]
        frozen_time = "2026-01-15T10:30:00+00:00"
        with patch("agentic_devtools.cli.setup.issue_type_discovery.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2026, 1, 15, 10, 30, 0, tzinfo=timezone.utc)
            mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)
            result = _build_metadata(types, "jira", existing=None)

        assert result["lastDiscovered"] == frozen_time
        assert result["lastRefreshed"] == frozen_time
        assert result["provider"] == "jira"
        assert result["issue_types"] == types

    def test_refresh_preserves_last_discovered(self) -> None:
        """Refresh preserves lastDiscovered and updates lastRefreshed."""
        types: list[IssueTypeEntry] = [
            IssueTypeEntry(id="Story", name="Story", description="", is_subtask=False, properties=[])
        ]
        existing = ProjectIssueTypesMetadata(
            lastDiscovered="2025-06-01T08:00:00+00:00",
            lastRefreshed="2025-06-01T08:00:00+00:00",
            provider="jira",
            issue_types=[],
        )
        frozen_time = "2026-07-20T14:00:00+00:00"
        with patch("agentic_devtools.cli.setup.issue_type_discovery.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2026, 7, 20, 14, 0, 0, tzinfo=timezone.utc)
            mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)
            result = _build_metadata(types, "github", existing=existing)

        assert result["lastDiscovered"] == "2025-06-01T08:00:00+00:00"
        assert result["lastRefreshed"] == frozen_time
        assert result["provider"] == "github"
        assert result["issue_types"] == types

    def test_empty_types_valid(self) -> None:
        """Empty list of issue types is valid metadata."""
        with patch("agentic_devtools.cli.setup.issue_type_discovery.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
            mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)
            result = _build_metadata([], "markdown", existing=None)

        assert result["issue_types"] == []
        assert result["provider"] == "markdown"

    def test_provider_slug_passed_through(self) -> None:
        """Provider slug from resolver is used directly."""
        with patch("agentic_devtools.cli.setup.issue_type_discovery.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
            mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)
            result = _build_metadata([], "github", existing=None)

        assert result["provider"] == "github"

    def test_update_refreshed_false_preserves_last_refreshed(self) -> None:
        """When update_refreshed=False, lastRefreshed is preserved from existing."""
        types: list[IssueTypeEntry] = [
            IssueTypeEntry(id="Bug", name="Bug", description="", is_subtask=False, properties=[])
        ]
        existing = ProjectIssueTypesMetadata(
            lastDiscovered="2025-06-01T08:00:00+00:00",
            lastRefreshed="2025-06-15T12:00:00+00:00",
            provider="jira",
            issue_types=[],
        )
        with patch("agentic_devtools.cli.setup.issue_type_discovery.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2026, 7, 20, 14, 0, 0, tzinfo=timezone.utc)
            mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)
            result = _build_metadata(types, "jira", existing=existing, update_refreshed=False)

        assert result["lastDiscovered"] == "2025-06-01T08:00:00+00:00"
        assert result["lastRefreshed"] == "2025-06-15T12:00:00+00:00"
