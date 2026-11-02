"""Tests for GitHubActionsProvider.list_closed_prs() method."""

import json
from unittest.mock import patch

import pytest

from agentic_devtools.cli.audit.models import ClosedPRInfo
from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.retry import ProviderRateLimitError


def _mock_run_safe_response(data):
    class _Result:
        returncode = 0
        stdout = json.dumps(data) if isinstance(data, (dict, list)) else data
        stderr = ""

    return _Result()


def _mock_run_safe_error(stderr_text: str = "API error"):
    class _ErrorResult:
        returncode = 1
        stdout = ""
        stderr = stderr_text

    return _ErrorResult()


class TestListClosedPrs:
    """Tests for GitHubActionsProvider.list_closed_prs()."""

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_returns_closed_pr_info_list(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_run_safe_response(
            {
                "total_count": 2,
                "items": [
                    {
                        "number": 10,
                        "title": "feat: add feature",
                        "html_url": "https://github.com/owner/repo/pull/10",
                        "closed_at": "2026-01-02T00:00:00Z",
                        "pull_request": {"merged_at": "2026-01-02T00:00:00Z"},
                    },
                    {
                        "number": 5,
                        "title": "fix: bug fix",
                        "html_url": "https://github.com/owner/repo/pull/5",
                        "closed_at": "2026-01-01T00:00:00Z",
                        "pull_request": {"merged_at": None},
                    },
                ],
            }
        )

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_closed_prs(exclude_labels=["audited"], limit=10)

        assert len(result) == 2
        assert all(isinstance(r, ClosedPRInfo) for r in result)
        assert result[0].number == 10
        assert result[0].merged is True
        assert result[1].number == 5
        assert result[1].merged is False

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_sorted_by_closed_at_descending(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_run_safe_response(
            {
                "total_count": 2,
                "items": [
                    {
                        "number": 1,
                        "title": "older",
                        "html_url": "",
                        "closed_at": "2026-01-01T00:00:00Z",
                        "pull_request": {"merged_at": None},
                    },
                    {
                        "number": 2,
                        "title": "newer",
                        "html_url": "",
                        "closed_at": "2026-01-02T00:00:00Z",
                        "pull_request": {"merged_at": None},
                    },
                ],
            }
        )

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_closed_prs(exclude_labels=["audited"], limit=10)

        assert result[0].number == 2  # newer first
        assert result[1].number == 1

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_empty_results(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_run_safe_response({"total_count": 0, "items": []})

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_closed_prs(exclude_labels=["audited"], limit=10)

        assert result == []

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_omits_repo_qualifier_when_repo_is_empty(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_run_safe_response({"total_count": 0, "items": []})

        provider = GitHubActionsProvider(repo="")
        provider.list_closed_prs(exclude_labels=["audited"], limit=10)

        args = mock_run_safe.call_args[0][0]
        endpoint = [a for a in args if "/search/issues" in a][0]
        assert "repo%3A" not in endpoint and "repo:" not in endpoint

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_respects_limit(self, mock_run_safe) -> None:
        items = [
            {
                "number": i,
                "title": f"PR {i}",
                "html_url": "",
                "closed_at": f"2026-01-0{i}T00:00:00Z",
                "pull_request": {"merged_at": None},
            }
            for i in range(1, 6)
        ]
        mock_run_safe.return_value = _mock_run_safe_response({"total_count": 5, "items": items})

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_closed_prs(exclude_labels=["audited"], limit=3)

        assert len(result) == 3

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_paginates_when_limit_exceeds_100(self, mock_run_safe) -> None:
        """When limit > 100 the method makes multiple API calls to collect all results."""

        def make_item(number: int) -> dict:
            return {
                "number": number,
                "title": f"PR {number}",
                "html_url": "",
                "closed_at": "2026-01-01T00:00:00Z",
                "pull_request": {"merged_at": None},
            }

        page1_items = [make_item(i) for i in range(1, 101)]  # 100 items — full page
        page2_items = [make_item(i) for i in range(101, 151)]  # 50 items — last page

        mock_run_safe.side_effect = [
            _mock_run_safe_response({"total_count": 150, "items": page1_items}),
            _mock_run_safe_response({"total_count": 150, "items": page2_items}),
        ]

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_closed_prs(exclude_labels=["audited"], limit=150)

        assert len(result) == 150
        # Two API calls should have been made
        assert mock_run_safe.call_count == 2

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_stops_pagination_when_api_returns_no_more_items(self, mock_run_safe) -> None:
        """Pagination stops early when an API page returns fewer items than requested."""

        def make_item(number: int) -> dict:
            return {
                "number": number,
                "title": f"PR {number}",
                "html_url": "",
                "closed_at": "2026-01-01T00:00:00Z",
                "pull_request": {"merged_at": None},
            }

        page1_items = [make_item(i) for i in range(1, 101)]  # 100 items
        page2_items = [make_item(i) for i in range(101, 131)]  # 30 items — signals end

        mock_run_safe.side_effect = [
            _mock_run_safe_response({"total_count": 130, "items": page1_items}),
            _mock_run_safe_response({"total_count": 130, "items": page2_items}),
            # A third call should NOT happen
            _mock_run_safe_response({"total_count": 0, "items": []}),
        ]

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_closed_prs(exclude_labels=["audited"], limit=200)

        assert len(result) == 130
        assert mock_run_safe.call_count == 2

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_falls_back_to_pulls_endpoint_when_merged_at_absent(self, mock_run_safe) -> None:
        """When merged_at is not in the pull_request dict, falls back to /pulls/{number}."""
        # Search result with pull_request dict that has NO merged_at key
        search_response = {
            "total_count": 1,
            "items": [
                {
                    "number": 7,
                    "title": "old PR without merged_at",
                    "html_url": "https://github.com/owner/repo/pull/7",
                    "closed_at": "2026-01-01T00:00:00Z",
                    "pull_request": {},  # merged_at key absent
                },
            ],
        }
        # Fallback lookup response for /repos/owner/repo/pulls/7
        pulls_response = {"number": 7, "merged": True}

        mock_run_safe.side_effect = [
            _mock_run_safe_response(search_response),
            _mock_run_safe_response(pulls_response),
        ]

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_closed_prs(exclude_labels=["audited"], limit=10)

        assert len(result) == 1
        # merged should be True from the fallback lookup
        assert result[0].merged is True
        assert mock_run_safe.call_count == 2

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_falls_back_to_pulls_endpoint_merged_false_when_not_merged(self, mock_run_safe) -> None:
        """Fallback returns merged=False when the pulls endpoint says merged=False."""
        search_response = {
            "total_count": 1,
            "items": [
                {
                    "number": 9,
                    "title": "closed not merged",
                    "html_url": "",
                    "closed_at": "2026-01-01T00:00:00Z",
                    "pull_request": {},  # merged_at key absent
                },
            ],
        }
        pulls_response = {"number": 9, "merged": False}

        mock_run_safe.side_effect = [
            _mock_run_safe_response(search_response),
            _mock_run_safe_response(pulls_response),
        ]

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_closed_prs(exclude_labels=["audited"], limit=10)

        assert result[0].merged is False

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_fallback_returns_false_when_no_repo_configured(self, mock_run_safe) -> None:
        """_get_pr_merged_status returns False immediately when repo is not set."""
        search_response = {
            "total_count": 1,
            "items": [
                {
                    "number": 3,
                    "title": "PR",
                    "html_url": "",
                    "closed_at": "2026-01-01T00:00:00Z",
                    "pull_request": {},  # merged_at absent
                },
            ],
        }
        mock_run_safe.return_value = _mock_run_safe_response(search_response)

        provider = GitHubActionsProvider(repo="")
        result = provider.list_closed_prs(exclude_labels=[], limit=10)

        assert result[0].merged is False
        # Only one call (search) — no fallback attempted without a repo
        assert mock_run_safe.call_count == 1

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_merged_status_defaults_to_false_when_pulls_api_fails(self, mock_run_safe) -> None:
        """merged defaults to False when the pulls API call raises."""
        search_response = {
            "total_count": 1,
            "items": [
                {
                    "number": 11,
                    "title": "PR",
                    "html_url": "",
                    "closed_at": "2026-01-01T00:00:00Z",
                    "pull_request": {},  # merged_at absent — triggers fallback
                },
            ],
        }

        mock_run_safe.side_effect = [
            _mock_run_safe_response(search_response),
            _mock_run_safe_error("Internal Server Error 500"),
        ]

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_closed_prs(exclude_labels=[], limit=10)

        # Exception is caught; merged defaults to False
        assert result[0].merged is False
        assert mock_run_safe.call_count == 2

    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_merged_status_rate_limit_is_propagated(self, mock_run_safe, _mock_sleep) -> None:
        search_response = {
            "total_count": 1,
            "items": [
                {
                    "number": 11,
                    "title": "PR",
                    "html_url": "",
                    "closed_at": "2026-01-01T00:00:00Z",
                    "pull_request": {},
                },
            ],
        }
        mock_run_safe.side_effect = [
            _mock_run_safe_response(search_response),
            ProviderRateLimitError(provider="github", is_rate_limit=True),
        ]

        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(ProviderRateLimitError):
            provider.list_closed_prs(exclude_labels=[], limit=10)
