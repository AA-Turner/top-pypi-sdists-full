"""Tests for _eligible_open_pr_count()."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.watchdog_command import _eligible_open_pr_count


class TestEligibleOpenPrCount:
    """Open PR counting and filtering behavior."""

    def test_counts_only_same_repo_prs_without_ignore_label(self) -> None:
        with patch(
            "agentic_devtools.cli.ci.watchdog_command._read_open_pr_page",
            return_value=[
                {
                    "base": {"repo": {"full_name": "o/r"}},
                    "head": {"repo": {"full_name": "o/r"}},
                    "labels": [{"name": "x"}],
                },
                {
                    "base": {"repo": {"full_name": "o/r"}},
                    "head": {"repo": {"full_name": "o/fork"}},
                    "labels": [],
                },
                {
                    "base": {"repo": {"full_name": "o/r"}},
                    "head": {"repo": {"full_name": "o/r"}},
                    "labels": [{"name": "ai-pr-loop-ignore"}],
                },
            ],
        ):
            count = _eligible_open_pr_count("o/r", "token")

        assert count == 1

    def test_raises_when_labels_are_malformed(self) -> None:
        with patch(
            "agentic_devtools.cli.ci.watchdog_command._read_open_pr_page",
            return_value=[
                {
                    "base": {"repo": {"full_name": "o/r"}},
                    "head": {"repo": {"full_name": "o/r"}},
                    "labels": "bad",
                }
            ],
        ):
            with pytest.raises(RuntimeError, match="malformed"):
                _eligible_open_pr_count("o/r", "token")

    def test_raises_when_any_label_entry_is_malformed(self) -> None:
        with patch(
            "agentic_devtools.cli.ci.watchdog_command._read_open_pr_page",
            return_value=[
                {
                    "base": {"repo": {"full_name": "o/r"}},
                    "head": {"repo": {"full_name": "o/r"}},
                    "labels": [{"name": "ok"}, {"name": None}],
                }
            ],
        ):
            with pytest.raises(RuntimeError, match="malformed"):
                _eligible_open_pr_count("o/r", "token")

    def test_raises_when_any_label_item_is_not_a_dict(self) -> None:
        with patch(
            "agentic_devtools.cli.ci.watchdog_command._read_open_pr_page",
            return_value=[
                {
                    "base": {"repo": {"full_name": "o/r"}},
                    "head": {"repo": {"full_name": "o/r"}},
                    "labels": [{"name": "ok"}, "broken"],
                }
            ],
        ):
            with pytest.raises(RuntimeError, match="malformed"):
                _eligible_open_pr_count("o/r", "token")

    def test_reads_additional_pages_until_short_page(self) -> None:
        first_page = [
            {
                "base": {"repo": {"full_name": "o/r"}},
                "head": {"repo": {"full_name": "o/r"}},
                "labels": [],
            }
        ] * 100
        second_page = [
            {
                "base": {"repo": {"full_name": "o/r"}},
                "head": {"repo": {"full_name": "o/r"}},
                "labels": [],
            }
        ]
        with patch(
            "agentic_devtools.cli.ci.watchdog_command._read_open_pr_page",
            side_effect=[first_page, second_page],
        ):
            count = _eligible_open_pr_count("o/r", "token")

        assert count == 101

    def test_stops_after_maximum_open_pr_pages(self) -> None:
        page = [
            {
                "base": {"repo": {"full_name": "o/r"}},
                "head": {"repo": {"full_name": "o/r"}},
                "labels": [],
            }
        ] * 100
        with patch(
            "agentic_devtools.cli.ci.watchdog_command._read_open_pr_page",
            side_effect=[page, page, page, page, page],
        ):
            count = _eligible_open_pr_count("o/r", "token")

        assert count == 500
