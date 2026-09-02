"""Tests for add_thumbs_up."""

from __future__ import annotations

import json
from unittest.mock import patch

import pytest

_MOD = "agentic_devtools.cli.github.issue_dedup_io"


class TestAddThumbsUp:
    """Tests for the add_thumbs_up function."""

    @patch(f"{_MOD}.resolve_github_repo", return_value="owner/repo")
    @patch(f"{_MOD}._gh_api")
    def test_posts_reaction_when_not_already_reacted(self, mock_api, mock_repo) -> None:
        """Posts +1 reaction when user hasn't already reacted."""
        from agentic_devtools.cli.github.issue_dedup_io import add_thumbs_up

        mock_api.side_effect = [
            json.dumps({"login": "testuser"}),  # /user
            json.dumps([]),  # reactions (empty)
            "",  # POST reaction
        ]
        add_thumbs_up(42, repo="owner/repo")
        # Third call is the POST
        assert mock_api.call_count == 3
        post_call = mock_api.call_args_list[2]
        assert post_call.args[0] == "/repos/owner/repo/issues/42/reactions"
        assert post_call.kwargs["method"] == "POST"
        assert post_call.kwargs["body"] == {"content": "+1"}

    @patch(f"{_MOD}.resolve_github_repo", return_value="owner/repo")
    @patch(f"{_MOD}._gh_api")
    def test_skips_post_when_already_reacted(self, mock_api, mock_repo) -> None:
        """Skips POST when user already has +1 reaction."""
        from agentic_devtools.cli.github.issue_dedup_io import add_thumbs_up

        mock_api.side_effect = [
            json.dumps({"login": "testuser"}),  # /user
            json.dumps([{"content": "+1", "user": {"login": "testuser"}}]),  # reactions
        ]
        add_thumbs_up(42, repo="owner/repo")
        # Only 2 calls: /user and reactions GET, no POST
        assert mock_api.call_count == 2

    @patch(f"{_MOD}.resolve_github_repo", return_value="owner/repo")
    @patch(f"{_MOD}._gh_api")
    def test_paginates_reactions(self, mock_api, mock_repo) -> None:
        """Paginates through reactions to find existing reaction."""
        from agentic_devtools.cli.github.issue_dedup_io import add_thumbs_up

        # Page 1: 100 reactions (none from our user with +1)
        page1 = [{"content": "heart", "user": {"login": f"user{i}"}} for i in range(100)]
        # Page 2: our user's +1
        page2 = [{"content": "+1", "user": {"login": "testuser"}}]

        mock_api.side_effect = [
            json.dumps({"login": "testuser"}),  # /user
            json.dumps(page1),  # reactions page 1
            json.dumps(page2),  # reactions page 2
        ]
        add_thumbs_up(42, repo="owner/repo")
        # No POST since found on page 2
        assert mock_api.call_count == 3

    @patch(f"{_MOD}.resolve_github_repo", return_value="owner/repo")
    @patch(f"{_MOD}._gh_api")
    def test_inaccessible_issue_raises(self, mock_api, mock_repo) -> None:
        """Raises RuntimeError when issue is inaccessible."""
        from agentic_devtools.cli.github.issue_dedup_io import add_thumbs_up

        mock_api.side_effect = [
            json.dumps({"login": "testuser"}),  # /user
            RuntimeError("Not Found"),  # reactions endpoint fails
        ]
        with pytest.raises(RuntimeError, match="inaccessible"):
            add_thumbs_up(999, repo="owner/repo")

    @patch(f"{_MOD}.resolve_github_repo", return_value="owner/repo")
    @patch(f"{_MOD}._gh_api")
    def test_failed_user_resolution_raises(self, mock_api, mock_repo) -> None:
        """Raises RuntimeError when /user returns invalid data."""
        from agentic_devtools.cli.github.issue_dedup_io import add_thumbs_up

        mock_api.return_value = "not json"
        with pytest.raises(RuntimeError, match="authenticated user"):
            add_thumbs_up(42, repo="owner/repo")

    @patch(f"{_MOD}.resolve_github_repo", return_value="owner/repo")
    @patch(f"{_MOD}._gh_api")
    def test_empty_login_raises(self, mock_api, mock_repo) -> None:
        """Raises RuntimeError when login is empty."""
        from agentic_devtools.cli.github.issue_dedup_io import add_thumbs_up

        mock_api.return_value = json.dumps({"login": ""})
        with pytest.raises(RuntimeError, match="authenticated user login"):
            add_thumbs_up(42, repo="owner/repo")

    @patch(f"{_MOD}.resolve_github_repo", return_value="owner/repo")
    @patch(f"{_MOD}._gh_api")
    def test_other_user_reaction_not_counted(self, mock_api, mock_repo) -> None:
        """Other users' +1 reactions don't prevent posting."""
        from agentic_devtools.cli.github.issue_dedup_io import add_thumbs_up

        mock_api.side_effect = [
            json.dumps({"login": "testuser"}),  # /user
            json.dumps([{"content": "+1", "user": {"login": "otheruser"}}]),  # reactions
            "",  # POST reaction
        ]
        add_thumbs_up(42, repo="owner/repo")
        assert mock_api.call_count == 3

    @patch(f"{_MOD}.resolve_github_repo", return_value="owner/repo")
    @patch(f"{_MOD}._gh_api")
    def test_malformed_reactions_json_posts_reaction(self, mock_api, mock_repo) -> None:
        """Malformed reactions JSON breaks pagination, proceeds to POST."""
        from agentic_devtools.cli.github.issue_dedup_io import add_thumbs_up

        mock_api.side_effect = [
            json.dumps({"login": "testuser"}),  # /user
            "not valid json",  # reactions (malformed)
            "",  # POST reaction
        ]
        add_thumbs_up(42, repo="owner/repo")
        assert mock_api.call_count == 3

    @patch(f"{_MOD}.resolve_github_repo", return_value="owner/repo")
    @patch(f"{_MOD}._gh_api")
    def test_non_list_reactions_posts_reaction(self, mock_api, mock_repo) -> None:
        """Non-list reactions response breaks pagination, proceeds to POST."""
        from agentic_devtools.cli.github.issue_dedup_io import add_thumbs_up

        mock_api.side_effect = [
            json.dumps({"login": "testuser"}),  # /user
            json.dumps({"error": "unexpected"}),  # reactions (not a list)
            "",  # POST reaction
        ]
        add_thumbs_up(42, repo="owner/repo")
        assert mock_api.call_count == 3
