# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for Slack thread posting utilities and feedback follow-up tool.

Tests cover:
- URL parsing (valid permalinks, wrong workspace, malformed URLs)
- Follow-up message wrapping (header + footer disclaimer)
- Feedback follow-up tool error handling
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from airbyte_ops_mcp.github_actions import WorkflowDispatchResult
from airbyte_ops_mcp.mcp.devin_ops import (
    _FOLLOWUP_HEADER,
    _build_feedback_body,
    _dispatch_triage_workflow,
    _wrap_followup_message,
    devin_session_feedback,
    devin_session_feedback_followup,
)
from airbyte_ops_mcp.slack_api import SlackURLParseError
from airbyte_ops_mcp.slack_posting import SlackPostResult, parse_slack_thread_url

# ---------------------------------------------------------------------------
# parse_slack_thread_url tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "url,expected_channel,expected_ts",
    [
        pytest.param(
            "https://airbytehq-team.slack.com/archives/C0ACUHRP6B1/p1773062711122019",
            "C0ACUHRP6B1",
            "1773062711.122019",
            id="basic_permalink",
        ),
        pytest.param(
            "https://airbytehq-team.slack.com/archives/C0AEN317Z7T/p1774646306048449",
            "C0AEN317Z7T",
            "1774646306.048449",
            id="test_channel_permalink",
        ),
        pytest.param(
            "https://airbytehq-team.slack.com/archives/C0ACUHRP6B1/p1773062711122019"
            "?thread_ts=1773062700.000001&cid=C0ACUHRP6B1",
            "C0ACUHRP6B1",
            "1773062711.122019",
            id="permalink_with_query_params",
        ),
        pytest.param(
            "https://airbytehq-team.slack.com/archives/C0ACUHRP6B1/p1773062711",
            "C0ACUHRP6B1",
            "1773062711",
            id="short_timestamp_10_digits",
        ),
    ],
)
def test_parse_slack_thread_url_valid(
    url: str, expected_channel: str, expected_ts: str
) -> None:
    channel_id, thread_ts = parse_slack_thread_url(url)
    assert channel_id == expected_channel
    assert thread_ts == expected_ts


@pytest.mark.unit
@pytest.mark.parametrize(
    "url,expected_error",
    [
        pytest.param(
            "https://example.com/not-a-slack-url",
            "Invalid Slack thread URL",
            id="not_slack_url",
        ),
        pytest.param(
            "https://other-workspace.slack.com/archives/C0ACUHRP6B1/p1773062711122019",
            "Unexpected Slack workspace",
            id="wrong_workspace",
        ),
        pytest.param(
            "not-even-a-url",
            "Invalid Slack thread URL",
            id="garbage_input",
        ),
        pytest.param(
            "https://airbytehq-team.slack.com/archives/C0ACUHRP6B1",
            "Invalid Slack thread URL",
            id="missing_timestamp",
        ),
    ],
)
def test_parse_slack_thread_url_invalid(url: str, expected_error: str) -> None:
    with pytest.raises(SlackURLParseError, match=expected_error):
        parse_slack_thread_url(url)


# ---------------------------------------------------------------------------
# _wrap_followup_message tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_build_feedback_body_renders_playbook_and_skill_links() -> None:
    """Feedback body renders playbook and skill identifiers as Slack links."""
    result = _build_feedback_body(
        feedback_type="negative",
        category="missing_guidance",
        task_description="Triage a Devin session",
        session_playbook="devin_feedback_triage",
        related_skill_name="delete-declarative-source-def",
        expected_behavior="The session follows the feedback playbook.",
        observed_behavior="The session omitted the playbook context.",
        what_went_well=None,
        severity="medium",
        steps_to_reproduce=None,
    )

    assert (
        "*Session Playbook:* "
        "<https://github.com/airbytehq/ai-skills/blob/main/devin/playbooks/"
        "devin_feedback_triage.md|devin_feedback_triage>"
    ) in result
    assert (
        "*Related Skill:* "
        "<https://internal.airbyte.ai/docs/internal-docs/ai-engineering/skills/"
        "#delete-declarative-source-def|delete-declarative-source-def>"
    ) in result


