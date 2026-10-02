# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for Slack feedback posting and triage dispatch."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
import requests

from airbyte_ops_mcp.github_actions import WorkflowDispatchResult
from airbyte_ops_mcp.mcp.devin_ops import (
    _FOLLOWUP_HEADER,
    _build_feedback_body,
    _dispatch_triage_workflow,
    _linear_issue_key,
    _post_feedback_report,
    _wrap_followup_message,
    devin_session_feedback,
    devin_session_feedback_followup,
)
from airbyte_ops_mcp.slack_api import SlackAPIError, SlackURLParseError
from airbyte_ops_mcp.slack_posting import SlackPostResult, parse_slack_thread_url

THREAD_URL = "https://airbytehq-team.slack.com/archives/C0ACUHRP6B1/p1773062711122019"
ISSUE_URL = "https://linear.app/airbyteio/issue/HYD-123"


@pytest.mark.unit
@pytest.mark.parametrize(
    ("issue_url", "issue_id", "expected"),
    [
        pytest.param(ISSUE_URL, "issue-uuid", "HYD-123", id="bare_issue_url"),
        pytest.param(
            f"{ISSUE_URL}/check-stream-regression",
            "issue-uuid",
            "HYD-123",
            id="issue_url_with_slug",
        ),
        pytest.param(
            "https://linear.app/airbyteio/team/HYD/all",
            "issue-uuid",
            "issue-uuid",
            id="non_issue_url_falls_back_to_uuid",
        ),
        pytest.param(None, "issue-uuid", "issue-uuid", id="no_url"),
        pytest.param(None, None, None, id="nothing_supplied"),
    ],
)
def test_linear_issue_key(
    issue_url: str | None, issue_id: str | None, expected: str | None
) -> None:
    assert _linear_issue_key(issue_url, issue_id) == expected


@pytest.mark.unit
@pytest.mark.parametrize(
    "url,expected_channel,expected_ts",
    [
        pytest.param(THREAD_URL, "C0ACUHRP6B1", "1773062711.122019"),
        pytest.param(
            f"{THREAD_URL}?thread_ts=1773062700.000001&cid=C0ACUHRP6B1",
            "C0ACUHRP6B1",
            "1773062711.122019",
        ),
        pytest.param(
            "https://airbytehq-team.slack.com/archives/C0ACUHRP6B1/p1773062711",
            "C0ACUHRP6B1",
            "1773062711",
        ),
    ],
)
def test_parse_slack_thread_url_valid(
    url: str, expected_channel: str, expected_ts: str
) -> None:
    assert parse_slack_thread_url(url) == (expected_channel, expected_ts)


@pytest.mark.unit
@pytest.mark.parametrize(
    "url,expected_error",
    [
        ("https://example.com/not-a-slack-url", "Invalid Slack thread URL"),
        (
            "https://other-workspace.slack.com/archives/C0ACUHRP6B1/p1773062711122019",
            "Unexpected Slack workspace",
        ),
        ("not-even-a-url", "Invalid Slack thread URL"),
        (
            "https://airbytehq-team.slack.com/archives/C0ACUHRP6B1",
            "Invalid Slack thread URL",
        ),
    ],
)
def test_parse_slack_thread_url_invalid(url: str, expected_error: str) -> None:
    with pytest.raises(SlackURLParseError, match=expected_error):
        parse_slack_thread_url(url)


@pytest.mark.unit
def test_build_feedback_body_renders_context_and_missing_session() -> None:
    result = _build_feedback_body(
        feedback_type="negative",
        category="tool_failure",
        task_description="Triage a Devin session",
        session_playbook="devin_feedback_triage",
        related_skill_name="delete-declarative-source-def",
        expected_behavior="The session follows the playbook.",
        observed_behavior="The session omitted the context.",
        what_went_well=None,
        severity="medium",
        steps_to_reproduce=None,
    )

    assert "*Category:* Tool Failure" in result
    assert "*Session link missing:*" in result
    assert "devin_feedback_triage" in result
    assert "delete-declarative-source-def" in result


