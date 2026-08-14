# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for GitHub API helpers."""

from __future__ import annotations

from typing import cast
from unittest.mock import MagicMock, patch

import pytest
import requests

from airbyte_ops_mcp.github_api import (
    COPILOT_REVIEWER_LOGIN,
    AgentEnum,
    request_pr_ai_review,
    resolve_default_github_token,
)
from airbyte_ops_mcp.mcp.github_ops import (
    request_pr_ai_review as request_pr_ai_review_tool,
)


@pytest.mark.unit
def test_resolve_default_github_token_returns_none_when_allowed() -> None:
    with patch(
        "airbyte_ops_mcp.github_api._get_gh_cli_token", return_value=None
    ), patch("airbyte_ops_mcp.github_api.os.getenv", return_value=None):
        token = resolve_default_github_token(allow_none=True)

    assert token is None


@pytest.mark.unit
def test_resolve_default_github_token_raises_by_default() -> None:
    with patch(
        "airbyte_ops_mcp.github_api._get_gh_cli_token", return_value=None
    ), patch("airbyte_ops_mcp.github_api.os.getenv", return_value=None), pytest.raises(
        ValueError, match="No GitHub token found"
    ):
        resolve_default_github_token()


def _response(payload: object) -> MagicMock:
    response = MagicMock()
    response.json.return_value = payload
    response.raise_for_status.return_value = None
    return response