@pytest.mark.unit
def test_build_feedback_body_renders_no_playbook_without_link() -> None:
    """Feedback body preserves none playbook identifier as plain text."""
    result = _build_feedback_body(
        feedback_type="positive",
        category="great_results",
        task_description="Complete a repo task",
        session_playbook="none",
        related_skill_name=None,
        expected_behavior=None,
        observed_behavior=None,
        what_went_well="The task was completed quickly.",
        severity=None,
        steps_to_reproduce=None,
    )

    assert "*Session Playbook:* none" in result
    assert "*Related Skill:*" not in result


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.devin_ops.trigger_workflow_dispatch")
@patch("airbyte_ops_mcp.mcp.devin_ops.resolve_ci_trigger_github_token")
def test_dispatch_triage_workflow_includes_playbook_and_skill(
    mock_token: MagicMock, mock_dispatch: MagicMock
) -> None:
    """Triage workflow dispatch receives playbook and skill identifiers."""
    mock_token.return_value = "fake-token"
    mock_dispatch.return_value = WorkflowDispatchResult(
        workflow_url="https://github.com/airbytehq/airbyte-ops-mcp/actions/workflows/devin-session-triage.yml",
    )

    _dispatch_triage_workflow(
        session_url="https://app.devin.ai/sessions/test123",
        feedback_context="Feedback context",
        reporting_user="aj@airbyte.io",
        session_playbook="devin_feedback_triage",
        related_skill_name="delete-declarative-source-def",
    )

    call_kwargs = mock_dispatch.call_args.kwargs
    assert call_kwargs["inputs"]["session_playbook"] == "devin_feedback_triage"
    assert (
        call_kwargs["inputs"]["related_skill_name"] == "delete-declarative-source-def"
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "session_playbook,related_skill_name,expected_error",
    [
        pytest.param(
            "None",
            None,
            "session_playbook must be 'none' or a lowercase playbook ID",
            id="capitalized_none",
        ),
        pytest.param(
            "bad|id",
            None,
            "session_playbook must be 'none' or a lowercase playbook ID",
            id="invalid_playbook_mrkdwn",
        ),
        pytest.param(
            "devin_feedback_triage",
            "bad|skill",
            "related_skill_name must be a lowercase skill ID",
            id="invalid_skill_mrkdwn",
        ),
    ],
)
@patch("airbyte_ops_mcp.mcp.devin_ops.dispatch_escalation")
def test_devin_session_feedback_rejects_invalid_context_ids(
    mock_dispatch: MagicMock,
    session_playbook: str,
    related_skill_name: str | None,
    expected_error: str,
) -> None:
    """Feedback submission rejects invalid playbook and related skill IDs."""
    result = devin_session_feedback(
        feedback_type="positive",
        category="great_results",
        task_description="Complete a repo task",
        agent_session_url="https://app.devin.ai/sessions/test123",
        reporting_user="aj@airbyte.io",
        session_playbook=session_playbook,
        related_skill_name=related_skill_name,
        expected_behavior=None,
        observed_behavior=None,
        what_went_well="The task was completed quickly.",
        severity=None,
        steps_to_reproduce=None,
        session_to_evaluate=None,
    )

    assert result.success is False
    assert expected_error in result.message
    mock_dispatch.assert_not_called()


@pytest.mark.unit
def test_wrap_followup_message_structure() -> None:
    """Wrapped message has header, body, and non-interactive footer."""
    body = "Here are my triage findings."
    session_url = "https://app.devin.ai/sessions/test123"
    result = _wrap_followup_message(body, agent_session_url=session_url)

    assert result.startswith(_FOLLOWUP_HEADER)
    assert body in result
    # Verify structure: header \n\n body \n\n footer (with hyperlinked session)
    assert f"<{session_url}|linked session>" in result
    assert "not monitored by Devin" in result
    assert result.endswith("or create a new task._")


# ---------------------------------------------------------------------------
# devin_session_feedback_followup tool tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_followup_tool_invalid_url() -> None:
    """Follow-up tool returns success=False for invalid thread URLs."""
    result = devin_session_feedback_followup(
        thread_url="https://example.com/not-slack",
        message="Triage report",
        agent_session_url="https://app.devin.ai/sessions/test123",
    )
    assert result.success is False
    assert "Invalid Slack thread URL" in result.message


@pytest.mark.unit
def test_followup_tool_wrong_workspace() -> None:
    """Follow-up tool returns success=False for wrong workspace."""
    result = devin_session_feedback_followup(
        thread_url="https://evil-workspace.slack.com/archives/C0ACUHRP6B1/p1773062711122019",
        message="Triage report",
        agent_session_url="https://app.devin.ai/sessions/test123",
    )
    assert result.success is False
    assert "Unexpected Slack workspace" in result.message


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.devin_ops.post_thread_reply")
def test_followup_tool_success(mock_post: MagicMock) -> None:
    """Follow-up tool returns success=True when post succeeds."""
    mock_post.return_value = SlackPostResult(
        channel_id="C0ACUHRP6B1", ts="1774646400.000100"
    )

    result = devin_session_feedback_followup(
        thread_url="https://airbytehq-team.slack.com/archives/C0ACUHRP6B1/p1773062711122019",
        message="Triage report",
        agent_session_url="https://app.devin.ai/sessions/test123",
    )
    assert result.success is True
    assert result.reply_ts == "1774646400.000100"
    assert "C0ACUHRP6B1" in result.message

    # Verify the message was wrapped with disclaimer
    call_kwargs = mock_post.call_args.kwargs
    assert "Automated Triage Update" in call_kwargs["message"]
    assert "not monitored by Devin" in call_kwargs["message"]
