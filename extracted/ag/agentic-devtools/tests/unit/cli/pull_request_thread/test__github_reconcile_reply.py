"""Tests for _github_reconcile_reply."""

from unittest.mock import MagicMock

import pytest

from agentic_devtools.adapters.base import PullRequestThreadReplyRequest
from agentic_devtools.cli.pull_request_thread import _github_reconcile_reply


def test_returns_matching_reply_id() -> None:
    requests = MagicMock()
    response = MagicMock(status_code=200)
    response.json.return_value = [{"body": "reply", "id": 56, "in_reply_to_id": 34}]
    requests.get.return_value = response

    result = _github_reconcile_reply(
        requests,
        {},
        PullRequestThreadReplyRequest("github", "owner/repo", 12, 34, "reply"),
    )

    assert result == 56
    call_url = requests.get.call_args.args[0]
    assert "/pulls/12/comments" in call_url
    assert "in_reply_to_id" not in call_url  # filter applied client-side


def test_returns_none_for_unmatched_or_malformed_results() -> None:
    requests = MagicMock()
    response = MagicMock(status_code=200)
    # Neither comment matches: wrong body, missing in_reply_to_id, and invalid entry
    response.json.return_value = [
        {"body": "other", "id": 56, "in_reply_to_id": 34},
        {"body": "reply", "id": 57},  # missing in_reply_to_id
        "invalid",
    ]
    requests.get.return_value = response

    result = _github_reconcile_reply(
        requests,
        {},
        PullRequestThreadReplyRequest("github", "owner/repo", 12, 34, "reply"),
    )

    assert result is None


def test_raises_for_http_failure() -> None:
    requests = MagicMock()
    requests.get.return_value = MagicMock(status_code=503)

    with pytest.raises(ValueError, match="baseline lookup returned HTTP 503"):
        _github_reconcile_reply(
            requests,
            {},
            PullRequestThreadReplyRequest("github", "owner/repo", 12, 34, "reply"),
        )


def test_raises_for_non_list_payload() -> None:
    requests = MagicMock()
    response = MagicMock(status_code=200)
    response.json.return_value = {}
    requests.get.return_value = response

    with pytest.raises(ValueError, match="baseline lookup returned a malformed payload"):
        _github_reconcile_reply(
            requests,
            {},
            PullRequestThreadReplyRequest("github", "owner/repo", 12, 34, "reply"),
        )


def test_paginates_until_match_found() -> None:
    requests = MagicMock()
    full_page = [{"body": "other", "id": i, "in_reply_to_id": 34} for i in range(100)]
    match_page = [{"body": "reply", "id": 99, "in_reply_to_id": 34}]
    page1 = MagicMock(status_code=200)
    page1.json.return_value = full_page
    page2 = MagicMock(status_code=200)
    page2.json.return_value = match_page
    requests.get.side_effect = [page1, page2]

    result = _github_reconcile_reply(
        requests,
        {},
        PullRequestThreadReplyRequest("github", "owner/repo", 12, 34, "reply"),
    )

    assert result == 99
    assert requests.get.call_count == 2


def test_stops_pagination_on_partial_page() -> None:
    requests = MagicMock()
    response = MagicMock(status_code=200)
    response.json.return_value = [{"body": "other", "id": 1, "in_reply_to_id": 34}]
    requests.get.return_value = response

    result = _github_reconcile_reply(
        requests,
        {},
        PullRequestThreadReplyRequest("github", "owner/repo", 12, 34, "reply"),
    )

    assert result is None
    assert requests.get.call_count == 1


def test_matches_string_discussion_id_against_integer_in_reply_to_id() -> None:
    """GitHub returns in_reply_to_id as int; CLI supplies discussion_id as str."""
    requests = MagicMock()
    response = MagicMock(status_code=200)
    response.json.return_value = [{"body": "reply", "id": 77, "in_reply_to_id": 34}]
    requests.get.return_value = response

    result = _github_reconcile_reply(
        requests,
        {},
        PullRequestThreadReplyRequest("github", "owner/repo", 12, "34", "reply"),
    )

    assert result == 77


def test_returns_none_when_reply_id_is_zero() -> None:
    """A zero id value is not a valid GitHub comment ID and must be ignored."""
    requests = MagicMock()
    response = MagicMock(status_code=200)
    response.json.return_value = [{"body": "reply", "id": 0, "in_reply_to_id": 34}]
    requests.get.return_value = response

    result = _github_reconcile_reply(
        requests,
        {},
        PullRequestThreadReplyRequest("github", "owner/repo", 12, 34, "reply"),
    )

    assert result is None


def test_returns_none_when_reply_id_is_negative() -> None:
    """A negative id value is not a valid GitHub comment ID and must be ignored."""
    requests = MagicMock()
    response = MagicMock(status_code=200)
    response.json.return_value = [{"body": "reply", "id": -5, "in_reply_to_id": 34}]
    requests.get.return_value = response

    result = _github_reconcile_reply(
        requests,
        {},
        PullRequestThreadReplyRequest("github", "owner/repo", 12, 34, "reply"),
    )

    assert result is None


def test_returns_none_when_reply_id_is_non_integer() -> None:
    """A non-integer id value (e.g. string) is not a valid GitHub comment ID and must be ignored."""
    requests = MagicMock()
    response = MagicMock(status_code=200)
    response.json.return_value = [{"body": "reply", "id": "abc", "in_reply_to_id": 34}]
    requests.get.return_value = response

    result = _github_reconcile_reply(
        requests,
        {},
        PullRequestThreadReplyRequest("github", "owner/repo", 12, 34, "reply"),
    )

    assert result is None


def test_returns_none_when_reply_id_is_bool() -> None:
    """A boolean id (True/False) must be excluded even though bool is a subclass of int in Python."""
    requests = MagicMock()
    response = MagicMock(status_code=200)
    response.json.return_value = [{"body": "reply", "id": True, "in_reply_to_id": 34}]
    requests.get.return_value = response

    result = _github_reconcile_reply(
        requests,
        {},
        PullRequestThreadReplyRequest("github", "owner/repo", 12, 34, "reply"),
    )

    assert result is None


def test_returns_only_matches_created_after_baseline_reply_id() -> None:
    requests = MagicMock()
    response = MagicMock(status_code=200)
    response.json.return_value = [
        {"body": "reply", "id": 56, "in_reply_to_id": 34},
        {"body": "reply", "id": 57, "in_reply_to_id": 34},
    ]
    requests.get.return_value = response

    result = _github_reconcile_reply(
        requests,
        {},
        PullRequestThreadReplyRequest("github", "owner/repo", 12, 34, "reply"),
        minimum_reply_id_exclusive=56,
    )

    assert result == 57
