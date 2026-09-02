"""Tests for GitHubActionsProvider.get_label_applied_at()."""

from datetime import datetime, timezone
from unittest.mock import patch

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


class TestGetLabelAppliedAt:
    """Most-recent ``labeled`` event timestamp lookup."""

    @patch("agentic_devtools.cli.ci.github_provider._parse_paginated_json")
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_returns_latest_labeled_timestamp(self, _mock_gh, mock_parse) -> None:
        mock_parse.return_value = [
            {"event": "labeled", "label": {"name": "in-progress"}, "created_at": "2026-06-01T10:00:00Z"},
            {"event": "labeled", "label": {"name": "in-progress"}, "created_at": "2026-06-02T10:00:00Z"},
            {"event": "labeled", "label": {"name": "in-progress"}, "created_at": "2026-06-01T05:00:00Z"},
        ]
        provider = GitHubActionsProvider(repo="o/r")
        result = provider.get_label_applied_at(1, "in-progress")
        assert result == datetime(2026, 6, 2, 10, 0, tzinfo=timezone.utc)

    @patch("agentic_devtools.cli.ci.github_provider._parse_paginated_json")
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_ignores_other_events_labels_and_bad_dates(self, _mock_gh, mock_parse) -> None:
        mock_parse.return_value = [
            {"event": "closed"},
            {"event": "labeled", "label": {"name": "other"}, "created_at": "2026-06-02T10:00:00Z"},
            {"event": "labeled", "label": {}, "created_at": "2026-06-02T10:00:00Z"},
            {"event": "labeled", "label": {"name": "in-progress"}, "created_at": ""},
            {"event": "labeled", "label": {"name": "in-progress"}, "created_at": "bad-date"},
            {"event": "labeled", "label": {"name": "in-progress"}, "created_at": "2026-06-03T10:00:00Z"},
        ]
        provider = GitHubActionsProvider(repo="o/r")
        result = provider.get_label_applied_at(1, "in-progress")
        assert result == datetime(2026, 6, 3, 10, 0, tzinfo=timezone.utc)

    @patch("agentic_devtools.cli.ci.github_provider._parse_paginated_json")
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_no_matching_event_returns_none(self, _mock_gh, mock_parse) -> None:
        mock_parse.return_value = [{"event": "closed"}]
        provider = GitHubActionsProvider(repo="o/r")
        assert provider.get_label_applied_at(1, "in-progress") is None

    @patch("agentic_devtools.cli.ci.github_provider._parse_paginated_json")
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_non_list_events_returns_none(self, _mock_gh, mock_parse) -> None:
        mock_parse.return_value = {"unexpected": "object"}
        provider = GitHubActionsProvider(repo="o/r")
        assert provider.get_label_applied_at(1, "in-progress") is None