@pytest.mark.unit
@pytest.mark.parametrize(
    ("repo", "expected_repo", "expected_error"),
    [
        pytest.param("ai-skills", "ai-skills", None, id="bare"),
        pytest.param("airbytehq/ai-skills", "ai-skills", None, id="prefixed"),
        pytest.param(
            "other-org/ai-skills",
            None,
            "owner must be 'airbytehq'",
            id="wrong-owner",
        ),
        pytest.param(
            "airbytehq/ai-skills/foo",
            None,
            "Invalid repository 'airbytehq/ai-skills/foo'",
            id="extra-path-segment",
        ),
        pytest.param(
            "airbytehq/",
            None,
            "Invalid repository 'airbytehq/'",
            id="empty-prefixed-repository",
        ),
        pytest.param(
            "",
            None,
            "Invalid repository ''",
            id="empty-repository",
        ),
    ],
)
@patch("airbyte_ops_mcp.mcp.github_ops.request_pr_ai_review_api")
@patch("airbyte_ops_mcp.mcp.github_ops.resolve_copilot_review_github_token")
def test_request_pr_ai_review_normalizes_repo(
    mock_token: MagicMock,
    mock_request: MagicMock,
    repo: str,
    expected_repo: str | None,
    expected_error: str | None,
) -> None:
    if expected_error:
        with pytest.raises(ValueError, match=expected_error):
            request_pr_ai_review_tool(repo=repo, pr_number=84321)
        return

    mock_token.return_value = "user-pat"
    mock_request.return_value = MagicMock(
        requested=True,
        reviewers=[COPILOT_REVIEWER_LOGIN],
        message="requested",
    )

    result = request_pr_ai_review_tool(repo=repo, pr_number=84321)

    assert result.requested is True
    mock_request.assert_called_once_with(
        "airbytehq", expected_repo, 84321, "user-pat", AgentEnum.DEFAULT
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    ("request_to", "expected_error"),
    [
        pytest.param(None, None, id="default"),
        pytest.param(AgentEnum.Copilot, None, id="explicit-copilot"),
        pytest.param(
            [AgentEnum.Copilot, AgentEnum.Copilot],
            None,
            id="deduplicated-list",
        ),
        pytest.param(
            cast(AgentEnum, "future-reviewer"),
            "Unsupported AI reviewer",
            id="unsupported",
        ),
    ],
)
@patch("airbyte_ops_mcp.mcp.github_ops.request_pr_ai_review_api")
@patch("airbyte_ops_mcp.mcp.github_ops.resolve_copilot_review_github_token")
def test_request_pr_ai_review_targets(
    mock_token: MagicMock,
    mock_request: MagicMock,
    request_to: AgentEnum | list[AgentEnum] | None,
    expected_error: str | None,
) -> None:
    if expected_error:
        with pytest.raises(ValueError, match=expected_error):
            request_pr_ai_review(
                "airbytehq",
                "airbyte",
                84321,
                "user-pat",
                cast(AgentEnum, request_to),
            )
        return

    mock_token.return_value = "user-pat"
    mock_request.return_value = MagicMock(
        requested=True,
        reviewers=[COPILOT_REVIEWER_LOGIN],
        message="requested",
    )
    kwargs = {} if request_to is None else {"request_to": request_to}

    result = request_pr_ai_review_tool(
        repo="airbyte",
        pr_number=84321,
        **kwargs,
    )

    assert result.requested is True
    mock_request.assert_called_once_with(
        "airbytehq",
        "airbyte",
        84321,
        "user-pat",
        AgentEnum.DEFAULT if request_to is None else request_to,
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    ("failure", "expected_message", "forbidden_message"),
    [
        pytest.param(
            "missing_pat",
            "GITHUB_CI_WORKFLOW_TRIGGER_PAT",
            None,
            id="missing-pat",
        ),
        pytest.param(
            "unresolvable_bot",
            "Copilot seat",
            None,
            id="unresolvable-bot",
        ),
        pytest.param(
            "mutation_rejected",
            "Copilot seat",
            None,
            id="mutation-rejected",
        ),
        pytest.param(
            "unverified",
            "reviewRequests does not show it",
            None,
            id="unverified",
        ),
        pytest.param(
            "pull_request_transport",
            "could not resolve the pull request",
            None,
            id="pull-request-transport",
        ),
        pytest.param(
            "mutation_transport",
            "GitHub rejected",
            None,
            id="mutation-transport",
        ),
        pytest.param(
            "verification_transport",
            "could not be confirmed",
            "Copilot seat",
            id="verification-transport",
        ),
        pytest.param(
            "verification_malformed",
            "could not be confirmed",
            "Copilot seat",
            id="verification-malformed",
        ),
    ],
)
def test_request_pr_ai_review_failure_modes(
    failure: str,
    expected_message: str,
    forbidden_message: str | None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    if failure == "missing_pat":
        monkeypatch.delenv("GITHUB_CI_WORKFLOW_TRIGGER_PAT", raising=False)
        with pytest.raises(ValueError, match=expected_message):
            request_pr_ai_review_tool(repo="airbyte", pr_number=84321)
        return

    with patch("airbyte_ops_mcp.github_api.requests.get") as mock_get, patch(
        "airbyte_ops_mcp.github_api.requests.post"
    ) as mock_post:
        mock_get.return_value = _response(
            {
                "login": "Copilot",
                "id": 175728472,
                "node_id": "BOT_kgDOCnlnWA",
                "type": "Bot",
            }
        )
        if failure == "unresolvable_bot":
            mock_get.return_value.raise_for_status.side_effect = requests.HTTPError(
                "Not Found"
            )
        elif failure == "pull_request_transport":
            response = _response({})
            response.raise_for_status.side_effect = requests.RequestException(
                "network down"
            )
            mock_post.side_effect = [response]
        elif failure == "mutation_rejected":
            mock_post.side_effect = [
                _response(
                    {"data": {"repository": {"pullRequest": {"id": "PR_NODE_ID"}}}}
                ),
                _response({"errors": [{"message": "Could not resolve to Bot node"}]}),
            ]
        elif failure == "mutation_transport":
            response = _response({})
            response.raise_for_status.side_effect = requests.RequestException(
                "network down"
            )
            mock_post.side_effect = [
                _response(
                    {"data": {"repository": {"pullRequest": {"id": "PR_NODE_ID"}}}}
                ),
                response,
            ]
        elif failure == "verification_transport":
            response = _response({})
            response.raise_for_status.side_effect = requests.RequestException(
                "network down"
            )
            mock_post.side_effect = [
                _response(
                    {"data": {"repository": {"pullRequest": {"id": "PR_NODE_ID"}}}}
                ),
                _response({"data": {"requestReviews": {}}}),
                response,
            ]
        elif failure == "verification_malformed":
            mock_post.side_effect = [
                _response(
                    {"data": {"repository": {"pullRequest": {"id": "PR_NODE_ID"}}}}
                ),
                _response({"data": {"requestReviews": {}}}),
                _response(
                    {
                        "data": {
                            "repository": {
                                "pullRequest": {
                                    "reviewRequests": {"nodes": "unexpected"},
                                }
                            }
                        }
                    }
                ),
            ]
        else:
            mock_post.side_effect = [
                _response(
                    {"data": {"repository": {"pullRequest": {"id": "PR_NODE_ID"}}}}
                ),
                _response({"data": {"requestReviews": {}}}),
                _response(
                    {
                        "data": {
                            "repository": {
                                "pullRequest": {
                                    "reviewRequests": {"nodes": []},
                                }
                            }
                        }
                    }
                ),
            ]

        result = request_pr_ai_review("airbytehq", "airbyte", 84321, "user-pat")

    assert result.requested is False
    assert expected_message in result.message
    if forbidden_message:
        assert forbidden_message not in result.message


def _configure_verified_request(
    mock_get: MagicMock,
    mock_post: MagicMock,
) -> None:
    mock_get.return_value = _response(
        {
            "login": "Copilot",
            "id": 175728472,
            "node_id": "BOT_kgDOCnlnWA",
            "type": "Bot",
        }
    )
    mock_post.side_effect = [
        _response({"data": {"repository": {"pullRequest": {"id": "PR_NODE_ID"}}}}),
        _response({"data": {"requestReviews": {}}}),
        _response(
            {
                "data": {
                    "repository": {
                        "pullRequest": {
                            "reviewRequests": {
                                "nodes": [
                                    {
                                        "requestedReviewer": {
                                            "__typename": "Bot",
                                            "login": COPILOT_REVIEWER_LOGIN,
                                        }
                                    }
                                ]
                            }
                        }
                    }
                }
            }
        ),
    ]


@pytest.mark.unit
@patch("airbyte_ops_mcp.github_api.requests.get")
@patch("airbyte_ops_mcp.github_api.requests.post")
def test_request_pr_ai_review_succeeds(
    mock_post: MagicMock,
    mock_get: MagicMock,
) -> None:
    _configure_verified_request(mock_get, mock_post)

    result = request_pr_ai_review("airbytehq", "airbyte", 84321, "user-pat")

    assert result.requested is True
    assert result.reviewers == [COPILOT_REVIEWER_LOGIN]


@pytest.mark.unit
@patch("airbyte_ops_mcp.github_api.requests.get")
@patch("airbyte_ops_mcp.github_api.requests.post")
def test_request_pr_ai_review_mutation_has_valid_payload_selection(
    mock_post: MagicMock,
    mock_get: MagicMock,
) -> None:
    _configure_verified_request(mock_get, mock_post)

    request_pr_ai_review("airbytehq", "airbyte", 84321, "user-pat")

    assert mock_post.call_args_list[1].kwargs["json"]["variables"]["input"] == {
        "pullRequestId": "PR_NODE_ID",
        "botIds": ["BOT_kgDOCnlnWA"],
        "union": True,
    }
    mutation_query = mock_post.call_args_list[1].kwargs["json"]["query"]
    # `RequestReviewsPayload` has no `reviewRequests` field; selecting it makes
    # GitHub reject the whole document at validation time, so nothing mutates.
    assert "pullRequest" in mutation_query
    assert "reviewRequests" not in mutation_query