@pytest.mark.unit
def test_build_feedback_body_renders_playbook_and_skill_links() -> None:
    result = _build_feedback_body(
        feedback_type="negative",
        category="missing_guidance",
        task_description="Triage a Devin session",
        session_playbook="devin_feedback_triage",
        related_skill_name="delete-declarative-source-def",
        expected_behavior="The session follows the feedback playbook.",
        observed_behavior="The session omitted the playbook context.",
        what_went_well=None,
        severity=None,
        steps_to_reproduce=None,
        session_to_evaluate="https://app.devin.ai/sessions/target",
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
def test_devin_session_feedback_rejects_invalid_context_ids() -> None:
    result = devin_session_feedback(
        feedback_type="negative",
        category="tool_failure",
        task_description="Triage a Devin session",
        agent_session_url="https://app.devin.ai/sessions/test123",
        reporting_user="reporter@airbyte.io",
        session_playbook="invalid playbook",
        related_skill_name=None,
        expected_behavior="It works.",
        observed_behavior="It fails.",
    )

    assert result.success is False
    assert "session_playbook must be" in result.message


@pytest.mark.unit
def test_build_feedback_body_omits_missing_session_note_when_present() -> None:
    result = _build_feedback_body(
        feedback_type="negative",
        category="tool_failure",
        task_description="Triage a Devin session",
        session_playbook="none",
        related_skill_name=None,
        expected_behavior="It works.",
        observed_behavior="It fails.",
        what_went_well=None,
        severity=None,
        steps_to_reproduce=None,
        session_to_evaluate="https://app.devin.ai/sessions/target",
        thread_url=THREAD_URL,
    )

    assert "*Session link missing:*" not in result
    assert f"*Originating thread:* <{THREAD_URL}|Slack thread>" in result


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.devin_ops.trigger_workflow_dispatch")
@patch("airbyte_ops_mcp.mcp.devin_ops.resolve_ci_trigger_github_token")
def test_dispatch_triage_workflow_forwards_ticket(
    mock_token: MagicMock, mock_dispatch: MagicMock
) -> None:
    mock_token.return_value = "fake-token"
    mock_dispatch.return_value = WorkflowDispatchResult(
        workflow_url="https://github.com/airbytehq/airbyte-ops-mcp/actions/workflows/"
        "devin-session-triage.yml",
    )

    _dispatch_triage_workflow(
        session_url="https://app.devin.ai/sessions/target",
        feedback_context="feedback",
        reporting_user="reporter@airbyte.io",
        session_playbook="none",
        linear_issue_url=ISSUE_URL,
        linear_issue_id="issue-uuid",
        thread_url=THREAD_URL,
    )

    inputs = mock_dispatch.call_args.kwargs["inputs"]
    assert inputs["session_playbook"] == "none"
    assert inputs["linear_issue_id"] == "issue-uuid"
    assert inputs["linear_issue_url"] == ISSUE_URL
    assert inputs["thread_url"] == THREAD_URL


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.devin_ops.trigger_workflow_dispatch")
@patch("airbyte_ops_mcp.mcp.devin_ops.resolve_ci_trigger_github_token")
def test_dispatch_omits_ticket_url_when_absent(
    mock_token: MagicMock, mock_dispatch: MagicMock
) -> None:
    mock_token.return_value = "fake-token"
    mock_dispatch.return_value = WorkflowDispatchResult(
        workflow_url="https://github.com/airbytehq/airbyte-ops-mcp/actions/workflows/"
        "devin-session-triage.yml",
    )

    _dispatch_triage_workflow(
        session_url="https://app.devin.ai/sessions/target",
        feedback_context="feedback",
        reporting_user="reporter@airbyte.io",
        session_playbook="none",
        linear_issue_id="issue-uuid",
    )

    inputs = mock_dispatch.call_args.kwargs["inputs"]
    assert inputs["linear_issue_id"] == "issue-uuid"
    assert "linear_issue_url" not in inputs


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.devin_ops.post_channel_message")
def test_feedback_report_posts_top_level_without_thread(mock_post: MagicMock) -> None:
    mock_post.return_value = SlackPostResult(
        channel_id="C0ACUHRP6B1",
        ts="1774646400.000100",
    )

    assert _post_feedback_report("feedback") == (
        "https://airbytehq-team.slack.com/archives/C0ACUHRP6B1/p1774646400000100"
    )
    mock_post.assert_called_once_with("C0ACUHRP6B1", "feedback")


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.devin_ops.send_hitl_notification")
def test_feedback_report_tags_reporter_without_thread(mock_send: MagicMock) -> None:
    mock_send.return_value = SlackPostResult(
        channel_id="C0ACUHRP6B1",
        ts="1774646400.000100",
    )

    _post_feedback_report(
        "feedback",
        target_person="reporter@airbyte.io",
        cc_persons=["S0BJ4K3LC4X"],
        issue_url=ISSUE_URL,
        header_emoji=":warning:",
        header_label="Devin Session Feedback (Negative)",
    )

    notification = mock_send.call_args.kwargs
    assert notification["target_person"] == "reporter@airbyte.io"
    assert notification["cc_persons"] == ["S0BJ4K3LC4X"]
    assert notification["issue_url"] == ISSUE_URL
    assert notification["channel_override"] == "C0ACUHRP6B1"
    assert notification["thread_ts"] is None


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.devin_ops.send_hitl_notification")
def test_feedback_report_tags_reporter_in_source_thread(mock_send: MagicMock) -> None:
    mock_send.return_value = SlackPostResult(
        channel_id="C0ACUHRP6B1",
        ts="1774646400.000100",
    )

    _post_feedback_report(
        "feedback",
        THREAD_URL,
        target_person="reporter@airbyte.io",
        cc_persons=["S0BJ4K3LC4X"],
        issue_url=ISSUE_URL,
    )

    notification = mock_send.call_args.kwargs
    assert notification["channel_override"] == "C0ACUHRP6B1"
    assert notification["thread_ts"] == "1773062711.122019"


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.devin_ops.post_thread_reply")
def test_feedback_report_replies_to_source_thread(mock_post: MagicMock) -> None:
    mock_post.return_value = SlackPostResult(
        channel_id="C0ACUHRP6B1",
        ts="1774646400.000100",
    )

    assert _post_feedback_report("feedback", THREAD_URL) == (
        "https://airbytehq-team.slack.com/archives/C0ACUHRP6B1/p1774646400000100"
    )
    mock_post.assert_called_once_with(
        channel_id="C0ACUHRP6B1",
        thread_ts="1773062711.122019",
        message="feedback",
    )


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.devin_ops.post_channel_message")
@patch("airbyte_ops_mcp.mcp.devin_ops.send_hitl_notification")
def test_rich_channel_notification_falls_back_to_plain_text(
    mock_send: MagicMock,
    mock_post: MagicMock,
) -> None:
    mock_send.side_effect = SlackAPIError("roster lookup failed")
    mock_post.return_value = SlackPostResult(
        channel_id="C0ACUHRP6B1",
        ts="1774646400.000100",
    )

    _post_feedback_report("feedback", target_person="reporter@airbyte.io")

    mock_post.assert_called_once_with("C0ACUHRP6B1", "feedback")


def _negative_feedback_kwargs() -> dict[str, object]:
    return {
        "feedback_type": "negative",
        "category": "tool_failure",
        "task_description": "Bump a connector version",
        "reporting_user": "reporter@airbyte.io",
        "session_playbook": "none",
        "related_skill_name": None,
        "expected_behavior": "The tool bumps the version.",
        "observed_behavior": "The tool errored.",
        "what_went_well": None,
        "severity": None,
        "steps_to_reproduce": None,
    }


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.devin_ops._dispatch_triage_workflow")
def test_negative_feedback_with_ticket_dispatches_and_uses_exact_url(
    mock_dispatch: MagicMock,
) -> None:
    mock_dispatch.return_value = WorkflowDispatchResult(
        workflow_url="https://github.com/airbytehq/airbyte-ops-mcp/actions/workflows/"
        "devin-session-triage.yml",
    )

    result = devin_session_feedback(
        **_negative_feedback_kwargs(),
        agent_session_url="https://app.devin.ai/sessions/reporter",
        session_to_evaluate=None,
        linear_issue_id="issue-uuid",
        linear_issue_url=ISSUE_URL,
    )

    assert result.success is True
    assert result.linear_issue_identifier == "HYD-123"
    assert result.linear_issue_url == ISSUE_URL
    dispatch_kwargs = mock_dispatch.call_args.kwargs
    assert dispatch_kwargs["linear_issue_id"] == "issue-uuid"
    assert dispatch_kwargs["linear_issue_url"] == ISSUE_URL
    assert f"<{ISSUE_URL}|HYD-123>" not in dispatch_kwargs["feedback_context"]
    assert dispatch_kwargs["session_url"] == "https://app.devin.ai/sessions/reporter"


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.devin_ops._dispatch_triage_workflow")
def test_feedback_area_routes_cc_to_db_sources_owner(
    mock_dispatch: MagicMock,
) -> None:
    mock_dispatch.return_value = WorkflowDispatchResult(
        workflow_url="https://github.com/airbytehq/airbyte-ops-mcp/actions/workflows/"
        "devin-session-triage.yml",
    )

    result = devin_session_feedback(
        **_negative_feedback_kwargs(),
        agent_session_url="https://app.devin.ai/sessions/reporter",
        session_to_evaluate=None,
        linear_issue_id="issue-uuid",
        linear_issue_url=ISSUE_URL,
        feedback_area="db_sources",
    )

    assert result.success is True
    cc = mock_dispatch.call_args.kwargs["cc_persons"].split(",")
    assert cc == ["U098P1QAELQ", "S0BKR63VAN5"]
    assert "S0BJ4K3LC4X" not in cc

    mock_dispatch.reset_mock()
    result = devin_session_feedback(
        **_negative_feedback_kwargs(),
        agent_session_url="https://app.devin.ai/sessions/reporter",
        session_to_evaluate=None,
        linear_issue_id="issue-uuid",
        linear_issue_url=ISSUE_URL,
    )

    assert result.success is True
    cc = mock_dispatch.call_args.kwargs["cc_persons"].split(",")
    assert cc == ["S0BJ4K3LC4X", "S0BKR63VAN5"]


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.devin_ops._post_feedback_report")
def test_feedback_area_routes_cc_on_post_only(
    mock_post: MagicMock,
) -> None:
    mock_post.return_value = "https://slack.example/db-sources"

    result = devin_session_feedback(
        **_negative_feedback_kwargs(),
        agent_session_url="https://app.devin.ai/sessions/reporter",
        session_to_evaluate=None,
        linear_issue_id="issue-uuid",
        linear_issue_url=ISSUE_URL,
        post_only=True,
        feedback_area="db_sources",
    )

    assert result.success is True
    mock_post.assert_called_once()
    assert mock_post.call_args.kwargs["cc_persons"] == [
        "U098P1QAELQ",
        "S0BKR63VAN5",
    ]


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.devin_ops.dispatch_escalation")
@patch("airbyte_ops_mcp.mcp.devin_ops._dispatch_triage_workflow")
def test_feedback_area_routes_cc_on_fallback_handoff(
    mock_dispatch: MagicMock, mock_escalation: MagicMock
) -> None:
    mock_dispatch.return_value = None
    mock_escalation.return_value = WorkflowDispatchResult(
        workflow_url="https://github.com/airbytehq/airbyte-ops-mcp/actions/workflows/"
        "human-in-the-loop.yml",
    )

    result = devin_session_feedback(
        **_negative_feedback_kwargs(),
        agent_session_url="https://app.devin.ai/sessions/reporter",
        session_to_evaluate=None,
        linear_issue_id="issue-uuid",
        linear_issue_url=ISSUE_URL,
        feedback_area="db_sources",
    )

    assert result.success is True
    mock_escalation.assert_called_once()
    assert mock_escalation.call_args.kwargs["cc"] == [
        "U098P1QAELQ",
        "S0BKR63VAN5",
    ]


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.devin_ops._dispatch_triage_workflow")
@patch("airbyte_ops_mcp.mcp.devin_ops._post_feedback_report")
def test_post_only_feedback_posts_without_dispatch(
    mock_post: MagicMock, mock_dispatch: MagicMock
) -> None:
    mock_post.return_value = "https://slack.example/repeat"

    result = devin_session_feedback(
        **_negative_feedback_kwargs(),
        agent_session_url="https://app.devin.ai/sessions/reporter",
        session_to_evaluate=None,
        linear_issue_id="issue-uuid",
        linear_issue_url=ISSUE_URL,
        post_only=True,
    )

    assert result.success is True
    assert "without dispatching triage" in result.message
    assert "No Linear ticket recorded" not in mock_post.call_args.args[0]
    assert "No Linear ticket recorded" not in result.message
    mock_post.assert_called_once()
    mock_dispatch.assert_not_called()
    assert len(mock_post.call_args.args) == 1


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.devin_ops._post_feedback_report")
def test_post_only_thread_feedback_posts_to_channel_then_thread(
    mock_post: MagicMock,
) -> None:
    mock_post.side_effect = [
        "https://slack.example/hydra-feedback",
        "https://slack.example/source-thread",
    ]

    result = devin_session_feedback(
        **_negative_feedback_kwargs(),
        agent_session_url="https://app.devin.ai/sessions/reporter",
        linear_issue_id="issue-uuid",
        linear_issue_url=ISSUE_URL,
        post_only=True,
        thread_url=THREAD_URL,
    )

    assert result.success is True
    assert (
        "Thread reply posted at https://slack.example/source-thread." in result.message
    )
    assert mock_post.call_count == 2
    assert len(mock_post.call_args_list[0].args) == 1
    assert mock_post.call_args_list[1].args[1] == THREAD_URL


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.devin_ops._post_feedback_report")
def test_post_only_thread_channel_failure_returns_failure(
    mock_post: MagicMock,
) -> None:
    mock_post.side_effect = SlackAPIError("channel post failed")

    result = devin_session_feedback(
        **_negative_feedback_kwargs(),
        agent_session_url="https://app.devin.ai/sessions/reporter",
        post_only=True,
        thread_url=THREAD_URL,
    )

    assert result.success is False
    assert "channel post failed" in result.message
    mock_post.assert_called_once()
    assert len(mock_post.call_args.args) == 1


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.devin_ops._dispatch_triage_workflow")
@patch("airbyte_ops_mcp.mcp.devin_ops.send_hitl_notification")
def test_untracked_thread_feedback_omits_linear_button(
    mock_send: MagicMock,
    mock_dispatch: MagicMock,
) -> None:
    mock_send.return_value = SlackPostResult(
        channel_id="C0ACUHRP6B1",
        ts="1774646400.000100",
    )
    mock_dispatch.return_value = WorkflowDispatchResult(
        workflow_url="https://github.com/airbytehq/airbyte-ops-mcp/actions/workflows/"
        "devin-session-triage.yml",
    )

    result = devin_session_feedback(
        **_negative_feedback_kwargs(),
        agent_session_url="https://app.devin.ai/sessions/reporter",
        post_only=True,
        thread_url=THREAD_URL,
    )

    assert result.success is True
    assert mock_send.call_count == 2
    channel_notification, thread_notification = (
        call.kwargs for call in mock_send.call_args_list
    )
    assert channel_notification["issue_url"] is None
    assert channel_notification["channel_override"] == "C0ACUHRP6B1"
    assert channel_notification["thread_ts"] is None
    assert thread_notification["issue_url"] is None
    assert thread_notification["channel_override"] == "C0ACUHRP6B1"
    assert thread_notification["thread_ts"] == "1773062711.122019"
    assert "No Linear ticket recorded" in thread_notification["message"]
    assert "No Linear ticket recorded" in result.message


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.devin_ops._post_feedback_report")
def test_untracked_negative_feedback_warns_in_post_and_response(
    mock_post: MagicMock,
) -> None:
    mock_post.return_value = "https://slack.example/untracked"

    result = devin_session_feedback(
        **_negative_feedback_kwargs(),
        agent_session_url="https://app.devin.ai/sessions/reporter",
        post_only=True,
    )

    assert result.success is True
    assert "No Linear ticket recorded" in mock_post.call_args.args[0]
    assert "not on the Linear list" in mock_post.call_args.args[0]
    assert "No Linear ticket recorded" in result.message
    assert "not on the Linear list" in result.message


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.devin_ops.dispatch_escalation")
@patch("airbyte_ops_mcp.mcp.devin_ops._dispatch_triage_workflow")
def test_fallback_handoff_preserves_tracking_issue(
    mock_dispatch: MagicMock, mock_escalation: MagicMock
) -> None:
    mock_dispatch.return_value = None
    mock_escalation.return_value = WorkflowDispatchResult(
        workflow_url="https://github.com/airbytehq/airbyte-ops-mcp/actions/workflows/"
        "human-in-the-loop.yml",
    )

    result = devin_session_feedback(
        **_negative_feedback_kwargs(),
        agent_session_url="https://app.devin.ai/sessions/reporter",
        session_to_evaluate=None,
        linear_issue_id="issue-uuid",
        linear_issue_url=ISSUE_URL,
    )

    assert result.success is True
    assert f"<{ISSUE_URL}|HYD-123>" in mock_escalation.call_args.kwargs["message"]


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.devin_ops._dispatch_triage_workflow")
@patch("airbyte_ops_mcp.mcp.devin_ops._post_feedback_report")
def test_thread_url_report_still_triages_agent_session(
    mock_post: MagicMock,
    mock_dispatch: MagicMock,
) -> None:
    mock_dispatch.return_value = WorkflowDispatchResult(
        workflow_url="https://github.com/airbytehq/airbyte-ops-mcp/actions/workflows/"
        "devin-session-triage.yml",
    )

    result = devin_session_feedback(
        **_negative_feedback_kwargs(),
        agent_session_url="https://app.devin.ai/sessions/filer",
        session_to_evaluate=None,
        thread_url=THREAD_URL,
    )

    assert result.success is True
    dispatch_kwargs = mock_dispatch.call_args.kwargs
    assert dispatch_kwargs["session_url"] == "https://app.devin.ai/sessions/filer"
    assert "Session link missing" not in dispatch_kwargs["feedback_context"]
    assert "Originating thread" in dispatch_kwargs["feedback_context"]
    assert dispatch_kwargs["thread_url"] == THREAD_URL
    mock_post.assert_called_once()
    assert mock_post.call_args.args[1] == THREAD_URL


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.devin_ops._dispatch_triage_workflow")
@patch("airbyte_ops_mcp.mcp.devin_ops._post_feedback_report")
def test_thread_post_failure_does_not_block_triage_dispatch(
    mock_post: MagicMock,
    mock_dispatch: MagicMock,
) -> None:
    mock_post.side_effect = SlackAPIError("thread reply failed")
    mock_dispatch.return_value = WorkflowDispatchResult(
        workflow_url="https://github.com/airbytehq/airbyte-ops-mcp/actions/workflows/"
        "devin-session-triage.yml",
    )

    result = devin_session_feedback(
        **_negative_feedback_kwargs(),
        agent_session_url="https://app.devin.ai/sessions/filer",
        session_to_evaluate=None,
        thread_url=THREAD_URL,
    )

    assert result.success is True
    assert "Posting to the originating thread failed: thread reply failed." in (
        result.message
    )
    mock_dispatch.assert_called_once()
    assert mock_dispatch.call_args.kwargs["thread_url"] == THREAD_URL


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.devin_ops._dispatch_triage_workflow")
@patch("airbyte_ops_mcp.mcp.devin_ops._post_feedback_report")
def test_thread_request_error_does_not_block_triage_dispatch(
    mock_post: MagicMock,
    mock_dispatch: MagicMock,
) -> None:
    mock_post.side_effect = requests.ConnectionError("boom")
    mock_dispatch.return_value = WorkflowDispatchResult(
        workflow_url="https://github.com/airbytehq/airbyte-ops-mcp/actions/workflows/"
        "devin-session-triage.yml",
    )

    result = devin_session_feedback(
        **_negative_feedback_kwargs(),
        agent_session_url="https://app.devin.ai/sessions/filer",
        session_to_evaluate=None,
        thread_url=THREAD_URL,
    )

    assert result.success is True
    assert "Posting to the originating thread failed: boom." in result.message
    mock_dispatch.assert_called_once()


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.devin_ops.dispatch_escalation")
@patch("airbyte_ops_mcp.mcp.devin_ops._dispatch_triage_workflow")
@patch("airbyte_ops_mcp.mcp.devin_ops._post_feedback_report")
def test_thread_report_is_followed_by_channel_fallback_when_dispatch_fails(
    mock_post: MagicMock,
    mock_dispatch: MagicMock,
    mock_escalation: MagicMock,
) -> None:
    mock_post.return_value = "https://slack.example/source-thread"
    mock_dispatch.return_value = None
    mock_escalation.return_value = WorkflowDispatchResult(
        workflow_url="https://github.com/airbytehq/airbyte-ops-mcp/actions/workflows/"
        "human-in-the-loop.yml",
    )

    result = devin_session_feedback(
        **_negative_feedback_kwargs(),
        agent_session_url="https://app.devin.ai/sessions/filer",
        session_to_evaluate=None,
        thread_url=THREAD_URL,
    )

    assert result.success is True
    assert (
        "Thread reply posted at https://slack.example/source-thread." in result.message
    )
    mock_post.assert_called_once()
    assert mock_post.call_args.args[1] == THREAD_URL
    mock_dispatch.assert_called_once()
    mock_escalation.assert_called_once()
    assert mock_escalation.call_args.kwargs["channel_override"] == "C0ACUHRP6B1"


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.devin_ops._dispatch_triage_workflow")
def test_session_to_evaluate_takes_precedence_over_agent_session(
    mock_dispatch: MagicMock,
) -> None:
    mock_dispatch.return_value = WorkflowDispatchResult(
        workflow_url="https://github.com/airbytehq/airbyte-ops-mcp/actions/workflows/"
        "devin-session-triage.yml",
    )

    result = devin_session_feedback(
        **_negative_feedback_kwargs(),
        agent_session_url="https://app.devin.ai/sessions/filer",
        session_to_evaluate="https://app.devin.ai/sessions/target",
    )

    assert result.success is True
    assert (
        mock_dispatch.call_args.kwargs["session_url"]
        == "https://app.devin.ai/sessions/target"
    )


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.devin_ops.dispatch_escalation")
def test_positive_feedback_does_not_call_linear_or_triage(
    mock_escalation: MagicMock,
) -> None:
    mock_escalation.return_value = WorkflowDispatchResult(
        workflow_url="https://github.com/airbytehq/airbyte-ops-mcp/actions/workflows/"
        "human-in-the-loop.yml",
    )

    result = devin_session_feedback(
        feedback_type="positive",
        category="great_results",
        task_description="Complete a repo task",
        agent_session_url="https://app.devin.ai/sessions/test123",
        reporting_user="reporter@airbyte.io",
        session_playbook="none",
        what_went_well="The task was completed quickly.",
    )

    assert result.success is True
    assert result.linear_issue_url is None
    mock_escalation.assert_called_once()


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.devin_ops.dispatch_escalation")
@patch("airbyte_ops_mcp.mcp.devin_ops._post_feedback_report")
def test_positive_thread_feedback_posts_to_thread_and_channel(
    mock_post: MagicMock,
    mock_escalation: MagicMock,
) -> None:
    mock_post.return_value = "https://slack.example/source-thread"
    mock_escalation.return_value = WorkflowDispatchResult(
        workflow_url="https://github.com/airbytehq/airbyte-ops-mcp/actions/workflows/"
        "human-in-the-loop.yml",
    )

    result = devin_session_feedback(
        feedback_type="positive",
        category="great_results",
        task_description="Complete a repo task",
        agent_session_url="https://app.devin.ai/sessions/test123",
        reporting_user="reporter@airbyte.io",
        session_playbook="none",
        what_went_well="The task was completed quickly.",
        thread_url=THREAD_URL,
    )

    assert result.success is True
    assert (
        "Thread reply posted at https://slack.example/source-thread." in result.message
    )
    mock_post.assert_called_once()
    assert mock_post.call_args.args[1] == THREAD_URL
    mock_escalation.assert_called_once()
    assert mock_escalation.call_args.kwargs["channel_override"] == "C0ACUHRP6B1"


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.devin_ops.dispatch_escalation")
@patch("airbyte_ops_mcp.mcp.devin_ops._post_feedback_report")
def test_positive_thread_feedback_escalation_uses_session_to_evaluate(
    mock_post: MagicMock,
    mock_escalation: MagicMock,
) -> None:
    mock_post.return_value = "https://slack.example/source-thread"
    mock_escalation.return_value = WorkflowDispatchResult(
        workflow_url="https://github.com/airbytehq/airbyte-ops-mcp/actions/workflows/"
        "human-in-the-loop.yml",
    )

    result = devin_session_feedback(
        feedback_type="positive",
        category="great_results",
        task_description="Complete a repo task",
        agent_session_url="https://app.devin.ai/sessions/filer",
        reporting_user="reporter@airbyte.io",
        session_playbook="none",
        what_went_well="The task was completed quickly.",
        session_to_evaluate="https://app.devin.ai/sessions/target",
        thread_url=THREAD_URL,
    )

    assert result.success is True
    mock_escalation.assert_called_once()
    assert (
        mock_escalation.call_args.kwargs["agent_session_url"]
        == "https://app.devin.ai/sessions/target"
    )


@pytest.mark.unit
def test_wrap_followup_message_structure() -> None:
    body = "Here are my triage findings."
    session_url = "https://app.devin.ai/sessions/test123"
    result = _wrap_followup_message(body, agent_session_url=session_url)

    assert result.startswith(_FOLLOWUP_HEADER)
    assert body in result
    assert f"<{session_url}|linked session>" in result
    assert "not monitored by Devin" in result


@pytest.mark.unit
def test_followup_tool_invalid_url() -> None:
    result = devin_session_feedback_followup(
        thread_url="https://example.com/not-slack",
        message="Triage report",
        agent_session_url="https://app.devin.ai/sessions/test123",
    )
    assert result.success is False
    assert "Invalid Slack thread URL" in result.message


@pytest.mark.unit
def test_followup_tool_wrong_workspace() -> None:
    result = devin_session_feedback_followup(
        thread_url=(
            "https://evil-workspace.slack.com/archives/C0ACUHRP6B1/p1773062711122019"
        ),
        message="Triage report",
        agent_session_url="https://app.devin.ai/sessions/test123",
    )
    assert result.success is False
    assert "Unexpected Slack workspace" in result.message


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.devin_ops.post_thread_reply")
def test_followup_tool_is_slack_only(mock_post: MagicMock) -> None:
    mock_post.return_value = SlackPostResult(
        channel_id="C0ACUHRP6B1", ts="1774646400.000100"
    )

    result = devin_session_feedback_followup(
        thread_url=THREAD_URL,
        message="Triage report",
        agent_session_url="https://app.devin.ai/sessions/test123",
    )

    assert result.success is True
    assert result.reply_ts == "1774646400.000100"
    mock_post.assert_called_once()
