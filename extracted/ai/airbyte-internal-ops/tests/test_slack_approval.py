# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for Slack-based approval resolution.

Tests cover:
- URL parsing
- Approval record extraction
- Bot authorship validation
- The shared approval_resolution dispatcher
"""

from unittest.mock import MagicMock, patch

import pytest

from airbyte_ops_mcp.approval_resolution import (
    ApprovalResolutionError,
    resolve_admin_email_from_approval,
)
from airbyte_ops_mcp.slack_api import (
    ApprovalRecord,
    SlackApprovalRecordError,
    SlackMessageInfo,
    SlackURLParseError,
    _extract_approval_record,
    _parse_slack_message_url,
    _validate_bot_authorship,
    validate_slack_approval_record,
)

# ---------------------------------------------------------------------------
# URL parsing tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "url,expected_channel,expected_ts,expected_thread_ts",
    [
        pytest.param(
            "https://airbytehq-team.slack.com/archives/C08BHPUMEPJ/p1773062711122019",
            "C08BHPUMEPJ",
            "1773062711.122019",
            None,
            id="basic_url",
        ),
        pytest.param(
            "https://airbytehq-team.slack.com/archives/C08BHPUMEPJ/p1773062711122019"
            "?thread_ts=1773062700.000001&cid=C08BHPUMEPJ",
            "C08BHPUMEPJ",
            "1773062711.122019",
            "1773062700.000001",
            id="url_with_thread_ts",
        ),
        pytest.param(
            "https://airbytehq-team.slack.com/archives/C08BHPUMEPJ/p1773062711",
            "C08BHPUMEPJ",
            "1773062711",
            None,
            id="short_timestamp",
        ),
    ],
)
def test_parse_slack_message_url_valid(
    url: str,
    expected_channel: str,
    expected_ts: str,
    expected_thread_ts: str | None,
) -> None:
    result = _parse_slack_message_url(url)
    assert isinstance(result, SlackMessageInfo)
    assert result.workspace == "airbytehq-team"
    assert result.channel_id == expected_channel
    assert result.message_ts == expected_ts
    assert result.thread_ts == expected_thread_ts


@pytest.mark.unit
@pytest.mark.parametrize(
    "url,expected_error",
    [
        pytest.param(
            "https://example.com/not-a-slack-url",
            "Invalid Slack message URL",
            id="invalid_format",
        ),
        pytest.param(
            "https://other-workspace.slack.com/archives/C08BHPUMEPJ/p1773062711122019",
            "Unexpected Slack workspace",
            id="wrong_workspace",
        ),
    ],
)
def test_parse_slack_message_url_invalid(url: str, expected_error: str) -> None:
    with pytest.raises(SlackURLParseError, match=expected_error):
        _parse_slack_message_url(url)


# ---------------------------------------------------------------------------
# Approval record extraction tests
# ---------------------------------------------------------------------------

_VALID_APPROVAL_MSG = {
    "blocks": [
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": (
                        "Metadata: ```"
                        '{"type": "approval_record", "action": "approved", '
                        '"user_id": "U05AKF1BCC9", "user_name": "AJ Steers", '
                        '"timestamp": "2026-03-09T12:00:00Z"}'
                        "```"
                    ),
                }
            ],
        }
    ]
}


@pytest.mark.unit
def test_extract_approval_record_valid() -> None:
    record = _extract_approval_record(_VALID_APPROVAL_MSG)
    assert isinstance(record, ApprovalRecord)
    assert record.action == "approved"
    assert record.user_id == "U05AKF1BCC9"
    assert record.user_name == "AJ Steers"
    assert record.timestamp == "2026-03-09T12:00:00Z"


@pytest.mark.unit
@pytest.mark.parametrize(
    "message,expected_error",
    [
        pytest.param(
            {
                "blocks": [
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "mrkdwn",
                                "text": (
                                    "```"
                                    '{"type": "approval_record", "action": "approved", '
                                    '"user_id": "", "user_name": "Someone", '
                                    '"timestamp": "2026-03-09T12:00:00Z"}'
                                    "```"
                                ),
                            }
                        ],
                    }
                ]
            },
            "missing 'user_id'",
            id="missing_user_id",
        ),
        pytest.param(
            {
                "blocks": [
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "mrkdwn",
                                "text": (
                                    "```"
                                    '{"type": "approval_record", "action": "maybe", '
                                    '"user_id": "U12345", "user_name": "Someone", '
                                    '"timestamp": "2026-03-09T12:00:00Z"}'
                                    "```"
                                ),
                            }
                        ],
                    }
                ]
            },
            "Invalid approval action",
            id="invalid_action",
        ),
        pytest.param(
            {
                "blocks": [
                    {"type": "section", "text": {"type": "mrkdwn", "text": "Hello"}}
                ]
            },
            "does not contain a valid approval record",
            id="no_context_block",
        ),
        pytest.param(
            {"blocks": []},
            "does not contain a valid approval record",
            id="empty_blocks",
        ),
    ],
)
def test_extract_approval_record_invalid(message: dict, expected_error: str) -> None:
    with pytest.raises(SlackApprovalRecordError, match=expected_error):
        _extract_approval_record(message)


# ---------------------------------------------------------------------------
# Bot authorship validation tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "message",
    [
        pytest.param({"bot_id": "B12345", "text": "hello"}, id="bot_id_present"),
        pytest.param({"subtype": "bot_message", "text": "hello"}, id="bot_subtype"),
    ],
)
def test_validate_bot_authorship_valid(message: dict) -> None:
    _validate_bot_authorship(message)  # Should not raise


@pytest.mark.unit
def test_validate_bot_authorship_not_bot() -> None:
    with pytest.raises(SlackApprovalRecordError, match="not posted by a bot"):
        _validate_bot_authorship({"user": "U12345", "text": "hello"})


@pytest.mark.unit
@patch("airbyte_ops_mcp.slack_api._fetch_slack_message")
def test_validate_slack_approval_record_rejects_rejected_record(
    mock_fetch_message: MagicMock,
) -> None:
    mock_fetch_message.return_value = {
        "bot_id": "B12345",
        "blocks": [
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": (
                            "```"
                            '{"type": "approval_record", "action": "rejected", '
                            '"user_id": "U12345", "user_name": "Someone", '
                            '"timestamp": "2026-03-09T12:00:00Z"}'
                            "```"
                        ),
                    }
                ],
            }
        ],
    }

    with pytest.raises(SlackApprovalRecordError, match="Request was not approved"):
        validate_slack_approval_record(
            "https://airbytehq-team.slack.com/archives/C08BHPUMEPJ/p1773062711122019"
        )


# ---------------------------------------------------------------------------
# Shared approval resolution tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "kwargs,expected_error",
    [
        pytest.param(
            {},
            "is required",
            id="neither_provided",
        ),
        pytest.param(
            {"approval_comment_url": "https://not-github.com/foo"},
            "Unrecognized approval URL domain",
            id="unrecognized_domain",
        ),
        pytest.param(
            {"approval_comment_url": "https://github.com/org/repo/issues/1"},
            "GitHub comment URL",
            id="github_url_missing_comment_fragment",
        ),
    ],
)
def test_resolve_admin_email_from_approval_validation(
    kwargs: dict, expected_error: str
) -> None:
    with pytest.raises(ApprovalResolutionError, match=expected_error):
        resolve_admin_email_from_approval(**kwargs)


@pytest.mark.unit
@patch("airbyte_ops_mcp.approval_resolution.get_admin_email_from_approval_comment")
def test_resolve_admin_email_from_approval_github(mock_github: MagicMock) -> None:
    mock_github.return_value = "admin@airbyte.io"
    result = resolve_admin_email_from_approval(
        approval_comment_url="https://github.com/org/repo/issues/1#issuecomment-123"
    )
    assert result == "admin@airbyte.io"
    mock_github.assert_called_once()


@pytest.mark.unit
@patch("airbyte_ops_mcp.approval_resolution.validate_slack_approval_record")
def test_resolve_admin_email_from_approval_slack(mock_validate: MagicMock) -> None:
    mock_validate.return_value = ApprovalRecord(
        action="approved",
        user_id="U05AKF1BCC9",
        user_name="AJ Steers",
        timestamp="2026-03-09T12:00:00Z",
        admin_email="admin@airbyte.io",
    )
    result = resolve_admin_email_from_approval(
        approval_comment_url="https://airbytehq-team.slack.com/archives/C08BHPUMEPJ/p1773062711122019"
    )
    assert result == "admin@airbyte.io"
    mock_validate.assert_called_once_with(
        "https://airbytehq-team.slack.com/archives/C08BHPUMEPJ/p1773062711122019",
        require_approved=True,
        resolve_admin_email=True,
    )
