# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for GitHub comment fetching with multi-token retry on 404.

Covers the retry logic in get_github_comment_info that tries all
available tokens when the first returns 404 (e.g., private repos).
"""

from unittest.mock import MagicMock, patch

import pytest

from airbyte_ops_mcp.github_api import (
    GitHubAPIError,
    GitHubCommentInfo,
    get_github_comment_info,
)


@pytest.mark.unit
@patch("airbyte_ops_mcp.github_api.requests.get")
@patch("airbyte_ops_mcp.github_api._resolve_all_default_github_tokens")
def test_get_comment_info_retries_on_404_then_succeeds(
    mock_resolve_tokens: MagicMock,
    mock_get: MagicMock,
) -> None:
    """First token gets 404 (no private-repo access), second token succeeds."""
    mock_resolve_tokens.return_value = ["token-no-access", "token-with-access"]

    resp_404 = MagicMock()
    resp_404.ok = False
    resp_404.status_code = 404
    resp_404.text = '{"message":"Not Found"}'

    resp_ok = MagicMock()
    resp_ok.ok = True
    resp_ok.json.return_value = {
        "user": {"login": "someuser"},
        "author_association": "MEMBER",
    }

    mock_get.side_effect = [resp_404, resp_ok]

    result = get_github_comment_info(
        owner="airbytehq",
        repo="airbyte-internal-issues",
        comment_id=123,
        comment_type="issue_comment",
    )
    assert isinstance(result, GitHubCommentInfo)
    assert result.author_login == "someuser"
    assert result.author_association == "MEMBER"
    assert mock_get.call_count == 2


@pytest.mark.unit
@patch("airbyte_ops_mcp.github_api.requests.get")
@patch("airbyte_ops_mcp.github_api._resolve_all_default_github_tokens")
def test_get_comment_info_all_tokens_404(
    mock_resolve_tokens: MagicMock,
    mock_get: MagicMock,
) -> None:
    """All tokens return 404 -- raises GitHubAPIError with token count."""
    mock_resolve_tokens.return_value = ["tok1", "tok2"]

    resp_404 = MagicMock()
    resp_404.ok = False
    resp_404.status_code = 404
    resp_404.text = '{"message":"Not Found"}'

    mock_get.return_value = resp_404

    with pytest.raises(GitHubAPIError, match="Tried 2 token"):
        get_github_comment_info(
            owner="airbytehq",
            repo="airbyte-internal-issues",
            comment_id=999,
            comment_type="issue_comment",
        )
    assert mock_get.call_count == 2


@pytest.mark.unit
@patch("airbyte_ops_mcp.github_api.requests.get")
@patch("airbyte_ops_mcp.github_api._resolve_all_default_github_tokens")
def test_get_comment_info_non_404_error_fails_immediately(
    mock_resolve_tokens: MagicMock,
    mock_get: MagicMock,
) -> None:
    """Non-404 errors (e.g., 403) should fail immediately without retrying."""
    mock_resolve_tokens.return_value = ["tok1", "tok2"]

    resp_403 = MagicMock()
    resp_403.ok = False
    resp_403.status_code = 403
    resp_403.text = '{"message":"Forbidden"}'

    mock_get.return_value = resp_403

    with pytest.raises(GitHubAPIError, match="403"):
        get_github_comment_info(
            owner="airbytehq",
            repo="airbyte-internal-issues",
            comment_id=123,
            comment_type="issue_comment",
        )
    # Should fail on first attempt, not retry
    assert mock_get.call_count == 1


@pytest.mark.unit
@patch("airbyte_ops_mcp.github_api.requests.get")
def test_get_comment_info_explicit_token_no_retry(
    mock_get: MagicMock,
) -> None:
    """When an explicit token is passed, only that token is tried."""
    resp_404 = MagicMock()
    resp_404.ok = False
    resp_404.status_code = 404
    resp_404.text = '{"message":"Not Found"}'

    mock_get.return_value = resp_404

    with pytest.raises(GitHubAPIError, match="Tried 1 token"):
        get_github_comment_info(
            owner="airbytehq",
            repo="airbyte-internal-issues",
            comment_id=123,
            comment_type="issue_comment",
            token="explicit-token",
        )
    assert mock_get.call_count == 1


@pytest.mark.unit
@patch("airbyte_ops_mcp.github_api._resolve_all_default_github_tokens")
def test_get_comment_info_no_tokens_raises(
    mock_resolve_tokens: MagicMock,
) -> None:
    """When no tokens are available, raises GitHubAPIError immediately."""
    mock_resolve_tokens.return_value = []

    with pytest.raises(GitHubAPIError, match="No GitHub token found"):
        get_github_comment_info(
            owner="airbytehq",
            repo="airbyte-internal-issues",
            comment_id=123,
            comment_type="issue_comment",
        )
