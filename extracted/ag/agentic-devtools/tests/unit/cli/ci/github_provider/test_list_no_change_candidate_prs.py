"""Tests for GitHubActionsProvider.list_no_change_candidate_prs()."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.retry import RetryableError


def _response(*, nodes: list[object], has_next_page: bool = False, end_cursor: str | None = None) -> dict:
    return {
        "data": {
            "repository": {
                "pullRequests": {
                    "nodes": nodes,
                    "pageInfo": {"hasNextPage": has_next_page, "endCursor": end_cursor},
                }
            }
        }
    }


class TestListNoChangeCandidatePrs:
    """Tests for the open-PR listing that feeds the suppressed-triage reaper."""

    def test_maps_every_field_of_a_candidate(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        with patch.object(
            GitHubActionsProvider,
            "graphql",
            return_value=_response(
                nodes=[
                    {
                        "number": 12,
                        "author": {"login": "copilot-swe-agent", "__typename": "Bot"},
                        "body": "no change",
                        "additions": 0,
                        "deletions": 0,
                        "changedFiles": 0,
                        "headRefName": "copilot/triage-1240",
                        "isCrossRepository": False,
                    }
                ]
            ),
        ):
            briefs = provider.list_no_change_candidate_prs()

        assert len(briefs) == 1
        brief = briefs[0]
        assert brief.number == 12
        assert brief.author_login == "copilot-swe-agent[bot]"
        assert brief.body == "no change"
        assert (brief.changed_files, brief.additions, brief.deletions) == (0, 0, 0)
        assert brief.head_branch == "copilot/triage-1240"
        assert brief.is_cross_repository is False

    def test_skips_non_dict_nodes_and_invalid_numbers(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        with patch.object(
            GitHubActionsProvider,
            "graphql",
            return_value=_response(
                nodes=[
                    "not-a-dict",
                    {"number": 0},
                    {"number": -1},
                    {"number": "x"},
                    {"number": 5, "author": {"login": "human", "__typename": "User"}},
                ]
            ),
        ):
            briefs = provider.list_no_change_candidate_prs()

        assert [b.number for b in briefs] == [5]
        assert briefs[0].author_login == "human"

    def test_defaults_missing_optional_fields(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        with patch.object(
            GitHubActionsProvider,
            "graphql",
            return_value=_response(nodes=[{"number": 7, "author": None}]),
        ):
            (brief,) = provider.list_no_change_candidate_prs()

        assert brief.author_login == ""
        assert brief.body == ""
        assert (brief.changed_files, brief.additions, brief.deletions) == (0, 0, 0)
        assert brief.head_branch == ""
        assert brief.is_cross_repository is False

    def test_empty_response_returns_empty(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        with patch.object(GitHubActionsProvider, "graphql", return_value=_response(nodes=[])):
            assert provider.list_no_change_candidate_prs() == []

    def test_raises_on_graphql_errors(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        with patch.object(
            GitHubActionsProvider,
            "graphql",
            return_value={"errors": [{"message": "boom"}]},
        ):
            with pytest.raises(RuntimeError, match="No-change candidate PR GraphQL query failed: boom"):
                provider.list_no_change_candidate_prs()

    def test_uses_fallback_message_when_graphql_errors_have_no_dict_entries(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        with patch.object(
            GitHubActionsProvider,
            "graphql",
            return_value={"errors": [None]},
        ):
            with pytest.raises(
                RuntimeError,
                match="No-change candidate PR GraphQL query failed: Unknown GraphQL error",
            ):
                provider.list_no_change_candidate_prs()

    def test_transient_failure_propagates_from_graphql(self) -> None:
        """A RetryableError from graphql() propagates; retries are scoped inside graphql()."""
        provider = GitHubActionsProvider(repo="o/r")
        with (
            patch("agentic_devtools.cli.ci.retry.time.sleep"),
            patch.object(GitHubActionsProvider, "graphql", side_effect=RetryableError("HTTP 503 service unavailable")),
        ):
            with pytest.raises(RetryableError, match="HTTP 503"):
                provider.list_no_change_candidate_prs()

    def test_paginates_past_the_first_page(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        with patch.object(
            GitHubActionsProvider,
            "graphql",
            side_effect=[
                _response(nodes=[{"number": 5}], has_next_page=True, end_cursor="cursor-1"),
                _response(nodes=[{"number": 6}]),
            ],
        ):
            briefs = provider.list_no_change_candidate_prs()

        assert [brief.number for brief in briefs] == [5, 6]

    def test_non_list_nodes_degrade_to_empty(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        with patch.object(
            GitHubActionsProvider,
            "graphql",
            return_value=_response(nodes=[]),
        ) as mock_graphql:
            mock_graphql.return_value["data"]["repository"]["pullRequests"]["nodes"] = {}
            assert provider.list_no_change_candidate_prs() == []

    def test_missing_end_cursor_stops_pagination(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        with patch.object(
            GitHubActionsProvider,
            "graphql",
            return_value=_response(nodes=[{"number": 5}], has_next_page=True, end_cursor=None),
        ):
            briefs = provider.list_no_change_candidate_prs()

        assert [brief.number for brief in briefs] == [5]

    def test_paginates_all_pages_until_has_next_page_is_false(self) -> None:
        """Pagination continues beyond _MAX_PR_PAGES until hasNextPage is false."""
        from agentic_devtools.cli.ci.github_provider import _MAX_PR_PAGES

        p = GitHubActionsProvider(repo="o/r")
        pages = [
            _response(nodes=[{"number": i}], has_next_page=True, end_cursor=f"cursor-{i}")
            for i in range(1, _MAX_PR_PAGES + 2)
        ]
        pages.append(_response(nodes=[{"number": _MAX_PR_PAGES + 2}]))
        with patch.object(
            GitHubActionsProvider,
            "graphql",
            side_effect=pages,
        ) as mock_graphql:
            briefs = p.list_no_change_candidate_prs()

        assert len(briefs) == _MAX_PR_PAGES + 2
        assert mock_graphql.call_count == _MAX_PR_PAGES + 2
