"""Tests for _latest_merged_at()."""

import json
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.watchdog_command import _latest_merged_at


class TestLatestMergedAt:
    """Merged PR inventory parsing."""

    def test_returns_greatest_merged_at_in_page(self) -> None:
        payload = (
            '[{"updated_at":"2026-09-02T11:00:00Z","merged_at":"2026-09-02T11:00:00Z"},'
            '{"updated_at":"2026-09-02T10:00:00Z","merged_at":"2026-09-02T10:00:00Z"},'
            '{"updated_at":"2026-09-02T12:00:00Z","merged_at":"2026-09-02T12:00:00Z"}]'
        )
        with patch("agentic_devtools.cli.ci.watchdog_command._gh_api", return_value=payload):
            merged_at = _latest_merged_at("o/r", "main", "token")

        assert merged_at == "2026-09-02T12:00:00Z"

    def test_returns_none_when_no_merged_pr_exists(self) -> None:
        with patch("agentic_devtools.cli.ci.watchdog_command._gh_api", return_value="[]"):
            assert _latest_merged_at("o/r", "main", "token") is None

    def test_ignores_unmerged_entries_with_null_merge_timestamp(self) -> None:
        with patch(
            "agentic_devtools.cli.ci.watchdog_command._gh_api",
            return_value='[{"updated_at":"2026-09-02T10:00:00Z","merged_at":null}]',
        ):
            assert _latest_merged_at("o/r", "main", "token") is None

    def test_rejects_malformed_payload(self) -> None:
        with patch("agentic_devtools.cli.ci.watchdog_command._gh_api", return_value='{"x":1}'):
            with pytest.raises(RuntimeError, match="malformed"):
                _latest_merged_at("o/r", "main", "token")

    def test_rejects_non_dict_entries(self) -> None:
        with patch("agentic_devtools.cli.ci.watchdog_command._gh_api", return_value="[1]"):
            with pytest.raises(RuntimeError, match="malformed"):
                _latest_merged_at("o/r", "main", "token")

    def test_rejects_invalid_merged_at_string(self) -> None:
        with patch(
            "agentic_devtools.cli.ci.watchdog_command._gh_api",
            return_value='[{"updated_at":"2026-09-02T10:00:00Z","merged_at":"bad"}]',
        ):
            with pytest.raises(RuntimeError, match="invalid merge date"):
                _latest_merged_at("o/r", "main", "token")

    def test_rejects_empty_merged_at_values(self) -> None:
        with patch(
            "agentic_devtools.cli.ci.watchdog_command._gh_api",
            return_value='[{"updated_at":"2026-09-02T10:00:00Z","merged_at":" "}]',
        ):
            with pytest.raises(RuntimeError, match="malformed"):
                _latest_merged_at("o/r", "main", "token")

    def test_paginates_closed_pr_inventory_to_find_recent_merge(self) -> None:
        first_page = [{"updated_at": "2026-09-02T13:00:00Z", "merged_at": None} for _ in range(100)]
        second_page = [{"updated_at": "2026-09-02T11:00:00Z", "merged_at": "2026-09-02T10:00:00Z"}]
        with patch(
            "agentic_devtools.cli.ci.watchdog_command._gh_api",
            side_effect=[json.dumps(first_page), json.dumps(second_page)],
        ) as gh_api:
            merged_at = _latest_merged_at("o/r", "main", "token")

        assert merged_at == "2026-09-02T10:00:00Z"
        assert gh_api.call_count == 2

    def test_rejects_non_json_payload(self) -> None:
        with patch("agentic_devtools.cli.ci.watchdog_command._gh_api", return_value="not-json"):
            with pytest.raises(RuntimeError, match="malformed"):
                _latest_merged_at("o/r", "main", "token")

    def test_rejects_missing_updated_at_values(self) -> None:
        with patch("agentic_devtools.cli.ci.watchdog_command._gh_api", return_value='[{"merged_at":null}]'):
            with pytest.raises(RuntimeError, match="malformed"):
                _latest_merged_at("o/r", "main", "token")

    def test_rejects_invalid_updated_at_string(self) -> None:
        with patch(
            "agentic_devtools.cli.ci.watchdog_command._gh_api",
            return_value='[{"updated_at":"not-a-date","merged_at":null}]',
        ):
            with pytest.raises(RuntimeError, match="invalid update date"):
                _latest_merged_at("o/r", "main", "token")

    def test_stops_after_first_page_once_older_updates_cannot_beat_latest_merge(self) -> None:
        first_page = [
            {"updated_at": "2026-09-02T12:00:00Z", "merged_at": "2026-09-02T12:00:00Z"}
            if index == 0
            else {"updated_at": "2026-09-02T11:00:00Z", "merged_at": None}
            for index in range(100)
        ]
        with patch("agentic_devtools.cli.ci.watchdog_command._gh_api", return_value=json.dumps(first_page)) as gh_api:
            merged_at = _latest_merged_at("o/r", "main", "token")

        assert merged_at == "2026-09-02T12:00:00Z"
        gh_api.assert_called_once()

    def test_returns_none_when_closed_pr_scan_budget_is_zero(self) -> None:
        with patch("agentic_devtools.cli.ci.watchdog_command.REDISPATCH_MAX_CLOSED_PR_PAGES", 0):
            assert _latest_merged_at("o/r", "main", "token") is None
